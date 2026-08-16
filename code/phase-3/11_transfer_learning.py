import torch
import torch.nn as nn
from torchvision import models, transforms, datasets
from torch.utils.data import Subset, DataLoader

N_EPOCH = 3
model = models.resnet18(weights="IMAGENET1K_V1")

sum_params = sum(p.numel() for p in model.parameters())
print(sum_params)

model.requires_grad_(False)
model.fc = nn.Linear(512, 2)

trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(trainable)

transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

train_data = datasets.CIFAR10(root="./data", train=True, download=True, transform=transform)
test_data = datasets.CIFAR10(root="./data", train=False, download=True, transform=transform)


сat_dog_idx = [i for i, label in enumerate(train_data.targets) if label in (3, 5)]
test_cat_dog_idx = [i for i, label in enumerate(test_data.targets) if label in (3, 5)]

train_subset = Subset(train_data, сat_dog_idx[:500])
test_subset = Subset(test_data, test_cat_dog_idx[:200])

train_loader = DataLoader(train_subset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_subset, batch_size=32)

print(len(train_subset), len(test_subset))

print([train_data.targets[i] for i in сat_dog_idx[:10]])
print(len(сat_dog_idx), сat_dog_idx[:10])

optimizer = torch.optim.Adam(model.fc.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

for epoch in range(N_EPOCH):
    for batch_x, batch_y in train_loader:
        batch_y = (batch_y == 5).long()
        optimizer.zero_grad()
        logits = model(batch_x)
        loss = criterion(logits, batch_y)
        loss.backward()
        optimizer.step()

    print(f"Loss {epoch}: {loss.item()}")

correct = 0
with torch.no_grad():
    for batch_x, batch_y in test_loader:
        batch_y = (batch_y == 5).long()
        logits = model(batch_x)
        predict = logits.argmax(dim=1)
        correct += (predict == batch_y).sum().item()

accuracy = correct / len(test_subset)

print(f"Test Accuracy: {accuracy:.4f}")

total_params = sum(p.numel() for p in model.parameters())
print(f"Total Parameters: {total_params}")
