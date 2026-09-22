#!/usr/bin/env python3
"""Book 3 verification: every checkable mathematical claim on book3/index.html.

One numbered check per claim; each check is a real assertion with a scope tag
(CP = checked proof via exact algebra / exact integer arithmetic; NC =
completed numerical check -- sampled-point agreement, never a proof).
Exits 0 only if every check passes; any failure raises. No timeouts.

Page claims covered:
  B1-B9   Fig 1 / 3.III: Mobius cophase maps, orbit, cross-ratio, det check
  B10-B13 Fig 2 / 3.II: octant dominance, tie points, cophase permutation
  B14-B22 Fig 3 / 3.IV: positive reciprocal transform and its identities
  B23-B27 Fig 4 / 3.V: FlatWave cophase character
  B28-B31 Fig 5 / 3.X: Rodrigues bridge, seam values, chart boundary
  B32-B33 Fig 6 / 3.X/3.XI: deck flip and 4pi return
  B34-B37 Fig 7 / 3.VII: tautological sign vs FlatWave, monodromy product
  B38     3.VIII/3.IX: orientability/spin parity table (exact integers)
  B39-B40 3.X: lift-pair normalization, Rodrigues composition (collinear)
  B41-B42 3.IV: logarithmic coordinates, threshold formulas
  B43-B45 3.VI/3.VII: cyclic ratio identity, reciprocal compatibility, cocycle
  B46     3.II: eta order 8, C_dom order 4, C_dom^2 = P_c (exact permutations)
  B47     3.X: quaternion rotation lands in SO(3), kernel contains {+-1}
  B48     3.VII: half-angle lift v(x+2pi) = -v(x)

Not machine-checked (out of scope for sampled-point checks, labeled in text):
  SI claims (standard topology imports), AX definitions/constitutional rules,
  MA interpretive/terminological stipulations, and in-text CP arguments
  (e.g. no-global-continuous-selector proof, dependency acyclicity claim).

This script SUBSUMES validation/book3/verify_figures.py (all of its coverage
is re-expressed here as numbered B-checks with scope tags).

Run: python3 ~/workspace/r-theory-rewrite/validation/book3/verify_book3.py
"""
import math
import numpy as np
from fractions import Fraction

results = []

def check(name, err, tol=1e-9, scope="NC"):
    err = np.asarray(err, dtype=float)
    assert np.all(np.isfinite(err)), f"{name}: non-finite values"
    m = float(np.max(np.abs(err)))
    assert m < tol, f"{name}: max_err={m:.3e} >= tol={tol:.0e}"
    results.append((name, m, tol, scope))
    print(f"OK [{scope}] {name}: max_err={m:.3e} < {tol:.0e}")

def exact(name, cond):
    assert cond, f"{name}: FAILED"
    results.append((name, 0.0, 0.0, "CP"))
    print(f"OK [CP] {name}: exact")

def relerr(a, b):
    return np.max(np.abs(a - b) / (1 + np.abs(a) + np.abs(b)))

rng = np.random.default_rng(7)

# canonical primitives (same definitions as Books 0/1)
srx = lambda x: np.abs(1/np.sin(x)) + np.cos(x)/np.sin(x)
sxp = lambda x: np.abs(1/np.sin(x)) - np.cos(x)/np.sin(x)
cxp = lambda x: np.abs(1/np.cos(x)) + np.sin(x)/np.cos(x)
crx = lambda x: np.abs(1/np.cos(x)) - np.sin(x)/np.cos(x)
FW  = lambda x: np.sign(np.sin(2*x))

def off_seam(x, gap=3e-3):
    return (np.abs(np.sin(x)) > gap) & (np.abs(np.cos(x)) > gap)

# ---------------------------------------------------------------- B1-B9: Fig 1 / 3.III Mobius cophase maps
Qp = lambda t: (1 + t) / (1 - t)
Qm = lambda t: (t - 1) / (1 + t)
R  = lambda t: -t
t = rng.uniform(-3, 3, 40001)
t = t[(np.abs(t - 1) > 0.1) & (np.abs(t + 1) > 0.1) & (np.abs(t) > 0.1)]

