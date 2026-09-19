#!/usr/bin/env python3
"""Book 18 verification: every checkable mathematical claim on book18/index.html.

Scope labels: CP = checked proof (exact integer/rational arithmetic or exact
identities — the ~1e-16 residuals are pure floating-point rounding, never
physics), NC = completed numerical check, ST = standard imported theorem
(recorded, not derived here). The IC exhibits re-verify the key arithmetic
behind the chunk-4 findings; the findings themselves are established in
~/workspace/vol4/book18/LEDGER_18.md (chunk 4: 40 assertions, 0 failed,
CP 31 / NC 1 / IC 8, no timeouts). This run: no timeouts.

Page claims verified (Part I figures, then Part II, then IC exhibits):
 V1  C(n,4) = n(n-1)(n-2)(n-3)/24; C(16,4) = 1820            (Fig 1, CP)
 V2  Sym^2(128) = 8256 = 1+1820+6435;
     Alt^2(128) = 8128 = 120+8008; 120 not in Sym^2 parts  (Fig 2, CP;
     IC-12 exhibit; the irrep content itself is ST, not derived here)
 V3  branching staircase partial sums 54 -> 74 -> 134 -> 135 (Fig 3, CP)
 V4  135 = 16*17/2 - 1 = Sym^2_0(16); 54 = 55-1 = Sym^2_0(10);
     (54,1)+(1,20')+(10,6)+(1,1) dims = 135                 (Fig 3, CP;
     the SO(10)xSU(4) representation content is ST)
 V5  conversion chain: (6/5)(5/2) = 3; a = S_F/3; a = (6/5)c;
     c = 5*S_F/18; -(1/256)(sqrt(10)/6) = -sqrt(10)/1536    (Fig 4, CP)
 V6  T-matrix spine (exact rationals): T = diag(1,1,-1/4 x8)
     traceless; ||T||^2 = 5/2; ||Q_F||^2 = 18/5; (1/4)^4 = 1/256 (CP)
 V7  conditional projector idempotency: Pi_pm = (1+-gamma_17)/2
     idempotent on eigenvalues +-1; sign (-1)^120 = +1       (Fig 5, CP as a
     conditional inference — the gamma_i relations are OPEN in v1)
 V8  C8 word (E,B,E,O)x2: 4 E / 2 B / 2 O; E on decay octants
     1,3,5,7; B on growth octants 2,6; O on growth octants 4,8 (Fig 6, CP)
 V9  (sqrt2)^4 = 4 (propagator cosh product);
     (sqrt2)^8 = 16 (all-eight product)                    (Part II, CP)
 V10 V_E^4 ~= 638.78: |5.0273^4 - 638.78| < 0.05           (Part II, NC)
 V11 IC-13 rank-nullity analogue: NullSpace of 8256x1 -> {}
     (nullity 0); of 1x8256 -> nullity 8255, not 1820       (CP)
 V12 IC-14 dimension incompatibility: 128^4 = 268435456;
     sandwich inner dims 8256 vs 268435456 mismatch        (CP)
 V13 IC-15: v1 prints both `S_F = -(1/256)*S_F_raw;` and
     `nHat54 = -(Sqrt[10]/1536)*S_F*m2^(-4);` — substituting,
     the -(1/256) factor is applied twice (exact algebra)  (CP)
 V14 IC-16: `wickSign` occurs exactly once in the v1 Book 18
     range and is never assigned                         (CP, text check)
 V15 IC-17: 8 qubit factors -> 256x256, not the required
     128x128; v1 shows i = 1,...,8 for 16 matrices        (CP + text check)
 V16 the missing-input lines ("explicit 1820x1820 E, B, O
     matrices") are present and framed as missing on the page (CP)

Also regenerates the 6 PNG fallbacks from the same expressions as the
Desmos embeds (240 dpi, ~/workspace/r-theory-rewrite/book18/graphs/).
"""
import math
import os
import re
from fractions import Fraction

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book18/index.html")
OUT = os.path.join(REPO, "book18/graphs")
V1 = os.path.expanduser("~/workspace/vol4/volume_iv_v1_raw.txt")
os.makedirs(OUT, exist_ok=True)

TOL = 1e-12
results = []

