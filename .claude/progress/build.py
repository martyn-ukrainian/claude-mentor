#!/usr/bin/env python3
"""ML Learning — генератор звіту прогресу.

Читає:
  state.json     — фази + прогрес уроків + вказівник поточної фази (веде AI)
  events.jsonl   — часовий лог (пише хук track-time.sh)

Пише:
  report.html    — самодостатня сторінка (дані вшиті, відкривається як file://)
  current_phase  — синхронізує вказівник для хука зі state.json

Підрахунок часу дзеркалить алгоритм prompt-tracker:
розбиваємо на сесії, у межах сесії проміжок між промптами > 30 хв
рахуємо як 60 с (пауза), інакше — фактичний проміжок; перший промпт сесії = 0.

Макет: чарт накопичених годин (X = календар, Y = сума годин) →
дві колонки: зліва роадмап-прогрес, справа таймлайн по днях.
"""
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

DIR = Path(__file__).resolve().parent
STATE = DIR / "state.json"
EVENTS = DIR / "events.jsonl"
REPORT = DIR / "report.html"
PHASE_PTR = DIR / "current_phase"

IDLE_CAP = 1800  # проміжок > 30 хв вважаємо паузою
PAUSE_SEC = 60   # і зараховуємо як 1 хв

WEEKDAYS = ["Понеділок", "Вівторок", "Середа", "Четвер", "П’ятниця", "Субота", "Неділя"]
MONTHS = ["січня", "лютого", "березня", "квітня", "травня", "червня",
          "липня", "серпня", "вересня", "жовтня", "листопада", "грудня"]

# Палітра по фазах (циклічна, якщо фаз більше) — узгоджена з дизайном сторінки.
PHASE_HUES = ["#3d7a6e", "#b8823a", "#5a55c9", "#b5544e", "#4d7ba6", "#8a6d3b", "#6a8a3b"]


def load_state():
    return json.loads(STATE.read_text(encoding="utf-8"))


def load_events():
    if not EVENTS.exists():
        return []
    out = []
    for line in EVENTS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
            rec["_ts"] = datetime.strptime(rec["ts"], "%Y-%m-%d %H:%M:%S")
            out.append(rec)
        except (ValueError, KeyError):
            continue
    return out


def aggregate(events):
    """Повертає (per_phase_sec, daily, series).

    daily  = [(date, weekday, sec, dominant_phase), ...] — дні з ≥1 хв, для таймлайну
    series = [(date, cumulative_sec, dominant_phase), ...] — усі дні, для чарта
    """
    per_phase = defaultdict(float)
    per_day = defaultdict(float)
    per_day_phase = defaultdict(lambda: defaultdict(float))

    by_session = defaultdict(list)
    for ev in events:
        by_session[ev.get("session", "")].append(ev)

    for evs in by_session.values():
        evs.sort(key=lambda e: e["_ts"])
        prev = None
        for ev in evs:
            ts = ev["_ts"]
            if prev is None:
                sec = 0.0
            else:
                dt = (ts - prev).total_seconds()
                sec = PAUSE_SEC if dt > IDLE_CAP else max(0.0, dt)
            day = ts.date()
            phase = ev.get("phase", "unknown")
            per_phase[phase] += sec
            per_day[day] += sec
            per_day_phase[day][phase] += sec
            prev = ts

    daily, series = [], []
    cum = 0.0
    for day in sorted(per_day):
        dominant = max(per_day_phase[day].items(), key=lambda kv: kv[1])[0]
        cum += per_day[day]
        series.append((day, cum, dominant))
        if per_day[day] >= 60:  # менше хвилини (зайшов на один промпт) — не рядок таймлайну
            daily.append((day, WEEKDAYS[day.weekday()], per_day[day], dominant,
                          dict(per_day_phase[day])))
    return per_phase, daily, series


def fmt_hm(sec):
    sec = int(sec)
    return f"{sec // 3600} год {sec % 3600 // 60:02d} хв"


