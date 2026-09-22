#!/usr/bin/env python3
"""Generate the 5 Book 10 PNG figures from the same formulas the audit checked.
Every number baked into a caption comes from verify_book10.py's verified output.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

OUT = "/home/hatch/workspace/r-theory-rewrite/book10/graphs"
ALPHA = 1/137.035999084
Z = 1.0
GA = np.sqrt(1-(Z*ALPHA)**2)          # 0.99997335
LAM = Z*ALPHA                          # ground-state decay const (hbar=c=m=1)
RATIO = (Z*ALPHA)/(1+GA)                # |G/F| ground sector = 0.00364872
X_HALF = 2*np.arctan(RATIO)             # 0.007297 rad
print(f"RATIO={RATIO:.8f}  X_HALF={X_HALF:.6f}  1/RATIO={1/RATIO:.4f}  LAM*e={LAM*np.e:.7f}")

def dirac_rhs(r, y, E, k):
    P_, Q_ = y
    return [-(k/r)*P_ + (E+1+Z*ALPHA/r)*Q_,
            (k/r)*Q_ - (E-1+Z*ALPHA/r)*P_]

def integrate(E, k, ga, r0, rmax, npts=30000):
    P0 = r0**ga; Q0 = r0**ga*(ga-1)/(Z*ALPHA)
    rs = np.geomspace(r0, rmax*(1-1e-9), npts)
    sol = solve_ivp(lambda r, y: dirac_rhs(r, y, E, k), (r0, rmax), [P0, Q0],
                    t_eval=rs, method='LSODA', rtol=1e-10, atol=1e-13)
    assert sol.success
    return sol.t, sol.y[0], sol.y[1]

# ground state (analytic, validated against ODE in the audit to 6.6e-11)
rg = np.geomspace(1e-3, 1500*(1-1e-9), 6000)
Fg = np.sqrt(1+GA)*rg**GA*np.exp(-LAM*rg)
Gg = -np.sqrt(1-GA)*rg**GA*np.exp(-LAM*rg)
Fg /= np.max(np.abs(Fg)); Gg /= np.max(np.abs(Fg*np.sqrt(1+GA)/np.sqrt(1+GA)))  # keep ratio exact
Gg = -RATIO*Fg  # exact constant ratio, as the standard formula gives

# excited state n=2, k=-1 (numerical, ODE validated on ground state)
n_r = 1; E2 = 1/np.sqrt(1 + (Z*ALPHA/(n_r+GA))**2)
re_, Pe_raw, Qe_raw = integrate(E2, -1, GA, 1e-4, 1400.0)
scl = np.max(np.abs(Pe_raw))          # one overall scale for both components
Pe, Qe = Pe_raw/scl, Qe_raw/scl
Th_e = np.unwrap(np.arctan2(Qe, Pe))
Ae = np.sqrt(Pe**2 + Qe**2); Ae /= np.max(Ae)
node_r = re_[1:][np.sign(Pe[1:]) != np.sign(Pe[:-1])][0]
print(f"excited node at r={node_r:.1f}; Theta range={Th_e.max()-Th_e.min():.3f} rad")

plt.rcParams.update({"font.size": 10})

# ---- Fig 1: projective-rank obstruction (10.II.T1) ----
fig, ax = plt.subplots(figsize=(7.2, 5.2))
ax.add_patch(plt.Rectangle((0, 0), 2*np.pi, 2*np.pi, fc="#eef3fa", ec="#1b5faa", lw=1.5))
ax.plot([0, 2*np.pi], [np.pi, np.pi], color="#1f77b4", lw=3.5,
        label="real meridian: q = tan(x/2) only (1 real coordinate)")
ax.set_xlim(-0.6, 2*np.pi+0.6); ax.set_ylim(-0.6, 2*np.pi+0.6)
ax.set_xlabel("meridian parameter x"); ax.set_ylabel("relative phase φ")
ax.set_title("Theorem 10.II.T1 — one real coordinate cannot cover CP¹")
ax.text(np.pi, 2*np.pi+0.25, "generic CP¹ state needs (x, φ): 2 real coordinates",
        ha="center", color="#1b5faa", fontsize=10)
ax.text(np.pi, np.pi-0.55, "q-only subfamily: rank 1 (SVD-checked)",
        ha="center", color="#1f77b4", fontsize=10)
ax.legend(loc="lower right", fontsize=9)
fig.tight_layout(); fig.savefig(f"{OUT}/g1_rank.png", dpi=150); plt.close(fig)

# ---- Fig 2: rapidity bridge (10.III.T1) ----
rng = np.random.default_rng(7)
E = 1 + rng.random(40)*6; p = np.sqrt(E**2-1)
rr_ = p/(E+1); aa = np.arccosh(E)
a_grid = np.linspace(0, 5, 400)
fig, ax = plt.subplots(figsize=(7.2, 4.8))
ax.plot(a_grid, np.tanh(a_grid/2), color="#1f77b4", lw=2.5, label="tanh(α/2)")
ax.scatter(aa, rr_, color="#ff7f0e", s=22, zorder=3,
           label="pc/(E+mc²) from random mass-shell pairs")
ax2 = ax.secondary_xaxis('top',
        functions=(lambda a: 2*np.arctan(np.tanh(a/2)),
                   lambda x: 2*np.arctanh(np.tan(x/2))))
ax2.set_xlabel("Projection half-angle x = 2·arctan(r)  [contract PC1]")
ax.set_xlabel("rapidity α  (E = mc²cosh α)"); ax.set_ylabel("ratio r")
ax.set_title("Theorem 10.III.T1 — sxp(x) = pc/(E+mc²) under the rapidity contract")
ax.set_xlim(0, 5); ax.set_ylim(-0.03, 1.03); ax.legend(fontsize=9)
ax.text(2.5, 0.18, "sxp(x) = tan(x/2) reproduces every sampled r to 1.4e-15",
        ha="center", fontsize=9, color="#555555")
fig.tight_layout(); fig.savefig(f"{OUT}/g2_rapidity.png", dpi=150); plt.close(fig)

# ---- Fig 3: ground-sector correspondence (10.IV.T1) ----
fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 6.4), sharex=True)
a1.plot(rg, Fg, color="#1f77b4", lw=2, label="F(r) (large, normalized)")
a1.plot(rg, -Gg/RATIO, color="#ff7f0e", lw=2, ls="--", label="−G(r)/|G/F| (rescaled)")
a1.set_ylabel("normalized"); a1.set_title("Theorem 10.IV.T1 — ground-sector half-angle correspondence")
a1.legend(fontsize=9); a1.set_xlim(0, 1500)
a1.text(750, 0.55, "curves coincide: G/F is r-independent", ha="center", fontsize=9, color="#555555")
a2.plot(rg, Gg/Fg, color="#2ca02c", lw=2)
a2.axhline(-RATIO, color="k", ls=":", lw=1)
a2.set_xlabel("r (units ħ=c=m=1)"); a2.set_ylabel("G/F")
a2.set_ylim(-0.006, 0.001)
a2.text(750, -0.0049, f"G/F = −Zα/(1+γ) = −{RATIO:.8f}  →  x = 2·arctan(|G/F|) = {X_HALF:.6f} rad,\n"
        f"sxp(x) = |G/F| (max err 1e-14)", ha="center", fontsize=9, color="#555555")
fig.tight_layout(); fig.savefig(f"{OUT}/g3_ground.png", dpi=150); plt.close(fig)

# ---- Fig 4: excited state — no universal angle + Prüfer (10.IV.N1, 10.V.T1) ----
fig, (b1, b2, b3) = plt.subplots(3, 1, figsize=(7.2, 8.2), sharex=True)
b1.plot(re_, Pe, color="#1f77b4", lw=1.6, label="P(r) = F(r)")
b1.plot(re_, Qe, color="#ff7f0e", lw=1.6, label="Q(r) = G(r)")
b1.axvline(node_r, color="k", ls="--", lw=1)
b1.text(node_r*1.06, 0.28, f"node at r≈{node_r:.0f}", fontsize=9)
b1.set_ylabel("normalized"); b1.legend(fontsize=9, loc="upper right")
b1.set_title("Negative Theorem 10.IV.N1 + Theorem 10.V.T1 — excited state (n=2, κ=−1)", pad=10)
b1.set_xlim(0, 1400)
b2.plot(re_, np.clip(Qe/Pe, -0.15, 0.15), color="#d62728", lw=1.2)
b2.set_ylabel("G/F (clipped)"); b2.set_ylim(-0.16, 0.16)
b2.text(700, 0.09, "raw ratio G/F: non-constant, pole at the node — inconvenient",
        ha="center", fontsize=9, color="#555555")
ax3 = b3
ax3.plot(re_, Th_e, color="#1f77b4", lw=1.8, label="Θ(r) unwrapped")
ax3.set_ylabel("Θ(r) [rad]", color="#1f77b4"); ax3.set_xlabel("r (units ħ=c=m=1)")
ax3b = ax3.twinx()
ax3b.plot(re_, Ae, color="#ff7f0e", lw=1.4, label="A(r)")
ax3b.set_ylabel("A(r) normalized", color="#ff7f0e")
ax3.text(700, Th_e.min()+0.25, f"Prüfer pair regular through the sign change; Θ runs "
         f"{Th_e.max()-Th_e.min():.2f} rad ≈ π", ha="center", fontsize=9, color="#555555")
fig.tight_layout(); fig.savefig(f"{OUT}/g4_prufer.png", dpi=150); plt.close(fig)

# ---- Fig 5: shared symplectic form (10.VI.T1) ----
fig, (c1, c1b, c2) = plt.subplots(1, 3, figsize=(11.4, 3.9))
# (a) unit square in the (F,G) plane
for k in np.linspace(0, 1, 6):
    c1.plot([k, k], [0, 1], color="#bbbbbb", lw=0.8)
    c1.plot([0, 1], [k, k], color="#bbbbbb", lw=0.8)
c1.add_patch(plt.Polygon([[0,0],[1,0],[1,1],[0,1]], fc="#dbe9fb", ec="#1f77b4", lw=2))
c1.text(0.5, 0.5, "area 1", ha="center", va="center", color="#1f77b4", fontsize=10)
c1.set_xlim(-0.15, 1.15); c1.set_ylim(-0.15, 1.15); c1.set_aspect("equal")
c1.set_xlabel("F"); c1.set_ylabel("G"); c1.set_title("(F, G) plane")
# (b) its image in the (u,v) = (F-G, F+G) plane: a parallelogram of area 2
xx = np.linspace(-1.6, 1.6, 60)
for k in np.linspace(0, 1, 6):
    c1b.plot(xx, xx+2*k, color="#cccccc", lw=0.8)    # F=k  ->  v = u + 2k
    c1b.plot(xx, -xx+2*k, color="#cccccc", lw=0.8)   # G=k  ->  v = -u + 2k
c1b.add_patch(plt.Polygon([[0,0],[1,1],[0,2],[-1,1]], fc="#fdeeda", ec="#ff7f0e", lw=2))
c1b.text(0, 1.0, "area 2", ha="center", va="center", color="#b36a00", fontsize=10)
c1b.set_xlim(-1.4, 1.4); c1b.set_ylim(-0.25, 2.3); c1b.set_aspect("equal")
c1b.set_xlabel("u = F−G"); c1b.set_ylabel("v = F+G")
c1b.set_title("image plane: area 1 → 2")
fig.text(0.38, 0.01, "du∧dv = 2·dF∧dG (exact, sympy)  ⇒  4·dF∧dG = 2·du∧dv: one shared area element",
         ha="center", fontsize=9, color="#555555")
# (c) four charts along a circle in the (F,G) plane
t = np.linspace(0, 2*np.pi, 1200); F_ = np.cos(t); G_ = np.sin(t)
c2.plot(t, 2*F_**2, color="#1f77b4", lw=1.8, label="p_sxp = 2F²")
c2.plot(t, -2*G_**2, color="#ff7f0e", lw=1.8, label="p_srx = −2G²")
c2.plot(t, (F_-G_)**2, color="#2ca02c", lw=1.8, label="p_cxp = (F−G)²")
c2.plot(t, -(F_+G_)**2, color="#d62728", lw=1.8, ls="--", label="p_crx = −(F+G)²")
c2.set_xlim(0, 2*np.pi); c2.set_xlabel("t  (F=cos t, G=sin t)")
c2.set_title("four presentations, one (F,G) pair")
c2.legend(fontsize=8, loc="upper right")
fig.suptitle("Theorem 10.VI.T1 — the four primitive charts share ω_spin = 4 dF∧dG",
             fontsize=11)
fig.subplots_adjust(top=0.86, bottom=0.20)
fig.tight_layout(rect=[0, 0.06, 1, 0.88]); fig.savefig(f"{OUT}/g5_symplectic.png", dpi=150); plt.close(fig)

print("figures written")
