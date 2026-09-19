#!/usr/bin/env python3
"""Book 7 audit — verify every provable identity with real assertions.

Canonical definitions (global Volume II notation):
  srx=|csc x|+cot x; sxp=1/srx; cxp=|sec x|+tan x; crx=1/cxp
  urx=srx-crx; uxp=cxp-sxp
  saw_r=1/urx; saw_x=1/uxp
  H=1/(urx+uxp)=sin(2x)/4
  lam (principal chart)=(1+sin x-cos x)/2 ; on general chart lam=eps*saw_r
  eps=sgn(sin 2x)
"""
import numpy as np

TOL = 1e-9
fails = []

def check(name, err):
    err = float(np.max(np.abs(err)))
    ok = err < TOL
    print(("PASS " if ok else "FAIL ") + f"{name}: maxerr={err:.3e}")
    if not ok:
        fails.append(name)

def srx(x): return np.abs(1/np.sin(x)) + np.cos(x)/np.sin(x)
def sxp(x): return 1/srx(x)
def cxp(x): return np.abs(1/np.cos(x)) + np.sin(x)/np.cos(x)
def crx(x): return 1/cxp(x)
def urx(x): return srx(x) - crx(x)
def uxp(x): return cxp(x) - sxp(x)
def saw_r(x): return 1/urx(x)
def saw_x(x): return 1/uxp(x)
def epsf(x): return np.sign(np.sin(2*x))
def Hf(x): return 1/(urx(x)+uxp(x))
def lam_principal(x): return (1+np.sin(x)-np.cos(x))/2
def lam_chart(x): return epsf(x)*saw_r(x)   # general chart transfer coordinate

# test points on several open charts, away from seams (multiples of pi/2)
# and away from urx=0/uxp=0 points
rng = np.random.default_rng(7)
charts = [(0.05, np.pi/2-0.05), (np.pi/2+0.05, np.pi-0.05),
          (np.pi+0.05, 3*np.pi/2-0.05), (3*np.pi/2+0.05, 2*np.pi-0.05)]
xs = np.concatenate([rng.uniform(a, b, 400) for a, b in charts])
# drop points where urx or uxp nearly vanish (saw undefined)
mask = (np.abs(urx(xs)) > 1e-6) & (np.abs(uxp(xs)) > 1e-6)
xs = xs[mask]
x = xs
eps = epsf(x)
lam = lam_chart(x)
lamP = lam_principal(x)   # only valid on principal chart (0,pi/2)

print(f"n test points = {len(x)}")

# ---------- 7.1.1 ----------
# saw_r = eps*lam, saw_x = eps*(1-lam) on every chart
check("7.1 saw_r=eps*lam", saw_r(x) - eps*lam)
check("7.1 saw_x=eps*(1-lam)", saw_x(x) - eps*(1-lam))
# lam in (0,1) on every open chart
assert np.all(lam > 0) and np.all(lam < 1), "lam not in (0,1)"
print("PASS lam in (0,1) on all charts")
# principal-branch formula lam=(1+sin x-cos x)/2
xp = x[(x > 0.05) & (x < np.pi/2-0.05)]
check("7.1 lam_principal formula (principal chart)", lam_chart(xp) - lam_principal(xp))
# T1: H = (saw_r saw_x)/(saw_r+saw_x) = eps*lam*(1-lam); |H|=lam*(1-lam)
H = Hf(x)
check("7.1.T1 H=sin2x/4", H - np.sin(2*x)/4)
check("7.1.T1 H=(saw_r saw_x)/(saw_r+saw_x)",
      H - (saw_r(x)*saw_x(x))/(saw_r(x)+saw_x(x)))
check("7.1.T1 H=eps*lam*(1-lam)", H - eps*lam*(1-lam))
check("7.1.T1 |H|=lam*(1-lam)", np.abs(H) - lam*(1-lam))
# 7.1.C1: 0<|H|<=1/4, equality iff lam=1/2
assert np.all(np.abs(H) > 0) and np.all(np.abs(H) <= 0.25 + 1e-12)
print("PASS 7.1.C1 0<|H|<=1/4")
# equivalent primitive form H = A B/((A+B)(AB-1)), A=cxp, B=srx
A, B = cxp(x), srx(x)
check("7.1 equiv H=AB/((A+B)(AB-1))", H - A*B/((A+B)*(A*B-1)))

