import torch

w = torch.tensor(5.0, requires_grad=True)

L = (w - 3.0) ** 2

L.backward()

print(w.grad)

def sigmoid(z):
    return 1.0 / (1.0 + torch.exp(-z))


x = torch.tensor(2.0)
y = torch.tensor(1.0)
w = torch.tensor(0.0, requires_grad=True)
b = torch.tensor(0.0, requires_grad=True)
lr = 0.1

for i in range(50):
    z = x * w + b
    a = sigmoid(z)

    L = (a - y) ** 2
    L.backward()

    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad
        w.grad.zero_()
        b.grad.zero_()


    if i % 10 == 0:
        print(L.item())

print("Part 2 ---------------------------------")

class Neuron(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(1, 1)

    def forward(self, x):
        z = self.linear(x)
        a = sigmoid(z)
        return a

model = Neuron()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
criterion = torch.nn.MSELoss()

x = torch.tensor([[2.0]])
y = torch.tensor([[1.0]])
for i in range(50):
    optimizer.zero_grad()
    a = model(x)

    L = criterion(a, y)
    L.backward()
    optimizer.step()

    if i % 10 == 0:
        print(L.item())
