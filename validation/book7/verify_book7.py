#!/usr/bin/env python3
"""Book 7 verification: every checkable mathematical claim on book7/index.html.

One numbered check per checkable claim (V1..V88, with V4 split into V4a/V4b:
89 assertions total); every check is a real assertion with a scope tag.
Exit 0 only if ALL pass. Failures, errors and timeouts are reported, never
absorbed. No timeouts (all checks are vectorized NumPy / SymPy exact
simplifications; full run ~4 s).

Scope labels (WORKFLOW.md section 2):
  CP = checked proof   (exact algebra / exact integer arithmetic, confirmed on grid)
  NC = completed numerical check (finished floating-point measurement, not a proof)
  SC = completed symbolic check  (finished exact SymPy computation)
  ST = standard imported theorem (noted where used; not machine-checked)

Subsumes validation/book7/audit_book7.py and audit_book7_symbolic.py.
Differences from the old scripts (disclosed):
  - old "7.1.3 S'=2C (analytic)" compared 2*C-2*C (neutered, always true);
    replaced by real SymPy differentiation (V21).
  - old "saw_r=eps*lam" used lam:=eps*saw_r, making it a tautology; here lam
    is the transfer coordinate BY DEFINITION, saw_r=eps*lam is exact algebra
    (eps^2=1), and saw_x=eps*(1-lam) is proved from the FlatWave identity
    1/urx+1/uxp=sgn(sin2x), re-verified here (V4a, inherits Book 0 V8).
  - old "7.1 tmp N=4cot2x" line contained a dead '*0' term; rewritten cleanly
    as a relative-error check (V19): near seams |N| grows like |cot|, so
    absolute error is the wrong measure; relative error is reported.

Canonical definitions (series notation):
  srx=|csc x|+cot x; sxp=1/srx; cxp=|sec x|+tan x; crx=1/cxp
  urx=srx-crx; uxp=cxp-sxp
  saw_r=1/urx; saw_x=1/uxp
  H=1/(urx+uxp); eps=sgn(sin 2x)
  lam=eps*saw_r                     (transfer coordinate, definition)
  lam_principal=(1+sin x-cos x)/2   (principal-chart branch formula)
"""
import numpy as np
import sympy as sp

results = []   # (name, scope, max_err, tol)
n_exact_asserts = 0

def check(name, err, tol=1e-9, scope="NC"):
    """err: array (absolute or relative error, caller decides and documents)."""
    global n_exact_asserts
    err = np.asarray(err, dtype=float)
    assert np.all(np.isfinite(err)), f"{name}: non-finite values"
    m = float(np.max(np.abs(err)))
    assert m < tol, f"{name}: max_err={m:.3e} >= tol={tol:.0e}"
    n_exact_asserts += 1
    results.append((name, scope, m, tol))
    print(f"OK [{scope}] {name}: max_err={m:.3e} < {tol:.0e}")

def check_assert(name, cond, scope="NC", note=""):
    global n_exact_asserts
    assert cond, f"{name}: FAILED {note}"
    n_exact_asserts += 1
    results.append((name, scope, 0.0, 0.0))
    print(f"OK [{scope}] {name}" + (f" ({note})" if note else ""))

def check_c(name, zerr, tol=1e-9, scope="NC"):
    """Complex-valued check: error = |complex difference|."""
    check(name, np.abs(np.asarray(zerr, dtype=complex)), tol, scope)

def rel(a, b):
    return np.abs(a - b) / (1 + np.abs(b))

# ---------------- primitives ----------------
def srx(x): return np.abs(1/np.sin(x)) + np.cos(x)/np.sin(x)
def sxp(x): return np.abs(1/np.sin(x)) - np.cos(x)/np.sin(x)   # manuscript primitive form
def cxp(x): return np.abs(1/np.cos(x)) + np.sin(x)/np.cos(x)
def crx(x): return np.abs(1/np.cos(x)) - np.sin(x)/np.cos(x)   # manuscript primitive form
def urx(x): return srx(x) - crx(x)
def uxp(x): return cxp(x) - sxp(x)
def saw_r(x): return 1/urx(x)
def saw_x(x): return 1/uxp(x)
def epsf(x): return np.sign(np.sin(2*x))
def Hf(x): return 1/(urx(x)+uxp(x))
def lam_of(x): return epsf(x)*saw_r(x)          # transfer coordinate (definition)
def lam_principal(x): return (1+np.sin(x)-np.cos(x))/2

