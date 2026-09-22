"""Generate 7 static PNG fallbacks for the Book 11 rewrite page.
Every number plotted was verified in verify_book11.py (exact fractions / identities)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fractions import Fraction

OUT = "/home/hatch/workspace/r-theory-rewrite/book11/graphs"
plt.rcParams.update({"font.size": 11, "figure.dpi": 150})

def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)

# --- g1: helicity odds: cxp(arcsin b), crx(arcsin b), sqrt((1+b)/(1-b)) ---
b = np.linspace(-0.999, 0.999, 2001)
chi = np.arcsin(b)
cxp = np.abs(1/np.cos(chi)) + np.tan(chi)
crx = np.abs(1/np.cos(chi)) - np.tan(chi)
e_eta = np.sqrt((1+b)/(1-b))
# assertions: these must coincide
assert np.max(np.abs(cxp - e_eta)) < 1e-9
assert np.max(np.abs(cxp * crx - 1)) < 1e-9
fig, ax = plt.subplots(figsize=(7, 4.6))
ax.plot(b, cxp, label=r"$cxp(\chi)=e^{\eta}$", lw=2)
ax.plot(b, e_eta, "--", label=r"$\sqrt{(1+\beta)/(1-\beta)}$ (coincident)", lw=1.5)
ax.plot(b, crx, label=r"$crx(\chi)=e^{-\eta}=1/cxp$", lw=2)
ax.set_xlim(-1, 1); ax.set_ylim(0, 8)
ax.set_xlabel(r"$\beta$ (with $\sin\chi=\beta$)"); ax.set_ylabel("amplitude odds")
ax.set_title("Helicity amplitude odds: reciprocal pair on one reciprocal line")
ax.legend(fontsize=9); ax.grid(alpha=0.3)
save(fig, "g1_helicity_odds")

# --- g2: the six central weights ---
w = [Fraction(0), Fraction(1), Fraction(1,6), Fraction(-2,3), Fraction(1,3), Fraction(-1,2)]
labels = ["(1,1)_0", "(1,1)_{+1}", "(2,3)_{+1/6}", "(1,3b)_{-2/3}", "(1,3b)_{+1/3}", "(2,1)_{-1/2}"]
assert len(w) == 6
fig, ax = plt.subplots(figsize=(7, 4.6))
xs = np.arange(1, 7)
ax.scatter(xs, [float(x) for x in w], s=80, c="#1f77b4", zorder=3)
for i, lab in enumerate(labels):
    ax.annotate(lab, (xs[i], float(w[i])), textcoords="offset points", xytext=(6, 6), fontsize=9)
ax.axhline(0, color="k", lw=0.8)
ax.set_xlim(0.4, 7.2); ax.set_xticks(xs)
ax.set_xticklabels([f"block {i}" for i in xs])
ax.set_ylabel("central weight y(p,q) = p/2 - q/3")
ax.set_title("One generator, six forced weights (Theorem 11.IV.T2)")
ax.grid(alpha=0.3, axis="y")
save(fig, "g2_weights")

# --- g3: the 16 charge values Q = T3 + Y0 ---
charges = [Fraction(2,3)]*3 + [Fraction(-1,3)]*3 + [Fraction(-2,3)]*3 + \
          [Fraction(1,3)]*3 + [Fraction(0), Fraction(-1), Fraction(0), Fraction(1)]
assert len(charges) == 16, len(charges)
fig, ax = plt.subplots(figsize=(7, 4.6))
ax.scatter(range(1, 17), [float(c) for c in charges], s=60, c="#2ca02c", zorder=3)
ax.axhline(0, color="k", lw=0.8)
ax.set_xlim(0.5, 16.5); ax.set_xlabel("matter component (1..16)")
ax.set_ylabel("Q = T3 + Y0")
ax.set_title("Conditional electric-charge pattern of the 16 (Theorem 11.IX.T3)")
ax.grid(alpha=0.3, axis="y")
save(fig, "g3_charges")

# --- g4: integral lattice x(p,q) = 3p - 2q ---
xw = [0, 6, 1, -4, 2, -3]
assert all(3*p - 2*q == x for (p, q), x in zip([(0,0),(2,0),(1,1),(0,2),(2,2),(1,3)], xw))
fig, ax = plt.subplots(figsize=(7, 4.6))
ax.scatter(xs, xw, s=80, c="#d62728", zorder=3)
for i, lab in enumerate(labels):
    ax.annotate(lab, (xs[i], xw[i]), textcoords="offset points", xytext=(6, 6), fontsize=9)
ax.axhline(0, color="k", lw=0.8)
ax.set_xlim(0.4, 7.2); ax.set_xticks(xs)
ax.set_xticklabels([f"block {i}" for i in xs])
ax.set_ylabel("primitive integral weight x(p,q) = 3p - 2q")
ax.set_title("Integers under the fractions: one rescaling by 6 (Corollary 11.IX.C1)")
ax.grid(alpha=0.3, axis="y")
save(fig, "g4_integral_lattice")

# --- g5: U(1)^3 anomaly walking to zero ---
terms = [Fraction(1), Fraction(1,36), Fraction(-8,9), Fraction(1,9), Fraction(-1,4), Fraction(0)]
cum, acc = [], Fraction(0)
for t in terms:
    acc += t; cum.append(acc)
assert cum[-1] == 0 and cum[-2] == 0
fig, ax = plt.subplots(figsize=(7, 4.6))
xc = np.arange(1, 7)
ax.plot(xc, [float(c) for c in cum], "o-", lw=2, c="#9467bd")
ax.axhline(0, color="k", ls="--", lw=1)
ax.set_xlim(0.6, 6.4); ax.set_xticks(xc)
ax.set_xticklabels(["+1", "+1/36", "-8/9", "+1/9", "-1/4", "0"])
ax.set_xlabel("added block term")
ax.set_ylabel("cumulative U(1)^3 anomaly")
ax.set_title("Anomaly coefficient walks to exactly zero (Theorem 11.VI.T4)")
ax.grid(alpha=0.3)
save(fig, "g5_anomaly_walk")

# --- g6: Z6 kernel: 6th roots of unity ---
fig, ax = plt.subplots(figsize=(5.2, 5.2))
th = np.linspace(0, 2*np.pi, 400)
ax.plot(np.cos(th), np.sin(th), color="#999999")
roots = np.exp(2j*np.pi*np.arange(6)/6)
# assertion: these are exactly the kernel preimages' z values
assert all(abs(r**6 - 1) < 1e-12 for r in roots)
ax.scatter(roots.real, roots.imag, s=90, c="#1f77b4", zorder=3)
for k, r in enumerate(roots):
    ax.annotate(f"k={k}", (r.real, r.imag), textcoords="offset points", xytext=(6, 4), fontsize=9)
ax.set_aspect("equal"); ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
ax.axhline(0, color="k", lw=0.6); ax.axvline(0, color="k", lw=0.6)
ax.set_title("Kernel of the covering map: the six roots z^6=1 (Theorem 11.III.B)")
ax.grid(alpha=0.3)
save(fig, "g6_z6_kernel")

# --- g7: mirror pair: weights vs their sign-reversed conjugates ---
wm = [-x for x in w]
fig, ax = plt.subplots(figsize=(7, 4.6))
ax.scatter(xs, [float(x) for x in w], s=80, c="#1f77b4", label="S+ weights", zorder=3)
ax.scatter(xs, [float(x) for x in wm], s=80, c="#d62728", marker="x", label="mirror conjugates (S-)", zorder=3)
ax.axhline(0, color="k", lw=0.8)
ax.set_xlim(0.4, 7.2); ax.set_xticks(xs)
ax.set_xticklabels([f"block {i}" for i in xs])
ax.set_ylabel("central weight")
ax.set_title("The mirror pair: sign reversal maps pattern to pattern (11.V.D / 11.VI.N1)")
ax.legend(fontsize=9); ax.grid(alpha=0.3, axis="y")
save(fig, "g7_mirror_pair")

import os
files = sorted(os.listdir(OUT))
print(files)
for f in files:
    p = os.path.join(OUT, f)
    assert os.path.getsize(p) > 0, f
print("all 7 PNGs non-empty")
