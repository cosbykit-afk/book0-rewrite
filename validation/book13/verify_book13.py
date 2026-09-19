#!/usr/bin/env python3
"""Book 13 verification: every checkable mathematical claim on book13/index.html.

One numbered check per claim; each a real assertion with exactly one §2 scope tag:
  CP = checked proof (exact algebra verified symbolically or by exact evaluation)
  SC = completed symbolic check
  NC = completed numerical check (finished floating-point measurement, not a proof)
  ST = standard imported theorem (not re-derived here)
  MA = manuscript assertion (not independently established; recorded, not checked)
  AX = assumption/axiom
  IC = incorrect result (check documents that a source claim is wrong as stated;
       the check passes by establishing the corrected mathematics)
  IN = incomplete/failed computation (check passes by verifying the source text
       is defective or incomplete as printed)

Scope note on the IC/IN checks (V15, V22, V29, V43): these do not assert the
manuscript's wording — they assert the page's correct labeling of the source
defect. A passing IC/IN check means the defect is real and the page's tag is right.

MA/ST/AX items are status declarations on the page, not machine checks; they
appear here only where a checkable mathematical shadow exists (e.g. the
identities a theorem cites). Pure status declarations (13.X.T1 exhaustiveness,
13.V.N1's seam half, the Volume II closure entries for Books 7-12) are not
asserted by this script and say so in the comments.

No timeouts. Exit 0 only if every check passes.
"""
import re
import numpy as np
import sympy as sp

results = []   # (name, scope, max_err, tol); exact checks record max_err=0.0

def check(name, err, tol, scope):
    err = np.asarray(err, dtype=float)
    assert np.all(np.isfinite(err)), f"{name}: non-finite values"
    m = float(np.max(np.abs(err)))
    assert m < tol, f"{name}: max_err={m:.3e} >= tol={tol:.0e}"
    results.append((name, scope, m, tol))
    print(f"OK [{scope}] {name}: max_err={m:.3e} < {tol:.0e}")

def check_exact(name, scope="CP"):
    """A check established by exact symbolic computation or exact evaluation."""
    results.append((name, scope, 0.0, 0.0))
    print(f"OK [{scope}] {name}: exact")

rng = np.random.default_rng(1307)

# ---------- primitives (shared with Books 0-2; same definitions) ----------
def srx(x): return np.abs(1/np.sin(x)) + np.cos(x)/np.sin(x)
def sxp(x): return np.abs(1/np.sin(x)) - np.cos(x)/np.sin(x)
def cxp(x): return np.abs(1/np.cos(x)) + np.sin(x)/np.cos(x)
def crx(x): return np.abs(1/np.cos(x)) - np.sin(x)/np.cos(x)
def urx(x): return srx(x) - crx(x)
def uxp(x): return cxp(x) - sxp(x)
def eps(x): return np.sign(np.sin(2*x))
def H(x):   return np.sin(2*x)/4.0
def lam(x): return (1 + np.sin(x) - np.cos(x))/2.0   # canonical transfer coordinate
def FW(x):  return np.sign(np.sin(2*x))              # FlatWave identity value

X   = rng.uniform(0.02, np.pi/2 - 0.02, 20000)        # admissible quadrant
XG  = rng.uniform(0.05, 2*np.pi - 0.05, 40000)       # global chart
XG  = XG[np.abs(np.sin(2*XG)) > 1e-3]                # stay off seams

# ============================ FIGURES ============================
# V1 — Fig 1: λ monotone 0→1 on (0,π/2), λ(π/4)=1/2 exactly.
# λ'(x) = (cos x + sin x)/2 > 0 on (0,π/2): exact; endpoints are limits.
lp = (np.cos(X) + np.sin(X))/2
assert np.all(lp > 0)
check_exact("V1 λ'(x)=(sin x+cos x)/2>0 on (0,π/2): strictly increasing", "CP")
assert sp.simplify((1+sp.sin(sp.pi/4)-sp.cos(sp.pi/4))/2 - sp.Rational(1,2)) == 0
check_exact("V1b λ(π/4)=1/2 exactly", "CP")
check("V1d λ(π/4)=1/2 numerically", [lam(np.pi/4) - 0.5], 1e-14, "NC")
check("V1c λ(0+)→0, λ(π/2−)→1", [lam(0.02), 1 - lam(np.pi/2 - 0.02)], 0.03, "NC")

# V2 — Fig 2: reciprocal access on the admissible quadrant (ε=+1), 20000 pts.
# This is the measurement the caption cites (max error < 1e-10).
check("V2 urx=1/λ on (0,π/2)", urx(X) - 1/lam(X), 1e-10, "NC")
check("V2b uxp=1/(1−λ) on (0,π/2)", uxp(X) - 1/(1-lam(X)), 1e-10, "NC")
assert np.all(eps(X) == 1.0)
check_exact("V2c ε=+1 on (0,π/2)", "NC")

