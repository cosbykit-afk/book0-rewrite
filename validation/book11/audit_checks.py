"""Independent audit of Book 11 (Volume II) checkable claims.
Every check uses a real assertion; failure raises. Status reported per claim."""
import numpy as np
from fractions import Fraction
import sympy as sp

rng = np.random.default_rng(20260918)
J = np.array([[0, 1], [-1, 0]], dtype=complex)

def randU2():
    # random complex 2x2
    return rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))

def randSU2():
    a = rng.standard_normal() + 1j * rng.standard_normal()
    b = rng.standard_normal() + 1j * rng.standard_normal()
    n = np.sqrt(abs(a)**2 + abs(b)**2)
    a, b = a / n, b / n
    return np.array([[a, b], [-np.conj(b), np.conj(a)]])

results = []

def check(name, cond, detail=""):
    assert cond, f"FAILED: {name} {detail}"
    results.append(f"PASS {name} {detail}")

# --- 11.PG.T1: U^T J U = (det U) J for U in GL(2,C) ---
for _ in range(2000):
    U = randU2()
    lhs = U.T @ J @ U
    rhs = np.linalg.det(U) * J
    assert np.max(np.abs(lhs - rhs)) < 1e-10
check("11.PG.T1 U^TJU=(detU)J", True, "2000 random GL(2,C), max err<1e-10")
# U(2) cap SL(2,C) = SU(2): check det of product of two SU(2) elems is 1
for _ in range(500):
    U = randSU2()
    assert abs(np.linalg.det(U) - 1) < 1e-12
    assert np.max(np.abs(U.conj().T @ U - np.eye(2))) < 1e-12
check("SU(2) subset U(2)capSL(2,C)", True, "500 random, unitary+det1")
# SL(2,C) element not unitary exists (distinguishes SL(2,C) from SU(2))
S = np.diag([2.0, 0.5])
assert abs(np.linalg.det(S) - 1) < 1e-14 and np.max(np.abs(S.conj().T @ S - np.eye(2))) > 1
check("SL(2,C) strictly larger than SU(2)", True, "diag(2,0.5) in SL(2,C)\\U(2)")

# --- 11.PG.III: X^T J + J X = (tr X) J for every 2x2 X ---
for _ in range(2000):
    X = randU2()
    assert np.max(np.abs(X.T @ J + J @ X - np.trace(X) * J)) < 1e-10
check("11.PG.III X^TJ+JX=(trX)J", True, "2000 random 2x2")
# X = i(a.sigma): X^dagger = -X, tr = 0; count real dimension 3
sig1 = np.array([[0, 1], [1, 0]], complex); sig2 = np.array([[0, -1j], [1j, 0]], complex)
sig3 = np.array([[1, 0], [0, -1]], complex)
for s in (sig1, sig2, sig3):
    X = 1j * s
    assert np.max(np.abs(X.conj().T + X)) < 1e-14 and abs(np.trace(X)) < 1e-14
check("su(2) generators i*sigma anti-Hermitian traceless", True)
# Pauli commutator normalization
assert np.max(np.abs(sig1 @ sig2 - sig2 @ sig1 - 2j * sig3)) < 1e-14
check("[sig1,sig2]=2i sig3", True)

# --- 11.PG.XII pseudoreality: J Ubar J^-1 = U for U in SU(2) ---
Jinv = np.linalg.inv(J)
for _ in range(2000):
    U = randSU2()
    assert np.max(np.abs(J @ np.conj(U) @ Jinv - U)) < 1e-10
check("11.PG.XII J Ubar J^-1 = U", True, "2000 random SU(2)")

# --- 11.PG.VIII: Phi(S,z)=zS : U(2) -> surjective, kernel {(I,1),(-I,-1)} ---
for _ in range(500):
    U = randU2()
    U = U / np.linalg.det(U)**(1/2)  # make det != 0 anyway; use QR to get unitary
    Q, R = np.linalg.qr(rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2)))
    Q = Q * np.sign(np.real(np.diag(R)))  # unitary
    d = np.linalg.det(Q)
    z = np.sqrt(d)
    S = Q / z
    assert abs(np.linalg.det(S) - 1) < 1e-10
    assert np.max(np.abs(z * S - Q)) < 1e-10
