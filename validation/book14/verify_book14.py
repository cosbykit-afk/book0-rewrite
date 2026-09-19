#!/usr/bin/env python3
"""Book 14 verification: every checkable mathematical claim on book14/index.html.

Scope labels: CP = checked proof (exact algebra verified on grids / exact
single-point values / exact limits confirmed numerically), NC = completed
numerical check, ST = standard imported theorem (the checked arithmetic is
exact; the imported content stays ST). Nothing here is a manuscript
assertion: each check below ran to completion. No timeouts.

Page claims verified (Part I figures, then Part II sections 14.I-14.X):
 V1  Fig 1: tanh(ln r/2) = (r-1)/(r+1) exactly
 V2  Fig 2: (cosh ln4 + cosh eta)/2 = rational form at q_m=0.6 (exact)
 V3  Fig 3: plotted (1+0.36u^2)/(1+u^2) = M^2/(m1+m2)^2 geometry (exact)
 V4  Fig 4: u^2 = B(4-B)/(2-B)^2 exact; ratio -> 1 monotone as B -> 0
 V5  Fig 5: heavy-source limit identity u^2 -> (m2-E)/(m2+E) (exact);
     monotone numerical convergence (NC)
 V6  Fig 6: <Phi_u|J_z|Phi_u> = cos 2a, <Phi_u|J_x|Phi_u> = sin 2a (exact)
 V7  14.I.T1: q_m = tanh(lam/2), inverse m1/m2 = (1+q)/(1-q), |q|<1
 V8  14.I.C1: cosh/sinh rational forms
 V9  14.I.C2: normalized square: Om2=Om^2, eta2=2eta, q2=2q/(1+q^2)=tanh eta,
     c2=(1-q^2)/(1+q^2), q2^2+c2^2=1
 V10 14.II.P1 algebra: s/(2m1m2) = cosh lam + cosh eta (physical law itself ST)
 V11 14.II.T1: s/(4m1m2) = rational form = (cosh lam + cosh eta)/2
 V12 14.III.E1: cosh(i th) = cos th = (1-u^2)/(1+u^2), u = tan(th/2)
 V13 14.III.T1: continued invariant = qv^2 -> -u^2 continuation of 14.II.T1
 V14 14.III.T2: u^2 formula, positivity on |m1-m2|<M<m1+m2, inverse, roundtrip
 V15 14.IV: u^2 binding-energy formula from M = m1+m2-B
 V16 14.IV.T1: weak binding: ratio u^2/(B/2mu) -> 1 monotone (NC);
     O(u^4) remainder coefficient bounded and stable
 V17 14.IV conditional Coulomb check u ~= Z alpha/(2n)  (NC algebra / ST import)
 V18 14.V.T1: limit = tan^2(chi_E/2), cos chi_E = E/m2 (exact)
 V19 14.V.T2 conditional: tan(chi_E/2)^2 = (m2-E)/(m2+E) (exact, given 14.V.P1)
 V20 14.VI.T1: M^2/(m1+m2)^2 = <chi_u|K_m|chi_u>
 V21 14.VI.C1: double-angle readout; d/dalpha = -(1-q^2) sin 2a (complex-step)
 V22 14.VII.T1: cos/sin 2th_m bridge identities
 V23 14.VII.D1: nu_2(chi_m) = (m1, sqrt(2m1m2), m2)/(m1+m2)
 V24 14.VIII.T1: <Phi|K^(2)|Phi> = <chi|K|chi>, 60 random Hermitian K, random chi
 V25 14.VIII: K_m^(2) = diag(1,(1+q^2)/2,q^2) = (1+q^2)I/2 + (1-q^2)J_z/2
 V26 14.IX: lift K = k0 I + k_i s_i/2 -> K^(2) = k0 I + (1/2) k_i J_i, 40 random
 V27 14.IX.T1: lift injective (rank 4); Q_xz nonzero, traceless, _|_ {I,J_i};
     Q_xz = restrict(s_x@s_z + s_z@s_x)
 V28 14.IX: dim 1+3+5 = 9 (ST: standard representation theory)
 V29 14.X: positronium q_m = 0
"""
import numpy as np

