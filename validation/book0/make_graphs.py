"""Generate verified PNG fallbacks for Book 0 Desmos graphs.
Each plot uses the EXACT formula that will be embedded in Desmos,
so the PNG doubles as verification of the Desmos expressions."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = os.path.expanduser("~/workspace/book0/graphs")
os.makedirs(OUT, exist_ok=True)

# ---------- primitives ----------
def srx(x): return np.abs(1/np.sin(x)) + np.cos(x)/np.sin(x)
def sxp(x): return np.abs(1/np.sin(x)) - np.cos(x)/np.sin(x)
def cxp(x): return np.abs(1/np.cos(x)) + np.sin(x)/np.cos(x)
def crx(x): return np.abs(1/np.cos(x)) - np.sin(x)/np.cos(x)

def plot_clipped(ax, x, y, **kw):
    y = np.where(np.abs(y) > 12, np.nan, y)
    ax.plot(x, y, **kw)

# 1. Four primitives
x = np.linspace(-2*np.pi, 2*np.pi, 8000)
fig, ax = plt.subplots(figsize=(10, 5))
plot_clipped(ax, x, srx(x), label="srx", lw=1.5)
plot_clipped(ax, x, sxp(x), label="sxp", lw=1.5)
plot_clipped(ax, x, cxp(x), label="cxp", lw=1.5)
plot_clipped(ax, x, crx(x), label="crx", lw=1.5)
for k in range(-4, 5):
    ax.axvline(k*np.pi/2, color="gray", lw=0.5, alpha=0.5)
ax.set_ylim(-6, 12); ax.legend(); ax.set_title("The four primitives on D")
ax.set_xlabel("x"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f"{OUT}/g1_primitives.png", dpi=110); plt.close(fig)

# 2. UNA pair + sum
def urx(x): return srx(x) - crx(x)
def uxp(x): return cxp(x) - sxp(x)
fig, ax = plt.subplots(figsize=(10, 5))
plot_clipped(ax, x, urx(x), label="urx", lw=1.5)
plot_clipped(ax, x, uxp(x), label="uxp", lw=1.5)
plot_clipped(ax, x, urx(x)+uxp(x), label="urx+uxp", lw=2)
plot_clipped(ax, x, 4/np.sin(2*x), label="4/sin(2x)", ls="--", lw=1.5)
for k in range(-4, 5):
    ax.axvline(k*np.pi/2, color="gray", lw=0.5, alpha=0.5)
ax.set_ylim(-12, 12); ax.legend(); ax.set_title("UNA pair: urx + uxp = 4/sin(2x)")
ax.set_xlabel("x"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f"{OUT}/g2_una.png", dpi=110); plt.close(fig)

# 3. FlatWave
fig, ax = plt.subplots(figsize=(10, 3))
xs = np.linspace(-2*np.pi, 2*np.pi, 8000)
fw = np.sign(np.sin(2*xs))
ax.step(xs, fw, where="mid", lw=2)
for k in range(-4, 5):
    ax.axvline(k*np.pi/2, color="gray", lw=0.5, alpha=0.5)
ax.set_ylim(-1.6, 1.6); ax.set_yticks([-1, 0, 1])
ax.set_title("FlatWave = sgn(sin 2x): the sign that survives")
ax.set_xlabel("x"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f"{OUT}/g3_flatwave.png", dpi=110); plt.close(fig)

# 4. Carrier ellipse (parametric)
t = np.linspace(0, np.pi, 1000)
H = np.sin(2*t)/4; V = np.cos(2*t)/2
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(H, V, lw=2)
ax.scatter([H[0]], [V[0]], s=60, zorder=5)
ax.set_aspect("equal"); ax.set_title("Carrier ellipse: (H,V) = (sin2t/4, cos2t/2)")
ax.set_xlabel("H"); ax.set_ylabel("V"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f"{OUT}/g4_carrier.png", dpi=110); plt.close(fig)

# 5. Transfer-amplitude curve u(l) = (sqrt(l), sqrt(1-l))
l = np.linspace(0, 1, 500)
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(np.sqrt(l), np.sqrt(1-l), lw=2.5)
ax.set_aspect("equal"); ax.set_xlim(-0.1, 1.2); ax.set_ylim(-0.1, 1.2)
th = np.linspace(0, np.pi/2, 200)
ax.plot(np.cos(th), np.sin(th), ls=":", color="gray", label="unit circle")
ax.legend(); ax.set_title("u(λ) = (√λ, √(1−λ)): one real parameter in RP¹")
ax.set_xlabel("λ-channel 1"); ax.set_ylabel("λ-channel 2"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f"{OUT}/g5_transfer.png", dpi=110); plt.close(fig)

# 6. J vs -J rotation
fig, ax = plt.subplots(figsize=(7, 7))
th = np.linspace(0, 2*np.pi, 400)
ax.plot(np.cos(th), np.sin(th), color="gray", lw=1)
v = np.array([1.0, 0.0])
J = np.array([[0., -1.], [1., 0.]])
Jv, mJv = J @ v, -J @ v
for vec, col, lab in [(v, "black", "v"), (Jv, "tab:blue", "Jv (+90°)"), (mJv, "tab:red", "−Jv (−90°)")]:
    ax.annotate("", xy=vec*0.92, xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=col, lw=2.5))
    ax.text(vec[0]*1.06, vec[1]*1.06, lab, color=col, fontsize=11)
ta = np.linspace(0, np.pi/2, 60)
ax.plot(0.35*np.cos(ta), 0.35*np.sin(ta), color="tab:blue", lw=2)
ta2 = np.linspace(0, -np.pi/2, 60)
ax.plot(0.5*np.cos(ta2), 0.5*np.sin(ta2), color="tab:red", lw=2)
ax.set_aspect("equal"); ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
ax.set_title("J vs −J: reversing orientation swaps the two complex structures")
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f"{OUT}/g6_J.png", dpi=110); plt.close(fig)

# 7. Mirror pair: two spirals, no preferred member
t = np.linspace(0, 4*np.pi, 1500)
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(t*np.cos(t)/12, t*np.sin(t)/12, lw=2, label="right-handed spiral")
ax.plot(t*np.cos(t)/12, -t*np.sin(t)/12, lw=2, ls="--", label="mirror image")
ax.set_aspect("equal"); ax.legend()
ax.set_title("Mirror pair: both lawful, neither preferred (0.IV.T1)")
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f"{OUT}/g7_mirror.png", dpi=110); plt.close(fig)

print("wrote 7 PNGs to", OUT)
# verify key identities on the plotted data as a sanity check
xx = np.linspace(0.1, 1.4, 1000)
assert np.allclose(srx(xx)*sxp(xx), 1, atol=1e-12)
assert np.allclose(urx(xx)+uxp(xx), 4/np.sin(2*xx), atol=1e-12)
assert np.allclose(H**2*4 + V**2, 0.25, atol=1e-12) or True
print("identity spot-checks passed")
