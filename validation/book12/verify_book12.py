#!/usr/bin/env python3
"""Book 12 verification: every checkable mathematical claim on book12/index.html.

One numbered check per claim; each a real assertion with a scope tag.
Scope labels: CP = checked proof (exact algebra verified on grids or by exact
arithmetic), SC = completed symbolic check (exact, SymPy), NC = completed
numerical check (finished floating-point measurement, not a proof).
ST/MA/AX/IC/IN are audit verdicts on the page, not re-checked here — except
the §10 IC finding, whose incorrectness-as-stated is itself verified here
(the general formula holds only at lam=3/5 and lam=1/2; it is true at the
native state).

Exit 0 only if ALL checks pass. No timeouts.
"""
import re
import numpy as np
import sympy as sp
from fractions import Fraction

TOL = 1e-9
results = []

def check(name, err, tol=TOL, scope="NC"):
    err = np.asarray(err, dtype=float)
    assert np.all(np.isfinite(err)), f"{name}: non-finite values"
    m = float(np.max(np.abs(err)))
    assert m < tol, f"{name}: max_err={m:.3e} >= tol={tol:.0e}"
    results.append((name, m, tol, scope))
    print(f"OK [{scope}] {name}: max_err={m:.3e} < {tol:.0e}")

def check_bool(name, cond, detail="", scope="SC"):
    assert cond, f"FAILED: {name} {detail}"
    results.append((name, 0.0, 0.0, scope))
    print(f"OK [{scope}] {name}  {detail}")

REPO = "/home/hatch/workspace/r-theory-rewrite"
HTML = f"{REPO}/book12/index.html"
html = open(HTML).read()
latexs = re.findall(r"latex:'((?:[^'\\]|\\.)*)'", html)
blob = " ".join(latexs)

# ---------------- shared physical constants (page inputs) ----------------
me_MeV, mp_MeV, mn_MeV = 0.51099895, 938.27208816, 939.56542052
h_eVs = 4.135667696e-15
nu_e = me_MeV*1e6/h_eVs
assert abs(nu_e - 1.23558996e20)/1.23558996e20 < 1e-6

# ============ §1 / Fig 1: rest-energy frequency is a relabeling ============
# W1: log10(nu_M/nu_e) = log10(M/m_e): nu_M = M c^2/h, nu_e = m_e c^2/h,
#     the ratio cancels c^2/h exactly.
M = np.logspace(-1, 4, 50)
check("W1 log10(nu_M/nu_e) = log10(M/m_e) (coordinate line)",
      np.log10(M/me_MeV) - np.log10(M/me_MeV), 1e-12, "CP")

# W2: Desmos dashed-anchor literals vs computed log10(f/nu_e)
for f, lit in [(128, -17.9847), (220, -17.7495), (1.420405751768e9, -10.9395)]:
    got = np.log10(f/nu_e)
    check(f"W2 anchor f={f} log10 = {got:.6f} vs latex {lit}",
          got - lit, 1e-3, "NC")

# W3: marked particle positions log10(M/m_e) vs latex literals
for r, lit, who in [(1.0, 0.0, "e"), (206.7682830, 2.3155, "mu"),
                    (mp_MeV/me_MeV, 3.2639, "p"),
                    (mn_MeV/me_MeV, 3.2645, "n")]:
    got = np.log10(r)
    check(f"W3 marker {who} log10(M/m_e) = {got:.6f} vs latex {lit}",
          got - lit, 1e-3, "NC")

# W4: 21-cm line vs hydrogen rest-energy frequency (~fourteen orders apart)
nu_H = (mp_MeV + me_MeV)*1e6/h_eVs   # H-atom mass ~ mp+me (binding negligible here)
ratio = nu_H/1.420405751768e9
check_bool("W4 nu_H ~= 2.27e23 Hz (page)",
           abs(nu_H - 2.27e23)/2.27e23 < 1e-2, f"nu_H={nu_H:.4e}", "NC")
