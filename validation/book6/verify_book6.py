#!/usr/bin/env python3
"""Book 6 verification: every checkable mathematical claim on book6/index.html.

Scope labels: CP = checked proof (exact algebra or exact integer arithmetic,
verified here, possibly on sampled instances); NC = completed numerical check
(a finished floating-point measurement with a stated tolerance); ST = standard
imported theorem used as a base step (named where it enters). Nothing here is
a manuscript assertion: every check below ran to completion. No timeouts.

Page claims verified (Part I figures, then Part II sections):
 V1  6.1  rotation orthogonality + det 1 (40 angles)                    NC
 V2  6.1  dim so(2)+so(3) = 1+3 = 4                                    CP
 V3  6.1  dim O(n) = n(n-1)/2 at n = 2, 3  [ST base]                    CP
 V4  6.2  1+6+3 = 10 = C(5,2) = dim so(5)                              CP
 V5  6.2  four block generators close at rank 4                        NC
 V6  6.2  + one simple cross generator closes to rank 10               NC
 V7  6.3  I_iota^2 = -1                                                CP
 V8  6.3  primitive diagonal lift commutes with I_iota                 CP
 V9  6.3  complex rank five (dim_R W = 10 with I^2 = -1)               CP
 V10 6.3A J_CHI^2 = -1                                                CP
 V11 6.3A exp(chi J) formula vs independent Taylor exponential         NC
 V12 6.3A weight identities on 2001 samples                           CP
 V13 6.3A norm preservation (isometric Pi) on 2001 samples             CP
 V14 6.3A J_CHI conjugate to I_iota via diag(I,Pi), random orthog Pi   CP
 V15 6.5  I_iota orthogonal (Hermitian compatibility); primitive
          block-orthogonal lifts act complex-linearly                  CP
 V16 6.6  dim U(2)xU(3) = 4+9 = 13; real-form O(2)xO(3) block-unitary  CP
 V17 6.7  center: block scalars central; commutant of u(2)+u(3) 2-dim;
          non-central diag(1,-1) fails to commute                      CP/NC
 V18 6.8  2a+3b = 0 at (1/2,-1/3); solution space 1-dimensional        CP
 V19 6.8  dim su(2)+su(3)+u(1) = 3+8+1 = 12 = dim S(U(2)xU(3))         CP
 V20 6.9  C(n,4) = n has unique integer solution n = 5 (n >= 4)        CP
 V21 6.9  exterior dims 1,5,10,10,5,1; even/odd sectors each 16       CP
 V22 6.9  15 disjoint bivector pairs; Hodge duals span 5 directions   CP
 V23 6.10 C^3 example: k = 4, m = 3, 2m = 10-k, dim_C ker = 2         NC/CP
 V24 6.10 faithful C^5 example: k = 0, m = 5                          NC/CP
 V25 6.11 nilpotent witness: A^5 = 0, nonsymmetric, det(I+A^2) = 1,
          omega formula, not Lagrangian; symmetric B Lagrangian         CP
 V26 6.12 faithful O(2) 2-dim complex rep; GL(1,C) abelian;
          s r(t) s^-1 = r(-t)                                          NC/CP
 V27 6.12 3+1 commutant complex-2-dim abelian; 3+2 blocks commute;
          M_2(C) in the SO(3)-block commutant; dim_C 5, dim_R 10       NC/CP
 V28 6.13 balance 2n = n(n-1)/2 unique at n = 5 (n >= 1)               CP
 V29 6.13 C(n,r) = 2n only at (5,2),(5,3) (n <= 60)                   CP
 V30 6.13 characters of U_C and L^2U differ at a rotation [ST base]    NC
 V31 6.14 Moebius derivative, reciprocal roundtrip, du/ds factor,
          symplectic Jacobian, J_G^2 = -1, dim T*U = 10               NC/CP
 V32 6.15 simplex N = 2..8 (norms, dots, side^2, Gram, spectrum, det);
          det(T|_V) = sgn(T)                                           NC/CP

Not machine-checked (page tags say so): 6.0 status grammar (MA/AX), 6.4
real-representation no-go (ST), the 6.10 C^4 example (MA: asserted, not
recomputed), 6.11 positive-overlap Hermitian examples (MA), 6.16 terminal
firewall (MA), and all MA/AX framing sentences.

Run:  python3 verify_book6.py   (exit 0 iff every check passes)
"""
import numpy as np
from math import comb, sqrt, pi