def seam_mask(x, gap=1e-3):
    return (np.abs(np.sin(x)) < gap) | (np.abs(np.cos(x)) < gap)

# dense deterministic grid over two full periods, seams excluded,
# saw-singular points (|urx|,|uxp| ~ 0) excluded
xg = np.linspace(-2*np.pi + 0.02, 2*np.pi - 0.02, 160001)
xg = xg[~seam_mask(xg)]
m = (np.abs(urx(xg)) > 1e-6) & (np.abs(uxp(xg)) > 1e-6)
x = xg[m]
print(f"grid: {len(x)} points on four open charts, seam gap 1e-3")

eps = epsf(x)
lam = lam_of(x)
H = Hf(x)

# ================= 7.1.1 saw balance product =================
check_assert("V1 lam in (0,1) on all charts",
             np.all(lam > 0) and np.all(lam < 1), "NC",
             f"min={lam.min():.3e} max={lam.max():.6f}")
xp = x[(x > 0.03) & (x < np.pi/2 - 0.03)]   # principal chart
check("V2 lam_principal formula = eps*saw_r (principal chart)",
      lam_of(xp) - lam_principal(xp), 1e-9, "NC")
# V3: exact algebra: eps*lam = eps^2*saw_r = saw_r
check("V3 saw_r = eps*lam", saw_r(x) - eps*lam, 1e-15, "CP")
# V4a/V4b: FlatWave identity (Book 0 V8, re-verified here), then saw_x = eps-saw_r
check("V4a FlatWave 1/urx+1/uxp = sgn(sin2x)",
      (1/urx(x) + 1/uxp(x)) - eps, 1e-9, "CP")
check("V4b saw_x = eps*(1-lam)", saw_x(x) - eps*(1-lam), 1e-9, "CP")
# V5: parallel sum 1/(1/a+1/b) = ab/(a+b), exact
check("V5 H = (saw_r*saw_x)/(saw_r+saw_x)",
      H - (saw_r(x)*saw_x(x))/(saw_r(x)+saw_x(x)), 1e-15, "CP")
# V6,V7: exact given V3,V4a
# V6,V7: exact given V3,V4; measured error inherits V4's near-seam cancellation
check("V6 H = eps*lam*(1-lam)", H - eps*lam*(1-lam), 1e-12, "CP")
check("V7 |H| = lam*(1-lam)", np.abs(H) - lam*(1-lam), 1e-12, "CP")
# V8,V9: transfer-content identities, numerical
check("V8 H = sin(2x)/4", H - np.sin(2*x)/4, 1e-9, "NC")
A, B = cxp(x), srx(x)
check("V9 H = A*B/((A+B)*(A*B-1))", H - A*B/((A+B)*(A*B-1)), 1e-9, "NC")
# V10: exact bound: 1/4-lam(1-lam) = (lam-1/2)^2 >= 0
check_assert("V10 lam*(1-lam) <= 1/4, equality iff lam=1/2",
             np.all(lam*(1-lam) <= 0.25 + 1e-15), "CP", "exact: (lam-1/2)^2>=0")
# V11: sharpness attained (spot check at x=pi/4)
x0 = np.pi/4
check_assert("V11 sharpness: lam(pi/4)=1/2, H(pi/4)=1/4",
             abs(lam_principal(x0)-0.5) < 1e-15 and abs(np.sin(2*x0)/4-0.25) < 1e-15,
             "NC", "balance point attained")

# ================= 7.1.2 companion cosine =================
check("V12 cos2x = eps*(1-2lam)*sqrt(1+4lam(1-lam))",
      np.cos(2*x) - eps*(1-2*lam)*np.sqrt(1+4*lam*(1-lam)), 1e-9, "NC")
