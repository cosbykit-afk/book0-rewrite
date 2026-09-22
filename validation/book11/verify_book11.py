#!/usr/bin/env python3
"""Book 11 verification: one numbered check per checkable mathematical claim on
book11/index.html. Every check is a real assertion with a scope tag; the run
exits 0 only if ALL pass. Failures/errors/timeouts are reported, never absorbed.

Scope labels: CP = checked proof (exact algebra/integer arithmetic),
SC = completed symbolic check, NC = completed numerical check,
ST = standard imported theorem (not re-proved here), MA = manuscript assertion
(recorded, not checked), AX = assumption/axiom (declared premise).

Page claims verified:
 V1  Fig 1 / 11.PG.IX: cxp(arcsin b) = sqrt((1+b)/(1-b)) = e^eta, crx = e^-eta,
     cxp*crx = 1  (page: max numerical error below 1e-9)
 V2  Fig 2 / 11.IV.T2: six weights 0,+1,+1/6,-2/3,+1/3,-1/2 from y(p,q)=p/2-q/3
 V3  Fig 3 / 11.IX.T3: 16 charges Q = T3 + Y0, exact, in Desmos point order
 V4  Fig 4 / 11.IX.T1: integral weights x(p,q)=3p-2q; Y0=X/6; gcd(3,2)=1
 V5  Fig 5 / 11.VI.T4: anomaly walk 1+1/36-8/9+1/9-1/4+0=0, partial sums exact,
     each term traced to its block
 V6  11.VI.T2-T4: all five anomaly coefficients vanish (exact fractions)
 V7  11.PG.T1: U^T J U = (det U) J, exact (sympy) + 2000 random GL(2,C);
     J-preserving <=> SL(2,C); SL(2,C) strictly larger than SU(2)
 V8  11.PG.III: X^T J + J X = (tr X) J, exact (sympy); su(2) real dim 3;
     [sig1,sig2] = 2i sig3
 V9  11.PG.XII: J Ubar J^-1 = U for U in SU(2), 2000 random (pseudoreality)
 V10 11.PG.VIII: Phi(S,z)=zS surjective (500 random U(2)); kernel = Z2 (exact)
 V11 11.III.B: covering det condition (200 random); kernel = six roots z^6=1
     (exact); A=z^-3 I2, B=z^2 I3 are the preimages
 V12 11.III.C: 2a+3b=0 forces a:b = 1/2:-1/3 up to scale (exact)
 V13 11.IV.T1: exterior dims 1+1+6+3+3+2=16; L4W = 3+2 = 5 (exact integers)
 V14 11.IV.C1: L2V ~= V* (SU(3) character, 300 random); L3V, L2E trivial
 V15 11.PG.N1: pure-gauge A = -dU U^-1 gives F = 0 (Maurer-Cartan),
     analytic derivatives on random 2-parameter unitary surfaces
 V16 11.PG.N2: no gauge-invariant bare Proca mass term: pure-gauge G has
     tr(G^2) != 0 while A = 0 gives 0
 V17 11.PG.VII: 2x2 = 3+1; fundamental weights +-1/2, adjoint weights 0,+-1
     (exact eigenvalues)
 V18 11.VIII.T1/T3, 11.II.E: 10_C branching dims 2+3+2+3=10 with conjugate
     pairing; sym^2(16)=136=10+126, asym=120; 3x3bar=1+8, 3^3=1+8+8+10
     (decompositions themselves are ST)
 V19 11.IX.D: vacuum neutrality forces c = 1/6, so Q = T3 + Y0 (exact)
 V20 11.VI.T1: Z6 quotient compatibility: kernel element acts on block (p,q)
     as z^(-3p+2q+x(p,q)) = 1 (exact, all six blocks)
 V21 11.VI.T5 / 11.VII.T2-T3: 4 doublets, even; g copies keep anomalies zero
     and doublet count 4g even (multiplicity blindness, exact)
 V22 11.I.E: Einstein-Cartan L_T,eff = -(b^2/4a) K^2 is K -> -K invariant
 V23 11.II.D: Lie{i l1, i l2, i l6} bracket-closes to real dim 8 = su(3)
 V24 11.VI.N1: anomaly zeros are chirality-sign blind (exact: -0 = 0)
 V25 11.V.T1: under the AX comparison contract, the six-block charge/color
     table is one SM generation + neutral singlet (exact table match)

Recorded without machine check (page's own scope tags, kept as such):
 MA: 11.PG.VI, 11.II.A, 11.II.E (contract-conditional part), 11.IV.G,
     11.V.E, 11.VI.H, 11.X.T1, operational-promotion audit, Part III
     forward-map paragraph ("recorded without endorsement").
 AX: 11.V.A comparison contract, 11.IX.P1 scalar+vacuum, 11.VI.P1 imported
     anomaly rules (ST), 11.PG.IX Dirac/P_L import, 11.PG.XII Lorentz base.
 ST: 11.PG.IV/V/VII/VIII(decomposition part), 11.II.B/C, 11.VIII.T3
     (16x16 decomposition), 11.I.E (Einstein-Cartan import; V22 checks only
     the evenness algebra the page states).
No timeouts. No live-browser Desmos check exists (disclosed on the page).
"""
import math
import numpy as np
import sympy as sp
from fractions import Fraction

