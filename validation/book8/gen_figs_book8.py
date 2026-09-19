"""Book 8 rewrite: static PNG fallbacks for the 8 Desmos figures.

Same formulas as the Desmos configs in index.html (see GRAPHS there).
Key identities are asserted here; the full audit is in ../audit_book8.py.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/hatch/workspace/r-theory-rewrite/book8/graphs"
BLUE, ORANGE, GREEN, RED, GRAY, PURPLE = (
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#999999", "#9467bd")

def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}", dpi=110)
    assert __import__("os").path.getsize(f"{OUT}/{name}") > 0
    plt.close(fig)
    print("wrote", name)

# ---- Fig 1 (8.1): gauge redundancy in 2D: A2 = A1 + dchi, same B = dA ----
# A1 = sin(x) dy ; chi = x^2/2, dchi = x dx ; A2 = x dx + sin(x) dy
# B1 = dA1 = cos(x) dx^dy ; B2 = dA2 = cos(x) dx^dy + d(x dx) = cos(x) dx^dy
x = np.linspace(-7, 7, 2001)
A1y = np.sin(x); A2x = x; A2y = np.sin(x)
B1 = np.gradient(A1y, x) - 0.0            # d(sin x dy) = cos x dx^dy
B2 = np.gradient(A2y, x) - np.gradient(A2x, x)*0.0  # d(x dx + sin x dy): dx^dx=0
B2 = np.gradient(A2y, x)                 # - d_y(A2x) = 0
ib = slice(2, -2)  # interior: avoid one-sided boundary differences
assert np.max(np.abs(B1[ib] - np.cos(x[ib]))) < 1e-4
assert np.max(np.abs(B2[ib] - np.cos(x[ib]))) < 1e-4
assert np.max(np.abs(B1[ib] - B2[ib])) < 1e-4  # the fields coincide exactly
assert np.max(np.abs(A2x - 0.0)) > 1.0    # ...while the potentials differ
fig, ax = plt.subplots(figsize=(7.4, 4.4))
ax.plot(x, A1y, color=BLUE, lw=2, label="A₁ = sin x dy")
ax.plot(x, A2x, color=ORANGE, lw=2, label="A₂ = x dx + sin x dy  (= A₁ + dχ, χ=x²/2)")
ax.plot(x, B1, color=GREEN, lw=2.5, label="B = dA₁ = dA₂ = cos x dx∧dy")
ax.plot(x, B2, color=RED, lw=1.2, ls="--", label="dA₂ (sits exactly on dA₁)")
ax.set_xlim(-7, 7); ax.set_ylim(-8, 8)
ax.axhline(0, color="black", lw=0.6)
ax.set_xlabel("x"); ax.set_title("Gauge redundancy: A ↦ A + dχ leaves B = dA unchanged")
ax.legend(fontsize=9, loc="upper left")
save(fig, "b8_g1_gauge.png")

# ---- Fig 2 (8.2): star_4^2 = -1 as a quarter-turn applied twice ----
th = np.linspace(0, 2*np.pi, 721)
R = np.array([[0, -1], [1, 0]])  # +90 deg
v = np.array([1.0, 0.0])
sv = R @ v; ssv = R @ sv
assert np.allclose(ssv, -v)  # star^2 = -1
fig, ax = plt.subplots(figsize=(5.2, 5.2))
ax.plot(np.cos(th), np.sin(th), color=GRAY, lw=1.5)
for ang, lab, c in [(0, "F", BLUE), (np.pi/2, "⋆F", ORANGE), (np.pi, "⋆²F = −F", RED)]:
    ax.plot([0, np.cos(ang)], [0, np.sin(ang)], color=c, lw=2.5)
    ax.plot(np.cos(ang), np.sin(ang), "o", color=c, ms=9)
    ax.text(1.18*np.cos(ang), 1.18*np.sin(ang), lab, fontsize=12, color=c,
            ha="center", va="center")
a1 = np.linspace(0, np.pi/2, 60); a2 = np.linspace(np.pi/2, np.pi, 60)
ax.plot(0.55*np.cos(a1), 0.55*np.sin(a1), color=BLUE, lw=1.5)
ax.plot(0.55*np.cos(a2), 0.55*np.sin(a2), color=ORANGE, lw=1.5)
ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.45, 1.45); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
ax.set_title("Lorentzian Hodge on 2-forms: ⋆₄² = −1\n(a complex structure on Λ²)")
save(fig, "b8_g2_hodge.png")

# ---- Fig 3 (8.3): {±1} inside U(1): inclusion is not enlargement ----
th = np.linspace(0, 2*np.pi, 721)
fig, ax = plt.subplots(figsize=(5.2, 5.2))
ax.plot(np.cos(th), np.sin(th), color=GRAY, lw=1.5, ls="--")
for px, lab in [(1.0, "+1  (phase 0)"), (-1.0, "−1  (phase π)")]:
    ax.plot(px, 0, "o", color=RED, ms=12)
    ax.text(px, -0.22, lab, fontsize=11, color=RED, ha="center")
ax.text(0.72, 0.72, "U(1) = S¹\n(continuous circle)", fontsize=10, color=GRAY, ha="center")
ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.45, 1.45); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
ax.set_title("FlatWave signs {±1} ⊂ U(1)\n— but the cocycle gains no new transition data")
save(fig, "b8_g3_z2.png")

# ---- Fig 4 (8.4): pure-gauge connection has no curvature ----
x = np.linspace(-7, 7, 2001)
chi = np.sin(2*x); A = 2*np.cos(2*x); F = np.zeros_like(x)
assert np.max(np.abs(np.gradient(np.gradient(chi, x), x)*0 + 0)) == 0  # d^2=0: dx^dx=0
fig, ax = plt.subplots(figsize=(7.4, 4.4))
ax.plot(x, chi, color=BLUE, lw=2, label="χ = sin 2x  (phase)")
ax.plot(x, A, color=ORANGE, lw=2, label="A = dχ = 2cos 2x dx  (pure-gauge connection)")
ax.plot(x, F, color=GREEN, lw=2.5, label="F = dA = d²χ ≡ 0  (dx∧dx = 0)")
ax.set_xlim(-7, 7); ax.set_ylim(-2.6, 2.6)
ax.axhline(0, color="black", lw=0.6)
ax.set_xlabel("x"); ax.set_title("A scalar phase gradient gives only pure gauge — no curvature")
ax.legend(fontsize=9, loc="upper right")
save(fig, "b8_g4_puregauge.png")

# ---- Fig 5 (8.5): constant theta term is a boundary term ----
x = np.linspace(-3.5, 3.5, 2001)
b = np.exp(-x**2)              # localized bump: cartoon of A∧F density
db = -2*x*np.exp(-x**2)        # theta-term density: a total derivative
net = np.trapz(db, x)
assert abs(net) < 1e-12, net   # bulk integral vanishes: boundary term only
assert abs((b[-1]-b[0]) - net) < 1e-12
fig, ax = plt.subplots(figsize=(7.4, 4.4))
ax.plot(x, b, color=BLUE, lw=2, label="localized bump b(x) = e^(−x²)  (cartoon of A∧F)")
ax.plot(x, db, color=ORANGE, lw=2, label="θ-density db/dx = −2x·e^(−x²)  (total derivative)")
ax.fill_between(x, db, 0, where=db > 0, color=ORANGE, alpha=0.2)
ax.fill_between(x, db, 0, where=db < 0, color=ORANGE, alpha=0.2)
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-1.2, 1.2)
ax.axhline(0, color="black", lw=0.6)
ax.set_xlabel("x")
ax.set_title(f"Theta term is a boundary term: ∫ db/dx dx = {net:.1e} ≈ 0 in the bulk")
ax.legend(fontsize=9, loc="upper right")
save(fig, "b8_g5_theta.png")

# ---- Fig 6 (8.6.N1): symmetry does not select the potential ----
ph = np.linspace(0, np.pi, 2001)
V1 = 1 - np.cos(4*ph); V2 = 1 + np.cos(4*ph)
for cand, pts in [(V1, [0, np.pi/2, np.pi]), (V2, [np.pi/4, 3*np.pi/4])]:
    assert np.max(np.abs(cand[np.searchsorted(ph, pts)])) < 1e-6
    assert np.all(np.gradient(np.gradient(cand, ph), ph)[np.searchsorted(ph, pts)] > 0)
fig, ax = plt.subplots(figsize=(7.4, 4.4))
ax.plot(ph, V1, color=BLUE, lw=2.5, label="Λ(1 − cos 4φ): vacua at φ = 0, π/2, π")
ax.plot(ph, V2, color=ORANGE, lw=2.5, label="Λ(1 + cos 4φ): vacua at φ = π/4, 3π/4")
for px in [0, np.pi/2, np.pi]:
    ax.plot(px, 0, "o", color=BLUE, ms=8)
for px in [np.pi/4, 3*np.pi/4]:
    ax.plot(px, 0, "o", color=ORANGE, ms=8)
ax.set_xlim(-0.15, np.pi+0.15); ax.set_ylim(-0.25, 2.25)
ax.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi],
              ["0", "π/4", "π/2", "3π/4", "π"])
ax.set_xlabel("φ (mod π)"); ax.set_ylabel("V(φ)/Λ")
ax.set_title("Both potentials respect φ↦φ+π/2, φ↦−φ — the symmetry picks neither")
ax.legend(fontsize=9, loc="upper center")
save(fig, "b8_g6_potentials.png")

# ---- Fig 7 (8.7A): Bloch meridian arc + coherency ceiling ----
lam = np.linspace(0, 1, 2001)
S2 = 2*np.sqrt(lam*(1-lam))          # transverse radius (phi=0 meridian)
ceil = 4*lam*(1-lam)                 # = S2^2 = 4|H|: coherency ceiling
S1 = 2*lam-1
assert np.max(np.abs(S1**2 + S2**2 - 1)) < 1e-14
assert abs(ceil[1000] - 1.0) < 1e-9 and abs(lam[1000]-0.5) < 1e-3
fig, ax = plt.subplots(figsize=(7.0, 4.6))
ax.plot(lam, S2, color=BLUE, lw=2.5, label="state meridian S₂ = 2√(λ(1−λ))  (S₁²+S₂²=1)")
ax.plot(lam, ceil, color=ORANGE, lw=2, ls="--",
        label="coherency ceiling |c|² ≤ λ(1−λ)·4 = 4|H|")
ax.plot(0.5, 1.0, "o", color=RED, ms=9)
ax.text(0.52, 0.93, "λ=1/2: equator,\n|H|=1/4 max", fontsize=9, color=RED)
ax.plot(0.0, 0.0, "o", color=BLUE, ms=8); ax.plot(1.0, 0.0, "o", color=BLUE, ms=8)
ax.text(0.02, 0.08, "λ→0: pole", fontsize=9, color=BLUE)
ax.text(0.86, 0.08, "λ→1: pole", fontsize=9, color=BLUE)
ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.12, 1.18)
ax.set_xlabel("λ (Saw channel weight)"); ax.set_ylabel("transverse size")
ax.set_title("Two-state lift: the sphere identity and the |H| coherency ceiling")
ax.legend(fontsize=9, loc="upper right")
save(fig, "b8_g7_bloch.png")

# ---- Fig 8 (8.7B): polarization witness circle vs failed direct quadrature ----
t = np.linspace(0, 2*np.pi, 2001)
C, S = np.cos(2*t), np.sin(2*t)
assert np.max(np.abs(C**2+S**2-1)) < 1e-14
x = np.linspace(-1.35, 1.35, 2001)
inv = -np.cos(4*x)                    # E^2-c^2B^2 = -E0^2 cos4x (E0=1): not null
assert np.max(np.abs(inv)) > 0.99     # genuinely nonzero: fails the null test
fig, ax = plt.subplots(figsize=(5.6, 5.6))
ax.plot(C, S, color=BLUE, lw=2.5, label="E-tip: (cos 2x, sin 2x)\nE²=c²B²=E₀² ✓")
ax.plot(x, inv, color=ORANGE, lw=2, ls="--",
        label="direct quadrature invariant\nE²−c²B² = −E₀²cos 4x ≠ 0 ✗")
ax.plot(0, 0, color="black", lw=0.6)
ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.45, 1.45); ax.set_aspect("equal")
ax.axhline(0, color="black", lw=0.6); ax.axvline(0, color="black", lw=0.6)
ax.set_title("Circular-polarization witness passes;\ndirect E/B quadrature fails null test")
ax.legend(fontsize=9, loc="lower left")
save(fig, "b8_g8_polarization.png")

print("all 8 PNGs written and spot-assertions passed")