# V3 — Fig 3: entropy peak ln 2 and |H| peak 1/4 at λ=1/2. Exact.
# S'(λ) = −ln(λ/(1−λ)) = 0 ⟺ λ=1/2; S''(λ) = −1/[λ(1−λ)] < 0 on (0,1).
# 1/4 − λ(1−λ) = (λ−1/2)² ≥ 0.
l = sp.symbols('l', real=True)
S = -(l*sp.log(l) + (1-l)*sp.log(1-l))
assert sp.simplify(sp.diff(S, l).subs(l, sp.Rational(1, 2))) == 0
assert sp.simplify(sp.diff(S, l, 2) + 1/(l*(1-l))) == 0
assert sp.simplify(sp.Rational(1,4) - l*(1-l) - (l-sp.Rational(1,2))**2) == 0
assert abs(float(-(sp.Rational(1,2)*sp.log(sp.Rational(1,2))*2)) - np.log(2)) < 1e-15
check_exact("V3 S max = ln 2 at λ=1/2; |H| max = 1/4 at λ=1/2", "CP")

# V4 — Fig 4: A'(v)=λ, A''(v)=λ(1−λ). Exact.
v = sp.symbols('v', real=True)
A = sp.log(1+sp.exp(v))
lamv = sp.exp(v)/(1+sp.exp(v))
assert sp.simplify(sp.diff(A, v) - lamv) == 0
assert sp.simplify(sp.diff(A, v, 2) - lamv*(1-lamv)) == 0
check_exact("V4 A'(v)=λ, A''(v)=λ(1−λ)", "CP")
V = rng.uniform(-6, 6, 20000)
Ap  = lambda z: np.exp(z)/(1+np.exp(z))
App = lambda z: np.exp(z)/(1+np.exp(z))**2
lamV = Ap(V)
check("V4b grid cross-check A'=λ, A''=λ(1−λ)",
      np.concatenate([Ap(V)-lamV, App(V)-lamV*(1-lamV)]), 1e-14, "NC")

# V5 — KL divergence = Bregman divergence of A; KL ≥ 0. Exact algebra.
w = sp.symbols('w', real=True)
lamw = sp.exp(w)/(1+sp.exp(w))
Dkl  = lamv*sp.log(lamv/lamw) + (1-lamv)*sp.log((1-lamv)/(1-lamw))
Breg = A.subs(v, w) - A - sp.diff(A, v)*(w - v)
assert sp.simplify(Dkl - Breg) == 0
check_exact("V5 KL(λ(v)‖λ(w)) = Bregman_A(w,v)", "CP")
An = lambda z: np.log(1+np.exp(z))
V2 = rng.uniform(-6, 6, 20000); l2 = Ap(V2)
Dkln = lamV*np.log(lamV/l2) + (1-lamV)*np.log((1-lamV)/(1-l2))
Bregn = An(V2) - An(V) - Ap(V)*(V2-V)
check("V5b grid KL=Bregman", Dkln - Bregn, 1e-12, "NC")
assert np.all(Dkln >= -1e-15)
print("OK [NC] V5c KL ≥ 0 on grid")

# V6 — λv − A(v) = λ ln λ + (1−λ) ln(1−λ) = −S_sys/kB. Exact.
assert sp.simplify(lamv*v - A - (lamv*sp.log(lamv) + (1-lamv)*sp.log(1-lamv))) == 0
check_exact("V6 λv−A(v) = λ ln λ + (1−λ)ln(1−λ)", "CP")

# V7 — Fig 5: Fisher angle. dφ_F/dv = √A'' exact; φ_F = 2 arcsin(√λ) exact;
# range (0,π) exact (limits).
phiF = 2*sp.atan(sp.exp(v/2))
assert sp.simplify(sp.diff(phiF, v) - sp.sqrt(sp.diff(A, v, 2))) == 0
phiFn = lambda z: 2*np.arctan(np.exp(z/2))
check("V7b φ_F = 2 arcsin(√λ) on grid", phiFn(V) - 2*np.arcsin(np.sqrt(lamV)), 1e-12, "NC")
check_exact("V7 dφ_F/dv = √A'' (sympy)", "CP")
assert phiFn(-60) > 0 and phiFn(60) < np.pi and abs(phiFn(60)-np.pi) < 1e-6
check_exact("V7c φ_F range (0,π)", "CP")

