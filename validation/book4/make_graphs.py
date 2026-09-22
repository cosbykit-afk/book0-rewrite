#!/usr/bin/env python3
"""Generate verified PNG fallbacks for Book 4 Desmos graphs.

Each plot uses the EXACT formula that is embedded in Desmos
(book4/index.html GRAPHS array), so the PNG doubles as verification of the
Desmos expressions. Mathematical verification lives in verify_book4.py;
this script only draws.
"""
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon, Circle

OUT = os.path.expanduser("~/workspace/r-theory-rewrite/book4/graphs")
os.makedirs(OUT, exist_ok=True)

r = 1.0  # construction length for display


def newfig():
    return plt.figure(figsize=(6.4, 4.8))


# ---------- Figure 1: six native sectors + synthetic right angle (4.IV.P0) ----
rays = np.array([90 - 60 * k for k in range(6)]) * np.pi / 180
pts = np.stack([np.cos(rays), np.sin(rays)], axis=1)
OA = pts[0]          # north
B, C = pts[1], pts[2]  # 30 deg, -30 deg
D = np.array([2 * np.cos(np.pi / 6), 0.0])  # (sqrt3, 0)

f = newfig()
ax = f.add_subplot(111, aspect="equal")
for k in range(6):
    p, q = pts[k], pts[(k + 1) % 6]
    ax.add_patch(MplPolygon([[0, 0], p, q], closed=True, fill=False, ec="#1f77b4"))
    ax.plot([0, p[0]], [0, p[1]], color="#1f77b4", lw=1.2)
ax.plot([0, OA[0]], [0, OA[1]], color="#d62728", lw=2.5, label="OA (north)")
ax.plot([0, D[0]], [0, D[1]], color="#d62728", lw=2.5, label="OD (east)")
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(th), np.sin(th), color="#999999", ls="--", lw=1)
ax.plot(B[0] + np.cos(th), B[1] + np.sin(th), color="#2ca02c", ls="--", lw=1)
ax.plot(C[0] + np.cos(th), C[1] + np.sin(th), color="#2ca02c", ls="--", lw=1)
s = 0.18
ax.add_patch(MplPolygon([[s, 0], [s, s], [0, s]], closed=True, fill=False, ec="#000"))
ax.plot([0], [0], "ko"); ax.plot([D[0]], [D[1]], "ko")
ax.text(0.02, 1.06, "O"); ax.text(D[0] + 0.05, 0.04, "D")
ax.text(B[0] + 0.05, B[1] + 0.04, "B"); ax.text(C[0] + 0.05, C[1] - 0.08, "C")
ax.set_xlim(-1.25, 1.95); ax.set_ylim(-1.25, 1.35)
ax.set_title("Flower plane: six 60° sectors, synthetic right angle (4.IV.P0)")
ax.legend(loc="lower right", fontsize=8)
f.tight_layout(); f.savefig(f"{OUT}/b4_flower.png", dpi=110); plt.close(f)

# ---------- Figure 2: Flower coords isometric to Cartesian -------------------
f = newfig()
ax = f.add_subplot(111, aspect="equal")
for k in range(-4, 5):
    ax.plot([-4.5, 4.5], [np.sqrt(3) * (x - k) for x in (-4.5, 4.5)],
            color="#1f77b4", lw=0.8)  # u = k
    ax.axhline(k * np.sqrt(3) / 2, color="#ff7f0e", lw=0.8)  # v = k
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(th), np.sin(th), color="#d62728", lw=2,
        label="u²+uv+v²=1 ↔ X²+Y²=1")
ax.set_xlim(-4.5, 4.5); ax.set_ylim(-4, 4)
ax.set_title("Flower coordinates vs Cartesian: same unit circle (Gate H)")
ax.legend(loc="upper right", fontsize=8)
f.tight_layout(); f.savefig(f"{OUT}/b4_coords.png", dpi=110); plt.close(f)

# ---------- Figure 3: regular tetrahedron witness (4.V.P0-P4) -----------------
s3 = np.sqrt(3)
a = np.array([1.0, 0.0, 0.0])
b = np.array([0.5, s3 / 2, 0.0])
c = np.array([0.5, 1 / np.sqrt(12), np.sqrt(2 / 3)])
O = np.zeros(3)
verts = {"O": O, "A": a, "B": b, "C": c}
edges = [("O", "A"), ("O", "B"), ("O", "C"),
         ("A", "B"), ("A", "C"), ("B", "C")]
G = (a + b + c) / 3


def proj(p):  # oblique projection to 2D, matches the Desmos overlay
    return np.array([p[0] + 0.45 * p[2], p[1] + 0.32 * p[2]])


P = {k: proj(v) for k, v in verts.items()}
Gp = proj(G)
f = newfig()
ax = f.add_subplot(111, aspect="equal")
for p, q in edges:
    ax.plot([P[p][0], P[q][0]], [P[p][1], P[q][1]], color="#1f77b4", lw=1.6)
ax.plot([P["O"][0], Gp[0]], [P["O"][1], Gp[1]], color="#d62728", lw=1.6,
        ls="--", label="OG = r√(2/3)")
for k, pv in P.items():
    ax.plot([pv[0]], [pv[1]], "ko"); ax.text(pv[0] + 0.03, pv[1] + 0.03, k)
ax.plot([Gp[0]], [Gp[1]], "ro"); ax.text(Gp[0] + 0.03, Gp[1] - 0.07, "G")
ax.set_xlim(-0.15, 1.55); ax.set_ylim(-0.1, 1.15)
ax.set_title("Regular tetrahedron: six equal edges, altitude r√(2/3) (4.V.P4)")
ax.legend(loc="upper right", fontsize=8)
f.tight_layout(); f.savefig(f"{OUT}/b4_tetra.png", dpi=110); plt.close(f)