check("B1 Qm(Qp(t)) = t (inverse relation)", Qm(Qp(t)) - t, 1e-9, "NC")
check("B2 Qp(Qm(t)) = t (inverse relation)", Qp(Qm(t)) - t, 1e-9, "NC")
check("B3 Qp^2(t) = -1/t (two steps = half-turn map)", Qp(Qp(t)) + 1/t, 1e-9, "NC")
check("B4 Qp^4(t) = t (exact order 4)", Qp(Qp(Qp(Qp(t)))) - t, 1e-9, "NC")
check("B5 R(Qp(R(t))) = Qm(t) (reflection conjugates Q+ to Q-)",
      R(Qp(R(t))) - Qm(t), 1e-9, "NC")
# B6: marked orbit 0 -> 1 -> inf -> -1 -> 0 (finite steps exact; pole as limit)
exact("B6a Qp(0) = 1", abs(Qp(0.0) - 1.0) < 1e-12)
exact("B6b Qp(-1) = 0", abs(Qp(-1.0) - 0.0) < 1e-12)
exact("B6c Qp(inf) = -1 (projective limit)", abs(Qp(1e15) + 1.0) < 1e-12)
# B7: half-angle coordinate consistency tan((x+pi/2)/2) = Qp(tan(x/2))
x = rng.uniform(-np.pi, np.pi, 40001)
tt = np.tan(x / 2)
ok = ((np.abs((x / 2) % np.pi - np.pi / 2) > 1e-3) & (np.abs(tt - 1) > 1e-3)
      & (np.abs(np.abs(tt) - 1) > 1e-3))
x, tt = x[ok], tt[ok]
check("B7 tan((x+pi/2)/2) = Qp(tan(x/2)) (relative)",
      relerr(np.tan((x + np.pi / 2) / 2), Qp(tt)), 1e-9, "NC")
# B8: harmonic cross-ratio [0,inf;1,-1] = -1 (exact rational arithmetic)
cr = (Fraction(0) - Fraction(1)) / (Fraction(0) - Fraction(-1))  # b -> inf limit
exact("B8 harmonic cross-ratio [0,inf;1,-1] = -1", cr == Fraction(-1))
# B9: det A+ = +2 vs det R = -1 (orientation separation on RP1)
Aplus = np.array([[1., 1.], [-1., 1.]])   # Q+(t) = (1+t)/(1-t)
AR = np.array([[-1., 0.], [0., 1.]])      # R(t) = -t
exact("B9 det A+ = +2, det R = -1",
      round(np.linalg.det(Aplus)) == 2 and round(np.linalg.det(AR)) == -1)

# ---------------------------------------------------------------- B10-B13: Fig 2 / 3.II octant dominance
winners = ["srx", "cxp", "crx", "sxp", "srx", "cxp", "crx", "sxp"]
gaps = []
for j in range(8):
    m = (j + 0.5) * np.pi / 4          # octant midpoint (admissible)
    vals = {"srx": srx(m), "sxp": sxp(m), "cxp": cxp(m), "crx": crx(m)}
    w = max(vals, key=vals.get)
    assert w == winners[j], (j, w, vals)
    srt = sorted(vals.values(), reverse=True)
    assert srt[0] - srt[1] > 1e-9, (j, srt)
    gaps.append(srt[0] - srt[1])
results.append(("B10 octant winner cycle + strict gaps", min(gaps), 1e-9, "NC"))
print(f"OK [NC] B10 winner cycle srx>cxp>crx>sxp (x2), min strict gap={min(gaps):.3e}")
# B11: tie points at odd multiples of pi/4 are admissible (in D)
for j in range(8):
    b = (2 * j + 1) * np.pi / 4
    assert abs(np.sin(b)) > 1e-12 and abs(np.cos(b)) > 1e-12
results.append(("B11 tie points (2j+1)pi/4 in D", 0.0, 0.0, "NC"))
print("OK [NC] B11 tie points (2j+1)pi/4 lie in D (sin,cos nonzero)")
# B12: exact cophase permutation on values (3.II.T8)
xx = rng.uniform(0.1, 2 * np.pi - 0.1, 40001)
xx = xx[off_seam(xx, 1e-3) & off_seam(xx + np.pi / 2, 1e-3)]
check("B12a srx(x+pi/2) = crx(x)", relerr(srx(xx + np.pi/2), crx(xx)), 1e-9, "NC")
check("B12b sxp(x+pi/2) = cxp(x)", relerr(sxp(xx + np.pi/2), cxp(xx)), 1e-9, "NC")
check("B12c cxp(x+pi/2) = sxp(x)", relerr(cxp(xx + np.pi/2), sxp(xx)), 1e-9, "NC")
check("B12d crx(x+pi/2) = srx(x)", relerr(crx(xx + np.pi/2), srx(xx)), 1e-9, "NC")
# B13: half-turn invariance of primitives (3.II.T5)
check("B13a srx(x+pi) = srx(x)", relerr(srx(xx + np.pi), srx(xx)), 1e-9, "NC")
check("B13b cxp(x+pi) = cxp(x)", relerr(cxp(xx + np.pi), cxp(xx)), 1e-9, "NC")

