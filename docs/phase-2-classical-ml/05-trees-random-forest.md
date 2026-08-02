# Урок 05 — Дерева рішень та Random Forest

## Що це

**Decision Tree (дерево рішень)** — модель, що передбачає, ставлячи серію питань «фіча > поріг?». Кожне питання ділить дані на дві гілки, і так доти, доки в листі не залишиться майже чистий клас. На відміну від регресії, дерево не шукає коефіцієнти — воно **будує структуру** під дані (non-parametric).

**Random Forest** — ансамбль із багатьох дерев (у нас 200). Кожне дерево вчиться на випадковій підвибірці даних, і всі разом голосують більшістю. Ідея: багато різних злегка перевчених дерев, усереднені, дають стабільніший прогноз, ніж одне.

## Для чого

Класичний робочий інструмент для табличних даних (як Telco Churn): майже не вимагає препроцесингу (не треба scaling), дає притомний baseline «з коробки», і показує, які фічі важливі. Random Forest — часто перша модель, яку пробують на реальній задачі класифікації/регресії ще до бустингу.

## Розбір

Датасет — Telco Customer Churn (передбачаємо, чи піде клієнт). Будуємо три моделі й порівнюємо.

### Overfitting наживо: глибоке vs обрізане дерево

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# глибоке дерево — без обмеження глибини
deep = DecisionTreeClassifier(random_state=42)
deep.fit(X_train_prepared, y_train)
# train acc: 0.999   test acc: 0.732   ← величезний розрив

# обрізане дерево
shallow = DecisionTreeClassifier(max_depth=4, random_state=42)
shallow.fit(X_train_prepared, y_train)
# train acc: 0.796   test acc: 0.780   ← розрив крихітний
```

| | train | test | розрив |
|---|---|---|---|
| deep tree | 0.999 | 0.732 | **0.27** |
| shallow (`depth=4`) | 0.796 | 0.780 | 0.02 |

**Читання цієї таблиці — суть уроку:**
- Глибоке дерево росте, поки в кожному листі не залишиться майже один приклад → воно **запам'ятовує train-набір разом із випадковим шумом**. Звідси train 0.999. Але на нових даних завчений шум не допомагає → test падає до 0.732. Розрив train≫test — це **overfitting**.
- Обрізане дерево (`max_depth=4`) не встигає завчити шум → гірше на train (0.796), але **краще на test (0.780)**. Модель, гірша на тренуванні, виграє на реальних даних. Тому train-точність сама по собі бреше — **дивимось на test**.

Мовою bias-variance: deep = низький bias, висока variance; shallow = трохи більший bias, нижча variance.

### Random Forest

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train_prepared, y_train)
# train acc: 0.999   test acc: 0.789   ← найкращий test із трьох
```

| | train | test |
|---|---|---|
| deep tree | 0.999 | 0.732 |
| shallow tree | 0.796 | 0.780 |
| **Random Forest** | **0.999** | **0.789** |

RF має **той самий** train 0.999, що й глибоке дерево, і схожий великий розрив — але виграє на test. Чому?

**Механізм (на одному клієнті).** Візьмемо тестового клієнта, чия правда = «No churn»:
- *Одне глибоке дерево* натрапляє на завчений шумний патерн → каже «Yes» ❌.
- *Random Forest*: 200 дерев, кожне вчилось на іншій підвибірці, тому завчили **різний** шум. На цьому клієнті вони не згодні — голосують, скажімо, 130 «No» vs 70 «Yes». Більшість = «No» ✅. 70 дерев обманулись, але **кожне своїм** шумом, тому вони в меншості.

Ось і весь фокус: випадкові помилки різних дерев **розсипаються й гасять одна одну** при голосуванні, а правильний сигнал — у більшості. Variance падає, bias майже не росте.

Два трюки, що роблять дерева різними (без різноманіття усереднення не працювало б):
- **bagging** (bootstrap aggregating) — кожне дерево на випадковій підвибірці рядків *із поверненням*;
- **random feature subsets** — на кожному спліті дерево бачить лише випадкову підмножину фіч.

### Feature importances + пастка корельованих фіч

