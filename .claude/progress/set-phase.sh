#!/bin/bash
# ML Learning — перемикач поточної фази.
# Використання: set-phase.sh phase-N
# Оновлює одразу два місця: state.json (джерело правди) і current_phase
# (вказівник для хука track-time.sh). Викликається Claude'ом автоматично
# при переході на нову фазу (правило в CLAUDE.md) або руками.

DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -z "$1" ]; then
  echo "usage: set-phase.sh phase-N" >&2
  exit 1
fi

/usr/bin/python3 - "$1" "$DIR" <<'EOF'
import json, sys
from pathlib import Path

phase, d = sys.argv[1], Path(sys.argv[2])
state_path = d / "state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))

ids = [p["id"] for p in state["phases"]]
if phase not in ids:
    sys.exit(f"невідома фаза {phase!r} — у state.json є: {', '.join(ids)}")

state["current_phase"] = phase
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(d / "current_phase").write_text(phase + "\n", encoding="utf-8")
print(f"✓ поточна фаза: {phase}")
EOF
