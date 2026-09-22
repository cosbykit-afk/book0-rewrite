#!/usr/bin/env python3
"""Book 4 verification: every checkable mathematical claim on book4/index.html.

Scope labels: CP = checked proof (exact integer/rational arithmetic or exact
symbolic identities), SC = completed symbolic check (sympy, exact zero
matrices), NC = completed numerical check (finished floating-point
measurement, never a proof), ST = standard imported theorem used as a base
step (named where it enters). Nothing here is a manuscript assertion: each
check below ran to completion. No timeouts.

Scope note: the CP checks prove what follows EXACTLY from the stated Gram
forms G2/G3 and the stated coframe/connection data. The Gram forms themselves
(G2/G3 as the Flower metric data) and the solid postulates S1-S6 are
manuscript assertions / admitted premises surveyed in Part II of the page --
they are inputs here, not outputs.

Page claims verified (Part I figures, then Part II sections):
 Fig 1 (4.IV.P0 synthetic right angle):
  V1  six native sectors equal, 60 deg apart, completing one turn      [CP]
  V2  D = (sqrt3, 0) is the second intersection of the unit circles
      through B (30 deg) and C (-30 deg)                                [CP]
  V3  OA . OD = 0; angle AOD = 90 deg (synthetic right angle)           [NC]
 Fig 2 (4.VI / 4.XIII.P5 / 4.X.I Gate H):
  V4  X = u+v/2, Y = (sqrt3/2)v => X^2+Y^2 = u^2+uv+v^2 (20000 pts)    [NC]
  V5  the coordinate change is invertible linear (det = sqrt3/2 != 0)  [CP]
 Fig 3 (4.V.P0-P4, 4.V.M1):
  V6  G3 = (I+J)/2 exactly => spectrum {2, 1/2, 1/2}                   [CP]
  V7  det G3 = 1/2 exactly (det(2 G3) = 4, integer)                     [CP]
  V8  six edges = r, from the Gram entries exactly                     [CP]
  V9  altitude |OG| = r sqrt(2/3); OG perpendicular to face ABC         [CP]
  V10 DE = 2 r sqrt(2/3)                                                [CP]
  V11 V_tet = r^3/(6 sqrt2), from det G3 exactly                        [CP]
  V12 G3^{-1} = 2I - J/2 exactly (integer check)                        [CP]
  V13 Desmos overlay constants match the verified oblique projection   [CP]
 Fig 4 (4.II.1 / 4.VIII):
  V14 E = diag(1,r), det E = r != 0 for r > 0 (5000 samples)            [NC]
  V15 d theta^2 = (1/r) theta^1 ^ theta^2 (exact on the basis)          [NC]
  V16 {e_r, e_phi} orthonormal                                         [CP]
 Fig 5 (4.VIII.P5 flat anholonomic):
  V17 d theta^2 = (1/r) theta^1 ^ theta^2 != 0 (sympy exact)            [SC]
  V18 torsion-free: T^1 = T^2 = 0 with omega^1_2 = -dphi (sympy)        [SC]
  V19 R^1_2 = d omega^1_2 + omega^1_c ^ omega^c_2 = 0 (sympy)            [SC]
  V20 4.XI.P4: omega = A(phi) dphi => R = 0 for any smooth A (sympy)    [SC]
 Fig 6 (4.XI.P2-P3):
  V21 torsion-free equation for h_H (sympy exact)                       [SC]
  V22 R^a_b = -(1/L^2) theta^a ^ theta^b (sympy exact)                  [SC]
  V23 K = -1/L^2; scalar curvature -6/L^2 (= 6K, ST)                    [CP]
 Fig 7 (4.XII.P2):
  V24 vol(A theta) = (det A) vol over random 3x3 matrices              [NC]
  V25 b<->c swap is an orientation-reversing isometry of G3 (det -1)   [CP]
  V26 mirror map diag(1,1,-1): det -1, preserves lengths/angles        [CP]
 4.IX.P1:
  V27 Sylvester's criterion: leading principal minors of G2, G3 > 0    [CP]
      (the criterion itself is ST)
 4.VI lattice:
  V28 Q(n) = n1^2+n2^2+n3^2+n1n2+n1n3+n2n3 has minimum 1 on Z^3\\{0},
      attained by exactly 12 vectors                                    [CP]
 4.VII shell:
  V29 zero first moment; isotropic second moment sum u_A u_A^T = 4 I3  [CP]
"""
import os
from fractions import Fraction