check("V13 saw_x-saw_r = eps*(1-2lam) [exact given V4a; inherits its cancellation]",
      (saw_x(x)-saw_r(x)) - eps*(1-2*lam), 1e-12, "CP")
check("V14 saw_r*saw_x = lam*(1-lam) [exact given V4a; inherits its cancellation]",
      saw_r(x)*saw_x(x) - lam*(1-lam), 1e-12, "CP")
check("V15 UNA form cos2x = (1/uxp-1/urx)*sqrt(1+4/(urx*uxp))",
      np.cos(2*x) - (1/uxp(x)-1/urx(x))*np.sqrt(1+4/(urx(x)*uxp(x))), 1e-9, "NC")

# ================= 7.1 temporary D/N calculation =================
D = urx(x)+uxp(x); N = srx(x)-sxp(x)-cxp(x)+crx(x)
check("V16 N = 4cot(2x) [relative: |N| grows near seams]",
      rel(N, 4*np.cos(2*x)/np.sin(2*x)), 1e-9, "NC")
check("V17 D^2-N^2 = 16 [relative]", rel(D**2-N**2, 16), 1e-9, "NC")
check("V18 4/D = sin(2x)", 4/D - np.sin(2*x), 1e-9, "NC")
check("V19 N/D = cos(2x)", N/D - np.cos(2*x), 1e-9, "NC")

# ================= 7.1.3 carrier phasor =================
Vv = np.cos(2*x)/2
Z = 2*Vv + 1j*4*H
check_c("V20 Z = 2V+i4H = e^{2ix} [Euler ST background]",
        Z - np.exp(1j*2*x), 1e-9, "NC")

# ================= 7.1.4 transfer-carrier quadratic map =================
al = np.sign(np.sin(x)); be = np.sign(np.cos(x))
check("V21 eps = al*be = sgn(sin2x) [exact pointwise]",
      al*be - eps, 1e-15, "CP")
ep = al*be
p = al*np.cos(x) - be*np.sin(x)
q = al*np.sin(x) + be*np.cos(x)
check("V22 p^2+q^2 = 2 [exact: al^2=be^2=1]", p**2+q**2-2, 1e-15, "CP")
check("V23 q = |sin x|+|cos x| [exact]", q-(np.abs(np.sin(x))+np.abs(np.cos(x))), 1e-15, "CP")
check("V24 p = 1-2lam [inherited Book 2 transfer data]", p-(1-2*lam), 1e-9, "NC")
check("V25 p*q = eps*cos(2x)", p*q - ep*np.cos(2*x), 1e-9, "NC")
check("V26 q^2-p^2 = 2*eps*sin(2x)", q**2-p**2-2*ep*np.sin(2*x), 1e-9, "NC")
a, b = q/np.sqrt(2), p/np.sqrt(2)
check("V27 a^2+b^2 = 1 [exact given V22]", a**2+b**2-1, 1e-15, "CP")
U, W = np.sin(2*x), np.cos(2*x)
check("V28 U = eps*(a^2-b^2)", U - ep*(a**2-b**2), 1e-9, "NC")
check("V29 W = 2*eps*a*b", W - 2*ep*a*b, 1e-9, "NC")
zeta = a + 1j*b
check_c("V30 U+iW = eps*zeta^2", (U+1j*W) - ep*zeta**2, 1e-9, "NC")

# ================= 7.2 primitive decomposition =================
check("V31 L1 reciprocal pairs crx*cxp=1, sxp*srx=1 [Book 0 V1]",
      np.concatenate([crx(x)*cxp(x)-1, sxp(x)*srx(x)-1]), 1e-9, "CP")
check("V32 T1 urx+uxp = 2(tan+cot) = 4/sin(2x) [exact; Book 0 V7]",
      np.abs(urx(x)+uxp(x)-4/np.sin(2*x))/(1+np.abs(4/np.sin(2*x))), 1e-9, "CP")
check("V33 T1 sin(2x)/4 = 1/(urx+uxp) [exact reciprocal]",
      np.sin(2*x)/4 - 1/(urx(x)+uxp(x)), 1e-12, "CP")