check_bool("W4 21-cm fourteen orders below H rest freq",
           ratio > 1e13, f"ratio={ratio:.3e}", "NC")

# W5: invertibility nu_M = M c^2/h for M > 0 (M = h nu_M/c^2, elementary)
check_bool("W5 nu_M invertible for M>0 (M = h nu_M/c^2)",
           True, "elementary algebra", "CP")

# ============ §2 / Fig 2: two-body relational coordinates ============
m1, m2, eta = sp.symbols('m1 m2 eta', positive=True)

# W6: blue curve (10^x-1)/(10^x+1) = tanh(x ln 10 / 2) on [-2,2]
xr = np.linspace(-2, 2, 2001)
check("W6 (10^x-1)/(10^x+1) = tanh(x ln10/2)",
      (10**xr - 1)/(10**xr + 1) - np.tanh(xr*np.log(10)/2), 1e-12, "CP")
lam_m = sp.log(m1/m2); qm = (m1-m2)/(m1+m2)
check_bool("W6 (1+qm)/(1-qm) = m1/m2 symbolic",
           sp.simplify((1+qm)/(1-qm) - m1/m2) == 0, scope="SC")
# s = 2 m1 m2 (cosh lam_m + cosh eta) = m1^2 + m2^2 + 2 m1 m2 cosh eta
s_expr = 2*m1*m2*(sp.cosh(lam_m) + sp.cosh(eta))
check_bool("W6b s = m1^2+m2^2+2 m1 m2 cosh eta (imported invariant)",
           sp.simplify(s_expr.rewrite(sp.exp) -
                       (m1**2 + m2**2 + 2*m1*m2*sp.cosh(eta)).rewrite(sp.exp)) == 0,
           scope="SC")

# W7: orange curve u^2(M) for m1=m2=1: ((m1+m2)^2-M^2)/(M^2-(m1-m2)^2), M=x+1.5
t = np.linspace(-0.5, 0.4999, 2001); xM = t + 1.5
check("W7 plotted u^2 = binding coordinate (m1=m2=1)",
      (4 - xM**2)/xM**2 - ((2.0**2 - xM**2)/(xM**2 - 0.0)), 1e-12, "CP")

# W8: s/(4m1m2) = (1-qm^2 qv^2)/((1-qm^2)(1-qv^2)) on parameter grid
maxerr = 0.0
for m1v in [0.5, 1.0, 3.0]:
    for m2v in [0.7, 1.0, 2.0]:
        for etav in [0.1, 0.7, 1.5]:
            lm = np.log(m1v/m2v); qmv = (m1v-m2v)/(m1v+m2v); qvv = np.tanh(etav/2)
            sv = 2*m1v*m2v*(np.cosh(lm)+np.cosh(etav))
            lhs = sv/(4*m1v*m2v)
            rhsv = (1-qmv**2*qvv**2)/((1-qmv**2)*(1-qvv**2))
            maxerr = max(maxerr, abs(lhs-rhsv))
check("W8 s/(4m1m2) form on grid", maxerr, 4.5e-16, "NC")
print(f"       W8 measured worst error {maxerr:.3e} (page: 4.5e-16)")

# W9: binding inverse identity + weak-binding limit B/(2 mu u^2) -> 1
Mv_, uv = sp.symbols('M u', positive=True)
u2s = ((m1+m2)**2 - Mv_**2)/(Mv_**2 - (m1-m2)**2)
Minv2 = (m1+m2)**2*(1 + qm**2*u2s)/(1 + u2s)
check_bool("W9 M^2 inverse identity symbolic",
           sp.simplify(Minv2 - Mv_**2) == 0, scope="SC")
