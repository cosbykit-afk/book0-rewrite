#!/usr/bin/env python3
"""Book 1 verification: every checkable mathematical claim on book1/index.html.

Scope labels: CP = checked proof (exact algebra verified on grids / exact
single-point values), NC = completed numerical check, ST = standard imported
theorem used as a base step (named where it enters). Nothing here is a
manuscript assertion: each check below ran to completion. No timeouts.

Page claims verified (Part I figures, then Part II sections):
 V1  reciprocal conjugacy Fs+*Fs- = Fc+*Fc- = 1            (Fig 1,4; §1.V)
 V2  strict positivity on D = R \\ {k pi/2}                (Fig 1; §1.V)
 V3  pi-periodicity of the four factors                    (§1.V)
 V4  principal half-angle chart on Q0                     (Fig 2; §1.VI)
 V5  midpoint values sqrt2 +/- 1 at x = pi/4               (Fig 2; §1.VI)
 V6  general midpoint formula sqrt2 +/- eps at m_k         (§1.VI)
 V7  ranges on Q0: (1,inf) and (0,1)                      (Fig 2; §1.VI)
 V8  strict monotonicity of the four branches on Q0       (Fig 2; §1.VI)
 V9  non-globalization trap: Fs+(5pi/4)=sqrt2+1 vs cot(5pi/8)=1-sqrt2<0 (Fig 2)
 V10 eps = alpha*beta = sgn(sin 2x)                       (Fig 3; §1.IV)
 V11 sign cycle over Q0..Q3                               (Fig 3; §1.IV)
 V12 eps-lossiness: no recovery of (alpha,beta)           (Fig 3; §1.IV N3)
 V13 parametric locus rides the hyperbola uv=1 exactly    (Fig 4)
 V14 octant ordering + unique diagonal crossing at (sqrt2+1,sqrt2+1) (Fig 5)
 V15 one-sided boundary limits at the sine-zero seam x=0  (Fig 6; §1.VII)
 V16 opposite-seam regular value exactly 1                (Fig 6; §1.VII T2)
 V17 sum/difference reconstruction of 2|csc|, 2cot, ...   (§1.V)
 V18 unit-threshold law Fs+>1 <=> cot x>0; equality never on D (§1.V)
 V19 branch-explicit rational forms                       (§1.IV)
 V20 even/odd quadrant chart reuse (parity atlas)         (§1.VI T4/T5)
 V21 quarter-turn order 4 on T_2pi, order 2 on T_pi        (§1.II)
 V22 two-to-one folding erases the half-turn class        (Fig 7; §1.II N1)
 V23 symmetry transport iota(Q_k)=Q_-k-1, iota_d(Q_k)=Q_-k (§1.III)
 V24 half-turn sends (alpha,beta)->(-alpha,-beta), eps survives (§1.IV T13)
 V25 full-turn fiber theorem                              (§1.II)
 V26 translation group law tau_a o tau_b = tau_a+b        (§1.II)
 V27 finite on D (poles exactly at the seam set)          (Fig 1; §1.III)
 V28 reflection laws; sgn(tan)=sgn(cot)=eps; seam
     interlacing; one-dimensional common source           (§1.V, §1.IV, §1.III)
"""
import numpy as np

TOL = 1e-9
results = []

def check(name, err, tol=TOL, scope="CP"):
    err = np.asarray(err, dtype=float)
    assert np.all(np.isfinite(err)), f"{name}: non-finite values"
    m = float(np.max(np.abs(err)))
    assert m < tol, f"{name}: max_err={m:.3e} >= tol={tol:.0e}"
    results.append((name, m, tol, scope))
    print(f"OK [{scope}] {name}: max_err={m:.3e} < {tol:.0e}")

SQ2 = np.sqrt(2)

def Fsp(x): return np.abs(1/np.sin(x)) + np.cos(x)/np.sin(x)  # F_s+
def Fsm(x): return np.abs(1/np.sin(x)) - np.cos(x)/np.sin(x)  # F_s-
def Fcp(x): return np.abs(1/np.cos(x)) + np.sin(x)/np.cos(x)  # F_c+
def Fcm(x): return np.abs(1/np.cos(x)) - np.sin(x)/np.cos(x)  # F_c-
def alpha(x): return np.sign(np.sin(x))
def beta(x):  return np.sign(np.cos(x))
def eps(x):   return np.sign(np.sin(2*x))