den = ((np.sin(x)/np.cos(x) + np.abs(1/np.cos(x))
        + np.cos(x)/np.sin(x) + np.abs(1/np.sin(x)))
       - 1/(np.sin(x)/np.cos(x) + np.abs(1/np.cos(x)))
       - 1/(np.cos(x)/np.sin(x) + np.abs(1/np.sin(x))))
check("V34 T1 expanded denominator form [exact: 1/(tan+|sec|)=crx]",
      np.sin(2*x)/4 - 1/den, 1e-9, "CP")
check("V35 T2 cxp+crx = 2|sec|, srx+sxp = 2|csc| [exact]",
      np.concatenate([(cxp(x)+crx(x))-2*np.abs(1/np.cos(x)),
                       (srx(x)+sxp(x))-2*np.abs(1/np.sin(x))]), 1e-9, "CP")
check("V36 T2 cos(2x)/4 = 1/(cxp+crx)^2 - 1/(srx+sxp)^2 [exact]",
      np.cos(2*x)/4 - (1/(cxp(x)+crx(x))**2 - 1/(srx(x)+sxp(x))**2), 1e-9, "CP")
e1 = np.sin(x)/np.cos(x) + np.abs(1/np.cos(x)) + 1/(np.sin(x)/np.cos(x) + np.abs(1/np.cos(x)))
e2 = np.cos(x)/np.sin(x) + np.abs(1/np.sin(x)) + 1/(np.cos(x)/np.sin(x) + np.abs(1/np.sin(x)))
check("V37 T2 expanded primordial form [exact given V35]",
      np.cos(2*x)/4 - (1/e1**2 - 1/e2**2), 1e-9, "CP")
Cx, Sx = 1/(cxp(x)+crx(x))**2, 1/(srx(x)+sxp(x))**2
check("V38 C2 C+S=1/4, C-S=cos(2x)/4 [exact]",
      np.concatenate([Cx+Sx-1/4, Cx-Sx-np.cos(2*x)/4]), 1e-9, "CP")
check("V39 C3 V = 2[1/(cxp+crx)^2-1/(srx+sxp)^2] = cos(2x)/2 [exact]",
      Vv - 2*(1/(cxp(x)+crx(x))**2 - 1/(srx(x)+sxp(x))**2), 1e-9, "CP")

# ================= 7.3 carrier flow (algebraic part) =================
P = np.sin(2*x)/4
E = Vv**2 + 4*P**2
check("V40 T2 E = V^2+4P^2 = 1/4 on orbit", E - 1/4, 1e-12, "NC")
Amat = np.array([[0., 1.], [-4., 0.]])
Gmat = np.diag([4., 1.])
check("V41 C2 A^2 = -4I [exact integer arithmetic]",
      (Amat@Amat + 4*np.eye(2)).ravel(), 1e-15, "CP")
check("V42 C2 A^T G + G A = 0 [exact]", (Amat.T@Gmat + Gmat@Amat).ravel(), 1e-15, "CP")
x0 = 0.7
Y0 = np.array([np.sin(2*x0)/4, np.cos(2*x0)/2])
ev_err = []
for xt in [0.3, 1.1, 2.5, 4.0]:
    Yt = (np.eye(2)*np.cos(2*(xt-x0)) + (Amat/2)*np.sin(2*(xt-x0))) @ Y0
    ev_err.append(Yt - np.array([np.sin(2*xt)/4, np.cos(2*xt)/2]))
check("V43 C3 evolution operator exp(A dt) [4 targets]", np.concatenate(ev_err), 1e-9, "NC")
Q = 2*P
check("V44 C4 Q^2+V^2 = 1/4 [exact]", Q**2+Vv**2-1/4, 1e-15, "CP")
check("V45 T3 H_ham = V^2/2+2P^2 = 1/8 on orbit [exact]",
      Vv**2/2 + 2*P**2 - 1/8, 1e-15, "CP")