```python
import pandas as pd

importances = pd.Series(
    rf_pipe.named_steps["model"].feature_importances_,
    index=rf_pipe.named_steps["preprocess"].get_feature_names_out(),
).sort_values(ascending=False)
```

Топ (скорочено):

| фіча | importance |
|---|---|
| TotalCharges | 0.157 |
| tenure | 0.144 |
| MonthlyCharges | 0.135 |
| Contract_Month-to-month | 0.053 |
| OnlineSecurity_No | 0.032 |
| PaymentMethod_Electronic check | 0.030 |

Домейн-логіка сходиться: місячний контракт (легко піти), малий стаж, відсутність техпідтримки/безпеки — типові кандидати на відхід.

**Пастка.** Дивимось на кореляцію числових фіч:

```
                tenure  MonthlyCharges  TotalCharges
tenure           1.00        0.25          0.83
MonthlyCharges   0.25        1.00          0.65
TotalCharges     0.83        0.65          1.00
```

`TotalCharges ≈ MonthlyCharges × tenure` — це фактично **похідна** фіча, всередині якої вже зашитий стаж. Тому `tenure ↔ TotalCharges = 0.83`: вони несуть майже один сигнал.

Коли дві фічі скорельовані, RF на кожному спліті випадково хапає одну з них → через увесь ліс заслуга за цей **один** сигнал **ділиться** на дві колонки. Наслідок:

> `feature_importances_` **применшує** кожну зі скорельованих фіч. `tenure` показує 0.144, а насправді його вага більша — половина захована в `TotalCharges`. Разом це один сигнал ~0.30, розрізаний навпіл.

Небезпека: подивитись на 0.144 і вирішити «стаж не важливий» → помилково викинути важливу фічу. Якби прибрати `TotalCharges`, importance `tenure` **підскочив** би — він забрав би назад свою половину.

**Важливо не сплутати два поверхи:**
- **Точність моделі (0.789) — справжня.** Кореляція фіч НЕ завищує test-результат; для *прогнозу* RF з корельованими фічами працює нормально.
- Обманює лише **читання таблиці важливості** — і в бік **недооцінки** окремої фічі, не переоцінки моделі.

Правило: `feature_importances_` завжди читаємо **разом із кореляційною матрицею**.

## Gotchas

- **Деревам scaling не потрібен.** Дерево ділить по «фіча > поріг», а масштабування — монотонне перетворення (зберігає порядок), тому розбиття не змінюється. `StandardScaler` у пайплайні дерева нешкідливий, але зайвий. Scaling потрібен лише коли алгоритм *змішує фічі в одну формулу*: відстань (KNN, K-means) або зважена сума (лінійна/логістична регресія, SVM). Ментальна модель: *scaling чіпає модель, тільки якщо вона рахує відстані або зважує коефіцієнти.*
- **`ColumnTransformer` за замовчуванням викидає** колонки, яких немає у списку (`remainder="drop"`). Якщо прибрати `StandardScaler` і лишити тільки `OneHotEncoder` для категоріальних — числові фічі **тихо зникнуть**. Рішення: `("numeric", "passthrough", numeric_cols)` або `remainder="passthrough"`.
- **`feature_importances_` — це масив без назв.** Назви (вже після OneHot) дістаємо через `named_steps["preprocess"].get_feature_names_out()`, інакше не зрозуміти, який рядок якій фічі відповідає.
- **train accuracy сама по собі не інформативна** — і deep tree, і RF дають 0.999. Порівнюй моделі за **test**, не за train і не за розривом.
- **`TotalCharges` у Telco «брудна»** — текст із пробілами для клієнтів зі стажем 0. `pd.to_numeric(..., errors="coerce")` перетворює сміття на `NaN`, далі `df.dropna(subset=["TotalCharges"])` викидає ці рядки (~11 штук). Не забути присвоїти назад: `df = df.dropna(...)`.

## Джерела

- sklearn: [DecisionTreeClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html), [RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- sklearn User Guide: [Feature importance — обережності інтерпретації](https://scikit-learn.org/stable/modules/permutation_importance.html) (permutation importance як надійніша альтернатива при корельованих фічах)
- StatQuest (Josh Starmer): Decision Trees, Random Forests — інтуїція на YouTube.
- Код уроку: `code/phase-2/05_1_trees_random_forest.py`.