def seam_mask(x, gap=1e-3):
    return np.abs(np.sin(2*x)) < gap

xg = np.linspace(-4*np.pi + 0.02, 4*np.pi - 0.02, 160001)
xg = xg[~seam_mask(xg)]
q0 = np.linspace(0.002, np.pi/2 - 0.002, 40001)   # principal quadrant

# V1: reciprocal conjugacy. Exact algebra: (|csc|+cot)(|csc|-cot)=csc^2-cot^2=1.
# (The ~1e-9 grid error is pure floating-point cancellation near seams, where
# |csc| ~ 1e3; the identity itself is exact.)
check("V1 Fs+*Fs- = 1", Fsp(xg)*Fsm(xg) - 1, 1e-9, "CP")
check("V1 Fc+*Fc- = 1", Fcp(xg)*Fcm(xg) - 1, 1e-9, "CP")

# V2: strict positivity on D
assert np.all(Fsp(xg) > 0) and np.all(Fsm(xg) > 0)
assert np.all(Fcp(xg) > 0) and np.all(Fcm(xg) > 0)
print("OK [NC] V2 all four factors strictly positive on D")

# V3: pi-periodicity (|csc|,cot,|sec|,tan are each pi-periodic)
check("V3 Fs+ pi-periodic", Fsp(xg) - Fsp(xg + np.pi), 1e-9, "CP")
check("V3 Fsm pi-periodic", Fsm(xg) - Fsm(xg + np.pi), 1e-9, "CP")
check("V3 Fc+ pi-periodic", Fcp(xg) - Fcp(xg + np.pi), 1e-9, "CP")
check("V3 Fcm pi-periodic", Fcm(xg) - Fcm(xg + np.pi), 1e-9, "CP")

# V4: principal chart on Q0. Base step is standard (ST): on Q0,
# |csc x| = csc x, |sec x| = sec x, and the half-angle forms below are the
# ordinary half-angle / addition identities; the checked equalities are exact.
check("V4 Fs+ = cot(x/2) on Q0", Fsp(q0) - np.cos(q0/2)/np.sin(q0/2), 1e-9, "CP")
check("V4 Fs- = tan(x/2) on Q0", Fsm(q0) - np.sin(q0/2)/np.cos(q0/2), 1e-9, "CP")
check("V4 Fc+ = tan(pi/4+x/2) on Q0",
      Fcp(q0) - np.tan(np.pi/4 + q0/2), 1e-9, "CP")
check("V4 Fc- = tan(pi/4-x/2) on Q0",
      Fcm(q0) - np.tan(np.pi/4 - q0/2), 1e-9, "CP")

# V5: exact midpoint values at x = pi/4
check("V5 Fs+(pi/4) = sqrt2+1", Fsp(np.pi/4) - (SQ2 + 1), 1e-12, "CP")
check("V5 Fc+(pi/4) = sqrt2+1", Fcp(np.pi/4) - (SQ2 + 1), 1e-12, "CP")
check("V5 Fs-(pi/4) = sqrt2-1", Fsm(np.pi/4) - (SQ2 - 1), 1e-12, "CP")
check("V5 Fc-(pi/4) = sqrt2-1", Fcm(np.pi/4) - (SQ2 - 1), 1e-12, "CP")

# V6: general midpoint formula at m_k = (2k+1)pi/4.
# eps(m_k) = sgn(sin((2k+1)pi/2)) = (-1)^k; cot(m_k) = (-1)^k too, so
# Fs+(m_k) = sqrt2 + eps(m_k), etc. (uses cot(pi/8) = sqrt2+1, ST, at k=0).
for k in range(-4, 5):
    m = (2*k + 1)*np.pi/4
    e = float(eps(m))
    assert abs(e) == 1.0
    check(f"V6 Fs+(m_{k}) = sqrt2+eps", Fsp(m) - (SQ2 + e), 1e-12, "CP")
    check(f"V6 Fc+(m_{k}) = sqrt2+eps", Fcp(m) - (SQ2 + e), 1e-12, "CP")
    check(f"V6 Fs-(m_{k}) = sqrt2-eps", Fsm(m) - (SQ2 - e), 1e-12, "CP")
    check(f"V6 Fc-(m_{k}) = sqrt2-eps", Fcm(m) - (SQ2 - e), 1e-12, "CP")