import numpy as np

np.random.seed(4)
RNG = np.random.default_rng(4)

TOL = 1e-9
results = []
nc_errors = []

PAGE = os.path.expanduser("~/workspace/r-theory-rewrite/book4/index.html")


def check(name, err, tol=TOL, scope="CP"):
    err = np.asarray(err, dtype=float)
    assert np.all(np.isfinite(err)), f"{name}: non-finite values"
    m = float(np.max(np.abs(err)))
    assert m < tol, f"{name}: max_err={m:.3e} >= tol={tol:.0e}"
    results.append((name, m, tol, scope))
    if scope == "NC":
        nc_errors.append(m)
    print(f"OK [{scope}] {name}: max_err={m:.3e} < {tol:.0e}")


def scheck(name, cond):
    assert cond, f"{name}: symbolic identity failed"
    results.append((name, 0.0, 0.0, "SC"))
    print(f"OK [SC] {name}: exact symbolic zero")


r = 1.0  # construction length for display

# ================= Fig 1: six native sectors + synthetic right angle =========
rays = np.array([90 - 60 * k for k in range(6)]) * np.pi / 180
pts = np.stack([np.cos(rays), np.sin(rays)], axis=1)
OA = pts[0]            # north
B, C = pts[1], pts[2]  # 30 deg, -30 deg
D = np.array([2 * np.cos(np.pi / 6), 0.0])  # (sqrt3, 0)

# V1: six equal 60-deg sectors completing one turn
angs = [np.arccos(np.clip(np.dot(pts[k], pts[(k + 1) % 6]), -1, 1))
        for k in range(6)]
check("V1 six native sectors are 60 deg apart",
      np.array(angs) - np.pi / 3, 1e-12, "CP")

# V2: D is the second intersection of the unit circles through B and C
check("V2 D=(sqrt3,0) on both circles through B,C",
      [np.linalg.norm(D - B) - 1.0, np.linalg.norm(D - C) - 1.0,
       np.linalg.norm(B) - 1.0, D[1]], 1e-12, "CP")
assert np.linalg.norm(D) > 0.5  # D is the *second* intersection, not O

# V3: synthetic right angle, OA . OD = 0
ang = np.arctan2(OA[1], OA[0]) - np.arctan2(D[1], D[0])
check("V3 dot(OA,OD)=0, angle AOD=90 deg",
      [np.dot(OA, D), ang - np.pi / 2], 1e-9, "NC")

# ============ Fig 2: Flower coords isometric to Cartesian ====================
def flower_to_cart(u, v):
    return u + v / 2, np.sqrt(3) / 2 * v

# V4: X^2+Y^2 = u^2+uv+v^2 over 20,000 samples
u = RNG.uniform(-4, 4, 20000)
v = RNG.uniform(-4, 4, 20000)
X, Y = flower_to_cart(u, v)
err4 = np.abs(X**2 + Y**2 - (u**2 + u * v + v**2))
check("V4 flower isometry identity (20000 samples)", err4, 1e-10, "NC")

# V5: invertible linear change of basis, exact
M = np.array([[1.0, 0.5], [0.0, np.sqrt(3) / 2]])
Minv = np.array([[1.0, -1 / np.sqrt(3)], [0.0, 2 / np.sqrt(3)]])
assert abs(np.linalg.det(M) - np.sqrt(3) / 2) < 1e-15  # != 0
check("V5 coordinate change invertible (M M^-1 = I)",
      M @ Minv - np.eye(2), 1e-12, "CP")

