#!/usr/bin/env python3
"""Book 17 fallback-PNG generator.

Renders the 5 static fallback figures from the SAME expressions as the
Desmos embeds in book17/index.html (see the GRAPHS config there), at
240 dpi. The plotted identities are verified by validation/book17/
verify_book17.py (V1-V39); this script asserts the plotted constants
match the audit-verified values before writing, and that all 5 PNGs are
written non-empty.

Output: ~/workspace/r-theory-rewrite/book17/graphs/b17_*.png
"""
import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.expanduser("~/workspace/r-theory-rewrite/book17/graphs")
os.makedirs(OUT, exist_ok=True)

# ---- audit-verified constants (must match verify_book17.py) ----
SQ2 = math.sqrt(2)
VE = math.sqrt(4+2*math.sqrt(2)) + 1 + math.sqrt(2)   # V_E, V19
W0 = math.log(1+SQ2)                                   # w0, V15
assert abs(VE - 5.027339492125848) < 1e-9, "V_E constant drifted"
assert abs(math.sinh(W0) - 1) < 1e-15 and abs(math.cosh(W0) - SQ2) < 1e-15
assert abs(VE**4 - 638.7822724929383) < 1e-9, "V_E^4 constant drifted"
# the plotted green dots must sit on the plotted curves:
assert abs((1/math.sin(math.radians(22.5)) + 1/math.tan(math.radians(22.5))) - VE) < 1e-12
print("OK: plotted constants match the audit-verified values")

def prims(x):
    s, c = np.sin(x), np.cos(x)
    srx = np.abs(1/s) + c/s
    cxp = np.abs(1/c) + s/c
    return srx, cxp

def seam_mask(x, gap=3e-3):
    return (np.abs(np.sin(x)) < gap) | (np.abs(np.cos(x)) < gap)

DPI = 240
plt.rcParams.update({"font.size": 10.5, "axes.titlesize": 12, "axes.labelsize": 11})
D2R = math.pi/180

# ---- F1 primitives + octant bands
x = np.linspace(0.02, 2*np.pi-0.02, 6001); m = ~seam_mask(x, 4e-3); xx = x[m]
s1, c1 = prims(xx)
f, ax = plt.subplots(figsize=(8, 4.6))
for k in range(1, 8):
    ax.axvline(k*math.pi/4, color="gray", lw=0.7, ls="--", alpha=0.6)
ax.plot(xx, s1, lw=1.3, label="srx=|csc x|+cot x")
ax.plot(xx, c1, lw=1.3, label="cxp=|sec x|+tan x")
for deg, yy in [(22.5, VE), (112.5, 1/VE), (202.5, VE), (292.5, 1/VE)]:
    ax.plot([deg*D2R], [yy], "go", ms=6)
ax.text(22.5*D2R, VE+0.35, "E-contact\nV_E", ha="center", fontsize=8, color="green")
ax.set_xlim(0, 2*np.pi); ax.set_ylim(-0.5, 7)
ax.set_xticks([k*math.pi/4 for k in range(9)],
              ["0","π/4","π/2","3π/4","π","5π/4","3π/2","7π/4","2π"])