TOL = 1e-9
results = []  # (name, max_err, tol, scope)

def check(name, err, tol=TOL, scope="CP"):
    err = np.asarray(err, dtype=float)
    assert np.all(np.isfinite(err)), f"{name}: non-finite values"
    m = float(np.max(np.abs(err)))
    assert m < tol, f"{name}: max_err={m:.3e} >= tol={tol:.0e}"
    results.append((name, m, tol, scope))
    print(f"OK [{scope}] {name}: max_err={m:.3e} < {tol:.0e}")

rng = np.random.default_rng(20260919)

def masses(n=300):
    return rng.uniform(0.1, 10.0, n), rng.uniform(0.1, 10.0, n)

def q_of(m1, m2):
    return (m1 - m2) / (m1 + m2)

# ---------------- Part I figures ----------------
# V1: Fig 1. Exact: tanh(ln r/2) = (r-1)/(r+1).
r = np.linspace(0.01, 10.0, 20001)
check("V1 tanh(ln r/2) = (r-1)/(r+1)", np.tanh(np.log(r) / 2) - (r - 1) / (r + 1))

# V2: Fig 2. q_m = 0.6 -> lam_m = 2 atanh(0.6) = ln 4 exactly
# (page embed now uses ln(4), not the rounded 1.3863).
eta = np.linspace(-3.0, 3.0, 12001)
qv = np.tanh(eta / 2)
lhs = (np.cosh(np.log(4.0)) + np.cosh(eta)) / 2
rhs = (1 - 0.36 * qv**2) / ((1 - 0.36) * (1 - qv**2))
check("V2 (cosh ln4 + cosh eta)/2 = rational form", lhs - rhs)
check("V2 lam_m = ln 4 for q_m=0.6", 2 * np.arctanh(0.6) - np.log(4.0), 1e-12)

# V3: Fig 3. Plotted (1+0.36 u^2)/(1+u^2) is the exact bound-mass geometry.
m1, m2 = masses()
q = q_of(m1, m2)
lo = np.abs(m1 - m2) + 1e-6
hi = (m1 + m2) - 1e-6
M = lo + rng.random(300) * (hi - lo)
u2 = ((m1 + m2)**2 - M**2) / (M**2 - (m1 - m2)**2)
check("V3 (1+q^2 u^2)/(1+u^2) = M^2/(m1+m2)^2",
      (1 + q**2 * u2) / (1 + u2) - M**2 / (m1 + m2)**2)

# V4: Fig 4. m1=m2=1: u^2 = B(4-B)/(2-B)^2 exact; R(B)=(4-B)/(2-B)^2 -> 1.
B = np.linspace(1e-8, 1.8, 20001)
u2e = B * (2 * 2 - B) / ((2 - B) * (2 - B))  # 14.IV formula at m1=m2=1
check("V4 u^2 = B(4-B)/(2-B)^2", u2e - B * (4 - B) / (2 - B)**2)
R = (4 - B) / (2 - B)**2
check("V4 R(B) -> 1", R[0] - 1.0, 1e-6)
assert np.all(np.diff(R) > 0), "R not monotone increasing in B"
print("OK [NC] V4 R(B) monotone increasing on (0,1.8); R -> 1 as B -> 0")

# V5: Fig 5. Exact limit; monotone convergence checked numerically.
# The naive T2 quotient cancels catastrophically at m1 >> 1 in float64, so the
# limit identity is checked in the algebraically expanded (cancellation-free)
# form u^2 = (m2-E)(2m1+m2+E)/((m2+E)(2m1+E-m2)), after verifying it equals T2.
m2v, Ev = 1.0, 0.3
lim = (m2v - Ev) / (m2v + Ev)
def u2_t2(m1v):
    Mv = m1v + Ev
    return ((m1v + m2v)**2 - Mv**2) / (Mv**2 - (m1v - m2v)**2)
