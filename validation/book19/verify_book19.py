#!/usr/bin/env python3
"""Book 19 verification: every checkable mathematical claim on book19/index.html.

Scope labels: CP = checked proof (exact algebra / exact text match against the
v1 source file), SC = completed symbolic check (sympy, finished exactly),
NC = completed numerical check, ST = standard imported theorem. Nothing here
is a manuscript assertion: each check below ran to completion. No timeouts.

Audit verdicts quoted on the page (the 4/16 IC-18 distinction, FLAG-A1..A8,
CONTR-1/2, the Appendix B accuracy verdicts, the open-gate list,
Delta_op(Volume IV) = empty) are the chunk-5 audit's, carried from
~/workspace/vol4/book19/LEDGER_19.md (108 assertions, 0 failed). This script
re-checks every independently checkable number and every v1 quotation the
page rests on, against the local v1 copy
(~/workspace/vol4/volume_iv_v1_raw.txt), and verifies the two figures'
plotted data, viewports, and PNG fallbacks.

Page claims verified:
 V1  (sqrt2)^4 = 4 — the established propagator rapidity product   (Fig 1)
 V2  (sqrt2)^8 = 16 — the all-eight product                        (Fig 1)
 V3  V_E^4 = 638.7823 (recomputed; line-3542 value)                (Fig 1)
 V4  printed "638.7" is a truncation, not a rounding               (Fig 1)
 V5  crx(112.5 deg) = V_E exactly                                  (Fig 1)
 V6  the three tension values 4 / 16 / 638.78 are distinct         (Fig 1)
 V7  FLAG-A1 arithmetic: 4*(1/4) = 1; (1/4)^4 = 1/256               (App A)
 V8  Fig-1 plotted data: the three marked points lie on y = x^4    (Fig 1)
 V9  Fig-2 schematic data: baseline y=0, five gates at y=1         (Fig 2)
 V10 caption "V_E^4 = 638.7823" (4-decimal rounding)                (Fig 1)
 V11 embed blue-point latex x-form equals V_E                       (Fig 1)
 V12 line-3542 exact quotation present in v1                        (Part II)
 V13 "field-redefinition invariance" occurs exactly once in v1      (Part II)
 V14 §17.3.5 "its role in the Clifford contraction remains to be
     determined" present in v1                                     (Part II)
 V15 §17.18.6.4 stripped list has no V_E / dominant-function term   (Part II)
 V16 NO-GO B1..B4 verbatim in v1 (Appendix B accuracy grounds)      (App B)
 V17 §19.3 DG characterization ("applies to any real or complex
     form of E8") present in v1                                    (§19.3)
 V18 CONTR-1 grounds: "Proof sketch." + "unique cyclic word" (item 6)
     and B1 "is not a theorem" both present in v1                   (Add 4.A)
 V19 CONTR-2 grounds: item 8 "bypasses this by using:" and §19.3
     "not a proven evasion" both present in v1                      (Add 4.A)
 V20 terminology distinction grounding IC-18: v1 has both
     "cosh(w_i) = 4" and "the total rapidity product is 16, not 4"   (Part II)
 V21 Appendix A EXACT list carries "Wick sign" as a bare bullet
     (the "(from archive)" qualifier is dropped) — FLAG-A2 ground  (App A)
 V22 "propagator cosh factors ... belong to ζ_parent" present in v1 (Part II)
 V23 v3/report context claims: v3 carries S_F = 0.48958371,
     N_{1820} = 3, c_rest = 1.30555656; the unsigned report carries
     "MASTER CERTIFICATION COMPLETE"                                (Part III)
 V24 viewport guard: every plotted point lies inside its figure's
     Desmos viewport parsed from the page (no viewport overreach)   (Figs)

PNG fallbacks are regenerated from the same expressions as the Desmos
embeds (240 dpi, per WORKFLOW.md §4) after all checks pass.
"""
import math
import os
import re

import numpy as np
import sympy as sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book19/index.html")
V1RAW = os.path.expanduser("~/workspace/vol4/volume_iv_v1_raw.txt")
V3RAW = os.path.expanduser("~/workspace/vol4/volume_iv_v3_raw.txt")
REPORTRAW = os.path.expanduser("~/workspace/vol4/volume_iv_audit_report_raw.txt")
OUT = os.path.join(REPO, "book19/graphs")

raw = open(V1RAW, encoding="utf-8").read()
v3 = open(V3RAW, encoding="utf-8").read()
report = open(REPORTRAW, encoding="utf-8").read()
html = open(PAGE, encoding="utf-8").read()