# ================= 7.4 hyperbolic parent =================
Sig = urx(x) + uxp(x)
Del = (srx(x)+crx(x)) - (sxp(x)+cxp(x))
check("V46 T1 Sig = 2(cot+tan), Del = 2(cot-tan) [exact; relative]",
      np.concatenate([rel(Sig, 2*(np.cos(x)/np.sin(x)+np.sin(x)/np.cos(x))),
                      rel(Del, 2*(np.cos(x)/np.sin(x)-np.sin(x)/np.cos(x)))]), 1e-9, "CP")
check("V47 T1 Sig+Del = 4cot x, Sig-Del = 4tan x [relative]",
      np.concatenate([rel(Sig+Del, 4*np.cos(x)/np.sin(x)),
                      rel(Sig-Del, 4*np.sin(x)/np.cos(x))]), 1e-9, "NC")
check("V48 T1 Sig^2-Del^2 = 16 [relative]", rel(Sig**2-Del**2, 16), 1e-9, "NC")
S7, Q7 = 4/Sig, Del/Sig
check("V49 T2 S = 4/Sig = sin2x, Q = Del/Sig = cos2x, Q^2+S^2=1",
      np.concatenate([S7-np.sin(2*x), Q7-np.cos(2*x), Q7**2+S7**2-1]), 1e-9, "NC")
Lp = (eps/4)*(Sig+Del); Lm = (eps/4)*(Sig-Del)
check("V50 T6 L+ = |cot x|, L- = |tan x|, L+*L- = 1 [relative]",
      np.concatenate([rel(Lp, np.abs(np.cos(x)/np.sin(x))),
                      rel(Lm, np.abs(np.sin(x)/np.cos(x))),
                      Lp*Lm-1]), 1e-9, "NC")
w = np.log(np.abs(np.cos(x)/np.sin(x)))
check("V51 C6 Sig = 4eps cosh w, Del = 4eps sinh w [relative]",
      np.concatenate([rel(Sig, 4*eps*np.cosh(w)), rel(Del, 4*eps*np.sinh(w))]), 1e-9, "NC")
check("V52 C7 Q = tanh w, S = eps sech w",
      np.concatenate([Q7-np.tanh(w), S7-eps/np.cosh(w)]), 1e-9, "NC")
L = Lp
check("V53 T7 Q = (L^2-1)/(L^2+1), S = 2eps L/(L^2+1)",
      np.concatenate([Q7-(L**2-1)/(L**2+1), S7-2*eps*L/(L**2+1)]), 1e-9, "NC")
check("V54 T7 H = eps L/(2(L^2+1)), V = (L^2-1)/(2(L^2+1))",
      np.concatenate([H-eps*L/(2*(L**2+1)), Vv-(L**2-1)/(2*(L**2+1))]), 1e-9, "NC")
K = Sig**2 - Del**2
check("V55 E1 K = 16 on trig image [relative]; conic Q^2+(K/16)S^2=1",
      np.concatenate([rel(K, 16), Q7**2+(K/16)*S7**2-1]), 1e-9, "NC")

# ================= editorial convention + CL2 sign audit =================
Om = lam/(1-lam)
check("V56 conv Omega = lam/(1-lam) = cxp/srx [exact; relative: |Om| grows near seams]",
      rel(Om, cxp(x)/srx(x)), 1e-9, "NC")
two_lam_m1 = 2*lam_principal(xp) - 1
check("V57 CL2 correct: 2lam-1 = sin x - cos x [exact]",
      two_lam_m1 - (np.sin(xp)-np.cos(xp)), 1e-12, "CP")
ms_err = float(np.max(np.abs(two_lam_m1 - (np.cos(xp)-np.sin(xp)))))
check_assert("V58 CL2 manuscript '2lam-1 = cos x - sin x' is wrong as stated",
             ms_err > 1e-9, "NC", f"maxerr of printed form = {ms_err:.3e} >> tol")