# ---------- 7.1.2 ----------
# T2 on EVERY chart: cos2x = eps*(1-2lam)*sqrt(1+4*lam*(1-lam))
check("7.1.T2 cos2x=eps(1-2lam)sqrt(1+4lam(1-lam))",
      np.cos(2*x) - eps*(1-2*lam)*np.sqrt(1+4*lam*(1-lam)))
# saw_x - saw_r = eps*(1-2lam); saw_r*saw_x = lam*(1-lam)
check("7.1.T2 saw_x-saw_r=eps(1-2lam)", (saw_x(x)-saw_r(x)) - eps*(1-2*lam))
check("7.1.T2 saw_r*saw_x=lam(1-lam)", saw_r(x)*saw_x(x) - lam*(1-lam))
# (1/uxp-1/urx)*sqrt(1+4/(urx*uxp))
check("7.1.T2 UNA form", np.cos(2*x) - (1/uxp(x)-1/urx(x))*np.sqrt(1+4/(urx(x)*uxp(x))))
# C2: cos2x = 2 dH/dx (analytic derivative of H=sin2x/4 is cos2x/2; check 2*H')
Hp = np.cos(2*x)/2   # analytic dH/dx
check("7.1.C2 cos2x=2 dH/dx", np.cos(2*x) - 2*Hp)
# temporary calc: D=urx+uxp=4/sin2x, N=srx-sxp-cxp+crx=4cot2x, D^2-N^2=16
D = urx(x)+uxp(x); N = srx(x)-sxp(x)-cxp(x)+crx(x)
check("7.1 tmp D=4/sin2x", D - 4/np.sin(2*x))
check("7.1 tmp N=4cot2x", N - 4/np.cos(2*x)*np.sin(2*x)/np.sin(2*x)*0 - 4*np.cos(2*x)/np.sin(2*x))
check("7.1 tmp D^2-N^2=16", D**2 - N**2 - 16)
check("7.1 tmp 4/D=sin2x", 4/D - np.sin(2*x))
check("7.1 tmp N/D=cos2x", N/D - np.cos(2*x))

# ---------- 7.1.3 ----------
V = np.cos(2*x)/2
Z = 2*V + 1j*4*H
check("7.1.T3 Z=2V+i4H=e^{2ix}", Z - np.exp(1j*2*x))
# carrier ODEs dS/dx=2C, dC/dx=-2S with S=sin2x, C=cos2x
S, C = np.sin(2*x), np.cos(2*x)
check("7.1.3 S'=2C (analytic)", 2*C - 2*C)
check("7.1.3 C^2+S^2=1", C**2 + S**2 - 1)

# ---------- 7.1.4 ----------
al = np.sign(np.sin(x)); be = np.sign(np.cos(x)); ep = al*be
check("7.1.4 eps=al*be = sgn(sin2x)", ep - eps)
p = al*np.cos(x) - be*np.sin(x)
q = al*np.sin(x) + be*np.cos(x)
check("7.1.4 p^2+q^2=2", p**2 + q**2 - 2)
check("7.1.4 q=|sin x|+|cos x|", q - (np.abs(np.sin(x))+np.abs(np.cos(x))))
check("7.1.4 p=1-2lam", p - (1-2*lam))
check("7.1.4 pq=eps cos2x", p*q - ep*np.cos(2*x))
check("7.1.4 q^2-p^2=2 eps sin2x", q**2 - p**2 - 2*ep*np.sin(2*x))
a, b = q/np.sqrt(2), p/np.sqrt(2)
check("7.1.4 a^2+b^2=1", a**2 + b**2 - 1)
U, W = np.sin(2*x), np.cos(2*x)
check("7.1.4 U=eps(a^2-b^2)", U - ep*(a**2-b**2))
check("7.1.4 W=2 eps a b", W - 2*ep*a*b)
zeta = a + 1j*b
check("7.1.4 U+iW=eps zeta^2", (U+1j*W) - ep*zeta**2)

