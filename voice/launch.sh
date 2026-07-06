#!/usr/bin/env bash
# Launcher для voice-claude — стартує сервер (якщо треба), відкриває браузер
# з flow і session_id, і стрімить транскрипт у log-файл для Claude Code.
#
# Використання:
#   ./launch.sh <flow-name> [session-id]
#   ./launch.sh tutor-ua_biological-neurons_medium
#   ./launch.sh tutor-ua_biological-neurons_medium mytest
#
# Після запуску Claude Code читає:
#   /tmp/voice-claude-<session-id>.log

set -e
cd "$(dirname "$0")"

FLOW="${1:?Usage: $0 <flow-name> [session-id]}"
SID="${2:-live-$(date +%Y%m%d-%H%M%S)}"
BASE="http://127.0.0.1:8000"
LOG="/tmp/voice-claude-${SID}.log"

# 1. Сервер запущений?
if ! curl -sf "$BASE/health" >/dev/null 2>&1; then
  echo "🚀 Стартую сервер у фоні (лог: /tmp/voice-claude-server.log)"
  nohup uv run python server.py >/tmp/voice-claude-server.log 2>&1 &
  echo "PID: $!"
  # чекаємо на health (перший старт ~45с через lazy Pipecat imports)
  for i in {1..90}; do
    if curl -sf "$BASE/health" >/dev/null 2>&1; then break; fi
    sleep 1
  done
  if ! curl -sf "$BASE/health" >/dev/null 2>&1; then
    echo "❌ Сервер не стартував за 90с. Дивись /tmp/voice-claude-server.log"
    exit 1
  fi
fi
echo "✅ Сервер живий"

# 2. Flow існує?
if ! curl -sf "$BASE/api/flows/$FLOW" >/dev/null 2>&1; then
  echo "❌ Flow '$FLOW' не знайдено. Доступні:"
  curl -s "$BASE/api/flows" | python3 -c "import json,sys;print('\n'.join(json.load(sys.stdin)['flows']))"
  exit 1
fi
echo "✅ Flow '$FLOW' є"

# 3. Стартуємо SSE-стрім у фоні
echo "📡 Підписуюсь на SSE → $LOG"
: > "$LOG"
nohup curl -sN "$BASE/api/stream/$SID" >>"$LOG" 2>&1 &
SSE_PID=$!
echo "SSE PID: $SSE_PID"

# 4. Відкриваємо браузер
URL="$BASE/?flow=$FLOW&session=$SID&autostart=1"
echo "🌐 Відкриваю: $URL"
open "$URL"

echo ""
echo "───────────────────────────────────────────"
echo "Session ID: $SID"
echo "Transcript log: $LOG"
echo "SSE PID: $SSE_PID (kill $SSE_PID щоб відписатись)"
echo "───────────────────────────────────────────"
