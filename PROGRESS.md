# PROGRESS

**Поточна фаза:** Фаза 0 ✅ **completed** → Фаза 1 (математика) **на паузі, 5/8 уроків** → **Фаза 2 в процесі, 5/9+capstone**

**Рішення від 2026-07-30 (втрата й відновлення записів Уроку 05):** Урок 05 (дерева/RF) було фактично пройдено раніше (~28.07), але записи `/end-lesson` (docs, memories, оновлення трекера) загубились — їх не було ні в git-історії, ні в `reflog`, ні в `stash` (лишився тільки код `code/phase-2/05_trees_random_forest.py`). Студент обрав **перепройти урок з нуля** новим файлом `code/phase-2/05_1_trees_random_forest.py` — і воно ж спрацювало як retrieval. Урок закрито 30.07 з повними записами.

**Рішення від 2026-07-19:** `lessons/phase-2/` розгорнуто в 9 уроків + capstone (README + методика). Урок 01 (sklearn fundamentals) і Урок 02 (лінійна регресія sklearn, closed-form vs GD, R², multicollinearity) — пройдено.

**Рішення від 2026-07-20:** ПЕРЕД Уроком 03 обов'язково закрити R²-прогалину (7 разів та сама помилка "% правильних відповідей", підтверджено retrieval review + практика на Diabetes dataset + спроба візуалізації — жодна текстова спроба не закріпилась). **Наступний крок — R²-сесія (voice чи новий формат), тільки потім Урок 03 (логістична регресія).**

**R²-прогалина ЗАКРИТА (2026-07-25):** текстовий формат "сам рахує на контрастних прикладах без означення наперед" (A/B/C/D/E: ідеальний, близько без точних збігів, прогноз=середнє, поганий, довільна константа) — спрацював там, де 7 попередніх текстових спроб не заходили. Студент сам вивів фінальне формулювання: "R²=0.7 = модель на 70% менше помиляється за стратегію 'завжди вгадуй середнє'". Деталі й тактика — `memories/profile.md` (секція "R² семантика — закрита") і `memories/voice-retrieval-queue.md` (архів). **Блокер знято — можна рухатись до Уроку 03.**

**Момент сесії Уроку 02:** студент прямо сказав "80% не розумію" посеред Задачі 3 — зупинились, розібрали з нуля. Решта уроку пішла значно впевненіше. Хороший приклад чому не форсувати темп.

**Практика 20.07 (`code/phase-2/02b_diabetes_practice.py`, `02c_r2_visualization.py`):** пайплайн (split→Pipeline→R²/MSE→coef_) перенісся на новий датасет (Diabetes) самостійно й бездоганно. R² словесна інтерпретація — ні, навіть після retrieval-контрприкладу і візуалізації (`02c_r2_visualization.png`, prediction vs actual scatter проти наївного baseline).

**Нове правило (19.07):** термінологію/поняття з практики (не тільки код) — накопичувати в `memories/voice-retrieval-queue.md`, перевіряти окремо голосом. Деталі в `CLAUDE.md`.

**Рішення від 2026-07-18 (друга половина сесії):** одна сесія пройшла 5 уроків Фази 1 поспіль (01→05), швидше за задуманий interleaving-темп. Студент сам чесно сказав "слабо насправді розібрався" наприкінці. **Наступна сесія — Фаза 2 (практика на реальних даних)**, а не Урок 06. Мета подвійна: (а) дати практикою "закріпити" щойно вивчену математику (лінійна регресія на реальних даних — застосування Уроків 04-05 напряму), (б) повернутись до інтерливінгу замість суцільного блоку. Уроки 06-08 Фази 1 (loss functions, probability, capstone) — не скасовані, а відкладені, підхопимо коли реально знадобляться в Фазі 2 (loss functions — при перших моделях; probability — при Naive Bayes/ймовірнісних метриках).

**Retrieval Фази 1 виконано 2026-07-19:**
- Cosine similarity — написав сам, одна помилка з дужками (пріоритет операцій), виправив миттєво ✓
- Некомутативність матриць — механіка/код бездоганні, словесне пояснення "чому" досі важке навіть з підказками (4-й раз поспіль той самий патерн — прийняв офіційну відповідь, не форсував далі)
- Chain rule (`e^(3x²+1)`) — одна помилка (зайвий множник у `d(e^u)/du`), виправив сам після наведення на таблицю ✓
- Нормалізація features "чому прискорює GD" — покращилось, коли зв'язав з учорашнім lr-експериментом (один lr, різні масштаби фіч = одночасно завеликий і замалий крок)

