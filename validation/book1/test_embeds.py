#!/usr/bin/env python3
"""Book 1 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1 every <div class="graph" id="dN"> has a GRAPHS entry with matching fb id
 E2 every <img class="fallback" id="fN" src="graphs/..."> file exists, non-empty
 E3 each graph's latex contains the formula its caption/fallback claims
 E4 Desmos API loader present
"""
import os
import re

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book1/index.html")
html = open(PAGE).read()

# E1: calc divs <-> GRAPHS entries <-> fallback imgs
# (book1 uses class="graph" for the Desmos divs; book0 used class="calc")
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
print(f"OK [E1] 7 graph divs <-> GRAPHS entries <-> fallback imgs linked")

# E2: fallback files exist and are non-empty
for fid, src in imgs:
    p = os.path.join(REPO, "book1", src)
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
    # d1: the four factors (caption: Fs^pm = |csc x| +- cot x, Fc^pm = |sec x| +- tan x)
    ("d1", r"\\left|\\frac{1}{\\sin(x)}\\right|+\\frac{\\cos(x)}{\\sin(x)}", "Fs+"),
    ("d1", r"\\left|\\frac{1}{\\sin(x)}\\right|-\\frac{\\cos(x)}{\\sin(x)}", "Fs-"),
    ("d1", r"\\left|\\frac{1}{\\cos(x)}\\right|+\\frac{\\sin(x)}{\\cos(x)}", "Fc+"),
    ("d1", r"\\left|\\frac{1}{\\cos(x)}\\right|-\\frac{\\sin(x)}{\\cos(x)}", "Fc-"),
    # d2: half-angle chart (caption: cot(x/2), tan(x/2), tan(pi/4+x/2), tan(pi/4-x/2))
    ("d2", r"\\frac{\\cos(x/2)}{\\sin(x/2)}", "cot(x/2) form"),
    ("d2", r"\\frac{\\sin(x/2)}{\\cos(x/2)}", "tan(x/2) form"),
    ("d2", r"\\frac{\\sin(\\pi/4+x/2)}{\\cos(\\pi/4+x/2)}", "tan(pi/4+x/2) form"),
    ("d2", r"\\frac{\\sin(\\pi/4-x/2)}{\\cos(\\pi/4-x/2)}", "tan(pi/4-x/2) form"),
    ("d2", r"(\\frac{\\pi}{4},\\sqrt{2}+1)", "midpoint dot sqrt2+1"),
    ("d2", r"(\\frac{\\pi}{4},\\sqrt{2}-1)", "midpoint dot sqrt2-1"),
    # d3: branch signs (caption: alpha=sgn(sin x), beta=sgn(cos x), eps=sgn(sin 2x))
    ("d3", r"\\operatorname{sign}(\\sin(x))+2.2", "alpha + 2.2"),
    ("d3", r"\\operatorname{sign}(\\cos(x))", "beta"),
    ("d3", r"\\operatorname{sign}(\\sin(2x))-2.2", "epsilon - 2.2"),
    # d4: hyperbola locus (caption: dashed uv=1, traced (Fs+(x), Fs-(x)))
    ("d4", r"xy=1", "uv=1 dashed"),
    ("d4", r"\\frac{1}{\\sin(\\pi t/2)}", "parametric Fs pair"),
    # d5: diagonal crossing (caption: u=v diagonal, (Fs+(x), Fc+(x)) locus)
    ("d5", r"y=x", "diagonal"),
    ("d5", r"\\frac{1}{\\cos(\\pi t/2)}", "parametric Fc coordinate"),
    # d6: boundary zoom (same four factors as d1)
    ("d6", r"\\left|\\frac{1}{\\sin(x)}\\right|+\\frac{\\cos(x)}{\\sin(x)}", "Fs+"),
    ("d6", r"\\left|\\frac{1}{\\sin(x)}\\right|-\\frac{\\cos(x)}{\\sin(x)}", "Fs-"),
    ("d6", r"\\left|\\frac{1}{\\cos(x)}\\right|+\\frac{\\sin(x)}{\\cos(x)}", "Fc+"),
    ("d6", r"\\left|\\frac{1}{\\cos(x)}\\right|-\\frac{\\sin(x)}{\\cos(x)}", "Fc-"),
    # d7: phase circle (caption: unit circle, four seam classes, Q0 highlighted)
    ("d7", r"x^{2}+y^{2}=1", "unit circle"),
    ("d7", r"\\left(\\cos(t),\\sin(t)\\right)", "Q0 highlight arc"),
    ("d7", r"0\\le t\\le\\frac{\\pi}{2}", "arc domain = Q0"),
    ("d7", r"(1,0)", "[0] seam"),
    ("d7", r"(0,1)", "[pi/2] seam"),
    ("d7", r"(-1,0)", "[pi] seam"),
    ("d7", r"(0,-1)", "[3pi/2] seam"),
]
for d, frag, what in checks:
    assert frag in L[d], f"{d}: missing latex for {what}"
print(f"OK [E3] all {len(checks)} latex formula fragments present and match captions")

# d2 must carry 4 curves + 2 midpoint dots (caption claims the black dots)
assert L["d2"].count("latex:") == 6, "d2 needs 6 exprs (4 curves + 2 dots)"
print("OK [E3b] d2 has all 6 expressions (4 half-angle curves + 2 midpoint dots)")

# d7 must carry the Q0 highlight arc the caption claims (6 exprs now)
assert L["d7"].count("latex:") == 6, "d7 needs 6 exprs (circle + Q0 arc + 4 seams)"
print("OK [E3b2] d7 has all 6 expressions (circle + Q0 arc + 4 seam labels)")

# d4/d5 use the pi*t/2 display reparametrization the captions describe
assert r"\\pi t/2" in L["d4"] and r"\\pi t/2" in L["d5"]
print("OK [E3c] d4/d5 parametric forms use the captioned pi*t/2 reparametrization")

# E4: Desmos loader (book1 pins v1.11 with an apiKey)
assert "https://www.desmos.com/api/" in html and "calculator.js" in html
print("OK [E4] Desmos API loader present")

print("\nAll embed consistency checks passed.")
