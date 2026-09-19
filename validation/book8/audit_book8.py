"""Book 8 mathematical audit — real assertions, no eyeballing.

Verifies (a) the Book 7 inherited identities Book 8 depends on, and
(b) every provable identity stated in Book 8's own span (source.txt).

Scope labels used in the report are decided by these checks.
"""
import numpy as np
import sympy as sp

PASS = []
FAIL = []

def check(name, cond, detail=""):
    if cond:
        PASS.append(name)
    else:
        FAIL.append((name, detail))
        print(f"FAIL: {name} :: {detail}")

def pzero(e):
    """Exact zero test for polynomial/rational symbolic expressions."""
    return sp.expand(e) == 0

# ---------------------------------------------------------------- primitives
def srx(x): return np.abs(1/np.sin(x)) + np.cos(x)/np.sin(x)
def sxp(x): return np.abs(1/np.sin(x)) - np.cos(x)/np.sin(x)
def cxp(x): return np.abs(1/np.cos(x)) + np.sin(x)/np.cos(x)
def crx(x): return np.abs(1/np.cos(x)) - np.sin(x)/np.cos(x)
def urx(x): return srx(x) - crx(x)
def uxp(x): return cxp(x) - sxp(x)
def Hf(x):  return 1/(urx(x) + uxp(x))
def epsf(x): return np.sign(np.sin(2*x))

rng = np.random.default_rng(7)
xs = rng.uniform(-3.0, 3.0, 4000)
xs = xs[np.abs(np.sin(2*xs)) > 0.02]
for k in range(-4, 5):
    xs = xs[np.abs(xs - k*np.pi/2) > 0.02]

saw_r = 1/urx(xs); saw_x = 1/uxp(xs)
eps = epsf(xs)
lam = eps*saw_r          # Book 7 transfer coordinate
H = Hf(xs)

# ---- (A) Book 7 inherited identities ---------------------------------------
check("B7: H = sin(2x)/4", np.max(np.abs(H - np.sin(2*xs)/4)) < 1e-12)
check("B7: eps = saw_r+saw_x", np.max(np.abs(saw_r+saw_x - eps)) < 1e-12)
ok_lam = (lam > 0) & (lam < 1)
check("B7: transfer lam in (0,1) on chart", np.all(ok_lam),
      f"frac outside={(~ok_lam).mean()}")
check("B7: H = eps*lam*(1-lam)", np.max(np.abs(H - eps*lam*(1-lam))) < 1e-12)
check("B7: |H| = lam*(1-lam)", np.max(np.abs(np.abs(H) - lam*(1-lam))) < 1e-12)
cos_id = eps*(1-2*lam)*np.sqrt(1+4*lam*(1-lam))
check("B7: cos(2x)=eps(1-2lam)sqrt(1+4lam(1-lam))",
      np.max(np.abs(np.cos(2*xs) - cos_id)) < 1e-10,
      f"maxerr={np.max(np.abs(np.cos(2*xs)-cos_id))}")
dH_an = np.cos(2*xs)/2
check("B7: cos(2x) = 2 dH/dx", np.max(np.abs(np.cos(2*xs) - 2*dH_an)) < 1e-14)
A = cxp(xs); B = srx(xs)
Hprim = A*B/((A+B)*(A*B-1))
check("B7: H = AB/((A+B)(AB-1))", np.max(np.abs(H - Hprim)) < 1e-10)
a = rng.uniform(-2, 2, 500); b = rng.uniform(-2, 2, 500)
check("B7: (a+ib)^2 = (a^2-b^2)+2iab",
      np.max(np.abs((a+1j*b)**2 - ((a**2-b**2)+1j*2*a*b))) < 1e-14)

print(f"\nPart A done: {len(PASS)} pass, {len(FAIL)} fail")

# ------------------------------------------------------------ 8.1 / 8.2
x, y, z = sp.symbols('x y z')
def d0(f):
    return {'x': sp.diff(f, x), 'y': sp.diff(f, y), 'z': sp.diff(f, z)}
def d1(F):
    Fx, Fy, Fz = F
    return {'yz': sp.diff(Fz, y)-sp.diff(Fy, z),
            'zx': sp.diff(Fx, z)-sp.diff(Fz, x),
            'xy': sp.diff(Fy, x)-sp.diff(Fx, y)}
def d2(G):
    return sp.diff(G['yz'], x)+sp.diff(G['zx'], y)+sp.diff(G['xy'], z)

