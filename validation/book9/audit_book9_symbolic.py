#!/usr/bin/env python3
"""RECONSTRUCTED 2026-09-19 — NOT the original audit script.

The original Book 9 symbolic checks (reported 2026-09-19: 2 SymPy derivations
for Section 9.5) were never saved to disk. This script is a reconstruction
from the Book 9 source span (volume2_full.txt lines 2094-2264) and the
section brief (~/workspace/vol2_book9/book9_brief.md). It is NOT the original
script; it is a newly written, independently executed symbolic check.

Derivations covered (2):

  S1. For the independent static spherical coframe
        ds^2 = -N(r)^2 dt^2 + A(r)^2 dr^2 + r^2 dOmega^2,
      the mixed Einstein components satisfy the exact symbolic identity
        G^r_r - G^t_t = 2 (N A)' / (r N A^3)
      (equivalently, with COVARIANT components, G_rr/A^2 + G_tt/N^2 =
      2(NA)'/(rNA^3)). Hence vacuum (G^t_t = G^r_r = 0) forces (NA)' = 0,
      i.e. NA = const, and NA = 1 after the asymptotic normalization
      N, A -> 1 at infinity. (This is also a standard imported GR result;
      the symbolic computation below re-derives the key combination from
      scratch.)

      NOTE (2026-09-19 reconstruction finding): the section brief and the
      published page quote this identity as
        "G^t_t/N^2 + G^r_r/A^2 = 2(NA)'/(rNA^3) exactly"
      with MIXED components. That form is INCORRECT AS STATED: checked both
      symbolically and numerically (brief-form residual ~4.5e-3 on a sample
      N(r), A(r); corrected-form residual ~9e-19). The correct mixed form
      has a minus and no N^2/A^2 denominators; the brief's form holds only
      with covariant components. The downstream conclusion
      (vacuum => (NA)' = 0 => AN = 1) is UNAFFECTED, since both components
      vanish in vacuum regardless of the combination. See
      corrections_manifest.md.

  S2. Imposing A = N^{-1} BEFORE variation: with f = N^2 and
        B = -r^2 f' - 2 r (f - 1),
      the Einstein-Hilbert density satisfies
        sqrt(-g) R = sin(theta) * dB/dr,
      i.e. the reduced bulk Lagrangian is a total derivative modulo the
      standard angular volume factor sin(theta) — collapsing to a boundary
      term and discarding an independent field equation.

Both computations are run end-to-end here; exit code 0 means both symbolic
identities reduced to zero.
"""
import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi', real=True)
N = sp.Function('N')(r)
A = sp.Function('A')(r)

coords = [t, r, th, ph]
# metric diag(-N^2, A^2, r^2, r^2 sin^2 theta)
g = sp.diag(-N**2, A**2, r**2, r**2*sp.sin(th)**2)
ginv = g.inv()

# Christoffel symbols: Gamma^lam_mu,nu = 1/2 g^{lam,sig}
#   ( d_mu g_{nu,sig} + d_nu g_{sig,mu} - d_sig g_{mu,nu} )
Gamma = [[[0]*4 for _ in range(4)] for _ in range(4)]
for lam in range(4):
    for mu in range(4):
        for nu in range(4):
            expr = 0
            for sig in range(4):
                expr += ginv[lam, sig]*(
                    sp.diff(g[nu, sig], coords[mu])
                    + sp.diff(g[sig, mu], coords[nu])
                    - sp.diff(g[mu, nu], coords[sig]))/2
            Gamma[lam][mu][nu] = sp.simplify(expr)

