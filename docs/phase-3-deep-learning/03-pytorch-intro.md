# 03 — PyTorch: тензори, autograd, nn.Module, optimizer

## Що це

**PyTorch** — фреймворк, який робить автоматично те, що ти вручну виводив і кодував у Уроках 01-02 (chain rule, `dL/dw`, `dL/dz1`, оновлення ваг). Три головні частини:

1. **`torch.Tensor`** — те саме, що `np.array`, тільки з `requires_grad=True` вміє запам'ятовувати кожну операцію над собою і будувати "граф обчислень".
2. **`autograd`** — коли викликаєш `.backward()`, PyTorch проходить цей граф **назад** (той самий chain rule) і рахує градієнти сам.
3. **`nn.Module` + `optimizer`** — готові будівельні блоки для мереж (шари, loss-функції, оновлення параметрів), щоб не писати все руками.

## Для чого

Ручний backprop (Уроки 01-02) показує **як** усе працює під капотом. Але для реальних мереж (сотні шарів, тисячі параметрів) виводити формули руками нереально. PyTorch — стандарт індустрії (разом із TensorFlow/JAX) для всього, що буде далі в курсі: CNN, transformers.

## Розбір

### Autograd на знайомому прикладі

```python
w = torch.tensor(5.0, requires_grad=True)
L = (w - 3.0) ** 2
L.backward()
print(w.grad)   # tensor(4.)
```

Те саме число `4`, яке рахували руками для `dL/dw` при `L(w)=(w-3)²`, `w=5` (Фаза 1, Урок 05). `requires_grad=True` — не про "запам'ятати значення", а про "почни записувати граф операцій над цим тензором". Без нього `.backward()` падає з `RuntimeError: does not require grad and does not have a grad_fn` — графу немає, нема по чому йти назад.

### Оновлення параметрів вручну

```python
with torch.no_grad():
    w -= lr * w.grad
    b -= lr * b.grad
    w.grad.zero_()
    b.grad.zero_()
```

`torch.no_grad()` — офіційний ідіоматичний спосіб (перевірено через документацію PyTorch), не `.data` (старий підхід, що обходить систему автограда). Градієнти в PyTorch **накопичуються** між викликами `.backward()` — після кожного кроку `optimizer`/`w.grad` треба обнулити, інакше на наступній ітерації складеться зі старим значенням.

### nn.Module — клас для мережі

```python
class Neuron(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(1, 1)   # сам створює w, b з requires_grad=True

    def forward(self, x):
        z = self.linear(x)
        return torch.sigmoid(z)
```

`forward` — обов'язкова назва методу: коли пізніше пишеш `model(x)`, PyTorch під капотом сам викликає `forward(x)` (не викликати `.forward()` напряму — `model(x)` йде через `__call__`, який ще й виконує внутрішні хуки бібліотеки).

`nn.Linear(in_features, out_features)` рахує `x @ weight.T + bias` — матричне множення, не поелементне. Це важливо: `x * weight` (поелементно) випадково дав би той самий результат для 1 входу, але зламався б для кількох входів — там треба **сума** `w1*x1 + w2*x2 + ... + b`, яку дає саме матричне множення, не поелементне.

### Shape-контракт: (batch, features)

`nn.Linear` очікує вхід форми `(batch_size, in_features)` — 2D, не голий скаляр:

```python
x = torch.tensor([[2.0]])   # (1 приклад, 1 фіча), НЕ torch.tensor(2.0)
y = torch.tensor([[1.0]])
```

Та сама конвенція, що в sklearn (`X` завжди `(rows, features)`).

### Optimizer і loss — прибирають ще більше ручного коду

```python
model = Neuron()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
criterion = torch.nn.MSELoss()

for i in range(50):
    optimizer.zero_grad()
    a = model(x)
    L = criterion(a, y)
    L.backward()
    optimizer.step()
```

`optimizer.step()`/`optimizer.zero_grad()` замінюють ручний `with torch.no_grad(): ...` блок для **всіх** параметрів моделі одразу (не по одному, як `w`, `b` окремо). `criterion = nn.MSELoss()` замінює ручний `(a-y)**2`.

Результат ідентичний ручному backprop з Уроку 01-02: `loss: 0.25 → 0.019` за 50 ітерацій.

## Gotchas

- **`self.linear.weight`/`.bias` вручну — легка пастка.** Виглядає ніби працює для 1 входу (поелементне множення випадково збігається з матричним для розміру 1×1), але це не те, що робить `nn.Linear` насправді. Завжди викликати шар як функцію: `self.linear(x)`.
- **`nn.Linear` вимагає 2D вхід.** `torch.tensor(2.0)` (0D) чи `torch.tensor([2.0])` (1D) не підійдуть — потрібно `torch.tensor([[2.0]])` (2D, `(batch, features)`).
- **Градієнти накопичуються.** Забудеш `optimizer.zero_grad()`/`.grad.zero_()` — градієнт з попередньої ітерації додасться до нового, і навчання піде не так.
- **`model(x)`, не `model.forward(x)`.** Функціонально різниці нема для простого прикладу, але `model(x)` — стандарт, бо йде через `__call__` і внутрішні хуки PyTorch.
- **`.data -= ...` vs `with torch.no_grad(): ... -= ...`** — обидва працюють, але офіційна документація показує `torch.no_grad()` як ідіоматичний підхід.

## Джерела

- PyTorch офіційні туторіали (перевірено через `context7`, `/pytorch/tutorials`) — приклад "Fit Polynomial to Sine Wave" з `torch.no_grad()` для ручного оновлення ваг
- "Deep Learning Specialization" (Andrew Ng, Coursera)
- Власний код: `code/phase-3/03_pytorch_autograd.py`