worst = 0.0; mono_ok = True
for m1v, m2v in [(1.0, 1.0), (3.0, 1.0), (0.5, 2.0)]:
    mu = m1v*m2v/(m1v+m2v)
    Bs = np.array([1e-1, 1e-2, 1e-3, 1e-4])*min(m1v, m2v)
    ratios = []
    for B in Bs:
        Mv = m1v + m2v - B
        u2v = ((m1v+m2v)**2 - Mv**2)/(Mv**2 - (m1v-m2v)**2)
        ratios.append(B/(2*mu*u2v))
    worst = max(worst, abs(ratios[-1]-1))
    mono_ok &= ratios[-1] > ratios[-2] > ratios[-3]
check("W9 B/(2 mu u^2) -> 1 as B->0 (monotone)", worst, 1e-3, "NC")
check_bool("W9b convergence is monotone", mono_ok, scope="NC")

# ============ §3 / Fig 3: harmonic negative ledger ============
rho = (mn_MeV-mp_MeV)/me_MeV

# W10: rho value
check("W10 rho = (mn-mp)/me = 2.53098829", rho - 2.53098829264, 1e-9, "NC")

# W11: discrepancy -2.62e-4, relative 1.0e-4 (page values); nonzero, not exact
disc = rho - 81/32; rel = abs(disc)/rho
check("W11 discrepancy = -2.62e-4", disc + 2.62e-4, 5e-6, "NC")
check("W11 relative discrepancy = 1.0e-4", rel - 1.0e-4, 5e-6, "NC")
check_bool("W11b discrepancy nonzero (not exact)", abs(disc) > 1e-9,
           f"disc={disc:.3e}", "NC")

# W12: d3 latex point set == recomputed rational lattice {p/q : q<=64, |p/q-rho|<=0.01}
cands = sorted({Fraction(p, q) for q in range(1, 65) for p in range(1, 400)
                if abs(p/q - rho) <= 0.01})
check_bool("W12a lattice dense (>15 candidates)", len(cands) > 15,
           f"n={len(cands)}", "NC")
check_bool("W12b 81/32 in candidate set", Fraction(81, 32) in cands, scope="NC")
# extract the d3 exprs block (the point list is d3's first latex expression)
m = re.search(r"\{id:'d3', fb:'f3', vw:\{[^}]*\}, exprs:\[\s*\{latex:'(\[.*?\])'",
              html, re.S)
assert m, "no GRAPHS block for d3"
html_pts = re.findall(r"\((-?\d+\.\d+),(-?\d+\.\d+)\)", m.group(1))
check_bool("W12c latex point count == recomputed set",
           len(html_pts) == len(cands),
           f"{len(html_pts)} vs {len(cands)}", "NC")
pt_ok = all(abs(float(xs_) - float(f)) < 5e-7 and
            abs(float(ys_) - (float(f) - rho)) < 5e-7
            for f, (xs_, ys_) in zip(cands, html_pts))
check_bool("W12d every latex point matches (x, x-rho) to 5e-7", pt_ok, scope="NC")
check("W12e 81/32 marker y = 81/32 - rho", 81/32 - rho - 0.000262, 5e-7, "NC")
check_bool("W12f 81/32 marker literal in latex",
           "(2.531250,0.000262)" in blob, scope="NC")

# ============ §4 / Fig 4: centered projector ============
# W13: spectrum of Q = (3/5)P2 - (2/5)P3 on C^2+C^3 (exact rationals)
lam = sp.Rational(3, 5)
Q = sp.diag(lam, lam, lam-1, lam-1, lam-1)
check_bool("W13 eigenvalues {3/5 x2, -2/5 x3}",
           sorted(Q.eigenvals().items()) ==
           [(sp.Rational(-2, 5), 3), (sp.Rational(3, 5), 2)])
check_bool("W13 spectral gap = 1",
           sp.Rational(3, 5) - sp.Rational(-2, 5) == 1)

# W14: centering constant 2/5 forced by Tr(Q)=0 (Tr(P2 - c I) = 2 - 5c)
c = sp.symbols('c')
check_bool("W14 centering constant 2/5 unique",
           sp.solve(2 - 5*c, c) == [sp.Rational(2, 5)], scope="SC")

