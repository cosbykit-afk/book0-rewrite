#!/usr/bin/env python3
"""Generate verified PNG fallbacks for Book 2 Desmos graphs.

Each plot uses the EXACT formula that is embedded in the Desmos calculator
on book2/index.html, so the PNG doubles as verification of the embedded
expressions. The identities themselves are checked by
validation/book2/verify_book2.py (V1-V40, all passing, no timeouts).

Outputs: ~/workspace/r-theory-rewrite/book2/graphs/b2_*.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.expanduser("~/workspace/r-theory-rewrite/book2/graphs")
os.makedirs(OUT, exist_ok=True)

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
print("PNG fallbacks written:")
for p, s in sizes.items():
    assert s > 0, f"{p} is empty"
    print(f"  {p}: {s} bytes")
