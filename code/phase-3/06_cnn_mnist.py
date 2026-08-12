from torchvision import datasets, transforms
import torch.nn as nn
import torch
from torch.utils.data import DataLoader

train_data = datasets.MNIST(root="./data", train=True, download=True, transform=transforms.ToTensor())
test_data = datasets.MNIST(root="./data", train=False, download=True, transform=transforms.ToTensor())

print(len(train_data))
print(len(test_data))

print(train_data[0][0].shape)

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3)
        self.pool = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3)
        self.flatten = nn.Flatten()
        self.fc = nn.Linear(400, 10)
        self.relu = torch.relu

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.flatten(x)
        x = self.fc(x)

        return x

model = CNN()
optimazer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()
loader = DataLoader(train_data, batch_size=64, shuffle=True)


image = train_data[0][0].unsqueeze(0)
output = model(image)
print(image.shape)
print(output.shape)

n = 0

for epoch in range(3):
    for batch_x, batch_y in loader:
        optimazer.zero_grad()
        a = model(batch_x)
        L = criterion(a, batch_y)
        L.backward()
        optimazer.step()

    n += 1
    print(f"Loss {n}: {L.item()}")

test_loader = DataLoader(test_data, batch_size=1000)

correct = 0
for batch_x, batch_y in test_loader:
    a = model(batch_x)
    predict = a.argmax(dim=1)
    correct += (predict == batch_y).sum().item()

accuracy = correct / len(test_data)
print(f"Test Accurace: {accuracy:.4f}")



class LinearMLP(nn.Module):
    def __init__(self):
        super().__init__()

        self.fl = nn.Flatten()
        self.l1 = nn.Linear(784, 128)
        self.relu = torch.relu
        self.l2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.fl(x)
        x = self.l1(x)
        x = self.relu(x)
        x = self.l2(x)

        return x

model2 = LinearMLP()
optimazer2 = torch.optim.Adam(model2.parameters(), lr=0.001)
criterion2 = nn.CrossEntropyLoss()

n2 = 0
for epoch in range(3):
    for batch_x, batch_y in loader:
        optimazer2.zero_grad()
        a = model2(batch_x)
        L = criterion2(a, batch_y)
        L.backward()
        optimazer2.step()

    n2 += 1
    print(f"Loss {n2}: {L.item()}")

test_loader = DataLoader(test_data, batch_size=1000)

cor2 = 0

for batch_x, batch_y in test_loader:
    a2 = model2(batch_x)
    predict2 = a2.argmax(dim=1)
    cor2 += (predict2 == batch_y).sum().item()

accuracy2 = cor2 / len(test_data)
print(f"Test Accuracy 2: {accuracy2:.4f} %")

total_params = sum(p.numel() for p in model.parameters())
total_params2 = sum(p.numel() for p in model2.parameters())

print(f"Total Parameters: {total_params}")
print(f"Total Parameters 2: {total_params2}")