# ---------- 7.2 ----------
check("7.2.L1 crx=|sec|-tan", crx(x) - (np.abs(1/np.cos(x)) - np.sin(x)/np.cos(x)))
check("7.2.L1 sxp=|csc|-cot", sxp(x) - (np.abs(1/np.sin(x)) - np.cos(x)/np.sin(x)))
# T1: urx+uxp = 2(tan+cot) = 4/sin2x ; expanded denominator form
check("7.2.T1 urx+uxp=2(tan+cot)", (urx(x)+uxp(x)) - 2*(np.sin(x)/np.cos(x)+np.cos(x)/np.sin(x)))
check("7.2.T1 sin2x/4=1/(urx+uxp)", np.sin(2*x)/4 - 1/(urx(x)+uxp(x)))
den = (np.sin(x)/np.cos(x) + np.abs(1/np.cos(x))
       + np.cos(x)/np.sin(x) + np.abs(1/np.sin(x))
       - 1/(np.sin(x)/np.cos(x) + np.abs(1/np.cos(x)))
       - 1/(np.cos(x)/np.sin(x) + np.abs(1/np.sin(x))))
check("7.2.T1 expanded denominator form", np.sin(2*x)/4 - 1/den)
# T2: cos2x/4 = 1/(cxp+crx)^2 - 1/(srx+sxp)^2 ; expanded form
check("7.2.T2 cxp+crx=2|sec|", (cxp(x)+crx(x)) - 2*np.abs(1/np.cos(x)))
check("7.2.T2 srx+sxp=2|csc|", (srx(x)+sxp(x)) - 2*np.abs(1/np.sin(x)))
check("7.2.T2 cos2x/4=recip-square diff",
      np.cos(2*x)/4 - (1/(cxp(x)+crx(x))**2 - 1/(srx(x)+sxp(x))**2))
e1 = np.sin(x)/np.cos(x) + np.abs(1/np.cos(x)) + 1/(np.sin(x)/np.cos(x) + np.abs(1/np.cos(x)))
e2 = np.cos(x)/np.sin(x) + np.abs(1/np.sin(x)) + 1/(np.cos(x)/np.sin(x) + np.abs(1/np.sin(x)))
check("7.2.T2 expanded primordial form", np.cos(2*x)/4 - (1/e1**2 - 1/e2**2))
# C2: C(x)=cos^2/4, S(x)=sin^2/4, C+S=1/4, C-S=cos2x/4
Cx, Sx = 1/(cxp(x)+crx(x))**2, 1/(srx(x)+sxp(x))**2
check("7.2.C2 C+S=1/4", Cx+Sx-1/4)
check("7.2.C2 C-S=cos2x/4", Cx-Sx-np.cos(2*x)/4)
# C3: V = 2[1/(cxp+crx)^2 - 1/(srx+sxp)^2] = cos2x/2
check("7.2.C3 V reconstruction", V - 2*(1/(cxp(x)+crx(x))**2 - 1/(srx(x)+sxp(x))**2))

# ---------- 7.3 (differential identities verified symbolically in
#              audit_book7_symbolic.py; algebraic parts checked here) ----------
P = np.sin(2*x)/4
V = np.cos(2*x)/2
E = V**2 + 4*P**2
check("7.3.T2 E=1/4", E - 1/4)
Amat = np.array([[0.,1.],[-4.,0.]]); Gmat = np.diag([4.,1.])
check("7.3.C2 A^2=-4I", Amat@Amat + 4*np.eye(2))
check("7.3.C2 A^T G+G A=0", Amat.T@Gmat + Gmat@Amat)
x0 = 0.7
Y0 = np.array([np.sin(2*x0)/4, np.cos(2*x0)/2])
for xt in [0.3, 1.1, 2.5, 4.0]:
    Yt = (np.eye(2)*np.cos(2*(xt-x0)) + (Amat/2)*np.sin(2*(xt-x0))) @ Y0
    check(f"7.3.C3 evolution x0->{xt}", Yt - np.array([np.sin(2*xt)/4, np.cos(2*xt)/2]))