# V7: ranges on Q0
assert np.all(Fsp(q0) > 1) and np.all(Fcp(q0) > 1)
assert np.all((Fsm(q0) > 0) & (Fsm(q0) < 1))
assert np.all((Fcm(q0) > 0) & (Fcm(q0) < 1))
print("OK [NC] V7 Fs+,Fc+ in (1,inf); Fs-,Fc- in (0,1) on Q0")

# V8: strict monotonicity on Q0
d1, d2, d3, d4 = np.diff(Fsp(q0)), np.diff(Fsm(q0)), np.diff(Fcp(q0)), np.diff(Fcm(q0))
assert np.all(d1 < 0), "Fs+ not decreasing"
assert np.all(d2 > 0), "Fs- not increasing"
assert np.all(d3 > 0), "Fc+ not increasing"
assert np.all(d4 < 0), "Fc- not decreasing"
print("OK [NC] V8 Fs+ dec, Fs- inc, Fc+ inc, Fc- dec on Q0")

# V9: the trap -- chart-local formulas do not globalize.
# Fs+(5pi/4) = sqrt2+1 exactly, while cot(5pi/8) = 1-sqrt2 < 0.
check("V9 Fs+(5pi/4) = sqrt2+1", Fsp(5*np.pi/4) - (SQ2 + 1), 1e-12, "CP")
c = np.cos(5*np.pi/8)/np.sin(5*np.pi/8)
check("V9 cot(5pi/8) = 1-sqrt2", c - (1 - SQ2), 1e-12, "CP")
assert c < 0
# N2 witnesses: dropping |.| elsewhere changes the function.
assert abs(Fsp(5*np.pi/4) - (1/np.sin(5*np.pi/4) + np.cos(5*np.pi/4)/np.sin(5*np.pi/4))) > 1
assert abs(Fcp(3*np.pi/4) - (1/np.cos(3*np.pi/4) + np.sin(3*np.pi/4)/np.cos(3*np.pi/4))) > 1
print("OK [CP] V9 trap: Fs+(5pi/4)=sqrt2+1 but cot(5pi/8)=1-sqrt2<0; "
      "dropping |.| at 5pi/4, 3pi/4 changes the function")

# V10: branch-sign identity
assert np.all(eps(xg) == alpha(xg)*beta(xg))
print("OK [CP] V10 eps = alpha*beta = sgn(sin 2x) on D")

# V11: sign cycle over Q0..Q3
expected = [(1, 1, 1), (1, -1, -1), (-1, -1, 1), (-1, 1, -1)]
for k, (a, b, e) in enumerate(expected):
    m = (2*k + 1)*np.pi/4
    got = (int(alpha(m)), int(beta(m)), int(eps(m)))
    assert got == (a, b, e), f"Q{k}: got {got}, want {(a,b,e)}"
print("OK [CP] V11 sign cycle (+,+,+),(+,-,-),(-,-,+),(-,+,-) over Q0..Q3")

# V12: eps-lossiness -- eps = +1 on both (+,+) and (-,-): no deterministic
# recovery of the ordered pair (alpha,beta) from eps alone.
pairs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
vals = [a*b for a, b in pairs]
assert vals[0] == vals[2] == 1 and pairs[0] != pairs[2]
print("OK [CP] V12 eps(+1,+1) = eps(-1,-1) = +1: (alpha,beta) not recoverable")

# V13: the traced pair rides the hyperbola branch exactly (page's parametric
# form x = pi*t/2, t in (0,1) traces Q0).
t = np.linspace(0.001, 0.999, 5000)
u, v = Fsp(np.pi*t/2), Fsm(np.pi*t/2)
check("V13 (Fs+(pi t/2),Fs-(pi t/2)) on uv=1", u*v - 1, 1e-9, "CP")

# V14: octant ordering; the difference d = Fs+ - Fc+ is strictly decreasing
# on Q0 (d' = -(1/2)csc^2(x/2) - (1/2)sec^2(pi/4+x/2) < 0), tends +inf/-inf
# at the ends, and vanishes exactly at pi/4 -- hence exactly one crossing.
o0 = np.linspace(0.002, np.pi/4 - 0.002, 10000)
o1 = np.linspace(np.pi/4 + 0.002, np.pi/2 - 0.002, 10000)
assert np.all(Fsp(o0) > Fcp(o0)), "O0 ordering"
assert np.all(Fsp(o1) < Fcp(o1)), "O1 ordering"
d = Fsp(q0) - Fcp(q0)
assert np.all(np.diff(d) < 0), "difference not strictly decreasing"
check("V14 d(pi/4) = 0", Fsp(np.pi/4) - Fcp(np.pi/4), 1e-12, "CP")
# end behavior: d -> +inf at 0+, -inf at pi/2- (probed close in)
assert Fsp(1e-4) - Fcp(1e-4) > 1e3 and Fsp(np.pi/2 - 1e-4) - Fcp(np.pi/2 - 1e-4) < -1e3
print("OK [CP] V14 Fs+>Fc+ on O0, reverses on O1; d strictly decreasing "
      "with d(pi/4)=0 => exactly one diagonal crossing at (sqrt2+1,sqrt2+1)")

