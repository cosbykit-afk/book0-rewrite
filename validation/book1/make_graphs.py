#!/usr/bin/env python3
"""Book 1: numeric verification of graphable identities + PNG fallbacks."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

G = os.path.expanduser("~/workspace/r-theory-rewrite/book1/graphs")
os.makedirs(G, exist_ok=True)
SQ2 = np.sqrt(2)

def Fs_p(x): return np.abs(1/np.sin(x)) + np.cos(x)/np.sin(x)
def Fs_m(x): return np.abs(1/np.sin(x)) - np.cos(x)/np.sin(x)
def Fc_p(x): return np.abs(1/np.cos(x)) + np.sin(x)/np.cos(x)
def Fc_m(x): return np.abs(1/np.cos(x)) - np.sin(x)/np.cos(x)

rng = np.random.default_rng(0)
# points in D (away from seams k*pi/2)
xs = rng.uniform(-7, 7, 4000)
xs = xs[np.abs(np.sin(2*xs)) > 1e-3]

print("== numeric checks ==")
print("1 reciprocal Fs:", np.max(np.abs(Fs_p(xs)*Fs_m(xs) - 1)))
print("2 reciprocal Fc:", np.max(np.abs(Fc_p(xs)*Fc_m(xs) - 1)))
print("3 positivity min:", min(Fs_p(xs).min(), Fs_m(xs).min(), Fc_p(xs).min(), Fc_m(xs).min()))
print("4 sum Fs = 2|csc|:", np.max(np.abs(Fs_p(xs)+Fs_m(xs) - 2*np.abs(1/np.sin(xs)))))
print("5 diff Fs = 2cot:", np.max(np.abs(Fs_p(xs)-Fs_m(xs) - 2*np.cos(xs)/np.sin(xs))))

q0 = rng.uniform(0.01, np.pi/2 - 0.01, 2000)
print("6 half-angle Fs+ = cot(x/2):", np.max(np.abs(Fs_p(q0) - np.cos(q0/2)/np.sin(q0/2))))
print("7 half-angle Fs- = tan(x/2):", np.max(np.abs(Fs_m(q0) - np.sin(q0/2)/np.cos(q0/2))))
print("8 half-angle Fc+ = tan(pi/4+x/2):",
      np.max(np.abs(Fc_p(q0) - np.tan(np.pi/4 + q0/2))))
print("9 half-angle Fc- = tan(pi/4-x/2):",
      np.max(np.abs(Fc_m(q0) - np.tan(np.pi/4 - q0/2))))

m = np.pi/4
print("10 midpoint Fs+(pi/4)=sqrt2+1:", abs(Fs_p(m) - (SQ2+1)))
print("11 midpoint Fs-(pi/4)=sqrt2-1:", abs(Fs_m(m) - (SQ2-1)))
print("12 midpoint Fc+(pi/4)=sqrt2+1:", abs(Fc_p(m) - (SQ2+1)))

th = np.max(np.abs(np.sign(Fs_p(xs)-1) - np.sign(np.cos(xs)/np.sin(xs))))
print("13 threshold sgn(Fs+-1)=sgn(cot):", th)

o1 = rng.uniform(0.01, np.pi/4 - 0.01, 500)   # O_0
o2 = rng.uniform(np.pi/4 + 0.01, np.pi/2 - 0.01, 500)  # O_1
print("14 octant O0: Fs+>Fc+ all:", np.all(Fs_p(o1) > Fc_p(o1)),
      "| O1: Fs+<Fc+ all:", np.all(Fs_p(o2) < Fc_p(o2)))

# boundary traces at x=0 (sine-zero seam b_0)
dl = -np.logspace(-8, -1, 8)   # from left
dr = np.logspace(-8, -1, 8)    # from right
print("15 left limits (Fs+,Fs-,Fc+,Fc-):",
      Fs_p(dl[-1]), Fs_m(dl[0]), Fc_p(dl[-1]), Fc_m(dl[-1]))
print("    expect -> (0, +inf, 1, 1)")
print("16 right limits:", Fs_p(dr[0]), Fs_m(dr[-1]), Fc_p(dr[0]), Fc_m(dr[0]))
print("    expect -> (+inf, 0, 1, 1)")

# branch signs
a = np.sign(np.sin(xs)); b = np.sign(np.cos(xs)); e = np.sign(np.sin(2*xs))
print("17 eps = a*b:", np.max(np.abs(e - a*b)))
q0s = rng.uniform(0.01, np.pi/2-0.01, 300); q2s = rng.uniform(np.pi+0.01, 3*np.pi/2-0.01, 300)
print("18 eps=+1 on Q0 and Q2 (lossy):",
      np.all(np.sign(np.sin(2*q0s)) == 1), np.all(np.sign(np.sin(2*q2s)) == 1))

print("== graphs ==")
def plot_four(ax, x0, x1, n=4000, ylim=None):
    x = np.linspace(x0, x1, n)
    s2 = np.abs(np.sin(2*x)); ok = s2 > 2e-3
    x = x[ok]
    ax.plot(x, Fs_p(x), lw=1.2, label="F_s+")
    ax.plot(x, Fs_m(x), lw=1.2, label="F_s-")
    ax.plot(x, Fc_p(x), lw=1.2, label="F_c+")
    ax.plot(x, Fc_m(x), lw=1.2, label="F_c-")
    for k in range(int(np.floor(x0/(np.pi/2))), int(np.ceil(x1/(np.pi/2)))+1):
        ax.axvline(k*np.pi/2, color="k", lw=0.5, alpha=0.4)
    if ylim: ax.set_ylim(*ylim)
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

# Fig 1: global four factors
fig, ax = plt.subplots(figsize=(9, 4.5))
plot_four(ax, -7, 7, ylim=(-0.5, 6))
ax.set_title("The four reciprocal-conjugate factors on D")
fig.savefig(f"{G}/b1_four.png", dpi=110, bbox_inches="tight"); plt.close(fig)

# Fig 2: principal chart Q0 half-angle forms
fig, ax = plt.subplots(figsize=(8, 4.5))
x = np.linspace(0.005, np.pi/2-0.005, 2000)
ax.plot(x, np.cos(x/2)/np.sin(x/2), lw=1.6, label="F_s+ = cot(x/2)")
ax.plot(x, np.sin(x/2)/np.cos(x/2), lw=1.6, label="F_s- = tan(x/2)")
ax.plot(x, np.tan(np.pi/4+x/2), lw=1.6, label="F_c+ = tan(pi/4+x/2)")
ax.plot(x, np.tan(np.pi/4-x/2), lw=1.6, label="F_c- = tan(pi/4-x/2)")
ax.plot([np.pi/4], [SQ2+1], "ko"); ax.plot([np.pi/4], [SQ2-1], "ko")
ax.axvline(np.pi/4, color="k", ls="--", lw=0.8)
ax.set_xlim(0, np.pi/2); ax.set_ylim(0, 7)
ax.set_title("Principal chart Q0=(0,pi/2): monotone branches, meet at (pi/4, sqrt2+/-1)")
ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.savefig(f"{G}/b1_chart.png", dpi=110, bbox_inches="tight"); plt.close(fig)

# Fig 3: branch signs (offset for legibility)
fig, ax = plt.subplots(figsize=(9, 4.5))
x = np.linspace(-7, 7, 6000); ok = np.abs(np.sin(2*x)) > 1e-3; x = x[ok]
ax.plot(x, np.sign(np.sin(x))+2.2, lw=1.2, label="alpha + 2.2")
ax.plot(x, np.sign(np.cos(x)), lw=1.2, label="beta")
ax.plot(x, np.sign(np.sin(2*x))-2.2, lw=1.2, label="epsilon - 2.2")
for k in range(-4, 5):
    ax.axvline(k*np.pi/2, color="k", lw=0.5, alpha=0.4)
ax.set_ylim(-3.6, 3.6); ax.set_title("Branch signs (vertically separated; true values +/-1)")
ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.savefig(f"{G}/b1_signs.png", dpi=110, bbox_inches="tight"); plt.close(fig)

# Fig 4: reciprocal locus on hyperbola uv=1
fig, ax = plt.subplots(figsize=(6.5, 5))
u = np.linspace(1.001, 12, 2000)
ax.plot(u, 1/u, "k--", lw=1, label="uv = 1")
t = np.linspace(0.004, np.pi/2-0.004, 3000)
ax.plot(Fs_p(t), Fs_m(t), lw=2, label="(F_s+(x), F_s-(x)), x in Q0")
ax.set_xlim(0.8, 8); ax.set_ylim(-0.1, 2.5)
ax.set_xlabel("u"); ax.set_ylabel("v")
ax.set_title("Reciprocal conjugacy: the pair rides the hyperbola uv=1")
ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.savefig(f"{G}/b1_hyperbola.png", dpi=110, bbox_inches="tight"); plt.close(fig)

# Fig 5: cross-channel comparison, diagonal crossing
fig, ax = plt.subplots(figsize=(6.5, 5))
t = np.linspace(0.004, np.pi/2-0.004, 3000)
ax.plot([0.8, 8], [0.8, 8], "k--", lw=1, label="diagonal u = v")
ax.plot(Fs_p(t), Fc_p(t), lw=2, label="(F_s+(x), F_c+(x)), x in Q0")
ax.plot([SQ2+1], [SQ2+1], "ko")
ax.set_xlim(0.8, 8); ax.set_ylim(0.8, 8)
ax.set_xlabel("F_s+"); ax.set_ylabel("F_c+")
ax.set_title("Octant ordering: crosses diagonal at (sqrt2+1, sqrt2+1)")
ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.savefig(f"{G}/b1_diagonal.png", dpi=110, bbox_inches="tight"); plt.close(fig)

# Fig 6: boundary zoom at sine-zero seam x=0
fig, ax = plt.subplots(figsize=(8, 4.5))
x = np.linspace(-1.2, 1.2, 6000); ok = np.abs(np.sin(2*x)) > 1e-4; x = x[ok]
ax.plot(x, Fs_p(x), lw=1.6, label="F_s+ : 0 from left, +inf from right")
ax.plot(x, Fs_m(x), lw=1.6, label="F_s- : +inf from left, 0 from right")
ax.plot(x, Fc_p(x), lw=1.6, label="F_c+ -> 1 both sides (regular)")
ax.plot(x, Fc_m(x), lw=1.6, label="F_c- -> 1 both sides (regular)")
ax.axvline(0, color="k", lw=0.8)
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-0.3, 6)
ax.set_title("Zero-pole exchange at a sine-zero seam; opposite channel regular at 1")
ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.savefig(f"{G}/b1_boundary.png", dpi=110, bbox_inches="tight"); plt.close(fig)

# Fig 7: unit circle with seam classes
fig, ax = plt.subplots(figsize=(5.5, 5.5))
th = np.linspace(0, 2*np.pi, 2000)
ax.plot(np.cos(th), np.sin(th), "k", lw=1.5)
seams = [(1,0,"[0]"), (0,1,"[pi/2]"), (-1,0,"[pi]"), (0,-1,"[3pi/2]")]
for (px, py, lab) in seams:
    ax.plot([px], [py], "ro", ms=9); ax.text(px*1.14, py*1.14, lab, fontsize=10, ha="center")
a0 = np.linspace(0, np.pi/2, 200)
ax.plot(np.cos(a0), np.sin(a0), lw=5, alpha=0.35, label="Q0")
ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.45, 1.45); ax.set_aspect("equal")
ax.set_title("Phase circle: 4 seam classes, quadrants Qk between")
ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.savefig(f"{G}/b1_circle.png", dpi=110, bbox_inches="tight"); plt.close(fig)

print("wrote PNGs to", G)
