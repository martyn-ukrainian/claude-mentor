# PROGRESS

**Поточна фаза:** Фаза 0 ✅ **completed** → Фаза 1 (математика) **на паузі, 6/8 уроків** → **Фаза 2 ✅ completed, 9/9** → **Фаза 3 (Deep Learning) — старт 2026-08-09, Урок 05 пройдено, Урок 06 В ПРОЦЕСІ (технічна частина готова, Feynman відкладено на завтра)**

**Рішення від 2026-08-12/13 (Урок 06 Фази 3 — В ПРОЦЕСІ, НЕ завершений):** Перша повна CNN на MNIST — архітектура (`Conv→ReLU→Pool→Conv→ReLU→Pool→Flatten→Linear`), тренування, оцінка, порівняння з `Linear`-бейзлайном — усе технічно зроблено і працює. Результат: **CNN 98.04-98.17% accuracy / 5,258 параметрів, Linear MLP 96.63-97.09% / 101,770 параметрів** — CNN краща і майже в 19 разів економніша, пряме числове підтвердження weight sharing з Уроку 05. Другу модель (`LinearMLP`) і весь її training/eval цикл студент написав **повністю сам**, без підказок — сильний сигнал трансферу навички. Студент чесно сказав "втомився" перед Feynman-питанням ("чому CNN з меншою кількістю параметрів дала кращий результат") — **свідомо відклав синтез на завтра, з невеликим повтором спочатку.** Retention-check на старті сесії (Linear, weight-sharing) показав що обидва потребують scaffolding, ще не стійкі. Деталі, повний список технічних уловів і план завтрашнього старту — `memories/lessons/04-06-cnn-mnist.md`. Код: `code/phase-3/06_cnn_mnist.py`, drill-задачі для розігріву: `code/phase-3/retrieval_weight_sharing.py`. **Завтра почати з:** невеликого retrieval (`retrieval_weight_sharing.py`), потім Feynman-питання про Урок 06, і тільки після нього — `docs/phase-3-deep-learning/06-cnn-mnist.md` + фінальний запис у `profile.md`/`PROGRESS.md` про закриття Уроку 06.

**Рішення від 2026-08-12 (Урок 05 Фази 3 пройдено — CNN: механіка згортки + похідні через weight sharing):** Перша тема з новою геометричною семантикою (CNN), механіка виявилась легшою за прогноз — формулу розміру виходу (`(H-K)/S+1`) вивів сам до підказки, edge detector і max pooling gradient з першої спроби. Найважчий момент — вербальний синтез "чому градієнт для спільної ваги сумується" (weight sharing), закрито конкретними числами + бінарним питанням. `nn.Conv2d` перевірений проти ручного розрахунку — збіглось. **Нова методологічна знахідка:** текстовий Feynman у кінці сесії розсипався сильніше звичного (загубив навіть `Linear`), але voice-сесія одразу після (monologue-flow, що переріс у діалог) відновила синтез того самого дня — voice реально виправляв розуміння в моменті, не тільки перевіряв. Деталі — `memories/lessons/04-05-cnn-convolution.md`, `memories/profile.md`, студентський урок — `docs/phase-3-deep-learning/05-cnn-convolution.md`. Код: `code/phase-3/05_cnn_convolution.py`. Voice flow: `voice/flows/eli5-ua_ml-phase3-05-cnn-convolution_monologue.json`. **Наступний крок — Урок 06 Фази 3** (повна CNN на MNIST), почати з перевірки retention `Linear` (несподівано забув на фінальному синтезі) і weight-sharing на новому прикладі.

**Мета-сесія від 2026-08-12 (04b, нічна, без коду):** студент сам ініціював концептуальне закріплення «навіщо була Фаза 2, якщо є PyTorch». Три нитки: sklearn vs PyTorch (різниця — хто робить X, не «хто вчиться сам»; «спочатку бейзлайн»), таргет для propensity-задачі (таргет / фільтр рядків / бізнес-пріоритезація — дійшов через 3 сходинки), «звідки в нейрона сенс» (representation learning — Feynman закрив чисто: «сенс заповнюється під тиском градієнта і loss»). Новий misconception на радар: «DL = самонавчання, класика = ми генеруємо» (сплив двічі). 3 нові пункти у voice-черзі. Деталі — `memories/lessons/04-04b-meta-sklearn-vs-pytorch.md`, студентський урок — `docs/phase-3-deep-learning/04b-sklearn-vs-pytorch-context.md`. Наступний крок без змін — Урок 05 Фази 3.