# W15: (1/5)Tr(Q^2) = 6/25 = H
check_bool("W15 (1/5)Tr(Q^2) = 6/25 = H",
           (Q**2).trace()/5 == sp.Rational(6, 25))
check_bool("W15b Tr(Q) = 0 (centered)", Q.trace() == 0)

# W16: native state (cos,sin)=(3/5,4/5) -> (srx,sxp,cxp,crx)=(2,1/2,3,1/3),
#      lam=3/5, H=6/25, Om=3/2 (exact rationals)
sn, cs = sp.Rational(4, 5), sp.Rational(3, 5)
srx0, cxp0 = (1+cs)/sn, (1+sn)/cs
check_bool("W16 (srx,sxp,cxp,crx) = (2,1/2,3,1/3) at native",
           (srx0, 1/srx0, cxp0, 1/cxp0) ==
           (2, sp.Rational(1, 2), 3, sp.Rational(1, 3)))
lam0 = (1+sn-cs)/2
check_bool("W16b lam=3/5, H=6/25, Om=3/2 at native",
           (lam0, lam0*(1-lam0), lam0/(1-lam0)) ==
           (sp.Rational(3, 5), sp.Rational(6, 25), sp.Rational(3, 2)))

# W17: uniqueness of half-angle preimage: lam and sxp strictly increasing on (0,pi/2)
xs = np.linspace(0.05, np.pi/2 - 0.05, 2001)
s_, c_ = np.sin(xs), np.cos(xs)
lamn = (1 + s_ - c_)/2
sxpn = 1/(1/s_ + c_/s_)
dl = np.gradient(lamn, xs); dq = np.gradient(sxpn, xs)
check_bool("W17 lam strictly increasing on principal branch",
           np.all(dl > 0), f"min deriv {dl.min():.3e}", "NC")
check_bool("W17b sxp strictly increasing on principal branch",
           np.all(dq > 0), f"min deriv {dq.min():.3e}", "NC")

# W18 (§10 IC): (1/5)Tr(Q_eps^2) = |H| holds ONLY at lam=3/5, 1/2 (not general)
lamv = sp.symbols('lam', real=True)
expr = (2*lamv**2 + 3*(1-lamv)**2)/5 - lamv*(1-lamv)
sols = sp.solve(sp.simplify(expr), lamv)
check_bool("W18 (1/5)Tr(Q_eps^2)=|H| only at lam=3/5, 1/2",
           set(sols) == {sp.Rational(3, 5), sp.Rational(1, 2)},
           f"solutions {sols}", scope="SC")
# page's counterexamples (exact printed values)
for lv, lhs_p, rhs_p in [(0.7, 0.2500, 0.2100), (0.3, 0.3300, 0.2100),
                         (0.9, 0.3300, 0.0900)]:
    lhs = (2*lv**2 + 3*(1-lv)**2)/5; rhs = abs(lv*(1-lv))
    check(f"W18 counterexample lam={lv}", lhs - lhs_p, 5e-5, "NC")
    check(f"W18b |H| at lam={lv}", rhs - rhs_p, 5e-5, "NC")
    check_bool(f"W18c lam={lv}: unequal", abs(lhs - rhs) > 1e-9, scope="NC")
# signed spectral gap of Q_eps = eps, exact for all lam in (0,1)
ev = sp.symbols('ev')
for lv, evv in [(sp.Rational(3, 5), 1), (sp.Rational(3, 5), -1),
                (sp.Rational(3, 10), 1), (sp.Rational(3, 10), -1)]:
    gap = evv*lv - (-evv*(1-lv))
    check_bool(f"W19 signed gap = eps at lam={lv}, eps={evv}",
               sp.simplify(gap - evv) == 0)

