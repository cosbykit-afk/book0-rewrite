#!/usr/bin/env python3
"""Book 2 figure verification + PNG fallback generation.

Every plotted identity is checked numerically with real assertions on
seam-avoiding grids. These are COMPLETED NUMERICAL CHECKS, never proofs.
All identities checked are proved in the manuscript text; the checks only
confirm the plotted curves coincide to floating-point tolerance.

Outputs: ~/workspace/r-theory-rewrite/book2/graphs/b2_*.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.expanduser("~/workspace/r-theory-rewrite/book2/graphs")
os.makedirs(OUT, exist_ok=True)

TOL = 1e-9          # tight tolerance for exact algebraic identities
TOL_LOOSE = 1e-6    # for finite-difference derivative checks

# ---------------------------------------------------------------- grids
def D_grid(lo=-7.0, hi=7.0, n=40001, seam_gap=1e-3):
    x = np.linspace(lo, hi, n)
    m = (np.abs(np.sin(x)) > seam_gap) & (np.abs(np.cos(x)) > seam_gap)
    return x[m]

xg = D_grid()                      # common-domain grid, |x|<=7
sn, cs = np.sin(xg), np.cos(xg)

# canonical primitives (2.I.D1-D3)
srx = np.abs(1/sn) + cs/sn
sxp = np.abs(1/sn) - cs/sn
cxp = np.abs(1/cs) + sn/cs
crx = np.abs(1/cs) - sn/cs

# UNA differences (2.IV.D1-D2, canonical sign lock)
urx = srx - crx
uxp = cxp - sxp
eps = np.sign(np.sin(2*xg))        # branch sign, nonzero on grid

results = []
def check(name, err, tol, scope="completed numerical check"):
    assert np.all(np.isfinite(err)), f"{name}: non-finite values"
    m = float(np.max(np.abs(err)))
    assert m < tol, f"{name}: max_error={m} >= tol={tol}"
    results.append((name, m, tol, scope))
    print(f"OK  {name}: max_err={m:.3e} < {tol:.0e}")

# ------------------------------------------------- Fig 1: quartet checks
check("F1 reciprocity srx*sxp=1", srx*sxp - 1, TOL)
check("F1 reciprocity cxp*crx=1", cxp*crx - 1, TOL)
assert np.all(srx > 0) and np.all(sxp > 0) and np.all(cxp > 0) and np.all(crx > 0)
print("OK  F1 positivity: all four > 0 on D grid")
# threshold law (2.I/2.II): eps=+1 iff both plus-factors > 1 (away from sin2x=0)
tm = np.abs(np.sin(2*xg)) > 1e-2
assert np.all(((srx[tm] > 1) & (cxp[tm] > 1)) == (eps[tm] > 0))
print("OK  F1 threshold law: (srx>1 & cxp>1) <=> eps=+1")
# principal-chart midpoint: srx(pi/4) = sqrt(2)+1 (2.II.T10)
assert abs((1/np.sin(np.pi/4) + np.cos(np.pi/4)/np.sin(np.pi/4)) - (np.sqrt(2)+1)) < 1e-12
print("OK  F1 midpoint srx(pi/4)=sqrt(2)+1")

# ------------------------------------------------- Fig 2: double angle
s2x = np.sin(2*xg)
check("F2 sum urx+uxp=4/sin2x",
      np.abs((urx+uxp) - 4/s2x) / (1 + np.abs(4/s2x)), TOL)
check("F2 product urx*uxp=4/|sin2x|",
      np.abs(urx*uxp - 4/np.abs(s2x)) / (1 + np.abs(4/s2x)), TOL)
check("F2 |sum|=product", np.abs(urx+uxp) - urx*uxp, TOL)

# ------------------------------------------------- Fig 3: FlatWave
zw = srx*cxp
fw = (srx + cxp)/(zw - 1)
assert np.all(np.abs(zw - 1) > 1e-9), "zw-1 too close to 0 on grid"
check("F3 FlatWave=sgn(sin2x)", fw - eps, 1e-9)
check("F3 FlatWave^2=1", fw**2 - 1, 1e-12)
# quadrant character (-1)^k on Q_k
for k in range(-4, 4):
    qm = (xg > k*np.pi/2 + 0.05) & (xg < (k+1)*np.pi/2 - 0.05)
    if np.any(qm):
        assert np.all(np.abs(fw[qm] - ((-1)**k)) < 1e-9), f"quadrant {k} character"
print("OK  F3 quadrant character FlatWave=(-1)^k on Q_-4..Q_3")

# ------------------------------------------------- Fig 4: Mobius map
def Mp(z): return (z+1)/(z-1)          # eps=+1 branch
def Mm(z): return (1-z)/(1+z)          # eps=-1 branch
zp = np.linspace(1.001, 8, 20000)
zm = np.linspace(0.001, 0.999, 20000)
check("F4 involution M+(M+(z))=z", Mp(Mp(zp)) - zp, TOL)
check("F4 involution M-(M-(z))=z", Mm(Mm(zm)) - zm, TOL)
assert np.all(Mp(zp) > 1) and np.all((Mm(zm) > 0) & (Mm(zm) < 1))
print("OK  F4 branch preservation: M+:I+->I+, M-:I-->I-")
assert abs(Mp(np.sqrt(2)+1) - (np.sqrt(2)+1)) < 1e-12
assert abs(Mm(np.sqrt(2)-1) - (np.sqrt(2)-1)) < 1e-12
print("OK  F4 fixed points sqrt(2)+1 and sqrt(2)-1")
dMp = (Mp(zp+1e-7) - Mp(zp-1e-7))/2e-7
dMm = (Mm(zm+1e-7) - Mm(zm-1e-7))/2e-7
assert np.all(dMp < 0) and np.all(dMm < 0)
print("OK  F4 strict order reversal on both branches")

# ------------------------------------------------- Fig 5: same-phase reduction
sm = (np.abs(np.sin(2*xg)) > 1e-3)
w_meps = (srx[sm] + eps[sm])/(eps[sm]*srx[sm] - 1)
assert np.all(np.abs(eps[sm]*srx[sm] - 1) > 1e-6), "Mobius denominator near 0"
check("F5 cxp=M_eps(srx) same phase",
      np.abs(cxp[sm] - w_meps)/(1 + np.abs(cxp[sm])), TOL)

# ------------------------------------------------- Fig 6: carrier ellipse
H = np.sin(2*xg)/4
V = np.cos(2*xg)/2
check("F6 ellipse V^2+4H^2=1/4", V**2 + 4*H**2 - 0.25, 1e-12)
U, W = 4*H, 2*V
check("F6 unit circle U^2+W^2=1", U**2 + W**2 - 1, 1e-12)
# derivative checks on a uniform seam-free grid (Q_0 interior)
xu = np.linspace(0.05, 1.5, 40001); dxu = xu[1] - xu[0]
Hu = np.sin(2*xu)/4; Vu = np.cos(2*xu)/2
dH = np.gradient(Hu, dxu); dV = np.gradient(Vu, dxu)
check("F6 H'=V (finite diff)", dH[1:-1] - Vu[1:-1], TOL_LOOSE)
check("F6 V'=-4H (finite diff)", dV[1:-1] + 4*Hu[1:-1], TOL_LOOSE)

# ------------------------------------------------- Fig 7: harmonic extraction
check("F7 1/(urx+uxp)=sin2x/4 on D",
      np.abs(1/(urx+uxp) - np.sin(2*xg)/4)/(1 + np.abs(np.sin(2*xg)/4)), TOL)
for k in range(-4, 5):
    assert abs(np.sin(2*(k*np.pi/2))/4) < 1e-15
print("OK  F7 H(b_k)=0 at seams b_k=k*pi/2")
check("F7 FlatWave=sgn(H) on D", fw - np.sign(H), 1e-9)

print(f"\nAll {len(results)} numerical checks passed.")

# ================================================================ PNGs
def seam_mask(x, gap=2e-3):
    return (np.abs(np.sin(x)) < gap) | (np.abs(np.cos(x)) < gap)

plt.rcParams.update({"font.size": 9})

# ---- F1 quartet
x = np.linspace(-7, 7, 4001); m = ~seam_mask(x); xx = x[m]
f, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(xx, np.abs(1/np.sin(xx))+np.cos(xx)/np.sin(xx), lw=1.2, label="srx=|csc x|+cot x")
ax.plot(xx, np.abs(1/np.sin(xx))-np.cos(xx)/np.sin(xx), lw=1.2, label="sxp=|csc x|-cot x")
ax.plot(xx, np.abs(1/np.cos(xx))+np.sin(xx)/np.cos(xx), lw=1.2, label="cxp=|sec x|+tan x")
ax.plot(xx, np.abs(1/np.cos(xx))-np.sin(xx)/np.cos(xx), lw=1.2, label="crx=|sec x|-tan x")
ax.set_xlim(-7, 7); ax.set_ylim(-0.5, 6); ax.legend(fontsize=8, loc="upper right")
ax.set_title("Fig 1 — Canonical primitive quartet on D (fallback)")
ax.set_xlabel("x"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b2_quartet.png", dpi=110); plt.close(f)

# ---- F2 double angle
x = np.linspace(-3.2, 3.2, 6001); m = ~seam_mask(x, 5e-3); xx = x[m]
snx, csx = np.sin(xx), np.cos(xx)
sr = np.abs(1/snx)+csx/snx; sp = np.abs(1/snx)-csx/snx
cp = np.abs(1/csx)+snx/csx; cr = np.abs(1/csx)-snx/csx
ur, ux = sr-cr, cp-sp
f, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(xx, ur+ux, lw=1.4, label="urx+uxp")
ax.plot(xx, 4/np.sin(2*xx), lw=1.2, ls="--", label="4/sin 2x")
ax.plot(xx, ur*ux, lw=1.2, label="urx·uxp")
ax.plot(xx, 4/np.abs(np.sin(2*xx)), lw=1.0, ls="--", label="4/|sin 2x|")
ax.set_xlim(-3.2, 3.2); ax.set_ylim(-10, 10); ax.legend(fontsize=8, loc="upper right")
ax.set_title("Fig 2 — Double-angle closure: sum and product (fallback)")
ax.set_xlabel("x"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b2_doubleangle.png", dpi=110); plt.close(f)

# ---- F3 FlatWave
x = np.linspace(-7, 7, 8001); m = ~seam_mask(x, 3e-3); xx = x[m]
snx, csx = np.sin(xx), np.cos(xx)
srz = np.abs(1/snx)+csx/snx; cw = np.abs(1/csx)+snx/csx
fwx = (srz+cw)/(srz*cw-1)
f, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(xx, fwx, lw=1.4, label="(srx+cxp)/(srx·cxp-1)")
ax.plot(xx, np.sign(np.sin(2*xx)), lw=1.0, ls="--", label="sgn(sin 2x)")
for k in range(-4, 5):
    ax.axvline(k*np.pi/2, color="k", lw=0.5, alpha=0.5)
ax.set_xlim(-7, 7); ax.set_ylim(-2, 2); ax.legend(fontsize=8, loc="upper right")
ax.set_title("Fig 3 — FlatWave binary collapse (fallback)")
ax.set_xlabel("x"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b2_flatwave.png", dpi=110); plt.close(f)

# ---- F4 Mobius branches
zp = np.linspace(1.002, 5, 2000); zm = np.linspace(0.002, 0.998, 2000)
f, ax = plt.subplots(figsize=(6.4, 6.4))
ax.plot(zp, (zp+1)/(zp-1), lw=1.6, label="M+(z)=(z+1)/(z-1), z>1")
ax.plot(zm, (1-zm)/(1+zm), lw=1.6, label="M-(z)=(1-z)/(1+z), 0<z<1")
zz = np.linspace(0, 5, 400)
ax.plot(zz, zz, lw=1.0, ls="--", color="gray", label="y=z")
ax.plot([np.sqrt(2)+1], [np.sqrt(2)+1], "ko", label="fixed √2+1")
ax.plot([np.sqrt(2)-1], [np.sqrt(2)-1], "ko", label="fixed √2-1")
ax.set_xlim(-0.2, 5); ax.set_ylim(-0.2, 5); ax.set_aspect("equal", adjustable="box")
ax.legend(fontsize=8, loc="upper right")
ax.set_title("Fig 4 — Möbius branches and fixed points (fallback)")
ax.set_xlabel("z"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b2_mobius.png", dpi=110); plt.close(f)

# ---- F5 same-phase reduction
x = np.linspace(-3.2, 3.2, 6001); m = ~seam_mask(x, 5e-3); xx = x[m]
snx, csx = np.sin(xx), np.cos(xx)
srz = np.abs(1/snx)+csx/snx; cw = np.abs(1/csx)+snx/csx
ee = np.sign(np.sin(2*xx))
f, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(xx, cw, lw=1.4, label="cxp(x)")
ax.plot(xx, (srz+ee)/(ee*srz-1), lw=1.2, ls="--", label="(srx+ε)/(ε·srx-1)")
ax.set_xlim(-3.2, 3.2); ax.set_ylim(-6, 6); ax.legend(fontsize=8, loc="upper right")
ax.set_title("Fig 5 — Same-phase Möbius reduction (fallback)")
ax.set_xlabel("x"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b2_mobius_phase.png", dpi=110); plt.close(f)

# ---- F6 carrier ellipse
th = np.linspace(0, 2*np.pi, 2001)
te = np.linspace(0, 2*np.pi, 400)
f, ax = plt.subplots(figsize=(6.4, 5.2))
ax.plot(0.25*np.sin(te), 0.5*np.cos(te), lw=1.0, ls="--", color="gray",
        label="v²+4h²=1/4")
ax.plot(np.sin(th)/4, np.cos(th)/2, lw=1.6, label="(H(x),V(x)) traced")
ax.plot([0], [0.5], "ko", label="(0, 1/2) at x=0")
ax.set_xlim(-0.45, 0.45); ax.set_ylim(-0.65, 0.65)
ax.set_aspect("equal", adjustable="box"); ax.legend(fontsize=8, loc="upper right")
ax.set_title("Fig 6 — Carrier ellipse and (H,V) trace (fallback)")
ax.set_xlabel("h"); ax.set_ylabel("v"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b2_carrier.png", dpi=110); plt.close(f)

# ---- F7 extraction through seams
x = np.linspace(-7, 7, 8001); m = ~seam_mask(x, 3e-3); xx = x[m]
snx, csx = np.sin(xx), np.cos(xx)
sr = np.abs(1/snx)+csx/snx; sp = np.abs(1/snx)-csx/snx
cp = np.abs(1/csx)+snx/csx; cr = np.abs(1/csx)-snx/csx
ur, ux = sr-cr, cp-sp
f, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(x, np.sin(2*x)/4, lw=1.6, label="H(x)=sin 2x/4 (smooth, all R)")
ax.plot(xx, 1/(ur+ux), lw=1.1, ls="--", label="1/(urx+uxp) on D")
bk = np.arange(-2, 3)*np.pi/2
ax.plot(bk, np.zeros_like(bk), "ko", ms=5, label="seam values H(bk)=0")
ax.set_xlim(-7, 7); ax.set_ylim(-0.4, 0.4); ax.legend(fontsize=8, loc="upper right")
ax.set_title("Fig 7 — Harmonic extraction through the seams (fallback)")
ax.set_xlabel("x"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b2_extraction.png", dpi=110); plt.close(f)

sizes = {p: os.path.getsize(os.path.join(OUT, p)) for p in sorted(os.listdir(OUT))}
print("\nPNG fallbacks written:")
for p, s in sizes.items():
    assert s > 0, f"{p} is empty"
    print(f"  {p}: {s} bytes")