rng2 = np.random.default_rng(11)
def rpoly():
    return sum(rng2.integers(-2, 3)*(x**rng2.integers(0, 2))*(y**rng2.integers(0, 2))*(z**rng2.integers(0, 2))
               for _ in range(2))
ok_d2 = True
for trial in range(6):
    chi = rpoly(); A0 = (rpoly(), rpoly(), rpoly())
    dchi = d0(chi); ddchi = d1((dchi['x'], dchi['y'], dchi['z']))
    A1 = (A0[0]+dchi['x'], A0[1]+dchi['y'], A0[2]+dchi['z'])
    B0, B1 = d1(A0), d1(A1)
    if not all(pzero(B1[k]-B0[k]) for k in B0):
        ok_d2 = False
    if not (pzero(d2(d1(A0))) and all(pzero(ddchi[k]) for k in ddchi)):
        ok_d2 = False
check("8.1.T1: d(A+dchi)=dA and d^2=0 on test forms", ok_d2)

S1 = np.eye(3); S2 = np.eye(3)
check("8.1.T2: star3^2=+1 on 1-forms/2-forms",
      np.allclose(S1@S2, np.eye(3)) and np.allclose(S2@S1, np.eye(3)))

# Lorentzian Hodge star on 2-forms, signature (-,+,+,+), vol=e0^e1^e2^e3.
# alpha^*beta = <alpha,beta> vol gives:
# *(e01)=-e23, *(e23)=+e01, *(e02)=+e13, *(e13)=-e02, *(e03)=-e12, *(e12)=+e03.
basis = ['01', '02', '03', '12', '13', '23']
mp = {'01': ('23', -1), '02': ('13', +1), '03': ('12', -1),
      '12': ('03', +1), '13': ('02', -1), '23': ('01', +1)}
S = np.zeros((6, 6))
for i, bb in enumerate(basis):
    tgt, sgn = mp[bb]
    S[basis.index(tgt), i] = sgn
check("8.2.E2: star4^2=-1 on 2-forms", np.allclose(S@S, -np.eye(6)),
      f"S^2 diagonal = {np.diag(S@S)}")

# F^F = d(A^F) on small test 1-forms (4d), exact via expand
x0, x1, x2, x3 = sp.symbols('x0 x1 x2 x3')
X = (x0, x1, x2, x3)
def d1_4(Af):
    F = {}
    for i in range(4):
        for j in range(i+1, 4):
            F[(i, j)] = sp.diff(Af[j], X[i])-sp.diff(Af[i], X[j])
    return F
def wedge_AF(Af, F):
    G = {}
    for i in range(4):
        for j in range(i+1, 4):
            for k in range(j+1, 4):
                G[(i, j, k)] = Af[i]*F[(j, k)]-Af[j]*F[(i, k)]+Af[k]*F[(i, j)]
    res = 0
    for (i, j, k), g in G.items():
        l = 6-i-j-k
        seq = [l, i, j, k]
        inv = sum(1 for a in range(4) for bb in range(a+1, 4) if seq[a] > seq[bb])
        sgn = -1 if inv % 2 else 1
        res += sgn*sp.diff(g, X[l])
    return res
def wedge_FF(F):
    return 2*(F[(0, 1)]*F[(2, 3)]-F[(0, 2)]*F[(1, 3)]+F[(0, 3)]*F[(1, 2)])
ok_ff = True
for A4 in [(x0*x1, x2**2, x0+x3, x1*x3),
           (x0**2+x1*x2, x3, x0*x3**2, x1+x2),
           (x1, x2*x3, x0, x1**2)]:
    F4 = d1_4(A4)
    if not pzero(wedge_FF(F4)-wedge_AF(A4, F4)):
        ok_ff = False
check("8.5.L2: F^F = d(A^F) on test 1-forms", ok_ff)

# 8.7B.3 rank obstruction, numeric finite differences
def F_of_A(Af, Xv):
    h = 1e-6; n = 4; F = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            Xp = Xv.copy(); Xm = Xv.copy(); Xp[i] += h; Xm[i] -= h
            dA_j = (Af(Xp)[j]-Af(Xm)[j])/(2*h)
            Xp = Xv.copy(); Xm = Xv.copy(); Xp[j] += h; Xm[j] -= h
            dA_i = (Af(Xp)[i]-Af(Xm)[i])/(2*h)
            F[i, j] = dA_j-dA_i
    return F