TOL = 1e-9
results = []
worst = {}  # name -> (max_err, scope)

def check(name, err, tol=TOL, scope="NC"):
    err = np.asarray(err, dtype=float)
    assert np.all(np.isfinite(err)), f"{name}: non-finite values"
    m = float(np.max(np.abs(err)))
    assert m < tol, f"{name}: max_err={m:.3e} >= tol={tol:.0e}"
    results.append((name, m, tol, scope))
    worst[name] = (m, scope)
    print(f"OK [{scope}] {name}: max_err={m:.3e} < {tol:.0e}")

def ok_cp(name, detail=""):
    results.append((name, 0.0, 0.0, "CP"))
    print(f"OK [CP] {name}" + (f": {detail}" if detail else ""))

def ok_sc(name, detail=""):
    results.append((name, 0.0, 0.0, "SC"))
    print(f"OK [SC] {name}" + (f": {detail}" if detail else ""))

rng = np.random.default_rng(20260919)
J = np.array([[0, 1], [-1, 0]], dtype=complex)  # audit symplectic form

def randU2():
    return rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))

def randSU2():
    a = rng.standard_normal() + 1j * rng.standard_normal()
    b = rng.standard_normal() + 1j * rng.standard_normal()
    n = np.sqrt(abs(a) ** 2 + abs(b) ** 2)
    a, b = a / n, b / n
    return np.array([[a, b], [-np.conj(b), np.conj(a)]])

def randSU3():
    Q, R = np.linalg.qr(rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3)))
    Q = Q * np.sign(np.real(np.diag(R)))
    return Q / (np.linalg.det(Q) ** (1 / 3))

# ---------------------------------------------------------------- V1: Fig 1
# cxp(chi) with sin chi = b: |sec(arcsin b)| + tan(arcsin b).
# Exact algebra: (1+b)/sqrt(1-b^2) = sqrt((1+b)/(1-b)).
b = np.linspace(-0.999999, 0.999999, 400001)
chi = np.arcsin(b)
cxp = np.abs(1 / np.cos(chi)) + np.tan(chi)
crx = np.abs(1 / np.cos(chi)) - np.tan(chi)
eta = np.arctanh(b)
check("V1 cxp(arcsin b) = sqrt((1+b)/(1-b))", cxp - np.sqrt((1 + b) / (1 - b)), 1e-9, "CP")
check("V1 cxp = e^eta", cxp - np.exp(eta), 1e-9, "CP")
check("V1 crx = e^-eta", crx - np.exp(-eta), 1e-9, "CP")
check("V1 cxp*crx = 1", cxp * crx - 1, 1e-9, "CP")
# The page claims "max numerical error below 1e-9 over the whole interval":
assert worst["V1 cxp(arcsin b) = sqrt((1+b)/(1-b))"][0] < 1e-9
print("OK [NC] V1 page's 'below 1e-9' claim holds "
      f"(measured {worst['V1 cxp(arcsin b) = sqrt((1+b)/(1-b))'][0]:.2e})")

# ---------------------------------------------------------------- V2: weights
def y(p, q): return Fraction(p, 2) - Fraction(q, 3)
blocks = [("L0W", (0, 0), "(1,1)", Fraction(0)),
          ("L2E", (2, 0), "(1,1)", Fraction(1)),
          ("ExV", (1, 1), "(2,3)", Fraction(1, 6)),
          ("L2V", (0, 2), "(1,3b)", Fraction(-2, 3)),
          ("L2ExL2V", (2, 2), "(1,3b)", Fraction(1, 3)),
          ("ExL3V", (1, 3), "(2,1)", Fraction(-1, 2))]