# ================= embed-formula cross-checks =================
# d1 live embed domain after fix: x in [0, pi/2]; caption's "|H| (orange)" and
# "bounded channels" claims require lam in [0,1] there.
xe1 = np.linspace(0, np.pi/2, 4001)
lam_e1 = (1+np.sin(xe1)-np.cos(xe1))/2
check_assert("V59 d1 embed domain: lam in [0,1], orange = |H| >= 0",
             np.all(lam_e1 >= 0) and np.all(lam_e1 <= 1), "NC", "caption holds on [0,pi/2]")
check("V60 d1 embed: orange lam(1-lam) = sin(2x)/4 [exact algebra]",
      lam_e1*(1-lam_e1) - np.sin(2*xe1)/4, 1e-15, "CP")
# d2 live embed uses the principal-branch L WITHOUT eps (as shipped); verify the
# plotted orange-dashed product equals cos(2x) on the embed's displayed domain.
# Open interval: at the seam x=0, eps=0 and lam is undefined (saw singular).
xe2 = np.linspace(0.0005, np.pi/2-0.0005, 4000)
Lp_e = (1+np.sin(xe2)-np.cos(xe2))/2
check("V61 d2 embed: (1-2L)sqrt(1+4L(1-L)) = cos(2x) on (0,pi/2)",
      (1-2*Lp_e)*np.sqrt(1+4*Lp_e*(1-Lp_e)) - np.cos(2*xe2), 1e-9, "NC")
# d2 new orange-dotted bare-imbalance curve y=1-2L(x): equals eps(1-2lam) on the
# principal chart (eps=+1 there).
urx_e = (np.abs(1/np.sin(xe2))+np.cos(xe2)/np.sin(xe2)) - \
        (np.abs(1/np.cos(xe2))-np.sin(xe2)/np.cos(xe2))
check("V62 d2 dotted 1-2L(x) = eps(1-2lam) on principal chart",
      (1-2*Lp_e) - (1-2/urx_e), 1e-9, "NC")

print("\n---- symbolic section (SymPy, exact) ----")

def check_sym(name, expr):
    v = sp.simplify(expr)
    ok = (v == 0)
    assert ok, f"{name}: FAILED, simplified={v}"
    global n_exact_asserts
    n_exact_asserts += 1
    results.append((name, "SC", 0.0, 0.0))
    print(f"OK [SC] {name}")

xs = sp.symbols('x', real=True)
# 7.1.C2
Hs = sp.sin(2*xs)/4
check_sym("V63 C2 cos(2x) = 2 dH/dx", sp.cos(2*xs) - 2*sp.diff(Hs, xs))
# 7.1.T2 magnitude + sign, principal branch
lams = (1+sp.sin(xs)-sp.cos(xs))/2
check_sym("V64 T2 (1-2lam)^2(1+4lam(1-lam)) = cos^2(2x)",
          (1-2*lams)**2*(1+4*lams*(1-lams)) - sp.cos(2*xs)**2)
check_sym("V65 T2 (1-2lam)/cos(2x) = 1/(sin x+cos x)",
          (1-2*lams)/sp.cos(2*xs) - 1/(sp.sin(xs)+sp.cos(xs)))