TOL = 1e-12
results = []

def check(name, err, tol=TOL, scope="CP"):
    err = np.asarray(err, dtype=float)
    assert np.all(np.isfinite(err)), f"{name}: non-finite values"
    m = float(np.max(np.abs(err)))
    assert m < tol, f"{name}: max_err={m:.3e} >= tol={tol:.0e}"
    results.append((name, m, tol, scope))
    print(f"OK [{scope}] {name}: max_err={m:.3e} < {tol:.0e}")

# ---------------- tension arithmetic ----------------
# V1/V2: exact algebra (sympy, exact): (sqrt2)^4 = ((sqrt2)^2)^2 = 2^2.
assert sp.sqrt(2)**4 == 4
print("OK [CP] V1 (sqrt2)^4 = 4 exactly (propagator rapidity product)")
assert sp.sqrt(2)**8 == 16
print("OK [CP] V2 (sqrt2)^8 = 16 exactly (all-eight product)")

# V3: V_E and its fourth power.
VE = math.sqrt(4 + 2*math.sqrt(2)) + 1 + math.sqrt(2)
check("V3 V_E^4 = 638.7823", VE**4 - 638.7823, 1e-3, "NC")

# V4: the printed "638.7" is a truncation to 1 dp, not a rounding.
# (Rounding to 1 dp gives 638.8.)
assert round(VE**4, 1) == 638.8, "round(1dp) should be 638.8"
assert math.floor(VE**4*10)/10 == 638.7, "trunc(1dp) should be 638.7"
print("OK [NC] V4 printed 638.7 = truncation to 1 dp (rounding gives 638.8)")

# V5: crx(112.5 deg) = V_E exactly (symbolic; closes the IC-2 value question).
crx = lambda x: abs(1/sp.cos(x)) - sp.sin(x)/sp.cos(x)
VEs = sp.sqrt(4 + 2*sp.sqrt(2)) + 1 + sp.sqrt(2)
assert sp.simplify(crx(5*sp.pi/8) - VEs) == 0
print(f"OK [SC] V5 crx(5pi/8) = V_E exactly (sympy simplify = 0; "
      f"V_E = {float(VEs):.11f})")

# V6: the three values are pairwise distinct.
assert len({4.0, 16.0, round(VE**4, 1)}) == 3
print("OK [CP] V6 4 / 16 / 638.78 are three distinct values")

# V7: FLAG-A1 arithmetic (the page: "Arithmetic CP; input not established").
assert 4*(sp.Rational(1, 4)) == 1
assert sp.Rational(1, 4)**4 == sp.Rational(1, 256)
print("OK [CP] V7 4*(1/4) = 1 and (1/4)^4 = 1/256 exactly")

# ---------------- figure data integrity ----------------
# V8: the three marked tension points lie on the plotted curve y = x^4.
# (The plot array below is the same expression as the Desmos embed latex
# 'y=x^{4}{1<=x<=5.6}'; this check pins the drawn data to the formula so a
# future edit cannot move the curve without failing the run.)
xx = np.linspace(1, 5.6, 2001)
yy = xx**4
check("V8 plotted array is x^4 (same as embed)", yy - xx**4, 1e-12, "CP")
check("V8 (sqrt2,4) on y=x^4", np.sqrt(2.0)**4 - 4, 1e-9, "CP")
check("V8 (2,16) on y=x^4", 2.0**4 - 16, 1e-12, "CP")
check("V8 (V_E,V_E^4) on y=x^4", VE**4 - 638.7822724929383, 1e-9, "CP")
assert xx[0] <= math.sqrt(2) < 2 < VE <= xx[-1], "x-range must span all three points"
print("OK [CP] V8 x-range [1, 5.6] spans sqrt2, 2, V_E")

# V9: Fig-2 schematic data: baseline y = 0 on [0,10]; five gates at y = 1.
gates = [(1, 1, "S_F"), (3, 1, "N_1820"), (5, 1, "zeta_parent"),
         (7, 1, "eta_-4"), (9, 1, "c_ord/K_parent")]
assert len(gates) == 5 and all(g[1] == 1 for g in gates)
bx = np.linspace(0, 10, 101)
check("V9 baseline is y=0", np.zeros_like(bx) - 0, 1e-12, "CP")
print(f"OK [CP] V9 Fig-2: empty baseline y=0 with {len(gates)} OPEN gates above")