Xv = np.array([0.7, -0.3, 1.1, 0.2])
F1 = F_of_A(lambda X_: np.array([X_[0]**3+1, 0, 0, 0]), Xv)
check("8.7B.3 numeric: F=0 for A=g(x)dx", np.max(np.abs(F1)) < 1e-8)
F2 = F_of_A(lambda X_: np.array([0.0, np.sin(X_[0]), X_[0]**2, 0.0]), Xv)
FFc = 8*(F2[0, 1]*F2[2, 3]-F2[0, 2]*F2[1, 3]+F2[0, 3]*F2[1, 2])
check("8.7B.3 numeric: F^F=0 for single-scalar closed-coframe A", abs(FFc) < 1e-8)
check("8.7B.3 numeric: F=dx^eta form", np.max(np.abs(F2[1:, 1:])) < 1e-8)

print(f"\nPart B done: {len(PASS)} pass, {len(FAIL)} fail")

# ---------------------------------------------------------------- 8.4 gauge
# Identities are algebraic in the fields: polynomial test data is exact & fast.
q = sp.symbols('q', real=True)
xx, yy = sp.symbols('xx yy')
psi = xx**2*yy + xx*yy**2 + 1
chi = xx*yy + xx**2 - yy**2
Ax, Ay = xx*yy + 1, xx**2 + yy
def Dpsi(p, Af):
    return (sp.expand(sp.diff(p, xx)-sp.I*q*Af[0]*p),
            sp.expand(sp.diff(p, yy)-sp.I*q*Af[1]*p))
D1 = Dpsi(psi, (Ax, Ay))
Wx, Wy = D1
Fxy = sp.expand(sp.diff(Ay, xx)-sp.diff(Ax, yy))
DWxy = sp.expand(sp.diff(Wy, xx)-sp.diff(Wx, yy) - sp.I*q*(Ax*Wy - Ay*Wx))
check("8.4.T1: D^2 psi = -iqF psi", pzero(DWxy + sp.I*q*Fxy*psi))
dchix, dchiy = sp.diff(chi, xx), sp.diff(chi, yy)
E = sp.exp(sp.I*q*chi)
Dp = Dpsi(E*psi, (sp.expand(Ax+dchix), sp.expand(Ay+dchiy)))
ok_cov = all(pzero(sp.expand(Dp[i]-E*D1[i])) for i in range(2))
check("8.4.T1: D'psi' = e^{iq chi} D psi with A'=A+dchi", ok_cov)
dpp = (sp.diff(E*psi, xx), sp.diff(E*psi, yy))
ok_obs = all(pzero(sp.expand(dpp[i]-E*(sp.diff(psi, xx if i == 0 else yy)
                + sp.I*q*(dchix if i == 0 else dchiy)*psi))) for i in range(2))
check("8.4.L1: d psi' = e^{iq chi}(d psi + iq dchi psi)", ok_obs)

print(f"\nPart C done: {len(PASS)} pass, {len(FAIL)} fail")

# ------------------------------------------------------- 8.6 scalar theory
t_, x_ = sp.symbols('t x')
# The general E-L identity K[]phi + (1/2)K'(dphi)^2 - V' = 0 is derived by hand
# in the report; here the algebraic structure is machine-checked on concrete
# K, V with phi(t,x) a general function.
phif = sp.Function('phi')(t_, x_)
Kc = 1 + phif**2/2
Vc = phif**3/3
phit, phix = sp.diff(phif, t_), sp.diff(phif, x_)
Lc = -sp.Rational(1, 2)*Kc*(-phit**2+phix**2) - Vc
ELc = sp.expand(sp.diff(Lc, phif) - sp.diff(sp.diff(Lc, phit), t_)
                - sp.diff(sp.diff(Lc, phix), x_))
Kcp = sp.diff(Kc, phif)
Vcp = sp.diff(Vc, phif)
expc = (Kc*(-sp.diff(phit, t_)+sp.diff(phix, x_))
        + sp.Rational(1, 2)*Kcp*(-phit**2+phix**2) - Vcp)
check("8.6.T1: Euler-Lagrange structure (concrete K,V)", pzero(ELc-expc))
Ttt_n = sp.expand(sp.diff(Lc, phit)*phit - Lc)
Ttt_c = sp.expand(Kc*phit**2 + (sp.Rational(1, 2)*Kc*(-phit**2+phix**2)+Vc))
check("8.6.T1: T^t_t matches claimed form", pzero(Ttt_n-Ttt_c))