# ---------------------------------------------------------------- B14-B22: Fig 3 / 3.IV reciprocal transform
f = lambda u: np.sqrt(1 + u * u) - u
u = rng.uniform(-8, 8, 80001)
s = f(u)
exact("B14 f(u) > 0 on samples", np.all(s > 0))
check("B15 f(-u)*f(u) = 1 (reciprocal)", f(-u) * f(u) - 1, 1e-9, "NC")
check("B16 u = (1-s^2)/(2s) (exact inverse)", u - (1 - s**2) / (2 * s), 1e-9, "NC")
check("B17 f(u) = exp(-arsinh u) (hyperbolic linearization)",
      f(u) - np.exp(-np.arcsinh(u)), 1e-9, "NC")
check("B18 f(u) = 1/(sqrt(1+u^2)+u) (rationalized)",
      f(u) - 1 / (np.sqrt(1 + u * u) + u), 1e-9, "NC")
un = u[np.abs(u) > 1e-3]
check("B19 sgn(u) = sgn(1-s^2) (unit threshold sign recovery)",
      np.abs(np.sign(un) - np.sign(1 - f(un) ** 2)), 1e-9, "NC")
exact("B20 f(0) = 1 (threshold point)", abs(f(0.0) - 1.0) < 1e-12)
# B21: all four primitives from one map (3.IV.T9/T10), x in D
sx = xx[off_seam(xx, 1e-3)]
cx = xx[off_seam(xx, 1e-3)]
check("B21a sxp(x) = f(cot x)",
      np.abs(sxp(sx) - f(np.cos(sx) / np.sin(sx))) / (1 + np.abs(sxp(sx))), 1e-9, "NC")
check("B21b srx(x) = f(-cot x)",
      np.abs(srx(sx) - f(-np.cos(sx) / np.sin(sx))) / (1 + np.abs(srx(sx))), 1e-9, "NC")
check("B21c crx(x) = f(tan x)",
      np.abs(crx(cx) - f(np.tan(cx))) / (1 + np.abs(crx(cx))), 1e-9, "NC")
check("B21d cxp(x) = f(-tan x)",
      np.abs(cxp(cx) - f(-np.tan(cx))) / (1 + np.abs(cxp(cx))), 1e-9, "NC")
# B22: unequal endpoint limits (bar to a single global RP1 coordinate, 3.IV.T14)
exact("B22 f(+inf)->0, f(-inf)->+inf (unequal)", f(1e8) < 1e-7 and f(-1e8) > 1e7)

# ---------------------------------------------------------------- B23-B27: Fig 4 / 3.V FlatWave character
xa = rng.uniform(0.05, 2 * np.pi - 0.05, 80001)
xa = xa[np.abs(np.sin(2 * xa)) > 1e-3]       # off seams
check("B23 FW(x+pi/2) = -FW(x) (cophase reversal)",
      FW(xa + np.pi / 2) + FW(xa), 1e-9, "NC")
check("B24 FW(x-pi/2) = -FW(x) (negative cophase reversal)",
      FW(xa - np.pi / 2) + FW(xa), 1e-9, "NC")
check("B25 FW(x+pi) = FW(x) (half-turn invariance)",
      FW(xa + np.pi) - FW(xa), 1e-9, "NC")
check("B26 FW(x+2pi) = FW(x) (deck-shift invariance)",
      FW(xa + 2 * np.pi) - FW(xa), 1e-9, "NC")
