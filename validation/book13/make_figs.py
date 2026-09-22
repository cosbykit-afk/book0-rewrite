#!/usr/bin/env python3
"""Book 13 figure fallbacks. Every plotted expression is the same formula that
the Desmos config targets; key numbers are asserted before saving.
Outputs: /home/hatch/workspace/r-theory-rewrite/book13/graphs/g1..g7_*.png"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "/home/hatch/workspace/r-theory-rewrite/book13/graphs"
os.makedirs(OUT, exist_ok=True)
BLUE, ORANGE, GREEN, RED, PURPLE = "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"

def check(name, cond):
    assert bool(cond), f"FIGURE CHECK FAILED: {name}"

def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=100, bbox_inches="tight")
    plt.close(fig)
    assert os.path.getsize(p) > 0, f"empty PNG {name}"
    print("wrote", p, os.path.getsize(p), "bytes")

lam  = lambda x: (1 + np.sin(x) - np.cos(x)) / 2
Ssys = lambda l: -(l*np.log(l) + (1-l)*np.log(1-l))  # /kB

# ---- g1: transfer coordinate on the principal quadrant
x = np.linspace(0.02, np.pi/2 - 0.02, 800)
l = lam(x)
check("g1 lam(0+)->0", l[0] < 0.03); check("g1 lam(pi/2-)->1", l[-1] > 0.97)
check("g1 lam(pi/4)=1/2", abs(lam(np.pi/4) - 0.5) < 1e-12)
fig, ax = plt.subplots(figsize=(12, 7.2))
ax.plot(x, l, color=BLUE, lw=2.5, label="λ(x) = (1+sin x − cos x)/2")
ax.plot(x, 1-l, color=ORANGE, lw=2.5, label="1 − λ(x)")
ax.axvline(np.pi/4, color="gray", ls="--", lw=1); ax.axhline(0.5, color="gray", ls="--", lw=1)
ax.set_xlim(0, np.pi/2); ax.set_ylim(-0.05, 1.05)
ax.set_xlabel("x"); ax.set_title("Figure 1 — The transfer coordinate λ on the admissible quadrant (0, π/2)")
ax.legend(); save(fig, "g1_lambda.png")

# ---- g2: reciprocal access urx=1/λ, uxp=1/(1−λ)
x = np.linspace(0.06, np.pi/2 - 0.03, 800)
ur, up = 1/lam(x), 1/(1-lam(x))
check("g2 urx=1/lam spot", abs(ur[400] - 1/lam(x[400])) < 1e-12)
fig, ax = plt.subplots(figsize=(12, 7.2))
ax.plot(x, ur, color=BLUE, lw=2.5, label="urx = 1/λ")
ax.plot(x, up, color=ORANGE, lw=2.5, label="uxp = 1/(1−λ)")
ax.set_xlim(0, np.pi/2); ax.set_ylim(0, 14)
ax.set_xlabel("x"); ax.set_title("Figure 2 — Reciprocal access: urx = ε/λ, uxp = ε/(1−λ), ε=+1 here")
ax.legend(); save(fig, "g2_reciprocal.png")

# ---- g3: Bernoulli entropy and |H| vs λ
l = np.linspace(0.005, 0.995, 800)
S = Ssys(l); Hh = l*(1-l)
check("g3 S(1/2)=ln2", abs(Ssys(0.5) - np.log(2)) < 1e-12)
check("g3 |H|max=1/4", abs(Hh.max() - 0.25) < 1e-6)
fig, ax = plt.subplots(figsize=(12, 7.2))
ax.plot(l, S, color=BLUE, lw=2.5, label="S_sys/kB = −[λ ln λ + (1−λ) ln(1−λ)]")
ax.plot(l, Hh, color=GREEN, lw=2.5, label="|H| = λ(1−λ)")
ax.axvline(0.5, color="gray", ls="--", lw=1)
ax.set_xlim(0, 1); ax.set_ylim(-0.02, 0.8)
ax.set_xlabel("λ"); ax.set_title("Figure 3 — Binary entropy and the response kernel |H| vs λ")
ax.legend(); save(fig, "g3_entropy.png")

# ---- g4: convex generator A(v)
v = np.linspace(-6, 6, 800)
A = np.log(1+np.exp(v)); Ap = np.exp(v)/(1+np.exp(v)); App = Ap*(1-Ap)
check("g4 A(0)=ln2", abs(np.log(2) - np.log(1+np.exp(0))) < 1e-14)
check("g4 A'' max 1/4 at v=0", abs(App[len(v)//2] - 0.25) < 1e-3)
fig, ax = plt.subplots(figsize=(12, 7.2))
ax.plot(v, A, color=BLUE, lw=2.5, label="A(v) = ln(1+e^v)")
ax.plot(v, Ap, color=ORANGE, lw=2.5, label="A′(v) = λ(v)")
ax.plot(v, App, color=GREEN, lw=2.5, label="A′′(v) = λ(1−λ) = |H|")
ax.set_xlim(-6, 6); ax.set_ylim(-0.05, 6.5)
ax.set_xlabel("v = logit(λ)"); ax.set_title("Figure 4 — The Bernoulli generator and its derivatives")
ax.legend(); save(fig, "g4_generator.png")

# ---- g5: Fisher angle compactification
v = np.linspace(-8, 8, 800)
phi = 2*np.arctan(np.exp(v/2))
check("g5 phi(0)=pi/2", abs(2*np.arctan(1) - np.pi/2) < 1e-14)
check("g5 phi->(0,pi)", phi[0] < 0.05 and phi[-1] > np.pi - 0.05)
fig, ax = plt.subplots(figsize=(12, 7.2))
ax.plot(v, phi, color=PURPLE, lw=2.5, label="φ_F(v) = 2 arctan(e^{v/2})")
ax.axhline(0, color="gray", ls="--", lw=1); ax.axhline(np.pi, color="gray", ls="--", lw=1)
ax.set_xlim(-8, 8); ax.set_ylim(-0.15, np.pi + 0.15)
ax.set_xlabel("v"); ax.set_title("Figure 5 — Fisher-angle compactification: v ∈ ℝ ↦ φ_F ∈ (0, π)")
ax.legend(); save(fig, "g5_fisherangle.png")

# ---- g6: two-level thermal bridge (equal multiplicities): Schottky heat capacity
t = np.linspace(0.05, 3.0, 800)  # t = kT/Δ
bv = 1/t
lamt = np.exp(bv)/(1+np.exp(bv))
C = bv**2 * lamt * (1-lamt)  # C/kB
imax = np.argmax(C)
check("g6 Schottky peak near kT/Δ≈0.42", abs(t[imax] - 0.417) < 0.02)
check("g6 C->0 at both ends", C[0] < 0.05 and C[-1] < 0.15)
fig, ax = plt.subplots(figsize=(12, 7.2))
ax.plot(t, C, color=RED, lw=2.5, label="C/kB = (βΔ)²|H|")
ax.plot(t, lamt, color=BLUE, lw=2.5, ls="--", label="λ(T) (equal multiplicities)")
ax.set_xlim(0, 3); ax.set_ylim(-0.02, 0.5)
ax.set_xlabel("kT/Δ"); ax.set_title("Figure 6 — Canonical bridge: Schottky heat capacity and λ(T)")
ax.legend(); save(fig, "g6_schottky.png")

# ---- g7: two-ended entropy along x (the arrow obstruction, drawn)
x = np.linspace(0.02, np.pi/2 - 0.02, 800)
Sx = Ssys(lam(x))
check("g7 symmetric about pi/4", np.max(np.abs(Sx - Sx[::-1])) < 1e-12)
check("g7 ends->0, middle=ln2", Sx[0] < 0.1 and Sx[-1] < 0.1 and abs(Sx.max()-np.log(2)) < 1e-3)
fig, ax = plt.subplots(figsize=(12, 7.2))
ax.plot(x, Sx, color=BLUE, lw=2.5, label="S_sys(x)/kB")
ax.axvline(np.pi/4, color="gray", ls="--", lw=1)
ax.annotate("past?", xy=(0.1, 0.15), fontsize=12, color="#8a5a00")
ax.annotate("future?", xy=(np.pi/2-0.35, 0.15), fontsize=12, color="#8a5a00")
ax.set_xlim(0, np.pi/2); ax.set_ylim(-0.02, 0.75)
ax.set_xlabel("x"); ax.set_title("Figure 7 — Two-ended entropy: S→0 at both ends, max at midpoint — no endpoint is picked out")
ax.legend(); save(fig, "g7_twoended.png")

print("ALL FIGURE CHECKS PASSED")