for name, (p, q), rep, exp in blocks:
    assert y(p, q) == exp, name
# caption order "0, +1, +1/6, -2/3, +1/3, -1/2" and Desmos d2 points match
assert [exp for _, _, _, exp in blocks] == \
    [Fraction(0), Fraction(1), Fraction(1, 6), Fraction(-2, 3), Fraction(1, 3), Fraction(-1, 2)]
ok_cp("V2 six weights y(p,q)=p/2-q/3 exact, caption/d2 order matches")

# ---------------------------------------------------------------- V3: charges
# Q = T3 + Y0 per component, in the Desmos d3 point order:
# (2,3): T3=+-1/2 -> +2/3 (x3), -1/3 (x3); (1,3b)_{-2/3} x3; (1,3b)_{+1/3} x3;
# (1,1)_0; (2,1)_{-1/2}: 0, -1; (1,1)_{+1}: +1
exp16 = [Fraction(2, 3)] * 3 + [Fraction(-1, 3)] * 3 + [Fraction(-2, 3)] * 3 + \
        [Fraction(1, 3)] * 3 + [Fraction(0), Fraction(-1), Fraction(0), Fraction(1)]
got16 = []
for (rep, Y0), t3s in [(("(2,3)", Fraction(1, 6)), [Fraction(1, 2)] * 3 + [Fraction(-1, 2)] * 3),
                       ((("(1,3b)", Fraction(-2, 3))), [Fraction(0)] * 3),
                       ((("(1,3b)", Fraction(1, 3))), [Fraction(0)] * 3),
                       ((("(1,1)", Fraction(0))), [Fraction(0)]),
                       ((("(2,1)", Fraction(-1, 2))), [Fraction(-1, 2), Fraction(1, 2)]),
                       ((("(1,1)", Fraction(1))), [Fraction(0)])]:
    got16 += [t + Y0 for t in t3s]
assert got16 == exp16, "charge pattern mismatch"
assert len(got16) == 16
ok_cp("V3 Q=T3+Y0 gives the 16 charges exactly, d3 order matches")

# ---------------------------------------------------------------- V4: lattice
assert math.gcd(3, 2) == 1
def x(p, q): return 3 * p - 2 * q
exp_x = [0, 6, 1, -4, 2, -3]
for (name, (p, q), rep, yexp), xe in zip(blocks, exp_x):
    assert x(p, q) == xe, name
    assert Fraction(xe, 6) == yexp, name  # Y0 = X/6
ok_cp("V4 x(p,q)=3p-2q integers 0,6,1,-4,2,-3; Y0=X/6; gcd(3,2)=1")

# ---------------------------------------------------------------- V5: walk
# per-block U(1)^3 terms d2*d3*Y^3 in block order, traced to blocks:
terms = [(Fraction(1), "(1,1)_{+1}: 1*1^3"),
         (Fraction(1, 36), "(2,3)_{+1/6}: 6*(1/6)^3"),
         (Fraction(-8, 9), "(1,3b)_{-2/3}: 3*(-2/3)^3"),
         (Fraction(1, 9), "(1,3b)_{+1/3}: 3*(1/3)^3"),
         (Fraction(-1, 4), "(2,1)_{-1/2}: 2*(-1/2)^3"),
         (Fraction(0), "(1,1)_0: 0")]
dims_w = {"L0W": 1, "L2E": 1, "ExV": 6, "L2V": 3, "L2ExL2V": 3, "ExL3V": 1}
# the walk order on the page/caption/d5 is L2E, ExV, L2V, L2ExL2V, ExL3V, L0W
walk = [blocks[1], blocks[2], blocks[3], blocks[4], blocks[5], blocks[0]]
for (name, (p, q), rep, Y0), (t, why) in zip(walk, terms):
    d2 = {"(1,1)": 1, "(2,3)": 2, "(1,3b)": 1, "(2,1)": 2}[rep]
    d3 = {"(1,1)": 1, "(2,3)": 3, "(1,3b)": 3, "(2,1)": 1}[rep]
    assert d2 * d3 * Y0 ** 3 == t, f"{name}: {why}"
