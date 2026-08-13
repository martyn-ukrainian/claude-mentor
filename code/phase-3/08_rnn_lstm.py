import torch

class RNNSum(torch.nn.Module):
    def __init__(self, hidden_size=16):
        super().__init__()
        self.rnn = torch.nn.RNN(input_size=1, hidden_size=hidden_size, batch_first=True)
        self.linear = torch.nn.Linear(hidden_size, 1)

    def forward(self, x):
        output, hidden = self.rnn(x)
        x = self.linear(hidden.squeeze(0))

        return x

model = RNNSum()
criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

def train_epoch(x, y):
    for epoch in range(100):
        for batch_x, batch_y in zip(x, y):
            optimizer.zero_grad()
            output = model(batch_x)
            loss = criterion(output, batch_y)
            loss.backward()
            optimizer.step()

        if epoch % 10 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item()}")

X = torch.randint(0, 10, (1000, 5))
X = X.unsqueeze(-1).float()
y = X.sum(dim=1)

output = model(X)
print(X.shape)
print(y.shape)
# print(output)
train_epoch(X, y)

x_test = torch.tensor([[1, 2, 3, 4, 5]])
x_test = x_test.unsqueeze(-1).float()

y_test = x_test.sum(dim=1)


print(x_test.shape)
print(y_test.shape)

prediction = model(x_test)
print(f"Prediction: {prediction.item()}, Actual: {y_test.item()}")
