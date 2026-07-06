"""In-memory pub/sub для live-транскрипту через SSE."""

import asyncio
from collections import defaultdict

_queues: dict[str, list[asyncio.Queue]] = defaultdict(list)


def subscribe(session_id: str) -> asyncio.Queue:
    q: asyncio.Queue = asyncio.Queue()
    _queues[session_id].append(q)
    return q


def unsubscribe(session_id: str, q: asyncio.Queue):
    subs = _queues.get(session_id)
    if not subs:
        return
    try:
        subs.remove(q)
    except ValueError:
        pass
    if not subs:
        _queues.pop(session_id, None)


async def publish(session_id: str, event: dict):
    for q in list(_queues.get(session_id, [])):
        await q.put(event)