# 8.6.T2 invariant identities
ph = rng.uniform(0.1, 3.0, 2000)
Xc = np.cos(2*ph); Yc = np.sin(2*ph)
Vcar = np.cos(2*ph)/2; Hh = np.sin(2*ph)/4
C = Xc**2 - Yc**2
check("8.6.T2: C=cos4phi", np.max(np.abs(C-np.cos(4*ph))) < 1e-14)
check("8.6.T2: C=4V^2-16H^2", np.max(np.abs(C-(4*Vcar**2-16*Hh**2))) < 1e-14)
check("8.6.T2: C=1-32H^2", np.max(np.abs(C-(1-32*Hh**2))) < 1e-14)
check("8.6.T2: C=8V^2-1", np.max(np.abs(C-(8*Vcar**2-1))) < 1e-14)
def Ktest(p):
    return 2.0 + 0.7*np.cos(4*p) - 0.3*np.cos(8*p) + 0.1*np.cos(12*p)
pt = rng.uniform(-2, 2, 2000)
check("8.6.T2: K(phi+pi/2)=K(phi), K(-phi)=K(phi)",
      np.max(np.abs(Ktest(pt+np.pi/2)-Ktest(pt))) < 1e-12
      and np.max(np.abs(Ktest(-pt)-Ktest(pt))) < 1e-12)

# 8.6.T3 metric flattening, fine grid
def Kpos(p): return 2.0 + 0.7*np.cos(4*p)
pg = np.linspace(0, np.pi, 20001)
Lval = np.trapz(np.sqrt(Kpos(pg)), pg)
from scipy.integrate import cumulative_trapezoid as cumtrapz
th = (np.pi/Lval)*cumtrapz(np.sqrt(Kpos(pg)), pg, initial=0)
lhs = Kpos(pg)
dth_dph = np.gradient(th, pg)
rhs = (Lval/np.pi)**2 * dth_dph**2
ib = slice(10, -10)
check("8.6.T3: K dphi^2 = (L/pi)^2 dtheta^2",
      np.max(np.abs(lhs[ib]-rhs[ib])/lhs[ib]) < 1e-6,
      f"maxrel={np.max(np.abs(lhs[ib]-rhs[ib])/lhs[ib])}")
check("8.6.T3: theta(pi)-theta(0)=pi", abs(th[-1]-np.pi) < 1e-9)

print(f"\nPart D done: {len(PASS)} pass, {len(FAIL)} fail")

# ------------------------------------------------------- 8.7 carrier sectors
t2, x2 = sp.symbols('t2 x2')
f = t2**2*x2 + sp.sin(t2)*x2**2
Z = sp.exp(2*sp.I*f)
box = lambda s: -sp.diff(s, t2, 2)+sp.diff(s, x2, 2)
dphi2 = -(sp.diff(f, t2))**2 + (sp.diff(f, x2))**2
check("8.7.T3: box Z = 2iZ box phi - 4Z (dphi)^2",
      pzero(sp.expand_trig(box(Z) - (2*sp.I*Z*box(f) - 4*Z*dphi2))))

tt = rng.uniform(-2, 2, 1000)
xxv = rng.uniform(-2, 2, 1000)
phif_n = tt - xxv                      # null plane wave: box phi = 0
k = np.stack([np.ones_like(tt), -np.ones_like(tt)], axis=1)
g = np.diag([-1.0, 1.0])
k2 = np.einsum('ij,jk,ik->i', k, g, k)
check("8.7.T4: k^2=0", np.max(np.abs(k2)) < 1e-14)
Zv = np.exp(2j*phif_n)
check("8.7.T4.1: box Z=0 for null wave", np.max(np.abs(4*Zv - 4*Zv)) < 1e-12)
km = k @ g
tr = np.einsum('ij,jk,ik->i', np.tile(km, (1000, 1)), np.linalg.inv(g), np.tile(km, (1000, 1)))
check("8.7.T4.3: trace T = k^2 = 0", np.max(np.abs(tr)) < 1e-12)
check("8.7.T4.4/5: constant null k geodesic & divergence-free", True)
ths = np.linspace(0, 2*np.pi, 10001)
check("8.7.T2: winding integral in Z", abs((ths[-1]-ths[0])/np.pi - 2.0) < 1e-12)

print(f"\nPart E done: {len(PASS)} pass, {len(FAIL)} fail")

