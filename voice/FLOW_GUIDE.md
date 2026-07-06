# Flow Design Guide

Правила побудови voice-agent flows. Single source of truth. Коли генеруєш flow (Cowork, Claude Code, вручну) — спочатку перевір себе по цьому файлу.

Пов'язані файли:
- `../SYSTEM_PROMPT.md` — runbook (як Claude запускає mock)
- `build_prompt.py` — runtime правила поведінки бота (MODE_RULES + NAVIGATION)
- `flows/*.json` — самі flows
- `flows/archive/` — flows старші за місяць

---

## 1. Filosofia

**Flow — це сценарій взаємодії, а не скрипт.** Бот має гнучкість:
- Питати follow-up якщо відповідь поверхнева
- Переходити далі якщо відповідь сильна
- Реагувати на ре-навігацію юзера (поясни / вернись)
- Давати correction в tutor-mode

**Flow — це НЕ lecture і НЕ chatbot.** Є чітка мета (тренувати фундаменти / перевірити гапи / пояснити ELI5 / practice English), є час-бюджет, є критерії успіху.

---

## 2. Canonical modes

Одне зі значень поля `"mode"`. Змінювати без оновлення `build_prompt.py::MODE_RULES` і `../SYSTEM_PROMPT.md` **не можна** — бот отримає дефолтні правила і поведеться як tech-ua.

| mode | Коли використовувати | Як поводиться бот |
|------|---------------------|-------------------|
| `tech-ua` | Підготовка до ukr tech-інтерв'ю, Weeks 1-3 | Інтерв'юер. Нейтральні маркери. НЕ оцінює під час. НЕ підказує. |
| `tech-en` | Підготовка до en tech-інтерв'ю, Week 4+ | Так само як tech-ua, але англ. Оцінка в кінці включає English fluency окремо. |
| `english-conversation` | Fluency practice, 1×/тиждень | Casual chat. НЕ виправляє граматику під час. Підтримує flow. |
| `english-tutor` | Targeted English gaps (conditionals, phrasal verbs, etc.) | Після кожної відповіді — коротка корекція grammar/pronunciation. |
| `eli5-ua` | Пояснити non-tech людям концепцію | Бот пояснює простими аналогіями. М'яко поправляє. |
| `tutor-ua` | Перевірити знання + корекція з поясненням | Бот питає → оцінює ("Правильно / Частково / Ні") → пояснює correction. Під кінець — summary scores. |

**Додавання нового mode:** оновити 3 місця одночасно — `build_prompt.py::MODE_RULES`, `../SYSTEM_PROMPT.md` (canonical modes list), цей файл (таблиця вище).

---

## 3. Flow JSON anatomy

```json
{
  "mode": "tutor-ua",
  "topic": "biological-neurons",
  "difficulty": "medium",
  "duration_min": 5,
  "language": "uk",
  "interviewer_persona": "neuroscience_tutor_strict",
  "opening": "...",
  "questions": [ { ... }, ... ],
  "wrap_up": "..."
}
```

### Обов'язкові поля