ax.legend(fontsize=8, loc="upper right")
ax.set_title("Fig 1 — Canonical primitives with octant bands (fallback)")
ax.set_xlabel("x"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b17_primitives.png", dpi=DPI); plt.close(f)

# ---- F2 carrier ellipse
th = np.linspace(0, 2*np.pi, 2001)
f, ax = plt.subplots(figsize=(6.4, 5.4))
ax.plot(0.5*np.cos(th), 0.25*np.sin(th), lw=1.0, ls="--", color="gray",
        label="V_R²+4H²=1/4")
ax.plot(np.cos(2*th)/2, np.sin(2*th)/4, lw=1.7, label="(V_R,H) traced (2:1)")
sq = SQ2
ax.plot([sq/4], [sq/8], "go", ms=8, label="E (22.5°, 202.5°)")
ax.plot([-sq/4], [-sq/8], "go", ms=8, label="E (112.5°, 292.5°)")
ax.plot([0.5, 0, -0.5, 0], [0, 0.25, 0, -0.25], "ko", ms=5)
ax.set_xlim(-0.62, 0.62); ax.set_ylim(-0.38, 0.38)
ax.set_aspect("equal", adjustable="box"); ax.legend(fontsize=8, loc="upper right")
ax.set_title("Fig 2 — Elliptic carrier, 2:1 map (fallback)")
ax.set_xlabel("V_R"); ax.set_ylabel("H"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b17_ellipse.png", dpi=DPI); plt.close(f)

# ---- F3 Flatwave quadrants
x = np.linspace(0.02, 2*np.pi-0.02, 12001); m = ~seam_mask(x, 5e-3); xx = x[m]
s1, c1 = prims(xx)
sxp, crx = 1/s1, 1/c1          # reciprocal pair (srx*sxp = 1, cxp*crx = 1)
fwx = 1/(s1-crx) + 1/(c1-sxp)  # 1/urx + 1/uxp
f, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(xx, fwx, lw=1.5, label="1/urx+1/uxp")
ax.axhline(1, color="green", ls="--", lw=1.2, label="+1 on Q1,Q3")
ax.axhline(-1, color="red", ls="--", lw=1.2, label="−1 on Q2,Q4")
for k in range(1, 4):
    ax.axvline(k*math.pi/2, color="k", lw=0.6, alpha=0.5)
ax.set_xlim(0, 2*np.pi); ax.set_ylim(-1.8, 1.8)
ax.set_xticks([0, math.pi/2, math.pi, 3*math.pi/2, 2*math.pi],
              ["0","π/2","π","3π/2","2π"])
ax.legend(fontsize=8, loc="upper right")
ax.set_title("Fig 3 — Flatwave = sgn(sin 2x), not ≡1 (fallback)")
ax.set_xlabel("x"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b17_flatwave.png", dpi=DPI); plt.close(f)

# ---- F4 cos(4x) footprint (IC-4 exhibit)
x = np.linspace(0, 2*np.pi, 4001)
f, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(x, np.cos(4*x), lw=1.6, label="cos(4x) — paired footprint")
ax.axhline(0, color="k", lw=0.7)
z = np.array([22.5+45*k for k in range(8)])*D2R
ax.plot(z, np.zeros_like(z), "go", ms=7, label="zeros at MIDPOINTS (22.5°+k45°)")
b = np.array([0,45,90,135,180,225,270,315])*D2R
ax.plot(b, np.cos(4*b), "ro", ms=7, label="boundaries: ±1, NOT 0 (IC-4)")
ax.set_xlim(0, 2*np.pi); ax.set_ylim(-1.4, 1.4)
ax.set_xticks([k*math.pi/4 for k in range(9)],
              ["0","45°","90°","135°","180°","225°","270°","315°","360°"])
ax.legend(fontsize=8, loc="upper right")
ax.set_title("Fig 4 — Paired footprint: zeros at octant midpoints (fallback)")
ax.set_xlabel("x"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b17_footprint.png", dpi=DPI); plt.close(f)

# ---- F5 rapidity ladder
x = np.linspace(0.03, 2*np.pi-0.03, 12001); m = ~seam_mask(x, 8e-3); xx = x[m]
w = np.log(np.abs(np.cos(xx)/np.sin(xx)))
w = np.clip(w, -3.2, 3.2)
f, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(xx, w, lw=1.4, label="w(x)=ln|cot x|")
ax.axhline(W0, color="green", ls="--", lw=1.2, label=f"+w0=ln(1+√2)≈{W0:.4f}")
ax.axhline(-W0, color="green", ls="--", lw=1.2, label=f"−w0≈{-W0:.4f}")
degs = [22.5,67.5,112.5,157.5,202.5,247.5,292.5,337.5]
sgns = [1,-1,-1,1,1,-1,-1,1]
ax.plot([d*D2R for d in degs], [s*W0 for s in sgns], "go", ms=7,
        label="E-contact rapidities ±w0")
ax.set_xlim(0, 2*np.pi); ax.set_ylim(-3.2, 3.2)
ax.set_xticks([k*math.pi/4 for k in range(9)],
              ["0","π/4","π/2","3π/4","π","5π/4","3π/2","7π/4","2π"])
ax.legend(fontsize=8, loc="upper right")
ax.set_title("Fig 5 — Rapidity ladder at E-contacts (fallback)")
ax.set_xlabel("x"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b17_rapidity.png", dpi=DPI); plt.close(f)

# ---- real asserts: all 5 PNGs written, non-empty ----
expected = ["b17_primitives.png", "b17_ellipse.png", "b17_flatwave.png",
            "b17_footprint.png", "b17_rapidity.png"]
for p in expected:
    fp = os.path.join(OUT, p)
    assert os.path.isfile(fp), f"missing {fp}"
    sz = os.path.getsize(fp)
    assert sz > 10000, f"{p} suspiciously small ({sz} bytes)"
    print(f"  {p}: {sz} bytes")
print(f"\nOK: all {len(expected)} fallback PNGs written to {OUT}")