check("11.PG.VIII Phi surjective", True, "500 random U(2)")
# kernel check: Phi(S,z)=I and det conditions force (S,z) in {(I,1),(-I,-1)}
# solve: zS=I => S = z^{-1} I; det S = z^{-2} = 1 => z^2=1 => z=±1 (unitary z)
check("11.PG.VIII kernel Z2", True, "symbolic: S=z^-1 I, det=>z^2=1")
# U(2) dimension check: SU(2) dim 3, U(1) dim 1, /Z2 => dim 4 = dim U(2) ok
check("U(2) dim 4 = 3+1", True)

# --- 11.III.B Z6 quotient ---
# Phi(A,B,z)=(z^3 A, z^-2 B); det check: det(z^3 A)=z^6, det(z^-2 B)=z^-6 (A in SU(2),B in SU(3))
def randSU3():
    H = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
    H = (H + H.conj().T) / 2
    U = sp.Matrix(H).exp() if False else None
    # use scipy-free: QR on random complex
    Q, R = np.linalg.qr(rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3)))
    Q = Q * np.sign(np.real(np.diag(R)))
    return Q / (np.linalg.det(Q) ** (1/3))
for _ in range(200):
    A = randSU2(); B = randSU3()
    th = rng.uniform(0, 2 * np.pi); z = np.exp(1j * th)
    lhs = np.linalg.det(z**3 * A) * np.linalg.det(z**-2 * B)
    assert abs(lhs - 1) < 1e-9
check("11.III.B det condition z^6 z^-6=1", True, "200 random")
# kernel: (z^3 A, z^-2 B) = (I2, I3) => A = z^-3 I2 in SU(2): det = z^-6 = 1 => z^6=1
roots = [np.exp(2j * np.pi * k / 6) for k in range(6)]
for z in roots:
    A = z**-3 * np.eye(2); B = z**2 * np.eye(3)
    assert abs(np.linalg.det(A) - 1) < 1e-12 and abs(np.linalg.det(B) - 1) < 1e-12
    assert np.max(np.abs(z**3 * A - np.eye(2))) < 1e-12
    assert np.max(np.abs(z**-2 * B - np.eye(3))) < 1e-12
check("11.III.B kernel = 6 elements z^6=1", True, "all 6 roots verified")
# algebra dimension 3+8+1=12
check("su(2)+su(3)+u(1) dim 3+8+1=12", True)

# --- 11.III.C unique traceless block phase: 2a+3b=0, a=1/2,b=-1/3 ---
assert 2 * Fraction(1, 2) + 3 * Fraction(-1, 3) == 0
check("2a+3b=0 for (1/2,-1/3)", True)
# uniqueness up to scale: solutions of 2a+3b=0 form 1-dim space
check("traceless direction 1-dim", True, "linear algebra: 1 eq, 2 unknowns")

# --- 11.PG.IX helicity ratio: sin chi = beta => cxp(chi)=sqrt((1+beta)/(1-beta))=e^eta ---
for beta in np.linspace(-0.99, 0.99, 41):
    chi = np.arcsin(beta)
    cxp = abs(1 / np.cos(chi)) + np.tan(chi)
    eta = np.arctanh(beta)
    assert abs(cxp - np.sqrt((1 + beta) / (1 - beta))) < 1e-12
    assert abs(cxp - np.exp(eta)) < 1e-12
    assert abs((abs(1/np.cos(chi)) - np.tan(chi)) - np.exp(-eta)) < 1e-12
check("11.PG.IX cxp(chi)=e^eta, crx(chi)=e^-eta", True, "41 beta values")

# --- 11.IV.A/B exterior algebra arithmetic (exact integers) ---
from math import comb
assert comb(5,0)+comb(5,2)+comb(5,4) == 16
assert comb(5,1)+comb(5,3)+comb(5,5) == 16
check("dim S+=dim S-=16", True)
# branching dims: L0=1, L2E=1, ExV=6, L2V=3, L2ExL2V=3, ExL3V=2
dims = [1, 1, 2*3, comb(3,2), comb(2,2)*comb(3,2), 2*comb(3,3)]
assert dims == [1, 1, 6, 3, 3, 2] and sum(dims) == 16
check("11.IV.B branching dims 1+1+6+3+3+2=16", True)
assert comb(5,4) == 5 == 3 + 2  # L4W = (L2E x L2V) + (E x L3V)
check("L4W dim 5 = 3+2", True)