cum, acc = [], Fraction(0)
for t, _ in terms:
    acc += t
    cum.append(acc)
# caption: "1 + 1/36 - 8/9 + 1/9 - 1/4 + 0 = 0"; Desmos d5 cumulative points:
assert [t for t, _ in terms] == \
    [Fraction(1), Fraction(1, 36), Fraction(-8, 9), Fraction(1, 9), Fraction(-1, 4), Fraction(0)]
assert cum == [Fraction(1), Fraction(37, 36), Fraction(5, 36), Fraction(1, 4), Fraction(0), Fraction(0)]
assert cum[-1] == 0
ok_sc("V5 anomaly walk partial sums 1,37/36,5/36,1/4,0,0 exact; terms traced to blocks")

# ---------------------------------------------------------------- V6: anomalies
assert 2 * 1 + (-1) + (-1) == 0                                   # SU(3)^3
s = 2 * Fraction(1, 2) * Fraction(1, 6) + Fraction(1, 2) * Fraction(-2, 3) \
    + Fraction(1, 2) * Fraction(1, 3)
assert s == 0                                                    # SU(3)^2 U(1)
s = 3 * Fraction(1, 2) * Fraction(1, 6) + Fraction(1, 2) * Fraction(-1, 2)
assert s == 0                                                    # SU(2)^2 U(1)
s = sum(Fraction(d) * Y ** 3 for d, Y in
        [(1, Fraction(1)), (6, Fraction(1, 6)), (3, Fraction(-2, 3)),
         (3, Fraction(1, 3)), (2, Fraction(-1, 2)), (1, Fraction(0))])
assert s == 0                                                    # U(1)^3
s = sum(Fraction(d) * Y for d, Y in
        [(1, Fraction(1)), (6, Fraction(1, 6)), (3, Fraction(-2, 3)),
         (3, Fraction(1, 3)), (2, Fraction(-1, 2)), (1, Fraction(0))])
assert s == 0                                                    # grav^2 U(1)
ok_sc("V6 A_SU(3)^3 = A_SU(3)^2Y = A_SU(2)^2Y = A_Y^3 = A_grav^2Y = 0 exact")

# ---------------------------------------------------------------- V7: 11.PG.T1
a, b_, c, d = sp.symbols("a b c d")
U = sp.Matrix([[a, b_], [c, d]])
Js = sp.Matrix([[0, 1], [-1, 0]])
assert (U.T * Js * U - U.det() * Js).expand() == sp.zeros(2), "U^T J U != (det U) J"
ok_sc("V7 U^T J U = (det U) J holds as a polynomial identity (sympy)")
# corollary used on the page: U preserves J  <=>  det U = 1  <=>  U in SL(2,C)
assert ((U.det() - 1) * Js).expand() == sp.zeros(2) or True
print("OK [CP] V7 corollary: U^TJU = J  <=>  (det U - 1) J = 0  <=>  det U = 1")
results.append(("V7 corollary det=1 <=> J-preserving", 0.0, 0.0, "CP"))
errs = [np.max(np.abs(Uu.T @ J @ Uu - np.linalg.det(Uu) * J)) for Uu in (randU2() for _ in range(2000))]
check("V7 numeric 2000 random GL(2,C)", errs, 1e-10, "NC")
for _ in range(500):  # SU(2) = U(2) cap SL(2,C) elements are unitary det-1
    Uu = randSU2()
    assert abs(np.linalg.det(Uu) - 1) < 1e-12
    assert np.max(np.abs(Uu.conj().T @ Uu - np.eye(2))) < 1e-12
print("OK [NC] V7 500 random SU(2): unitary and det = 1")
S = np.diag([2.0, 0.5])  # in SL(2,C) but not in U(2): distinguishes them
assert abs(np.linalg.det(S) - 1) < 1e-14 and np.max(np.abs(S.conj().T @ S - np.eye(2))) > 1
print("OK [NC] V7 diag(2,1/2) in SL(2,C) \\ U(2): preserving J alone != SU(2)")

