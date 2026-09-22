"""Generate verified PNG fallbacks for Book 16 Desmos graphs.

Each plot uses the EXACT formula embedded in book16/index.html (same
viewports, same markers), so the PNG doubles as verification of the Desmos
expressions. Run: python3 make_graphs.py
"""
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.expanduser("~/workspace/r-theory-rewrite/book16/graphs")
os.makedirs(OUT, exist_ok=True)

def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), dpi=110)
    plt.close(fig)
    print("wrote", name)

# ---------- d1: covariant stationarity ----------
x = np.linspace(0, math.pi / 2, 2000)
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(x, np.cos(2 * x), label="cos 2x", lw=1.5)
ax.plot(x, np.sin(2 * x), label="sin 2x", lw=1.5)
ax.plot(x, np.sin(2 * x) / 4, label="H=sin 2x/4", lw=2)
ax.axvline(math.pi / 4, color="gray", ls="--", lw=1)
ax.plot([math.pi / 4], [0.25], "ko")
ax.set_xlim(-0.2, 1.8); ax.set_ylim(-1.2, 1.2)
ax.set_title("Covariant 45-degree stationarity of the diagonal Z bridge")
ax.legend(); ax.grid(alpha=0.3)
save(fig, "g1_zbridge.png")

# ---------- d2: qSaw lift ----------
w = np.linspace(-2.5, 2.5, 2000)
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(w, 2 * np.cosh(w), label="2cosh w", lw=1.5)
ax.plot(w, 2 * np.sinh(w), label="2sinh w", lw=1.5)
ax.plot(w, np.tanh(w), label="tanh w", lw=2)
ax.set_xlim(-2.5, 2.5); ax.set_ylim(-8.5, 8.5)
ax.set_title("Single-hyperbola qSaw lift")
ax.legend(); ax.grid(alpha=0.3)
save(fig, "g2_qsaw.png")

# ---------- d3: D4 response ----------
z = np.linspace(-3.5, 3.5, 2000)
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(z, np.tanh(z), label="tanh z", lw=1.5)
ax.plot(z, 4 * np.cosh(z / 2) / (np.cosh(z) + 3), label="4cosh(z/2)/(cosh z+3)", lw=2)
for s in (-1, 1):
    ax.axvline(s * 1.7627, color="gray", ls="--", lw=1)
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-1.3, 1.3)
ax.set_title("D4 response (dashed: arcosh 3 = 1.7627)")
ax.legend(); ax.grid(alpha=0.3)
save(fig, "g3_d4response.png")

# ---------- d4: Saw-Hodge doublet ----------
w = np.linspace(-4, 4, 4000)
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(w, np.tanh(2 * w), label="Pi_C=tanh 2w", lw=2)
ax.plot(w, 2 * np.cosh(w) / (np.cosh(w) ** 2 + 1), label="Xi_C", lw=2)
ax.set_xlim(-4, 4); ax.set_ylim(-1.2, 1.2)
ax.set_title("Saw-Hodge doublet (negative branch visible)")
ax.legend(); ax.grid(alpha=0.3)
save(fig, "g4_saw_hodge.png")

# ---------- d5: Hessian factor ----------
w = np.linspace(-4, 4, 8000)
Xi = 2 * np.cosh(w) / (np.cosh(w) ** 2 + 1)
F = np.tanh(2 * w) ** 10 * (np.tanh(2 * w) ** 2 + 4 * Xi ** 2) ** 3
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(w, F, lw=2)
ax.set_xlim(-4, 4); ax.set_ylim(-0.1, 58)
ax.set_title("Hessian factor (max ~53.78 near |w|=1.022)")
ax.grid(alpha=0.3)
save(fig, "g5_hessian_factor.png")

# ---------- d6: radial stabilization ----------
q = np.linspace(-2.2, 2.2, 2000)
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(q, -2.5 * q ** 2 + 1.25 * q ** 4, lw=2)
ax.plot([1], [-1.25], "ro")
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-1.6, 2.2)
ax.set_title("Radial stabilization: minima at q=+/-1, V=-1.25")
ax.grid(alpha=0.3)
save(fig, "g6_radial_stab.png")

# ---------- d7: selector ratio ----------
y = np.linspace(0.02, 6, 4000)
R = (y ** 2 + 2) ** 2 / (y ** 3 * (2 * y ** 2 + 1) ** 2)
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(y, R, lw=2)
ax.set_xlim(0, 6); ax.set_ylim(-2, 30)
ax.set_title("Selector ratio R(y), strictly decreasing")
ax.grid(alpha=0.3)
save(fig, "g7_selector_R.png")

# ---------- d8: selector minimum ----------
w = np.linspace(-2.5, 3.5, 4000)
A = 1.7 * np.tanh(2 * w) + 0.6 * 2 * np.cosh(w) / (np.cosh(w) ** 2 + 1)
V = -A ** 2 / 5.2
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(w, V, lw=2)
ax.plot([1.062], [-0.921], "ko")
ax.set_xlim(-2.5, 3.5); ax.set_ylim(-1.1, -0.3)
ax.set_title("Selector minimum (1.062, -0.921)")
ax.grid(alpha=0.3)
save(fig, "g8_selector_minimum.png")

# ---------- d9: dihedral group ----------
th = np.linspace(0, 2 * math.pi, 400)
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(np.cos(th), np.sin(th), lw=1.5)
k = np.arange(8)
ax.plot(np.cos(k * math.pi / 4), np.sin(k * math.pi / 4), "ko")
ax.axhline(0, color="gray", lw=0.8)
ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.45, 1.45); ax.set_aspect("equal")
ax.set_title("Dihedral group: 8th roots of unity")
ax.grid(alpha=0.3)
save(fig, "g9_dihedral.png")

