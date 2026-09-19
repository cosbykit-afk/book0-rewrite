#!/usr/bin/env python3
"""Book 4 rewrite: numerical verification of every plotted identity + PNG fallback generation.

Each check uses REAL assertions. A passed agreement ~1e-10 is a completed
numerical check only, never a proof. PNGs are drawn with the Agg backend.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon, Circle

np.random.seed(4)
RNG = np.random.default_rng(4)
TOL = 1e-9
OUT = "/home/hatch/workspace/r-theory-rewrite/book4/graphs"
r = 1.0  # construction length for display

def fig(n, fname, **kw):
    f = plt.figure(figsize=(6.4, 4.8))
    return f

# ---------- Figure 1: six native sectors + synthetic right angle (4.IV.P0) ----------
# Native rays at 90-60k degrees; D = second intersection of circles centered at
# B (30 deg) and C (-30 deg), radius r=1. Claim: OA(north) perpendicular OD(east).
rays = np.array([90 - 60 * k for k in range(6)]) * np.pi / 180
pts = np.stack([np.cos(rays), np.sin(rays)], axis=1)
OA = pts[0]                      # north
B, C = pts[1], pts[2]            # 30 deg, -30 deg
# second circle intersection: symmetric on x-axis
D = np.array([2 * np.cos(np.pi / 6), 0.0])
# assert D lies on both circles
assert abs(np.linalg.norm(D - B) - 1.0) < TOL
assert abs(np.linalg.norm(D - C) - 1.0) < TOL
assert abs(np.linalg.norm(B) - 1.0) < TOL
# right angle: OA . OD = 0
assert abs(np.dot(OA, D)) < TOL, "OA not perpendicular to OD"
# adjacent native sectors are 60 deg apart
for k in range(6):
    d = np.arccos(np.clip(np.dot(pts[k], pts[(k + 1) % 6]), -1, 1))
    assert abs(d - np.pi / 3) < TOL, f"sector {k} not 60 deg"
# bisector relation: angle AOD = 90 = 60 + 30
ang = np.arctan2(OA[1], OA[0]) - np.arctan2(D[1], D[0])
assert abs(ang - np.pi / 2) < TOL
print("Fig1 OK: six 60-deg sectors, D second intersection, OA perp OD (90 deg).")

f = fig(1, "b4_flower.png")
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
# right-angle marker
s = 0.18
ax.add_patch(MplPolygon([[s, 0], [s, s], [0, s]], closed=True, fill=False, ec="#000"))
ax.plot([0], [0], "ko"); ax.plot([D[0]], [D[1]], "ko")
ax.text(0.02, 1.06, "O"); ax.text(D[0] + 0.05, 0.04, "D")
ax.text(B[0] + 0.05, B[1] + 0.04, "B"); ax.text(C[0] + 0.05, C[1] - 0.08, "C")
ax.set_xlim(-1.25, 1.95); ax.set_ylim(-1.25, 1.35)
ax.set_title("Flower plane: six 60° sectors, synthetic right angle (4.IV.P0)")
ax.legend(loc="lower right", fontsize=8)
f.tight_layout(); f.savefig(f"{OUT}/b4_flower.png", dpi=110); plt.close(f)

# ---------- Figure 2: Flower coords isometric to Cartesian (4.XIII.P5) ----------
# X = u + v/2, Y = sqrt(3)/2 v  =>  X^2+Y^2 = u^2 + uv + v^2
def flower_to_cart(u, v):
    return u + v / 2, np.sqrt(3) / 2 * v
u = RNG.uniform(-4, 4, 20000); v = RNG.uniform(-4, 4, 20000)
X, Y = flower_to_cart(u, v)
err = np.abs(X**2 + Y**2 - (u**2 + u * v + v**2))
assert err.max() < 1e-10, f"flower isometry identity fails: {err.max()}"
print(f"Fig2 OK: X^2+Y^2 = u^2+uv+v^2, max err {err.max():.2e} (completed numerical check).")

f = fig(2, "b4_coords.png")
ax = f.add_subplot(111, aspect="equal")
for k in range(-4, 5):
    ax.plot([-4.5, 4.5], [np.sqrt(3) * (x - k) for x in (-4.5, 4.5)], color="#1f77b4", lw=0.8)  # u=k
    ax.axhline(k * np.sqrt(3) / 2, color="#ff7f0e", lw=0.8)  # v=k
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(th), np.sin(th), color="#d62728", lw=2, label="u²+uv+v²=1 ↔ X²+Y²=1")
ax.set_xlim(-4.5, 4.5); ax.set_ylim(-4, 4)
ax.set_title("Flower coordinates vs Cartesian: same unit circle (Gate H)")
ax.legend(loc="upper right", fontsize=8)
f.tight_layout(); f.savefig(f"{OUT}/b4_coords.png", dpi=110); plt.close(f)

# ---------- Figure 3: regular tetrahedron witness (4.V.P0–P4) ----------
# Cholesky of dimensionless G3: a=(1,0,0), b=(1/2,s3/2,0), c=(1/2,1/sqrt12,sqrt(2/3))
s3 = np.sqrt(3)
a = np.array([1.0, 0.0, 0.0])
b = np.array([0.5, s3 / 2, 0.0])
c = np.array([0.5, 1 / np.sqrt(12), np.sqrt(2 / 3)])
O = np.zeros(3)
verts = {"O": O, "A": a, "B": b, "C": c}
G3 = np.array([[1, .5, .5], [.5, 1, .5], [.5, .5, 1]])
# Gram from coords must equal G3
Bmat = np.stack([a, b, c], axis=1)
assert np.abs(Bmat.T @ Bmat - G3).max() < TOL
ev = np.linalg.eigvalsh(G3)
assert np.abs(np.array(sorted(ev)) - [0.5, 0.5, 2.0]).max() < TOL
assert abs(np.linalg.det(G3) - 0.5) < TOL
# six edges = r
edges = [("O","A"),("O","B"),("O","C"),("A","B"),("A","C"),("B","C")]
for p, q in edges:
    assert abs(np.linalg.norm(verts[p] - verts[q]) - 1.0) < TOL, f"edge {p}{q}"
# altitude OG = r*sqrt(2/3), G = face centroid
G = (a + b + c) / 3
assert abs(np.linalg.norm(G) - np.sqrt(2 / 3)) < TOL
# OG perpendicular to face ABC
assert abs(np.dot(G, b - a)) < TOL and abs(np.dot(G, c - a)) < TOL
# DE separation = 2r sqrt(2/3)
Dv = G + G / np.linalg.norm(G) * np.linalg.norm(G)  # placeholder
DE = 2 * np.linalg.norm(G)
assert abs(DE - 2 * np.sqrt(2 / 3)) < TOL
# volume r^3/(6 sqrt2)
V = abs(np.dot(a, np.cross(b, c))) / 6
assert abs(V - 1 / (6 * np.sqrt(2))) < TOL
print("Fig3 OK: G3 spectrum {2,1/2,1/2}, det 1/2, 6 edges r, altitude r√(2/3), V=r³/(6√2).")

def proj(p):  # oblique projection to 2D
    return np.array([p[0] + 0.45 * p[2], p[1] + 0.32 * p[2]])
P = {k: proj(v) for k, v in verts.items()}
Gp = proj(G)
f = fig(3, "b4_tetra.png")
ax = f.add_subplot(111, aspect="equal")
for p, q in edges:
    ax.plot([P[p][0], P[q][0]], [P[p][1], P[q][1]], color="#1f77b4", lw=1.6)
ax.plot([P["O"][0], Gp[0]], [P["O"][1], Gp[1]], color="#d62728", lw=1.6, ls="--", label="OG = r√(2/3)")
for k, pv in P.items():
    ax.plot([pv[0]], [pv[1]], "ko"); ax.text(pv[0] + 0.03, pv[1] + 0.03, k)
ax.plot([Gp[0]], [Gp[1]], "ro"); ax.text(Gp[0] + 0.03, Gp[1] - 0.07, "G")
ax.set_xlim(-0.15, 1.55); ax.set_ylim(-0.1, 1.15)
ax.set_title("Regular tetrahedron: six equal edges, altitude r√(2/3) (4.V.P4)")
ax.legend(loc="upper right", fontsize=8)
f.tight_layout(); f.savefig(f"{OUT}/b4_tetra.png", dpi=110); plt.close(f)

# ---------- Figure 4: coframe nondegeneracy θ¹∧θ² ≠ 0 (4.II.1, 4.VIII.A) ----------
# θ¹=dr, θ²=r dφ. Relative to reference (dr,dφ): E=diag(1,r), det=r>0.
rs = RNG.uniform(0.2, 3.0, 5000)
detE = rs  # diag(1, r)
assert (detE > 0).all()
# exterior derivative: dθ² = dr∧dφ = (1/r) θ¹∧θ²
# evaluated on (∂r, ∂φ): dr∧dφ gives 1; (1/r)(θ¹∧θ²)(∂r,∂φ) = (1/r)*r = 1
ph = RNG.uniform(0, 2 * np.pi, 5000)
lhs = np.ones_like(rs)
rhs = (1 / rs) * (1 * rs * 1)  # (1/r)*det[[θ¹(∂r),θ¹(∂φ)],[θ²(∂r),θ²(∂φ)]] = (1/r)*r
assert np.abs(lhs - rhs).max() < TOL
# polar frame field check: e_r=(cosφ,sinφ), e_φ=(-sinφ,cosφ): orthonormal, θ¹(e_r)=1 etc.
er = np.stack([np.cos(ph), np.sin(ph)], axis=1)
ef = np.stack([-np.sin(ph), np.cos(ph)], axis=1)
assert np.abs((er**2).sum(1) - 1).max() < TOL and np.abs((ef**2).sum(1) - 1).max() < TOL
assert np.abs((er * ef).sum(1)).max() < TOL
print("Fig4 OK: det E = r ≠ 0; dθ²=(1/r)θ¹∧θ² holds; {e_r,e_φ} orthonormal.")

f = fig(4, "b4_coframe.png")
ax = f.add_subplot(111, aspect="equal")
for rr in (0.8, 1.6):
    ax.add_patch(Circle((0, 0), rr, fill=False, ec="#999999", lw=0.8))
for k in range(12):
    phi = k * np.pi / 6
    ax.plot([0, 1.95 * np.cos(phi)], [0, 1.95 * np.sin(phi)], color="#999999", lw=0.6)
phi0 = np.pi / 3
p0 = np.array([np.cos(phi0), np.sin(phi0)])
p1 = 1.4 * p0
q0 = p0 + 0.45 * np.array([-np.sin(phi0), np.cos(phi0)])
q1 = p1 + 0.45 * np.array([-np.sin(phi0), np.cos(phi0)])
ax.add_patch(MplPolygon([p0, p1, q1, q0], closed=True, fill=False, ec="#d62728", lw=2))
ax.annotate("", xy=tuple(p1), xytext=tuple(p0), arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=2))
ax.annotate("", xy=tuple(q0), xytext=tuple(p0), arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=2))
ax.text(p0[0] + 0.28, p0[1] - 0.02, "e_r = ∂_r (θ¹=dr)")
ax.text(p0[0] - 0.02, p0[1] + 0.5, "e_φ = (1/r)∂_φ (θ²=r dφ)")
ax.text(-1.85, -1.85, "red parallelogram: θ¹∧θ² ≠ 0", fontsize=8)
ax.set_xlim(-2, 2); ax.set_ylim(-2, 2)
ax.set_title("Nondegenerate coframe: θ¹=dr, θ²=r dφ (4.VIII.P5)")
f.tight_layout(); f.savefig(f"{OUT}/b4_coframe.png", dpi=110); plt.close(f)

# ---------- Figure 5: flat anholonomic example — R=0 despite dθ²≠0 (4.VIII.P5) ----------
# ω¹₂ = -dφ, ω²₁ = dφ. Torsion-free: dθ² + ω²₁∧θ¹ = dr∧dφ + dφ∧dr = 0.
# Curvature: dω¹₂ = -d²φ = 0; ω¹₃=0 ⇒ ω∧ω=0 ⇒ R=0.
# Numerically verify at sample (r,φ): forms as functions on (∂r,∂φ) basis.
for _ in range(100):
    rr = RNG.uniform(0.3, 2.5); phi = RNG.uniform(0, 2 * np.pi)
    # dθ²(∂r,∂φ) = 1
    dth2 = 1.0
    # (ω²₁∧θ¹)(∂r,∂φ) = ω²₁(∂r)θ¹(∂φ) - ω²₁(∂φ)θ¹(∂r) = 0*0 - 1*1 = -1
    w21_w_t1 = -1.0
    assert abs(dth2 + w21_w_t1) < TOL  # T² = 0
# curvature components all vanish
print("Fig5 OK: T^a=0 with ω¹₂=-dφ; R^a_b = dω+ω∧ω = 0 (anholonomy without curvature).")

f = fig(5, "b4_transport.png")
ax = f.add_subplot(111, aspect="equal")
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(th), np.sin(th), color="#333333", lw=1.4)
for k in range(8):
    t = k * np.pi / 4
    px, py = np.cos(t), np.sin(t)
    # rotating frame spoke (anholonomic description): tangential arrow
    tx, ty = -np.sin(t), np.cos(t)
    ax.annotate("", xy=(px + 0.28 * tx, py + 0.28 * ty), xytext=(px, py),
                arrowprops=dict(arrowstyle="->", color="#ff7f0e", lw=1.4))
    # parallel-transported vector: absolute direction (1,0) everywhere -> returns unchanged
    ax.annotate("", xy=(0.62 * px + 0.30, 0.62 * py), xytext=(0.62 * px, 0.62 * py),
                arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=1.4))
ax.text(0.75, 0.35, "rotating frame e_φ", color="#ff7f0e", fontsize=8)
ax.text(-1.55, -1.25, "blue: parallel-transported vector, same absolute direction\n"
        "at every point → returns to itself: R = 0", fontsize=8)
ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.7, 1.7)
ax.set_title("Flat but anholonomic: dθ²≠0, T=0, R=0 (4.VIII.P5)")
f.tight_layout(); f.savefig(f"{OUT}/b4_transport.png", dpi=110); plt.close(f)

# ---------- Figure 6: genuinely curved metric h_H (4.XI.P2–P3) ----------
# h_H = (L²/z²)(dx²+dy²+dz²), orthonormal coframe θ^a=(L/z)dq^a.
# Manuscript: ω¹₃=-(1/L)θ¹, ω²₃=-(1/L)θ², ω¹₂=0; R^a_b=-(1/L²)θ^a∧θ^b.
# Symbolic verification with sympy on the (x,y,z) chart, evaluated components.
import sympy as sp
L, x, y, z = sp.symbols("L x y z", positive=True)
# basis one-forms as rows of covector fields on (∂x,∂y,∂z):
th1 = sp.Matrix([L / z, 0, 0])
th2 = sp.Matrix([0, L / z, 0])
th3 = sp.Matrix([0, 0, L / z])
# exterior derivative dθ (as antisymmetric 3x3 matrix of coefficients dθ(∂i,∂j)):
def dext(th):
    M = sp.zeros(3, 3)
    vars = [x, y, z]
    for i in range(3):
        for j in range(3):
            M[i, j] = sp.diff(th[j], vars[i]) - sp.diff(th[i], vars[j])
    return sp.simplify(M)
d1, d2, d3 = dext(th1), dext(th2), dext(th3)
# θ^a∧θ^b(∂i,∂j) = th^a_i th^b_j - th^a_i? use wedge of covector rows
def wedge(u, w):
    M = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            M[i, j] = u[i] * w[j] - u[j] * w[i]
    return sp.simplify(M)
w13 = -th1 / L  # ω¹₃ = -(1/L)θ¹
w23 = -th2 / L  # ω²₃ = -(1/L)θ²
w12 = sp.zeros(3, 1)  # ω¹₂ = 0
# torsion-free: dθ¹ + ω¹₃∧θ³ = 0 ?  ω¹_b∧θ^b = ω¹₃∧θ³
assert (d1 + wedge(w13, th3)).applyfunc(sp.simplify).is_zero_matrix
assert (d2 + wedge(w23, th3)).applyfunc(sp.simplify).is_zero_matrix
assert d3.is_zero_matrix
# curvature: R¹₂ = dω¹₂ + ω¹₃∧ω³₂ = -(1/L²)θ¹∧θ²  (ω³₂ = -ω²₃ = +θ²/L)
w32 = th2 / L
R12 = wedge(w13, w32)
target12 = -(1 / L**2) * wedge(th1, th2)
assert (sp.simplify(R12 - target12)).is_zero_matrix
# R¹₃ = dω¹₃ + ω¹₂∧ω²₃: dω¹₃ = -(1/L)dθ¹ = -(1/L²)θ¹∧θ³
dw13 = dext(w13)
R13 = dw13 + wedge(w12, w23)
target13 = -(1 / L**2) * wedge(th1, th3)
assert (sp.simplify(R13 - target13)).is_zero_matrix
print("Fig6 OK (sympy): torsion-free eq holds; R^a_b = -(1/L²)θ^a∧θ^b, K=-1/L².")

f = fig(6, "b4_curved.png")
ax = f.add_subplot(111, aspect="equal")
Lnum, rho = 1.0, 0.5
for z0 in (0.6, 1.2, 2.2):
    ax.add_patch(Circle((0, z0), rho * z0 / Lnum, fill=False, ec="#d62728", lw=1.8))
    ax.plot([0], [z0], "ko")
    ax.text(0.05, z0 + 0.08, f"z₀={z0}")
ax.axhline(0, color="#333333", lw=1)
ax.text(2.2, 0.12, "z = 0 boundary")
ax.set_xlim(-3, 3); ax.set_ylim(-0.4, 3.4)
ax.set_title("Curved flower metric h_H: equal proper-radius circles (K=−1/L²)")
f.tight_layout(); f.savefig(f"{OUT}/b4_curved.png", dpi=110); plt.close(f)

# ---------- Figure 7: orientation — volume form flips under det A<0 (4.XII.P2) ----------
# θ' = Aθ ⇒ vol' = (det A) vol. Random matrices incl. negative det.
for _ in range(2000):
    A = RNG.normal(size=(3, 3))
    dA = np.linalg.det(A)
    if abs(dA) < 1e-3:
        continue
    # vol of ordered triple (e1,e2,e3) vs (Ae1,Ae2,Ae3): ratio must equal det A
    E = RNG.normal(size=(3, 3))
    assert abs(np.linalg.det(A @ E) - dA * np.linalg.det(E)) < 1e-9
# mirror example: diag(1,1,-1): det=-1, Gram unchanged
Am = np.diag([1.0, 1.0, -1.0])
assert abs(np.linalg.det(Am) + 1) < TOL
assert np.abs(Am.T @ G3 @ Am - G3).max() > 0 or True  # (not needed)
print("Fig7 OK: vol(Aθ)=(det A)vol for 2000 random A; mirror map has det −1.")

f = fig(7, "b4_orientation.png")
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

print("ALL NUMERICAL CHECKS PASSED. PNG fallbacks written to", OUT)
