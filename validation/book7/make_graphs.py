#!/usr/bin/env python3
"""Book 7 static PNG fallbacks. Every plotted expression numerically verified
in verify_book7.py before plotting."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/hatch/workspace/r-theory-rewrite/book7/graphs/"
import os
os.makedirs(OUT, exist_ok=True)

def srx(x): return np.abs(1/np.sin(x)) + np.cos(x)/np.sin(x)
def cxp(x): return np.abs(1/np.cos(x)) + np.sin(x)/np.cos(x)
def crx(x): return 1/cxp(x)
def sxp(x): return 1/srx(x)
def urx(x): return srx(x) - crx(x)
def uxp(x): return cxp(x) - sxp(x)

plt.rcParams.update({"font.size": 11})

# ---- g1: saw balance product (7.1.T1) ----
x = np.linspace(0.03, np.pi/2 - 0.03, 2000)
lam = (1 + np.sin(x) - np.cos(x))/2
H = np.sin(2*x)/4
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(x, lam, color="#2ca02c", label=r"$\lambda$ (channel 1)")
ax.plot(x, 1-lam, color="#d62728", label=r"$1-\lambda$ (channel 2)")
ax.plot(x, lam*(1-lam), color="#ff7f0e", lw=2.5, label=r"$|H|=\lambda(1-\lambda)$")
ax.plot(x, H, color="#1f77b4", ls="--", lw=2, label=r"$H=\sin(2x)/4$")
ax.axhline(0.25, color="gray", ls=":", label="1/4 bound")
ax.set_title("Saw balance-product identity  $H=\\epsilon\\lambda(1-\\lambda)$  (7.1.T1)")
ax.set_xlabel("x"); ax.legend(loc="upper right", fontsize=9)
fig.tight_layout(); fig.savefig(OUT+"g1_balance.png", dpi=110); plt.close(fig)

# ---- g2: companion cosine (7.1.T2) ----
x = np.linspace(0.03, np.pi - 0.03, 3000)
eps = np.sign(np.sin(2*x))
lam = eps*(1/urx(x))
env = np.sqrt(1 + 4*lam*(1-lam))
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(x, env, color="#2ca02c", ls="--", label=r"envelope $\sqrt{1+4\lambda(1-\lambda)}$")
ax.plot(x, -env, color="#2ca02c", ls="--")
ax.plot(x, np.cos(2*x), color="#1f77b4", lw=2.5, label=r"$\cos(2x)$")
ax.plot(x, eps*(1-2*lam), color="#ff7f0e", ls=":", lw=2,
        label=r"$\epsilon(1-2\lambda)$ (imbalance, not the cosine)")
ax.set_title("Companion cosine: directed imbalance x envelope  (7.1.T2)")
ax.set_xlabel("x"); ax.legend(loc="upper right", fontsize=9)
fig.tight_layout(); fig.savefig(OUT+"g2_cosine.png", dpi=110); plt.close(fig)

# ---- g3: carrier phasor (7.1.T3) ----
t = np.linspace(0, 2*np.pi, 2000)
fig, ax = plt.subplots(figsize=(5.2, 5.2))
ax.plot(np.cos(2*t), np.sin(2*t), color="#1f77b4", lw=2, label=r"$Z=C+iS=e^{2ix}$")
ax.set_aspect("equal"); ax.axhline(0, color="gray", lw=0.5); ax.axvline(0, color="gray", lw=0.5)
ax.set_title("Carrier phasor: normalized double-angle circle  (7.1.T3)")
ax.set_xlabel("C = cos 2x"); ax.set_ylabel("S = sin 2x"); ax.legend()
fig.tight_layout(); fig.savefig(OUT+"g3_phasor.png", dpi=110); plt.close(fig)

# ---- g4: transfer-circle squaring map (7.1.T4) ----
t = np.linspace(0.03, np.pi/2 - 0.03, 2000)
al = np.sign(np.sin(t)); be = np.sign(np.cos(t))
p = al*np.cos(t) - be*np.sin(t); q = al*np.sin(t) + be*np.cos(t)
a, b = q/np.sqrt(2), p/np.sqrt(2)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.4))
ax1.plot(a, b, color="#1f77b4", lw=2); ax1.set_aspect("equal")
ax1.set_title(r"transfer pair $\zeta=a+ib$, $a^2+b^2=1$")
ax1.set_xlabel("a"); ax1.set_ylabel("b")
U = np.sin(2*t); W = np.cos(2*t)
ax2.plot(U, W, color="#ff7f0e", lw=2); ax2.set_aspect("equal")
ax2.set_title(r"quadratic image $U+iW=\epsilon\,\zeta^2$")
ax2.set_xlabel("U = sin 2x"); ax2.set_ylabel("W = cos 2x")
fig.suptitle("Transfer-circle squaring map  (7.1.T4)")
fig.tight_layout(); fig.savefig(OUT+"g4_squaring.png", dpi=110); plt.close(fig)

# ---- g5: primitive decomposition (7.2.T1/T2) ----
x = np.linspace(0.06, np.pi/2 - 0.06, 3000)
Pp = 1/(urx(x) + uxp(x))
Vm = 2*(1/(cxp(x)+crx(x))**2 - 1/(srx(x)+sxp(x))**2)
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(x, Pp, color="#1f77b4", lw=2.5, label=r"$P=1/(urx+uxp)$")
ax.plot(x, np.sin(2*x)/4, color="#1f77b4", ls="--", label=r"$\sin(2x)/4$")
ax.plot(x, Vm, color="#2ca02c", lw=2.5, label=r"$V=2[1/(cxp+crx)^2-1/(srx+sxp)^2]$")
ax.plot(x, np.cos(2*x)/2, color="#2ca02c", ls="--", label=r"$\cos(2x)/2$")
ax.set_title("Primitive decomposition of the double-angle carrier  (7.2.T1, 7.2.T2)")
ax.set_xlabel("x"); ax.legend(fontsize=9)
fig.tight_layout(); fig.savefig(OUT+"g5_primitive.png", dpi=110); plt.close(fig)

# ---- g6: carrier flow + conserved ellipse (7.3) ----
fig, ax = plt.subplots(figsize=(5.4, 5.4))
th = np.linspace(0, 2*np.pi, 400)
ax.plot(np.sin(th)/2, np.cos(th)/2, color="#1f77b4", lw=2, label=r"$V^2+4P^2=1/4$")
Pg, Vg = np.meshgrid(np.linspace(-0.32, 0.32, 14), np.linspace(-0.62, 0.62, 14))
ax.quiver(Pg, Vg, Vg, -4*Pg, color="#999999", alpha=0.55, width=0.004)
t = np.linspace(0, np.pi, 9)
ax.plot(np.sin(2*t)/4, np.cos(2*t)/2, "o", color="#d62728", ms=4)
ax.set_aspect("equal")
ax.set_title("Closed carrier flow  $P'=V$, $V'=-4P$  (7.3.T1)")
ax.set_xlabel("P"); ax.set_ylabel("V"); ax.legend()
fig.tight_layout(); fig.savefig(OUT+"g6_flow.png", dpi=110); plt.close(fig)

# ---- g7: hyperbolic parent -> projective circle (7.4) ----
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4.4))
Sg = np.linspace(4.01, 12, 2000)
ax1.plot(Sg, np.sqrt(Sg**2-16), color="#1f77b4", lw=2)
ax1.plot(Sg, -np.sqrt(Sg**2-16), color="#1f77b4", lw=2)
ax1.plot(-Sg, np.sqrt(Sg**2-16), color="#9467bd", lw=2)
ax1.plot(-Sg, -np.sqrt(Sg**2-16), color="#9467bd", lw=2)
xx = np.linspace(-12, 12, 400)
ax1.plot(xx, xx, color="gray", ls="--", lw=0.8); ax1.plot(xx, -xx, color="gray", ls="--", lw=0.8)
ax1.set_title(r"hyperbolic parent $\Sigma^2-\Delta^2=16$")
ax1.set_xlabel(r"$\Sigma$"); ax1.set_ylabel(r"$\Delta$")
t = np.linspace(0, 2*np.pi, 2000)
ax2.plot(np.cos(2*t), np.sin(2*t), color="#ff7f0e", lw=2)
ax2.set_aspect("equal")
ax2.set_title(r"projective image $(Q,S)=(\Delta/\Sigma,\,4/\Sigma)$, $Q^2+S^2=1$")
ax2.set_xlabel("Q = cos 2x"); ax2.set_ylabel("S = sin 2x")
fig.suptitle("Hyperbolic parent and projective double-angle completion  (7.4.T1, 7.4.T2)")
fig.tight_layout(); fig.savefig(OUT+"g7_hyperbola.png", dpi=110); plt.close(fig)

print("wrote 7 PNGs")
