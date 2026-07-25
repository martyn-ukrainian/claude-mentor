# Трекер прогресу навчання

Самодостатня система: рахує **час** над проєктом по фазах і показує **прогрес** по
роадмапу як сторінку. Живе повністю всередині репозиторію — нічого глобального.

## Як воно влаштоване (3 частини)

```
   хук                     стан                     збірка
track-time.sh   ──►   events.jsonl  ─┐
(пише час)                            ├─►  build.py  ──►  report.html
                      state.json    ─┘   (агрегує)      (готова сторінка)
(веде AI/людина) ──►
```

1. **`track-time.sh`** — UserPromptSubmit-хук. На кожен твій промпт дописує один
   рядок у `events.jsonl`: час + поточна фаза (бере з файлу `current_phase`).
   Швидкий, без залежностей. Реєструється в `.claude/settings.json`.

2. **`events.jsonl`** — лог часу, по рядку на промпт: `{"ts","phase","session"}`.
   Append-only, runtime-дані (у `.gitignore`).

3. **`state.json`** — джерело правди про фази й прогрес уроків. Веде AI (з ROADMAP.md
   + PROGRESS.md) або редагуєш руками. Схема — див. нижче.

4. **`build.py`** — читає `state.json` + `events.jsonl`, рахує час (та сама логіка що
   в глобальному prompt-tracker: проміжок > 30 хв = пауза 60 с) і генерує самодостатню
   `report.html` (дані вшиті — відкривається як `file://`, без сервера). Заодно
   синхронізує `current_phase` для хука.

5. **`set-phase.sh phase-N`** — перемикач фази: оновлює `state.json` + `current_phase`
   одним викликом (з валідацією, що така фаза існує). Claude запускає його автоматично
   в момент переходу на нову фазу (правило в CLAUDE.md), можна й руками. Це важливо
   робити саме на межі фаз — інакше час до наступного `/progress` тегається старою фазою.

## Команди

- `/progress-init` — розгорнути з нуля (читає ROADMAP, будує `state.json`, ставить хук).
- `/progress` — оновити прогрес і перезібрати сторінку.

Вручну:
```bash
python3 .claude/progress/build.py            # перезібрати звіт
open .claude/progress/report.html            # відкрити
.claude/progress/set-phase.sh phase-3        # перейти на нову фазу
```

## `state.json`

```json
{
  "project": "ML Learning",
  "current_phase": "phase-2",
  "phases": [
    { "id": "phase-0", "name": "Фаза 0", "subtitle": "Python", "total": 7, "done": 7 }
  ]
}
```

- `total: null` — фаза ще не розписана на уроки → в лоадері показується як «не почато»,
  у відсоток прогресу входить як 0%.
- Загальний відсоток = середнє `done/total` по всіх фазах (кожна важить однаково).

## Бекфіл історії (одноразово)

Якщо є глобальний prompt-tracker — засіяти `events.jsonl` минулим часом проєкту,
конвертуючи UTC→localtime і тегуючи фази за датами:

**Тільки в порожній файл.** Скрипт перезаписує `events.jsonl` — повторний запуск,
коли хук уже назбирав історію, зітре її (а фази за захардкодженими датами для нових
подій будуть хибні). Тому обов'язковий guard на початку:

```python
import sqlite3, json, sys
from pathlib import Path
out = Path(".claude/progress/events.jsonl")
if out.exists():
    sys.exit("events.jsonl вже існує — бекфіл лише в порожній файл, інакше зітреш зібрану історію")
db = sqlite3.connect("/Users/martyn/.claude/prompt-tracker/prompts.db")
rows = db.execute("""SELECT datetime(timestamp,'localtime'), session_id FROM prompts
                     WHERE project_path LIKE '%MLLearning%' AND session_id<>''
                     ORDER BY timestamp""").fetchall()
def phase(ts):                      # межі фаз за датами — під свій проєкт
    d = ts[:10]
    return "phase-0" if d<="2026-07-13" else "phase-1" if d<="2026-07-18" else "phase-2"
with out.open("w") as f:
    for ts, sid in rows:
        f.write(json.dumps({"ts":ts.split(".")[0],"phase":phase(ts),"session":sid})+"\n")
```

Без бекфілу — трекер просто рахує з моменту встановлення.

## Перенести в інший проєкт

Скопіювати теку `.claude/progress/` + `.claude/settings.json`, додати `.gitignore`-винятки
(`!.claude/progress/`, `!.claude/settings.json`, і навпаки ігнор `events.jsonl`/`report.html`),
запустити `/progress-init`.
