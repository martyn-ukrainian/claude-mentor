import numpy as np

def rely(z: np.ndarray) -> np.ndarray:
    return np.maximum(0, z)

def rely_derivative(z: np.ndarray) -> np.ndarray:
    return (z > 0).astype(int)


z = np.array([-2, -1, 0, 1, 2])

print(rely(z))
print(rely_derivative(z))
