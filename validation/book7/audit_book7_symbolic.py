#!/usr/bin/env python3
"""Book 7 audit part 2 — exact symbolic verification of differential identities."""
import sympy as sp

x = sp.symbols('x', real=True)
fails = []

def check(name, expr):
    v = sp.simplify(expr)
    ok = (v == 0)
    print(("PASS " if ok else "FAIL ") + f"{name}: simplified={v}")
    if not ok:
        fails.append(name)

# 7.3 carrier
P = sp.sin(2*x)/4
V = sp.cos(2*x)/2
check("7.3.T1 P'-V=0", sp.diff(P, x) - V)
check("7.3.T1 V'+4P=0", sp.diff(V, x) + 4*P)
check("7.3.C1 P''+4P=0", sp.diff(P, x, 2) + 4*P)
check("7.3.C1 V''+4V=0", sp.diff(V, x, 2) + 4*V)
# E conserved: E=V^2+4P^2, dE/dx=0
E = V**2 + 4*P**2
check("7.3.T2 dE/dx=0", sp.simplify(sp.diff(E, x)))
# Hamilton: dH/dV=P', -dH/dP=V' with H=V^2/2+2P^2 (treat P,V as symbols)
Ps, Vs = sp.symbols('P V')
Hh = Vs**2/2 + 2*Ps**2
check("7.3.T3 dH/dV=V", sp.diff(Hh, Vs) - Vs)
check("7.3.T3 -dH/dP=-4P", -sp.diff(Hh, Ps) + 4*Ps)
# Lagrange: EL of L=(P')^2/2-2P^2 is P''+4P=0 (verified above)
# 7.4 parent: Sig=2(cot+tan), Del=2(cot-tan)
Sig = 2*(sp.cos(x)/sp.sin(x) + sp.sin(x)/sp.cos(x))
Del = 2*(sp.cos(x)/sp.sin(x) - sp.sin(x)/sp.cos(x))
check("7.4.T4 Sig'+Sig*Del/2=0", sp.simplify(sp.diff(Sig, x) + Sig*Del/2))
check("7.4.T4 Del'+Sig^2/2=0", sp.simplify(sp.diff(Del, x) + Sig**2/2))
# C4: d(Sig^2-Del^2)/dx=0
check("7.4.C4 d(Sig^2-Del^2)/dx=0",
      sp.simplify(sp.diff(Sig**2 - Del**2, x)))
# T5: S=4/Sig, Q=Del/Sig -> S'=2Q, Q'=-2S
S7, Q7 = 4/Sig, Del/Sig
check("7.4.T5 S'-2Q=0", sp.simplify(sp.diff(S7, x) - 2*Q7))
check("7.4.T5 Q'+2S=0", sp.simplify(sp.diff(Q7, x) + 2*S7))
# C8: w=ln|cot x| on chart where cot>0 (quadrant I); w'=-Sig/2
w = sp.log(sp.cos(x)/sp.sin(x))
check("7.4.C8 w'+Sig/2=0 (cot>0 chart)", sp.simplify(sp.diff(w, x) + Sig/2))
# C10: L=|cot x|=eps*cot x on quadrant; L'=-eps(1+L^2).
# Take principal chart eps=+1, L=cot x:
L = sp.cos(x)/sp.sin(x)
check("7.4.C10 L'+(1+L^2)=0 (eps=+1 chart)", sp.simplify(sp.diff(L, x) + (1+L**2)))
# Riccati reproduces S'=2Q: with S=2L/(L^2+1), Q=(L^2-1)/(L^2+1), L' = -(1+L^2)
# (eps=+1 chart), differentiate rational forms via chain rule
Ls = sp.symbols('L')
Sr = 2*Ls/(Ls**2+1); Qr = (Ls**2-1)/(Ls**2+1)
Lp_rule = -(1+Ls**2)
dS = sp.diff(Sr, Ls)*Lp_rule - 2*Qr
dQ = sp.diff(Qr, Ls)*Lp_rule + 2*Sr
check("7.4.C10 Riccati->S'=2Q", sp.simplify(dS))
check("7.4.C10 Riccati->Q'=-2S", sp.simplify(dQ))
# 7.1.C2: cos2x = 2 dH/dx with H=sin2x/4
H = sp.sin(2*x)/4
check("7.1.C2 cos2x-2H'=0", sp.simplify(sp.cos(2*x) - 2*sp.diff(H, x)))
# 7.1.T2 magnitude identity on principal branch:
# (1-2lam)^2*(1+4lam(1-lam)) = cos^2(2x), lam=(1+sin x-cos x)/2
lam = (1+sp.sin(x)-sp.cos(x))/2
check("7.1.T2 (1-2lam)^2(1+4lam(1-lam))=cos^2(2x)",
      sp.simplify((1-2*lam)**2*(1+4*lam*(1-lam)) - sp.cos(2*x)**2))
# sign: on (0,pi/4): 1-2lam>0 and cos2x>0; on (pi/4,pi/2): both <0.
# check sign agreement symbolically via trigsimp of (1-2lam)/cos(2x) >= 0:
# 1-2lam = cos x - sin x; (cos x - sin x)/cos(2x) = 1/(cos x + sin x)
check("7.1.T2 sign: (1-2lam)/cos2x = 1/(sin x+cos x)",
      sp.simplify((1-2*lam)/sp.cos(2*x) - 1/(sp.sin(x)+sp.cos(x))))
# 7.4.C9: eps=(-1)^k on quadrant k — numeric spot check done in part 1; skip here.
# E1: abstract flow conservation K'=0 with Sig'=-Sig*Del/2, Del'=-Sig^2/2 as symbols
Sg, Dg = sp.symbols('Sg Dg')
Kp = 2*Sg*(-Sg*Dg/2) - 2*Dg*(-Sg**2/2)
check("7.4.E1 K'=0 (abstract)", sp.simplify(Kp))
# projective: S=4/Sg, Q=Dg/Sg; S'=2Q; Q'=-(K/8)S with K=Sg^2-Dg^2
K = Sg**2 - Dg**2
Sp2 = -4*(-Sg*Dg/2)/Sg**2
Qp2 = ((-Sg**2/2)*Sg - Dg*(-Sg*Dg/2))/Sg**2
check("7.4.E1 S'=2Q (abstract)", sp.simplify(Sp2 - 2*Dg/Sg))
check("7.4.E1 Q'=-(K/8)S (abstract)", sp.simplify(Qp2 + (K/8)*(4/Sg)))
# conic: Q^2+(K/16)S^2=1
check("7.4.E1 conic (abstract)",
      sp.simplify((Dg/Sg)**2 + (K/16)*(4/Sg)**2 - 1))

print()
if fails:
    print(f"{len(fails)} FAILURES: {fails}")
else:
    print("ALL SYMBOLIC ASSERTIONS PASSED")
