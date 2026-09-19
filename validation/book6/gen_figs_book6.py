"""Book 6 rewrite: static PNG fallbacks for the 7 Desmos figures.

Same formulas as the Desmos configs in ../index.html (see GRAPHS there).
Identities already asserted in verify_book6.py; this file only renders.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon as MplPolygon
from math import comb, sqrt, pi

OUT = "/home/hatch/workspace/r-theory-rewrite/book6/graphs"
BLUE, ORANGE, GREEN, RED, GRAY = "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#999999"

def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}", dpi=110)
    plt.close(fig)
    print("wrote", name)

# ---- Fig 1 (6.1): block structure O(2)xO(3) -------------------------------
# Orientation matches the Desmos config and the caption: E-block (O(2))
# lower-left, V-block (O(3)) upper-right, off-diagonal rectangles empty.
fig, ax = plt.subplots(figsize=(5.2, 5.2))
for i in range(6):
    ax.plot([0, 5], [i, i], color="black", lw=0.8)
    ax.plot([i, i], [0, 5], color="black", lw=0.8)
ax.add_patch(Rectangle((0, 0), 2, 2, facecolor=BLUE, alpha=0.35, edgecolor=BLUE, lw=2))
ax.add_patch(Rectangle((2, 2), 3, 3, facecolor=GREEN, alpha=0.35, edgecolor=GREEN, lw=2))
ax.text(1, 1, "E-block\nO(2)", ha="center", va="center", fontsize=11, color="#0b3d66")
ax.text(3.5, 3.5, "V-block\nO(3)", ha="center", va="center", fontsize=11, color="#14532d")
ax.text(3.5, 1, "no primitive\nmaps", ha="center", va="center", fontsize=9, color=GRAY)
ax.text(1, 3.5, "no primitive\nmaps", ha="center", va="center", fontsize=9, color=GRAY)
ax.set_xlim(-0.15, 5.15); ax.set_ylim(-0.15, 5.15); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
ax.set_title("Block structure: Aut_blk = O(2)×O(3)\nso(2)⊕so(3), dim 1+3 = 4", fontsize=12)
save(fig, "b6_block.png")

# ---- Fig 2 (6.2): bivector decomposition -----------------------------------
fig, ax = plt.subplots(figsize=(7.2, 2.6))
segs = [(0, 1, BLUE, "Λ²E: 1"), (1, 7, ORANGE, "E⊗V: 6\n(cross-block extension)"),
        (7, 10, GREEN, "Λ²V: 3")]
for x0, x1, c, lab in segs:
    ax.add_patch(Rectangle((x0, 0), x1 - x0, 1, facecolor=c, alpha=0.45, edgecolor=c, lw=2))
    ax.text((x0 + x1) / 2, 0.5, lab, ha="center", va="center", fontsize=10)
ax.set_xlim(-0.2, 10.2); ax.set_ylim(-0.35, 1.35); ax.set_yticks([])
ax.set_xlabel("bivector sectors of Λ²U")
ax.set_title("Λ²U = Λ²E ⊕ (E⊗V) ⊕ Λ²V :  1 + 6 + 3 = 10", fontsize=12)
ax.text(5, -0.22, "inherited block Lie algebra (1+3)", ha="center", fontsize=9, color=GRAY)
save(fig, "b6_bivector.png")

# ---- Fig 3 (6.3A): CHI copy weights ----------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 4.2))
chi = np.linspace(0, 2 * pi, 2001)
ax.plot(chi, np.cos(chi) ** 2, color=BLUE, lw=2, label="w_U = cos²χ")
ax.plot(chi, np.sin(chi) ** 2, color=ORANGE, lw=2, label="w_U♯ = sin²χ")
ax.axhline(0.5, color=GRAY, ls="--", lw=1)
for x0, lab in [(0, "χ=0\none-copy"), (pi / 4, "χ=π/4\nequal weight"), (pi / 2, "χ=π/2\nfull transfer")]:
    ax.plot([x0], [np.cos(x0) ** 2], "o", color=BLUE)
    ax.plot([x0], [np.sin(x0) ** 2], "o", color=ORANGE)
    ax.text(x0, 1.06, lab, ha="center", fontsize=9)
ax.set_xlim(-0.15, 2 * pi + 0.15); ax.set_ylim(-0.08, 1.3)
ax.set_xticks([0, pi / 2, pi, 3 * pi / 2, 2 * pi],
              ["0", "π/2", "π", "3π/2", "2π"])
ax.set_xlabel("χ_CHI"); ax.set_ylabel("copy weight")
ax.set_title("CHI orbit: w_U + w_U♯ = 1,  w_U − w_U♯ = cos 2χ", fontsize=12)
ax.legend(loc="center right", fontsize=10)
save(fig, "b6_chi.png")

# ---- Fig 4 (6.8): traceless line 2a+3b=0 ------------------------------------
fig, ax = plt.subplots(figsize=(5.4, 5.4))
a = np.linspace(-1.1, 1.1, 400)
ax.plot(a, -2 * a / 3, color=BLUE, lw=2, label="2a + 3b = 0")
ax.axhline(0, color="black", lw=0.7); ax.axvline(0, color="black", lw=0.7)
ax.plot([0.5], [-1 / 3], "o", color=RED, ms=9)
ax.text(0.55, -0.28, "(1/2, −1/3)", fontsize=11, color=RED)
ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_aspect("equal")
ax.set_xlabel("a (E-block scalar)"); ax.set_ylabel("b (V-block scalar)")
ax.set_title("Conditional volume reduction → S(U(2)×U(3))\nsu(2)⊕su(3)⊕u(1): 3+8+1 = 12", fontsize=12)
ax.legend(fontsize=10)
save(fig, "b6_traceless.png")

# ---- Fig 5 (6.13): balance 2n = n(n−1)/2 ------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 4.6))
n = np.linspace(0, 8, 400)
ax.plot(n, 2 * n, color=BLUE, lw=2, label="dim_R(U⊗C) = 2n")
ax.plot(n, n * (n - 1) / 2, color=ORANGE, lw=2, label="dim_R Λ²U = n(n−1)/2")
ns = np.arange(1, 9)
ax.plot(ns, 2 * ns, "o", color=BLUE, ms=5)
ax.plot(ns, ns * (ns - 1) / 2, "o", color=ORANGE, ms=5)
ax.plot([5], [10], "o", color="black", ms=10)
ax.text(5.15, 10.6, "n = 5: common dim 10", fontsize=11)
ax.set_xlim(-0.2, 8.2); ax.set_ylim(-1, 30)
ax.set_xlabel("n (real carrier dimension)"); ax.set_ylabel("dimension")
ax.set_title("Complexification–bivector balance: 2n = n(n−1)/2  ⟺  n = 5", fontsize=12)
ax.legend(fontsize=10)
save(fig, "b6_balance.png")

# ---- Fig 6 (6.9): exterior dimension pattern ---------------------------------
fig, ax = plt.subplots(figsize=(7.2, 4.4))
dims = [1, 5, 10, 10, 5, 1]
cols = [BLUE if r % 2 == 0 else GRAY for r in range(6)]
bars = ax.bar(range(6), dims, color=cols, alpha=0.6, edgecolor="black")
for r, h in enumerate(dims):
    ax.text(r, h + 0.3, str(h), ha="center", fontsize=11)
ax.set_xticks(range(6), ["0", "1", "2", "3", "4", "5"])
ax.set_xlabel("exterior grade r"); ax.set_ylabel("dim ΛʳU")
ax.set_ylim(0, 12)
ax.set_title("Exterior pattern at n=5: even 1+10+5 = 16, odd 5+10+1 = 16", fontsize=12)
ax.text(2, 11.2, "grade pattern  0:1   2:10   4:5  →  Λ⁴U Hodge-dual to U", fontsize=10,
        ha="center", color="#0b3d66")
save(fig, "b6_exterior.png")

# ---- Fig 7 (6.15): regular 2-simplex (N=3) ------------------------------------
fig, ax = plt.subplots(figsize=(5.4, 5.0))
v1 = np.array([1 / sqrt(2), 1 / sqrt(6)])
v2 = np.array([-1 / sqrt(2), 1 / sqrt(6)])
v3 = np.array([0.0, -2 / sqrt(6)])
tri = MplPolygon([v1, v2, v3], closed=True, facecolor=BLUE, alpha=0.18,
                 edgecolor=BLUE, lw=2)
ax.add_patch(tri)
for v, lab in [(v1, "v₁"), (v2, "v₂"), (v3, "v₃")]:
    ax.plot([v[0]], [v[1]], "o", color=BLUE, ms=8)
    ax.text(v[0] * 1.12, v[1] * 1.12 + 0.03, lab, fontsize=13, ha="center")
ax.plot([0], [0], "o", color="black", ms=5)
ax.text(0.04, -0.06, "0 (centroid)", fontsize=10)
ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.1, 0.95); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
ax.set_title("Regular 2-simplex: v_A = e_A − ⅓·1\n|v_A|²=2/3, v_A·v_B=−1/3, |v_A−v_B|²=2",
             fontsize=12)
save(fig, "b6_simplex.png")

print("ALL 7 PNG FALLBACKS WRITTEN")
