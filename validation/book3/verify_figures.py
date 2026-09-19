"""Numerical verification of every identity plotted in the Book 3 rewrite figures.

Each block ends in real `assert` statements. A sampled-point agreement
~1e-10 is a *completed numerical check*, never a proof. Run:
    python3 ~/workspace/book3/checks/verify_figures.py
Exit code nonzero on any failure.
"""
import numpy as np

TOL = 1e-10
n_fail = 0

def check(name, err):
    global n_fail
    ok = err < TOL
    print(("PASS " if ok else "FAIL ") + name + "  max_err=%.3e" % err)
    if not ok:
        n_fail += 1

def relerr(a, b):
    """Relative error, safe near poles where the compared values blow up."""
    return np.max(np.abs(a - b) / (1 + np.abs(a) + np.abs(b)))

rng = np.random.default_rng(7)

# ---------------------------------------------------------------- Fig 1: Mobius cophase maps (3.III)
Qp = lambda t: (1 + t) / (1 - t)
Qm = lambda t: (t - 1) / (1 + t)
R  = lambda t: -t
t = rng.uniform(-3, 3, 20001)
t = t[(np.abs(t - 1) > 0.1) & (np.abs(t + 1) > 0.1) & (np.abs(t) > 0.1)]
# stay well off poles/zeros where the rational maps are ill-conditioned
# inverse relation Q_- = Q_+^{-1}
check("Qm(Qp(t)) - t == 0", np.max(np.abs(Qm(Qp(t)) - t)))
check("Qp(Qm(t)) - t == 0", np.max(np.abs(Qp(Qm(t)) - t)))
# two steps = half-turn map -1/t
check("Qp^2(t) + 1/t == 0", np.max(np.abs(Qp(Qp(t)) + 1 / t)))
# four steps = identity
check("Qp^4(t) - t == 0", np.max(np.abs(Qp(Qp(Qp(Qp(t)))) - t)))
# scalar reflection conjugacy R Q+ R = Q-
check("R(Qp(R(t))) - Qm(t) == 0", np.max(np.abs(R(Qp(R(t))) - Qm(t))))
# marked orbit 0 -> 1 -> inf -> -1 -> 0 (finite steps)
assert abs(Qp(0.0) - 1.0) < TOL
assert abs(Qp(-1.0) - 0.0) < TOL
# Qp(1) is the pole: image is projective infinity; check as a limit
big = 1e15
assert abs(Qp(big) + 1.0) < 1e-12    # Qp(inf) = 1/(-1) = -1
assert abs(Qp(-big) + 1.0) < 1e-12
# half-angle coordinate consistency: tan((x+pi/2)/2) == Qp(tan(x/2))
x = rng.uniform(-np.pi, np.pi, 20001)
tt = np.tan(x / 2)
ok = (np.abs((x / 2) % np.pi - np.pi / 2) > 1e-3) & (np.abs(tt - 1) > 1e-3)
x, tt = x[ok], tt[ok]
check("tan((x+pi/2)/2) - Qp(tan(x/2)) == 0 (relative)",
      relerr(np.tan((x + np.pi / 2) / 2), Qp(tt)))
# harmonic cross-ratio [0,inf;1,-1] = -1  (limit b -> inf of ((a-c)(b-d))/((a-d)(b-c)))
a, c, d = 0.0, 1.0, -1.0
cr = (a - c) / (a - d)   # limit as b -> inf
assert abs(cr + 1.0) < TOL
print("PASS harmonic cross-ratio [0,inf;1,-1] == -1")