**Рішення від 2026-08-11 (Урок 04 Фази 3 пройдено, та сама сесія що Уроки 02-03):** SGD vs Adam — чесне порівняння через `torch.manual_seed(42)` (однаковий старт), `Adam` на порядки швидший біля мінімуму. `StepLR` LR scheduling — емпірично виявили, що занадто раннє/агресивне зменшення `lr` **шкодить** збіжності (не сліпо довіряти гіперпараметру). `TensorDataset`/`DataLoader`, правильна структура `for epoch → for batch` (переплутав вкладеність двічі, третя спроба з прямим кодом спрацювала), `scheduler.step()` на рівні епохи. Урок пройшов значно легше/швидше за Уроки 01-03 — жодного тривалого семантичного застрягання, підтвердило прогноз кінця Уроку 03 (новий фреймворк освоюється швидше за математичну семантику). Два самостійні критичні улови без підказки: помітив що scheduler уповільнив тренування; сам вивів `Linear(1,1)` vs `Linear(2,1)` shape-логіку. Деталі — `memories/lessons/04-04-optimizers-scheduling-batching.md`, `memories/profile.md`, студентський урок — `docs/phase-3-deep-learning/04-optimizers-scheduling-batching.md`. Код: `code/phase-3/04_optimizers_scheduling.py`.

**Рішення від 2026-08-11 (Урок 03 Фази 3 пройдено, та сама сесія що Урок 02):** Перше знайомство з PyTorch: `torch.Tensor`+`requires_grad`, `autograd`/`.backward()`, `nn.Module`/`nn.Linear`, `torch.optim.SGD`, `nn.MSELoss`. Перевірено на знайомому прикладі (`L(w)=(w-3)²` дало `grad=4.0`, те саме число що рахували руками годину тому) і на повному перезбиранні градієнтного спуску одного нейрона з Уроку 01 — той самий результат (`loss: 0.25→0.019`). Найважливіший сигнал: **autograd "закрив" емоційно важкий момент сесії** — retention-борги (навіщо градієнт/що таке похідна) підтвердились через інструмент, а не підмінились чорною скринькою. Усі застрягання сьогодні в PyTorch-частині були суто механічні (imports, shape `(batch,features)`, `self.linear(x)` vs ручний доступ до `.weight`), жодних семантичних. Два API-твердження перевірено через `context7`, не з пам'яті (`torch.no_grad()` vs `.data`, `model(x)` vs `model.forward(x)`). Деталі — `memories/lessons/04-03-pytorch-intro.md`, `memories/profile.md`, студентський урок — `docs/phase-3-deep-learning/03-pytorch-intro.md`. Код: `code/phase-3/03_pytorch_autograd.py`. **PyTorch додано в залежності проєкту (`uv add torch`).**

**Рішення від 2026-08-11 (Урок 02 Фази 3 пройдено):** Спочатку закрито борг Уроку 01 — retention-check "навіщо градієнт", **текстом, не голосом як планувалось** (перехід на вже знайомий приклад `L(w)=(w-3)²` з Фази 1 Уроку 05 замість нового абстрактного). Потім сам Урок 02: ReLU (`max(0,z)`, чому рятує від vanishing gradient sigmoid) + виведення формули `dL/dz1 = dL/dz2·w2·a1(1-a1)` для backprop через два шари + код градієнтного спуску для 2-шарової мережі (`loss: 0.25→0.082` за 40 ітерацій). Найважливіший новий сигнал — **рецидив "що таке похідна"**, базового терміну з Фази 1 Уроку 04, довелось повністю відновлювати з нуля. Дуже щільна сесія (4 окремі застрягання), жодне не форсоване. Деталі — `memories/lessons/04-02-relu-backprop-mlp.md`, `memories/profile.md`, студентський урок — `docs/phase-3-deep-learning/02-relu-backprop.md`. Код: `code/phase-3/02_rely.py`, `code/phase-3/02b_backprop_mlp.py`.

