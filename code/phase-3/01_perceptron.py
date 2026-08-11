import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def neuron_forward(x, w, b):
    z = np.dot(x, w) + b
    a = sigmoid(z)
    return a

def layer_forward(x, W, b):
    z = np.dot(W, x) + b
    a = sigmoid(z)
    return a

x = np.array([1, 2])
w = np.array([0.5, -0.5])
b = 0.1

w2 = np.array([0.2, 0.8])
b2 = -0.2

W = np.array([w, w2])
B = np.array([b, b2])

W2 = np.array([[1, -1]])
B2 = np.array([0])

sigmoid_z = neuron_forward(x, w, b)
hidden_output = layer_forward(x, W, B)
output = layer_forward(hidden_output, W2, B2)

print(f"hidden output = {hidden_output}")
print(f"output = {output}")


print("---------------------------------------------")

x = 2.0
y = 1.0

w = 0.0
b = 0.0
lr = 0.1

for i in range(50):
  z = np.dot(x, w) + b
  a = sigmoid(z)

  L = (a - y) ** 2
  dL_dz = 2 * (a - y) * a * (1 - a)
  dL_dw = dL_dz * x
  dL_db = dL_dz * 1

  w -= lr * dL_dw
  b -= lr * dL_db

  if i % 10 == 0:
    print(f"iteration {i}, loss = {L}")