def fmt_hm_short(sec):
    """Компактний формат для легенди: «14г 05хв» / «45хв»."""
    sec = int(sec)
    h, m = sec // 3600, sec % 3600 // 60
    return f"{h}г {m:02d}хв" if h else f"{m}хв"


def fmt_date(d):
    return f"{d.day} {MONTHS[d.month - 1]}"


def phase_color(state, phase_id):
    ids = [p["id"] for p in state["phases"]]
    if phase_id in ids:
        return PHASE_HUES[ids.index(phase_id) % len(PHASE_HUES)]
    return "#948d80"


def overall_percent(phases):
    """Середнє по всіх фазах: детальна фаза = done/total, ще не розписана = 0."""
    ratios = [(p["done"] / p["total"]) if p.get("total") else 0.0 for p in phases]
    return round(100 * sum(ratios) / len(ratios)) if ratios else 0


def chart_svg(state, series):
    """Накопичені години: X — календарні дні (перерви видно як плато), Y — сума годин."""
    if len(series) < 2:
        return '<p class="empty">Замало днів для графіка — він з’явиться з другого дня роботи.</p>'
    # компактні розміри — чарт живе внизу лівої колонки, вужчий за неї (SVG 1:1)
    W, H = 330, 170
    PL, PR, PT, PB = 34, 10, 10, 24
    iw, ih = W - PL - PR, H - PT - PB
    d0, d1 = series[0][0], series[-1][0]
    span = max((d1 - d0).days, 1)
    max_c = series[-1][1]

    def x(d):
        return PL + iw * (d - d0).days / span

    def y(c):
        return PT + ih * (1 - c / max_c)

    pts = [(x(d), y(c), phase_color(state, ph)) for d, c, ph in series]
    line = " L".join(f"{px:.1f},{py:.1f}" for px, py, _ in pts)
    area = f"M{pts[0][0]:.1f},{PT + ih} L{line} L{pts[-1][0]:.1f},{PT + ih} Z"

    # 3 горизонтальні лінії: 0, середина, максимум
    grid, ylabels = [], []
    for frac in (0.0, 0.5, 1.0):
        gy = PT + ih * (1 - frac)
        grid.append(f'<line class="grid" x1="{PL}" y1="{gy:.1f}" x2="{W - PR}" y2="{gy:.1f}"/>')
        ylabels.append(f'<text class="tick" x="{PL - 6}" y="{gy + 3.5:.1f}" text-anchor="end">'
                       f'{round(frac * max_c / 3600)}г</text>')

    dots = "\n".join(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.6" fill="{c}"/>' for px, py, c in pts)

    return f'''<svg viewBox="0 0 {W} {H}" role="img" aria-label="Накопичені години навчання по днях">
{"".join(grid)}
{"".join(ylabels)}
<text class="tick" x="{PL}" y="{H - 6}">{fmt_date(d0)}</text>
<text class="tick" x="{W - PR}" y="{H - 6}" text-anchor="end">{fmt_date(d1)}</text>
<path class="area" d="{area}"/>
<path class="line" d="M{line}" fill="none"/>
{dots}
</svg>'''


def donut_svg(state, per_phase):
    """Кільцевий чарт розподілу часу по фазах: сегменти = частки, в центрі — сума."""
    ids = [p["id"] for p in state["phases"]]
    items = sorted(
        ((pid, sec) for pid, sec in per_phase.items() if sec >= 60),
        key=lambda kv: ids.index(kv[0]) if kv[0] in ids else len(ids),
    )
    total = sum(sec for _, sec in items)
    if not total:
        return ""
    pmap = {p["id"]: p for p in state["phases"]}
    R, SW, CX = 54, 24, 70          # радіус, товщина кільця, центр
    C = 2 * 3.141592653589793 * R
    segs, legend, off = [], [], 0.0
    for pid, sec in items:
        frac = sec / total
        c = phase_color(state, pid)
        dash = max(frac * C - 2.5, 0.8)  # -2.5 = проміжок між сегментами
        segs.append(
            f'<circle r="{R}" cx="{CX}" cy="{CX}" fill="none" stroke="{c}" stroke-width="{SW}" '
            f'stroke-dasharray="{dash:.1f} {C:.1f}" stroke-dashoffset="{-off:.1f}" '
            f'transform="rotate(-90 {CX} {CX})" stroke-linecap="butt"/>'
        )
        off += frac * C
        name = pmap.get(pid, {"name": "Інше"})["name"]
        legend.append(
            f'<div class="d-leg"><span class="dot" style="background:{c}"></span>'
            f'<span class="d-name">{name}</span>'
            f'<span class="d-val">{round(100 * frac)}% · {fmt_hm_short(sec)}</span></div>'
        )
    return (
        '<div class="donut-wrap">'
        f'<svg class="donut" viewBox="0 0 {2 * CX} {2 * CX}" role="img" aria-label="Розподіл часу по фазах">'
        + "".join(segs)
        + f'<text class="d-center" x="{CX}" y="{CX + 1}" text-anchor="middle">{int(total // 3600)}г</text>'
        + f'<text class="d-sub" x="{CX}" y="{CX + 15}" text-anchor="middle">разом</text>'
        + "</svg>"
        + '<div class="donut-legend">' + "".join(legend) + "</div></div>"
    )


def render(state, per_phase, daily, series):
    phases = state["phases"]
    total_sec = sum(per_phase.values())
    pct = overall_percent(phases)
    active_days = len(daily)
    avg = total_sec / active_days if active_days else 0
    days_span = f"{fmt_date(daily[0][0])} — {fmt_date(daily[-1][0])}" if daily else "ще без записів"

    # шкала таймлайну: найдовший день, округлений угору до цілої години —
    # стабільна й зрозуміла («повна смужка = N год»), не стрибає від нового рекорду
    max_day = max((s for _, _, s, _, _ in daily), default=1) or 1
    scale_sec = ((int(max_day) + 3599) // 3600) * 3600

    # стек-бар у шапці: вся смужка = весь витрачений час, сегменти = частки фаз
    ids = [p["id"] for p in phases]
    stack_items = sorted(
        ((pid, sec) for pid, sec in per_phase.items() if sec >= 60),
        key=lambda kv: ids.index(kv[0]) if kv[0] in ids else len(ids),
    )
    pmap_all = {p["id"]: p for p in phases}
    stack_segs = []
    for pid, sec in stack_items:
        share = 100 * sec / total_sec
        name = pmap_all.get(pid, {"name": "Інше"})["name"]
        stack_segs.append(
            f'<span style="width:{share:.1f}%;background:{phase_color(state, pid)}" '
            f'title="{name} · {fmt_hm_short(sec)} ({round(share)}%)"></span>'
        )
    stack_html = f'<div class="stack">{"".join(stack_segs)}</div>' if stack_segs else ""

    pmap = {p["id"]: p for p in phases}

    def seg_html(breakdown, scale):
        """Міні-стек сегментів по фазах для однієї смужки."""
        segs = []
        for pid in sorted(breakdown, key=lambda k: ids.index(k) if k in ids else len(ids)):
            s = breakdown[pid]
            if s < 30:  # секундний шум не малюємо
                continue
            name = pmap.get(pid, {"name": "Інше"})["name"]
            segs.append(f'<span class="bar-fill" style="width:{100 * s / scale:.1f}%;'
                        f'background:{phase_color(state, pid)}" title="{name} · {fmt_hm_short(s)}"></span>')
        return "".join(segs)

    # тижні (пн–нд): рядок на тиждень, смужка — стек по фазах.
    # Це головний вид: показує темп, а не журнал; рік навчання = ~50 рядків.
    weeks_phase = defaultdict(lambda: defaultdict(float))
    weeks_tot, weeks_days = defaultdict(float), defaultdict(int)
    for day, _, sec, _, breakdown in daily:
        monday = day - timedelta(days=day.weekday())
        weeks_tot[monday] += sec
        weeks_days[monday] += 1
        for pid, s in breakdown.items():
            weeks_phase[monday][pid] += s
    max_week = max(weeks_tot.values(), default=1)
    week_scale = ((int(max_week) + 3599) // 3600) * 3600
    week_rows = []
    for monday in sorted(weeks_tot):
        sunday = monday + timedelta(days=6)
        if monday.month == sunday.month:
            label = f"{monday.day}–{sunday.day} {MONTHS[monday.month - 1]}"
        else:
            label = f"{monday.day} {MONTHS[monday.month - 1][:3]} – {sunday.day} {MONTHS[sunday.month - 1][:3]}"
        n = weeks_days[monday]
        days_word = "день" if n == 1 else "дні" if n <= 4 else "днів"
        week_rows.append(
            f'<div class="row"><span class="when"><span class="day">{label}</span>'
            f'<span class="date">{n} {days_word} роботи</span></span>'
            f'<span class="bar-track">{seg_html(weeks_phase[monday], week_scale)}</span>'
            f'<span class="dur">{fmt_hm(weeks_tot[monday])}</span></div>'
        )
    weeks_html = "\n".join(week_rows) or '<p class="empty">Ще немає записів часу — попрацюй над проєктом і перегенеруй.</p>'

    # деталізація по днях — лише поточний тиждень (або останній активний, якщо цей порожній)
    curweek_title = "Цей тиждень по днях"
    cur_days = []
    if daily:
        today = datetime.now().date()
        cur_days = [d for d in daily if d[0] >= today - timedelta(days=today.weekday())]
        if not cur_days:
            last = daily[-1][0]
            cur_days = [d for d in daily if d[0] >= last - timedelta(days=last.weekday())]
            curweek_title = "Останній активний тиждень"
    day_rows = [
        f'<div class="row"><span class="when"><span class="day">{wd}</span>'
        f'<span class="date">{fmt_date(day)}</span></span>'
        f'<span class="bar-track">{seg_html(breakdown, scale_sec)}</span>'
        f'<span class="dur">{fmt_hm(sec)}</span></div>'
        for day, wd, sec, _, breakdown in cur_days
    ]
    curdays_html = "\n".join(day_rows) or '<p class="empty">Цього тижня ще не було роботи.</p>'

    # роадмап: рядок на фазу — назва, бар done/total, значення (+ час фази)
    ph_rows = []
    for p in phases:
        c = phase_color(state, p["id"])
        if p.get("total"):
            ratio, fill, done_cls, val = round(100 * p["done"] / p["total"], 1), c, "done", f'{p["done"]}/{p["total"]}'
        else:
            ratio, fill, done_cls, val = 0, "var(--muted)", "", "—"
        psec = per_phase.get(p["id"], 0)
        if psec >= 60:  # фаза з реальним часом — показуємо і його
            val += f" · {fmt_hm_short(psec)}"
        ph_rows.append(
            f'<div class="ph-row {done_cls}">'
            f'<div class="ph-top"><span class="name"><span class="dot" style="background:{c}"></span>'
            f'{p["name"]} · {p["subtitle"]}</span><span class="val">{val}</span></div>'
            f'<div class="ph-bar"><span class="ph-fill" style="--w:{ratio}%;background:{fill}"></span></div>'
            f'</div>'
        )
    phases_html = "\n".join(ph_rows)

    # прогноз для поточної фази: (уроків лишилось) × (годин/урок за фактом цієї фази)
    forecast_html = ""
    curp = pmap.get(state.get("current_phase"))
    cur_sec = per_phase.get(state.get("current_phase"), 0)
    if curp and curp.get("total") and curp["done"] and curp["done"] < curp["total"] and cur_sec > 0:
        per_lesson = cur_sec / curp["done"]
        remaining = (curp["total"] - curp["done"]) * per_lesson
        forecast_html = (
            f'<p class="forecast">{curp["name"]}: ще ~{max(1, round(remaining / 3600))} год '
            f'до кінця фази (темп ~{fmt_hm_short(per_lesson)}/урок)</p>'
        )

    return TEMPLATE.format(
        total_hm=fmt_hm(total_sec),
        span=days_span,
        active_days=active_days,
        avg=fmt_hm_short(avg),
        pct=pct,
        maxday=f"{scale_sec // 3600} год",
        wmax=f"{week_scale // 3600} год",
        stack=stack_html,
        chart=chart_svg(state, series),
        donut=donut_svg(state, per_phase),
        phases=phases_html,
        forecast=forecast_html,
        weeks=weeks_html,
        curweek_title=curweek_title,
        curdays=curdays_html,
    )


TEMPLATE = """<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ML Learning — прогрес</title>
<style>
:root {{
  --bg:#f6f3ee; --surface:#fff; --ink:#1e1b17; --ink-soft:#4a453e; --muted:#948d80;
  --rule:#e3ddd0; --track:#e9e3d6;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --bg:#15171c; --surface:#1b1e25; --ink:#eae7e0; --ink-soft:#b8b3a8; --muted:#6f7078;
    --rule:#2a2d35; --track:#23262e;
  }}
}}
:root[data-theme="dark"] {{
  --bg:#15171c; --surface:#1b1e25; --ink:#eae7e0; --ink-soft:#b8b3a8; --muted:#6f7078;
  --rule:#2a2d35; --track:#23262e;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink);
  font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif; -webkit-font-smoothing:antialiased; }}
.page {{ max-width:1240px; margin:0 auto;
  padding:clamp(1.8rem,4vw,3.5rem) clamp(1rem,3vw,1.5rem) calc(5rem + env(safe-area-inset-bottom,0px)); }}
.eyebrow {{ font-size:.72rem; font-weight:600; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); margin:0 0 .6rem; }}
h1 {{ font-family:ui-serif,Georgia,"Times New Roman",serif; font-weight:500; font-size:clamp(1.55rem,3.2vw,2.1rem); line-height:1.15; margin:0; text-wrap:balance; }}
h2 {{ font-family:ui-serif,Georgia,serif; font-weight:500; font-size:1.15rem; margin:0; }}
.head {{ display:grid; grid-template-columns:1fr auto; align-items:end; gap:1.2rem 2.5rem; }}
.num {{ font-family:ui-monospace,"SF Mono",Menlo,monospace; font-variant-numeric:tabular-nums; font-size:1.9rem; font-weight:600; letter-spacing:-.02em; line-height:1.1; }}
.head-num {{ text-align:right; max-width:23rem; justify-self:end; }}
@media (max-width:640px) {{ .head {{ grid-template-columns:1fr; }} .head-num {{ text-align:left; justify-self:start; }} }}
.range {{ font-size:.82rem; color:var(--muted); margin:.3rem 0 0; }}
.stack {{ display:flex; gap:3px; height:10px; margin-top:1.5rem; }}
.stack span {{ display:block; border-radius:3px; transform:scaleX(0); transform-origin:left; animation:grow 1s cubic-bezier(.16,.8,.3,1) forwards; }}
.stack span:first-child {{ border-radius:5px 3px 3px 5px; }}
.stack span:last-child {{ border-radius:3px 5px 5px 3px; }}
@media (prefers-reduced-motion: reduce) {{ .stack span {{ animation:none; transform:none; }} }}

.chart-section {{ margin:2.4rem 0 0; }}
.chart-section h2 {{ margin-bottom:.9rem; }}
.chart-section svg {{ display:block; width:100%; max-width:480px; height:auto; }}
svg .grid {{ stroke:var(--rule); stroke-width:1; }}
svg .tick {{ fill:var(--muted); font-family:ui-monospace,"SF Mono",Menlo,monospace; font-size:11px; }}
svg .area {{ fill:var(--ink); opacity:.05; }}
svg .line {{ stroke:var(--ink-soft); stroke-width:1.5; stroke-linejoin:round; }}

.layout {{ display:grid; grid-template-columns:minmax(340px,420px) 1fr; gap:clamp(2.2rem,4vw,3.4rem); align-items:start;
  margin-top:2.6rem; padding-top:2.2rem; border-top:1px solid var(--rule); }}
/* Планшет: одна колонка, але donut і чарт стають поруч, шрифти й бари більші під палець */
@media (max-width:1024px) {{
  .layout {{ grid-template-columns:1fr; gap:2.6rem; }}
  .progress-side {{ display:grid; grid-template-columns:1fr 1fr; column-gap:3rem; align-items:start; }}
  .progress-side > .progress-head, .progress-side > .ph-row, .progress-side > .forecast {{ grid-column:1 / -1; }}
  .ph-top {{ font-size:.85rem; }}
  .d-leg {{ font-size:.85rem; }}
  .ph-bar {{ height:8px; }}
  .row {{ padding:.7rem 0; }}
  .bar-track {{ height:9px; }}
  .when {{ font-size:.92rem; }}
  .when .date {{ font-size:.8rem; }}
  .dur {{ font-size:.92rem; }}
  .donut {{ width:150px; height:150px; }}
}}
@media (max-width:640px) {{
  .progress-side {{ display:block; }}
}}
/* Нижня панель viewer-а (артефакт/браузер на планшеті) перекриває низ — резервуємо місце */
@media (pointer:coarse) {{
  .page {{ padding-bottom:calc(9rem + env(safe-area-inset-bottom,0px)); }}
}}

.donut-section {{ margin:2.4rem 0 0; }}
.donut-section h2 {{ margin-bottom:.9rem; }}
.donut-wrap {{ display:flex; align-items:center; gap:1.5rem; }}
.donut {{ width:132px; height:132px; flex-shrink:0; }}
.d-center {{ fill:var(--ink); font-family:ui-monospace,"SF Mono",Menlo,monospace; font-size:22px; font-weight:600; }}
.d-sub {{ fill:var(--muted); font-family:ui-monospace,"SF Mono",Menlo,monospace; font-size:9px; }}
.donut-legend {{ flex:1; min-width:0; }}
.d-leg {{ display:flex; align-items:baseline; gap:.45rem; font-size:.78rem; padding:.22rem 0; }}
.d-leg .dot {{ width:6px; height:6px; border-radius:50%; flex-shrink:0; align-self:center; }}
.d-leg .d-name {{ color:var(--ink-soft); }}
.d-leg .d-val {{ margin-left:auto; font-family:ui-monospace,monospace; font-variant-numeric:tabular-nums; color:var(--muted); white-space:nowrap; }}

.progress-head {{ display:flex; align-items:baseline; justify-content:space-between; margin-bottom:1.2rem; }}
.progress-pct {{ font-family:ui-monospace,"SF Mono",monospace; font-variant-numeric:tabular-nums; font-size:1.6rem; font-weight:600; }}
.progress-pct .sign {{ font-size:1rem; color:var(--muted); font-weight:400; }}
.ph-row {{ padding:.55rem 0; }}
.ph-top {{ display:flex; align-items:baseline; justify-content:space-between; gap:.5rem; font-size:.78rem; margin-bottom:.4rem; }}
.ph-top .name {{ color:var(--ink-soft); display:flex; align-items:center; gap:.45rem; }}
.ph-top .dot {{ width:6px; height:6px; border-radius:50%; flex-shrink:0; }}
.ph-top .val {{ font-family:ui-monospace,monospace; font-variant-numeric:tabular-nums; color:var(--muted); white-space:nowrap; }}
.ph-row.done .val {{ color:var(--ink); }}
.ph-bar {{ height:6px; background:var(--track); border-radius:3px; overflow:hidden; }}
.ph-fill {{ display:block; height:100%; border-radius:3px; width:var(--w); transform:scaleX(0); transform-origin:left; animation:grow 1.1s cubic-bezier(.16,.8,.3,1) forwards; }}

.log-head {{ display:flex; align-items:baseline; justify-content:space-between; gap:1rem; flex-wrap:wrap; margin-bottom:1.2rem; }}
.log-head.second {{ margin-top:2.6rem; }}
.scale-note {{ font-size:.75rem; color:var(--muted); }}
.forecast {{ font-size:.75rem; color:var(--muted); margin:1rem 0 0; padding-top:.9rem; border-top:1px solid var(--rule); }}
.row {{ display:grid; grid-template-columns:8rem 1fr 4.8rem; align-items:center; gap:.9rem; padding:.55rem 0; border-bottom:1px solid var(--rule); }}
.when {{ font-size:.83rem; }}
.when .day {{ color:var(--ink); font-weight:500; }}
.when .date {{ display:block; color:var(--muted); font-size:.75rem; }}
.bar-track {{ display:flex; gap:2px; height:7px; background:var(--track); border-radius:4px; overflow:hidden; }}
.bar-fill {{ display:block; height:100%; border-radius:4px; transform:scaleX(0); transform-origin:left; animation:grow 1s cubic-bezier(.16,.8,.3,1) .15s forwards; }}
@keyframes grow {{ from {{ transform:scaleX(0); }} to {{ transform:scaleX(1); }} }}
@media (prefers-reduced-motion: reduce) {{ .bar-fill,.ph-fill {{ animation:none; transform:none; }} }}
.dur {{ font-family:ui-monospace,"SF Mono",Menlo,monospace; font-variant-numeric:tabular-nums; font-size:.83rem; text-align:right; white-space:nowrap; }}
.empty {{ color:var(--muted); font-size:.9rem; }}
</style>
</head>
<body>
<div class="page">
  <header class="head">
    <div class="head-main">
      <p class="eyebrow">ML Learning · журнал часу</p>
      <h1>Скільки часу пішло на навчання</h1>
    </div>
    <div class="head-num">
      <div class="num">{total_hm}</div>
      <p class="range">{span} · {active_days} активних днів · у середньому {avg}/день</p>
    </div>
  </header>
{stack}

  <div class="layout">
    <aside class="progress-side">
      <div class="progress-head">
        <h2>Роадмап</h2>
        <span class="progress-pct">{pct}<span class="sign">%</span></span>
      </div>
{phases}
{forecast}
      <section class="donut-section">
        <h2>Розподіл часу</h2>
{donut}
      </section>
      <section class="chart-section">
        <h2>Накопичено годин</h2>
{chart}
      </section>
    </aside>

    <section class="log">
      <div class="log-head">
        <h2>По тижнях</h2>
        <span class="scale-note">повна смужка = {wmax} · кольори = фази</span>
      </div>
{weeks}
      <div class="log-head second">
        <h2>{curweek_title}</h2>
        <span class="scale-note">повна смужка = {maxday}</span>
      </div>
{curdays}
    </section>
  </div>
</div>
</body>
</html>
"""


def main():
    state = load_state()
    PHASE_PTR.write_text(state.get("current_phase", "unknown") + "\n", encoding="utf-8")
    per_phase, daily, series = aggregate(load_events())
    REPORT.write_text(render(state, per_phase, daily, series), encoding="utf-8")
    total = sum(per_phase.values())
    print(f"✓ {REPORT.name}: {fmt_hm(total)} загалом, {len(daily)} днів, прогрес {overall_percent(state['phases'])}%")


if __name__ == "__main__":
    sys.exit(main())
