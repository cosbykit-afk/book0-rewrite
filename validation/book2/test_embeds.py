#!/usr/bin/env python3
"""Book 2 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1 every <div class="graph" id="dN"> has a GRAPHS entry with matching fb id
 E2 every <img class="fallback" id="fN" src="graphs/..."> file exists, non-empty
 E3 each graph's latex contains the formula its caption/fallback claims
 E4 Desmos API loader present
"""
import os
import re

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book2/index.html")
html = open(PAGE).read()

# E1: graph divs <-> GRAPHS entries <-> fallback imgs
# (book2 uses class="graph" for the Desmos divs, like book1)
divs = re.findall(r'<div class="graph" id="(d\d+)">', html)
imgs = re.findall(r'<img class="fallback" id="(f\d+)" src="(graphs/[^"]+)"', html)
entries = re.findall(r"\{id:'(d\d+)', fb:'(f\d+)'", html)
assert divs, "no graph divs found"
assert len(divs) == len(imgs) == len(entries) == 7, \
    f"counts: divs={divs} imgs={imgs} entries={entries}"
for d, (eid, fb) in zip(divs, entries):
    assert d == eid, f"div {d} != entry {eid}"
for (eid, fb), (fid, src) in zip(entries, imgs):
    assert fb == fid, f"entry fb {fb} != img {fid}"
print("OK [E1] 7 graph divs <-> GRAPHS entries <-> fallback imgs linked")

# E2: fallback files exist and are non-empty
for fid, src in imgs:
    p = os.path.join(REPO, "book2", src)
    assert os.path.isfile(p), f"missing {p}"
    assert os.path.getsize(p) > 0, f"empty {p}"
print("OK [E2] all 7 fallback PNGs exist and are non-empty")

# E3: latex formula fragments per graph (must match the caption-claimed formulas)
def latex_of(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  html, re.S)
    assert m, f"no GRAPHS block for {d}"
    return m.group(1)

L = {d: latex_of(d) for d, _ in entries}
# Note: the HTML holds JS strings, so every latex backslash appears doubled.
checks = [
    # d1: canonical primitive quartet
    ("d1", r"\\left|\\frac{1}{\\sin(x)}\\right|+\\frac{\\cos(x)}{\\sin(x)}", "srx"),
    ("d1", r"\\left|\\frac{1}{\\sin(x)}\\right|-\\frac{\\cos(x)}{\\sin(x)}", "sxp"),
    ("d1", r"\\left|\\frac{1}{\\cos(x)}\\right|+\\frac{\\sin(x)}{\\cos(x)}", "cxp"),
    ("d1", r"\\left|\\frac{1}{\\cos(x)}\\right|-\\frac{\\sin(x)}{\\cos(x)}", "crx"),
    # d2: double-angle closure (caption: urx+uxp, 4/sin2x, product, 4/|sin2x|)
    ("d2", r"\\left|\\frac{1}{\\sin(x)}\\right|+\\frac{\\cos(x)}{\\sin(x)}-\\left|\\frac{1}{\\cos(x)}\\right|+\\frac{\\sin(x)}{\\cos(x)}", "urx summand"),
    ("d2", r"\\left|\\frac{1}{\\cos(x)}\\right|+\\frac{\\sin(x)}{\\cos(x)}-\\left|\\frac{1}{\\sin(x)}\\right|+\\frac{\\cos(x)}{\\sin(x)}", "uxp summand"),
    ("d2", r"\\frac{4}{\\sin(2x)}", "4/sin(2x) dashed"),
    ("d2", r"\\frac{4}{\\left|\\sin(2x)\\right|}", "4/|sin(2x)| dashed"),
    # d3: FlatWave rational collapse (caption: (srx+cxp)/(srx*cxp-1), sgn(sin2x))
    ("d3", r"\\frac{\\left|\\frac{1}{\\sin(x)}\\right|+\\frac{\\cos(x)}{\\sin(x)}+\\left|\\frac{1}{\\cos(x)}\\right|+\\frac{\\sin(x)}{\\cos(x)}}", "FlatWave numerator srx+cxp"),
    ("d3", r"\\operatorname{sign}(\\sin(2x))", "sgn(sin 2x) dashed"),
    # d4: Mobius branches (caption: M+, M-, diagonal, fixed-point dots)
    ("d4", r"\\frac{x+1}{x-1}\\left\\{x>1\\right\\}", "M+ branch"),
    ("d4", r"\\frac{1-x}{1+x}\\left\\{0<x<1\\right\\}", "M- branch"),
    ("d4", r"y=x", "reference diagonal"),
    ("d4", r"(\\sqrt{2}+1,\\sqrt{2}+1)", "fixed point sqrt2+1"),
    ("d4", r"(\\sqrt{2}-1,\\sqrt{2}-1)", "fixed point sqrt2-1"),
    # d5: same-phase reduction (caption: cxp(x), Mobius formula at srx(x))
    ("d5", r"y=\\left|\\frac{1}{\\cos(x)}\\right|+\\frac{\\sin(x)}{\\cos(x)}', color:'#1f77b4'", "cxp solid blue"),
    ("d5", r"\\operatorname{sign}(\\sin(2x))", "branch datum epsilon"),
    ("d5", r"\\operatorname{sign}(\\sin(2x))\\left(\\left|\\frac{1}{\\sin(x)}\\right|+\\frac{\\cos(x)}{\\sin(x)}\\right)-1}", "Mobius denominator eps*srx-1"),
    # d6: carrier ellipse (caption: v^2+4h^2=1/4 dashed, traced (H,V), x=0 dot)
    ("d6", r"y^{2}+4x^{2}=\\frac{1}{4}", "ellipse dashed"),
    ("d6", r"\\frac{\\sin(2\\pi t)}{4},\\frac{\\cos(2\\pi t)}{2}", "traced (H,V) parametric"),
    ("d6", r"(0,\\frac{1}{2})", "x=0 dot"),
    # d7: extraction through seams (caption: smooth H, raw reciprocal, H=0 dots)
    ("d7", r"y=\\frac{\\sin(2x)}{4}', color:'#1f77b4'", "H solid blue"),
    ("d7", r"y=\\frac{1}{\\left|\\frac{1}{\\sin(x)}\\right|", "raw reciprocal dashed"),
    ("d7", r"(-\\pi,0)", "seam dot -pi"),
    ("d7", r"(-\\frac{\\pi}{2},0)", "seam dot -pi/2"),
    ("d7", r"(0,0)", "seam dot 0"),
    ("d7", r"(\\frac{\\pi}{2},0)", "seam dot pi/2"),
    ("d7", r"(\\pi,0)", "seam dot pi"),
]
for d, frag, what in checks:
    assert frag in L[d], f"{d}: missing latex for {what}"