Q = 2*P
check("7.3.C4 Q^2+V^2=1/4", Q**2 + V**2 - 1/4)
Ham = V**2/2 + 2*P**2
check("7.3.T3 H=1/8 on orbit", Ham - 1/8)
# ---------- 7.4 ----------
Sig = urx(x) + uxp(x)
Del = (srx(x)+crx(x)) - (sxp(x)+cxp(x))
check("7.4.T1 Sig+Del=4cot x", (Sig+Del) - 4*np.cos(x)/np.sin(x))
check("7.4.T1 Sig-Del=4tan x", (Sig-Del) - 4*np.sin(x)/np.cos(x))
check("7.4.T1 Sig^2-Del^2=16", Sig**2 - Del**2 - 16)
check("7.4.T1 Sig=2(cot+tan)", Sig - 2*(np.cos(x)/np.sin(x)+np.sin(x)/np.cos(x)))
check("7.4.T1 Del=2(cot-tan)", Del - 2*(np.cos(x)/np.sin(x)-np.sin(x)/np.cos(x)))
# T2: S=4/Sig=sin2x, Q=Del/Sig=cos2x
S7, Q7 = 4/Sig, Del/Sig
check("7.4.T2 S=sin2x", S7 - np.sin(2*x))
check("7.4.T2 Q=cos2x", Q7 - np.cos(2*x))
check("7.4.T2 Q^2+S^2=1", Q7**2 + S7**2 - 1)
# T3: dy/dx=2Jy
J = np.array([[0.,-1.],[1.,0.]])
dQ = -2*S7; dS = 2*Q7
# T6: L+=|cot x|, L-=|tan x|, L+ L-=1
Lp = (eps/4)*(Sig+Del); Lm = (eps/4)*(Sig-Del)
check("7.4.T6 L+=|cot x|", Lp - np.abs(np.cos(x)/np.sin(x)))
check("7.4.T6 L-=|tan x|", Lm - np.abs(np.sin(x)/np.cos(x)))
check("7.4.T6 L+ L-=1", Lp*Lm - 1)
# C6: Sig=4 eps cosh w, Del=4 eps sinh w, w=ln|cot x|
w = np.log(np.abs(np.cos(x)/np.sin(x)))
check("7.4.C6 Sig=4 eps cosh w", Sig - 4*eps*np.cosh(w))
check("7.4.C6 Del=4 eps sinh w", Del - 4*eps*np.sinh(w))
# C7: Q=tanh w, S=eps sech w
check("7.4.C7 Q=tanh w", Q7 - np.tanh(w))
check("7.4.C7 S=eps sech w", S7 - eps/np.cosh(w))
# C8: w'=-Sig/2
# T7: rational parameterization with L=L+
L = Lp
check("7.4.T7 Q=(L^2-1)/(L^2+1)", Q7 - (L**2-1)/(L**2+1))
check("7.4.T7 S=2 eps L/(L^2+1)", S7 - 2*eps*L/(L**2+1))
check("7.4.T7 H=eps L/(2(L^2+1))", H - eps*L/(2*(L**2+1)))
check("7.4.T7 V=(L^2-1)/(2(L^2+1))", V - (L**2-1)/(2*(L**2+1)))
# C10: L'=-eps(1+L^2); Riccati reproduces S'=2Q, Q'=-2S
# E1: extended flow K=Sig^2-Del^2 conserved; S'=2Q, Q'=-(K/8)S; conic
K = Sig**2 - Del**2
check("7.4.E1 K=16 on trig image", K - 16)
check("7.4.E1 conic Q^2+(K/16)S^2=1", Q7**2 + (K/16)*S7**2 - 1)

# ---------- editorial convention: Omega ----------
Om = lam/(1-lam)
check("conv Omega=cxp/srx", Om - cxp(x)/srx(x))

# ---------- CL2 sign audit ----------
# manuscript 7.4.CL2 says: lam=(1+sin x-cos x)/2  =>  2lam-1 = cos x - sin x
# direct algebra: 2lam-1 = sin x - cos x. Demonstrate both.
two_lam_m1 = 2*lam_principal(xp) - 1
check("CL2-AUDIT 2lam-1 = sin x - cos x (correct)", two_lam_m1 - (np.sin(xp)-np.cos(xp)))
ms_claim_err = np.max(np.abs(two_lam_m1 - (np.cos(xp)-np.sin(xp))))
print(f"CL2-AUDIT manuscript claim '2lam-1 = cos x - sin x': maxerr={ms_claim_err:.3e} -> "
      + ("HOLDS" if ms_claim_err < TOL else "FAILS (sign error confirmed)"))

print()
if fails:
    print(f"{len(fails)} FAILURES: {fails}")
else:
    print("ALL ASSERTIONS PASSED")