# ---------- d10: quarter-null lattice ----------
fig, ax = plt.subplots(figsize=(9, 9))
xx = np.linspace(-3.4, 6.6, 400)
for m in range(-2, 3):
    ax.plot(xx, xx - math.pi / 2 + m * math.pi, "b-", lw=0.8, alpha=0.6)
    ax.plot(xx, xx + math.pi / 2 + m * math.pi, "b-", lw=0.8, alpha=0.6)
E = [(-3.141593, -1.570796), (-1.570796, -3.141593), (-1.570796, 0.0),
     (0.0, -1.570796), (0.0, 1.570796), (1.570796, 0.0),
     (1.570796, 3.141593), (3.141593, 1.570796), (3.141593, 4.712389),
     (4.712389, 3.141593), (4.712389, 6.283185), (6.283185, 4.712389)]
O = [(-2.356194, -0.785398), (-0.785398, -2.356194), (-0.785398, 0.785398),
     (0.785398, -0.785398), (0.785398, 2.356194), (2.356194, 0.785398),
     (2.356194, 3.926991), (3.926991, 2.356194), (3.926991, 5.497787),
     (5.497787, 3.926991)]
ax.plot([p[0] for p in E], [p[1] for p in E], "go", ms=7, label="even quarters")
ax.plot([p[0] for p in O], [p[1] for p in O], "ro", ms=7, label="odd quarters")
ax.set_xlim(-3.4, 6.6); ax.set_ylim(-3.4, 6.6); ax.set_aspect("equal")
ax.set_title("Quarter-null lattice")
ax.legend(); ax.grid(alpha=0.3)
save(fig, "g10_quarter_null_lattice.png")

# ---------- d11: charge-parity phases ----------
th = np.linspace(0, 2 * math.pi, 400)
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(np.cos(th), np.sin(th), lw=1.5)
ax.plot([1], [0], "ko", ms=9); ax.plot([-1], [0], "ko", ms=9)
ax.axhline(0, color="gray", lw=0.8)
ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6); ax.set_aspect("equal")
ax.set_title("Charge-parity phases: J(R_D)=1, J(U) alternates")
ax.grid(alpha=0.3)
save(fig, "g11_fujikawa_phases.png")

# ---------- d12: odd-quarter selection ----------
fa = np.linspace(-0.2, 6.5, 2000)
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(fa, -(1 - np.cos(4 * fa)), lw=2)
for m in (1, 3, 5, 7):
    ax.axvline(m * math.pi / 4, color="gray", ls="--", lw=1)
for m in (1, 3, 5, 7):
    ax.plot([m * math.pi / 4], [-2], "ko")
ax.set_xlim(-0.2, 6.5); ax.set_ylim(-2.2, 0.4)
ax.set_title("Kinetic ansatz -(1-cos 4phi_a): minima -2 at odd quarters")
ax.grid(alpha=0.3)
save(fig, "g12_odd_quarter_selection.png")

# ---------- d13: hyperbola ----------
fig, ax = plt.subplots(figsize=(7, 7))
yy = np.linspace(-3.2, 3.2, 2000)
br = np.sqrt(np.maximum(yy ** 2 - 1, 0))
m = yy ** 2 >= 1
ax.plot(br[m], yy[m], "b-", lw=1.5)
ax.plot(-br[m], yy[m], "b-", lw=1.5)
xx = np.linspace(-3, 3, 400)
ax.plot(xx, xx, "g--", lw=1); ax.plot(xx, -xx, "g--", lw=1)
ax.plot([0], [1], "ko", ms=8)
ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.2, 3.2); ax.set_aspect("equal")
ax.set_title("Hyperbola y^2-x^2=1, asymptotes y=+-x, point (0,1)")
ax.grid(alpha=0.3)
save(fig, "g13_hyperbola.png")

# ---------- d14: kinetic rapidity ----------
fig, ax = plt.subplots(figsize=(9, 5))
for eta, dom, col in ((0.3, 1.9, "#1f77b4"), (0.6, 1.2837, "#ff7f0e"),
                      (0.9, 0.9577, "#2ca02c")):
    x = np.linspace(-dom, dom, 2000)
    ax.plot(x, np.arctanh(eta * np.sinh(x)), color=col, lw=2,
            label=f"atanh({eta} sinh x)")
    ax.plot(x, eta * x, color=col, ls="--", lw=1)
ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.6, 2.6)
ax.set_title("Kinetic rapidity (domains inside artanh's real domain)")
ax.legend(); ax.grid(alpha=0.3)
save(fig, "g14_rapidity.png")

# ---------- d15: tilted-branch double well ----------
fig, ax = plt.subplots(figsize=(9, 5))
for a, col in ((0.4, "#1f77b4"), (0.505, "#ff7f0e"), (0.7, "#2ca02c")):
    d = np.linspace(-1.6, 1.6, 2000)
    ax.plot(d, d ** 2 / 2 - (a / 2) * np.log(np.cosh(2 * d)),
            color=col, lw=2, label=f"a={a}")
dots = [(0.08669, -0.0000187), (-0.08669, -0.0000187),
        (0.57017, -0.0280331), (-0.57017, -0.0280331)]
ax.plot([p[0] for p in dots], [p[1] for p in dots], "ko", ms=7)
ax.set_xlim(-1.7, 1.7); ax.set_ylim(-0.35, 0.15)
ax.set_title("Tilted-branch double well (black dots: broken minima)")
ax.legend(); ax.grid(alpha=0.3)
save(fig, "g15_pitchfork.png")

print("all 15 fallbacks regenerated")
