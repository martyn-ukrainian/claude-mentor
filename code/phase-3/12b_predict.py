import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image


from typing import Annotated
from fastapi import FastAPI, File
from fastapi.responses import FileResponse
from pathlib import Path
import io


BASE_DIR = Path(__file__).parent

device = "mps" if torch.backends.mps.is_available() else "cpu"

app = FastAPI()
model = models.resnet18(weights=None)
model.fc = nn.Linear(512, 2)
model.to(device)
model.load_state_dict(torch.load(BASE_DIR / "best_model_2.pt"))
model.eval()

transform = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def read_image(file_bytes):
    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    x = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        probs = torch.softmax(model(x)[0], dim=-1)

    return probs

@app.post("/predict")
async def predict(file: Annotated[bytes, File()]):
    if not file:
        return {"message": "No file sent"}
    else:
        probs = read_image(file)
        return {"cat": float(probs[0]), "dog": float(probs[1])}

@app.get("/info")
async def info():
    return {"device": device, "input_size": "224x224 (resize + center crop)"}


@app.get("/")
async def main():
    return FileResponse(BASE_DIR / "static" / "index.html")
