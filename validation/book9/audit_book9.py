#!/usr/bin/env python3
"""RECONSTRUCTED 2026-09-19 — NOT the original audit script.

The original Book 9 numerical audit (reported 2026-09-19: 17 numerical
assertions, max error <= 5.7e-14) was never saved to disk. This script is a
reconstruction from the Book 9 source span (volume2_full.txt lines 2094-2264,
saved as ~/workspace/vol2_book9/source.txt) and the section brief
(~/workspace/vol2_book9/book9_brief.md). It is NOT the original script; it is a
newly written, independently executed check of the same identities.

Assertions covered (17 numerical, numbered N1..N17):

  Section 9.1 (local Lorentz witness; m=1, c=1 units; contract sin chi = beta,
  cos chi = 1/E; 2000 random beta in (0.01, 0.99)):
    N1  sxp(chi) = p*c/(E+m*c^2)
    N2  srx(chi) = (E+m*c^2)/(p*c)
    N3  cxp(chi) = (E+p*c)/(m*c^2)
    N4  crx(chi) = (E-p*c)/(m*c^2)
    N5  cxp = e^eta        (beta = tanh eta)
    N6  crx = e^(-eta)
    N7  cxp*crx = 1        (normalized mass-shell factorization)
    N8  srx*sxp = 1        (upstream Book 2 spine, re-checked here)

  Section 9.3 (reciprocal half-weight theorem; q = sxp(chi) > 0,
  chi in (0.05, pi/2 - 0.05), a = 1):
    N9   u*v = 1            (u = q^(-1/2), v = q^(1/2))
    N10  E_r^2 - O_r^2 = 4  (E_r = u+v, O_r = u-v)
    N11  N = (1-q)/(1+q)    (N = O_r/E_r)
    N12  (1-q)/(1+q) = crx(chi)   (first exterior chart identity)
    N13  r*(1-N^2) = 4*a    (r = a*E_r^2)
    N14  N^2 = 1 - 4*a/r

  Section 9.4 (vacuum Einstein first integral; f(r) = 1 - 4a/r, a = 1,
  r in (5, 20)):
    N15  r*f' + f - 1 = 0
    N16  d[r*(1-f)]/dr = 0  (first integral; checked via numerical gradient)

  Section 9.6 (exact (q, sigma) chart; N in (0.01, 0.99)):
    N17  q = (1-N)/(1+N) inverts N = (1-q)/(1+q) exactly (round-trip)

Deliberately NOT covered here (manuscript assertions, no computation in
source span): Section 9.6 Poisson recovery and static-dust collapse;
Section 9.7 Palatini derivation beyond the standard theorem statement.
Section 9.5's two derivations are symbolic (SymPy) and live in
audit_book9_symbolic.py (also reconstructed).
Section 9.2's two obstructions are checked proofs (linear/wedge algebra),
not numerical assertions.

Global Volume II primitive conventions used here:
  srx = |csc x| + cot x ; sxp = 1/srx (= |csc x| - cot x)
  cxp = |sec x| + tan x ; crx = 1/cxp (= |sec x| - tan x)
"""
import numpy as np

TOL = 1e-9
fails = []
n_assert = 0
max_err = 0.0

def check(name, err):
    global n_assert, max_err
    n_assert += 1
    err = float(np.max(np.abs(err)))
    max_err = max(max_err, err)
    ok = err < TOL
    print(("PASS " if ok else "FAIL ") + f"{name}: maxerr={err:.3e}")
    if not ok:
        fails.append(name)

# ---- canonical primitives (global conventions) ----
def srx(x): return np.abs(1/np.sin(x)) + np.cos(x)/np.sin(x)
def sxp(x): return 1/srx(x)
def cxp(x): return np.abs(1/np.cos(x)) + np.sin(x)/np.cos(x)
def crx(x): return 1/cxp(x)

rng = np.random.default_rng(9)

# ================= 9.1 =================
beta = rng.uniform(0.01, 0.99, 2000)
E = 1/np.sqrt(1-beta**2)   # m=1, c=1
pc = beta*E
mc2 = 1.0
chi = np.arcsin(beta)      # branch chi in (0, pi/2); contract sin chi=beta, cos chi=1/E
assert np.all(chi > 0) and np.all(chi < np.pi/2)

check("N1  9.1 sxp=pc/(E+mc^2)", sxp(chi) - pc/(E+mc2))
check("N2  9.1 srx=(E+mc^2)/pc", srx(chi) - (E+mc2)/pc)
check("N3  9.1 cxp=(E+pc)/mc^2", cxp(chi) - (E+pc)/mc2)
check("N4  9.1 crx=(E-pc)/mc^2", crx(chi) - (E-pc)/mc2)

eta = np.arctanh(beta)     # beta = tanh eta
check("N5  9.1 cxp=e^eta", cxp(chi) - np.exp(eta))
check("N6  9.1 crx=e^-eta", crx(chi) - np.exp(-eta))
check("N7  9.1 cxp*crx=1 (mass shell)", cxp(chi)*crx(chi) - 1)
check("N8  9.1 srx*sxp=1 (upstream spine)", srx(chi)*sxp(chi) - 1)

# ================= 9.3 =================
chi3 = rng.uniform(0.05, np.pi/2 - 0.05, 2000)
q = sxp(chi3)
assert np.all(q > 0)
u = q**(-0.5); v = q**0.5
Er = u + v; Or = u - v
a = 1.0
check("N9  9.3 u*v=1", u*v - 1)
check("N10 9.3 Er^2-Or^2=4", Er**2 - Or**2 - 4)
N = Or/Er
check("N11 9.3 N=(1-q)/(1+q)", N - (1-q)/(1+q))
check("N12 9.3 (1-q)/(1+q)=crx(chi)", (1-q)/(1+q) - crx(chi3))
r = a*Er**2
check("N13 9.3 r(1-N^2)=4a", r*(1-N**2) - 4*a)
check("N14 9.3 N^2=1-4a/r", N**2 - (1-4*a/r))

# ================= 9.4 =================
rr = np.linspace(5.0, 20.0, 2000)   # outside horizon r=4a
f = 1 - 4*a/rr
fp = 4*a/rr**2                       # analytic f'
check("N15 9.4 r f'+f-1=0", rr*fp + f - 1)
C = rr*(1-f)                          # conserved first integral: should be constant 4a
dC = np.gradient(C, rr)
check("N16 9.4 d[r(1-f)]/dr=0", dC)
assert abs(np.mean(C) - 4*a) < 1e-12, "first integral not 4a"
print(f"PASS first integral r(1-f) = {np.mean(C):.15f} (= 4a)")

# ================= 9.6 =================
Nn = rng.uniform(0.01, 0.99, 2000)
qq = (1-Nn)/(1+Nn)
Nback = (1-qq)/(1+qq)
check("N17 9.6 chart inversion round-trip", Nback - Nn)

print(f"\nassertions run: {n_assert}; failed: {len(fails)}; max error: {max_err:.3e}")
if fails:
    print("FAILED:", fails)
    raise SystemExit(1)
print("ALL PASS")