**Висновок:** готовий рухатись до Фази 2. "Некомутативність словами" — приймаємо як стабільну, некритичну прогалину (механіка ідеальна), не блокуючий фактор.

**Де зупинились:** Фаза 2, Урок 05 (дерева рішень, Random Forest) — пройдено 30.07 (перепройдено після втрати записів, див. рішення вгорі). Overfitting наживо, bagging/голосування, `feature_importances_` + пастка корельованих фіч, scaling деревам не потрібен. **Наступний крок — Урок 06 Фази 2 (Gradient Boosting: XGBoost / LightGBM)** — наступний ансамбль після bagging, вже boosting-логіка (дерева одне за одним виправляють помилки попередніх, не голосують паралельно).

**Сильна сесія:** студент самостійно придумав числові приклади для precision/recall і самостійно вивів чому accuracy=94% оманлива (розчинення помилки міноритарного класу) — обидва глибше за мінімальний критерій уроку. Єдина нова прогалина — плутанина AUC vs threshold (див. `voice-retrieval-queue.md`).

*(Історичне: Фаза 1, Урок 05 (градієнтний спуск з нуля на NumPy) — пройдено технічно, засвоєння за словами студента було "слабке" на момент 18.07. Retrieval Фази 1 виконано 19.07, див. нижче.)*

**Рішення від 2026-07-13 (порядок фаз):** Фаза 2 первою, не паралельно. Причина: hands-on ML — найшвидший шлях до реального portfolio-об'єкта. Математика в вакуумі (3Blue1Brown без застосування) ризикує стати "перегляданням відео". Коли лінійна регресія не збігається — тоді відкриваємо градієнтний спуск; коли модель overfit-иться — тоді регуляризація і L1/L2 у контексті. Andrew Ng сам будував курс саме так.

## Наступний крок — Фаза 2 (класичний ML)

**Рішення від 2026-07-13:** пропускаємо синтетичний capstone (Iris/Wine/House Prices тощо). Причина: практика-датасети виглядають як junior-signal, не диференціюють у portfolio. Реальний portfolio-об'єкт народиться природно у Фазі 2 коли будемо застосовувати класичний ML до **реальних задач** — agro (LoRa greenhouse monitoring), персональні дані, або справжня Kaggle-змагання з leaderboard.

**Learning-артефакт для процесу:** сам репо `claude-mentor` (7 уроків, docs, code, Titanic notebook як приклад workflow) — це вже свідчення структурованого підходу. Не виносити Titanic в окремий портфоліо-репо.

### Фаза 1 — Математика для ML (4-6 тижнів)

- **3Blue1Brown "Essence of Linear Algebra"** — YouTube playlist, 15 епізодів по 10-15 хв. Вектори, матриці, лінійні перетворення, власні значення. Візуальний, інтуїтивний.
- **Похідні + градієнти + chain rule** — основа backpropagation. 3Blue1Brown "Essence of Calculus" перші 6 епізодів.
- **Ймовірності і статистика** — розподіли, matematичне сподівання, дисперсія, Байєс. StatQuest на YouTube (Josh Starmer) для інтуїції.
- **Градієнтний спуск руками на NumPy** — реалізувати з нуля, побачити як воно збігається.
- **Функції втрат** — MSE, cross-entropy. Що вони означають геометрично.

Ресурси: 3Blue1Brown (YouTube), StatQuest, безкоштовна книга "Mathematics for Machine Learning" (Deisenroth) для довідки. Khan Academy для прогалин.

### Фаза 2 — Класичний ML (6-8 тижнів)

- **sklearn основи** — train/test split, pipelines, transformers.
- **Лінійна регресія** — з нуля на NumPy, потім через sklearn.
- **Логістична регресія** — класифікація.
- **Дерева, Random Forest** — non-parametric методи.
- **Gradient Boosting** — XGBoost / LightGBM.
- **KNN, SVM, Naive Bayes**.
- **Метрики** — precision/recall, F1, ROC-AUC, confusion matrix. Коли яку.
- **Крос-валідація, регуляризація** (L1/L2).
- **Feature engineering** — encoding категорних (one-hot, target, ordinal), scaling, feature importance.
- **Гіперпараметри** — GridSearch, RandomSearch, Optuna.

Ресурси: **"Hands-On Machine Learning"** (Aurélien Géron, 3rd ed) — ключова книга. **Andrew Ng "Machine Learning Specialization"** (Coursera) для інтуїції. sklearn docs для reference.

### Як їх чергувати

**Основний трек — Фаза 2.** Кожна сесія починається з практики sklearn / реальних даних. Математика підтягується just-in-time коли:

- Не збігається градієнтний спуск → відкриваємо похідні і chain rule (3Blue1Brown Calculus Ep 1-3).
- Модель overfit-иться → відкриваємо bias-variance, L1/L2 (StatQuest regularization).
- Не розумію чому Random Forest працює краще за одне дерево → відкриваємо ensemble math + матсподівання (3Blue1Brown Probability).
- Не розумію PCA / eigenvectors → 3Blue1Brown Linear Algebra Ep 13-14.

**Прапорець "борг математики":** якщо тричі уперлись в один концепт (напр. градієнти в різних алгоритмах) — робимо окрему math-сесію на 45-60 хв. Не раніше.

### Retrieval-check на старті Фази 2 (перший урок)

Три питання перед першим hands-on ML:

- **EDA методологія** — три мети (якість → гіпотези → sanity). Із Уроку 04 (Feynman зупинявся на "знайомство з даними").
- **Correlation ≠ causation** — сформулювати confounder на новому прикладі (не bar/beer, не fare/pclass). Із Уроку 05.
- **notebook vs .py вибір** — прочитати завдання "тренуємо модель у cron" і сказати які файли робити в чому.

Плюс борг з Фази 0 який спливе природно у Фазі 2:

- **NumPy broadcasting** — правило справа наліво без підказки. Знадобиться при роботі з batched данними в sklearn (`.predict(X)` де `X` — 2D array).
- **`axis` семантика** — на shape (3, 4) що робить `sum(axis=0)` і чому. Знадобиться при aggregations pandas і feature engineering.
- **Z-score інтерпретація** — не min-max scaling, це centered + scaled (третій раз, борг з Уроку 03). Знадобиться коли будемо застосовувати `StandardScaler` у sklearn pipeline.

## Пройдено — Фаза 0

