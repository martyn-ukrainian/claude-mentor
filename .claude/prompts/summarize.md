You are summarizing ONE mentoring/learning session of an ML-learning project.
The folder path is given at the very end of this prompt.

Read the `dialogue.md` in that folder. It is the session as plain
`USER:` / `ASSISTANT:` lines (tool calls are already stripped out).

Then write `summary.md` in that SAME folder, using the Write tool, in **Ukrainian**,
formatted exactly as:

    # <короткий заголовок, до ~6 слів>

    - **Тема / концепція:** <яку тему чи концепцію розбирали>
    - **Що робив учень:** <який таск / практику виконував студент>
    - **Ключові висновки:** <1–2 головні думки, що засвоїли>
    - **Де плавав / gotchas:** <де студент плавав або неочевидні моменти; якщо не було — "—">

Rules:
- Ukrainian, factual, concise. Never invent content not present in the dialogue.
- Focus on the LEARNING: what was taught, what the student practiced, what was hard.
- Ignore system noise (task-notifications, `/command` caveats, hook-feedback lines).
- Never modify `dialogue.md`; only create `summary.md`.
- Do nothing (write no file) if `dialogue.md` is missing or empty, or if `summary.md`
  already exists in that folder.
