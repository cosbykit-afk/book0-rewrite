#!/usr/bin/env python3
"""Book 12 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1 every <div class="calc" id="dN"> has a GRAPHS entry with matching fb id
 E2 every <img class="fallback" id="fN" src="graphs/..."> file exists, non-empty
 E3 each graph's latex contains the formula its caption/fallback claims
    (d3: full recomputed rational-lattice point list; d1/d5/d6/d7: marker
    values vs audited formulas)
 E4 Desmos API loader present
 ID: container/config/fallback id-match incl. negative control (the old
     test_graphs.py id test, subsumed here)
"""
import os
import re
from fractions import Fraction

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book12/index.html")
html = open(PAGE).read()

# E1: calc divs <-> GRAPHS entries <-> fallback imgs
divs = re.findall(r'<div class="calc" id="(d\d+)">', html)
imgs = re.findall(r'<img class="fallback" id="(f\d+)" src="(graphs/[^"]+)"', html)
entries = re.findall(r"\{id:'(d\d+)', fb:'(f\d+)'", html)
assert divs, "no calc divs found"
assert len(divs) == len(imgs) == len(entries) == 7, \
    f"counts: divs={divs} imgs={imgs} entries={entries}"
for d, (eid, fb) in zip(divs, entries):
    assert d == eid, f"div {d} != entry {eid}"
for (eid, fb), (fid, src) in zip(entries, imgs):
    assert fb == fid, f"entry fb {fb} != img {fid}"
print(f"OK [E1] 7 calc divs <-> GRAPHS entries <-> fallback imgs linked")
# uniqueness (negative control below mutates configs; containers must be unique)
assert len(set(divs)) == 7, "duplicate container ids"

# E2: fallback files exist and are non-empty
for fid, src in imgs:
    p = os.path.join(REPO, "book12", src)
    assert os.path.isfile(p), f"missing {p}"
    assert os.path.getsize(p) > 0, f"empty {p}"
print("OK [E2] all 7 fallback PNGs exist and are non-empty")

# ---- ID-match negative control: the old Volume-I-Book-1 bug pattern ----
# (d1-d7 containers, e1-e7 configs) must be caught.
broken = html
for n in range(1, 8):
    broken = broken.replace("{id:'d%d', fb:'f%d'" % (n, n),
                            "{id:'e%d', fb:'f%d'" % (n, n))
broken_entries = re.findall(r"\{id:'(d\d+|e\d+)', fb:'(f\d+)'", broken)
mismatch = [cid for cid, _ in broken_entries if cid not in divs]
assert mismatch, "NEGATIVE CONTROL FAILED: id mismatch not detected"
print(f"OK [ID-neg] negative control (e1-e7 configs) correctly detected: {mismatch}")

# E3: latex formula fragments per graph (must match caption-claimed formulas)
def latex_of(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  html, re.S)
    assert m, f"no GRAPHS block for {d}"
    return m.group(1)

