#!/bin/bash
# ML Learning — трекер часу по фазах.
# UserPromptSubmit-хук: на кожен промпт дописує рядок у events.jsonl,
# тегований поточною фазою (з файлу current_phase).
# Мінімальний і швидкий — жодних залежностей окрім python3 для парсингу session_id.

DIR="$(cd "$(dirname "$0")" && pwd)"
EVENTS="$DIR/events.jsonl"
PHASE_FILE="$DIR/current_phase"

INPUT=$(cat)

# session_id зі stdin (для коректного розбиття на сесії при підрахунку)
SESSION=$(printf '%s' "$INPUT" | /usr/bin/python3 -c "
import sys, json
try: print(json.load(sys.stdin).get('session_id',''))
except: pass
" 2>/dev/null)

PHASE="unknown"
[ -f "$PHASE_FILE" ] && PHASE=$(tr -d '[:space:]' < "$PHASE_FILE")

TS=$(date '+%Y-%m-%d %H:%M:%S')

printf '{"ts":"%s","phase":"%s","session":"%s"}\n' "$TS" "$PHASE" "$SESSION" >> "$EVENTS"

exit 0
