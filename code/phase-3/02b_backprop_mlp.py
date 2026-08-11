import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def neuron_forward(x, w, b):
    return np.dot(x, w) + b

def mlp_gradient_descent(x, y, lr = 0.1):
    w1 = 0.0
    b1 = 0.0
    w2 = 0.0
    b2 = 0.0

    for i in range(50):
        z1 = neuron_forward(x, w1, b1)
        a1 = sigmoid(z1)
        z2 = neuron_forward(a1, w2, b2)
        a2 = sigmoid(z2)

        dL_dz2 = 2 * (a2 - y) * a2 * (1 - a2)
        dL_dz1 = dL_dz2 * w2 * a1 * (1 - a1)
        dL_dw2 = dL_dz2 * a1
        dL_db2 = dL_dz2 * 1
        dL_dw1 = dL_dz1 * x
        dL_db1 = dL_dz1 * 1

        w2 -= lr * dL_dw2
        b2 -= lr * dL_db2
        w1 -= lr * dL_dw1
        b1 -= lr * dL_db1

        L = (a2 - y) ** 2


        if i % 10 == 0:
          print(f"iteration {i}, loss = {L}")





mlp_gradient_descent(x=2.0, y=1.0)
