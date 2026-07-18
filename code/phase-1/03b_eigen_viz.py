import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

# "Сигароподібна" хмара точок: сильно розтягнута в одному напрямку, майже пряма лінія
n = 300
x = np.random.randn(n) * 5           # великий розкид по x
y = x * 0.5 + np.random.randn(n) * 0.3  # y майже повторює x, з малим шумом

data = np.column_stack([x, y])
data = data - data.mean(axis=0)  # центруємо (як завжди перед PCA)

cov = np.cov(data.T)  # коваріаційна матриця (те саме, що X.T @ X / (n-1))
eigenvalues, eigenvectors = np.linalg.eigh(cov)  # eigh: для симетричних матриць, повертає дійсні числа
print("Коваріаційна матриця:\n", cov)
print("λ (eigenvalues):", eigenvalues)
print("eigenvectors (стовпці):\n", eigenvectors)

fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(data[:, 0], data[:, 1], alpha=0.3, s=15, label="дані (300 точок)")

colors = ["tab:red", "tab:green"]
for i in range(2):
    v = eigenvectors[:, i]
    lam = eigenvalues[i]
    # довжина стрілки пропорційна sqrt(λ) -- це і є "наскільки розтягнуті дані" вздовж цього напрямку
    scale = np.sqrt(lam) * 2
    ax.arrow(0, 0, v[0]*scale, v[1]*scale, head_width=0.3, color=colors[i], linewidth=2,
              label=f"eigenvector {i}, λ={lam:.2f}")

ax.set_xlim(-15, 15)
ax.set_ylim(-15, 15)
ax.axhline(0, color="gray", linewidth=0.5)
ax.axvline(0, color="gray", linewidth=0.5)
ax.set_aspect("equal")
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()
ax.set_title("Eigenvectors коваріаційної матриці: напрямки розкиду даних")
plt.tight_layout()
plt.savefig("code/phase-1/03b_eigen_viz.png", dpi=120)
print("saved to code/phase-1/03b_eigen_viz.png")