def check(name, err, tol=TOL, scope="CP"):
    err = np.asarray(err, dtype=float)
    assert np.all(np.isfinite(err)), f"{name}: non-finite values"
    m = float(np.max(np.abs(err)))
    assert m < tol, f"{name}: max_err={m:.3e} >= tol={tol:.0e}"
    results.append((name, m, tol, scope))
    print(f"OK [{scope}] {name}: max_err={m:.3e} < {tol:.0e}")

def exact(name, cond, note=""):
    assert cond, f"{name}: FAILED {note}"
    results.append((name, 0.0, 0.0, "CP"))
    print(f"OK [CP] {name}" + (f" ({note})" if note else ""))

# ---------------- V1: C(n,4) = 1820 (Fig 1) ----------------
n = np.arange(4, 21)
check("V1 C(n,4) = n(n-1)(n-2)(n-3)/24",
      n*(n-1)*(n-2)*(n-3)/24 - np.array([math.comb(int(k), 4) for k in n]),
      1e-9)
exact("V1 C(16,4) = 1820", math.comb(16, 4) == 1820)

# ---------------- V2: Sym^2 / Alt^2 dims (Fig 2; IC-12 exhibit) ----------------
exact("V2 Sym^2(128) = 8256", 128*129//2 == 8256)
exact("V2 1 + 1820 + 6435 = 8256", 1 + 1820 + 6435 == 8256)
exact("V2 Alt^2(128) = 8128", 128*127//2 == 8128)
exact("V2 120 + 8008 = 8128", 120 + 8008 == 8128)
exact("V2 120 not among Sym^2 parts (IC-12 exhibit)",
      120 not in (1, 1820, 6435))
print("OK [ST] V2 irrep content Sym^2(128) = 1+1820+6435, "
      "Alt^2 S = 120+8008: standard SO(16) representation theory, "
      "imported, not derived here")

# ---------------- V3/V4: branching 135 (Fig 3) ----------------
exact("V3 staircase partial sums 54 -> 74 -> 134 -> 135",
      [54, 54+20, 54+20+60, 54+20+60+1] == [54, 74, 134, 135])
exact("V4 135 = 16*17/2 - 1 = Sym^2_0(16)", 16*17//2 - 1 == 135)
exact("V4 54 = 55 - 1 = Sym^2_0(10)", 55 - 1 == 54)
exact("V4 (54,1)+(1,20')+(10,6)+(1,1) dims = 135",
      54*1 + 1*20 + 10*6 + 1*1 == 135)
print("OK [ST] V4 SO(10)xSU(4) representation content of the 135: standard "
      "imported representation theory, not derived here")

# ---------------- V5: conversion chain (Fig 4) ----------------
exact("V5 (6/5)(5/2) = 3", Fraction(6, 5)*Fraction(5, 2) == 3)
s = np.linspace(0, 3, 301)
a, c = s/3, 5*s/18
check("V5 S_F = 3a  <=>  a = S_F/3", 3*a - s, 1e-15)
check("V5 a = (6/5)c", a - (6/5)*c, 1e-15)
check("V5 c = 5*S_F/18", c - 5*s/18, 1e-15)
# Exact rational identity; the 1e-18 residual is pure float rounding.
check("V5 -(1/256)(sqrt10/6) = -sqrt10/1536",
      -(1/256)*(math.sqrt(10)/6) - (-math.sqrt(10)/1536), 1e-18)

# ---------------- V6: T-matrix spine (exact rationals) ----------------
T = [Fraction(1), Fraction(1)] + [Fraction(-1, 4)]*8
exact("V6 T traceless", sum(T) == 0)
exact("V6 ||T||^2 = 5/2", sum(t*t for t in T) == Fraction(5, 2))
exact("V6 ||Q_F||^2 = (6/5)^2*(5/2) = 18/5",
      Fraction(6, 5)**2 * Fraction(5, 2) == Fraction(18, 5))
exact("V6 (1/4)^4 = 1/256", Fraction(1, 4)**4 == Fraction(1, 256))

# ---------------- V7: conditional projector idempotency (Fig 5) ----------------
exact("V7 sign (-1)^120 = +1", (-1)**120 == 1)
for g in (-1.0, 1.0):
    for pm in (1.0, -1.0):
        Pi = (1 + pm*g)/2
        assert abs(Pi**2 - Pi) < 1e-15, f"g={g}, pm={pm}"
print("OK [CP] V7 Pi_pm = (1+-gamma_17)/2 idempotent on eigenvalues +-1 "
      "(conditional inference: the gamma_i relations are OPEN in v1)")

# ---------------- V8: C8 word (Fig 6) ----------------
word = ['E', 'B', 'E', 'O']*2
exact("V8 C8 word (E,B,E,O)x2: 8 entries, 4 E / 2 B / 2 O",
      len(word) == 8 and word.count('E') == 4
      and word.count('B') == 2 and word.count('O') == 2)
degs = [22.5 + 45*k for k in range(8)]
exact("V8 E on decay octants 1,3,5,7 (22.5,112.5,202.5,292.5 deg)",
      [d for d, ch in zip(degs, word) if ch == 'E']
      == [22.5, 112.5, 202.5, 292.5])
exact("V8 B on growth octants 2,6 (67.5,247.5 deg)",
      [d for d, ch in zip(degs, word) if ch == 'B'] == [67.5, 247.5])
exact("V8 O on growth octants 4,8 (157.5,337.5 deg)",
      [d for d, ch in zip(degs, word) if ch == 'O'] == [157.5, 337.5])

# ---------------- V9: tension arithmetic (Part II) ----------------
sq2 = math.sqrt(2)
# Exact identities: (sqrt2)^4 = ((sqrt2)^2)^2 = 2^2 = 4; float residual only.
check("V9 (sqrt2)^4 = 4 (propagator cosh product)", sq2**4 - 4, 1e-12)
check("V9 (sqrt2)^8 = 16 (all-eight product)", sq2**8 - 16, 1e-12)

# ---------------- V10: V_E^4 bound (Part II, NC) ----------------
vE4 = 5.0273**4
dev = abs(vE4 - 638.78)
assert dev < 0.05, f"V10: |5.0273^4 - 638.78| = {dev} >= 0.05"
results.append(("V10 |5.0273^4 - 638.78| < 0.05", dev, 0.05, "NC"))
print(f"OK [NC] V10 5.0273^4 = {vE4:.6f}; |5.0273^4 - 638.78| = {dev:.4f} < 0.05")

# ---------------- V11: IC-13 rank-nullity analogue ----------------
rng = np.random.default_rng(18)
v = rng.standard_normal(8256)
A_tall = v.reshape(8256, 1)     # Transpose[{traceVector}]: 8256 x 1
A_wide = v.reshape(1, 8256)     # intended reading NullSpace[{traceVector}]
null_tall = A_tall.shape[1] - np.linalg.matrix_rank(A_tall)
null_wide = A_wide.shape[1] - np.linalg.matrix_rank(A_wide)
exact("V11 IC-13: 8256x1 nullity = 0 (code yields {})", null_tall == 0)
exact("V11 IC-13: 1x8256 nullity = 8255, not 1820", null_wide == 8255)

# ---------------- V12: IC-14 dimension incompatibility ----------------
exact("V12 IC-14: 128^4 = 268435456", 128**4 == 268435456)
exact("V12 IC-14: sandwich inner dims 8256 vs 268435456 mismatch",
      8256 != 128**4)

# ---------------- V13: IC-15 double-counted -(1/256) ----------------
with open(V1, encoding="utf-8") as f:
    v1lines = f.readlines()
b18 = v1lines[2998:3220]   # Book 18 range (1-indexed lines 2999-3220)
has_sf = any("S_F = -(1/256) * S_F_raw;" in ln for ln in b18)
has_nh = any("nHat54 = -(Sqrt[10]/1536) * S_F * m2^(-4);" in ln for ln in b18)
exact("V13 IC-15: v1 prints `S_F = -(1/256)*S_F_raw;`", has_sf)
exact("V13 IC-15: v1 prints `nHat54 = -(Sqrt[10]/1536)*S_F*m2^(-4);`", has_nh)
# Substituting the first into the second: the -(1/256) factor is applied
# twice, relative to the section's own definition S_F := <Q_F, R~> (stripped).
check("V13 IC-15: substituted nHat54 = +(sqrt10/393216)*S_F_raw*m2^-4 "
      "(double application, exact)",
      -(math.sqrt(10)/1536)*(-(1/256)) - (math.sqrt(10)/393216), 1e-18)

# ---------------- V14: IC-16 wickSign never assigned ----------------
occ = [ln for ln in b18 if "wickSign" in ln]
exact("V14 IC-16: `wickSign` occurs exactly once in v1 Book 18",
      len(occ) == 1)
exact("V14 IC-16: no assignment to `wickSign` anywhere in Book 18",
      not any(re.search(r"wickSign\s*[:=]", ln) for ln in b18))

# ---------------- V15: IC-17 gamma template ----------------
exact("V15 IC-17: 8 qubit factors -> 256x256, not 128x128",
      2**8 == 256 and 256 != 128)
exact("V15 IC-17: v1 requires 'The 16 gamma matrices'",
      any("The 16 gamma matrices" in ln for ln in b18))
exact("V15 IC-17: template shows only 'for i = 1,...,8'",
      any("for i = 1,...,8" in ln for ln in b18))

# ---------------- V16: missing-input lines present on the page ----------------
with open(PAGE, encoding="utf-8") as f:
    html = f.read()
exact("V16 page names the missing 'explicit 1820×1820 E, B, O matrices'",
      "explicit 1820×1820 E, B, O matrices" in html)
exact("V16 page frames them as missing inputs", "missing-input" in html)

n_cp = sum(1 for r in results if r[3] == "CP")
n_nc = sum(1 for r in results if r[3] == "NC")
print(f"\nAll {len(results)} checks passed ({n_cp} CP, {n_nc} NC). No timeouts.")

# ================================================================ PNGs
# Render quality: 240 dpi fallbacks, generated from the SAME expressions
# as the Desmos embeds. Output path: book18/graphs/ (the live page path).
DPI = 240
plt.rcParams.update({"font.size": 10.5, "axes.titlesize": 12, "axes.labelsize": 11})

# ---- F1 C(n,4)
nn = np.linspace(4, 20, 400)
f, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(nn, nn*(nn-1)*(nn-2)*(nn-3)/24, lw=1.6, label="C(n,4)=n(n−1)(n−2)(n−3)/24")
ax.plot([16], [1820], "go", ms=9, label="C(16,4)=1820")
ax.set_xlim(4, 20); ax.set_ylim(0, 5200); ax.legend(fontsize=9)
ax.set_title("Fig 1 — The 1820 as C(16,4) (fallback)")
ax.set_xlabel("n"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b18_comb.png", dpi=DPI); plt.close(f)

# ---- F2 Sym^2 / Alt^2
nn = np.linspace(0, 140, 400)
f, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(nn, nn*(nn+1)/2, lw=1.6, label="dim Sym²(n)=n(n+1)/2")
ax.plot(nn, nn*(nn-1)/2, lw=1.6, label="dim Λ²(n)=n(n−1)/2")
ax.plot([128], [8256], "bo", ms=8, label="Sym²(128)=8256")
ax.plot([128], [8128], "mo", ms=8, label="Λ²(128)=8128")
for y, lab in [(1, "1"), (1820, "1820"), (6435, "6435")]:
    ax.axhline(y, color="gray", ls="--", lw=1.0)
    ax.text(140, y+180, lab, fontsize=8, color="gray", ha="right")
ax.axhline(120, color="red", ls="--", lw=1.4)
ax.text(140, 120+260, "120 lives here (in Λ²), not in Sym² (IC-12)",
        fontsize=8, color="red", ha="right")
ax.set_xlim(0, 140); ax.set_ylim(0, 10500); ax.legend(fontsize=8, loc="upper left")
ax.set_title("Fig 2 — Sym²(128) vs Λ²(128): the 120 is not in Sym² (fallback)")
ax.set_xlabel("n"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b18_sym_alt.png", dpi=DPI); plt.close(f)

# ---- F3 branching staircase
f, ax = plt.subplots(figsize=(8, 4.6))
segs = [(0, 1, 54, "(54,1)"), (1, 2, 74, "(1,20′)"), (2, 3, 134, "(10,6)"), (3, 4, 135, "(1,1)")]
for lo, hi, y, lab in segs:
    ax.plot([lo, hi], [y, y], lw=3.5, label=f"{lab}: partial sum {y}")
ax.axhline(135, color="k", ls="--", lw=1.0)
ax.text(4.02, 135, "135 = 16·17/2 − 1", fontsize=9, va="center")
ax.set_xlim(0, 4.6); ax.set_ylim(0, 150); ax.legend(fontsize=9, loc="upper left")
ax.set_title("Fig 3 — 135 → (54,1)⊕(1,20′)⊕(10,6)⊕(1,1) under SO(10)×SU(4) (fallback)")
ax.set_xlabel("branch"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b18_branch.png", dpi=DPI); plt.close(f)

# ---- F4 conversion chain
s = np.linspace(0, 3, 400)
f, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(s, s/3, lw=1.6, label="a = S_F/3")
ax.plot(s, 5*s/18, lw=1.6, label="c = 5·S_F/18")
ax.plot([3], [1], "ko", ms=7); ax.text(3.02, 1.0, "a=S_F/3", fontsize=9, va="center")
ax.plot([3], [5/6], "ko", ms=7); ax.text(3.02, 5/6, "c=5S_F/18", fontsize=9, va="center")
ax.text(0.15, 1.05, "no established point: S_F value OPEN", fontsize=9, color="red")
ax.set_xlim(0, 3.4); ax.set_ylim(0, 1.25); ax.legend(fontsize=9, loc="upper left")
ax.set_title("Fig 4 — Conversion chain: algebraic form only (fallback)")
ax.set_xlabel("S_F (unestablished)"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b18_chain.png", dpi=DPI); plt.close(f)

# ---- F5 projector idempotency
x = np.linspace(-1, 1, 400)
f, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(x, (1+x)/2, lw=1.6, label="Π₊=(1+γ₁₇)/2")
ax.plot(x, (1-x)/2, lw=1.6, label="Π₋=(1−γ₁₇)/2")
ax.plot([-1, -1, 1, 1], [0, 1, 0, 1], "ko", ms=7)
ax.text(0.02, 0.5, "γ₁₇=±1 → Π values {0,1}\n(conditional: γ-relations OPEN in v1)",
        fontsize=9, ha="left", va="center",
        bbox=dict(boxstyle="round", fc="wheat", alpha=0.5))
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-0.15, 1.15); ax.legend(fontsize=9)
ax.set_title("Fig 5 — Conditional projector idempotency (fallback)")
ax.set_xlabel("γ₁₇ eigenvalue"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b18_projector.png", dpi=DPI); plt.close(f)

# ---- F6 ordered contraction diagram
word = ['E', 'B', 'E', 'O']*2
cols = {'E': 'green', 'B': 'blue', 'O': 'orange'}
f, ax = plt.subplots(figsize=(6.4, 6.4))
th = np.linspace(0, 2*np.pi, 400)
ax.plot(np.cos(th), np.sin(th), lw=1.0, color="gray")
for k, ch in enumerate(word):
    ang = math.radians(22.5 + 45*k)
    ax.plot([math.cos(ang)], [math.sin(ang)], "o", ms=14, color=cols[ch])
    ax.text(1.18*math.cos(ang), 1.18*math.sin(ang), f"{ch}{k+1}",
            fontsize=10, ha="center", va="center", color=cols[ch], weight="bold")
ax.text(0, 0, "→ 54\n(target:\nNOT established)", fontsize=10, ha="center",
        va="center", bbox=dict(boxstyle="round", fc="mistyrose", alpha=0.9))
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
ax.set_aspect("equal", adjustable="box"); ax.axis("off")
ax.set_title("Fig 6 — Ordered contraction (E,B,E,O)×2 → 54 (fallback)")
f.tight_layout(); f.savefig(f"{OUT}/b18_contraction.png", dpi=DPI); plt.close(f)

sizes = {p: os.path.getsize(os.path.join(OUT, p)) for p in sorted(os.listdir(OUT))}
print("\nPNG fallbacks written:")
for p, s in sizes.items():
    assert s > 0, f"{p} empty"
    print(f"  {p}: {s} bytes")