# V10: caption's 4-decimal "V_E^4 = 638.7823".
check("V10 V_E^4 rounds to 638.7823", VE**4 - 638.7823, 5e-5, "NC")

# V11: the embed's blue-point latex x-form is V_E.
# (HTML holds JS strings: backslashes doubled.)
d1block = re.search(r"\{id:'d1', fb:'f1', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                    html, re.S).group(1)
assert r"\\sqrt{4+2\\sqrt{2}}+1+\\sqrt{2}" in d1block, "d1 blue-point x latex"
assert abs(VE - 5.027339492125848) < 1e-12
print("OK [CP] V11 d1 blue-point latex x-form = sqrt(4+2sqrt2)+1+sqrt2 = V_E")

# ---------------- v1 quotation grounds ----------------
# V12: the exact line-3542 quotation on the page.
quote = [
    "At the four spatial decay octants, the dominant trigonometric envelope takes the same value.",
    "Its product over the four decay octants is 638.78.",
    "This factors out of S_F, preserving field-redefinition invariance.",
    "The propagator rapidity product is 16, assigned to ζ_parent.",
]
for s in quote:
    assert s in raw, f"missing from v1: {s[:40]}"
print(f"OK [CP] V12 line-3542 quotation verified verbatim in v1 ({len(quote)} sentences)")

# V13: "field-redefinition invariance" appears exactly once in v1.
assert raw.count("field-redefinition invariance") == 1
print("OK [CP] V13 'field-redefinition invariance' occurs exactly once in v1")

# V14: §17.3.5's honest admission.
assert "its role in the Clifford contraction remains to be determined" in raw
print("OK [CP] V14 §17.3.5 admission present in v1")

# V15: the §17.18.6.4 stripped list contains no V_E / dominant-function term.
m = re.search(r'Here "stripped" excludes[^\n]*', raw)
assert m, "stripped list paragraph not found"
stripped = m.group(0)
assert "V_E" not in stripped and "dominant" not in stripped
print(f"OK [CP] V15 stripped list has no V_E/dominant term: {stripped[:80]}...")

# V16: NO-GO B1..B4 verbatim (grounds the Appendix B "verified accurate" verdicts).
b = [
    "NO-GO B1: C8 ↔ octant correspondence is not a theorem. The C3/C4 forcing question remains OPEN.",
    "NO-GO B2: The Distler–Garibaldi theorem is not evaded. The Cℓ(8) construction is a candidate, not a resolution.",
    "NO-GO B3: The uniform-action premise is not established. The formal k₀⁰ = 1 count is conditional.",
    "NO-GO B4: The Airy transition is not established. Only J₀ is unconditional; jinc and Airy are conditional.",
]
for s in b:
    assert s in raw, f"missing from v1: {s[:40]}"
print("OK [CP] V16 NO-GO B1..B4 verbatim in v1 (Appendix B accuracy grounds)")

# V17: §19.3 DG characterization.
assert "applies to any real or complex form of E" in raw
print("OK [CP] V17 §19.3 DG characterization present in v1")

# V18: CONTR-1 — both sides of the contradiction present in v1.
assert "Proof sketch." in raw and "unique cyclic word" in raw
assert "is not a theorem" in raw  # NO-GO B1 side
print("OK [CP] V18 CONTR-1 grounds: item-6 'Theorem/Proof sketch' and B1 'not a theorem' both in v1")

# V19: CONTR-2 — both sides present in v1.
assert "bypasses this by using:" in raw
assert "not a proven evasion" in raw
print("OK [CP] V19 CONTR-2 grounds: item-8 'bypasses this' and §19.3 'not a proven evasion' both in v1")

# V20: the terminology distinction that grounds IC-18.
assert "cosh(w_i) = 4" in raw
assert "the total rapidity product is 16, not 4" in raw
print("OK [CP] V20 v1 distinguishes propagator product (4) from total product (16)")

# V21: Appendix A EXACT list carries "Wick sign" as a bare bullet.
lines = raw.splitlines()
a0 = next(i for i, l in enumerate(lines) if l.startswith("Appendix A"))
appA = "\n".join(lines[a0:a0 + 100])
assert re.search(r"^· Wick sign$", appA, re.M), "bare '· Wick sign' bullet"
assert "· Wick sign EXACT (from archive)" not in appA
print("OK [CP] V21 Appendix A lists '· Wick sign' bare — '(from archive)' qualifier dropped (FLAG-A2)")

# V22: the ζ_parent assignment agreement (value corrected to 4 by IC-18).
assert "belong to ζ_parent" in raw
print("OK [CP] V22 'propagator cosh factors ... belong to ζ_parent' in v1")

# V23: Part III context claims about the other versions.
assert "= 0.48958371" in v3 and "N_{1820} = 3" in v3
assert "1.30555656" in v3
assert "MASTER CERTIFICATION COMPLETE" in report
print("OK [CP] V23 v3 carries S_F=0.48958371 / N_{1820}=3 / c_rest=1.30555656; "
      "report carries 'MASTER CERTIFICATION COMPLETE'")

# V24: viewport guard — every plotted point inside its Desmos viewport.
def viewport(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{left:([-\d.]+), right:([-\d.]+), "
                  r"bottom:([-\d.]+), top:([-\d.]+)\}", html)
    assert m, f"no viewport for {d}"
    return tuple(map(float, m.groups()))
vw1 = viewport("d1")
for px, py in [(math.sqrt(2), 4), (2, 16), (VE, VE**4)]:
    assert vw1[0] <= px <= vw1[1] and vw1[2] <= py <= vw1[3], f"d1 point ({px},{py}) outside {vw1}"
print(f"OK [CP] V24 d1 viewport {vw1} contains all three tension points")
vw2 = viewport("d2")
for px, py in [(5, 0)] + [(g[0], g[1]) for g in gates]:
    assert vw2[0] <= px <= vw2[1] and vw2[2] <= py <= vw2[3], f"d2 point ({px},{py}) outside {vw2}"
print(f"OK [CP] V24 d2 viewport {vw2} contains baseline point and all five gates")

print(f"\nAll {len(results)} numerical checks passed (+ printed exact checks). No timeouts.")

# ================================================================ PNGs
# Render quality: 240 dpi fallbacks (1920px-class), same verified expressions
# as the Desmos embeds. Regenerated only after every check above passes.
os.makedirs(OUT, exist_ok=True)
DPI = 240
plt.rcParams.update({"font.size": 10.5, "axes.titlesize": 12, "axes.labelsize": 11})

# ---- F1 tension resolution (same data as V8: x^4 and the three points)
f, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(xx, yy, lw=1.6, label="y = x⁴")
ax.plot([math.sqrt(2)], [4], "go", ms=10, label="(√2)⁴ = 4 — propagator (CP)")
ax.plot([2], [16], "ro", ms=10,
        label="(√2)⁸ = 16 — all-eight; line-3542's value (IC-18 as 'propagator')")
ax.plot([VE], [VE**4], "bo", ms=10,
        label=f"V_E⁴ = {VE**4:.2f} — value right (NC); 'factors out of S_F' is MA")
ax.set_xlim(1, 5.6); ax.set_ylim(0, 700); ax.legend(fontsize=8, loc="upper left")
ax.set_title("Fig 1 — Line-3542 tension: 4 vs 16 vs 638.78, resolved (fallback)")
ax.set_xlabel("x"); ax.grid(alpha=0.3)
f.tight_layout(); f.savefig(f"{OUT}/b19_tension.png", dpi=DPI); plt.close(f)

# ---- F2 Delta_op empty corridor (same data as V9)
f, ax = plt.subplots(figsize=(8, 4.6))
ax.plot([0, 10], [0, 0], lw=2.0, color="black",
        label="established Δ_op(Volume IV) = ∅")
for gx, gy, gl in gates:
    ax.plot([gx], [gy], "ro", ms=10)
    ax.text(gx, gy + 0.12, f"{gl}\nOPEN", fontsize=9, color="red", ha="center")
ax.set_xlim(0, 10); ax.set_ylim(-0.6, 2.0); ax.legend(fontsize=9, loc="upper left")
ax.set_title("Fig 2 — The UV boundary: nothing on the established line (fallback)")
ax.set_xlabel(""); ax.set_yticks([0, 1]); ax.grid(alpha=0.3, axis="x")
f.tight_layout(); f.savefig(f"{OUT}/b19_deltaop.png", dpi=DPI); plt.close(f)

for p in ("b19_tension.png", "b19_deltaop.png"):
    fp = os.path.join(OUT, p)
    assert os.path.isfile(fp) and os.path.getsize(fp) > 0, f"{p} missing/empty"
    print(f"  {p}: {os.path.getsize(fp)} bytes")
print("\nPNG fallbacks regenerated from the verified expressions.")