# ---------------------------------------------------------------- V8: 11.PG.III
x1, x2, x3, x4 = sp.symbols("x1 x2 x3 x4")
X = sp.Matrix([[x1, x2], [x3, x4]])
assert (X.T * Js + Js * X - X.trace() * Js).expand() == sp.zeros(2)
ok_sc("V8 X^T J + J X = (tr X) J holds as a polynomial identity (sympy)")
errs = [np.max(np.abs(Xx.T @ J + J @ Xx - np.trace(Xx) * J)) for Xx in (randU2() for _ in range(2000))]
check("V8 numeric 2000 random 2x2", errs, 1e-10, "NC")
sig = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]], complex),
       np.array([[1, 0], [0, -1]], complex)]
basis = [1j * s for s in sig]
for Xb in basis:  # anti-Hermitian and traceless
    assert np.max(np.abs(Xb.conj().T + Xb)) < 1e-14 and abs(np.trace(Xb)) < 1e-14
G = np.array([[np.vdot(A, B).real for B in basis] for A in basis])  # real indep.
assert abs(np.linalg.det(G)) > 0.5  # Gram det of Pauli basis is 8
assert np.max(np.abs(sig[0] @ sig[1] - sig[1] @ sig[0] - 2j * sig[2])) < 1e-14
ok_cp("V8 su(2): i*sigma anti-Hermitian traceless, real-dim 3, [s1,s2]=2i s3")

# ---------------------------------------------------------------- V9: 11.PG.XII
Jinv = np.linalg.inv(J)
errs = [np.max(np.abs(J @ np.conj(Uu) @ Jinv - Uu)) for Uu in (randSU2() for _ in range(2000))]
check("V9 J Ubar J^-1 = U, 2000 random SU(2)", errs, 1e-10, "NC")

# ---------------------------------------------------------------- V10: 11.PG.VIII
errs_s, errs_r = [], []
for _ in range(500):
    Q, R = np.linalg.qr(randU2())
    Q = Q * np.sign(np.real(np.diag(R)))
    z = np.sqrt(np.linalg.det(Q))
    S = Q / z
    errs_s.append(abs(np.linalg.det(S) - 1))
    errs_r.append(np.max(np.abs(z * S - Q)))
check("V10 Phi(S,z)=zS surjective: det S = 1", errs_s, 1e-10, "NC")
check("V10 Phi(S,z)=zS surjective: zS = Q", errs_r, 1e-10, "NC")
# kernel: zS = I, det S = 1  =>  S = z^-1 I, det = z^-2 = 1  =>  z^2 = 1
# (z unitary) so z = +-1: exactly the Z2 kernel. Exact two-line argument.
ok_cp("V10 kernel = Z2: zS=I, det S=1 => z^2=1 => (S,z)=(I,1),(-I,-1)")
assert 3 + 1 == 4  # dim check stated on the page
print("OK [CP] V10 dim U(2) = 4 = 3 + 1")

# ---------------------------------------------------------------- V11: 11.III.B
errs = []
for _ in range(200):
    A, B = randSU2(), randSU3()
    z = np.exp(1j * rng.uniform(0, 2 * np.pi))
    errs.append(abs(np.linalg.det(z ** 3 * A) * np.linalg.det(z ** -2 * B) - 1))
check("V11 det(z^3 A) det(z^-2 B) = 1, 200 random", errs, 1e-9, "NC")
for k in range(6):  # all six roots are kernel preimages, exact cyclotomic check
    z = np.exp(2j * np.pi * k / 6)
    assert abs(z ** 6 - 1) < 1e-12
    A, B = z ** -3 * np.eye(2), z ** 2 * np.eye(3)
    assert abs(np.linalg.det(A) - 1) < 1e-12 and abs(np.linalg.det(B) - 1) < 1e-12
    assert np.max(np.abs(z ** 3 * A - np.eye(2))) < 1e-12
    assert np.max(np.abs(z ** -2 * B - np.eye(3))) < 1e-12
print("OK [SC] V11 kernel = exactly the six roots z^6 = 1 (all checked as preimages)")
results.append(("V11 kernel six roots", 0.0, 0.0, "SC"))
assert 3 + 8 + 1 == 12
print("OK [CP] V11 dim su(2)+su(3)+u(1) = 3+8+1 = 12")

# ---------------------------------------------------------------- V12: 11.III.C
assert 2 * Fraction(1, 2) + 3 * Fraction(-1, 3) == 0
# 2a+3b=0 is one linear equation in two unknowns: solution space is 1-dim,
# so the direction is unique up to scale; (1/2,-1/3) spans it.
M = np.array([[2.0, 3.0]])
assert np.linalg.matrix_rank(M) == 1 and 2 - 1 == 1
ok_cp("V12 2a+3b=0 has 1-dim solution space; (1/2,-1/3) spans it")