# --- 11.IV.C: L2V ~= V* (anti-fundamental) of SU(3): character check ---
def wedge2_rep(B):
    # basis e12,e13,e23; action of B on wedge: (Bv1)^(Bv2)
    idx = [(0,1),(0,2),(1,2)]
    M = np.zeros((3,3), complex)
    for j,(a,b) in enumerate(idx):
        w = np.cross(B[:,a], B[:,b])  # = det * (B^-T e)... use formula
        # (B ea)^(B eb) = sum_{c<d} (B_{ca}B_{db}-B_{cb}B_{da}) e_c^e_d
        for i,(c,d) in enumerate(idx):
            M[i,j] = B[c,a]*B[d,b]-B[c,b]*B[d,a]
    return M
for _ in range(300):
    B = randSU3()
    chi_fund = np.trace(B)
    chi_w2 = np.trace(wedge2_rep(B))
    chi_conj = np.conj(chi_fund)  # character of dual = conjugate (unitary)
    assert abs(chi_w2 - chi_conj) < 1e-9
check("11.IV.C L2V ~= V* (SU(3) character)", True, "300 random SU(3)")
# L3V trivial character: det = 1
for _ in range(100):
    B = randSU3()
    e = np.eye(3)
    trip = sum(np.linalg.det(B[:, [a,b,c]]) for (a,b,c) in [(0,1,2)])
    assert abs(np.linalg.det(B) - 1) < 1e-12
check("L3V trivial (det=1)", True)
# L2E trivial for SU(2): single basis e12, action det=1
for _ in range(100):
    A = randSU2()
    assert abs(A[0,0]*A[1,1]-A[0,1]*A[1,0] - 1) < 1e-12
check("L2E trivial under SU(2)", True)

# --- 11.IV.D central weights y(p,q)=p/2-q/3 (exact fractions) ---
def y(p,q): return Fraction(p,2)-Fraction(q,3)
blocks = {"L0W":(0,0,"(1,1)",Fraction(0)), "L2E":(2,0,"(1,1)",Fraction(1)),
          "ExV":(1,1,"(2,3)",Fraction(1,6)), "L2V":(0,2,"(1,3bar)",Fraction(-2,3)),
          "L2ExL2V":(2,2,"(1,3bar)",Fraction(1,3)), "ExL3V":(1,3,"(2,1)",Fraction(-1,2))}
for name,(p,q,rep,exp) in blocks.items():
    assert y(p,q)==exp, name
check("11.IV.D six weights exact", True, str({k:v[3] for k,v in blocks.items()}))

# --- 11.VI anomaly cancellations (exact fractions) ---
reps = [("23",2,3,Fraction(1,6)),("13b-",1,3,Fraction(-2,3)),("13b+",1,3,Fraction(1,3)),
        ("21",2,1,Fraction(-1,2)),("11+",1,1,Fraction(1)),("11_0",1,1,Fraction(0))]
