# MLLearning

**A public learning system with a voice agent right in your terminal.**

Universal method for learning hard technical subjects with an AI mentor — currently applied to ML engineering, but the structure works for any field: Rust, Kubernetes, systems design, anything with depth.

## How it works

1. **Lesson** with Claude Code as mentor — hint ladders, no immediate solutions, you write the code
2. **10-min voice session** with an AI agent right in your terminal — you explain the topic out loud, the agent plays a curious beginner and catches your hand-waving
3. **Written lesson** in `docs/` in portfolio quality
4. **Calibrated memory** — `memories/profile.md` tracks *demonstrated* ability, not just topics covered

Reading and writing code isn't enough. Explaining out loud reveals what you're actually missing — the whole loop is designed to close that gap.

## What's inside

- **[ROADMAP.md](./ROADMAP.md)** — 7-phase plan (Python → Math → Classical ML → DL → LLM → MLOps → Portfolio)
- **[CLAUDE.md](./CLAUDE.md)** — mentor rules: hint ladders, Feynman check, spaced retrieval
- **[VOICE-TUTORIALS.md](./VOICE-TUTORIALS.md)** — voice agent method + setup + post-session review
- **[PROGRESS.md](./PROGRESS.md)** — where I am right now
- **[docs/](./docs/)** — completed lessons
- **[voice/](./voice/)** — self-hosted voice agent (Pipecat + WebRTC + Deepgram + Cartesia + Piper/Whisper)

## Adapt to your own topic

Fork it, replace `ROADMAP.md` with your subject, adjust rules in `CLAUDE.md`, add API keys to `voice/.env`, run. The scaffolding is the point.

## Demo

*Screenshot / video coming soon.*

---

Voice pipeline: [Pipecat](https://pipecat.ai) · [Deepgram](https://deepgram.com) · OpenAI · [Cartesia](https://cartesia.ai) · optional self-hosted [Piper](https://github.com/rhasspy/piper) + [Whisper](https://github.com/openai/whisper) for offline / private inference.