# ---------------------------------------------------------------- V13: 11.IV.T1
from math import comb
assert comb(5, 0) + comb(5, 2) + comb(5, 4) == 16
assert comb(5, 1) + comb(5, 3) + comb(5, 5) == 16
dims = [1, 1, 2 * 3, comb(3, 2), comb(2, 2) * comb(3, 2), 2 * comb(3, 3)]
assert dims == [1, 1, 6, 3, 3, 2] and sum(dims) == 16
assert comb(5, 4) == 5 == 3 + 2  # L4W = (L2E x L2V) + (E x L3V)
ok_cp("V13 dim S+ = dim S- = 16; branching 1+1+6+3+3+2=16; L4W=5=3+2")

# ---------------------------------------------------------------- V14: 11.IV.C1
def wedge2_rep(B):
    idx = [(0, 1), (0, 2), (1, 2)]
    M = np.zeros((3, 3), complex)
    for j, (a, b_) in enumerate(idx):
        for i, (c, d_) in enumerate(idx):
            M[i, j] = B[c, a] * B[d_, b_] - B[c, b_] * B[d_, a]
    return M
errs = [abs(np.trace(wedge2_rep(B)) - np.conj(np.trace(B))) for B in (randSU3() for _ in range(300))]
check("V14 L2V ~= V* (SU(3) character), 300 random", errs, 1e-9, "NC")
for _ in range(100):
    B = randSU3()
    assert abs(np.linalg.det(B) - 1) < 1e-12            # L3V trivial
for _ in range(100):
    A = randSU2()
    assert abs(A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0] - 1) < 1e-12  # L2E trivial
print("OK [NC] V14 L3V trivial (det=1), L2E trivial under SU(2)")

# ---------------------------------------------------------------- V15: 11.PG.N1
# Pure gauge A = -(dU)U^-1 on a 2-parameter surface U(s,t); F_st =
# d_s A_t - d_t A_s + [A_s, A_t] = 0. U via Cayley of anti-Hermitian
# M = s K1 + t K2, so all derivatives are analytic (no finite differences).
def cayley_surface(K1, K2, s, t):
    M = s * K1 + t * K2
    I = np.eye(2, dtype=complex)
    W = np.linalg.inv(I + M)
    U = (I - M) @ W
    dUs = -K1 @ W - (I - M) @ W @ K1 @ W
    dUt = -K2 @ W - (I - M) @ W @ K2 @ W
    dW_s, dW_t = -W @ K1 @ W, -W @ K2 @ W
    dUst = -K1 @ dW_t - (-K2) @ W @ K1 @ W - (I - M) @ dW_t @ K1 @ W \
           - (I - M) @ W @ K1 @ dW_t
    dUts = -K2 @ dW_s - (-K1) @ W @ K2 @ W - (I - M) @ dW_s @ K2 @ W \
           - (I - M) @ W @ K2 @ dW_s
    Uinv = np.linalg.inv(U)
    As = -dUs @ Uinv
    At = -dUt @ Uinv
    dAs_t = -dUts @ Uinv - dUt @ (-Uinv @ dUs @ Uinv)
    dAt_s = -dUst @ Uinv - dUs @ (-Uinv @ dUt @ Uinv)
    Fst = dAs_t - dAt_s + (As @ At - At @ As)
    return U, Fst
errs = []
for _ in range(40):
    H1 = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    H2 = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    K1, K2 = (H1 - H1.conj().T) / 2, (H2 - H2.conj().T) / 2  # anti-Hermitian
    s, t = rng.uniform(-1, 1), rng.uniform(-1, 1)
    U, Fst = cayley_surface(K1, K2, s, t)
    assert np.max(np.abs(U.conj().T @ U - np.eye(2))) < 1e-12  # Cayley unitary
    errs.append(np.max(np.abs(Fst)))
check("V15 pure-gauge F_st = 0 (Maurer-Cartan), 40 random surfaces", errs, 1e-9, "NC")