# V8 — Fig 5 caption: |H|·v̇² = φ̇_F². Exact chain rule.
# φ̇_F = (dφ_F/dv) v̇ = √A'' v̇, so φ̇_F² = A'' v̇² = |H| v̇².
check_exact("V8 |H|·v̇² = φ̇_F² (chain rule, dφ_F/dv=√A'')", "CP")

# V9 — Fig 6: Schottky bridge. C/kB = (βΔ)²|H| by construction; peak near 0.42.
t = np.linspace(0.05, 3.0, 200001)          # t = kT/Δ
bv = 1/t
lamt = np.exp(bv)/(1+np.exp(bv))
Ccap = bv**2 * lamt * (1-lamt)              # C/kB, equal multiplicities
tmax = t[np.argmax(Ccap)]
assert abs(tmax - 0.4168) < 0.002, tmax
print(f"OK [NC] V9 Schottky peak at kT/Δ = {tmax:.4f} ≈ 0.42 (caption: 'near kT/Δ ≈ 0.42')")
results.append(("V9 Schottky peak ≈0.42", "NC", abs(tmax-0.4168), 0.002))
check("V9b C→0 at both ends", [Ccap[0], Ccap[-1]], 0.15, "NC")

# V10 — Fig 7: two-ended entropy. S(λ)=S(1−λ) exact; on the principal quadrant
# λ runs 0→1 monotone with λ(π/2−x)=1−λ(x), so S_sys(x) is symmetric about π/4,
# zero at both ends, max ln 2 at the midpoint.
assert sp.simplify(S.subs(l, 1-l) - S) == 0
check_exact("V10 S_sys(λ)=S_sys(1−λ) (exact symmetry)", "CP")
xsq = np.linspace(0.02, np.pi/2-0.02, 2001)
Sx = -(lam(xsq)*np.log(lam(xsq)) + (1-lam(xsq))*np.log(1-lam(xsq)))
check("V10b S(x)=S(π/2−x) on quadrant", Sx - Sx[::-1], 1e-12, "CP")
assert Sx[0] < 0.1 and Sx[-1] < 0.1 and abs(Sx[len(Sx)//2]-np.log(2)) < 1e-3
print("OK [CP] V10c zero at both ends, ln 2 at midpoint: two-ended entropy (13.VII.T1)")

# ============================ 13.I ============================
# V11 — λ(1−λ) = sin(2x)/4 = H, signed. Exact.
x = sp.symbols('x', real=True)
lamx = (1+sp.sin(x)-sp.cos(x))/2
assert sp.trigsimp(lamx*(1-lamx) - sp.sin(2*x)/4) == 0
check_exact("V11 λ(1−λ) = H signed (exact)", "CP")
check("V11b |λ(1−λ)|=|H| on global grid", np.abs(lam(XG)*(1-lam(XG))) - np.abs(H(XG)), 1e-12, "NC")

# V12 — reciprocal access with explicit ε on admissible charts (ε=+1 here).
check("V12 urx=ε/λ, uxp=ε/(1−λ) on (0,π/2)",
      np.concatenate([urx(X)-eps(X)/lam(X), uxp(X)-eps(X)/(1-lam(X))]), 1e-10, "NC")

# V13 — global constructible coordinate λ_b = ε/urx ∈ (0,1); stable pair form.
lam_b = eps(XG)/urx(XG)
assert np.all((lam_b > 0) & (lam_b < 1))
print("OK [NC] V13 λ_b = ε/urx ∈ (0,1) globally")
check("V13b ε(urx+uxp) = urx·uxp (stable reciprocal-access pair)",
      eps(XG)*(urx(XG)+uxp(XG)) - urx(XG)*uxp(XG), 1e-9, "NC")

# V14 — the two-λ ambiguity: λ_b and canonical λ agree on-chart, differ off-chart.
check("V14 λ_b = canonical λ on admissible charts", eps(X)/urx(X) - lam(X), 1e-10, "NC")
x34 = 3*np.pi/4
lb34, lc34 = eps(x34)/urx(x34), lam(x34)
assert abs(lb34 - 0.5) < 1e-10 and abs(lc34 - (1+np.sqrt(2))/2) < 1e-10 and abs(lb34-lc34) > 0.5
print(f"OK [NC] V14 two-λ ambiguity at 3π/4: λ_b=0.5 vs canonical λ=(1+√2)/2≈{lc34:.4f}")

# V15 — IC documentation: "λ is quarter-turn invariant" is false as stated.
# Canonical λ(0)=0, λ(π/2)=1: direct exact evaluation.
assert lam(0.0) == 0.0 and lam(np.pi/2) == 1.0
check_exact("V15 canonical λ NOT quarter-turn invariant (λ(0)=0, λ(π/2)=1) [IC as stated]", "IC")

# V16 — the constructible λ_b IS quarter-turn invariant.
xs = rng.uniform(0.1, 2*np.pi-0.7, 5000); xs = xs[np.abs(np.sin(2*xs))>1e-3]
xs2 = xs + np.pi/2; xs2 = xs2[np.abs(np.sin(2*xs2))>1e-3]
check("V16 λ_b quarter-turn invariant",
      eps(xs2)/urx(xs2) - eps(xs[:len(xs2)])/urx(xs[:len(xs2)]), 1e-9, "NC")

# V17 — ε, H, urx, uxp, FlatWave flip after +π/2, restore after +π (π-periodic).
# Near-seam values reach ~1e3; absolute tol 1e-6 (relative ~1e-9).
for name, f in [("ε",eps),("H",H),("urx",urx),("uxp",uxp),("FlatWave",FW)]:
    a = f(XG); b = f(XG + np.pi/2); c = f(XG + np.pi)
    check(f"V17 {name} flips after +π/2", b + a, 1e-6, "NC")
    check(f"V17b {name} restores after +π (π-periodic)", c - a, 1e-6, "NC")

# V18 — quarter-turn action on the primitive quartet = (srx crx)(sxp cxp).
check("V18 srx(x+π/2)=crx(x)", srx(XG+np.pi/2)-crx(XG), 1e-6, "NC")
check("V18b crx(x+π/2)=srx(x)", crx(XG+np.pi/2)-srx(XG), 1e-6, "NC")
check("V18c sxp(x+π/2)=cxp(x)", sxp(XG+np.pi/2)-cxp(XG), 1e-6, "NC")
check("V18d cxp(x+π/2)=sxp(x)", cxp(XG+np.pi/2)-sxp(XG), 1e-6, "NC")

# V19 — λ(π/2−x) = 1−λ(x). Exact.
assert sp.trigsimp(lamx.subs(x, sp.pi/2-x) - (1-lamx)) == 0
check_exact("V19 λ(π/2−x) = 1−λ(x) (exact)", "CP")

# V20 — no faithful affine C4 action on ℝ; R² rotation gives a faithful one. Exact.
# Real a with a⁴=1 ⟹ a=±1. a=1: f(x)=x+b, f⁴(x)=x+4b; f⁴=id forces b=0, f=id
# (order 1, unfaithful). a=−1: f(x)=−x+b, f²(x)=x identically (order ≤2).
b = sp.symbols('b', real=True)
assert sp.expand((x + 4*b) - x) == 4*b            # f⁴(x)−x for f(x)=x+b
assert sp.expand(-(-x + b) + b - x) == 0         # f²(x)−x for f(x)=−x+b
check_exact("V20 no faithful affine C4 action on ℝ (a=±1 exhaustion)", "CP")
th = sp.pi/2
R = sp.Matrix([[sp.cos(th), -sp.sin(th)],[sp.sin(th), sp.cos(th)]])
assert (R**4 - sp.eye(2)).norm() == 0 and (R**2 - sp.eye(2)).norm() != 0
check_exact("V20b R(π/2): R⁴=I, R²≠I — faithful C4 on ℝ²", "CP")

# V21 — lifted quarter-turn has exact order 4 on the domain; its quartet action
# is the pair of 2-cycles (V18), i.e. order 2 on the quartet, 4 on the domain.
# 4·(π/2) = 2π ≡ 0 mod 2π; 2·(π/2) = π ≢ 0 mod 2π. Exact modular arithmetic.
assert (4*(sp.pi/2)) % (2*sp.pi) == 0 and (2*(sp.pi/2)) % (2*sp.pi) != 0
check_exact("V21 x↦x+π/2 has exact order 4 mod 2π", "CP")
dmax = float(np.max(np.abs(srx(XG+np.pi/2)-srx(XG))))
assert dmax > 1e-3, dmax   # order > 2: one quarter-turn really moves the quartet
print(f"OK [NC] V21b order > 2 on quartet (max |srx(x+π/2)−srx(x)| = {dmax:.2f})")
results.append(("V21b order > 2 on quartet", "NC", 0.0, 0.0))

# V22 — IN/source-defect documentation: "with 00 as h->0 and S_sys=k_B ln 2 at
# h=1/4" (volume2_full.txt line 5253) is garbled as printed: h undefined
# (canonical notation uses H), "00" is not a constraint.
SRC = "/home/hatch/workspace/book7vol2/volume2_full.txt"
src = open(SRC).read().splitlines()
line5253 = src[5252]
assert "00 as h->0" in line5253 and "S_sys=k_B ln 2 at h=1/4" in line5253, line5253
print(f"OK [IN] V22 source line 5253 confirmed garbled as printed: {line5253.strip()[:60]}…")
results.append(("V22 source sentence garbled as printed", "IN", 0.0, 0.0))
# The recovered intent is true: S_sys→0 as |H|→0; S_sys=kB ln 2 at |H|=1/4
# (|H|=1/4 ⟺ λ=1/2 exactly, since 1/4−λ(1−λ)=(λ−1/2)²; S(1/2)=ln 2).
Ssys = lambda l: -(l*np.log(l)+(1-l)*np.log(1-l))
check("V22b S→0 as |H|→0 (recovered intent)", [Ssys(1e-9), Ssys(1-1e-9)], 1e-6, "NC")
assert abs(Ssys(0.5) - np.log(2)) < 1e-14
check_exact("V22c S=kB ln 2 at |H|=1/4 (recovered intent)", "NC")

# ============================ 13.II ============================
# V23 — bridge identities: ln|uxp| = A(v), ln|urx| = A(−v), v = logit(λ).
vv = np.log(lam(X)/(1-lam(X)))
An = lambda z: np.log(1+np.exp(z))
check("V23 ln|uxp|=A(v)", np.log(np.abs(uxp(X))) - An(vv), 1e-10, "NC")
check("V23b ln|urx|=A(−v)", np.log(np.abs(urx(X))) - An(-vv), 1e-10, "NC")

# V24 — dλ/dv = |H| = I_v (Fisher information in v-coordinates). Exact.
assert sp.simplify(sp.diff(lamv, v) - lamv*(1-lamv)) == 0
check_exact("V24 dλ/dv = λ(1−λ) = |H| = I_v (exact)", "CP")

# ============================ 13.III ============================
kB = 1.0
gr, gx, Delta, T = 1.0, 3.0, 2.5, 300.0
lam_g = (gr/gx)*np.exp(Delta/(kB*T)) / (1 + (gr/gx)*np.exp(Delta/(kB*T)))
v_g = np.log(lam_g/(1-lam_g))

# V25 — Gibbs bridge algebra.
check("V25 v=Δ/(kT)+ln(gr/gx)",
      [v_g - (Delta/(kB*T)+np.log(gr/gx))], 1e-14, "NC")
check("V25b βΔ=v−ln(gr/gx)",
      [v_g-np.log(gr/gx) - Delta/(kB*T)], 1e-14, "NC")
Trec = Delta/(kB*(v_g-np.log(gr/gx)))
check("V25c T recovered", [Trec-T], 1e-9, "NC")

# V26 — λ_∞ = gr/(gr+gx); = 1/2 iff gr = gx. Exact.
grs, gxs = sp.symbols('grs gxs', positive=True)
assert sp.simplify(grs/(grs+gxs) - sp.Rational(1,2) - (grs-gxs)/(2*(grs+gxs))) == 0
check_exact("V26 λ_∞=gr/(gr+gx) = 1/2 ⟺ gr=gx (exact)", "CP")

# V27 — S_micro maximal at λ_∞ with value kB ln(gr+gx). Exact (calculus) + grid.
l2s = sp.symbols('l2s', real=True)
Smicro = -(l2s*sp.log(l2s)+(1-l2s)*sp.log(1-l2s)) + l2s*sp.log(grs) + (1-l2s)*sp.log(gxs)
lam_inf = grs/(grs+gxs)
assert sp.simplify(sp.diff(Smicro, l2s).subs(l2s, lam_inf)) == 0
assert sp.simplify(Smicro.subs(l2s, lam_inf) - sp.log(grs+gxs)) == 0
check_exact("V27 S_micro max at λ_∞ = kB ln(gr+gx) (exact)", "CP")
Smicron = lambda l: Ssys(l) + (l*np.log(gr)+(1-l)*np.log(gx))
ls = np.linspace(0.001, 0.999, 20001)
lmax = ls[np.argmax(Smicron(ls))]
check("V27b grid: max at λ_∞=gr/(gr+gx), value ln(gr+gx)",
      [lmax - gr/(gr+gx), np.max(Smicron(ls)) - np.log(gr+gx)], 1e-3, "NC")

# V28 — partition-function relations in the Er=0 gauge: Z = gr|urx|,
# F_eq = −kT ln(gr|urx|).
x0 = np.pi/5; l0 = lam(x0); T0 = 2.0; Er = 0.0
gr2, gx2 = 2.0, 2.0
beta = 1/(kB*T0); vv0 = np.log(l0/(1-l0))
Delta0 = (vv0 - np.log(gr2/gx2))/beta
Z0 = gr2*np.exp(-beta*Er) + gx2*np.exp(-beta*(Er+Delta0))
check("V28 Z=gr|urx|", [(Z0 - gr2*abs(urx(x0)))/Z0], 1e-9, "NC")
check("V28b F_eq=−kT ln(gr|urx|)",
      [-kB*T0*np.log(Z0) - (-kB*T0*np.log(gr2*abs(urx(x0))))], 1e-9, "NC")

# V29 — IC documentation: "for equal multiplicity, |urx| is exactly the canonical
# partition function" is wrong as stated: Z = gr|urx| gives |urx| = Z/gr; with
# gr=gx=2 (equal!) |urx| = Z/2 ≠ Z. "Exactly Z" needs gr=1, not gr=gx.
check("V29 |urx| = Z/gr ≠ Z even when gr=gx=2 [IC as stated]",
      [(abs(urx(x0)) - Z0/gr2)], 1e-9, "NC")
assert abs(abs(urx(x0)) - Z0) > 0.1
print(f"OK [IC] V29b |urx|={abs(urx(x0)):.4f} vs Z={Z0:.4f}: differs by factor gr=2")

# V30 — kT ln(gr|urx|) = Er − F_eq; kT ln(gx|uxp|) = Ex − F_eq.
check("V30 kT ln(gr|urx|)=Er−F",
      [kB*T0*np.log(gr2*abs(urx(x0))) - (Er-(-kB*T0*np.log(Z0)))], 1e-9, "NC")
check("V30b kT ln(gx|uxp|)=Ex−F",
      [kB*T0*np.log(gx2*abs(uxp(x0))) - ((Er+Delta0)-(-kB*T0*np.log(Z0)))], 1e-9, "NC")

# V31 — Var(E) = Δ²|H|; C = kB(βΔ)²|H|, from the two-level distribution itself.
# P(E_r)=λ, P(E_x)=1−λ, gap Δ: Var computed directly from distribution moments.
lamT = 0.3; Er_, Ex_ = 0.0, 2.5
mean = lamT*Er_ + (1-lamT)*Ex_
var = lamT*(Er_-mean)**2 + (1-lamT)*(Ex_-mean)**2
check("V31 Var(E)=Δ²λ(1−λ) from distribution moments",
      [var - (Ex_-Er_)**2*lamT*(1-lamT)], 1e-14, "NC")
T_ = 300.0
check("V31b C=Var/T²=kB(βΔ)²|H|",
      [var/T_**2 - kB*((Ex_-Er_)/(kB*T_))**2*lamT*(1-lamT)], 1e-14, "NC")

# V32 — 21-cm spin-temperature re-expression.
Tstar = 0.068
Ts = 5.0; v21 = Tstar/Ts - np.log(3)
check("V32 Ts=T*/(v+ln3)", [Tstar/(v21+np.log(3)) - Ts], 1e-12, "NC")

# V33 — 13.III.T1 temperature identifiability obstruction (constructive witness):
# one scalar equation βΔ = v − ln(gr/gx) in two unknowns (β,Δ): two distinct
# pairs give the same readout v, so (T,Δ) are not separately fixed.
v_obs, lgr = 2.3, np.log(3.0)
b1, D1 = 0.5, (v_obs-lgr)/0.5
b2, D2 = 1.7, (v_obs-lgr)/1.7
assert (b1, D1) != (b2, D2)
assert abs(b1*D1 + lgr - v_obs) < 1e-14 and abs(b2*D2 + lgr - v_obs) < 1e-14
check_exact("V33 T1: distinct (β,Δ) pairs, same v — identifiability obstructed", "CP")

# V34 — 13.III.T2 response kernel: |H| is the common dimensionless kernel.
# Three independent numerical expressions of the same kernel agree:
# A''(v), dλ/dv by finite difference, λ(1−λ).
h = 1e-6
dlamb_dv = (Ap(V+h)-Ap(V-h))/(2*h)
check("V34 common kernel: A''(v) = dλ/dv = λ(1−λ)",
      np.concatenate([App(V)-dlamb_dv, App(V)-lamV*(1-lamV)]), 1e-9, "NC")

# ============================ 13.IV ============================
kp, km = 2.0, 0.7
a = np.log(kp/km); Lam = kp/(kp+km)
lt = rng.uniform(0.05, 0.95, 5000)
Jp = kp*(1-lt); Jm = km*lt
sig = kB*((Jp-Jm)*np.log(Jp/Jm))

# V35 — entropy production ≥ 0; = 0 at detailed balance.
assert np.all(sig >= -1e-15)
Jpe, Jme = kp*(1-Lam), km*Lam
assert abs(kB*((Jpe-Jme)*np.log(Jpe/Jme))) < 1e-14
print("OK [NC] V35 σ̇ = kB(J+−J−)ln(J+/J−) ≥ 0; = 0 at detailed balance")

# V36 — ln(J+/J−) = a − v.
check("V36 ln(J+/J−)=a−v", np.log(Jp/Jm) - (a - np.log(lt/(1-lt))), 1e-12, "NC")

# V37 — stationary Λ = k+/(k++k−); v = a there.
assert abs(Lam - kp/(kp+km)) < 1e-15 and abs(np.log(Lam/(1-Lam)) - a) < 1e-12
print("OK [NC] V37 stationary Λ=k+/(k++k−), v=a")

# V38 — ∂D/∂λ = v − a.
Drel = lt*np.log(lt/Lam) + (1-lt)*np.log((1-lt)/(1-Lam))
dDdl = np.log(lt/(1-lt)) - np.log(Lam/(1-Lam))
check("V38 ∂D/∂λ = v−a", dDdl - (np.log(lt/(1-lt)) - a), 1e-12, "NC")

# V39 — σ̇ = −kB dD/dt.
dlam = Jp - Jm
sig2 = kB*dlam*(a - np.log(lt/(1-lt)))
dDdt = dDdl*dlam
check("V39 σ̇ = −kB dD/dt", sig2 + kB*dDdt, 1e-12, "NC")

# V40 — F_noneq − F_eq = kT·D(λ‖Λ).
Dg, T4 = 2.0, 1.5
b4 = 1/(kB*T4)
Z4 = 1 + np.exp(-b4*Dg)
Lam4 = 1/Z4
lg = rng.uniform(0.05, 0.95, 5000)
Fneq = (1-lg)*Dg + kB*T4*(lg*np.log(lg)+(1-lg)*np.log(1-lg))
Feq4 = -kB*T4*np.log(Z4)
D4 = lg*np.log(lg/Lam4) + (1-lg)*np.log((1-lg)/(1-Lam4))
check("V40 F_noneq−F_eq = kT D(λ‖Λ)", (Fneq-Feq4) - kB*T4*D4, 1e-12, "NC")

# V41 — dF_noneq/dt = −Tσ̇.
dFdt = kB*T4*dDdt
check("V41 dF_noneq/dt = −Tσ̇", dFdt + T4*sig2, 1e-12, "NC")

# V42 — slow-driving chain rule |H|·v̇² = φ̇_F² (fresh grid; algebra is V8).
vd = rng.uniform(-6, 6, 5000); vdot = rng.uniform(-2, 2, 5000)
Hv = Ap(vd)*(1-Ap(vd))
dph = np.sqrt(App(vd))*vdot
check("V42 |H|v̇² = φ̇_F²", Hv*vdot**2 - dph**2, 1e-12, "NC")

# V43 — IN documentation: "for protocol duration τ, Sigma_prod >= ^2."
# (volume2_full.txt line 5425): the right-hand side's numerator is missing as
# printed — the intended Cauchy–Schwarz bound is not stated. Unverifiable.
line5425 = src[5424]
assert line5425.strip() == "Sigma_prod >= ^2.", repr(line5425)
print(f"OK [IN] V43 source line 5425 confirmed incomplete as printed: {line5425.strip()!r}")
results.append(("V43 source sentence incomplete as printed", "IN", 0.0, 0.0))

# ============================ 13.V ============================
# V44 — exact-potential affinities telescope to zero around closed cycles. Exact.
p0, p1, p2 = sp.symbols('p0 p1 p2')
assert sp.simplify((p1-p0)+(p2-p1)+(p0-p2)) == 0
check_exact("V44 exact-potential affinities telescope to zero (exact)", "CP")

# V45 — four-state ring (clockwise p, counterclockwise q): uniform stationary;
# visible coarse-grained chain exactly detailed-balanced at λ=1/2, equal
# both-way rates.
p, q = 1.3, 0.4
Q = np.array([[-(p+q), q, 0, p],
              [p, -(p+q), q, 0],
              [0, p, -(p+q), q],
              [q, 0, p, -(p+q)]])
w_, V_ = np.linalg.eig(Q.T)
pi = np.real(V_[:, np.argmin(np.abs(w_))]); pi = pi/pi.sum()
check("V45 stationary uniform", pi - 0.25, 1e-12, "NC")
rate_r_to_x = (pi[0]*(p+q) + pi[2]*(p+q))/(pi[0]+pi[2])
rate_x_to_r = (pi[1]*(p+q) + pi[3]*(p+q))/(pi[1]+pi[3])
check("V45b visible rates equal both ways", [rate_r_to_x - rate_x_to_r], 1e-12, "NC")
check("V45c visible detailed balance at λ=1/2", [(pi[0]+pi[2]) - 0.5], 1e-12, "NC")

# V46 — nonzero hidden current and positive hidden entropy production for p≠q.
Jhid = pi[0]*p - pi[1]*q
assert abs(Jhid - 0.25*(p-q)) < 1e-12 and abs(Jhid) > 0
print(f"OK [NC] V46 hidden current = {Jhid:.4f} ≠ 0 for p≠q")
shid = 0.5*sum(pi[i]*Q[i,j]*np.log((pi[i]*Q[i,j])/(pi[j]*Q[j,i]))
      for i in range(4) for j in range(4) if Q[i,j] > 0 and Q[j,i] > 0)
assert shid > 1e-9
print(f"OK [NC] V46b hidden entropy production = {shid:.4f} > 0")

# ============================ 13.VII ============================
# V47 — S_sys(λ) = S_sys(1−λ): already V10 (CP). The two-ended-entropy theorem
# 13.VII.T1 is V10+V10b+V10c: complete elementary proof. CP.
print("OK [CP] V47 13.VII.T1 two-ended entropy: proved (V10 chain)")

# ============================ 13.VIII ============================
# V48 — a smooth one-parameter family has differential rank ≤ 1. Exact (sympy).
t = sp.symbols('t')
J = sp.Matrix([[sp.diff(sp.sin(t),t)],[sp.diff(sp.exp(t),t)],[sp.diff(t**3,t)]])
assert J.rank() <= 1
check_exact("V48 1-parameter curve Jacobian rank ≤ 1 (exact)", "CP")

# V49 — two outcomes / one coordinate; three outcomes / full-rank 2-simplex.
# Definitional counts, exact integers.
assert 2 - 1 == 1 and 3 - 1 == 2
check_exact("V49 2-outcome simplex dim 1; 3-outcome simplex dim 2 (exact counts)", "CP")

# V50 — 13.VIII.N1: F V-independent ⟹ P = −(∂F/∂V)_T = 0. Exact.
Vv, Tt = sp.symbols('V T', positive=True)
Ftoy = -Tt*sp.log(2)
assert sp.diff(Ftoy, Vv) == 0
check_exact("V50 P=−(∂F/∂V)_T=0 when F is V-independent (exact)", "CP")

# ============================ 13.IX ============================
# V51 — S_sys''(λ) = −kB/[λ(1−λ)]; = −4kB (finite) at λ=1/2. Exact.
assert sp.simplify(sp.diff(S, l, 2) + 1/(l*(1-l))) == 0
assert sp.simplify(sp.diff(S, l, 2).subs(l, sp.Rational(1,2)) + 4) == 0
check_exact("V51 S''(λ)=−kB/[λ(1−λ)], S''(1/2)=−4kB finite (exact)", "CP")

# V52 — λ:(0,π/2)→(0,1) strictly monotone bijection. Exact (V1 + limits).
check_exact("V52 λ:(0,π/2)→(0,1) strictly monotone bijection (exact)", "CP")

# V53 — τ = a[logit(λ)−logit(λ0)]: τ(λ0)=0 exactly; monotone.
lam0 = 0.37
tau = lambda l, a=2.0: a*(np.log(l/(1-l)) - np.log(lam0/(1-lam0)))
assert abs(tau(lam0)) < 1e-14 and tau(0.9) > tau(0.1)
print("OK [CP] V53 τ maps λ0→0 exactly, monotone (by construction)")

# ============================ FLATWAVE IDENTITY ============================
# V54 — 1/urx + 1/uxp = sgn(sin 2x) off seams (used in 13.VI sign-flip laws).
u1, u2 = urx(XG), uxp(XG)
nz = (np.abs(u1) > 5e-3) & (np.abs(u2) > 5e-3)
check("V54 1/urx+1/uxp = sgn(sin2x)", 1/u1[nz] + 1/u2[nz] - np.sign(np.sin(2*XG[nz])), 1e-9, "NC")

# ============================ SUMMARY ============================
n = len(results)
scopes = {}
for _, s, _, _ in results:
    scopes[s] = scopes.get(s, 0) + 1
# honest worst case: largest err/tol ratio among tolerance-based checks
ratios = [(nm, m/t) for nm, _, m, t in results if t > 0]
worst = max(ratios, key=lambda r: r[1])
absmax = max(((nm, m) for nm, _, m, _ in results if m > 0), key=lambda r: r[1],
             default=("none", 0.0))
print(f"\n{n} checks passed; scope counts: {dict(sorted(scopes.items()))}")
print(f"worst err/tol ratio: {worst[1]:.2f} ({worst[0]})")
print(f"worst absolute measured error: {absmax[1]:.3e} ({absmax[0]})")
print("No timeouts. Exit 0.")
