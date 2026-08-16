import torch
import torch.nn as nn
from torchvision import models, transforms, datasets
from torch.utils.data import Subset, DataLoader, random_split

N_EPOCH = 10
N_TRAIN_DATA = 500
N_VAL = N_TRAIN_DATA // 5

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

train_subset = Subset(train_data, сat_dog_idx[:N_TRAIN_DATA])
test_subset = Subset(test_data, test_cat_dog_idx[:200])

train_part, val_part = random_split(train_subset, [N_TRAIN_DATA - N_VAL, N_VAL])

train_loader = DataLoader(train_part, batch_size=32, shuffle=True)
val_loader = DataLoader(val_part, batch_size=32, shuffle=False)
test_loader = DataLoader(test_subset, batch_size=32)


print(len(train_subset), len(test_subset))

print([train_data.targets[i] for i in сat_dog_idx[:10]])
print(len(сat_dog_idx), сat_dog_idx[:10])

optimizer = torch.optim.Adam([p for p in model.parameters() if p.requires_grad], lr=1e-3)
criterion = nn.CrossEntropyLoss()

best_val_loss = float("inf")
patience_counter = 0

for epoch in range(N_EPOCH):
    for batch_x, batch_y in train_loader:
        batch_y = (batch_y == 5).long()
        optimizer.zero_grad()
        logits = model(batch_x)
        loss = criterion(logits, batch_y)
        loss.backward()
        optimizer.step()

    total_val_loss = 0
    with torch.no_grad():
        for val_x, val_y in val_loader:
            val_y = (val_y == 5).long()
            val_logits = model(val_x)
            val_loss = criterion(val_logits, val_y)
            total_val_loss += val_loss.item()

    avg_val_loss = total_val_loss / len(val_loader)

    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        patience_counter = 0
        torch.save(model.state_dict(), "best_model.pt")
    else:
        patience_counter += 1

    if patience_counter >= 2:
        print("Early stopping!")
        break

    print(f"Epoch {epoch}: train {loss.item():.4f}, val {avg_val_loss:.4f}")

model.load_state_dict(torch.load("best_model.pt"))
model.eval()


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
