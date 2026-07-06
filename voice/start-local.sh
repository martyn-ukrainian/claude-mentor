#!/bin/bash
set -e

cd "$(dirname "$0")"

if ! command -v uv &> /dev/null; then
  echo "❌ uv не встановлено. curl -LsSf https://astral.sh/uv/install.sh | sh"
  exit 1
fi

if [ ! -f ".env" ]; then
  echo "⚠️  .env не знайдено — копіюю .env.example"
  cp .env.example .env
  echo "   → Додай API ключі в .env і перезапусти"
  exit 1
fi

echo "📦 uv sync..."
uv sync

echo "🚀 http://127.0.0.1:8000 — відкривай в браузері"
echo ""
uv run python server.py
