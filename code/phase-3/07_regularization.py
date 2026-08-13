import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split


train_data = datasets.MNIST(root="./data", train=True, download=True, transform=transforms.ToTensor())
test_data = datasets.MNIST(root="./data", train=False, download=True, transform=transforms.ToTensor())

print(train_data[0][0].shape)

class CNN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = torch.nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3)
        self.conv2 = torch.nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3)
        self.pool = torch.nn.MaxPool2d(2)
        self.flatten = torch.nn.Flatten()
        self.fc = torch.nn.Linear(400, 10)
        self.relu = torch.nn.ReLU()
        self.dropout = torch.nn.Dropout()
        self.bn1 = torch.nn.BatchNorm2d(8)
        self.bn2 = torch.nn.BatchNorm2d(16)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.dropout(x)
        x = self.flatten(x)
        x = self.fc(x)
        return x

model = CNN()
optimazer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = torch.nn.CrossEntropyLoss()
# loader = DataLoader(train_data, batch_size=64, shuffle=True)


train_subset, val_subset = random_split(train_data, [50000, 10000])

train_loader = DataLoader(train_subset, batch_size=64, shuffle=True)
val_loader = DataLoader(val_subset, batch_size=64, shuffle=False)



image = train_subset[0][0].unsqueeze(0)
output = model(image)
print(image.shape)
print(output.shape)

best_val_loss = float('inf')
patience_counter = 0

for epoch in range(15):
    for batch_x, batch_y in train_loader:
        optimazer.zero_grad()
        a = model(batch_x)
        L = criterion(a, batch_y)

        L.backward()
        optimazer.step()

    total_val_loss = 0
    for batch_x, batch_y in val_loader:
        a = model(batch_x)
        val_loss = criterion(a, batch_y)
        total_val_loss += val_loss.item()

    avg_val_loss = total_val_loss / len(val_loader) # одне число на епоху

    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        patience_counter = 0
    else:
        patience_counter += 1

    if patience_counter >= 2:
        print("Early stopping!")
        break

    print(f"Epoch {epoch}, Loss: {L.item()}")


model.eval() # вимикає dropout — оцінка має йти на повній мережі, без випадкового обнулення

test_loader = DataLoader(test_data, batch_size=1000)

correct = 0
for batch_x, batch_y in test_loader:
    a = model(batch_x)
    predict = torch.argmax(a, dim=1)
    correct += (predict == batch_y).sum().item()

acc_test = correct / len(test_data)
print(f"Test Accuracy: {100*acc_test:.4f}%")

correct_train = 0
for batch_x, batch_y in train_loader:
    a = model(batch_x)
    predict = torch.argmax(a, dim=1)
    correct_train += (predict == batch_y).sum().item()

acc_train = correct_train / len(train_subset)
print(f"Train Accuracy: {100*acc_train:.4f}%")


total_params = sum(p.numel() for p in model.parameters())
print(f"Total Test Parameters: {total_params}")