# ---------- Figure 4: coframe nondegeneracy ----------------------------------
f = newfig()
ax = f.add_subplot(111, aspect="equal")
for rr in (0.8, 1.6):
    ax.add_patch(Circle((0, 0), rr, fill=False, ec="#999999", lw=0.8))
for k in range(12):
    phi = k * np.pi / 6
    ax.plot([0, 1.95 * np.cos(phi)], [0, 1.95 * np.sin(phi)],
            color="#999999", lw=0.6)
phi0 = np.pi / 3
p0 = np.array([np.cos(phi0), np.sin(phi0)])
p1 = 1.4 * p0
q0 = p0 + 0.45 * np.array([-np.sin(phi0), np.cos(phi0)])
q1 = p1 + 0.45 * np.array([-np.sin(phi0), np.cos(phi0)])
ax.add_patch(MplPolygon([p0, p1, q1, q0], closed=True, fill=False,
                        ec="#d62728", lw=2))
ax.annotate("", xy=tuple(p1), xytext=tuple(p0),
            arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=2))
ax.annotate("", xy=tuple(q0), xytext=tuple(p0),
            arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=2))
ax.text(p0[0] + 0.28, p0[1] - 0.02, "e_r = ∂_r (θ¹=dr)")
ax.text(p0[0] - 0.02, p0[1] + 0.5, "e_φ = (1/r)∂_φ (θ²=r dφ)")
ax.text(-1.85, -1.85, "red parallelogram: θ¹∧θ² ≠ 0", fontsize=8)
ax.set_xlim(-2, 2); ax.set_ylim(-2, 2)
ax.set_title("Nondegenerate coframe: θ¹=dr, θ²=r dφ (4.VIII.P5)")
f.tight_layout(); f.savefig(f"{OUT}/b4_coframe.png", dpi=110); plt.close(f)

# ---------- Figure 5: flat anholonomic example --------------------------------
f = newfig()
ax = f.add_subplot(111, aspect="equal")
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(th), np.sin(th), color="#333333", lw=1.4)
for k in range(8):
    t = k * np.pi / 4
    px, py = np.cos(t), np.sin(t)
    tx, ty = -np.sin(t), np.cos(t)  # rotating frame spoke (tangential)
    ax.annotate("", xy=(px + 0.28 * tx, py + 0.28 * ty), xytext=(px, py),
                arrowprops=dict(arrowstyle="->", color="#ff7f0e", lw=1.4))
    # parallel-transported vector: absolute direction (1,0) -> returns unchanged
    ax.annotate("", xy=(0.62 * px + 0.30, 0.62 * py), xytext=(0.62 * px, 0.62 * py),
                arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=1.4))
ax.text(0.75, 0.35, "rotating frame e_φ", color="#ff7f0e", fontsize=8)
ax.text(-1.55, -1.25, "blue: parallel-transported vector, same absolute direction\n"
        "at every point → returns to itself: R = 0", fontsize=8)
ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.7, 1.7)
ax.set_title("Flat but anholonomic: dθ²≠0, T=0, R=0 (4.VIII.P5)")
f.tight_layout(); f.savefig(f"{OUT}/b4_transport.png", dpi=110); plt.close(f)

# ---------- Figure 6: genuinely curved metric h_H -----------------------------
f = newfig()
ax = f.add_subplot(111, aspect="equal")
Lnum, rho = 1.0, 0.5
for z0 in (0.6, 1.2, 2.2):
    ax.add_patch(Circle((0, z0), rho * z0 / Lnum, fill=False,
                        ec="#d62728", lw=1.8))
    ax.plot([0], [z0], "ko")
    ax.text(0.05, z0 + 0.08, f"z₀={z0}")
ax.axhline(0, color="#333333", lw=1)
ax.text(2.2, 0.12, "z = 0 boundary")
ax.set_xlim(-3, 3); ax.set_ylim(-0.4, 3.4)
ax.set_title("Curved flower metric h_H: equal proper-radius circles (K=−1/L²)")
f.tight_layout(); f.savefig(f"{OUT}/b4_curved.png", dpi=110); plt.close(f)

# ---------- Figure 7: orientation classes --------------------------------------
f = newfig()
ax = f.add_subplot(111, aspect="equal")
for cx, sgn, lab, col in [(-2.2, 1, "positive class\nvol > 0", "#2ca02c"),
                          (2.2, -1, "mirror class\nvol < 0", "#d62728")]:
    ax.annotate("", xy=(cx + 1.0, 0), xytext=(cx, 0),
                arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=2))
    ax.annotate("", xy=(cx, 1.0), xytext=(cx, 0),
                arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=2))
    ax.annotate("", xy=(cx - 0.55 * sgn, -0.55 * sgn), xytext=(cx, 0),
                arrowprops=dict(arrowstyle="->", color=col, lw=2))
    ax.text(cx - 0.5, -1.05, lab, ha="center", fontsize=8, color=col)
    ax.text(cx + 1.05, 0.05, "e₁"); ax.text(cx + 0.05, 0.9, "e₂")
    ax.text(cx - 0.62 * sgn, -0.62 * sgn, "e₃", color=col)
ax.text(0, 1.35, "θ′=Aθ, vol′=(det A)·vol — same lengths/angles, opposite sign",
        ha="center", fontsize=9)
ax.set_xlim(-4, 4); ax.set_ylim(-1.7, 1.7); ax.axis("off")
ax.set_title("Two orientation classes; reversal flips the volume form (4.XII)")
f.tight_layout(); f.savefig(f"{OUT}/b4_orientation.png", dpi=110); plt.close(f)

print("PNG fallbacks written to", OUT)
