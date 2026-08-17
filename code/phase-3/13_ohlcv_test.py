import yfinance as yf
import torch

SYMBOL = "BTC-USD"
INTERVAL = "1h"
PERIOD = "730d"
WINDOW = 168

df = yf.download(SYMBOL, period=PERIOD, interval=INTERVAL)

print("BTC", df.shape, df.tail(3))

returns = df["Close"].pct_change().dropna()
data = torch.tensor(returns.values, dtype=torch.float32).flatten()

X = torch.stack([data[i:i+WINDOW] for i in range(len(data) - WINDOW)])
X = X.unsqueeze(-1)

y = torch.stack([data[i+WINDOW] for i in range(len(data) - WINDOW)])

n = int(len(X) * 0.8)
X_train, X_test = X[:n], X[n:]
y_train, y_test = y[:n], y[n:]

print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

baseline_mae = y_test.abs().mean()
print(f"Baseline MAE: {baseline_mae:.5f}")

class PricePredictor(torch.nn.Module):
    def __init__(self, hidden_size=32):
        super().__init__()
        self.lstm = torch.nn.LSTM(input_size=1, hidden_size=hidden_size, batch_first=True)
        self.ln = torch.nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        last = out[:, -1, :]
        return self.ln(last).squeeze(-1)

model = PricePredictor()
criterion = torch.nn.L1Loss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(50):
    optimizer.zero_grad()
    output = model(X_train)
    loss = criterion(output, y_train)
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.5f}")

with torch.no_grad():
    pred = model(X_test)
    test_mae = (pred - y_test).abs().mean()

print(f"Baseline MAE: {baseline_mae:.5f}")
print(f"LSTM MAE:     {test_mae:.5f}")