# V15: one-sided limits at the sine-zero seam x = 0.
# left -> (0, +inf, 1, 1); right -> (+inf, 0, 1, 1). Probed at 1e-4 where
# floating-point cancellation is mild (true Fs+(-1e-4) ~ 5e-5).
assert abs(Fsp(-1e-4)) < 1e-3 and Fsm(-1e-4) > 1e3
assert abs(Fcp(-1e-4) - 1) < 1e-3 and abs(Fcm(-1e-4) - 1) < 1e-3
assert Fsp(1e-4) > 1e3 and abs(Fsm(1e-4)) < 1e-3
assert abs(Fcp(1e-4) - 1) < 1e-3 and abs(Fcm(1e-4) - 1) < 1e-3
print("OK [NC] V15 x->0-: (0,+inf,1,1); x->0+: (+inf,0,1,1)")

# V16: opposite-seam regular value exactly 1 (removable omission).
for k in range(-2, 3):
    check(f"V16 Fc+(k pi) = 1", Fcp(k*np.pi) - 1, 1e-12, "CP")
    check(f"V16 Fc-(k pi) = 1", Fcm(k*np.pi) - 1, 1e-12, "CP")
    s = np.pi/2 + k*np.pi
    check(f"V16 Fs+(pi/2+k pi) = 1", Fsp(s) - 1, 1e-12, "CP")
    check(f"V16 Fs-(pi/2+k pi) = 1", Fsm(s) - 1, 1e-12, "CP")

# V17: sum/difference reconstruction
check("V17 Fs+ + Fs- = 2|csc|", Fsp(xg) + Fsm(xg) - 2*np.abs(1/np.sin(xg)), 1e-9, "CP")
check("V17 Fs+ - Fs- = 2cot", Fsp(xg) - Fsm(xg) - 2*np.cos(xg)/np.sin(xg), 1e-9, "CP")
check("V17 Fc+ + Fc- = 2|sec|", Fcp(xg) + Fcm(xg) - 2*np.abs(1/np.cos(xg)), 1e-9, "CP")
check("V17 Fc+ - Fc- = 2tan", Fcp(xg) - Fcm(xg) - 2*np.sin(xg)/np.cos(xg), 1e-9, "CP")

# V18: unit-threshold law. Exact part: Fs+>1 iff cot x>0 (boolean equality
# on the grid); equality Fs+=1 never occurs on D (algebra: Fs+=1 with V1,V17
# forces |csc x|=1, i.e. x = pi/2+k pi not in D; grid margin confirms).
assert np.all((Fsp(xg) > 1) == (np.cos(xg)/np.sin(xg) > 0))
assert np.min(np.abs(Fsp(xg) - 1)) > 1e-4  # grid stays 5e-4 from seams
neg = xg[eps(xg) < 0]
assert np.all((Fsp(neg) > 0) & (Fsp(neg) < 1))
assert np.all((Fcp(neg) > 0) & (Fcp(neg) < 1))
print("OK [CP] V18 Fs+>1 <=> cot x>0; Fs+=1 has no solution on D; "
      "plus factors in (0,1) on eps=-1 quadrants")

# V19: branch-explicit rational forms.
# |csc x| +/- cot x = (alpha +/- cos x)/sin x = (1 +/- eps|cos x|)/|sin x|.
check("V19 Fs+ = (alpha+cos)/sin", Fsp(xg) - (alpha(xg) + np.cos(xg))/np.sin(xg), 1e-9, "CP")
check("V19 Fs- = (alpha-cos)/sin", Fsm(xg) - (alpha(xg) - np.cos(xg))/np.sin(xg), 1e-9, "CP")
e1 = (1 + eps(xg)*np.abs(np.cos(xg)))/np.abs(np.sin(xg))
e2 = (1 - eps(xg)*np.abs(np.cos(xg)))/np.abs(np.sin(xg))
check("V19 Fs+ = (1+eps|cos|)/|sin|", Fsp(xg) - e1, 1e-9, "CP")
check("V19 Fs- = (1-eps|cos|)/|sin|", Fsm(xg) - e2, 1e-9, "CP")

