from pathlib import Path
from importlib import import_module

import torch
import torch.nn as nn

BLOCK_SIZE = 64
BATCH_SIZE = 16

EMBED_DIM = 32
NUM_HEADS = 4
N_LAYERS = 2
N_EPOCHS = 5000

LR = 1e-3

files = Path("../../docs/phase-3-deep-learning").glob("*.md")
TransformerBlock = import_module("10_multihead_attention").TransformerBlock

class TinyLM(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_heads, n_layers):
        super().__init__()
        self.token_emb = nn.Embedding(vocab_size, embed_dim)
        self.pos_emb = nn.Embedding(BLOCK_SIZE, embed_dim)
        self.block = nn.Sequential(*[TransformerBlock(embed_dim, num_heads) for _ in range(n_layers)])
        self.head = nn.Linear(embed_dim, vocab_size)

    def forward(self, x):
        tok = self.token_emb(x)
        pos = self.pos_emb(torch.arange(x.shape[1]))

        x = tok + pos
        x = self.block(x)
        x = self.head(x)
        return x


all_text = "".join([f.read_text() for f in files])

print(len(all_text))

chars = sorted(set(all_text))
vocab_size = len(chars)

print(vocab_size)

itos = {index: char for index, char in enumerate(chars)}
stoi = {char: index for index, char in enumerate(chars)}


data = torch.tensor([stoi[ch] for ch in all_text])

print(stoi['а'], itos[0])
print(data[:50])
print("".join(itos[i.item()] for i in data[:50]))

def get_batch():
    ix = torch.randint(0, len(data) - BLOCK_SIZE, (BATCH_SIZE,))
    x = torch.stack([data[i:i+BLOCK_SIZE] for i in ix])
    y = torch.stack([data[i+1:i+BLOCK_SIZE+1] for i in ix])
    return x, y

x, y = get_batch()
print(x.shape, y.shape)


print("".join(itos[i.item()] for i in x[0]))
print("".join(itos[i.item()] for i in y[0]))

model = TinyLM(vocab_size, EMBED_DIM, NUM_HEADS, N_LAYERS)
optimazer = torch.optim.Adam(model.parameters(), lr=LR)
criterion = nn.CrossEntropyLoss()

logits = model(x)

print(logits.shape)

for step in range(N_EPOCHS):
    optimazer.zero_grad()

    x, y = get_batch()
    logits = model(x)
    loss = criterion(logits.reshape(-1, vocab_size), y.reshape(-1))
    loss.backward()
    optimazer.step()

    if step % 100 == 0:
        print(f"step {step}, loss: {loss.item()}")


def generate(start_text, n_chars):
    context = torch.tensor([[stoi[c] for c in start_text]])
    for _ in range(n_chars):
        logits = model(context[:, -BLOCK_SIZE:])
        prob = torch.softmax(logits[0, -1], dim=-1)
        next_char = torch.multinomial(prob, num_samples=1)
        context = torch.cat([context, next_char.view(1, 1)], dim=-1)
    return "".join(itos[i.item()] for i in context[0])


print(generate("Град ", 100))
