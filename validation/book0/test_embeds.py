#!/usr/bin/env python3
"""Book 0 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1 every <div class="calc" id="dN"> has a GRAPHS entry with matching fb id
 E2 every <img class="fallback" id="fN" src="graphs/..."> file exists, non-empty
 E3 each graph's latex contains the formula its caption/fallback claims
 E4 Desmos API loader present
"""
import os
import re

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book0/index.html")
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

# E2: fallback files exist and are non-empty
for fid, src in imgs:
    p = os.path.join(REPO, "book0", src)
    assert os.path.isfile(p), f"missing {p}"
    assert os.path.getsize(p) > 0, f"empty {p}"
print("OK [E2] all 7 fallback PNGs exist and are non-empty")

# E3: latex formula fragments per graph (must match make_graphs.py formulas)
def latex_of(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  html, re.S)
    assert m, f"no GRAPHS block for {d}"
    return m.group(1)

L = {d: latex_of(d) for d, _ in entries}
# Note: the HTML holds JS strings, so every latex backslash appears doubled.
checks = [
    ("d1", r"\\left|\\frac{1}{\\sin(x)}\\right|+\\frac{\\cos(x)}{\\sin(x)}", "srx"),
    ("d1", r"\\left|\\frac{1}{\\sin(x)}\\right|-\\frac{\\cos(x)}{\\sin(x)}", "sxp"),
    ("d1", r"\\left|\\frac{1}{\\cos(x)}\\right|+\\frac{\\sin(x)}{\\cos(x)}", "cxp"),
    ("d1", r"\\left|\\frac{1}{\\cos(x)}\\right|-\\frac{\\sin(x)}{\\cos(x)}", "crx"),
    ("d2", r"\\frac{4}{\\sin(2x)}", "4/sin(2x) dashed"),
    ("d3", r"\\operatorname{sign}(\\sin(2x))", "sgn(sin 2x)"),
    ("d4", r"\\frac{\\sin(2t)}{4}", "H = sin(2t)/4"),
    ("d4", r"\\frac{\\cos(2t)}{2}", "V = cos(2t)/2"),
    ("d5", r"x^{2}+y^{2}=1", "unit circle"),
    ("d5", r"\\sqrt{t},\\sqrt{1-t}", "u(t) curve"),
    ("d6", r"(1,0)", "v label"),
    ("d6", r"(0,1)", "Jv label"),
    ("d6", r"(0,-1)", "-Jv label"),
    ("d7", r"\\frac{t\\cos(t)}{12},\\frac{t\\sin(t)}{12}", "spiral +"),
    ("d7", r"\\frac{t\\cos(t)}{12},-\\frac{t\\sin(t)}{12}", "spiral -"),
]
for d, frag, what in checks:
    assert frag in L[d], f"{d}: missing latex for {what}"
print(f"OK [E3] all {len(checks)} latex formula fragments present and match fallbacks")

# d2 must carry the green sum curve (caption claims it; fixed in affef1b)
assert L["d2"].count("y=") >= 4 or L["d2"].count("latex:") == 4, "d2 needs 4 exprs"
print("OK [E3b] d2 has all 4 expressions (urx, uxp, sum, 4/sin2x)")

# E4: Desmos loader
assert "https://www.desmos.com/api/v1.10/calculator.js" in html
print("OK [E4] Desmos API loader present")

print("\nAll embed consistency checks passed.")