**Рішення від 2026-08-09 (старт Фази 3, Урок 01 пройдено):** Свідомо підтверджено початок Фази 3 (Deep Learning), звірено з ROADMAP.md — `set-phase.sh phase-3` виконано. Урок 01 (перцептрон, шар через матрицю, MLP forward pass, chain rule refresher, ручний вивід і код градієнтного спуску для одного нейрона) — пройдено. Найважливіший момент: "навіщо градієнт" (семантика, не механіка) виявився найабстрактнішим концептом курсу дотепер, НЕ закрився попри 4 ескалації тактик в одній сесії (текст → аналогія → емпірична демонстрація → графік). Студент сам сказав "складно", сесію зупинили чесно, без форсування. **Закрито 11.08 у наступній сесії, текстом** — див. рішення вище.

**Математичний борг Фази 1 перед Фазою 3 — частково підхоплено.** Chain rule (Урок 04 Фази 1) виявився повністю забутим, відновлений just-in-time на конкретному прикладі в Уроці 01 Фази 3. Matrix calculus для повного backprop мережі (не одного нейрона) — ще попереду, у наступному уроці.

**Рішення від 2026-08-08 (Фаза 2 завершена):** Урок 09 (GridSearchCV, PCA, K-Means) закрито — останній урок Фази 2. Усі 9 уроків класичного ML пройдено: sklearn fundamentals → регресія → метрики → дерева/RF → gradient boosting → KNN/SVM/NB → регуляризація/CV → tuning/PCA/K-Means. Синтетичний capstone свідомо пропущений (рішення 13.07) — реальний portfolio-об'єкт (agro, коли з'явиться телеметрія) чекає окремо, не блокує перехід до Фази 3. **Найважливіша подія уроку 09 — найдовше закриття концептуального боргу за весь курс: PCA/eigenvalue-семантика** (тягнеться з Фази 1 Уроку 03, 18.07), закрито через триптих трьох контрастних реальних прикладів кореляції. Деталі — `memories/lessons/03-09-feature-engineering-tuning-pca-kmeans.md`, `memories/profile.md`.

**Наступний крок — Фаза 3 (Deep Learning), коли свідомо підтверджено старт** (не автоматично, звірити з ROADMAP.md і власним рішенням студента). Математичний борг перед Фазою 3: matrix calculus для backprop (розширення chain rule Фази 1 Уроку 04), і, ймовірно, E[X]/Var/розподіли (недозакритий борг Фази 1 Уроку 07) — підхопити just-in-time, як робилось увесь курс.

**Звірка боргу Фази 1 (2026-08-08):** Урок 06 Фази 1 (loss functions, MSE+cross-entropy) — ЗАКРИТО, JIT у Уроці 06 Фази 2 (Gradient Boosting). Урок 07 Фази 1 (розподіли/E[X]/Var/Байєс) — ЧАСТКОВО, Байєс закрито JIT у Уроці 07 Фази 2 (Naive Bayes, реальні числа Telco), але E[X]/Var/розподіли — ні, це той самий z-score/std борг з Фаз 0-1 (3+ рази). Урок 08 Фази 1 (capstone "лінійна регресія з нуля") — ймовірно зайвий, дублює вже зроблене в Уроці 05 Фази 1 (ручний GD + regression). **Наступна хвиля математики — Фаза 3 (Deep Learning):** matrix calculus для backprop (розширення chain rule Уроку 04 на вектори/тензори), і, ймовірно, розподіли/E[X]/Var природно спливуть (weight init, dropout=Bernoulli, batch norm statistics) — той самий JIT-принцип, не окрема math-фаза.

**Рішення від 2026-08-08 (Урок 08 закрито):** Overfitting/underfitting, L1/L2 регуляризація, крос-валідація. Ключовий момент — CV на реальних числах "перевернув" висновок з одного train_test_split (C=1 sweet spot виявився статистично невідрізнимим від C=100, різниця mean << std). Феinman-синтез вийшов за межі мінімуму — студент сформулював загальний методологічний принцип (перевіряти висновки під різними параметрами). Два самостійні debug-улови (DRY-рефакторинг, знайшов bug з "прилиплою" змінною в циклі).