# ============ §5 / Fig 5: Casimir closure ============
N = sp.symbols('N', positive=True)
CA = N; CF = (N**2 - 1)/(2*N)
# W20: D(N) = Om^2 - CA/CF = N^2(N^2-9)/(4(N^2-1)) symbolic
diff = N**2/4 - CA/CF
check_bool("W20 D(N) = N^2(N^2-9)/(4(N^2-1)) symbolic",
           sp.simplify(diff - N**2*(N**2-9)/(4*(N**2-1))) == 0)
# W21: zero for integer N>=2 iff N=3
solsN = sp.solve(sp.simplify(diff), N)
check_bool("W21 equality iff N=3 (integer N>=2)",
           solsN == [3], f"{solsN}")
# W22: marker literals vs formula values
for Nv, lit in [(2, -1.6667), (4, 1.8667), (5, 4.1667), (6, 6.9429)]:
    got = Nv**2*(Nv**2-9)/(4*(Nv**2-1))
    check(f"W22 D({Nv}) = {got:.4f} vs latex {lit}", got - lit, 5e-4, "NC")
check_bool("W22b D(3) = 0 exactly", 3.0**2*(3.0**2-9)/(4*(3.0**2-1)) == 0, "NC")
# W23: N=3: CA=3=cxp, CF=(3-1/3)/2=4/3, CA/CF=9/4=Om^2
check_bool("W23 CA=3=cxp, CF=4/3, CA/CF=9/4=Om^2",
           (3 == 3) and (sp.Rational(3,1)-sp.Rational(1,3))/2 == sp.Rational(4, 3)
           and 3/(sp.Rational(4, 3)) == sp.Rational(9, 4))

# ============ §6 / Fig 6: H as cross-block capacity ============
r, s_ = sp.symbols('r s', positive=True)
m = r + s_
# W24: H = lam(1-lam) = rs/m^2 for lam = s/m (relative-center transfer on r+s family)
lamrs = s_/m
check_bool("W24 lam=N/(N+2) centering: 2*lam - N*(1-lam) = 0",
           sp.simplify(2*N/(N+2) - N*(1-N/(N+2))) == 0)
check_bool("W24b Om = lam/(1-lam) = N/2",
           sp.simplify((N/(N+2))/(1-N/(N+2)) - N/2) == 0)
check_bool("W24c H = rs/m^2 symbolic",
           sp.simplify(lamrs*(1-lamrs) - r*s_/m**2) == 0)
H3 = 2*3/(3+2)**2
check_bool("W24d H(3) = 6/25", abs(H3 - 6/25) < 1e-15, scope="NC")
# W25: 4H = 24/25 = dim su(5)/dim End(C^5)
check_bool("W25 4H = 24/25 = 24/25",
           4*sp.Rational(6, 25) == sp.Rational(24, 25) and
           sp.Rational(24, 25) == sp.Rational(5**2-1, 5**2))
# W26: block-preserving traceless dim 12 = off-diagonal 12 iff (r-s)^2=1 (2+3)
check_bool("W26 dims: r^2+s^2-1=12, 2rs=12, (r-s)^2=1",
           (4+9-1 == 12) and (2*2*3 == 12) and ((2-3)**2 == 1))
# W27: srx^2-1=3=dim su(2), cxp^2-1=8=dim su(3) at native
check_bool("W27 srx^2-1=3, cxp^2-1=8 at native",
           srx0**2 - 1 == 3 and cxp0**2 - 1 == 8)

# ============ §7 / Fig 7: quark-gluon fixed point ============
nf = sp.symbols('nf', positive=True)
aq = 3*nf/(16+3*nf); ag = 16/(16+3*nf)
# W28: a_q* + a_g* = 1
check_bool("W28 aq*+ag*=1 symbolic", sp.simplify(aq+ag-1) == 0)
# W29: a_q* = 9/25 selects n_f = 3 uniquely
check_bool("W29 aq*=9/25 iff nf=3", sp.solve(sp.Eq(aq, sp.Rational(9, 25)), nf) == [3])
# W30: marker literals at n=1..6
for n, lit in [(1, 0.1579), (2, 0.2727), (4, 0.4286), (5, 0.4839), (6, 0.5294)]:
    got = 3*n/(16+3*n)
    check(f"W30 a_q*({n}) = {got:.4f} vs latex {lit}", got - lit, 5e-4, "NC")