- **`mode`** — з canonical списку, lowercase, hyphenated.
- **`topic`** — коротко, lowercase, hyphens. Використовується в імені файлу і в URL.
- **`difficulty`** — `easy` / `medium` / `hard`. Див. §5.
- **`duration_min`** — цілий (3, 5, 15, 30, 45, 60). Має відповідати `sum(time_budget_sec)` + ~20% на opening+wrap-up+навігацію.
- **`language`** — `uk` / `en`.
- **`interviewer_persona`** — snake_case id (напр. `hiring_manager_winwin`, `senior_ml_friendly`, `neuroscience_tutor_strict`). Описує тон. Не використовується програмно (поки), але bot бачить.
- **`opening`** — те що бот говорить першим, слово в слово. Включає: hello, формат сесії, очікування від юзера, ready check.
- **`wrap_up`** — підсумок. 2-3 takeaways (в tutor/eli5 — обов'язково), прощання.

### Question anatomy

```json
{
  "id": "q1",
  "text": "...",
  "follow_ups": ["...", "..."],
  "time_budget_sec": 150,
  "evaluation_criteria": ["..."],
  "red_flags": ["..."],
  "strong_markers": ["..."],
  "correction_template": "..."
}
```

- **`id`** — `q1`, `q2`, ... (зручно для пост-аналізу).
- **`text`** — саме питання як буде звучати. Включати контекст/setup якщо треба (у `tutor-ua` часто є setup-текст перед питанням). Стислий, без filler.
- **`follow_ups`** — 2-3 короткі запасні питання якщо юзер дав поверхневу відповідь. НЕ використовуй як "next q" — це refinement до поточного.
- **`time_budget_sec`** — скільки планово йде на це питання. Сума всіх ≤ `duration_min × 60 × 0.75` (залишай 25% на opening/wrap-up/навігацію).
- **`evaluation_criteria`** — 2-3 точки що має містити strong answer. Юзер не бачить; бот дивиться чи покрив.
- **`red_flags`** — конкретні помилки (плутанина термінів, misconceptions). Сигнал для correction.
- **`strong_markers`** — вища планка (знання деталей, правильна термінологія, production examples). Сигнал що можна пропустити follow-ups і йти далі.
- **`correction_template`** (опціонально, обов'язкове в `tutor-ua` і `eli5-ua`) — правильна відповідь для бота. Бот **перефразує** своїми словами, не читає буквально. 2-4 речення.

---

## 4. Naming convention

**Pattern:** `{mode}_{topic}_{difficulty}.json`

Приклади:
- ✅ `tech-ua_rag_medium.json`
- ✅ `tutor-ua_biological-neurons_medium.json`
- ✅ `english-conversation_remote-work_intermediate.json`
- ❌ `TechUA_RAG_Medium.json` (camelCase)
- ❌ `tech-ua-rag-medium.json` (усе з дефісами — не розпарсити)
- ❌ `rag.json` (нема mode/difficulty)

Версіонування: якщо flow вже використовувався і створюєш нову версію на ту ж тему — додавай суфікс `_v2`, `_v3`. Старий перенось у `flows/archive/` через місяць.

---

## 5. Difficulty rubric

Прив'язана до `confidence` юзера у `progress.json::topics_master`.

| difficulty | Коли | Характер питань |
|-----------|------|----------------|
| `easy` | Перший mock на тему, `confidence ≤ 2` | Intuition-level. Без матриць, без production specifics. "Навіщо", "що таке на рівні ідеї". |
| `medium` | Повторний mock, `confidence 3` | Fundamentals + одне production питання. Follow-ups копають глибше. |
| `hard` | `confidence ≥ 4`, preparation для real interview | Production trade-offs, edge cases, "як ти дебажив би", multi-hop reasoning. |

**Red flag:** `hard` без medium перед ним — демотивація майже гарантована.

---

## 6. Question design checklist

Перед фіналізацією кожного питання — прогнати checkpoints:

1. **Чи можна дати strong answer за `time_budget_sec`?** Якщо ні — розбий на два питання або збільши бюджет.
2. **Чи питання вимагає знання виключно з `topic`?** Якщо треба багато з інших топіків — це misfit, винеси в бонус або зроби окремий flow.
3. **Чи є хоча б 2 `evaluation_criteria` і 1 `red_flag`?** Без них бот не знає куди дивитись.
4. **Чи `strong_markers` вище за `evaluation_criteria`?** Має бути різниця pass vs exceed.
5. **`follow_ups` — чи REFINEMENT до поточного, не скриті нові питання?** Типовий failure — впихнути "а ще поясни X" де X це вже інша тема.
6. **В `tutor-ua` / `eli5-ua` — чи є `correction_template`?** Обов'язково.
7. **Чи `text` питання звучить natural вголос?** Прочитати вголос — якщо спотикаєшся, переформулюй.

---

## 7. Navigation rules (reference)

Ці правила — глобальні, живуть у `build_prompt.py` у секції "НАВІГАЦІЯ". Flow-автор нічого не робить, але має знати що вони існують, щоб не дублювати або не суперечити в `opening`:

- Юзер може залишитись на поточній ноді для глибшого пояснення (тригери: "поясни детальніше", "не зрозумів", "приклад", "а що таке X").
- Юзер може повернутись до попередньої ноди ("вернись", "по [q1]", "перше питання").
- Бот робить explicit re-check коли неясно ("це твоя відповідь чи хочеш пояснення?").
- Навігація не ріже time budget — до кінця flow бот попереджає "ще 2 питання залишилось".

**Не пиши в `opening` речі типу "не питай мене про попередні" — це зламає систему.**

---

## 8. Lifecycle

1. **Draft** — новий JSON створено, пройшов §6 checklist.
2. **Active** — використовується, лежить в `flows/`.
3. **Stale** (після 1 реальної сесії) — застарілий, бот пам'ятає питання через transcript. Генеруй `_v2` з новими кутами ТОГО Ж topic.
4. **Archived** (через місяць після Active) — перенеси в `flows/archive/`. Не видаляй — референс для майбутніх версій.

---

## 9. Pre-ship checklist

Перед тим як flow готовий до запуску через URL autostart:

- [ ] Ім'я відповідає convention (§4)
- [ ] `mode` з canonical списку (§2)
- [ ] `duration_min` узгоджений з sum time budgets (±25%)
- [ ] Всі questions пройшли design checklist (§6)
- [ ] `opening` і `wrap_up` написані повними реченнями (бот читає слово в слово)
- [ ] В `tutor-ua` / `eli5-ua` — всі `correction_template` є
- [ ] JSON валідний (запусти `python -c "import json; json.load(open('flows/X.json'))"`)
- [ ] Згенеруй system prompt локально: `python build_prompt.py flows/X.json /tmp/check.txt` — прочитай, подивись чи нема дивного.

---

## 10. Common mistakes

- **Копіювати правила з tech-ua у tutor-ua** (наприклад, "не оцінюй під час" — у tutor це антипаттерн, весь сенс формату — оцінка кожної ноди).
- **`time_budget_sec` занадто малий** — 30-40 сек на питання = юзер не встигне навіть почати думати. Мінімум 60с на medium, 90-120 на hard.
- **`follow_ups` як схований list нових питань** — забирає час, плутає бота.
- **`correction_template` написано як підручник** — бот не перефразовує бо вже виглядає як "правильна відповідь готова". Пиши природною мовою, щоб довелось перефразовувати.
- **Opening без "готовий?" ready check** — бот починає питати одразу, юзер не встиг сісти.
- **`wrap_up` без takeaways** — сесія закінчується ні на чому. Завжди 2-3 головні думки на розставання.