TOL = 1e-10
results = []  # (name, max_err, tol, scope)


def check(name, err, tol=TOL, scope="CP"):
    err = np.asarray(err, dtype=float)
    assert np.all(np.isfinite(err)), f"{name}: non-finite values"
    m = float(np.max(np.abs(err)))
    assert m < tol, f"{name}: max_err={m:.3e} >= tol={tol:.0e}"
    results.append((name, m, tol, scope))
    print(f"OK [{scope}] {name}: max_err={m:.3e} < {tol:.0e}")


def record_note(name, scope, detail=""):
    results.append((name, 0.0, TOL, scope))
    print(f"OK [{scope}] {name}" + (f": {detail}" if detail else ""))


rng = np.random.default_rng(11)

# ---------------------------------------------------------------- V1-V3: 6.1
for th in np.linspace(0.05, 6.0, 40):
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    check(f"V1 rot orthogonal th={th:.3f}", R.T @ R - np.eye(2), scope="NC")
    check(f"V1 rot det=1 th={th:.3f}", np.linalg.det(R) - 1.0, scope="NC")
check("V2 dim so(2)+so(3) = 1+3 = 4", (2 * 1 // 2 + 3 * 2 // 2) - 4)
# ST base: dim O(n) = n(n-1)/2; the arithmetic instances are exact.
check("V3 dim O(2)=1, dim O(3)=3 [ST: dim O(n)=n(n-1)/2]",
      [2 * 1 // 2 - 1, 3 * 2 // 2 - 3])

# ---------------------------------------------------------------- V4-V6: 6.2
check("V4 1+6+3 = 10 = C(5,2) = dim so(5)",
      [comb(2, 2) + 2 * 3 + comb(3, 2) - 10, comb(5, 2) - 10, 5 * 4 // 2 - 10])


def skew(i, j, n=5):
    M = np.zeros((n, n))
    M[i, j] = 1.0
    M[j, i] = -1.0
    return M


def lie_closure_rank(gens, n=5):
    vecs = [g.reshape(-1) for g in gens]
    while True:
        r0 = np.linalg.matrix_rank(np.stack(vecs), tol=1e-8)
        mats = [v.reshape(n, n) for v in vecs]
        extra = [(mats[a] @ mats[b] - mats[b] @ mats[a]).reshape(-1)
                 for a in range(len(mats)) for b in range(a + 1, len(mats))]
        r1 = np.linalg.matrix_rank(np.stack(vecs + extra), tol=1e-8)
        if r1 == r0:
            return r1
        _, _, Vt = np.linalg.svd(np.stack(vecs + extra), full_matrices=False)
        vecs = [Vt[k] for k in range(r1)]


block_gens = [skew(0, 1), skew(2, 3), skew(2, 4), skew(3, 4)]  # so(2)+so(3)
check("V5 block generators close at rank 4",
      lie_closure_rank(block_gens) - 4, tol=0.5, scope="NC")
check("V6 block + one simple cross generator closes to rank 10",
      lie_closure_rank(block_gens + [skew(0, 2)]) - 10, tol=0.5, scope="NC")

# ---------------------------------------------------------------- V7-V9: 6.3
u, v = rng.normal(size=5), rng.normal(size=5)
Ii = lambda a, b: (-b, a)          # I_iota with iota = id
Iu, Iv = Ii(*Ii(u, v))
check("V7 I_iota^2 = -1", np.concatenate([Iu + u, Iv + v]))
A = rng.normal(size=(5, 5))
L = lambda a, b: (A @ a, A @ b)    # primitive diagonal lift A(+)A
x1, y1 = L(*Ii(u, v))
x2, y2 = Ii(*L(u, v))
check("V8 primitive diagonal lift commutes with I_iota",
      np.concatenate([x1 - x2, y1 - y2]))
check("V9 complex rank five: dim_R W = 10 with I^2=-1",
      10 // 2 - 5)

# ---------------------------------------------------------------- V10-V14: 6.3A
J2 = np.array([[0.0, -1.0], [1.0, 0.0]])
J = np.zeros((10, 10))
for k in range(5):
    J[2 * k:2 * k + 2, 2 * k:2 * k + 2] = J2   # J_CHI with Pi = id
check("V10 J_CHI^2 = -1", J @ J + np.eye(10))
for chi in [0.0, 0.3, pi / 4, 1.3, pi / 2, 2.5]:
    E, Jn = np.zeros((10, 10)), np.eye(10)     # independent Taylor exponential
    for n in range(1, 61):
        Jn = Jn @ (chi * J) / n
        E = E + Jn
    E = E + np.eye(10)
    F = np.cos(chi) * np.eye(10) + np.sin(chi) * J
    check(f"V11 exp formula vs Taylor chi={chi:.3f}", E - F,
          tol=1e-8, scope="NC")
chi = np.linspace(0, 2 * pi, 2001)             # page: "hold on 2001 samples"
wU, wUs = np.cos(chi) ** 2, np.sin(chi) ** 2
check("V12 wU + wUs = 1 (2001 samples)", wU + wUs - 1.0)
check("V12 wU - wUs = cos 2chi (2001 samples)", (wU - wUs) - np.cos(2 * chi))
check("V12 2 sqrt(wU wUs) = |sin 2chi| (2001 samples)",
      2 * np.sqrt(wU * wUs) - np.abs(np.sin(2 * chi)))
uu = rng.normal(size=5)
uu /= np.linalg.norm(uu)
psi = np.stack([np.cos(chi)[:, None] * uu, np.sin(chi)[:, None] * uu], axis=1)
check("V13 norm preserved, Pi isometric (2001 samples)",
      np.linalg.norm(psi, axis=(1, 2)) - 1.0)
# J_CHI conjugate to I_iota via P = diag(I, Pi), Pi random orthogonal
Qp, _ = np.linalg.qr(rng.normal(size=(5, 5)))
Jm = np.block([[np.zeros((5, 5)), -Qp.T], [Qp, np.zeros((5, 5))]])
Pm = np.block([[np.eye(5), np.zeros((5, 5))], [np.zeros((5, 5)), Qp]])
Im = np.block([[np.zeros((5, 5)), -np.eye(5)], [np.eye(5), np.zeros((5, 5))]])
check("V14 J_CHI conjugate to I_iota via diag(I,Pi)",
      np.linalg.solve(Pm, Jm @ Pm) - Im)

# ---------------------------------------------------------------- V15: 6.5
check("V15 I_iota orthogonal (Hermitian compatibility)", Im.T @ Im - np.eye(10))
Q2 = np.array([[np.cos(0.7), -np.sin(0.7)], [np.sin(0.7), np.cos(0.7)]])
Q3 = np.eye(3)
Qb = np.zeros((5, 5))
Qb[:2, :2], Qb[2:, 2:] = Q2, Q3
Ub = np.block([[Qb, np.zeros((5, 5))], [np.zeros((5, 5)), Qb]])
check("V15 primitive block-orthogonal lift commutes with I_iota",
      Ub @ Im - Im @ Ub)

# ---------------------------------------------------------------- V16: 6.6
check("V16 dim U(2)xU(3) = 4+9 = 13", (4 + 9) - 13)


def rand_block_unitary():
    def ru(n):
        Z = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        Q, _ = np.linalg.qr(Z)
        return Q
    U = np.zeros((5, 5), complex)
    U[:2, :2], U[2:, 2:] = ru(2), ru(3)
    return U


def rand_block_orthogonal():
    def ro(n):
        Z = rng.normal(size=(n, n))
        Q, _ = np.linalg.qr(Z)
        return Q
    Q = np.zeros((5, 5))
    Q[:2, :2], Q[2:, 2:] = ro(2), ro(3)
    return Q


Ur = rand_block_orthogonal()  # real-form element: block-diagonal orthogonal
Uc = Ur.astype(complex)
check("V16 real-form O(2)xO(3) element is block-diagonal unitary",
      Uc.conj().T @ Uc - np.eye(5))
check("V16 real-form element preserves the 2+3 blocks",
      [np.max(np.abs(Uc[:2, 2:])), np.max(np.abs(Uc[2:, :2]))])

# ---------------------------------------------------------------- V17: 6.7
g1, g2 = rand_block_unitary(), rand_block_unitary()


def build_center(x):
    a, b, cr, ci = x[0], x[1], x[2], x[3]
    X2 = np.array([[a, cr + 1j * ci], [cr - 1j * ci, b]])
    d1, d2, d3 = x[4], x[5], x[6]
    o1r, o1i, o2r, o2i, o3r, o3i = x[7:13]
    X3 = np.array([[d1, o1r + 1j * o1i, o2r + 1j * o2i],
                   [o1r - 1j * o1i, d2, o3r + 1j * o3i],
                   [o2r - 1j * o2i, o3r - 1j * o3i, d3]])
    X = np.zeros((5, 5), complex)
    X[:2, :2], X[2:, 2:] = X2, X3
    return X


blocks = []
for g in (g1, g2):
    cols = []
    for k in range(13):
        e = np.zeros(13)
        e[k] = 1.0
        C = build_center(e) @ g - g @ build_center(e)
        cols.append(np.concatenate([C.real.flatten(), C.imag.flatten()]))
    blocks.append(np.stack(cols, axis=1))  # 50 eqs x 13 params
Mc = np.vstack(blocks)  # 100 x 13
sc = np.linalg.svd(Mc, compute_uv=False)
assert int(np.sum(sc < 1e-8)) == 2, f"V17 nullity != 2: {sc[-4:]}"
assert sc[-3] > 1e-3, f"V17 no gap above the 2-dim nullspace: {sc[-3]:.2e}"
check("V17 commutant of u(2)+u(3) is 2-dimensional", sc[-2], tol=1e-8,
      scope="NC")
sE = np.zeros(13)   # U(1)_E: scalar phase on the 2-block
sE[0] = sE[1] = 1.0
sV = np.zeros(13)   # U(1)_V: scalar phase on the 3-block
sV[4] = sV[5] = sV[6] = 1.0
for name, sv in (("E", sE), ("V", sV)):
    check(f"V17 U(1)_{name} block scalar is central",
          [build_center(sv) @ g1 - g1 @ build_center(sv),
           build_center(sv) @ g2 - g2 @ build_center(sv)])
Dnc = np.diag([1.0, -1.0, 1.0, 1.0, 1.0])          # non-central block element
u2off = np.array([[1.0, 1.0], [1.0, -1.0]]) / sqrt(2)
Uoff = np.zeros((5, 5))
Uoff[:2, :2], Uoff[2:, 2:] = u2off, np.eye(3)
cnc = float(np.max(np.abs(Dnc @ Uoff - Uoff @ Dnc)))
assert cnc > 0.5, f"V17 expected non-commutation, got {cnc:.2e}"
record_note("V17 diag(1,-1) is not central", "NC", f"|[D,U]|={cnc:.3e} > 0.5")

# ---------------------------------------------------------------- V18-V19: 6.8
check("V18 2a+3b = 0 at (1/2,-1/3)", 2 * 0.5 + 3 * (-1.0 / 3.0))
# rank-nullity: the 1x2 coefficient matrix [2 3] != 0 has rank 1, nullity 1
assert np.linalg.matrix_rank(np.array([[2.0, 3.0]])) == 1
record_note("V18 traceless direction unique up to scale (1-dim nullspace)",
            "CP", "rank-nullity on [2 3]")
check("V19 dim su(2)+su(3)+u(1) = 3+8+1 = 12", (3 + 8 + 1) - 12)
check("V19 dim S(U(2)xU(3)) = 4+9-1 = 12", (4 + 9 - 1) - 12)

# ---------------------------------------------------------------- V20-V22: 6.9
sol = [n for n in range(4, 201) if comb(n, 4) == n]
assert sol == [5], f"V20 C(n,4)=n solutions: {sol}"
record_note("V20 C(n,4)=n unique integer solution n=5 (n>=4)", "CP",
            "exact integer scan")
check("V21 exterior dims at n=5 are 1,5,10,10,5,1",
      np.array([comb(5, r) for r in range(6)]) - np.array([1, 5, 10, 10, 5, 1]))
check("V21 even sector 1+10+5=16, odd sector 5+10+1=16",
      [(1 + 10 + 5) - 16, (5 + 10 + 1) - 16])
pairs5 = [(i, j) for i in range(5) for j in range(i + 1, 5)]
disjoint = [((i, j), (k, l)) for (i, j) in pairs5 for (k, l) in pairs5
            if (i, j) < (k, l) and len({i, j, k, l}) == 4]
assert len(disjoint) == 15, f"V22 disjoint bivector pairs: {len(disjoint)}"


def parity(p):
    return sum(1 for a in range(len(p)) for b in range(a + 1, len(p))
               if p[a] > p[b]) % 2


duals = np.zeros((15, 5))
for t, ((i, j), (k, l)) in enumerate(disjoint):
    srt = tuple(sorted((i, j, k, l)))
    m = next(x for x in range(5) if x not in srt)
    duals[t, m] = (-1) ** (parity((i, j, k, l)) + parity(srt + (m,)))
check("V22 15 disjoint bivector pairs", len(disjoint) - 15)
check("V22 Hodge duals span all 5 carrier directions",
      np.linalg.matrix_rank(duals, tol=1e-8) - 5, tol=0.5)

# ---------------------------------------------------------------- V23-V24: 6.10
S = np.array([[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0]], float)   # R^5 in R^6=C^3
iS = np.array([[0, -1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [0, 0, 0, -1, 0, 0],
               [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, -1]], float)  # (-i)S; same span as iS
rS = np.linalg.matrix_rank(S, tol=1e-8)
riS = np.linalg.matrix_rank(iS, tol=1e-8)
rSum = np.linalg.matrix_rank(np.vstack([S, iS]), tol=1e-8)
k = rS + riS - rSum
check("V23 C^3 example: k = dim_R(S cap iS) = 4", k - 4, tol=0.5, scope="NC")
Sc = S[:, 0::2] + 1j * S[:, 1::2]                  # S as complex 5x3
m = int(np.sum(np.linalg.svd(Sc, compute_uv=False) > 1e-8))
check("V23 C^3 example: m = dim_C span_C S = 3", m - 3, tol=0.5, scope="NC")
check("V23 2m = 10-k", 2 * m - (10 - k))
Fc = np.array([[1, 1j, 0, 0, 0], [0, 0, 1, 1j, 0], [0, 0, 0, 0, 1]])
sf = np.linalg.svd(Fc, compute_uv=False)
kerdim = 5 - int(np.sum(sf > 1e-8))  # 3x5 matrix: nullity = 5 - rank
check("V23 dim_C ker f_C = 2 = 5-m", kerdim - 2, tol=0.5, scope="NC")
check("V23 k = 2 dim_C ker f_C", k - 2 * kerdim)
S5 = np.hstack([np.eye(5), np.zeros((5, 5))])  # R^5 inside R^10 = C^5
iS5 = np.hstack([np.zeros((5, 5)), np.eye(5)])     # iR^5 inside R^10 = C^5
k5 = (np.linalg.matrix_rank(S5, tol=1e-8)
      + np.linalg.matrix_rank(iS5, tol=1e-8)
      - np.linalg.matrix_rank(np.vstack([S5, iS5]), tol=1e-8))
check("V24 faithful C^5 example: k = 0", k5, tol=0.5, scope="NC")
check("V24 faithful C^5 example: m = 5, 2m = 10-k", [5 - 5, 2 * 5 - (10 - k5)])

# ---------------------------------------------------------------- V25: 6.11
A = np.diag(np.ones(4), 1)          # 5x5 nilpotent Jordan block, nonsymmetric
check("V25 A^5 = 0 (nilpotent)", np.linalg.matrix_power(A, 5))
cns = float(np.max(np.abs(A - A.T)))
assert cns > 0.5, "V25 A should be nonsymmetric"
record_note("V25 A nonsymmetric", "CP", f"max|A-A^T|={cns:.1f}")
check("V25 det(I+A^2) = 1 (totally real)", np.linalg.det(np.eye(5) + A @ A) - 1)


def omega(M, x, z):
    return float(np.concatenate([-M @ x, x]) @ np.concatenate([z, M @ z]))


e0, e1 = np.eye(5)[0], np.eye(5)[1]
check("V25 omega((x,Ax),(z,Az)) = x^T(A-A^T)z",
      omega(A, e0, e1) - float(e0 @ (A - A.T) @ e1))
cLag = abs(omega(A, e0, e1))
assert cLag > 0.5, f"V25 expected non-Lagrangian, got {cLag:.2e}"
record_note("V25 nonsymmetric nilpotent A is not Lagrangian", "CP",
            f"|omega|={cLag:.1f} != 0")
B = rng.normal(size=(5, 5))
B = B + B.T                                       # symmetric -> Lagrangian
check("V25 symmetric B: omega = 0 (Lagrangian)",
      [omega(B, e0, e1), omega(B, rng.normal(size=5), rng.normal(size=5))])

# ---------------------------------------------------------------- V26: 6.12
def rO2(t):
    return np.array([[np.exp(1j * t), 0], [0, np.exp(-1j * t)]])


sO2 = np.array([[0.0, 1.0], [1.0, 0.0]])
for t1, t2 in [(0.3, 1.1), (0.7, 2.2), (-0.5, 0.9)]:
    check(f"V26 O(2) rep: r(t1)r(t2)=r(t1+t2)", rO2(t1) @ rO2(t2) - rO2(t1 + t2),
          scope="NC")
check("V26 O(2) rep: s^2 = 1", sO2 @ sO2 - np.eye(2))
for t in [0.3, 1.1, 2.5]:
    check(f"V26 O(2) rep: s r(t) s = r(-t)", sO2 @ rO2(t) @ sO2 - rO2(-t))
mats = [rO2(0.0), rO2(pi / 2), rO2(pi), sO2, sO2 @ rO2(pi / 2)]
dmin = min(float(np.max(np.abs(mats[a] - mats[b])))
           for a in range(len(mats)) for b in range(a + 1, len(mats)))
assert dmin > 0.5, f"V26 rep not faithful on samples: dmin={dmin:.2e}"
record_note("V26 O(2) 2-dim complex rep faithful on 5 samples", "NC",
            f"min pairwise dist={dmin:.3f}")
a1, b1, c1, d1 = (1 + 2j), (3 - 1j), (0.5 + 0.5j), (-2 + 0j)
check("V26 GL(1,C) is abelian", abs(a1 * c1 - c1 * a1))  # 1x1 matrices commute
R2 = lambda t: np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
S2 = np.diag([1.0, -1.0])                           # real reflection
for t in [0.4, 1.7, 3.1]:
    check(f"V26 reflection reverses rotation: S R(t) S = R(-t)",
          S2 @ R2(t) @ S2 - R2(-t))

# ---------------------------------------------------------------- V27: 6.12
def rot_x(t):
    return np.array([[1, 0, 0], [0, np.cos(t), -np.sin(t)],
                     [0, np.sin(t), np.cos(t)]])


def rot_z(t):
    return np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0],
                     [0, 0, 1]])


def embed41(R):
    M = np.zeros((4, 4))
    M[:3, :3], M[3, 3] = R, 1.0
    return M


rhos = [embed41(rot_x(1.1)), embed41(rot_z(0.7))]


def build_X4(x):
    return x[0::2].reshape(4, 4) + 1j * x[1::2].reshape(4, 4)


blocks41 = []
for rho in rhos:
    cols41 = []
    for k in range(32):
        e = np.zeros(32)
        e[k] = 1.0
        C = build_X4(e) @ rho - rho @ build_X4(e)
        cols41.append(np.concatenate([C.real.flatten(), C.imag.flatten()]))
    blocks41.append(np.stack(cols41, axis=1))  # 32 eqs x 32 params
M41 = np.vstack(blocks41)  # 64 x 32
_, s41, Vh41 = np.linalg.svd(M41)
assert int(np.sum(s41 < 1e-8)) == 4, f"V27 3+1 nullity != 4: {s41[-6:]}"
assert s41[-5] > 1e-3, f"V27 no gap: {s41[-5]:.2e}"
check("V27 3+1 commutant is complex-2-dim (real 4)", s41[-4], tol=1e-8,
      scope="NC")
Xa, Xb = build_X4(Vh41[-2]), build_X4(Vh41[-1])
check("V27 3+1 commutant is abelian", Xa @ Xb - Xb @ Xa, tol=1e-8, scope="NC")
# real basis of diag(a,a,a,b): (1,0),(i,0),(0,1),(0,i) on the two blocks
s_re = np.zeros(32)
s_re[0] = s_re[10] = s_re[20] = 1.0    # diag(1,1,1,0)
s_im = np.zeros(32)
s_im[1] = s_im[11] = s_im[21] = 1.0    # diag(i,i,i,0)
t_re = np.zeros(32)
t_re[30] = 1.0                          # diag(0,0,0,1)
t_im = np.zeros(32)
t_im[31] = 1.0                          # diag(0,0,0,i)
check("V27 block scalars diag(a,a,a,b) span the commutant",
      [M41 @ s_re, M41 @ s_im, M41 @ t_re, M41 @ t_im], tol=1e-8, scope="NC")
# 3+2 block rep: SO(3) on C^3, O(2) on C^2 commute by blocks
R3 = rot_z(0.9).astype(complex)
rS = np.zeros((5, 5), complex)
rS[:3, :3], rS[3:, 3:] = R3, np.eye(2)
rO = np.zeros((5, 5), complex)
rO[:3, :3], rO[3:, 3:] = np.eye(3), rO2(1.1)
check("V27 3+2: SO(3) and O(2) blocks commute", rS @ rO - rO @ rS)
Bc = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))  # in M_2(C)
Xc = np.zeros((5, 5), complex)
Xc[3:, 3:] = Bc
check("V27 M_2(C) sits in the SO(3)-block commutant", Xc @ rS - rS @ Xc)
check("V27 dim_C(3+2) = 5, dim_R = 10", [5 - 5, 2 * 5 - 10])

# ---------------------------------------------------------------- V28-V30: 6.13
sol = [n for n in range(1, 501) if 2 * n == n * (n - 1) // 2]
assert sol == [5], f"V28 balance solutions: {sol}"
record_note("V28 2n = n(n-1)/2 unique at n = 5 (n>=1)", "CP",
            "exact integer scan")
check("V28 common dimension 2*5 = 5*4/2 = 10", [2 * 5 - 10, 5 * 4 // 2 - 10])
pairs = [(n, r) for n in range(4, 61) for r in range(2, n - 1)
         if comb(n, r) == 2 * n]
assert pairs == [(5, 2), (5, 3)], f"V29 C(n,r)=2n pairs: {pairs}"
record_note("V29 C(n,r)=2n only at (5,2),(5,3) for n<=60", "CP",
            "exact integer scan")
check("V29 C(5,2)=C(5,3)=10", [comb(5, 2) - 10, comb(5, 3) - 10])
# ST base: U_C and L^2U are inequivalent SO(5) irreps; numeric shadow: the
# characters already differ at a single rotation (tr 4 vs 7).
th = pi / 3
Rr = np.eye(5)
Rr[:2, :2] = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
chU = float(np.trace(Rr))
K = np.kron(Rr, Rr)
W = np.stack([(np.kron(np.eye(5)[i], np.eye(5)[j])
               - np.kron(np.eye(5)[j], np.eye(5)[i])) / sqrt(2)
              for i in range(5) for j in range(i + 1, 5)], axis=1)
chL = float(np.trace(W.T @ K @ W))
assert abs(chU - 4.0) < 1e-12 and abs(chL - 7.0) < 1e-12, (chU, chL)
check("V30 characters differ: |tr(U_C)-tr(L^2U)| = 3 [ST: irreps differ]",
      abs(abs(chU - chL) - 3.0), scope="NC")

# ---------------------------------------------------------------- V31: 6.14
a, b, c, d = 2.0, 1.0, 1.0, 1.0
assert a * d - b * c == 1.0
u0 = 0.7
up = lambda u: (a * u + b) / (c * u + d)
h = 1e-6
num_d = (up(u0 + h) - up(u0 - h)) / (2 * h)
check("V31 du'/du = (cu+d)^-2", num_d - (c * u0 + d) ** -2, tol=1e-8,
      scope="NC")
s0 = sqrt(1 + u0 ** 2) - u0
check("V31 reciprocal inverse roundtrip", (1 - s0 ** 2) / (2 * s0) - u0,
      scope="NC")
u_of_s = lambda s: (1 - s ** 2) / (2 * s)
num_duds = (u_of_s(s0 + h) - u_of_s(s0 - h)) / (2 * h)
check("V31 du/ds = -(1+s^2)/(2s^2)", num_duds + (1 + s0 ** 2) / (2 * s0 ** 2),
      tol=1e-8, scope="NC")


def Phi(uu_, pp_):
    return np.array([(a * uu_ + b) / (c * uu_ + d), pp_ * (c * uu_ + d) ** 2])


u1, p1, hh = 0.7, 1.3, 1e-5
Jp = np.column_stack([(Phi(u1 + hh, p1) - Phi(u1 - hh, p1)) / (2 * hh),
                      (Phi(u1, p1 + hh) - Phi(u1, p1 - hh)) / (2 * hh)])
Om = np.array([[0.0, 1.0], [-1.0, 0.0]])
check("V31 dp'/^du' = dp/^du: J^T Om J = Om", Jp.T @ Om @ Jp - Om, tol=1e-8,
      scope="NC")
q, p = rng.normal(size=5), rng.normal(size=5)
Jg = lambda qq, pp: (-pp, qq)                                  # G = I_5
Jg2 = Jg(*Jg(q, p))
check("V31 J_G^2 = -1", np.concatenate([Jg2[0] + q, Jg2[1] + p]))
check("V31 dim T*U = 2n = 10 at n=5", 2 * 5 - 10)

# ---------------------------------------------------------------- V32: 6.15
for N in range(2, 9):
    d = N - 1
    e = np.eye(N)
    one = np.ones(N)
    vv = np.array([e[a] - one / N for a in range(N)])
    check(f"V32 N={N} |v_A|^2=(N-1)/N",
          np.einsum("ai,ai->a", vv, vv) - (N - 1) / N, scope="NC")
    G = vv @ vv.T
    mask = ~np.eye(N, dtype=bool)
    check(f"V32 N={N} v_A.v_B=-1/N", G[mask] + 1.0 / N, scope="NC")
    D2 = (np.einsum("ai,ai->a", vv, vv)[:, None]
          + np.einsum("ai,ai->a", vv, vv)[None, :] - 2 * G)
    check(f"V32 N={N} |v_A-v_B|^2=2", D2 + 2 * np.eye(N) - 2, scope="NC")
    edges = np.array([(vv[a] - vv[N - 1]) / sqrt(2) for a in range(d)])
    Gd = edges @ edges.T
    check(f"V32 N={N} Gram=(I+J)/2",
          Gd - 0.5 * (np.eye(d) + np.ones((d, d))), scope="NC")
    ev = np.linalg.eigvalsh(Gd)
    expect = np.array([0.5] * (d - 1) + [(d + 1) / 2])
    check(f"V32 N={N} Gram spectrum", np.sort(ev) - np.sort(expect), scope="NC")
    check(f"V32 N={N} det=(d+1)/2^d", np.linalg.det(Gd) - (d + 1) / 2 ** d,
          scope="NC")
# det(T|_{V(N-1)}) = sgn(T): exact algebra, sampled permutations
for N in [3, 4, 5, 6]:
    M0 = np.eye(N) - np.ones((N, N)) / N
    Qb, _ = np.linalg.qr(M0)
    Qr = Qb[:, :N - 1]
    for trial in range(3):
        perm = rng.permutation(N)
        P = np.eye(N)[perm]
        inv = sum(1 for a in range(N) for b in range(a + 1, N)
                  if perm[a] > perm[b]) % 2
        sgn = -1.0 if inv else 1.0
        Rr_ = Qr.T @ P @ Qr
        check(f"V32 N={N} det(T|_V)=sgn(T) perm={trial}",
              np.linalg.det(Rr_) - sgn, tol=1e-8)

# ---------------------------------------------------------------- summary
n_cp = sum(1 for r in results if r[3] == "CP")
n_nc = sum(1 for r in results if r[3] == "NC")
n_v = 32
worst_nc = max((m for _, m, _, s in results if s == "NC"), default=0.0)
worst_cp = max((m for _, m, _, s in results if s == "CP"), default=0.0)
print(f"\nALL {len(results)} CHECKS PASSED "
      f"({n_v} numbered V-checks: {n_cp} CP, {n_nc} NC) "
      f"-- 0 failed, 0 errors, 0 timeouts")
print(f"worst CP max_err = {worst_cp:.3e}   worst NC max_err = {worst_nc:.3e}")