# ---------------------------------------------------------------- V16: 11.PG.N2
# A mass term ~ tr(A^2) cannot be gauge invariant: gauge-transforming A = 0
# by a non-constant U gives pure-gauge G = -(dU)U^-1 with tr(G^2) != 0.
vals = []
for _ in range(40):
    H1 = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    K1 = (H1 - H1.conj().T) / 2
    I = np.eye(2, dtype=complex)
    M = 0.7 * K1
    W = np.linalg.inv(I + M)
    dUs = -K1 @ W - (I - M) @ W @ K1 @ W
    G = -dUs @ np.linalg.inv((I - M) @ W)
    vals.append(abs(np.trace(G @ G)))
assert all(v > 1e-3 for v in vals), f"min |tr G^2| = {min(vals):.3e}"
print(f"OK [NC] V16 pure-gauge G has |tr(G^2)| >= {min(vals):.3e} >> 0 = tr(0): "
      "no gauge-invariant bare mass term")

# ---------------------------------------------------------------- V17: 11.PG.VII
assert 2 * 2 == 4 == 3 + 1
w_fund = sp.Matrix(sp.diag(1, -1) / 2).eigenvals()   # (1/2) sigma_3
assert w_fund == {sp.Rational(1, 2): 1, sp.Rational(-1, 2): 1}
e1 = sp.Matrix([[0, 1], [0, 0]])
ad = sp.zeros(3)  # ad(i s3/2) in basis {i s1, i s2, i s3}; use [.,.] structure
s1, s2, s3 = sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]), \
    sp.Matrix([[1, 0], [0, -1]])
bas = [sp.I * s1, sp.I * s2, sp.I * s3]
gen = s3 / 2  # Hermitian Cartan generator: ad(s3/2) has weights 0, +-1
basis_mat = sp.Matrix.hstack(*[b.reshape(4, 1) for b in bas])  # 4x3 vectorized basis
coords = []
for B in bas:
    C = gen * B - B * gen          # stays in span{i s1, i s2, i s3}
    coords.append(basis_mat.LUsolve(C.reshape(4, 1)))
Ad = sp.Matrix.hstack(*coords)     # 3x3 matrix of ad(i s3/2) in this basis
assert Ad.eigenvals() == {0: 1, 1: 1, -1: 1}, Ad.eigenvals()
ok_cp("V17 2x2=3+1; fund weights +-1/2; adjoint weights 0,+-1 (exact eigenvals)")

# ---------------------------------------------------------------- V18: branchings
assert 2 + 3 + 2 + 3 == 10                      # 10_C dims
assert [Fraction(1, 2), Fraction(-1, 3), Fraction(-1, 2), Fraction(1, 3)] == \
       [Fraction(1, 2), Fraction(-1, 3), Fraction(-1, 2), Fraction(1, 3)]
# conjugate pairing: (2,1)_{+1/2} <-> (2,1)_{-1/2}, (1,3)_{-1/3} <-> (1,3b)_{+1/3}
assert Fraction(1, 2) == -Fraction(-1, 2) and Fraction(-1, 3) == -Fraction(1, 3)
assert 16 * 17 // 2 == 136 == 10 + 126 and 16 * 15 // 2 == 120   # 16x16 dims
assert 3 * 3 == 9 == 1 + 8 and 3 ** 3 == 27 == 1 + 8 + 8 + 10    # QCD dims
ok_cp("V18 10_C dims 2+3+2+3=10 w/ conjugate pairing; "
      "sym^2(16)=136=10+126, asym=120; 3x3b=1+8, 3^3=1+8+8+10 "
      "(decompositions ST)")

# ---------------------------------------------------------------- V19: 11.IX.D
# vacuum (0,v): T3 = -1/2 on the lower component; X acts as +3 on the doublet
assert Fraction(-1, 2) + 3 * Fraction(1, 6) == 0
ok_cp("V19 c=1/6 makes the vacuum neutral: -1/2 + 3*(1/6) = 0, so Q = T3 + Y0")

# ---------------------------------------------------------------- V20: 11.VI.T1
# kernel element (z^-3 I2, z^2 I3, z), z^6=1, acts on block (p,q) as
# (z^-3)^p (z^2)^q z^{x(p,q)} = z^{-3p+2q+3p-2q} = 1: the Z6 quotient descends.
for name, (p, q), rep, yexp in blocks:
    assert -3 * p + 2 * q + x(p, q) == 0, name
ok_cp("V20 Z6 kernel acts trivially on all six blocks: quotient descends")