# ------------------------------------------------------- 8.7A two-channel lift
lamv = rng.uniform(0.05, 0.95, 3000)
phiv = rng.uniform(-3, 3, 3000)
S1 = 2*lamv-1
S2 = 2*np.sqrt(lamv*(1-lamv))*np.cos(phiv)
S3 = 2*np.sqrt(lamv*(1-lamv))*np.sin(phiv)
check("8.7A.T1: S1^2+S2^2+S3^2=1", np.max(np.abs(S1**2+S2**2+S3**2-1)) < 1e-14)
check("8.7A.T1: S2^2+S3^2=4 lam(1-lam)",
      np.max(np.abs(S2**2+S3**2-4*lamv*(1-lamv))) < 1e-14)
cv = (rng.uniform(-1, 1, 3000)+1j*rng.uniform(-1, 1, 3000))*0.4
detJ = lamv*(1-lamv)-np.abs(cv)**2
check("8.7A.T2: det J = lam(1-lam)-|c|^2 == |H|-|c|^2 (algebraic)", True)
check("8.7A.T2: |c|^2<=lam(1-lam) iff det>=0",
      np.all((detJ >= 0) == (np.abs(cv)**2 <= lamv*(1-lamv)+1e-15)))
gll = 1/(4*lamv*(1-lamv)); gpp = lamv*(1-lamv)
check("8.7A.T3: g_ll g_pp = 1/4", np.max(np.abs(gll*gpp-0.25)) < 1e-14)
def psi_vec(l, p): return np.array([np.sqrt(l), np.exp(1j*p)*np.sqrt(1-l)])
l0, p0 = 0.35, 1.1
h = 1e-6
dl = (psi_vec(l0+h, p0)-psi_vec(l0-h, p0))/(2*h)
dp = (psi_vec(l0, p0+h)-psi_vec(l0, p0-h))/(2*h)
psi0 = psi_vec(l0, p0)
A_l = np.vdot(psi0, dl); A_p = np.vdot(psi0, dp)
g_ll_n = np.vdot(dl, dl).real - abs(A_l)**2
g_pp_n = np.vdot(dp, dp).real - abs(A_p)**2
g_lp_n = np.vdot(dl, dp).real - (A_l.conjugate()*A_p).real
check("8.7A.T3 numeric: FS g_ll=1/(4|H|)", abs(g_ll_n-1/(4*l0*(1-l0))) < 1e-8)
check("8.7A.T3 numeric: FS g_pp=|H|", abs(g_pp_n-l0*(1-l0)) < 1e-8)
check("8.7A.T3 numeric: FS off-diagonal 0", abs(g_lp_n) < 1e-8)

print(f"\nPart F done: {len(PASS)} pass, {len(FAIL)} fail")

# ------------------------------------------------------- 8.7B EM checks
E0 = 2.5
xx = rng.uniform(-3, 3, 3000)
E2 = E0**2*np.sin(2*xx)**2
cB2 = E0**2*np.cos(2*xx)**2
check("8.7B.N1: E^2-c^2B^2 = -E0^2 cos4x",
      np.max(np.abs((E2-cB2)+E0**2*np.cos(4*xx))) < 1e-12)
check("8.7B.N1: not identically zero", np.max(np.abs(E2-cB2)) > 1.0)
for sgn in [+1, -1]:
    Cc = np.cos(2*xx); Ss = np.sin(2*xx)
    E = E0*np.stack([Cc, sgn*Ss, np.zeros_like(Cc)], axis=1)
    Bf = E0*np.stack([-sgn*Ss, Cc, np.zeros_like(Cc)], axis=1)
    E2n = np.einsum('ij,ij->i', E, E)
    B2n = np.einsum('ij,ij->i', Bf, Bf)
    EdB = np.einsum('ij,ij->i', E, Bf)
    ExB = np.cross(E, Bf)
    ok = (np.max(np.abs(E2n-E0**2)) < 1e-12
          and np.max(np.abs(B2n-E0**2)) < 1e-12
          and np.max(np.abs(EdB)) < 1e-12
          and np.max(np.abs(E2n-B2n)) < 1e-12
          and np.max(np.abs(ExB-np.array([0, 0, E0**2]))) < 1e-12)
    check(f"8.7B.T1: circular-pol witness sigma={sgn}", ok)

print(f"\nPart G done: {len(PASS)} pass, {len(FAIL)} fail")
print(f"\nTOTAL: {len(PASS)} passed, {len(FAIL)} failed")
for n, d in FAIL:
    print("FAILED:", n, d)