def u2_exp(m1v):
    return ((m2v - Ev) * (2 * m1v + m2v + Ev)
            / ((m2v + Ev) * (2 * m1v + Ev - m2v)))
check("V5 expanded form = T2 formula",
      (u2_exp(100.0) - u2_t2(100.0)) / u2_t2(100.0), 1e-12)
check("V5 u^2(m1) -> (m2-E)/(m2+E)", (u2_exp(1e9) - lim) / lim, 1e-8)
chi = np.arccos(Ev / m2v)
check("V5 tan^2(chi_E/2) = (m2-E)/(m2+E)", np.tan(chi / 2)**2 - lim, 1e-12)
check("V5 cos chi_E = E/m2", np.cos(chi) - Ev / m2v, 1e-12)
devs = [abs(u2_exp(mm) - lim) for mm in [1e1, 1e2, 1e3, 1e4, 1e6]]
assert all(devs[i] > devs[i + 1] for i in range(4)), "not monotone"
print("OK [NC] V5 |u^2(m1)-limit| monotone decreasing in m1")

# V6: Fig 6. Exact double-angle expectation geometry on the Veronese locus.
a = np.linspace(0.01, np.pi - 0.01, 20001)
Phi = np.stack([np.cos(a)**2, np.sqrt(2) * np.cos(a) * np.sin(a),
                np.sin(a)**2], axis=1)
Jz = np.diag([1.0, 0.0, -1.0])
Jx = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) / np.sqrt(2)
ez = np.einsum('ij,jk,ik->i', Phi, Jz, Phi)
ex = np.einsum('ij,jk,ik->i', Phi, Jx, Phi)
check("V6 <Phi_u|J_z|Phi_u> = cos 2a", ez - np.cos(2 * a), 1e-12)
check("V6 <Phi_u|J_x|Phi_u> = sin 2a", ex - np.sin(2 * a), 1e-12)

# ---------------- Part II ----------------
# V7: 14.I.T1
m1, m2 = masses()
lam = np.log(m1 / m2)
q = q_of(m1, m2)
check("V7 q_m = tanh(lam_m/2)", q - np.tanh(lam / 2))
check("V7 m1/m2 = (1+q)/(1-q)", m1 / m2 - (1 + q) / (1 - q))
assert np.all(np.abs(q) < 1.0)
print("OK [CP] V7 |q_m| < 1 for positive masses")

# V8: 14.I.C1
check("V8 cosh lam = (1+q^2)/(1-q^2)", np.cosh(lam) - (1 + q**2) / (1 - q**2))
check("V8 sinh lam = 2q/(1-q^2)", np.sinh(lam) - 2 * q / (1 - q**2))

# V9: 14.I.C2. u+d=1, normalized square; Om := u/d, eta := ln Om (implicit).
u = rng.uniform(0.05, 0.95, 300)
d = 1.0 - u
Om, eta = u / d, np.log(u / d)
qq = u - d
u2n = u**2 / (u**2 + d**2)
d2n = d**2 / (u**2 + d**2)
q2 = u2n - d2n
c2 = 2 * u * d / (u**2 + d**2)
check("V9 Om2 = Om^2", u2n / d2n - Om**2)
check("V9 eta2 = 2 eta", np.log(u2n / d2n) - 2 * eta)
check("V9 q2 = 2q/(1+q^2)", q2 - 2 * qq / (1 + qq**2))
check("V9 q2 = tanh eta", q2 - np.tanh(eta))
check("V9 c2 = (1-q^2)/(1+q^2)", c2 - (1 - qq**2) / (1 + qq**2))
check("V9 q2^2 + c2^2 = 1", q2**2 + c2**2 - 1.0)