L = {d: latex_of(d) for d, _ in entries}
# Note: the HTML holds JS strings, so every latex backslash appears doubled.
checks = [
    # d1: coordinate line y=x, four mass markers, three dashed anchors
    ("d1", r"y=x\\{-0.6\\le x\\le4.6\\}", "coordinate line y=x"),
    ("d1", r"(0,0)", "electron marker"),
    ("d1", r"(2.3155,2.3155)", "muon marker"),
    ("d1", r"(3.2639,3.2639)", "proton marker"),
    ("d1", r"(3.2645,3.2645)", "neutron marker"),
    ("d1", r"y=-17.9847", "128 Hz anchor"),
    ("d1", r"y=-17.7495", "220 Hz anchor"),
    ("d1", r"y=-10.9395", "21-cm line"),
    # d2: q_m curve and u^2(M) curve (M-axis shifted)
    ("d2", r"\\frac{10^{x}-1}{10^{x}+1}", "q_m = (10^x-1)/(10^x+1)"),
    ("d2", r"\\frac{4-(x+1.5)^{2}}{(x+1.5)^{2}}", "u^2(M) shifted"),
    # d3: rational lattice point list, 81/32 marker, measured-rho line
    ("d3", r"(2.531250,0.000262)", "81/32 marker"),
    ("d3", r"y=0", "rho = 0 reference line"),
    # d4: spectrum points, eigenvalue levels, gap arrow
    ("d4", r"(1,0.6)", "3/5 eigenvalue point"),
    ("d4", r"(3,-0.4)", "-2/5 eigenvalue point"),
    ("d4", r"y=0.6", "3/5 dashed level"),
    ("d4", r"y=-0.4", "-2/5 dashed level"),
    ("d4", r"gap = 1", "gap arrow label"),
    # d5: Casimir closure curve, N=3 marker
    ("d5", r"\\frac{x^{2}(x^{2}-9)}{4(x^{2}-1)}", "D(N) curve"),
    ("d5", r"(3,0)", "N=3 zero marker"),
    ("d5", r"N=3", "N=3 label"),
    # d6: cross-block capacity, H=6/25 marker
    ("d6", r"\\frac{2x}{(x+2)^{2}}", "H(N) curve"),
    ("d6", r"(3,0.24)", "H=6/25 marker"),
    ("d6", r"H=6/25", "H=6/25 label"),
    # d7: fixed-point curve, n_f=3 marker
    ("d7", r"\\frac{3x}{16+3x}", "a_q*(n_f) curve"),
    ("d7", r"(3,0.36)", "n_f=3 marker"),
    ("d7", r"n_f=3", "n_f=3 label"),
]
for d, frag, what in checks:
    assert frag in L[d], f"{d}: missing latex for {what}"
print(f"OK [E3] all {len(checks)} latex formula fragments present and match captions")

# E3b: d3 lattice completeness — every p/q (q<=64, |p/q-rho|<=0.01) in latex
rho = (939.56542052-938.27208816)/0.51099895
cands = sorted({Fraction(p, q) for q in range(1, 65) for p in range(1, 400)
                if abs(p/q - rho) <= 0.01})
for f in cands:
    assert f"{float(f):.6f}" in L["d3"], f"candidate {f} missing from d3 latex"
pts = re.findall(r"\((-?\d+\.\d+),(-?\d+\.\d+)\)",
                 re.search(r"\{latex:'(\[.*?\])'", L["d3"]).group(1))
assert len(pts) == len(cands), f"d3 point count {len(pts)} != {len(cands)}"
print(f"OK [E3b] d3 holds exactly the {len(cands)} lattice candidates, no extras")

# E3c: marker values agree with audited formulas (display rounding)
for d, val, tol, what in [
        ("d1", -17.9846644, 1e-3, "128 Hz anchor"),
        ("d1", -17.7494517, 1e-3, "220 Hz anchor"),
        ("d1", -10.9394619, 1e-3, "21-cm line"),
        ("d5", 4*(4-9)/(4*3), 5e-4, "D(2)"),
        ("d5", 16*(16-9)/(4*15), 5e-4, "D(4)"),
        ("d5", 25*(25-9)/(4*24), 5e-4, "D(5)"),
        ("d5", 36*(36-9)/(4*35), 5e-4, "D(6)"),
        ("d7", 3/(16+3), 5e-4, "a_q*(1)"),
        ("d7", 6/(16+6), 5e-4, "a_q*(2)"),
        ("d7", 12/(16+12), 5e-4, "a_q*(4)"),
        ("d7", 15/(16+15), 5e-4, "a_q*(5)"),
        ("d7", 18/(16+18), 5e-4, "a_q*(6)")]:
    nums = [float(x) for x in re.findall(r"-?\d+\.\d+", L[d])]
    best = min(nums, key=lambda v: abs(v - val))
    assert abs(best - val) < tol, f"{d} {what}: no literal near {val} (best {best})"
print("OK [E3c] all 12 marker literals agree with audited formulas to display rounding")

# E4: Desmos loader
assert "https://www.desmos.com/api/v1.10/calculator.js" in html
print("OK [E4] Desmos API loader present")

print("\nAll embed consistency checks passed.")