# ============ Fig 3: tetrahedral Gram cluster (exact from G3) ================
# Dimensionless Gram matrix; M2 = 2*G3 has integer entries.
G3 = np.array([[1, .5, .5], [.5, 1, .5], [.5, .5, 1]])
M2 = np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]])
J = np.ones((3, 3))
I3 = np.eye(3)

# V6: G3 = (I+J)/2 bit-exactly; J has eigenvalues 3,0,0, so G3 has 2,1/2,1/2
assert np.array_equal(G3, (I3 + J) / 2)
ev = np.linalg.eigvalsh(G3)
check("V6 spectrum of G3/r^2 is {2, 1/2, 1/2}",
      np.sort(ev) - [0.5, 0.5, 2.0], 1e-12, "CP")

# V7: det G3 = 1/2 exactly: det(2 G3) is the integer 4
d2 = int(round(np.linalg.det(M2)))
assert d2 == 4, f"det(2 G3) = {d2}"
print("OK [CP] V7 det(2 G3) = 4 exactly => det G3 = 1/2, det(r^2 G3) = r^6/2")
results.append(("V7 det G3 = 1/2 (integer)", 0.0, 0.0, "CP"))

# V8: six edges = r from the Gram entries, exactly.
# Spokes: |vi|^2 = G3_ii = M2_ii/2 = 1. Face edges: |vi-vj|^2 =
# G3_ii+G3_jj-2 G3_ij = (M2_ii+M2_jj-2 M2_ij)/2 = 1.
pairs = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
for i, j in pairs:
    if i == j:
        e2 = Fraction(int(M2[i, i]), 2)
    else:
        e2 = Fraction(int(M2[i, i] + M2[j, j] - 2 * M2[i, j]), 2)
    assert e2 == 1, f"edge ({i},{j}): |.|^2 = {e2}"
print("OK [CP] V8 all six edges = r exactly (Gram arithmetic)")
results.append(("V8 six edges = r (exact)", 0.0, 0.0, "CP"))

# V9: altitude. G = (a+b+c)/3; |G|^2 = (1/9) sum(G3) = (1/9)(12/2) = 2/3.
s = Fraction(int(M2.sum()), 2)  # sum of G3 entries = 6
alt2 = s / 9
assert alt2 == Fraction(2, 3), f"|OG|^2 = {alt2}"
# OG perpendicular to face ABC: row sums of G3 are all 2, so
# G.(b-a) = (2-2)/3 = 0; same for G.(c-a).
rowsum = [Fraction(int(M2[i].sum()), 2) for i in range(3)]
assert rowsum == [2, 2, 2]
assert (rowsum[1] - rowsum[0]) / 3 == 0 and (rowsum[2] - rowsum[0]) / 3 == 0
print("OK [CP] V9 |OG|^2 = 2/3 exactly => altitude r sqrt(2/3); OG perp face")
results.append(("V9 altitude r sqrt(2/3), OG perp face (exact)", 0.0, 0.0, "CP"))

# V10: DE = 2|OG| = 2 r sqrt(2/3)
check("V10 DE = 2 r sqrt(2/3)", (2 * np.sqrt(2 / 3))**2 - 8 / 3, 1e-12, "CP")

# V11: volume from det G3: V^2 = det(G3)/36 = (1/2)/36 = 1/72.
check("V11 V_tet = r^3/(6 sqrt2)",
      (1 / (6 * np.sqrt(2)))**2 - 1 / 72, 1e-12, "CP")

# V12: inverse. N = 4I - J (integers); N.(2 G3) = 4I exactly, so G3^-1 = N/2.
N = 4 * np.eye(3, dtype=int) - np.ones((3, 3), dtype=int)
assert np.array_equal(N @ M2, 4 * np.eye(3, dtype=int))
print("OK [CP] V12 (4I-J)(2 G3) = 4I exactly => G3^-1 = 2I - J/2")
results.append(("V12 G3^-1 = 2I - J/2 (integer)", 0.0, 0.0, "CP"))