**Рішення від 2026-08-08 (Урок 07 закрито):** KNN/SVM/Naive Bayes. Scaling-логіка закріплена (обов'язковий для KNN/SVM, на відміну від дерев). JIT-закриття боргу Фази 1 (теорема Байєса, на реальних числах Telco). Naive Bayes досліджено найглибше за весь курс — 4 варіанти (Gaussian усі фічі, Gaussian тільки numeric, Bernoulli, VotingClassifier ансамбль), включно з самостійним архітектурним питанням студента про межі ColumnTransformer. Голосовий канал вперше використано в новому форматі (`voice/bot_cli.py`, TTS-piper видалено з проєкту раніше в сесії). Феinman частково зійшовся — правильний механізм застосований не до того явища, закрито прямим поясненням.

**Рішення від 2026-08-07 (Урок 06 — синтез спочатку не зійшовся, потім зійшовся сам):** Урок 06 (Gradient Boosting) пройдено з перервами протягом тижня (31.07 loss functions → 04.08 → 07.08 boosting-механіка). Усі окремі кроки (cross-entropy на числах, механіка залишків, чому `n_estimators` небезпечний у GB на відміну від RF, `max_features`-пастка importance) пройдено правильно, часто самостійно. Перший Feynman-синтез студент сам чесно назвав "не зрозумів насправді що вивчали" — але одразу після цього попросив коротке пряме пояснення ще раз і **сам вивів тонший інсайт** (пізні дерева GB ганяються за дедалі меншим залишком, де дедалі більша частка шуму, не сигналу — звідси overfitting з кількістю дерев). Урок закрито як CLOSED. Деталі й нова тактика (пряме пояснення-місток як ескалація, коли guided-discovery не зшиває матеріал) — `memories/lessons/03-06-gradient-boosting.md`, `memories/profile.md`.

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

**Де зупинились:** Фаза 3 стартувала 09.08, Уроки 01-05 пройдено, **Урок 06 (CNN на MNIST) В ПРОЦЕСІ** — технічна частина повністю зроблена і працює (CNN 98%+ accuracy, 5258 параметрів vs Linear MLP 97%, 101770 параметрів; другу модель студент написав повністю сам), але **Feynman-синтез свідомо відкладений студентом на наступну сесію** ("втомився, завтра з невеликого повтору"). **Наступний крок — ЗАВЕРШИТИ Урок 06, НЕ починати Урок 07:** (1) невеликий retrieval-розігрів `code/phase-3/retrieval_weight_sharing.py`, (2) Feynman-питання "чому CNN з ~19x меншою кількістю параметрів дала кращий результат за Linear MLP", (3) тільки після цього — `docs/phase-3-deep-learning/06-cnn-mnist.md` + фінальні записи в `profile.md`/`PROGRESS.md` про закриття уроку. Деталі — `memories/lessons/04-06-cnn-mnist.md`. Уроки 02-05 пройшли значно легше за Урок 01 (механіка/API vs математична семантика) — підтверджений патерн, включно з CNN. Retention-перевірка "форвард vs backward pass" закрита (12.08); "epoch/batch nesting" і "tensor shape nesting" (структурний, не семантичний паттерн, 3+ підтвердження, знову спливло в Уроці 06 — пропущений `relu`/`pool` у forward) — у черзі `voice-retrieval-queue.md`. Weight-sharing chain rule (символьна підстановка) — досі НЕ стійке, потребувало числової похибки-костиля вдруге поспіль (Урок 05 і старт Уроку 06) — топ-кандидат для завтрашнього розігріву. Уроку 06 Фази 2 (Gradient Boosting) і PCA-семантики (Урок 09 Фази 2) retention-check — досі бажаний, у черзі. **Дрон-проєкт "Колонія"** (`~/development/colony`, див. пам'ять) — потенційний реальний datasеt для CNN-блоку/Проєкту 2, звірити коли дійдемо туди.

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
- **Урок 06** — Gradient Boosting: cross-entropy/log-loss на числах, механіка залишків, чому `n_estimators` небезпечний у GB (на відміну від RF), `max_features`-пастка importance (RF `sqrt` vs GB `None`) ([docs](docs/phase-2-classical-ml/06-gradient-boosting.md), [memories](memories/lessons/03-06-gradient-boosting.md), [код](code/phase-2/06_gradient_boosting.py)). Перший синтез не зійшовся, другий (одразу після) — зійшовся самостійно й глибше мінімуму.
- **Урок 07** — KNN, SVM, Naive Bayes: scaling обов'язковий (відстані/добутки), теорема Байєса на реальних числах (JIT-закриття боргу Фази 1), 4 варіанти Naive Bayes (Gaussian/Bernoulli/VotingClassifier), самостійне архітектурне питання про межі ColumnTransformer ([docs](docs/phase-2-classical-ml/07-knn-svm-naive-bayes.md), [memories](memories/lessons/03-07-knn-svm-naive-bayes.md), [код](code/phase-2/07_knn_svm_naive_bayes.py), [код VotingClassifier](code/phase-2/07_nb_voiting_classifier.py)).
- **Урок 08** — Overfitting/underfitting, L1/L2 регуляризація, крос-валідація: геометрія L1 vs L2, немонотонна поведінка L1 при мультиколінеарності, CV "перевернув" висновок з одного спліту ([docs](docs/phase-2-classical-ml/08-overfitting-regularization-cv.md), [memories](memories/lessons/03-08-overfitting-regularization-cv.md), [код](code/phase-2/08_overfitting_regularization_cv.py)).
- **Урок 09** — GridSearchCV, PCA, K-Means (останній урок Фази 2): автоматизація tuning, PCA-стиснення скорельованих фіч + eigenvalue-семантика (триптих контрастних прикладів закрив старий борг Фази 1), K-Means знайшов реальний churn-ризик без y ([docs](docs/phase-2-classical-ml/09-feature-engineering-tuning-pca-kmeans.md), [memories](memories/lessons/03-09-feature-engineering-tuning-pca-kmeans.md), [код](code/phase-2/09_feature_engineering_tuning_pca.py)).

## Пройдено — Фаза 3

- **Урок 01** — Перцептрон: нейрон (зважена сума+bias+sigmoid), шар через матрицю, MLP forward pass, chain rule refresher, ручний вивід і код градієнтного спуску для одного нейрона ([docs](docs/phase-3-deep-learning/01-perceptron-neuron.md), [memories](memories/lessons/04-01-perceptron-neuron-basics.md), [код](code/phase-3/01_perceptron.py)). "Навіщо градієнт" — закрито 11.08, див. Урок 02.
- **Урок 02** — ReLU + backprop для мережі з двох шарів: `relu(z)=max(0,z)`, чому рятує від vanishing gradient sigmoid, виведення `dL/dz1 = dL/dz2·w2·a1(1-a1)`, повний градієнтний спуск для 2-шарової мережі ([docs](docs/phase-3-deep-learning/02-relu-backprop.md), [memories](memories/lessons/04-02-relu-backprop-mlp.md), [код ReLU](code/phase-3/02_rely.py), [код backprop](code/phase-3/02b_backprop_mlp.py)).
- **Урок 03** — PyTorch: тензори, autograd, nn.Module, optimizer — перше знайомство з фреймворком, повний ідіоматичний pipeline перевірений проти ручного backprop ([docs](docs/phase-3-deep-learning/03-pytorch-intro.md), [memories](memories/lessons/04-03-pytorch-intro.md), [код](code/phase-3/03_pytorch_autograd.py)).
- **Урок 04** — Оптимізатори (SGD/Adam), LR scheduling, batching: чесне порівняння SGD/Adam через `manual_seed`, `StepLR` (з висновком "може зашкодити"), `TensorDataset`/`DataLoader`, `for epoch → for batch` структура ([docs](docs/phase-3-deep-learning/04-optimizers-scheduling-batching.md), [memories](memories/lessons/04-04-optimizers-scheduling-batching.md), [код](code/phase-3/04_optimizers_scheduling.py)).
- **Мета-сесія 04b** — sklearn vs PyTorch (хто робить X), таргет/фільтр/пріоритезація для propensity, звідки в нейрона сенс (representation learning) — концептуальне закріплення без коду ([docs](docs/phase-3-deep-learning/04b-sklearn-vs-pytorch-context.md), [memories](memories/lessons/04-04b-meta-sklearn-vs-pytorch.md)).
- **Урок 05** — CNN: механіка 1D/2D згортки, edge detector, формула розміру виходу (вивів сам), похідна через спільну вагу (weight sharing, ключова ідея уроку), градієнт через max pooling, `nn.Conv2d` звірений з ручним розрахунком ([docs](docs/phase-3-deep-learning/05-cnn-convolution.md), [memories](memories/lessons/04-05-cnn-convolution.md), [код](code/phase-3/05_cnn_convolution.py)).

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
