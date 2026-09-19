#!/usr/bin/env python3
"""Book 10 audit: every checkable mathematical claim, with REAL ASSERTIONS.
Source: /home/hatch/workspace/vol2_book10/source.txt (vol2 lines 2265-2496).
Scope labels assigned per claim; see book10_brief.md for the ledger.
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

rng = np.random.default_rng(20260918)
ALPHA = 1/137.035999084  # fine-structure constant

def sxp(x):
    return np.abs(1/np.sin(x)) - np.cos(x)/np.sin(x)

def srx(x):
    return np.abs(1/np.sin(x)) + np.cos(x)/np.sin(x)

print("=== A. Canonical half-angle identities (used by 10.III.T1, 10.IV.T1) ===")
xs = np.linspace(0.01, np.pi-0.01, 20001)
e1 = np.max(np.abs(sxp(xs) - np.tan(xs/2)))
e2 = np.max(np.abs(srx(xs) - 1/np.tan(xs/2)))
print(f"max|sxp - tan(x/2)| = {e1:.3e}, max|srx - cot(x/2)| = {e2:.3e}")
assert e1 < 1e-12 and e2 < 1e-12, "canonical half-angle identity failed"
print("PASS: sxp(x)=tan(x/2), srx(x)=cot(x/2) on (0,pi)")

print("=== B. Free-Dirac lower/upper ratio identities (10.III.P1 import, checked) ===")
# standard: |chi|/|phi| = pc/(E+mc^2) = sqrt((E-mc^2)/(E+mc^2)); rapidity: = tanh(a/2)
m = 1.0; c = 1.0
E = m*c**2 * (1 + rng.random(500)*5)          # E >= mc^2
p = np.sqrt(E**2 - (m*c**2)**2)/c
r1 = p*c/(E + m*c**2)
r2 = np.sqrt((E - m*c**2)/(E + m*c**2))
a = np.arccosh(E/(m*c**2))
r3 = np.tanh(a/2)
d1 = np.max(np.abs(r1-r2)); d2 = np.max(np.abs(r1-r3))
print(f"max|pc/(E+mc^2)-sqrt((E-mc^2)/(E+mc^2))| = {d1:.3e}")
print(f"max|pc/(E+mc^2)-tanh(a/2)|            = {d2:.3e}")
assert d1 < 1e-14 and d2 < 1e-14
print("PASS: standard free-spinor ratio magnitude identities")

print("=== C. 10.III.T1 bridge: sxp(x)=pc/(E+mc^2) under rapidity contract ===")
# contract: q = tan(x/2) = tanh(a/2); check sxp(x) reproduces the ratio
r = rng.random(300)*3.0 + 1e-3                # sample ratio values
x = 2*np.arctan(r)                            # invert tan(x/2)
assert np.all((x > 0) & (x < np.pi))
e3 = np.max(np.abs(sxp(x) - r))
print(f"max|sxp(2*arctan(r)) - r| = {e3:.3e}")
assert e3 < 1e-14
print("PASS: under the contract, sxp(x) is exactly the spinor ratio magnitude")

print("=== D. 10.II.T1 projective-rank obstruction (rank via SVD) ===")
# psi(x) = (cos(x/2), sin(x/2)) real meridian, phi fixed: image rank 1
# psi(x,phi) = (cos(x/2), cos(phi)sin(x/2), sin(phi)sin(x/2)): rank 2
def jac_rank(f, pt, h=1e-7):
    pt = np.asarray(pt, float); n = len(pt)
    J = np.column_stack([(f(pt+np.eye(n)[i]*h)-f(pt-np.eye(n)[i]*h))/(2*h)
                         for i in range(n)])
    return np.linalg.svd(J, compute_uv=False)
f1 = lambda v: np.array([np.cos(v[0]/2), np.sin(v[0]/2)])
s1 = jac_rank(f1, [1.0]); print("meridian jacobian sing vals:", s1)
assert s1[0] > 0.1 and (len(s1) < 2 or s1[1] < 1e-9), "meridian rank != 1"
f2 = lambda v: np.array([np.cos(v[0]/2), np.cos(v[1])*np.sin(v[0]/2),
                         np.sin(v[1])*np.sin(v[0]/2)])
s2 = jac_rank(f2, [1.0, 0.7]); print("CP1-chart jacobian sing vals:", s2)
assert s2[0] > 0.1 and s2[1] > 0.1 and (len(s2) < 3 or s2[2] < 1e-9), "chart rank != 2"
print("PASS: real meridian has rank 1; (x,phi) chart has rank 2 -> 1 coord cannot cover CP1")

print("=== E. 10.IV.T1 ground-sector: |G/F| constant = sxp(x) (standard formulas) ===")
Z = 1.0; ga = np.sqrt(1-(Z*ALPHA)**2); lam = Z*ALPHA  # hbar=c=m=1, lam=sqrt(1-E^2)=Z*alpha
rr = np.logspace(-3, 3, 4000)
P = np.sqrt(1+ga) * rr**ga * np.exp(-lam*rr)          # F (large)
Q = -np.sqrt(1-ga) * rr**ga * np.exp(-lam*rr)         # G (small)
ratio = np.abs(Q/P)
const = (Z*ALPHA)/(1+ga)                             # = sqrt((1-ga)/(1+ga))
print(f"ratio mean={ratio.mean():.8f}, rel std={ratio.std()/ratio.mean():.3e}")
print(f"expected Z*alpha/(1+gamma) = {const:.8f}")
assert ratio.std()/ratio.mean() < 1e-10, "ground-sector ratio not constant"
assert np.max(np.abs(ratio - const)) < 1e-12
xg = 2*np.arctan(const)
assert 0 < xg < np.pi
assert abs(sxp(xg) - const) < 1e-14
print(f"PASS: |G/F| constant; x=2*arctan(|G/F|)={xg:.6f} rad, sxp(x)=|G/F|")

print("=== F. Radial Dirac ODE validation on ground state (import sanity) ===")
# (hbar=c=m=1) P' = -(k/r)P + (E+1+Z a/r)Q ; Q' = (k/r)Q - (E-1+Z a/r)P
def dirac_rhs(r, y, E, k):
    P_, Q_ = y
    return [-(k/r)*P_ + (E+1+Z*ALPHA/r)*Q_,
            (k/r)*Q_ - (E-1+Z*ALPHA/r)*P_]
def integrate(E, k, r0, rmax, npts=20000):
    P0 = r0**ga; Q0 = r0**ga*(ga-1)/(Z*ALPHA)   # small-r asymptotics (checked: Q/P=(ga-1)/(Za))
    rs = np.geomspace(r0, rmax*(1-1e-9), npts)
    sol = solve_ivp(lambda r, y: dirac_rhs(r, y, E, k), (r0, rmax), [P0, Q0],
                    t_eval=rs, method='LSODA', rtol=1e-10, atol=1e-13)
    assert sol.success, "ODE integration failed"
    return sol.t, sol.y[0], sol.y[1]
rg, Pg_num, Qg_num = integrate(ga, -1, 1e-4, 900.0)
Pg_an = np.sqrt(1+ga)*rg**ga*np.exp(-lam*rg)
Qg_an = -np.sqrt(1-ga)*rg**ga*np.exp(-lam*rg)
s = Pg_num[np.argmax(np.abs(Pg_num))]/Pg_an[np.argmax(np.abs(Pg_an))]  # overall scale
rel = np.max(np.abs(Pg_num - s*Pg_an))/np.max(np.abs(Pg_an))
relq = np.max(np.abs(Qg_num - s*Qg_an))/np.max(np.abs(Qg_an))
print(f"ground-state ODE vs analytic: max rel err P={rel:.3e}, Q={relq:.3e}")
assert rel < 1e-5 and relq < 1e-5, "ODE does not reproduce standard ground state"
print("PASS: ODE setup reproduces the standard imported ground state")

print("=== G. 10.IV.N1: excited state (n=2,k=-1) has node + non-constant ratio ===")
n_r = 1; ga2 = np.sqrt(1-(Z*ALPHA)**2)
E2 = 1/np.sqrt(1 + (Z*ALPHA/(n_r+ga2))**2)
lam2 = np.sqrt(1-E2**2)
print(f"n=2,k=-1: E={E2:.10f}, lambda={lam2:.6f}")
re_, Pe, Qe = integrate(E2, -1, 1e-4, 1400.0, npts=30000)
# node count in P (sign changes away from tiny values)
sgn = np.sign(Pe); sgn = sgn[sgn != 0]
nodes = np.sum(sgn[1:] != sgn[:-1])
print(f"sign changes in P: {nodes}")
assert nodes >= 1, "no node found in excited P"
rat = Qe/Pe
mask = np.abs(Pe) > 0.05*np.max(np.abs(Pe))   # away from nodes
rratio = rat[mask]
print(f"Q/P over r (away from nodes): min={rratio.min():.4f}, max={rratio.max():.4f}, "
      f"std/mean={rratio.std()/abs(rratio.mean()):.3f}")
assert rratio.std()/abs(rratio.mean()) > 0.3, "excited ratio looks constant"
print("PASS: excited state has a node and a non-constant G/F -> no universal fixed angle")

print("=== H. 10.V.T1 Prufer completion: reconstruction + regularity ===")
for name, F_, G_ in [("ground", Pg_num, Qg_num), ("excited", Pe, Qe)]:
    A = np.sqrt(F_**2 + G_**2)
    Th = np.arctan2(G_, F_)
    assert np.min(A) > 0, f"{name}: F=G=0 somewhere, Theta undefined"
    assert np.max(np.abs(F_ - A*np.cos(Th))) < 1e-9*np.max(A)
    assert np.max(np.abs(G_ - A*np.sin(Th))) < 1e-9*np.max(A)
    ok = np.abs(F_) > 1e-6*np.max(np.abs(F_))
    assert np.max(np.abs(np.tan(Th[ok]) - (G_/F_)[ok])) < 1e-8
    Th_unw = np.unwrap(Th)
    print(f"{name}: recon exact; tan(Theta)=G/F where finite; "
          f"Theta range={Th_unw.max()-Th_unw.min():.3f} rad; min A^2>0 (regular)")
print("PASS: (Theta,P=A^2) reconstructs (F,G); regular through sign changes")
print("      (excited-state Theta runs; ground-state Theta is constant, as expected)")

print("=== I. 10.VI.T1 shared symplectic form (sympy, exact) ===")
F, G = sp.symbols('F G')
u = F - G; v = F + G
J = sp.Matrix([[sp.diff(u, F), sp.diff(u, G)],
               [sp.diff(v, F), sp.diff(v, G)]])
detJ = sp.simplify(J.det())
print(f"det d(u,v)/d(F,G) = {detJ}")
assert detJ == 2, "wedge scaling identity failed"
# hence du^dv = 2 dF^dG, i.e. 4 dF^dG = 2 du^dv: the area element is chart-independent
print("PASS: du∧dv = 2 dF∧dG exactly -> 4*dF∧dG = 2*du∧dv (shared area element)")

print()
print("ALL AUDIT ASSERTIONS PASSED")