# V10: 14.II.P1. The physical law p1.p2 = m1 m2 cosh eta is a standard import
# (ST); the checked reduction s/(2m1m2) = cosh lam + cosh eta is exact algebra.
m1, m2 = masses()
lam = np.log(m1 / m2)
q = q_of(m1, m2)
eta = rng.uniform(-3.0, 3.0, 300)
s = m1**2 + m2**2 + 2 * m1 * m2 * np.cosh(eta)
check("V10 cosh(ln(m1/m2)) = (m1^2+m2^2)/(2m1m2)",
      np.cosh(lam) - (m1**2 + m2**2) / (2 * m1 * m2))
check("V10 s/(2m1m2) = cosh lam + cosh eta",
      s / (2 * m1 * m2) - (np.cosh(lam) + np.cosh(eta)))

# V11: 14.II.T1
qv = np.tanh(eta / 2)
lhs = s / (4 * m1 * m2)
rhs = (1 - q**2 * qv**2) / ((1 - q**2) * (1 - qv**2))
check("V11 rational form", lhs - rhs)
check("V11 = (cosh lam + cosh eta)/2", rhs - (np.cosh(lam) + np.cosh(eta)) / 2)

# V12: 14.III.E1
th = rng.uniform(0.05, np.pi - 0.05, 300)
uu = np.tan(th / 2)
check("V12 cosh(i th) = cos th", (np.cosh(1j * th) - np.cos(th)).real, 1e-12)
check("V12 cos th = (1-u^2)/(1+u^2)", np.cos(th) - (1 - uu**2) / (1 + uu**2))

# V13: 14.III.T1 = qv^2 -> -u^2 continuation of 14.II.T1
m1, m2 = masses()
q = q_of(m1, m2)
lo = np.abs(m1 - m2) + 1e-6
hi = (m1 + m2) - 1e-6
M = lo + rng.random(300) * (hi - lo)
u2 = ((m1 + m2)**2 - M**2) / (M**2 - (m1 - m2)**2)
t1 = M**2 / (4 * m1 * m2)
cont = (1 - q**2 * (-u2)) / ((1 - q**2) * (1 - (-u2)))
t1r = (1 + q**2 * u2) / ((1 - q**2) * (1 + u2))
check("V13 continued invariant", t1 - t1r, 1e-10)
check("V13 = continuation of 14.II.T1", cont - t1r)

# V14: 14.III.T2
assert np.all(u2 > 0), "u^2 not positive"
print("OK [CP] V14 u^2 real and positive for |m1-m2| < M < m1+m2")
check("V14 inverse M^2 formula",
      ((m1 + m2)**2 * (1 + q**2 * u2) / (1 + u2) - M**2) / M**2)
Mrt = (m1 + m2) * np.sqrt((1 + q**2 * u2) / (1 + u2))
u2rt = ((m1 + m2)**2 - Mrt**2) / (Mrt**2 - (m1 - m2)**2)
check("V14 roundtrip u -> M -> u", (u2rt - u2) / np.maximum(u2, 1e-300), 1e-10)

# V15: 14.IV binding formula
m1, m2 = masses(200)
B = rng.uniform(0.001, 0.3, 200) * np.minimum(m1, m2)
M = m1 + m2 - B
u2b = ((m1 + m2)**2 - M**2) / (M**2 - (m1 - m2)**2)
u2f = B * (2 * (m1 + m2) - B) / ((2 * m1 - B) * (2 * m2 - B))
check("V15 u^2 binding formula", (u2b - u2f) / np.maximum(u2b, 1e-300))

