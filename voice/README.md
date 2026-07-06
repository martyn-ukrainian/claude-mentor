# voice-agent

Локальний voice-interviewer на базі Pipecat. Витягнуто з `stacy/pipecat-cloud-server` — **без** pipecat-cloud, Daily, flows, RTVI-cache, Sentry, PostHog, Langfuse, S3, Redis, Postgres.

Залишено лише те, що потрібно для mock-інтерв'ю:

- **STT** — Deepgram (nova-3)
- **LLM** — OpenAI (gpt-4.1, temperature 0.4)
- **TTS** — Cartesia (sonic-3)
- **Transport** — `SmallWebRTCTransport` (P2P WebRTC між браузером і сервером через `aiortc` + STUN). **Нуль зовнішніх сервісів для transport.**
- **Transcript** — локально у `./transcripts/*.json` + `*.vtt`

## Старт

```bash
cp .env.example .env
# Додай: OPENAI_API_KEY, CARTESIA_API_KEY, DEEPGRAM_API_KEY
./start-local.sh
```

Відкриваєш [http://127.0.0.1:8000](http://127.0.0.1:8000) → дозволяєш мікрофон → кнопка "Почати інтерв'ю" → WebRTC встановлюється напряму з сервером, агент вітається і ставить перші питання.

**Нема Daily room, нема iframe, нема CDN-клієнта** — сирий WebRTC через Google STUN для NAT traversal.

## Кастомний промпт / голос

Прямо у веб-UI заповнюєш поля System prompt / Bot name / Voice ID і тиснеш Start. Параметри летять у тіло `POST /api/offer` як `request_data`.

## Endpoints

| Метод | Шлях | Призначення |
|---|---|---|
| `GET` | `/` | Веб-UI |
| `POST` | `/api/offer` | SDP offer → answer (стартує bot) |
| `PATCH` | `/api/offer` | ICE candidate trickle |
| `GET` | `/health` | healthcheck |
| `GET` | `/api/flows` | список flow-файлів з `flows/*.json` |
| `GET` | `/api/flows/{name}` | будує system prompt з flow через `build_prompt.py` |

## URL-параметри (zero-click launch)

```
http://127.0.0.1:8000/?flow=tech-ua_transformers_easy
http://127.0.0.1:8000/?flow=tech-ua_rag_medium&autostart=1
```

- `flow=X` — підтягує `flows/X.json`, будує system prompt і підставляє в textarea
- `autostart=1` — одразу клікає Start після завантаження flow

Готуєш закладки в браузері під кожен тип інтерв'ю — одне натискання і ти в сесії.

## Файли

| Файл | Що робить |
|---|---|
| `server.py` | FastAPI: WebRTC signaling (`/api/offer`), спавнить bot, віддає UI |
| `bot.py` | Pipecat pipeline: SmallWebRTCTransport → STT → LLM → TTS |
| `public/index.html` | Веб-UI з сирим RTCPeerConnection, нуль залежностей |
| `transcript.py` | Збирач транскрипту (JSON + VTT) |
| `pyproject.toml` | Залежності (pipecat-ai[webrtc], fastapi, uvicorn) |
| `.env.example` | API ключі |

## Що НЕ переносив зі stacy

- `pipecatcloud` + Daily — транспорт тепер `SmallWebRTCTransport`, нуль зовнішніх сервісів для transport
- `pipecat-flows` + `flow_handlers.py` + `premade_flows/` — для інтерв'ю досить простого system prompt
- `pipecat_posthog/`, `sentry_sdk`, Langfuse — аналітика не потрібна
- `tts_cache_simple/` (PostgreSQL + S3 кеш) — для mock-сесій зайве
- `api_client.py`, `state_persistence.py`, `s3_utils.py`, `ear_logs.py` — все зав'язане на backend stacy
- `local_recording.py` — можна додати пізніше через audio buffer processor
- `quickjs_handler.py`, `us_zips.py` — специфіка Stacy-продукту
- AssemblyAI fallback — достатньо Deepgram

Якщо знадобиться щось з цього — додаси точково.

## NAT / сторонні сітки

Якщо тестуєш на одному компі (браузер + сервер на localhost) — ICE нічого не треба, з'єднається напряму. Якщо потім захочеш зовнішній доступ (інший комп, мобілка) — додасть TURN-сервер у `iceServers` в `server.py` і `public/index.html`. Google STUN уже стоїть для NAT discovery.

## Flow-файли

Mock-інтерв'ю структуровані через JSON-файли в `flows/`. Формат імені: `{mode}_{topic}_{difficulty}.json`.

**Приклади імен:**
- `tech-ua_rag_medium.json`
- `tech-en_system-design-voice-ai_hard.json`
- `english-conversation_music_intermediate.json`
- `english-tutor_conditionals_easy.json`

**Структура файлу:**

```json
{
  "mode": "tech-ua",
  "topic": "rag",
  "difficulty": "medium",
  "duration_min": 30,
  "language": "uk",
  "interviewer_persona": "hiring_manager_winwin",
  "opening": "Привіт. Я сьогодні твій інтерв'юер...",
  "questions": [
    {
      "id": "q1",
      "text": "Поясни різницю між dense і sparse retrieval",
      "follow_ups": [
        "А коли б ти використав hybrid?",
        "Які tradeoffs у reranking-моделі поверх hybrid?"
      ],
      "time_budget_sec": 180,
      "evaluation_criteria": [
        "Правильне пояснення BM25 vs embeddings",
        "Розуміння precision vs recall tradeoff"
      ],
      "red_flags": [
        "Плутає embeddings з tokenization",
        "Не знає що таке BM25"
      ],
      "strong_markers": [
        "Згадує hybrid з reciprocal rank fusion",
        "Розуміє коли cross-encoder vs bi-encoder"
      ]
    }
  ],
  "wrap_up": "Дякую. Маєш 5 хв на питання до мене."
}
```

**Як підхоплюються:** сервер читає `system_prompt` при старті; flow-файл треба передати як частину system prompt або через окремий параметр (TODO — інтеграція з `server.py`, поки що можна копіювати opening+questions у `system_prompt` вручну).

**Lifecycle:** після використання — застарілий, генеруй новий для того ж topic. Старі flows кладуться у `flows/archive/` через місяць (не видаляти).

Детальний runbook як Claude має запускати mock — у `../SYSTEM_PROMPT.md` секція "Voice Interview Runbook".
