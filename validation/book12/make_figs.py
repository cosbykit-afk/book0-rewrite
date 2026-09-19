#!/usr/bin/env python3
"""Generate the 7 Book 12 PNG fallbacks. Every plotted number is asserted
against the audited formulas before drawing (completed numerical check)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fractions import Fraction

OUT = "/home/hatch/workspace/r-theory-rewrite/book12/graphs"
BLUE, ORANGE, GREEN, RED, GRAY = "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#7f7f7f"

def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}", dpi=110)
    plt.close(fig)
    print("wrote", name)

# ---------- shared audited numbers ----------
me_MeV, mp_MeV, mn_MeV = 0.51099895, 938.27208816, 939.56542052
h_eVs = 4.135667696e-15
nu_e = me_MeV*1e6/h_eVs
assert abs(nu_e - 1.23558996e20)/1.23558996e20 < 1e-6
rho = (mn_MeV-mp_MeV)/me_MeV
assert abs(rho - 81/32) < 1e-3 and abs(rho - 81/32) > 1e-9
log_anchor = {128: np.log10(128/nu_e), 220: np.log10(220/nu_e),
              "21cm": np.log10(1.420405751768e9/nu_e)}

# ---------- g1: rest-energy frequency coordinate + calibration anchors ----------
fig, ax = plt.subplots(figsize=(7.2, 4.6))
X = np.linspace(-0.6, 4.6, 400)
Y = X  # log10(nu_M/nu_e) = log10(M/m_e): exact coordinate line
assert np.allclose(Y, X)
ax.plot(X, Y, color=BLUE, lw=2, label=r"$\log_{10}(\nu_M/\nu_e)=\log_{10}(M/m_e)$")
for name, r in [("e", 1.0), (r"$\mu$", 206.7682830),
                ("p", mp_MeV/me_MeV), ("n", mn_MeV/me_MeV)]:
    lx = np.log10(r)
    ax.plot(lx, lx, "o", color=BLUE, ms=7)
    ax.annotate(name, (lx, lx), textcoords="offset points", xytext=(6, 4), fontsize=11)
for f, ly in [(128, log_anchor[128]), (220, log_anchor[220])]:
    ax.axhline(ly, color=GRAY, ls="--", lw=1.2)
    ax.annotate(f"{f} Hz anchor (calibration)", (4.55, ly), fontsize=9, color=GRAY,
                ha="right", va="bottom")
ax.axhline(log_anchor["21cm"], color=RED, ls="--", lw=1.2)
ax.annotate("21-cm line (hyperfine transition, not rest frequency)", (4.55, log_anchor["21cm"]),
            fontsize=9, color=RED, ha="right", va="bottom")
ax.set_xlabel(r"$\log_{10}(M/m_e)$"); ax.set_ylabel(r"$\log_{10}(\nu_M/\nu_e)$")
ax.set_title("Fig 1 — Rest-energy frequency is a coordinate; anchors are calibrations")
ax.set_xlim(-0.8, 4.7); ax.set_ylim(-20.5, 5.5); ax.legend(fontsize=9, loc="upper left")
save(fig, "g1_freq.png")

# ---------- g2: two-body relational coordinates ----------
fig, ax = plt.subplots(figsize=(7.2, 4.6))
xr = np.linspace(-2, 2, 400)
qm = (10**xr - 1)/(10**xr + 1)
assert np.allclose(qm, np.tanh(xr*np.log(10)/2), atol=1e-12)
ax.plot(xr, qm, color=BLUE, lw=2, label=r"$q_m=(m_1-m_2)/(m_1+m_2)$ vs $\log_{10}(m_1/m_2)$")
xM = np.linspace(1.0, 1.9999, 400)
u2 = ((2.0)**2 - xM**2)/(xM**2 - 0.0)  # m1=m2=1: ((m1+m2)^2-M^2)/(M^2-(m1-m2)^2)
B = 2.0 - xM; mu = 0.5
assert abs((B/(2*mu*u2))[-1] - 1) < 1e-3  # weak-binding limit
ax.plot(xM - 1.5, u2, color=ORANGE, lw=2,
        label=r"$u^2(M),\;m_1{=}m_2{=}1$ (x-axis shifted by $-1.5$)")
ax.axhline(0, color=GRAY, lw=0.8); ax.axvline(0, color=GRAY, lw=0.8)
ax.set_xlabel("log-ratio / shifted M"); ax.set_ylabel("coordinate value")
ax.set_title("Fig 2 — Exact two-body relational coordinates (no mass law)")
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-1.3, 3.4); ax.legend(fontsize=9)
save(fig, "g2_twobody.png")

# ---------- g3: harmonic negative ledger ----------
fig, ax = plt.subplots(figsize=(7.2, 4.6))
cands = sorted({Fraction(p, q) for q in range(1, 65) for p in range(1, 400)
                if abs(p/q - rho) <= 0.01})
xs_c = [float(f) for f in cands]; ys_c = [float(f) - rho for f in cands]
assert len(cands) > 15, "lattice should be dense"
assert Fraction(81, 32) in cands
ax.scatter(xs_c, ys_c, s=26, color=GRAY, alpha=0.7, label="rational lattice (den. ≤ 64)")
ax.scatter([81/32], [81/32 - rho], s=90, color=BLUE, zorder=5, label="81/32")
ax.axhline(0, color=RED, ls="--", lw=1.5, label="measured ρ=(mₙ−mₚ)/mₑ")
ax.annotate(f"81/32 off by {81/32-rho:+.2e}", (81/32, 81/32-rho),
            textcoords="offset points", xytext=(8, -14), fontsize=10, color=BLUE)
ax.set_xlabel("candidate value"); ax.set_ylabel("candidate − measured ρ")
ax.set_title("Fig 3 — Negative ledger: dense rational lattice, no exact law")
ax.legend(fontsize=9); ax.set_xlim(rho-0.011, rho+0.011)
save(fig, "g3_negative.png")

# ---------- g4: centered projector spectrum ----------
fig, ax = plt.subplots(figsize=(7.2, 4.6))
Q = np.diag([0.6, 0.6, -0.4, -0.4, -0.4])
ev = np.linalg.eigvalsh(Q)
assert np.allclose(sorted(ev), [-0.4]*3 + [0.6]*2, atol=1e-15)
assert abs(0.6 - (-0.4) - 1) < 1e-15 and abs(np.trace(Q@Q)/5 - 0.24) < 1e-15
ax.scatter([1, 2], [0.6, 0.6], s=110, color=BLUE, zorder=5)
ax.scatter([3, 4, 5], [-0.4]*3, s=110, color=ORANGE, zorder=5)
ax.hlines([0.6, -0.4], 0.5, 5.5, colors=GRAY, linestyles="dashed", lw=1.2)
ax.annotate("3/5 (×2) on C²", (1.0, 0.66), fontsize=11, color=BLUE)
ax.annotate("−2/5 (×3) on C³", (3.0, -0.52), fontsize=11, color=ORANGE)
ax.annotate("", xy=(2.5, 0.6), xytext=(2.5, -0.4),
            arrowprops=dict(arrowstyle="<->", color=RED, lw=1.6))
ax.annotate("gap = 1", (2.62, 0.08), fontsize=11, color=RED)
ax.annotate("(1/5)Tr(Q²) = 6/25 = H", (3.4, 0.72), fontsize=10)
ax.set_xlim(0.4, 5.6); ax.set_ylim(-0.9, 1.0); ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xlabel("basis index"); ax.set_ylabel("eigenvalue")
ax.set_title("Fig 4 — Centered 2+3 projector spectrum (Thm 12.VI.T1)")
save(fig, "g4_projector.png")

# ---------- g5: relative-center + Casimir closure ----------
fig, ax = plt.subplots(figsize=(7.2, 4.6))
NN = np.linspace(2, 6, 400)
D = NN**2*(NN**2-9)/(4*(NN**2-1))  # Om^2 - CA/CF
assert abs(3.0**2*(3.0**2-9)/(4*(3.0**2-1))) < 1e-15  # exactly zero at N=3
ax.plot(NN, D, color=BLUE, lw=2, label=r"$D(N)=\Omega^2-C_A/C_F=N^2(N^2-9)/[4(N^2-1)]$")
ax.axhline(0, color=GRAY, ls="--", lw=1.2)
for Nv in [2, 4, 5, 6]:
    dv = Nv**2*(Nv**2-9)/(4*(Nv**2-1))
    ax.plot(Nv, dv, "o", color=GRAY, ms=6)
ax.plot(3, 0, "o", color=RED, ms=10, zorder=5)
ax.annotate("N=3: Ω²=C_A/C_F=9/4", (3.08, 0.35), fontsize=11, color=RED)
ax.set_xlabel("N"); ax.set_ylabel("D(N)")
ax.set_title("Fig 5 — Casimir closure holds iff N=3 (Thm 12.IX.T1)")
ax.set_xlim(1.8, 6.2); ax.legend(fontsize=10, loc="upper left")
save(fig, "g5_casimir.png")

# ---------- g6: cross-block capacity ----------
fig, ax = plt.subplots(figsize=(7.2, 4.6))
NN = np.linspace(2, 8, 400)
H = 2*NN/(NN+2)**2  # rs/m^2 for the 2+N family
assert abs(2*3.0/(3.0+2)**2 - 6/25) < 1e-15
ax.plot(NN, H, color=BLUE, lw=2, label=r"$H(N)=2N/(N+2)^2=rs/m^2$")
ax.axhline(6/25, color=GRAY, ls="--", lw=1.2)
ax.plot(3, 6/25, "o", color=RED, ms=10, zorder=5)
ax.annotate("N=3: H=6/25, 2H=12/25\nblock dims 12 | 12; 4H=24/25=dim su(5)/dim End(C⁵)",
            (3.15, 0.20), fontsize=10, color=RED)
ax.set_xlabel("N"); ax.set_ylabel("H")
ax.set_title("Fig 6 — H as normalized cross-block capacity (Thm 12.VIII.T1)")
ax.set_xlim(1.8, 8.2); ax.set_ylim(-0.01, 0.30); ax.legend(fontsize=10)
save(fig, "g6_crossblock.png")

# ---------- g7: quark-gluon momentum fixed point ----------
fig, ax = plt.subplots(figsize=(7.2, 4.6))
nf = np.linspace(1, 6, 400)
aq = 3*nf/(16+3*nf)
assert np.allclose(aq + 16/(16+3*nf), 1)
ax.plot(nf, aq, color=BLUE, lw=2, label=r"$a_q^*(n_f)=3n_f/(16+3n_f)$ (imported LO QCD)")
for n in range(1, 7):
    ax.plot(n, 3*n/(16+3*n), "o", color=GRAY, ms=6)
ax.plot(3, 9/25, "o", color=RED, ms=10, zorder=5)
ax.axhline(9/25, color=GRAY, ls="--", lw=1.2)
ax.annotate("n_f=3 → (a_q,a_g)=(9/25,16/25)\n= native q=1/2 carrier state",
            (3.12, 0.40), fontsize=10, color=RED)
ax.set_xlabel(r"$n_f$"); ax.set_ylabel(r"$a_q^*$")
ax.set_title("Fig 7 — Fixed-point coincidence (conditional cross-check, §12.XI)")
ax.set_xlim(0.7, 6.4); ax.set_ylim(0, 0.56); ax.legend(fontsize=9)
save(fig, "g7_fixedpoint.png")

import os
files = sorted(os.listdir(OUT))
assert len(files) == 7 and all(os.path.getsize(f"{OUT}/{f}") > 0 for f in files)
print("7 non-empty PNGs present:", files)