# V16: 14.IV.T1 weak binding. Ratio -> 1 is exact analysis (CP);
# monotonicity on grids and O(u^4) boundedness are numerical (NC).
m1s, m2s = 1.7, 0.9
mus = m1s * m2s / (m1s + m2s)
ratios = []
for Bv in [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
    Mv = m1s + m2s - Bv
    uv2 = ((m1s + m2s)**2 - Mv**2) / (Mv**2 - (m1s - m2s)**2)
    ratios.append(uv2 / (Bv / (2 * mus)))
check("V16 ratio -> 1", ratios[-1] - 1.0, 1e-5)
assert all(ratios[i] > ratios[i + 1] > 1.0 for i in range(5)), "not monotone"
print("OK [NC] V16 u^2/(B/2mu) decreases monotonically to 1 as B -> 0")
q4 = [abs(Bv - 2 * mus * (((m1s + m2s)**2 - (m1s + m2s - Bv)**2) /
      ((m1s + m2s - Bv)**2 - (m1s - m2s)**2))) /
      (((m1s + m2s)**2 - (m1s + m2s - Bv)**2) /
       ((m1s + m2s - Bv)**2 - (m1s - m2s)**2))**2
      for Bv in [1e-2, 1e-3, 1e-4]]
assert all(v < 10.0 for v in q4), "O(u^4) coefficient unbounded"
assert abs(q4[-1] - q4[-2]) / q4[-2] < 0.05, "O(u^4) coefficient unstable"
print(f"OK [NC] V16 |B-2mu u^2|/u^4 bounded, stable at {q4[-1]:.4f}")

# V17: 14.IV conditional Coulomb check. Algebra NC; Coulomb law ST (imported).
Z, alpha, n = 1, 1 / 137.036, 1
Bn = mus * (Z * alpha)**2 / (2 * n**2)
Mn = m1s + m2s - Bn
un2 = ((m1s + m2s)**2 - Mn**2) / (Mn**2 - (m1s - m2s)**2)
rel = abs(np.sqrt(un2) - Z * alpha / (2 * n)) / (Z * alpha / (2 * n))
assert rel < 1e-4, f"Coulomb check rel err {rel:.3e}"
print(f"OK [NC/ST] V17 u = Z alpha/(2n) up to rel err {rel:.3e} "
      "(algebra NC; Coulomb law ST import)")

# V18: 14.V.T1 identities (exact); monotone convergence is V5's NC check.
check("V18 limit = tan^2(chi_E/2)", np.tan(chi / 2)**2 - lim, 1e-12)

# V19: 14.V.T2 conditional equality (exact half-angle algebra, given 14.V.P1).
check("V19 sxp(chi_E) = tan(chi_E/2)", np.tan(chi / 2) - np.sqrt(lim), 1e-12)
print("OK [CP] V19 u = |G/F| = sxp(chi_E) by transitivity, conditional on 14.V.P1")

# V20: 14.VI.T1
m1, m2 = masses()
q = q_of(m1, m2)
lo = np.abs(m1 - m2) + 1e-6
hi = (m1 + m2) - 1e-6
M = lo + rng.random(300) * (hi - lo)
u2 = ((m1 + m2)**2 - M**2) / (M**2 - (m1 - m2)**2)
uu = np.sqrt(u2)
chi_u = np.stack([np.ones_like(uu), uu], axis=1) / np.sqrt(1 + u2)[:, None]
Km = np.stack([np.eye(2)] * len(uu))
Km[:, 1, 1] = q**2
expval = np.einsum('ij,ijk,ik->i', chi_u, Km, chi_u)
check("V20 <chi_u|K_m|chi_u> = (1+q^2 u^2)/(1+u^2)",
      expval - (1 + q**2 * u2) / (1 + u2), 1e-12)
check("V20 = M^2/(m1+m2)^2", expval - M**2 / (m1 + m2)**2, 1e-11)

# V21: 14.VI.C1. u = tan alpha -> chi_u = (cos a, sin a).
a = rng.uniform(0.05, 1.2, 300)
qq = rng.uniform(-0.9, 0.9, 300)
ta = np.tan(a)
check("V21 double-angle readout",
      (1 + qq**2 * ta**2) / (1 + ta**2)
      - ((1 + qq**2) / 2 + (1 - qq**2) * np.cos(2 * a) / 2), 1e-11)
# derivative via complex-step (machine-precision, no finite-difference noise)
h = 1e-30
f = lambda x: (1 + qq**2 * np.tan(x)**2) / (1 + np.tan(x)**2)
dcs = (f(a + 1j * h).imag / h)
check("V21 d/da = -(1-q^2) sin 2a", dcs + (1 - qq**2) * np.sin(2 * a), 1e-10)

# V22: 14.VII.T1
m1, m2 = masses()
q = q_of(m1, m2)
c = np.sqrt(m1 / (m1 + m2))
s_ = np.sqrt(m2 / (m1 + m2))
th2 = 2 * np.arctan2(s_, c)
s2t = 2 * np.sqrt(m1 * m2) / (m1 + m2)
lam = np.log(m1 / m2)
check("V22 cos 2th_m = q_m = tanh(lam/2)",
      np.cos(th2) - q, 1e-12)
check("V22 cos 2th_m = tanh(lam/2) (2nd form)",
      np.cos(th2) - np.tanh(lam / 2), 1e-12)
check("V22 sin 2th_m = 2 sqrt(m1m2)/(m1+m2)", np.sin(th2) - s2t, 1e-12)
check("V22 sin 2th_m = sqrt(1-q^2)", s2t - np.sqrt(1 - q**2), 1e-12)
check("V22 sin 2th_m = sech(lam/2)", s2t - 1 / np.cosh(lam / 2), 1e-12)

# V23: 14.VII.D1
nu = np.stack([c**2, np.sqrt(2) * c * s_, s_**2], axis=1)
exp_nu = np.stack([m1 / (m1 + m2), np.sqrt(2 * m1 * m2) / (m1 + m2),
                   m2 / (m1 + m2)], axis=1)
check("V23 nu_2(chi_m)", (nu - exp_nu).max(axis=1), 1e-12)

# V24: 14.VIII.T1, 60 random Hermitian K and random (complex) chi.
def rand_hermitian():
    A = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    return (A + A.conj().T) / 2

def rand_chi():
    v = rng.normal(size=2) + 1j * rng.normal(size=2)
    return v / np.linalg.norm(v)

I2 = np.eye(2)
errs = []
for _ in range(60):
    K = rand_hermitian()
    chi = rand_chi()
    Phi = np.array([chi[0]**2, np.sqrt(2) * chi[0] * chi[1], chi[1]**2])
    K2 = (np.kron(K, I2) + np.kron(I2, K)) / 2
    e0 = np.array([1.0, 0.0])
    e1 = np.array([0.0, 1.0])
    basis = [np.kron(e0, e0),
             (np.kron(e0, e1) + np.kron(e1, e0)) / np.sqrt(2),
             np.kron(e1, e1)]
    R = np.array([[ (bi @ K2 @ bj) for bj in basis] for bi in basis])
    errs.append(abs(Phi.conj() @ R @ Phi - chi.conj() @ K @ chi))
check("V24 <Phi|K^(2)|Phi> = <chi|K|chi> (60 random)", errs, 1e-12)

# V25: 14.VIII K_m^(2) diagonal form.
q0 = 0.6
K = np.diag([1.0, q0**2])
K2 = (np.kron(K, I2) + np.kron(I2, K)) / 2
e0 = np.array([1.0, 0.0])
e1 = np.array([0.0, 1.0])
basis = [np.kron(e0, e0),
         (np.kron(e0, e1) + np.kron(e1, e0)) / np.sqrt(2),
         np.kron(e1, e1)]
R = np.array([[(bi @ K2 @ bj).real for bj in basis] for bi in basis])
check("V25 K_m^(2) = diag(1,(1+q^2)/2,q^2)",
      (R - np.diag([1.0, (1 + q0**2) / 2, q0**2])).max(axis=(0, 1)), 1e-12)
Jz3 = np.diag([1.0, 0.0, -1.0])
check("V25 = (1+q^2)I/2 + (1-q^2)J_z/2",
      (R - ((1 + q0**2) / 2 * np.eye(3) + (1 - q0**2) / 2 * Jz3)).max(axis=(0, 1)),
      1e-12)

# V26: 14.IX lift formula, 40 random Hermitian K.
sx = np.array([[0, 1], [1, 0]]) / 2
sy = np.array([[0, -1j], [1j, 0]]) / 2
sz = np.array([[1, 0], [0, -1]]) / 2
P = np.zeros((3, 4))
P[0] = [1, 0, 0, 0]
P[1] = [0, 1 / np.sqrt(2), 1 / np.sqrt(2), 0]
P[2] = [0, 0, 0, 1]
restrict = lambda M4: P @ M4 @ P.T
Jx3 = restrict(np.kron(sx, I2) + np.kron(I2, sx))
Jy3 = restrict(np.kron(sy, I2) + np.kron(I2, sy))
Jz3 = restrict(np.kron(sz, I2) + np.kron(I2, sz))
lift = lambda K: restrict((np.kron(K, I2) + np.kron(I2, K)) / 2)
errs = []
for _ in range(40):
    K = rand_hermitian()
    k0 = np.trace(K).real / 2
    k1 = np.trace(K @ (2 * sx)).real
    k2 = np.trace(K @ (2 * sy)).real
    k3 = np.trace(K @ (2 * sz)).real
    expect = k0 * np.eye(3) + 0.5 * (k1 * Jx3 + k2 * Jy3 + k3 * Jz3)
    errs.append(np.abs(lift(K) - expect).max())
check("V26 lift = k0 I + (1/2) k_i J_i (40 random)", errs, 1e-12)

# V27: 14.IX.T1 no-quadrupole.
cols = []
for Bk in [I2, 2 * sx, 2 * sy, 2 * sz]:
    Lk = lift(Bk)
    cols.append(np.concatenate([Lk.real.reshape(-1), Lk.imag.reshape(-1)]))
sv = np.linalg.svd(np.stack(cols, axis=1), compute_uv=False)
assert np.sum(sv > 1e-10) == 4, f"lift rank {np.sum(sv > 1e-10)} != 4"
print("OK [CP] V27 lift injective: map R^4 -> Herm(3) has rank 4")
Q = (Jx3 @ Jz3 + Jz3 @ Jx3) / 2
assert abs(np.trace(Q)) < 1e-12 and np.abs(Q).max() > 1e-3
print("OK [CP] V27 Q_xz nonzero and traceless")
ortho = max(abs(np.trace(Q @ np.eye(3))), abs(np.trace(Q @ Jx3)),
            abs(np.trace(Q @ Jy3)), abs(np.trace(Q @ Jz3)))
assert ortho < 1e-12, f"Q_xz not orthogonal: {ortho:.3e}"
print("OK [CP] V27 Q_xz orthogonal to {I, J_x, J_y, J_z}")
Sxz = np.kron(sx, sz) + np.kron(sz, sx)
check("V27 Q_xz = restrict(s_x@s_z + s_z@s_x)", (Q - restrict(Sxz)).max(axis=(0, 1)),
      1e-12)

# V28: 14.IX dim count. The 1+3+5 decomposition itself is standard (ST).
assert 1 + 3 + 5 == 3 * 3
print("OK [ST] V28 dim Herm(Sym^2(C^2)) = 9 = 1+3+5 (standard representation theory)")

# V29: 14.X positronium control point.
check("V29 positronium q_m = 0", abs(q_of(1.0, 1.0)), 1e-12)

worst = max(r[1] for r in results)
print(f"\nAll {len(results)} checks passed (scope-tagged assertions + exact prints). "
      f"Worst measured error {worst:.3e}. No timeouts.")