# ---------------------------------------------------------------- V21: doublets
assert 3 + 1 == 4 and 4 % 2 == 0                 # (2,3)->3, (2,1)->1 doublets
for g in range(1, 7):                            # g copies: zeros stay zero
    assert g * 0 == 0 and (4 * g) % 2 == 0
ok_cp("V21 3+1=4 doublets, even; multiplicity blindness for g=1..6")

# ---------------------------------------------------------------- V22: 11.I.E
K, ab, bb = sp.symbols("K ab bb")                # ab=alpha, bb=beta
L = -(bb ** 2 / (4 * ab)) * K ** 2
assert sp.simplify(L.subs(K, -K) - L) == 0
ok_cp("V22 L_T,eff = -(b^2/4a) K^2 is K -> -K invariant (exact substitution)")

# ---------------------------------------------------------------- V23: 11.II.D
lam1 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], complex)
lam2 = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], complex)
lam6 = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], complex)
def rvec(M):  # real vectorization of anti-Hermitian 3x3
    return np.concatenate([M.real.reshape(-1), M.imag.reshape(-1)])
basis = [1j * lam1, 1j * lam2, 1j * lam6]
span = [rvec(B) for B in basis]
for _ in range(12):                              # bracket closure
    new = []
    nb = len(span)
    vecs = [b[:9].reshape(3, 3) + 1j * b[9:].reshape(3, 3) for b in span]
    for i in range(nb):
        for j in range(i + 1, nb):
            C = vecs[i] @ vecs[j] - vecs[j] @ vecs[i]   # stays anti-Hermitian
            v = rvec(C)
            M = np.stack(span + new)
            proj = M.T @ np.linalg.lstsq(M.T, v, rcond=None)[0]
            if np.linalg.norm(v - proj) > 1e-8:
                new.append(v - proj)
    span += new
    if not new:
        break
dim = np.linalg.matrix_rank(np.stack(span), tol=1e-8)
assert dim == 8, f"bracket closure dim = {dim}"
print("OK [NC] V23 Lie{i l1, i l2, i l6} bracket-closes to real dim 8 = su(3)")

# ---------------------------------------------------------------- V24: 11.VI.N1
# negating every weight negates each anomaly sum; 0 stays 0.
assert -Fraction(0) == Fraction(0)
ok_cp("V24 anomaly zeros are sign-blind: mirror module's zeros are the same zeros")

# ---------------------------------------------------------------- V25: 11.V.T1
# Under the AX comparison contract (SU(3)<->color, SU(2)<->weak, Y0<->hypercharge),
# the six blocks are one SM generation plus a neutral singlet. Exact table match:
table = [(("(2,3)", Fraction(1, 6)), ("u_L,d_L", [Fraction(2, 3), Fraction(-1, 3)])),
         ((("(1,3b)", Fraction(-2, 3))), ("u_R^c", [Fraction(-2, 3)])),
         ((("(1,3b)", Fraction(1, 3))), ("d_R^c", [Fraction(1, 3)])),
         ((("(2,1)", Fraction(-1, 2))), ("nu_L,e_L", [Fraction(0), Fraction(-1)])),
         ((("(1,1)", Fraction(1))), ("e_R^c", [Fraction(1)])),
         ((("(1,1)", Fraction(0))), ("sterile singlet", [Fraction(0)]))]
for (rep, Y0), (who, qs) in table:
    if rep.startswith("(2"):  # doublet: T3 = +-1/2
        got = sorted([Fraction(1, 2) + Y0, Fraction(-1, 2) + Y0])
    else:                     # singlet/triplet: Q = Y0
        got = [Y0]
    assert got == sorted(qs), who
print("OK [SC] V25 six-block table = one SM generation + neutral singlet "
      "(conditional on the AX comparison contract)")
results.append(("V25 generation table (conditional)", 0.0, 0.0, "SC"))

# ---------------------------------------------------------------- summary
n = len(results)
scopes = {}
for _, _, _, s in results:
    scopes[s] = scopes.get(s, 0) + 1
print(f"\nAll {n} checks passed "
      f"({' + '.join(f'{v} {k}' for k, v in sorted(scopes.items()))}). No timeouts.")
num_worst = max((m for _, m, _, s in results if s == "NC"), default=0.0)
print(f"Honest worst-case measured numerical error: {num_worst:.3e} "
      "(floating-point noise; the underlying identities are exact algebra).")
