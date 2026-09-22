"""Static PNG fallbacks for the Book 3 rewrite figures (matplotlib, Agg).

Mirrors the Desmos expressions/viewports in index.html as closely as a
static renderer allows. Run:
    python3 ~/workspace/book3/checks/gen_graphs.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "/home/hatch/workspace/r-theory-rewrite/book3/graphs/"
BLUE, ORANGE, GREEN, RED, GRAY, BLACK = (
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#999999", "#000000")

def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT + name, dpi=110)
    plt.close(fig)
    print("wrote", OUT + name)

def masked(t, y, lo, hi):
    y = np.where((y > lo) & (y < hi), y, np.nan)
    return y

# ---------------------------------------------------------------- Fig 1
t = np.linspace(-2.5, 2.5, 4001)
Qp = (1 + t) / (1 - t)
Qm = (t - 1) / (1 + t)
fig, ax = plt.subplots(figsize=(7.2, 5.2))
ax.plot(t, masked(t, Qp, -3, 3), color=BLUE, lw=1.6, label="Q+(t)=(1+t)/(1-t)")
ax.plot(t, masked(t, Qm, -3, 3), color=ORANGE, lw=1.6, label="Q-(t)=(t-1)/(1+t)")
ax.plot(t, masked(t, -1 / np.where(t == 0, np.nan, t), -3, 3), color=GREEN,
        lw=1.6, label="-1/t  (two cophase steps = half-turn)")
ax.plot(t, t, color=GRAY, ls="--", lw=1.2, label="identity")
ax.plot([0], [1], "o", color=BLACK); ax.text(0.06, 1.06, "0 -> 1", fontsize=9)
ax.plot([-1], [0], "o", color=BLACK); ax.text(-0.94, 0.14, "-1 -> 0", fontsize=9)
ax.axvline(1, color=GRAY, ls=":", lw=1); ax.text(1.04, 2.5, "t=1 pole\n(1 -> inf)", fontsize=8)
ax.set_xlim(-2.5, 2.5); ax.set_ylim(-3, 3)
ax.set_xlabel("t = tan(x/2)"); ax.set_ylabel("projective image")
ax.set_title("Cophase as Mobius maps on the projective phase line")
ax.legend(fontsize=8, loc="upper left")
save(fig, "b3_mobius.png")

# ---------------------------------------------------------------- Fig 2
x = np.linspace(0.001, 2 * np.pi - 0.001, 6001)
sn, cs = np.sin(x), np.cos(x)
srx = np.abs(1 / sn) + cs / sn
sxp = np.abs(1 / sn) - cs / sn
cxp = np.abs(1 / cs) + sn / cs
crx = np.abs(1 / cs) - sn / cs
fig, ax = plt.subplots(figsize=(7.6, 5.2))
for j in range(8):
    if j % 2 == 0:
        ax.axvspan(j * np.pi / 4, (j + 1) * np.pi / 4, color="#f2f2f2", zorder=0)
winners = ["srx", "cxp", "crx", "sxp", "srx", "cxp", "crx", "sxp"]
for j, w in enumerate(winners):
    ax.text((j + 0.5) * np.pi / 4, 7.6, w, ha="center", fontsize=8,
            color="#555555")
ax.plot(x, np.clip(srx, 0, 8), color=BLUE, lw=1.4, label="srx")
ax.plot(x, np.clip(sxp, 0, 8), color=ORANGE, lw=1.4, label="sxp")
ax.plot(x, np.clip(cxp, 0, 8), color=GREEN, lw=1.4, label="cxp")
ax.plot(x, np.clip(crx, 0, 8), color=RED, lw=1.4, label="crx")
ax.set_xlim(0, 2 * np.pi); ax.set_ylim(0, 8)
ax.set_xticks([k * np.pi / 4 for k in range(9)],
              ["0", "p/4", "p/2", "3p/4", "p", "5p/4", "3p/2", "7p/4", "2p"])
ax.set_xlabel("phase x"); ax.set_ylabel("primitive value")
ax.set_title("Eight-octant dominance cycle: srx > cxp > crx > sxp > ...")
ax.legend(fontsize=8, loc="upper right")
save(fig, "b3_octants.png")

# ---------------------------------------------------------------- Fig 3
u = np.linspace(-4, 4, 2001)
f = np.sqrt(1 + u * u) - u
fig, ax = plt.subplots(figsize=(7.2, 5.2))
ax.plot(u, f, color=BLUE, lw=1.8, label="s = f(u)")
ax.plot(u, 1 / f, color=ORANGE, lw=1.8, label="f(-u) = 1/f(u)")
ax.axhline(1, color=GRAY, ls="--", lw=1.2); ax.text(3.1, 1.08, "unit threshold s=1", fontsize=9)
ax.axvline(0, color=GRAY, ls=":", lw=1); ax.text(0.08, 3.4, "u=0", fontsize=9)
ax.plot([0], [1], "o", color=BLACK)
ax.set_xlim(-4, 4); ax.set_ylim(0, 4)
ax.set_xlabel("signed affine coordinate u"); ax.set_ylabel("positive coordinate s")
ax.set_title("Positive reciprocal transform f(u) = sqrt(1+u^2) - u")
ax.legend(fontsize=9)
save(fig, "b3_transform.png")

# ---------------------------------------------------------------- Fig 4
x = np.linspace(0, 2 * np.pi, 4001)
fw = np.sign(np.sin(2 * x))
fig, ax = plt.subplots(figsize=(7.6, 4.6))
ax.plot(x, fw, color=BLUE, lw=2, drawstyle="steps-post")
x0 = np.pi / 8
pts = [(x0 + k * np.pi / 2, (-1) ** k) for k in range(5)]
for px, py in pts:
    ax.plot([px], [py], "o", color=RED, ms=7)
ax.annotate("", xy=(x0 + np.pi / 2 - 0.06, -0.82), xytext=(x0 + 0.06, 0.82),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
ax.text(x0 + np.pi / 4, 0.15, "+pi/2 flips sign", color=RED, fontsize=9, ha="center")
ax.annotate("", xy=(x0 + np.pi - 0.06, 0.82), xytext=(x0 + 0.06, 0.82),
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.4))
ax.text(x0 + np.pi / 2, 1.18, "+pi preserves sign", color=GREEN, fontsize=9, ha="center")
ax.set_xlim(0, 2 * np.pi); ax.set_ylim(-1.6, 1.6)
ax.set_yticks([-1, 0, 1])
ax.set_xticks([k * np.pi / 2 for k in range(5)], ["0", "p/2", "p", "3p/2", "2p"])
ax.set_xlabel("phase x"); ax.set_ylabel("FlatWave(x) = sgn(sin 2x)")
ax.set_title("First climax: cophase reverses FlatWave, half-turn preserves it")
save(fig, "b3_flatwave.png")

# ---------------------------------------------------------------- Fig 5
th = np.linspace(0.02, np.pi - 0.02, 2001)
rho = np.tan(th / 2)
sxpv = np.abs(1 / np.sin(th)) - np.cos(th) / np.sin(th)
fig, ax = plt.subplots(figsize=(7.2, 5.2))
ax.plot(th, np.clip(rho, 0, 6), color=BLUE, lw=1.8, label="rho = tan(th/2)")
ax.plot(th, np.clip(sxpv, 0, 6), color=ORANGE, lw=1.2, ls="--",
        label="sxp(th) (coincides on (0,pi))")
ax.plot([np.pi / 2], [1], "o", color=RED, ms=8)
ax.text(np.pi / 2 + 0.06, 1.15, "FlatWave seam th=pi/2:\nrho=1, q0=1/sqrt(2) != 0\n(regular in Rodrigues chart)",
        color=RED, fontsize=9)
ax.text(np.pi - 0.55, 4.6, "chart boundary\nth -> pi: q0 -> 0", fontsize=9, color="#555555")
ax.set_xlim(0, np.pi + 0.15); ax.set_ylim(0, 6)
ax.set_xticks([0, np.pi / 2, np.pi], ["0", "pi/2", "pi"])
ax.set_xlabel("rotation angle th"); ax.set_ylabel("rho")
ax.set_title("Rodrigues chart: operator seam is not the chart boundary")
ax.legend(fontsize=9, loc="upper left")
save(fig, "b3_rodrigues.png")

# ---------------------------------------------------------------- Fig 6
th = np.linspace(0, 4 * np.pi, 2001)
q0 = np.cos(th / 2)
fig, ax = plt.subplots(figsize=(7.6, 4.8))
ax.axvspan(0, 2 * np.pi, color="#eef3f8", zorder=0)
ax.text(np.pi, 1.32, "one full rotation (base SO(3))", ha="center", fontsize=9)
ax.plot(th, q0, color=BLUE, lw=1.8, label="lift sheet A: q0 = cos(th/2)")
ax.plot(th, -q0, color=ORANGE, lw=1.8, label="lift sheet B: q0 = -cos(th/2)")
for px, py, lab in [(0, 1, "q"), (2 * np.pi, -1, "-q"), (4 * np.pi, 1, "q")]:
    ax.plot([px], [py], "o", color=BLACK, ms=7)
    ax.text(px + 0.12, py + 0.08, lab, fontsize=10)
ax.annotate("", xy=(2 * np.pi - 0.15, -0.9), xytext=(0.15, 0.9),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.4, ls="--"))
ax.text(3.4, 0.25, "deck shift D:\nth -> th+2pi\nflips the sheet", color=RED, fontsize=9)
ax.set_xlim(0, 4 * np.pi); ax.set_ylim(-1.5, 1.5)
ax.set_xticks([0, 2 * np.pi, 4 * np.pi], ["0", "2pi", "4pi"])
ax.set_xlabel("lifted angle th"); ax.set_ylabel("quaternion scalar part q0")
ax.set_title("Double cover: the lift needs 4pi to close; no single sheet works globally")
ax.legend(fontsize=9, loc="lower left")
save(fig, "b3_cover.png")

# ---------------------------------------------------------------- Fig 7
t = np.linspace(-2.5, 2.5, 4001)
tau = np.sign(t)
fwt = np.sign(t * (1 - t * t))
fig, ax = plt.subplots(figsize=(7.6, 4.8))
ax.axvspan(-1, 1, color="#e8f4e8", zorder=0)
ax.text(0, 2.35, "agree on |t| < 1", ha="center", fontsize=9, color="#2c6e2c")
ax.text(-1.75, 2.35, "disagree", ha="center", fontsize=9, color="#a33")
ax.text(1.75, 2.35, "disagree", ha="center", fontsize=9, color="#a33")
ax.plot(t, fwt + 1.2, color=BLUE, lw=2, drawstyle="steps-post",
        label="FlatWave = sgn[t(1-t^2)]  (offset +1.2)")
ax.plot(t, tau - 1.2, color=ORANGE, lw=2, drawstyle="steps-post",
        label="tautological pullback = sgn(t)  (offset -1.2)")
ax.axvline(-1, color=GRAY, ls=":", lw=1); ax.axvline(1, color=GRAY, ls=":", lw=1)
ax.set_xlim(-2.5, 2.5); ax.set_ylim(-2.6, 2.6)
ax.set_yticks([])
ax.set_xlabel("projective coordinate t = tan(x/2)")
ax.set_title("Not the same sign function: FlatWave vs tautological transition sign")
ax.legend(fontsize=9, loc="lower right")
save(fig, "b3_comparison.png")

print("done")