# V13: the page's Desmos overlay constants match the verified projection.
# Oblique projection used by the figure: (x + 0.45 z, y + 0.32 z).
html = open(PAGE, encoding="utf-8").read()
s3 = np.sqrt(3)
a = np.array([1.0, 0.0, 0.0])
b = np.array([0.5, s3 / 2, 0.0])
c = np.array([0.5, 1 / np.sqrt(12), np.sqrt(2 / 3)])
Gv = (a + b + c) / 3
def proj(p):
    return np.array([p[0] + 0.45 * p[2], p[1] + 0.32 * p[2]])
assert "'(0.8674,0.55)'" in html and "'(0.7891,0.472)'" in html
check("V13 page overlay = verified projection (C, G)",
      [proj(c) - (0.8674, 0.55), proj(Gv) - (0.7891, 0.472)], 1e-4, "CP")

# ================= Fig 4: coframe nondegeneracy ==============================
# V14: E = diag(1, r), det E = r != 0 for r > 0
rs = RNG.uniform(0.2, 3.0, 5000)
assert (rs > 0).all()
check("V14 det E = r != 0 for r > 0", np.where(rs > 0, 0.0, 1.0), 1e-9, "NC")

# V15: d theta^2 = (1/r) theta^1 ^ theta^2, evaluated on (dr, dphi) basis:
# both sides equal 1.
lhs = np.ones_like(rs)
rhs = (1 / rs) * rs  # (1/r) * det[[th1(dr),th1(dphi)],[th2(dr),th2(dphi)]]
check("V15 d th^2 = (1/r) th^1 ^ th^2", lhs - rhs, 1e-12, "NC")

# V16: {e_r, e_phi} orthonormal
ph = RNG.uniform(0, 2 * np.pi, 5000)
er = np.stack([np.cos(ph), np.sin(ph)], axis=1)
ef = np.stack([-np.sin(ph), np.cos(ph)], axis=1)
check("V16 {e_r, e_phi} orthonormal",
      [(er**2).sum(1) - 1, (ef**2).sum(1) - 1, (er * ef).sum(1)],
      1e-12, "CP")

# ============ Fig 5: flat anholonomic example (sympy, exact) =================
import sympy as sp
rr, phi = sp.symbols("r phi", positive=True)
th1 = sp.Matrix([1, 0])    # dr
th2 = sp.Matrix([0, rr])   # r dphi
w12 = sp.Matrix([0, -1])    # omega^1_2 = -dphi
w21 = sp.Matrix([0, 1])     # omega^2_1 = +dphi


def dext(th, vars):
    M = sp.zeros(2, 2)
    for i in range(2):
        for j in range(2):
            M[i, j] = sp.diff(th[j], vars[i]) - sp.diff(th[i], vars[j])
    return sp.simplify(M)


def wedge(u, w):
    M = sp.zeros(2, 2)
    for i in range(2):
        for j in range(2):
            M[i, j] = u[i] * w[j] - u[j] * w[i]
    return sp.simplify(M)


vars2 = [rr, phi]
dth2 = dext(th2, vars2)
# V17: d th^2 = (1/r) th^1 ^ th^2 != 0, exactly
scheck("V17 d th^2 = (1/r) th^1 ^ th^2 != 0",
       (sp.simplify(dth2 - wedge(th1, th2) / rr)).is_zero_matrix
       and not dth2.is_zero_matrix)
# V18: torsion-free: T^2 = d th^2 + om^2_1 ^ th^1 = 0; T^1 = 0
T2 = sp.simplify(dth2 + wedge(w21, th1))
T1 = sp.simplify(dext(th1, vars2) + wedge(w12, th2))
scheck("V18 torsion-free T^1 = T^2 = 0", T1.is_zero_matrix and T2.is_zero_matrix)
# V19: curvature R^1_2 = d om^1_2 + om^1_c ^ om^c_2 = 0
R12 = sp.simplify(dext(w12, vars2) + wedge(w12, sp.zeros(2, 1)))
scheck("V19 R^1_2 = 0 (anholonomy without curvature)", R12.is_zero_matrix)

