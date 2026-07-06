"""
Voice-agent pipeline на SmallWebRTCTransport (pipecat-ai[webrtc]).
Нуль зовнішніх сервісів окрім OpenAI/Cartesia/Deepgram — WebRTC peer-to-peer.
"""

import os
import uuid
from datetime import datetime, timezone

from dotenv import load_dotenv
from loguru import logger

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.processors.transcript_processor import TranscriptProcessor
from deepgram import LiveOptions

from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transcriptions.language import Language

import transcript_stream
from pipecat.transports.base_transport import TransportParams
from pipecat.transports.smallwebrtc.transport import SmallWebRTCTransport

from transcript import TranscriptCollector

load_dotenv()

DEFAULT_VOICE_ID = "05ffab9c-d380-4909-8375-cd12f59238c3"
DEFAULT_SYSTEM_PROMPT = (
    "Ти — голосовий помічник для ML Learning. Користувач запустив сесію "
    "без flow-файлу. Привітайся українською, коротко спитай яку тему "
    "хоче обговорити, і скажи що для повноцінної сесії краще запустити "
    "з flow: './launch.sh <flow-name>'."
)


async def run_bot(
    webrtc_connection,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    voice_id: str = DEFAULT_VOICE_ID,
    bot_name: str = "Interviewer",
    session_id: str | None = None,
    transcript_dir: str = "./transcripts",
    language_mode: str = "uk",
):
    session_id = session_id or str(uuid.uuid4())
    logger.info(f"Starting bot session {session_id} [lang={language_mode}]")

    transport = SmallWebRTCTransport(
        webrtc_connection=webrtc_connection,
        params=TransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            audio_out_10ms_chunks=2,
            vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.5)),
        ),
    )

    if language_mode == "multi":
        stt_opts = LiveOptions(
            model="nova-3",
            language="multi",
            smart_format=True,
            punctuate=True,
            interim_results=True,
            encoding="linear16",
            channels=1,
            sample_rate=16000,
        )
        tts_params = CartesiaTTSService.InputParams()  # sonic-3 auto-detects
        lang_instruction = (
            "ВАЖЛИВО: відповідай тією ж мовою, якою щойно говорив користувач "
            "(автоматично switch між українською і англійською)."
        )
    else:
        stt_opts = LiveOptions(
            model="nova-2-general",
            language=Language.UK.value,
            smart_format=True,
            punctuate=True,
            interim_results=True,
            encoding="linear16",
            channels=1,
            sample_rate=16000,
        )
        tts_params = CartesiaTTSService.InputParams(language=Language.UK)
        lang_instruction = "Розмовляй українською."

    stt = DeepgramSTTService(
        api_key=os.environ["DEEPGRAM_API_KEY"],
        audio_passthrough=True,
        live_options=stt_opts,
    )

    llm = OpenAILLMService(
        api_key=os.environ["OPENAI_API_KEY"],
        model=os.getenv("OPENAI_MODEL", "gpt-4.1"),
        params=OpenAILLMService.InputParams(temperature=0.4),
    )

    tts = CartesiaTTSService(
        api_key=os.environ["CARTESIA_API_KEY"],
        voice_id=voice_id,
        model="sonic-3",
        params=tts_params,
    )

    context = OpenAILLMContext(
        messages=[
            {"role": "system", "content": f"{system_prompt}\n\n{lang_instruction}"},
            {
                "role": "user",
                "content": "Привіт, я готовий. Почни mock-інтерв'ю коротким вітанням і першим питанням.",
            },
        ],
    )
    context_aggregator = llm.create_context_aggregator(context)

    transcript_proc = TranscriptProcessor()
    collector = TranscriptCollector(session_id, out_dir=transcript_dir)
    collector.start_session(datetime.now(timezone.utc))

    pipeline = Pipeline(
        [
            transport.input(),
            stt,
            transcript_proc.user(),
            context_aggregator.user(),
            llm,
            tts,
            transport.output(),
            transcript_proc.assistant(),
            context_aggregator.assistant(),
        ]
    )

    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            allow_interruptions=True,
            enable_metrics=True,
            enable_usage_metrics=True,
            report_only_initial_ttfb=True,
        ),
    )

    @transcript_proc.event_handler("on_transcript_update")
    async def _on_transcript(_proc, frame):
        for msg in frame.messages:
            collector.add_utterance(msg.role, msg.content)
            logger.info(f"[{msg.role}] {msg.content}")
            await transcript_stream.publish(
                session_id, {"role": msg.role, "text": msg.content}
            )

    @transport.event_handler("on_client_connected")
    async def _on_connected(_t, _client):
        logger.info(f"Client connected to {bot_name}, starting conversation")
        await task.queue_frames([LLMRunFrame()])

    @transport.event_handler("on_client_disconnected")
    async def _on_disconnected(_t, _client):
        logger.info("Client disconnected, finalizing")
        collector.save()
        await task.cancel()

    runner = PipelineRunner(handle_sigint=False)
    try:
        await runner.run(task)
    finally:
        collector.save()
        logger.info(f"Session {session_id} ended")
