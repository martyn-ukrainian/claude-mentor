"""
Локальний FastAPI сервер з WebRTC signaling (SmallWebRTCTransport).
Нуль зовнішніх сервісів для transport — браузер ↔ сервер напряму через aiortc.
"""

import asyncio
import json
import os
import sys
import uuid
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

import transcript_stream

from pipecat.transports.smallwebrtc.connection import IceServer
from pipecat.transports.smallwebrtc.request_handler import (
    ConnectionMode,
    SmallWebRTCPatchRequest,
    SmallWebRTCRequest,
    SmallWebRTCRequestHandler,
)

from bot import DEFAULT_SYSTEM_PROMPT, DEFAULT_VOICE_ID, run_bot
from build_prompt import build_prompt

load_dotenv()

BOT_DIR = Path(__file__).parent.resolve()
PUBLIC_DIR = BOT_DIR / "public"
FLOWS_DIR = BOT_DIR / "flows"

app = FastAPI(title="Voice Agent (local WebRTC)", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if PUBLIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=PUBLIC_DIR), name="static")

ice_servers = [IceServer(urls="stun:stun.l.google.com:19302")]
webrtc_handler = SmallWebRTCRequestHandler(
    ice_servers=ice_servers,
    connection_mode=ConnectionMode.MULTIPLE,
)


@app.get("/")
async def index():
    return FileResponse(PUBLIC_DIR / "index.html")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/flows")
async def list_flows():
    if not FLOWS_DIR.exists():
        return {"flows": []}
    return {
        "flows": sorted(
            p.stem for p in FLOWS_DIR.glob("*.json") if not p.stem.startswith(".")
        )
    }


@app.get("/api/flows/{name}")
async def get_flow_prompt(name: str):
    from fastapi import HTTPException

    if "/" in name or ".." in name:
        raise HTTPException(400, "invalid flow name")
    path = FLOWS_DIR / f"{name}.json"
    if not path.exists():
        raise HTTPException(404, f"flow '{name}' not found")
    return {"name": name, "system_prompt": build_prompt(str(path))}


@app.get("/api/stream/{session_id}")
async def stream_transcript(session_id: str):
    q = transcript_stream.subscribe(session_id)

    async def gen():
        try:
            yield 'data: {"role":"system","text":"stream connected"}\n\n'
            while True:
                try:
                    event = await asyncio.wait_for(q.get(), timeout=15)
                    yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
        finally:
            transcript_stream.unsubscribe(session_id, q)

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.post("/api/offer")
async def offer(payload: dict):
    """SDP offer — стартує bot, повертає answer (sdp + pc_id)."""
    request = SmallWebRTCRequest.from_dict(
        {k: v for k, v in payload.items() if k in {"sdp", "type", "pc_id", "restart_pc", "request_data"}}
    )
    request_data = payload.get("request_data") or {}
    session_id = request_data.get("session_id") or str(uuid.uuid4())

    async def on_new_connection(pipecat_connection):
        logger.info(f"New WebRTC connection → spawning bot [session={session_id[:8]}]")
        asyncio.create_task(
            run_bot(
                webrtc_connection=pipecat_connection,
                system_prompt=request_data.get("system_prompt") or DEFAULT_SYSTEM_PROMPT,
                voice_id=request_data.get("voice_id") or DEFAULT_VOICE_ID,
                bot_name=request_data.get("bot_name") or "Interviewer",
                session_id=session_id,
                language_mode=request_data.get("language_mode") or "uk",
            )
        )

    answer = await webrtc_handler.handle_web_request(request, on_new_connection)
    if answer is not None:
        answer["session_id"] = session_id
    return answer


@app.patch("/api/offer")
async def offer_patch(payload: dict):
    """ICE candidate patches."""
    request = SmallWebRTCPatchRequest(
        pc_id=payload["pc_id"],
        candidates=payload.get("candidates", []),
    )
    # Coerce dicts to IceCandidate if needed
    from pipecat.transports.smallwebrtc.request_handler import IceCandidate

    request.candidates = [
        c if isinstance(c, IceCandidate) else IceCandidate(**c) for c in request.candidates
    ]
    await webrtc_handler.handle_patch_request(request)
    return {"ok": True}


@app.on_event("shutdown")
async def _shutdown():
    await webrtc_handler.close()


def main():
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <7}</level> | {message}",
        level="INFO",
    )
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    logger.info(f"Voice agent server → http://{host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