# ---------------------------------------------------------------- Fig 2: octant dominance (3.II)
srx = lambda x: np.abs(1 / np.sin(x)) + np.cos(x) / np.sin(x)
sxp = lambda x: np.abs(1 / np.sin(x)) - np.cos(x) / np.sin(x)
cxp = lambda x: np.abs(1 / np.cos(x)) + np.sin(x) / np.cos(x)
crx = lambda x: np.abs(1 / np.cos(x)) - np.sin(x) / np.cos(x)
winners = ["srx", "cxp", "crx", "sxp", "srx", "cxp", "crx", "sxp"]
for j in range(8):
    m = (j + 0.5) * np.pi / 4          # octant midpoint (admissible)
    vals = {"srx": srx(m), "sxp": sxp(m), "cxp": cxp(m), "crx": crx(m)}
    w = max(vals, key=vals.get)
    assert w == winners[j], (j, w, vals)
    # uniqueness: strict gap to runner-up
    srt = sorted(vals.values(), reverse=True)
    assert srt[0] - srt[1] > 1e-9, (j, srt)
print("PASS octant dominance cycle srx>cxp>crx>sxp>srx>cxp>crx>sxp (midpoints, strict)")
# tie points at odd multiples of pi/4 are admissible (in D): sin,cos nonzero
for j in range(8):
    b = (2 * j + 1) * np.pi / 4
    assert abs(np.sin(b)) > 1e-12 and abs(np.cos(b)) > 1e-12
print("PASS tie points (2j+1)pi/4 lie in D")
# exact cophase permutation on values: srx(x+pi/2) == crx(x) etc. (3.II.T8)
xx = rng.uniform(0.1, 2 * np.pi - 0.1, 20001)
xx = xx[np.abs(np.sin(xx)) > 1e-3]
xx = xx[np.abs(np.cos(xx)) > 1e-3]
xx = xx[np.abs(np.sin(xx + np.pi / 2)) > 1e-3]
xx = xx[np.abs(np.cos(xx + np.pi / 2)) > 1e-3]
check("srx(x+pi/2) - crx(x) == 0 (relative)", relerr(srx(xx + np.pi/2), crx(xx)))
check("sxp(x+pi/2) - cxp(x) == 0 (relative)", relerr(sxp(xx + np.pi/2), cxp(xx)))
check("cxp(x+pi/2) - sxp(x) == 0 (relative)", relerr(cxp(xx + np.pi/2), sxp(xx)))
check("crx(x+pi/2) - srx(x) == 0 (relative)", relerr(crx(xx + np.pi/2), srx(xx)))
# half-turn invariance of primitives (3.II.T5)
check("srx(x+pi) - srx(x) == 0 (relative)", relerr(srx(xx + np.pi), srx(xx)))
check("cxp(x+pi) - cxp(x) == 0 (relative)", relerr(cxp(xx + np.pi), cxp(xx)))

# ---------------------------------------------------------------- Fig 3: positive reciprocal transform (3.IV)
f = lambda u: np.sqrt(1 + u * u) - u
u = rng.uniform(-8, 8, 40001)
s = f(u)
assert np.all(s > 0)
print("PASS f(u) > 0 on samples")
check("f(-u)*f(u) - 1 == 0", np.max(np.abs(f(-u) * f(u) - 1)))
check("u - (1-s^2)/(2s) == 0 (inverse)", np.max(np.abs(u - (1 - s**2) / (2 * s))))
check("f(u) - exp(-arsinh(u)) == 0",
      np.max(np.abs(f(u) - np.exp(-np.arcsinh(u)))))
# rationalized form
check("f(u) - 1/(sqrt(1+u^2)+u) == 0",
      np.max(np.abs(f(u) - 1 / (np.sqrt(1 + u * u) + u))))
# unit threshold: sgn(u) == sgn(1 - s^2) for u != 0
un = u[np.abs(u) > 1e-3]
check("sgn(u) - sgn(1-s^2) == 0",
      np.max(np.abs(np.sign(un) - np.sign(1 - f(un) ** 2))))