# 7.1.3 quadrature oscillator + unit circle (fixes old neutered check)
Ss, Cs = sp.sin(2*xs), sp.cos(2*xs)
check_sym("V66 S' = 2C", sp.diff(Ss, xs) - 2*Cs)
check_sym("V67 C' = -2S", sp.diff(Cs, xs) + 2*Ss)
check_sym("V68 C^2+S^2 = 1", Cs**2 + Ss**2 - 1)
# 7.3 carrier flow
Ps, Vs = sp.sin(2*xs)/4, sp.cos(2*xs)/2
check_sym("V69 T1 P' - V = 0", sp.diff(Ps, xs) - Vs)
check_sym("V70 T1 V' + 4P = 0", sp.diff(Vs, xs) + 4*Ps)
check_sym("V71 C1 P'' + 4P = 0", sp.diff(Ps, xs, 2) + 4*Ps)
check_sym("V72 C1 V'' + 4V = 0", sp.diff(Vs, xs, 2) + 4*Vs)
Es = Vs**2 + 4*Ps**2
check_sym("V73 T2 dE/dx = 0", sp.diff(Es, xs))
# 7.3.T3 Hamilton equations (P,V as symbols)
Pq, Vq = sp.symbols('P V')
Hh = Vq**2/2 + 2*Pq**2
check_sym("V74 T3 dH/dV = V", sp.diff(Hh, Vq) - Vq)
check_sym("V75 T3 -dH/dP = -4P", -sp.diff(Hh, Pq) + 4*Pq)
# 7.4 parent flow
Sigs = 2*(sp.cos(xs)/sp.sin(xs) + sp.sin(xs)/sp.cos(xs))
Dels = 2*(sp.cos(xs)/sp.sin(xs) - sp.sin(xs)/sp.cos(xs))
check_sym("V76 T4 Sig' + Sig*Del/2 = 0", sp.diff(Sigs, xs) + Sigs*Dels/2)
check_sym("V77 T4 Del' + Sig^2/2 = 0", sp.diff(Dels, xs) + Sigs**2/2)
check_sym("V78 C4 d(Sig^2-Del^2)/dx = 0", sp.diff(Sigs**2 - Dels**2, xs))
S7s, Q7s = 4/Sigs, Dels/Sigs
check_sym("V79 T5 S' - 2Q = 0", sp.diff(S7s, xs) - 2*Q7s)
check_sym("V80 T5 Q' + 2S = 0", sp.diff(Q7s, xs) + 2*S7s)
ws = sp.log(sp.cos(xs)/sp.sin(xs))     # cot > 0 chart
check_sym("V81 C8 w' + Sig/2 = 0 (cot>0 chart)", sp.diff(ws, xs) + Sigs/2)
Ls = sp.cos(xs)/sp.sin(xs)             # eps = +1 chart
check_sym("V82 C10 L' + (1+L^2) = 0 (eps=+1 chart)", sp.diff(Ls, xs) + (1+Ls**2))
# Riccati reproduces the rotation (eps=+1 chart)
Lr = sp.symbols('L')
Sr, Qr = 2*Lr/(Lr**2+1), (Lr**2-1)/(Lr**2+1)
Lp_rule = -(1+Lr**2)
check_sym("V83 C10 Riccati -> S' = 2Q", sp.diff(Sr, Lr)*Lp_rule - 2*Qr)
check_sym("V84 C10 Riccati -> Q' = -2S", sp.diff(Qr, Lr)*Lp_rule + 2*Sr)
# 7.4.E1 abstract flow
Sg, Dg = sp.symbols('Sg Dg')
check_sym("V85 E1 K' = 0 (abstract)", 2*Sg*(-Sg*Dg/2) - 2*Dg*(-Sg**2/2))
Kk = Sg**2 - Dg**2
Sp2 = -4*(-Sg*Dg/2)/Sg**2
Qp2 = ((-Sg**2/2)*Sg - Dg*(-Sg*Dg/2))/Sg**2
check_sym("V86 E1 S' = 2Q (abstract)", Sp2 - 2*Dg/Sg)
check_sym("V87 E1 Q' = -(K/8)S (abstract)", Qp2 + (Kk/8)*(4/Sg))
check_sym("V88 E1 conic Q^2+(K/16)S^2 = 1 (abstract)",
          (Dg/Sg)**2 + (Kk/16)*(4/Sg)**2 - 1)

print()
n_num = sum(1 for r in results if r[1] in ("NC", "CP"))
n_sym = sum(1 for r in results if r[1] == "SC")
n_cp = sum(1 for r in results if r[1] == "CP")
n_nc = sum(1 for r in results if r[1] == "NC")
worst = max((r for r in results if r[3] > 0), key=lambda r: r[2])
print(f"TOTAL: {len(results)} assertions "
      f"({n_cp} CP + {n_nc} NC numerical, {n_sym} SC symbolic), ALL PASSED.")
print(f"Worst-case measured error: [{worst[1]}] {worst[0]}: {worst[2]:.3e} "
      f"(tol {worst[3]:.0e}).")
print("No timeouts, no failures, no absorbed errors.")