- **Урок 01** — Python basics ([docs](docs/phase-0-python/01-python-basics.md), [memories](memories/lessons/01-01-python-basics.md))
- **Урок 02** — Type hints + mypy ([docs](docs/phase-0-python/02-type-hints.md), [memories](memories/lessons/01-02-type-hints.md), voice Feynman ✓)
- **Урок 03** — NumPy ([docs](docs/phase-0-python/03-numpy.md), [memories](memories/lessons/01-03-numpy.md), voice Feynman ✓ + retrieval ✓)
- **Урок 04** — pandas + Titanic EDA ([docs](docs/phase-0-python/04-pandas.md), [memories](memories/lessons/01-04-pandas.md)). Перше знайомство з `uv`.
- **Урок 05** — matplotlib + seaborn + Pearson correlation + confounder problem ([docs](docs/phase-0-python/05-visualization.md), [memories](memories/lessons/01-05-visualization.md))
- **Урок 06** — Jupyter workflow + Titanic EDA notebook ([docs](docs/phase-0-python/06-jupyter.md), [memories](memories/lessons/01-06-jupyter.md)). Артефакт: [`notebooks/titanic_eda.ipynb`](notebooks/titanic_eda.ipynb).
- **Урок 07** — Git-for-ML: nbstripout, ML gitignore, LFS/branching (deferred to Фази 2 коли з'явиться реальна модель) ([docs](docs/phase-0-python/07-git-for-ml.md), [memories](memories/lessons/01-07-git-for-ml.md))

## Пройдено — Фаза 1

- **Урок 01** — Вектори, dot product, cosine similarity ([docs](docs/phase-1-math/01-vectors.md), [memories](memories/lessons/02-01-vectors.md), [код](code/phase-1/01_vectors.py))
- **Урок 02** — Матриці як перетворення, множення, некомутативність, transpose/inverse ([docs](docs/phase-1-math/02-matrices.md), [memories](memories/lessons/02-02-matrices.md), [код](code/phase-1/02_matrices.py), [візуалізація](code/phase-1/02b_matrices_viz.py))
- **Урок 03** — Власні значення/вектори (eigenvalues/eigenvectors), звʼязок з PCA ([docs](docs/phase-1-math/03-eigen.md), [memories](memories/lessons/02-03-eigen.md), [код](code/phase-1/03_eigen.py), [візуалізація](code/phase-1/03b_eigen_viz.py))
- **Урок 04** — Похідні, часткові похідні, градієнт, chain rule; вивів `∂L/∂w`, `∂L/∂b` для MSE ([docs](docs/phase-1-math/04-derivatives-gradients.md), [memories](memories/lessons/02-04-derivatives-gradients.md), [код](code/phase-1/04_derivatives.py))
- **Урок 05** — Градієнтний спуск з нуля: scalar GD, learning rate heuristics, лінійна і multiple regression, нормалізація ([docs](docs/phase-1-math/05-gradient-descent.md), [memories](memories/lessons/02-05-gradient-descent.md), [код](code/phase-1/05_gradient_descent.py))

## Пройдено — Фаза 2

- **Урок 01** — sklearn fundamentals: train/test split, Pipeline, fit/transform/predict, data leakage, R² ([docs](docs/phase-2-classical-ml/01-sklearn-fundamentals.md), [memories](memories/lessons/03-01-sklearn-fundamentals.md), [код](code/phase-2/01_sklearn_fundamentals.py))
- **Урок 02** — Лінійна регресія sklearn: closed-form vs GD, `.coef_`/R², scaling, multicollinearity ([docs](docs/phase-2-classical-ml/02-linear-regression.md), [memories](memories/lessons/03-02-linear-regression.md), [код](code/phase-2/02_linear_regression.py))
- **Урок 03** — Логістична регресія: sigmoid, decision boundary, `.predict()`/`.predict_proba()`, `ColumnTransformer`+`Pipeline`, знак `.coef_`, accuracy на незбалансованих класах ([docs](docs/phase-2-classical-ml/03-logistic-regression.md), [memories](memories/lessons/03-03-logistic-regression.md), [код](code/phase-2/03_logistic_regression.py), датасет Telco Customer Churn у `data/raw/`)
- **Урок 04** — Метрики класифікації: confusion matrix, precision/recall/F1, ROC-AUC, threshold tuning ([docs](docs/phase-2-classical-ml/04-classification-metrics.md), [memories](memories/lessons/03-04-classification-metrics.md), [код](code/phase-2/04_classification_metrics.py))
- **Урок 05** — Дерева рішень + Random Forest: overfitting (deep vs shallow tree), bagging/random feature subsets/голосування, `feature_importances_` + пастка корельованих фіч, чому деревам не потрібен scaling ([docs](docs/phase-2-classical-ml/05-trees-random-forest.md), [memories](memories/lessons/03-05-trees-random-forest.md), [код](code/phase-2/05_1_trees_random_forest.py)). Перепройдено 30.07 після втрати записів першого проходу.

## Portfolio-об'єкти (що народиться пізніше, природно)

Не робимо синтетичні capstone-и. Реальні portfolio-piece з'являться коли:

1. **ML на agro (ФІНАЛЬНЕ ЗАВДАННЯ, 2026-07-18)** — прогнозне керування поливом теплиць. Повна архітектура вже спроєктована в окремому проєкті: [`/Users/martyn/development/agro/docs/greenhouse_architecture.md`](/Users/martyn/development/agro/docs/greenhouse_architecture.md). Система: LoRa P2P між базою (мозок) і вузлами теплиць (ESP32 + сенсори + клапан), Етапи 1-3 — автоматика на порогах + телеметрія + масштаб (без ML), **Етап 4 — ML-шар** (це і є наш capstone). Ключове для планування Фази 2-3:
   - **Дані:** телеметрія (temp, hum_air, hum_soil, valve-стан) + зовнішній погодний прогноз (API) + **дії системи** (полив/вікна) як фічі — confounding вже вирішений архітектурно (система сама логує свої дії, тому "похолодало бо похмуро" відділяється від "похолодало бо відкрили вікно").
   - **Задача:** прогноз локальних умов + рекомендаційне керування ("не лий — завтра дощ", "відкрий вікно щоб втримати 24°") — регресія/прогнозування часових рядів, потім перехід у recommendation/control.
   - **Критично:** train/test split **по часу**, не випадковий (це вже зафіксовано в самій архітектурі документа — уникнення data leakage).
   - Дані ще не назбирались (Етапи 1-3 у процесі) — тому цей capstone чекає на реальну телеметрію з теплиць, не блокує Фазу 2 (там практикуємось на інших реальних даних, agro підключиться коли буде історія).
2. **ML на власних даних** — trading history, gym progress, GitHub-репо аналіз, будь-що персональне. Головне — питання яке ти сам хочеш відповісти.
3. **Kaggle competition з реальним leaderboard-фінішем** — не просто "скачав датасет", а серйозна конкуренція.

Ці об'єкти виникнуть на маркерах Фази 2 (перша модель, feature engineering, hyperparameter tuning) — тоді ж і відкриємо `exp/` гілки та LFS з Уроку 07.

---

*Оновлюй цей файл після кожного уроку: перекидай завершене в "Пройдено" з посиланням, ставиш новий "Наступний крок".*