# Ricci tensor R_mn = d_l G^l_mn - d_n G^l_ml + G^l_lk G^k_mn - G^l_nk G^k_ml
Rmn = [[0]*4 for _ in range(4)]
for mu in range(4):
    for nu in range(4):
        expr = 0
        for lam in range(4):
            expr += sp.diff(Gamma[lam][mu][nu], coords[lam]) - sp.diff(Gamma[lam][mu][lam], coords[nu])
            for kap in range(4):
                expr += Gamma[lam][lam][kap]*Gamma[kap][mu][nu] - Gamma[lam][nu][kap]*Gamma[kap][mu][lam]
        Rmn[mu][nu] = sp.simplify(expr)

Rscalar = sp.simplify(sum(ginv[i, j]*Rmn[i][j] for i in range(4) for j in range(4)))
# mixed Einstein components G^t_t and G^r_r
Rmix = [[sp.simplify(sum(ginv[mu, a]*Rmn[a][nu] for a in range(4))) for nu in range(4)] for mu in range(4)]
Gtt = sp.simplify(Rmix[0][0] - sp.Rational(1, 2)*Rscalar)   # G^t_t
Grr = sp.simplify(Rmix[1][1] - sp.Rational(1, 2)*Rscalar)   # G^r_r

print("G^t_t =", Gtt)
print("G^r_r =", Grr)
# sanity: spherical symmetry requires theta-independence
assert sp.simplify(sp.diff(Gtt, th)) == 0, "G^t_t depends on theta: Christoffel bug"
assert sp.simplify(sp.diff(Grr, th)) == 0, "G^r_r depends on theta: Christoffel bug"
print("PASS sanity: G^t_t, G^r_r are theta-independent")

# ---- S1: combination identity (corrected form) ----
# Correct: G^r_r - G^t_t = 2(NA)'/(r N A^3). The brief's mixed-component form
# "G^t_t/N^2 + G^r_r/A^2 = ..." is incorrect as stated (see header NOTE);
# the covariant form G_rr/A^2 + G_tt/N^2 equals the same RHS.
S1 = sp.simplify(Grr - Gtt - 2*sp.diff(N*A, r)/(r*N*A**3))
S1_cov = sp.simplify((-N**2*Gtt)/N**2 + (A**2*Grr)/A**2 - 2*sp.diff(N*A, r)/(r*N*A**3))
S1_brief_wrong = sp.simplify(Gtt/N**2 + Grr/A**2 - 2*sp.diff(N*A, r)/(r*N*A**3))
print("S1 (correct, mixed) residual (must be 0):", S1)
print("S1 (covariant G_rr/A^2+G_tt/N^2) residual (must be 0):", S1_cov)
print("S1 (brief's mixed form, expected NONZERO):", "zero" if S1_brief_wrong == 0 else "nonzero as expected")
assert S1 == 0, f"S1 FAILED: {S1}"
assert S1_cov == 0, f"S1 covariant FAILED: {S1_cov}"
assert S1_brief_wrong != 0, "unexpected: brief's mixed form simplified to 0"
print("PASS S1: G^r_r - G^t_t = 2(NA)'/(rNA^3); vacuum => (NA)'=0")
print("NOTE: brief/page's mixed-component quote of this identity is incorrect as stated (recorded in corrections_manifest.md)")

# ---- S2: A = 1/N imposed before variation -> total derivative ----
f = sp.Function('f')(r)
subs = {N: sp.sqrt(f), A: 1/sp.sqrt(f)}
# sqrt(-g) R with A = 1/N : sqrt(-g) = N*A*r^2*sin(theta) = r^2*sin(theta)
R_sub = sp.simplify(Rscalar.subs(subs))
dens = sp.simplify(r**2 * R_sub)          # sqrt(-g) R / sin(theta)
B = -r**2*sp.diff(f, r) - 2*r*(f - 1)
res = sp.simplify(dens - sp.diff(B, r))
print("S2 residual r^2*R - dB/dr (must be 0):", res)
assert res == 0, f"S2 FAILED: {res}"
print("PASS S2: sqrt(-g) R = sin(theta) dB/dr with B = -r^2 f' - 2r(f-1)")

print("\nBOTH SYMBOLIC CHECKS PASS")