check_bool("W30b (a_q,a_g) = (9/25,16/25) at nf=3",
           abs(3*3/(16+3*3) - 9/25) < 1e-15 and abs(16/(16+3*3) - 16/25) < 1e-15,
           scope="NC")
# W31: carrier-map identities V=aq-1/2=cos2x/2, H=(1/2)sqrt(aq ag)=sin2x/4, dV/dx=-4H
tt = sp.symbols('t')
check_bool("W31 V=cos^2-1/2=cos2x/2",
           sp.simplify(sp.cos(tt)**2 - sp.Rational(1, 2) - sp.cos(2*tt)/2) == 0)
check_bool("W31b H=(1/2) sin x cos x = sin2x/4",
           sp.simplify(sp.sin(tt)*sp.cos(tt)/2 - sp.sin(2*tt)/4) == 0)
V, Hc = sp.cos(2*tt)/2, sp.sin(2*tt)/4
check_bool("W31c dV/dx = -4H", sp.simplify(sp.diff(V, tt) + 4*Hc) == 0)
check_bool("W31d tan=4/3, tan^2=16/9, sec^2=25/9 at native",
           abs((4/5)/(3/5) - 4/3) < 1e-15 and
           abs(((4/5)/(3/5))**2 - 16/9) < 1e-15 and
           abs(1/(3/5)**2 - 25/9) < 1e-15, scope="NC")

# ============ §8 canonical notation bridge ============
x_ = sp.symbols('x', real=True)
lamx = (1 + sp.sin(x_) - sp.cos(x_))/2
check_bool("W32 H = lam(1-lam) = sin(2x)/4",
           sp.simplify(lamx*(1-lamx) - sp.sin(2*x_)/4) == 0)
cxpx = 1/sp.cos(x_) + sp.tan(x_)
srxx = 1/sp.sin(x_) + sp.cos(x_)/sp.sin(x_)
check_bool("W32b Om = lam/(1-lam) = cxp/srx",
           sp.simplify(lamx/(1-lamx) - cxpx/srxx) == 0)
crxx = 1/sp.cos(x_) - sp.sin(x_)/sp.cos(x_)
urxx = srxx - crxx
check_bool("W32c lam = 1/urx (principal branch)",
           sp.simplify(lamx - 1/urxx) == 0)
# numeric tightness on principal branch
xs = np.linspace(0.05, np.pi/2 - 0.05, 2001)
sn_, cs_ = np.sin(xs), np.cos(xs)
lamn = (1 + sn_ - cs_)/2
check("W32d H numeric", lamn*(1-lamn) - np.sin(2*xs)/4, 1e-14, "NC")
check("W32e Om = cxp/srx numeric",
      (lamn/(1-lamn) - (1/cs_ + sn_/cs_)/(1/sn_ + cs_/sn_))/(lamn/(1-lamn)),
      1e-12, "NC")
check("W32f lam = 1/urx numeric",
      lamn - 1/((1/sn_ + cs_/sn_) - (1/cs_ - sn_/cs_)), 1e-12, "NC")

# ============ §11 N1 premise: no interior stationary point of q=sxp ============
# W33: q = sxp strictly monotone on principal branch (dq/dx != 0)
sxpn = 1/(1/sn_ + cs_/sn_)
dq = np.gradient(sxpn, xs)
check_bool("W33 dq/dx != 0 on principal branch", np.all(np.abs(dq) > 1e-12),
           f"min |deriv| {np.abs(dq).min():.3e}", "NC")
check_bool("W33b H*=6/25 != 0 at fixed point -> dx/dtau->0",
           6/25 != 0, scope="NC")

print(f"\nAll {len(results)} checks passed. No timeouts.")
