import torch

conv = torch.nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, bias=False)

image_2d = [
    [1, 1, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 1, 1],
    [0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0],
]

x = torch.tensor([[image_2d]], dtype=torch.float32)
print(x.shape)

kernel_2d = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1],
]

kernel_tensor = torch.tensor([[kernel_2d]], dtype=torch.float32)
print(kernel_tensor.shape)

conv.weight.data = kernel_tensor

print(conv)


output = conv(x)
print(output)
