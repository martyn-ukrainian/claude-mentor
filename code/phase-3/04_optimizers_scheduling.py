import torch
from torch.utils.data import TensorDataset, DataLoader

def sigmoid(z):
    return 1 / (1 + torch.exp(-z))

class Neuron(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(1, 1)

    def forward(self, x):
        z = self.linear(x)
        a = sigmoid(z)
        return a

torch.manual_seed(42)
model = Neuron()
optimizer = torch.optim.Adam(model.parameters(), lr=0.1)
criterion = torch.nn.MSELoss()
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)


x = torch.tensor([[2.0], [3.0], [1.0], [4.0]])
y = torch.tensor([[0.0], [1.0], [0.0], [1.0]])

dataset = TensorDataset(x, y)
loader = DataLoader(dataset, batch_size=2, shuffle=True)

n = 0


for epoch in range(21):
    for batch_x, batch_y in loader:
        optimizer.zero_grad()
        a = model(batch_x)
        L = criterion(a, batch_y)
        L.backward()
        optimizer.step()
    scheduler.step()

    if epoch % 5 == 0:
        n += 1
        print(f"Loss {n}: {L.item()}")
