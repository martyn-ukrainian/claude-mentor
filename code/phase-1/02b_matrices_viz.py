import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# --- Ліва панель: dot product / кут між двома векторами ---
ax = axes[0]
a = np.array([1, 1])
b = np.array([1, -1])
dot = a @ b
cos_sim = dot / (np.linalg.norm(a) * np.linalg.norm(b))

ax.quiver(0, 0, a[0], a[1], angles="xy", scale_units="xy", scale=1, color="tab:blue", label="a = [1, 1]")
ax.quiver(0, 0, b[0], b[1], angles="xy", scale_units="xy", scale=1, color="tab:red", label="b = [1, -1]")
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.axhline(0, color="gray", linewidth=0.5)
ax.axvline(0, color="gray", linewidth=0.5)
ax.set_aspect("equal")
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()
ax.set_title(f"Dot product: a·b = {dot}, кут = 90° (перпендикулярні)\ncos_sim = {cos_sim:.2f}")

# --- Права панель: матричне перетворення (поворот на 90°) ---
ax = axes[1]
R90 = np.array([[0, -1], [1, 0]])
v = np.array([1, 0])
v_rotated = R90 @ v

ax.quiver(0, 0, v[0], v[1], angles="xy", scale_units="xy", scale=1, color="tab:green", label="v = [1, 0] (до)")
ax.quiver(0, 0, v_rotated[0], v_rotated[1], angles="xy", scale_units="xy", scale=1, color="tab:purple", label="R90 @ v (після)")
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.axhline(0, color="gray", linewidth=0.5)
ax.axvline(0, color="gray", linewidth=0.5)
ax.set_aspect("equal")
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()
ax.set_title("Матричне перетворення: R90 @ v = поворот стрілки на 90°")

plt.tight_layout()
plt.savefig("code/phase-1/02b_matrices_viz.png", dpi=120)
print("saved to code/phase-1/02b_matrices_viz.png")
