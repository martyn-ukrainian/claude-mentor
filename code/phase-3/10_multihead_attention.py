import torch
import torch.nn as nn

class MultiHeadSelfAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()

        self.query = nn.Linear(embed_dim, embed_dim)
        self.key = nn.Linear(embed_dim, embed_dim)
        self.value = nn.Linear(embed_dim, embed_dim)
        self.output = nn.Linear(embed_dim, embed_dim)

        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads

    def split_heads(self, x):
        return x.view(x.shape[0], -1, self.num_heads, self.head_dim).transpose(1, 2)

    def forward(self, x):
        query = self.split_heads(x=self.query(x))
        key = self.split_heads(x=self.key(x))
        value = self.split_heads(x=self.value(x))

        scores = query @ key.transpose(-2, -1) / (self.head_dim ** 0.5)

        T = scores.shape[-1]

        mask = torch.tril(torch.ones(T, T))
        scores = scores.masked_fill(mask == 0, float('-inf'))

        weights = torch.softmax(scores, dim=-1)
        output = (weights @ value).transpose(1, 2)
        output = output.reshape(output.shape[0], -1, self.head_dim * self.num_heads)

        return self.output(output)

class TransformerBlock(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.attention = MultiHeadSelfAttention(embed_dim, num_heads)
        self.norm1, self.norm2 = nn.LayerNorm(embed_dim), nn.LayerNorm(embed_dim)

        self.ffn = nn.Sequential(
          nn.Linear(embed_dim, embed_dim * 4),
          nn.ReLU(),
          nn.Linear(embed_dim * 4, embed_dim),
        )

    def forward(self, x):
        x = self.norm1(x + self.attention(x))
        x = self.norm2(x + self.ffn(x))
        return x


if __name__ == "__main__":
    mha = MultiHeadSelfAttention(embed_dim=8, num_heads=2)
    tb = TransformerBlock(embed_dim=8, num_heads=2)

    x = torch.randn(1, 3, 8)

    print(tb(x).shape)
    print(mha(x).shape)
