
import torch
import torch.nn as nn


class SelfAttention(nn.Module):
    def __init__(self, embed_dim):
        super().__init__()
        self.query = nn.Linear(embed_dim, embed_dim)
        self.key = nn.Linear(embed_dim, embed_dim)
        self.value = nn.Linear(embed_dim, embed_dim)

        self.embed_dim = embed_dim

    def forward(self, x):
        Q = self.query(x)
        K = self.key(x)
        V = self.value(x)

        scores = Q @ K.transpose(-2, -1)  / (self.embed_dim ** 0.5)
        weights = torch.softmax(scores, dim=-1)
        output = weights @ V

        return output


model = SelfAttention(embed_dim=4)
x = torch.randn(1, 3, 4)

output = model(x)
print(output)
print(output.shape)