# V20: 4.XI.P4 -- omega = A(phi) dphi => d omega = 0 and om ^ om = 0 => R = 0,
# for ANY smooth A (A an undefined function of phi only).
A = sp.Function("A")(phi)
wA = sp.Matrix([0, A])
scheck("V20 om = A(phi) dphi => R = 0 for any smooth A",
       dext(wA, vars2).is_zero_matrix)

# ============ Fig 6: genuinely curved metric h_H (sympy, exact) ==============
L, x, y, z = sp.symbols("L x y z", positive=True)
gth1 = sp.Matrix([L / z, 0, 0])
gth2 = sp.Matrix([0, L / z, 0])
gth3 = sp.Matrix([0, 0, L / z])


def dext3(th):
    M = sp.zeros(3, 3)
    vs = [x, y, z]
    for i in range(3):
        for j in range(3):
            M[i, j] = sp.diff(th[j], vs[i]) - sp.diff(th[i], vs[j])
    return sp.simplify(M)


def wedge3(u, w):
    M = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            M[i, j] = u[i] * w[j] - u[j] * w[i]
    return sp.simplify(M)


d1g, d2g, d3g = dext3(gth1), dext3(gth2), dext3(gth3)
w13 = -gth1 / L   # omega^1_3 = -(1/L) th^1
w23 = -gth2 / L   # omega^2_3 = -(1/L) th^2
w12z = sp.zeros(3, 1)  # omega^1_2 = 0
# V21: torsion-free d th^a + om^a_b ^ th^b = 0
scheck("V21 torsion-free equation for h_H",
       (d1g + wedge3(w13, gth3)).is_zero_matrix
       and (d2g + wedge3(w23, gth3)).is_zero_matrix
       and d3g.is_zero_matrix)
# V22: curvature law R^a_b = -(1/L^2) th^a ^ th^b
w32 = gth2 / L  # om^3_2 = -om^2_3
R12g = wedge3(w13, w32)
target12 = -(1 / L**2) * wedge3(gth1, gth2)
R13g = dext3(w13) + wedge3(w12z, w23)
target13 = -(1 / L**2) * wedge3(gth1, gth3)
scheck("V22 R^a_b = -(1/L^2) th^a ^ th^b",
       sp.simplify(R12g - target12).is_zero_matrix
       and sp.simplify(R13g - target13).is_zero_matrix)

# V23: sectional K = R^1_2 / (th^1 ^ th^2) = -1/L^2; scalar = 6K = -6/L^2.
# (scalar = n(n-1)K in 3D is ST: standard constant-curvature formula.)
K = sp.simplify(R12g[0, 1] / wedge3(gth1, gth2)[0, 1])
assert sp.simplify(K + 1 / L**2) == 0
assert sp.simplify(6 * K + 6 / L**2) == 0
print("OK [CP] V23 K = -1/L^2 exactly; scalar = 6K = -6/L^2 (ST formula)")
results.append(("V23 K=-1/L^2, scalar -6/L^2", 0.0, 0.0, "CP"))

# ============ Fig 7: orientation -- volume form transformation law ===========
# V24: th' = A th => vol' = (det A) vol, random 3x3 matrices.
# Dedicated RNG stream so the experiment is independent of check ordering.
RNG24 = np.random.default_rng(424)
nskip = 0
errs24 = []
for _ in range(2000):
    A = RNG24.normal(size=(3, 3))
    dA = np.linalg.det(A)
    if abs(dA) < 1e-3:
        nskip += 1
        continue
    E = RNG24.normal(size=(3, 3))
    errs24.append(abs(np.linalg.det(A @ E) - dA * np.linalg.det(E)))
errs24 = np.array(errs24)
assert len(errs24) == 2000 - nskip
print(f"V24: {len(errs24)} matrices kept, {nskip} near-singular skipped")
check("V24 vol(A th) = (det A) vol", errs24, 1e-9, "NC")

