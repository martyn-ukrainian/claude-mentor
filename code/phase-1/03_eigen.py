import numpy as np

A = np.array([[4, 0], [0, 5]])
eigenvalues, eigenvectors = np.linalg.eig(A)
print("λ:", eigenvalues)
print("v:\n", eigenvectors)


A1 = np.array([[2, 1], [1, 2]])
print("A1:\n", A1)
eigenvalues1, eigenvectors1 = np.linalg.eig(A1)
print("λ1:", eigenvalues1)
print("v1:\n", eigenvectors1)


print("A1 @ v1:\n", A1 @ eigenvectors1)


v0 = eigenvalues1[0] * eigenvectors1[:, 0]
print("v0:\n", v0)

v1 = eigenvalues1[1] * eigenvectors1[:, 1]
print("v1:\n", v1)

print(A1 @ eigenvectors1)