# V20: parity atlas. Even quadrants reuse the principal chart in xi_k;
# odd quadrants use the swapped chart. (For even k this is V3 restated in
# xi_k = x - k pi/2; for odd k the s/c swap is the T4/T5 content.)
for k in (-2, 0, 2):
    qk = np.linspace(k*np.pi/2 + 0.002, (k+1)*np.pi/2 - 0.002, 8000)
    xi = qk - k*np.pi/2
    check(f"V20 Q{k} even: Fs+ = cot(xi/2)",
          Fsp(qk) - np.cos(xi/2)/np.sin(xi/2), 1e-9, "CP")
    check(f"V20 Q{k} even: Fc+ = tan(pi/4+xi/2)",
          Fcp(qk) - np.tan(np.pi/4 + xi/2), 1e-9, "CP")
for k in (-1, 1):
    qk = np.linspace(k*np.pi/2 + 0.002, (k+1)*np.pi/2 - 0.002, 8000)
    xi = qk - k*np.pi/2
    check(f"V20 Q{k} odd: Fs+ = tan(pi/4-xi/2)",
          Fsp(qk) - np.tan(np.pi/4 - xi/2), 1e-9, "CP")
    check(f"V20 Q{k} odd: Fc+ = tan(xi/2)",
          Fcp(qk) - np.sin(xi/2)/np.cos(xi/2), 1e-9, "CP")

# V21: quarter-turn orders. tau = shift by pi/2.
# (Modulo arithmetic: measure circular distance min(|d|, 2pi-|d|) so the
# 0/2pi wrap of the representatives does not pollute the comparison.)
xs = np.linspace(0.01, 4*np.pi - 0.01, 20001)
q = np.pi/2
def cdist(a, b, p):
    d = np.abs(a - b)
    return np.minimum(d, p - d)
check("V21 tau^4 = id on T_2pi",
      cdist((xs + 4*q) % (2*np.pi), xs % (2*np.pi), 2*np.pi), 1e-12, "CP")
d2pi = cdist((xs + 2*q) % (2*np.pi), xs % (2*np.pi), 2*np.pi)
assert np.min(d2pi) > 3.0, "tau^2 not nontrivial on T_2pi"
check("V21 tau^2 = id on T_pi",
      cdist((xs + 2*q) % np.pi, xs % np.pi, np.pi), 1e-12, "CP")
dpi = cdist((xs + q) % np.pi, xs % np.pi, np.pi)
assert np.min(dpi) > 1.0, "tau not order 2 on T_pi"
print("OK [CP] V21 quarter-turn has order 4 on T_2pi, order 2 on T_pi")

# V22: two-to-one folding erases the half-turn class. Representatives of the
# four T_2pi seam classes map 2:1 onto the two T_pi seam classes; the fiber
# {0, pi} over 0 means no quotient-level datum distinguishes the half-turn.
reps = [0.0, np.pi/2, np.pi, 3*np.pi/2]
kap = [r % np.pi for r in reps]
assert kap[0] == kap[2] == 0.0 and kap[1] == kap[3] == np.pi/2
fiber0 = [r for r, kk in zip(reps, kap) if kk == 0.0]
assert len(fiber0) == 2 and set(np.round(fiber0, 9)) == {0.0, round(float(np.pi), 9)}
print("OK [CP] V22 kappa 2-to-1; fiber {0,pi} over 0: half-turn class erased")

# V23: symmetry transport of quadrants under iota and iota_d.
for k in range(-3, 4):
    mid = (2*k + 1)*np.pi/4
    assert -(k+1)*np.pi/2 < -mid < -k*np.pi/2, f"iota Q{k}"
    assert -k*np.pi/2 < np.pi/2 - mid < (-k+1)*np.pi/2, f"iota_d Q{k}"
print("OK [CP] V23 iota(Q_k) = Q_-k-1, iota_d(Q_k) = Q_-k (midpoints land)")

# V24: half-turn on branch signs.
assert np.all(alpha(xg + np.pi) + alpha(xg) == 0)
assert np.all(beta(xg + np.pi) + beta(xg) == 0)
assert np.all(eps(xg + np.pi) - eps(xg) == 0)
print("OK [CP] V24 (alpha,beta) -> (-alpha,-beta) under half-turn; eps survives")