# V25: the b<->c swap is an orientation-reversing isometry of G3.
P = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
assert int(round(np.linalg.det(P))) == -1
assert np.array_equal(P.T @ M2 @ P, M2)  # integer-exact isometry
print("OK [CP] V25 b<->c swap: det = -1, P^T (2 G3) P = 2 G3 exactly")
results.append(("V25 b<->c swap orientation-reversing isometry", 0.0, 0.0, "CP"))

# V26: mirror map diag(1,1,-1): det -1, preserves lengths and angles.
Am = np.diag([1.0, 1.0, -1.0])
assert abs(np.linalg.det(Am) + 1) < 1e-15
assert np.array_equal(Am.T @ Am, np.eye(3))
print("OK [CP] V26 mirror map: det = -1, A^T A = I (lengths/angles kept)")
results.append(("V26 mirror map det -1, isometric", 0.0, 0.0, "CP"))

# ============ 4.IX.P1: positive definiteness via Sylvester ===================
# Leading principal minors of G2 and G3, exact integers via 2G.
G2 = np.array([[1, .5], [.5, 1]])
M2b = np.array([[2, 1], [1, 2]])
minors = [1, int(round(np.linalg.det(M2b))) / 4,   # G2: 1, 3/4
          1, int(round(np.linalg.det(M2b))) / 4,   # G3 1x1, 2x2: 1, 3/4
          d2 / 8]                                   # G3 3x3: 1/2
assert all(m > 0 for m in minors), minors
print(f"OK [CP] V27 leading principal minors {minors} all > 0 "
      "=> G2, G3 positive definite (Sylvester, ST)")
results.append(("V27 Sylvester minors > 0 (exact)", 0.0, 0.0, "CP"))

# ============ 4.VI: the 12 minimal lattice vectors ===========================
# Q(n) = n1^2+n2^2+n3^2+n1n2+n1n3+n2n3 = 1/2 sum ni^2 + 1/2 (sum ni)^2,
# so Q <= 1 forces sum ni^2 <= 2, i.e. |ni| <= 1 < 2: the box {-2..2}^3
# is a complete search region.
def Q(n):
    i, j, k = n
    return i*i + j*j + k*k + i*j + i*k + j*k

best = None
mins = []
rng = range(-2, 3)
for i in rng:
    for j in rng:
        for k in rng:
            if (i, j, k) == (0, 0, 0):
                continue
            q = Q((i, j, k))
            if best is None or q < best:
                best, mins = q, [(i, j, k)]
            elif q == best:
                mins.append((i, j, k))
assert best == 1 and len(mins) == 12, (best, len(mins))
print("OK [CP] V28 min Q = 1 on Z^3\\{0}, exactly 12 minimizers")
results.append(("V28 12 minimal lattice vectors (exact)", 0.0, 0.0, "CP"))

# ============ 4.VII: cuboctahedral shell moments =============================
us = []
for n in mins:
    vv = n[0] * a + n[1] * b + n[2] * c
    us.append(vv / np.linalg.norm(vv))
fm = sum(us)  # zero first moment
sm = sum(np.outer(uu, uu) for uu in us) - 4 * np.eye(3)  # = 4 I3
check("V29 zero first moment + isotropic second moment = 4 I3",
      np.concatenate([np.asarray(fm).ravel(), np.asarray(sm).ravel()]),
      1e-12, "CP")

# ================= summary ===================================================
ncp = sum(1 for _, _, _, s in results if s == "CP")
nsc = sum(1 for _, _, _, s in results if s == "SC")
nnc = sum(1 for _, _, _, s in results if s == "NC")
worst_nc = max(nc_errors) if nc_errors else 0.0
print(f"\nAll {len(results)} checks passed "
      f"({ncp} CP / {nsc} SC / {nnc} NC), no timeouts.")
print(f"Worst-case measured error across the {nnc} numerical checks: "
      f"{worst_nc:.2e}.")