assert abs(f(0.0) - 1.0) < TOL
print("PASS threshold s=1 exactly at u=0")
# endpoint limits (affine-chart limitation, 3.IV.T14)
assert f(1e8) < 1e-7 and f(-1e8) > 1e7
print("PASS limits: f(+inf)->0, f(-inf)->+inf (unequal: no global RP1 value)")
# primitives from one map (3.IV.T9/T10), x in D
sx = xx[np.abs(np.sin(xx)) > 1e-3]
cx = xx[np.abs(np.cos(xx)) > 1e-3]
check("sxp(x) - f(cot x) == 0",
      np.max(np.abs(sxp(sx) - f(np.cos(sx) / np.sin(sx)))))
check("srx(x) - f(-cot x) == 0",
      np.max(np.abs(srx(sx) - f(-np.cos(sx) / np.sin(sx)))))
check("crx(x) - f(tan x) == 0",
      np.max(np.abs(crx(cx) - f(np.tan(cx)))))
check("cxp(x) - f(-tan x) == 0",
      np.max(np.abs(cxp(cx) - f(-np.tan(cx)))))

# ---------------------------------------------------------------- Fig 4: FlatWave cophase character (3.V)
FW = lambda x: np.sign(np.sin(2 * x))
xa = rng.uniform(0.05, 2 * np.pi - 0.05, 40001)
xa = xa[np.abs(np.sin(2 * xa)) > 1e-3]       # off seams
check("FW(x+pi/2) + FW(x) == 0 (cophase reversal)",
      np.max(np.abs(FW(xa + np.pi / 2) + FW(xa))))
check("FW(x-pi/2) + FW(x) == 0 (negative cophase reversal)",
      np.max(np.abs(FW(xa - np.pi / 2) + FW(xa))))
check("FW(x+pi) - FW(x) == 0 (half-turn invariance)",
      np.max(np.abs(FW(xa + np.pi) - FW(xa))))
check("FW(x+2pi) - FW(x) == 0 (deck-shift invariance)",
      np.max(np.abs(FW(xa + 2 * np.pi) - FW(xa))))