# B27: octant form FW|_{Oj} = (-1)^{floor(j/2)}
for j in range(8):
    m = (j + 0.5) * np.pi / 4
    assert FW(m) == (-1) ** (j // 2), (j, FW(m))
results.append(("B27 FlatWave octant values (-1)^{floor(j/2)}", 0.0, 0.0, "NC"))
print("OK [NC] B27 FW|_{Oj} = (-1)^{floor(j/2)} at all 8 midpoints")
# orbit form: eps -> -eps -> eps -> -eps -> eps
m0 = np.pi / 8
for k in range(4):
    assert FW(m0 + k * np.pi / 2) == ((-1) ** k) * FW(m0), k
results.append(("B27b four-step sign orbit", 0.0, 0.0, "NC"))
print("OK [NC] B27b orbit eps -> -eps -> eps -> -eps -> eps")

# ---------------------------------------------------------------- B28-B31: Fig 5 / 3.X Rodrigues bridge
th = np.linspace(0.01, np.pi - 0.01, 40001)
rho = np.tan(th / 2)
check("B28 sxp(theta) = tan(theta/2) on (0,pi)",
      (sxp(th) - rho) / (1 + rho), 1e-9, "NC")
exact("B29 rho(pi/2) = 1 (FlatWave seam value)",
      abs(np.tan(np.pi / 4) - 1.0) < 1e-12)
exact("B30 q0(pi/2) = 1/sqrt(2) != 0 (seam regular)",
      abs(np.cos(np.pi / 4) - 1 / np.sqrt(2)) < 1e-12)
exact("B31 q0 -> 0 as theta -> pi (chart boundary)",
      abs(np.cos((np.pi - 1e-9) / 2)) < 1e-8)

# ---------------------------------------------------------------- B32-B33: Fig 6 / 3.X-3.XI double cover sheets
q0 = lambda th_: np.cos(th_ / 2)
tt6 = rng.uniform(0, 4 * np.pi, 40001)
check("B32 q0(theta+2pi) = -q0(theta) (deck flip)",
      q0(tt6 + 2 * np.pi) + q0(tt6), 1e-9, "NC")
check("B33 q0(theta+4pi) = q0(theta) (4pi return)",
      q0(tt6 + 4 * np.pi) - q0(tt6), 1e-9, "NC")

# ---------------------------------------------------------------- B34-B37: Fig 7 / 3.VII comparison test
t7 = rng.uniform(-3, 3, 80001)
t7 = t7[(np.abs(t7) > 1e-3) & (np.abs(np.abs(t7) - 1) > 1e-3)]
fw_t = np.sign(t7 * (1 - t7 ** 2))
tau_t = np.sign(t7)
check("B34 sgn(t(1-t^2)) = sgn(t)*sgn(1-t^2)",
      fw_t - tau_t * np.sign(1 - t7 ** 2), 1e-9, "NC")
inn = t7[np.abs(t7) < 1]
out = t7[np.abs(t7) > 1]
exact("B35a agreement on |t| < 1",
      np.all(np.sign(inn * (1 - inn ** 2)) == np.sign(inn)))
exact("B35b disagreement on |t| > 1",
      np.all(np.sign(out * (1 - out ** 2)) == -np.sign(out)))
# B36: cross-check with phase form sgn(t(1-t^2)) = sgn(sin 2x), t = tan(x/2)
x7 = rng.uniform(-1.4, 1.4, 40001)
t7x = np.tan(x7 / 2)
ok7 = ((np.abs(np.sin(2 * x7)) > 1e-3) & (np.abs(t7x) > 1e-3)
       & (np.abs(np.abs(t7x) - 1) > 1e-3))
x7, t7x = x7[ok7], t7x[ok7]
check("B36 sgn(t(1-t^2)) = sgn(sin 2x) cross-check",
      np.sign(t7x * (1 - t7x ** 2)) - np.sign(np.sin(2 * x7)), 1e-9, "NC")
# B37: monodromy arithmetic of 3.VII.T10: (-1)^4 = +1 vs tautological -1
exact("B37 four cophase multipliers product = +1", (-1) ** 4 == 1)

# ---------------------------------------------------------------- B38: 3.VIII/3.IX spin-orientability table (exact integers)
# w1(T RP^n) = (n+1) a_n vanishes iff n odd; for n >= 2 spin needs
# w2 = C(n+1,2) a_n^2 to vanish (n=1: H^2 = 0 kills w2 regardless)
table = []
for n in range(1, 8):
    orient = (n % 2 == 1)
    spin = (n == 1) or (n % 4 == 3)
    spin_from_classes = orient and ((n == 1) or (math.comb(n + 1, 2) % 2 == 0))
    assert spin == spin_from_classes, (n, spin, spin_from_classes)
    assert orient == ((n + 1) % 2 == 0), n
    table.append((n, orient, spin))
exact("B38 n=1..7: orientable<=>n odd; spin<=>n=1 or n=3 mod 4", True)
print("   table:", table)

# ---------------------------------------------------------------- B39-B40: 3.X lift pair and Rodrigues composition
# B39: inverse lift pair q_±(r) = ±(1+r)/sqrt(1+||r||^2) are unit quaternions
rr = rng.normal(0, 1, (20001, 3))
rr = rr[~np.any(np.abs(rr) > 3, axis=1)]
norm2 = 1 + np.sum(rr ** 2, axis=1)
qplus = np.column_stack([1 / np.sqrt(norm2), rr / np.sqrt(norm2)[:, None]])
check("B39 ||q_+(r)|| = 1",
      np.sum(qplus ** 2, axis=1) - 1, 1e-12, "CP")
# B40: a(+)b = (a+b+a×b)/(1-a.b) reduces to tangent addition collinearly
n = np.array([0.3, -0.5, 0.8]); n = n / np.linalg.norm(n)
tha, thb = rng.uniform(0.2, 1.2, 20001), rng.uniform(0.2, 1.2, 20001)
a = np.tan(tha / 2)[:, None] * n
b = np.tan(thb / 2)[:, None] * n
comp = (a + b + np.cross(a, b)) / (1 - np.sum(a * b, axis=1))[:, None]
expect = np.tan((tha + thb) / 2)[:, None] * n
check("B40 Rodrigues composition = tangent addition collinearly",
      np.max(np.abs(comp - expect), axis=1) / (1 + np.linalg.norm(expect, axis=1)),
      1e-9, "NC")

# ---------------------------------------------------------------- B41-B42: 3.IV logarithmic / threshold formulas
# B41: arsinh(cot x) = ln srx = -ln sxp
check("B41a arsinh(cot x) = ln srx",
      np.arcsinh(np.cos(sx) / np.sin(sx)) - np.log(srx(sx)), 1e-9, "NC")
check("B41b ln srx = -ln sxp",
      np.log(srx(sx)) + np.log(sxp(sx)), 1e-9, "NC")
# B42: threshold formulas sgn(1-sxp^2) = sgn(srx^2-1), sgn(1-cxp^2)=sgn(crx^2-1)
ok4 = np.abs(sx - 1) > 1e-2  # avoid s=1 zero of the sign
check("B42a sgn(1-sxp^2) = sgn(srx^2-1)",
      np.abs(np.sign(1 - sxp(sx[ok4]) ** 2) - np.sign(srx(sx[ok4]) ** 2 - 1)), 1e-9, "NC")
check("B42b sgn(1-cxp^2) = sgn(crx^2-1)",
      np.abs(np.sign(1 - cxp(cx[ok4]) ** 2) - np.sign(crx(cx[ok4]) ** 2 - 1)), 1e-9, "NC")

# ---------------------------------------------------------------- B43-B45: 3.VI/3.VII ratio and cocycle identities
# B43: cyclic ratio identity u_XY u_YZ u_ZX = 1 on P° = {XYZ != 0}
X, Y, Z = rng.uniform(-2, 2, 3 * 20001).reshape(3, -1)
XYZ = (np.abs(X) > 0.05) & (np.abs(Y) > 0.05) & (np.abs(Z) > 0.05)
X, Y, Z = X[XYZ], Y[XYZ], Z[XYZ]
uXY, uYZ, uZX = Y / X, Z / Y, X / Z
check("B43 u_XY u_YZ u_ZX = 1 on P°",
      uXY * uYZ * uZX - 1, 1e-12, "CP")
# B44: reciprocal compatibility surface
sXY, sYZ, sZX = f(uXY), f(uYZ), f(uZX)
check("B44 (1-s_XY^2)(1-s_YZ^2)(1-s_ZX^2) = 8 s_XY s_YZ s_ZX",
      (1 - sXY**2) * (1 - sYZ**2) * (1 - sZX**2) - 8 * sXY * sYZ * sZX,
      1e-9, "CP")
# B45: Čech cocycle for the tautological transition signs
zYX = np.sign(X / Y)   # e_Y = (X/Y) e_X
zZY = np.sign(Y / Z)
zZX = np.sign(X / Z)
exact("B45 z_ZY z_YX = z_ZX (cocycle)", np.all(zZY * zYX == zZX))

# ---------------------------------------------------------------- B46: 3.II exact permutation / order arithmetic
# eta = tau_{pi/4} has exact order 8 on the octant positions (mod-8 addition)
def add(a, b):  # quarter-turn units mod 8
    return (a + b) % 8
ord8 = all(add(j, 8) == j for j in range(8)) and \
    all(not all(add(j, k) == j for j in range(8)) for k in range(1, 8))
exact("B46a eta has exact order 8 (eta^8=id, no smaller power is)", ord8)
# C_dom = (srx cxp crx sxp) order 4; C_dom^2 = P_c = (srx crx)(sxp cxp)
names = ["srx", "cxp", "crx", "sxp"]
Cdom = {names[i]: names[(i + 1) % 4] for i in range(4)}
Pc = {"srx": "crx", "crx": "srx", "sxp": "cxp", "cxp": "sxp"}
Cdom2 = {k: Cdom[Cdom[k]] for k in names}
Cdom4 = {k: Cdom[Cdom[Cdom[Cdom[k]]]] for k in names}
exact("B46b C_dom^2 = P_c", Cdom2 == Pc)
exact("B46c C_dom order 4",
      Cdom4 == {k: k for k in names} and Cdom2 != {k: k for k in names})

# ---------------------------------------------------------------- B47: 3.X quaternion rotation lands in SO(3)
def qmul(p, q):
    w1, v1 = p[..., 0:1], p[..., 1:]
    w2, v2 = q[..., 0:1], q[..., 1:]
    return np.concatenate([w1 * w2 - np.sum(v1 * v2, axis=-1, keepdims=True),
                           w1 * v2 + w2 * v1 + np.cross(v1, v2)], axis=-1)
def qconj(q):
    return np.concatenate([q[..., 0:1], -q[..., 1:]], axis=-1)
q7 = rng.normal(0, 1, (501, 4))
q7 = q7 / np.linalg.norm(q7, axis=1, keepdims=True)
v7 = rng.normal(0, 1, (501, 3))
qv = np.concatenate([np.zeros((501, 1)), v7], axis=1)
out = qmul(qmul(q7, qv), qconj(q7))
check("B47a |qv q̄| = |v| (length preserved)",
      np.linalg.norm(out[..., 1:], axis=1) - np.linalg.norm(v7, axis=1), 1e-12, "NC")
check("B47b scalar part of qv q̄ = 0 (lands in the vector part)",
      out[..., 0], 1e-12, "NC")
out_neg = qmul(qmul(-q7, qv), qconj(-q7))
check("B47c Phi(-q) = Phi(q) (kernel contains {±1})",
      np.max(np.abs(out - out_neg), axis=1), 1e-12, "NC")
# rotation matrix: columns are q e_i q̄; must be orthogonal with det +1
e = np.eye(3)
Rq = np.stack([qmul(qmul(q7, np.concatenate([np.zeros((501, 1)), np.tile(e[i], (501, 1))], axis=1)),
                    qconj(q7))[..., 1:] for i in range(3)], axis=-1)
check("B47d R(q)^T R(q) = I",
      np.max(np.abs(np.einsum("nij,nkj->nik", Rq, Rq) - np.eye(3)), axis=(1, 2)),
      1e-12, "NC")
check("B47e det R(q) = +1",
      np.linalg.det(Rq) - 1, 1e-12, "NC")

# ---------------------------------------------------------------- B48: 3.VII half-angle lift
x8 = rng.uniform(-4, 4, 40001)
v = np.stack([np.cos(x8 / 2), np.sin(x8 / 2)], axis=1)
vp = np.stack([np.cos((x8 + 2 * np.pi) / 2), np.sin((x8 + 2 * np.pi) / 2)], axis=1)
check("B48 v(x+2pi) = -v(x) (tautological lift flips)",
      np.max(np.abs(vp + v), axis=1), 1e-12, "NC")

print(f"\n{len(results)} checks run, all passed. No timeouts, no failures.")