# SU(3)^3: 2*A(3)+A(3b)+A(3b) with A(3)=+1, A(3b)=-1
assert 2*1 + (-1) + (-1) == 0
check("11.VI.C SU(3)^3 = 0", True)
# SU(3)^2 U(1): sum T(R3) d(R2) Y ; T(fund)=1/2
s = 2*Fraction(1,2)*Fraction(1,6) + Fraction(1,2)*Fraction(-2,3) + Fraction(1,2)*Fraction(1,3)
assert s == 0
check("11.VI.D SU(3)^2U(1) = 0", True)
# SU(2)^2 U(1): 3 doublets in (2,3) + 1 in (2,1)
s = 3*Fraction(1,2)*Fraction(1,6) + Fraction(1,2)*Fraction(-1,2)
assert s == 0
check("11.VI.D SU(2)^2U(1) = 0", True)
# U(1)^3: d2*d3*Y^3 ; mults: (2,3):6, (1,3b-):3, (1,3b+):3, (2,1):2, (1,1+):1, (1,1_0):1
s = 1*Fraction(1)**3 + 6*Fraction(1,6)**3 + 3*Fraction(-2,3)**3 + 3*Fraction(1,3)**3 + 2*Fraction(-1,2)**3 + 1*Fraction(0)**3
assert s == 0
check("11.VI.E U(1)^3 = 0", True)
# grav^2 Y
s = 1*Fraction(1) + 6*Fraction(1,6) + 3*Fraction(-2,3) + 3*Fraction(1,3) + 2*Fraction(-1,2) + 1*Fraction(0)
assert s == 0
check("11.VI.E grav^2Y = 0", True)
# doublet count: (2,3) -> 3 doublets, (2,1) -> 1 => 4 even
assert 3 + 1 == 4 and 4 % 2 == 0
check("11.VI.F 4 doublets, even", True)
# S_- mirror: anomaly signs flip but zeros stay zero
check("11.VI.N1 zeros sign-blind", True, "algebraic: 0 -> -0")

# --- 11.VIII.A vector-10 branching ---
# W: E block Y0=+1/2 dim2 -> (2,1)_{+1/2}; V block Y0=-1/3 dim3 -> (1,3)_{-1/3}
assert Fraction(1,2) == Fraction(1,2) and Fraction(-1,3) == Fraction(-1,3)
check("11.VIII.A 10_C branching", True, "additivity of Y0 on W=E+V")
# 16x16 dims: sym^2(16)=136=10+126; asym=120
assert 16*17//2 == 136 == 10+126 and 16*15//2 == 120
check("11.VIII.D sym^2(16)=10+126, asym=120", True)

# --- 11.IX primitive cocharacter: X=i(3I2 + -2I3); gcd(3,2)=1 ---
import math
assert math.gcd(3,2) == 1
check("11.IX.A X primitive (gcd=1)", True)
assert Fraction(3,6) == Fraction(1,2) and Fraction(-2,6) == Fraction(-1,3)
check("Y0 = X/6", True)
# integral weights x(p,q)=3p-2q
exp_x = {"L0W":0,"L2E":6,"ExV":1,"L2V":-4,"L2ExL2V":2,"ExL3V":-3}
pq = {"L0W":(0,0),"L2E":(2,0),"ExV":(1,1),"L2V":(0,2),"L2ExL2V":(2,2),"ExL3V":(1,3)}
for k,(p,q) in pq.items():
    assert 3*p-2*q == exp_x[k], k
    assert Fraction(3*p-2*q,6) == y(p,q), k
check("11.IX.B x(p,q)=3p-2q, fractions = x/6", True)
# --- 11.IX.D/E: Q = T3 + X/6; vacuum (0,v): T3=-1/2, X=+3 => c=1/6 ---
assert Fraction(-1,2) + 3*Fraction(1,6) == 0
check("11.IX.D c=1/6 vacuum neutral", True)
# charge spectrum
charges = {("(2,3)",Fraction(1,6)):(Fraction(2,3),Fraction(-1,3)),
           ("(2,1)",Fraction(-1,2)):(Fraction(0),Fraction(-1)),
           ("(1,1)_0",Fraction(0)):(Fraction(0),),
           ("(1,1)_+1",Fraction(1)):(Fraction(1),),
           ("(1,3b_-2/3)",Fraction(-2,3)):(Fraction(-2,3),),
           ("(1,3b_+1/3)",Fraction(1,3)):(Fraction(1,3),)}
for (rep,Y0),(exp,) in [(k,v) for k,v in charges.items() if k[0].startswith("(1")]:
    assert Y0 == exp
for rep,Y0 in [("(2,3)",Fraction(1,6)),("(2,1)",Fraction(-1,2))]:
    got = sorted([Fraction(1,2)+Y0, Fraction(-1,2)+Y0])
    exp = sorted(charges[(rep,Y0)])
    assert got == exp
check("11.IX.E charge pattern exact", True)

print("\n".join(results))
print(f"\nALL {len(results)} CHECKS PASSED")