print(f"OK [E3] all {len(checks)} latex formula fragments present and match captions")

# E3b: expression counts per graph (caption-claimed curves and dots)
assert L["d1"].count("latex:") == 4, "d1 needs 4 exprs (the quartet)"
assert L["d2"].count("latex:") == 4, "d2 needs 4 exprs (sum, 4/sin2x, product, 4/|sin2x|)"
assert L["d3"].count("latex:") == 2, "d3 needs 2 exprs (rational form, sgn)"
assert L["d4"].count("latex:") == 5, "d4 needs 5 exprs (2 branches + diagonal + 2 dots)"
assert L["d5"].count("latex:") == 2, "d5 needs 2 exprs (cxp, Mobius formula)"
assert L["d6"].count("latex:") == 3, "d6 needs 3 exprs (ellipse + trace + dot)"
assert L["d7"].count("latex:") == 7, "d7 needs 7 exprs (H + raw reciprocal + 5 seam dots)"
print("OK [E3b] expression counts match the caption-claimed curves and dots")

# E3c: caption color claims (solid vs dashed, blue vs orange/red)
assert ("{latex:'y=\\\\frac{4}{\\\\sin(2x)}', color:'#ff7f0e', lineStyle:'dashed'}"
        in L["d2"]), "d2: 4/sin(2x) must be dashed orange"
assert ("{latex:'y=\\\\frac{4}{\\\\left|\\\\sin(2x)\\\\right|}', color:'#d62728', "
        "lineStyle:'dashed'}"
        in L["d2"]), "d2: 4/|sin(2x)| must be dashed red"
assert ("{latex:'y=\\\\operatorname{sign}(\\\\sin(2x))', color:'#d62728', "
        "lineStyle:'dashed'}"
        in L["d3"]), "d3: sgn(sin 2x) must be dashed red"
assert "lineStyle:'dashed'" in L["d5"].split("color:'#ff7f0e'")[1][:60] or \
    re.search(r"color:'#ff7f0e', lineStyle:'dashed'", L["d5"]), \
    "d5: Mobius formula must be dashed orange"
print("OK [E3c] dashed/solid color assignments match the captions")

# E4: Desmos loader (book2 pins v1.11 with an apiKey)
assert "https://www.desmos.com/api/" in html and "calculator.js" in html
print("OK [E4] Desmos API loader present")

print("\nAll embed consistency checks passed.")