# octant form FW|_{Oj} = (-1)^{floor(j/2)}
for j in range(8):
    m = (j + 0.5) * np.pi / 4
    assert FW(m) == (-1) ** (j // 2), (j, FW(m))
print("PASS FlatWave octant values (-1)^{floor(j/2)}")
# character homomorphism values: chi(tau_{k pi/2}) = (-1)^k for k=0..3
for k in range(4):
    m = np.pi / 8
    assert FW(m + k * np.pi / 2) == ((-1) ** k) * FW(m), k
print("PASS four-step orbit eps -> -eps -> eps -> -eps -> eps")

# ---------------------------------------------------------------- Fig 5: Rodrigues bridge + seam nonidentity (3.X)
th = np.linspace(0.01, np.pi - 0.01, 20001)
rho = np.tan(th / 2)
check("sxp(theta) - tan(theta/2) == 0 on (0,pi)",
      np.max(np.abs(sxp(th) - rho)))
assert abs(rho[np.argmin(np.abs(th - np.pi / 2))] - 1.0) < 1e-6
print("PASS rho(pi/2) == 1 (FlatWave seam value)")
# q0 = cos(theta/2) != 0 at the FlatWave seam theta = pi/2
assert abs(np.cos(np.pi / 4) - 1 / np.sqrt(2)) < TOL
print("PASS q0(pi/2) = 1/sqrt(2) != 0: seam is regular in Rodrigues chart")
# chart boundary: q0 -> 0 as theta -> pi
assert abs(np.cos((np.pi - 1e-9) / 2)) < 1e-8
print("PASS q0 -> 0 as theta -> pi (chart boundary distinct from seam)")

# ---------------------------------------------------------------- Fig 6: double cover sheets (3.X/3.XI)
q0 = lambda th: np.cos(th / 2)
tt6 = rng.uniform(0, 4 * np.pi, 20001)
check("q0(theta+2pi) + q0(theta) == 0 (deck flip)",
      np.max(np.abs(q0(tt6 + 2 * np.pi) + q0(tt6))))
check("q0(theta+4pi) - q0(theta) == 0 (4pi return)",
      np.max(np.abs(q0(tt6 + 4 * np.pi) - q0(tt6))))
# the two sheets over one rotation period exchange after one full turn:
# sheet A at theta and sheet B at theta coincide with sheet A at theta+2pi swapped
check("sheet exchange: cos((t)/2) vs -cos((t+2pi)/2)",
      np.max(np.abs(q0(tt6) + q0(tt6 + 2 * np.pi))))

# ---------------------------------------------------------------- Fig 7: tautological sign vs FlatWave (3.VII.T8)
t7 = rng.uniform(-3, 3, 40001)
t7 = t7[(np.abs(t7) > 1e-3) & (np.abs(np.abs(t7) - 1) > 1e-3)]
fw_t = np.sign(t7 * (1 - t7 ** 2))
tau_t = np.sign(t7)
# identity FlatWave = (rho*zeta) * sgn(1 - t^2)
check("sgn(t(1-t^2)) - sgn(t)*sgn(1-t^2) == 0",
      np.max(np.abs(fw_t - tau_t * np.sign(1 - t7 ** 2))))
# agreement only on |t| < 1
inn = t7[np.abs(t7) < 1]
out = t7[np.abs(t7) > 1]
assert np.all(np.sign(inn * (1 - inn ** 2)) == np.sign(inn))
assert np.all(np.sign(out * (1 - out ** 2)) == -np.sign(out))
print("PASS agreement on |t|<1, disagreement on |t|>1")
# cross-check with phase form: sgn(t(1-t^2)) == sgn(sin 2x), t = tan(x/2)
x7 = rng.uniform(-1.4, 1.4, 20001)
t7x = np.tan(x7 / 2)
ok7 = (np.abs(np.sin(2 * x7)) > 1e-3) & (np.abs(t7x) > 1e-3) \
    & (np.abs(np.abs(t7x) - 1) > 1e-3)
x7, t7x = x7[ok7], t7x[ok7]
check("sgn(t(1-t^2)) - sgn(sin 2x) == 0",
      np.max(np.abs(np.sign(t7x * (1 - t7x ** 2)) - np.sign(np.sin(2 * x7)))))
# monodromy arithmetic of T10: (-1)^4 = +1 vs tautological -1
assert (-1) ** 4 == 1
print("PASS four cophase multipliers product = +1 (vs tautological -1)")

# ---------------------------------------------------------------- Spin/orientability parity table (3.VIII/3.IX)
# orientable iff n odd  <=>  (n+1) even  <=>  w1 = (n+1) a_n vanishes
# spin (n>=2) iff C(n+1,2) even  <=>  n = 2k+1 with k odd  <=>  n = 3 mod 4
import math
for n in range(1, 8):
    orient = (n % 2 == 1)
    spin_expected = (n == 1) or (n % 4 == 3)
    # spin needs orientability first; then w2 = C(n+1,2) a_n^2 vanishes
    # (for n=1, H^2 = 0 kills w2 regardless of the coefficient)
    spin_from_classes = orient and ((n == 1) or (math.comb(n + 1, 2) % 2 == 0))
    assert spin_expected == spin_from_classes, (n, spin_expected, spin_from_classes)
    assert orient == ((n + 1) % 2 == 0), n
print("PASS n=1..7: orientable<=>n odd; spin<=>n=1 or n=3 mod 4; matches (orientability, C(n+1,2) parity)")
print("table:", [(n, n % 2 == 1, (n == 1) or (n % 4 == 3)) for n in range(1, 8)])

print()
if n_fail:
    print("FAILURES: %d" % n_fail)
    raise SystemExit(1)
print("ALL NUMERICAL CHECKS PASSED (completed numerical checks, ~1e-10; not proofs)")