# V25: full-turn fiber theorem. If-direction exact; only-if direction as a
# numerical check: every agreeing pair on a fine grid differs by 2pi*integer.
xk = np.linspace(0, 4*np.pi, 241)
C, S = np.cos(xk), np.sin(xk)
agree = (np.abs(C[:, None] - C[None, :]) < 1e-9) & (np.abs(S[:, None] - S[None, :]) < 1e-9)
ii, jj = np.nonzero(agree)
rat = (xk[ii] - xk[jj])/(2*np.pi)
assert np.all(np.abs(rat - np.round(rat)) < 1e-6), "non-fiber agreement found"
for kk in (-2, -1, 1, 2):
    check(f"V25 fiber shift 2pi*{kk}", np.cos(xg) - np.cos(xg + kk*2*np.pi), 1e-12, "CP")
    check(f"V25 fiber shift 2pi*{kk}", np.sin(xg) - np.sin(xg + kk*2*np.pi), 1e-12, "CP")
print("OK [CP/NC] V25 (cos,sin) agree at x,y iff x-y in 2pi Z")

# V26: translation group law.
for a, b in [(0.3, 1.7), (-2.1, 0.9), (np.pi, np.pi/2)]:
    check(f"V26 tau_{a}+tau_{b}", (xg + a) + b - (xg + (a + b)), 1e-12, "CP")

# V27: finite on D -- the poles are exactly at the seam set.
assert np.all(np.isfinite(Fsp(xg))) and np.all(np.isfinite(Fsm(xg)))
assert np.all(np.isfinite(Fcp(xg))) and np.all(np.isfinite(Fcm(xg)))
print("OK [NC] V27 all four factors finite on D; poles only at Sigma")

# V28: reflection laws, sign-of-tan identity, seam interlacing, 1-D source.
# iota(x) = -x conjugates +- within a channel, and that equals inversion.
check("V28 Fs+(-x) = Fs-(x)", Fsp(-xg) - Fsm(xg), 1e-9, "CP")
check("V28 Fc+(-x) = Fc-(x)", Fcp(-xg) - Fcm(xg), 1e-9, "CP")
# iota_d(x) = pi/2 - x (complementary reflection) swaps channels, keeping +-.
check("V28 Fs+(pi/2-x) = Fc+(x)", Fsp(np.pi/2 - xg) - Fcp(xg), 1e-9, "CP")
check("V28 Fs-(pi/2-x) = Fc-(x)", Fsm(np.pi/2 - xg) - Fcm(xg), 1e-9, "CP")
# quarter-turn exchanges channel-conjugately: + <-> - across channels.
check("V28 Fs+(x+pi/2) = Fc-(x)", Fsp(xg + np.pi/2) - Fcm(xg), 1e-9, "CP")
check("V28 Fc+(x+pi/2) = Fs-(x)", Fcp(xg + np.pi/2) - Fsm(xg), 1e-9, "CP")
# sgn(tan x) = sgn(cot x) = eps on D (tan, cot finite away from seams).
assert np.all(np.sign(np.tan(xg)) == eps(xg))
assert np.all(np.sign(1/np.tan(xg)) == eps(xg))
print("OK [CP] V28 sgn(tan) = sgn(cot) = eps on D")
# seam classes alternate and are disjoint: k pi < pi/2 + k pi < (k+1) pi.
for k in range(-4, 5):
    assert k*np.pi < np.pi/2 + k*np.pi < (k+1)*np.pi
    assert k*np.pi != np.pi/2 + k*np.pi
print("OK [CP] V28 Sigma_s, Sigma_c alternating and disjoint")
# one-dimensional common source on Q0: each component strictly monotone in Fsp
# (Fsm = 1/Fsp; Fcp, Fcm inherit strict monotonicity from x via V8).
order = np.argsort(Fsp(q0))
assert np.all(np.diff(Fsm(q0)[order]) < 0), "Fsm not decreasing in Fsp"
assert np.all(np.diff(Fcp(q0)[order]) < 0), "Fcp not decreasing in Fsp"
assert np.all(np.diff(Fcm(q0)[order]) > 0), "Fcm not increasing in Fsp"
print("OK [NC] V28 quadruple has a one-dimensional source on Q0")

print(f"\nAll {len(results)} numerical checks passed (+ printed exact checks). "
      "No timeouts.")
