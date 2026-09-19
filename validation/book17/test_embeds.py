#!/usr/bin/env python3
"""Book 17 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1 every <div class="graph" id="dN"> has a GRAPHS entry with matching fb id
 E2 every <img class="fallback" id="fN" src="graphs/..."> file exists, non-empty
 E3 each graph's latex contains the formula its caption/fallback claims
 E4 Desmos API loader present
"""
import os
import re

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book17/index.html")
html = open(PAGE).read()

# E1: calc divs <-> GRAPHS entries <-> fallback imgs
divs = re.findall(r'<div class="graph" id="(d\d+)">', html)
imgs = re.findall(r'<img class="fallback" id="(f\d+)" src="(graphs/[^"]+)"', html)
entries = re.findall(r"\{id:'(d\d+)', fb:'(f\d+)'", html)
assert divs, "no graph divs found"
assert len(divs) == len(imgs) == len(entries) == 5, \
    f"counts: divs={divs} imgs={imgs} entries={entries}"
for d, (eid, fb) in zip(divs, entries):
    assert d == eid, f"div {d} != entry {eid}"
for (eid, fb), (fid, src) in zip(entries, imgs):
    assert fb == fid, f"entry fb {fb} != img {fid}"
print("OK [E1] 5 graph divs <-> GRAPHS entries <-> fallback imgs linked")

# E2: fallback files exist and are non-empty
for fid, src in imgs:
    p = os.path.join(REPO, "book17", src)
    assert os.path.isfile(p), f"missing {p}"
    assert os.path.getsize(p) > 0, f"empty {p}"
print("OK [E2] all 5 fallback PNGs exist and are non-empty")

# E3: latex formula fragments per graph (must match the caption-claimed formulas)
def latex_of(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  html, re.S)
    assert m, f"no GRAPHS block for {d}"
    return m.group(1)

L = {d: latex_of(d) for d, _ in entries}
# Note: the HTML holds JS strings, so every latex backslash appears doubled.
checks = [
    # d1: the two plotted primitives (caption: srx = |csc x| + cot x,
    #     cxp = |sec x| + tan x) + octant-boundary dashed lines + E-contact dots
    ("d1", r"\\left|\\frac{1}{\\sin(x)}\\right|+\\frac{\\cos(x)}{\\sin(x)}", "srx"),
    ("d1", r"\\left|\\frac{1}{\\cos(x)}\\right|+\\frac{\\sin(x)}{\\cos(x)}", "cxp"),
    ("d1", r"x=\\frac{\\pi}{4}", "octant boundary pi/4"),
    ("d1", r"(\\frac{\\pi}{8},\\sqrt{4+2\\sqrt{2}}+1+\\sqrt{2})", "V_E dot at 22.5 deg"),
    ("d1", r"(\\frac{5\\pi}{8},\\frac{1}{\\sqrt{4+2\\sqrt{2}}+1+\\sqrt{2}})", "1/V_E dot at 112.5 deg"),
    # d2: carrier ellipse (caption: V_R = cos(2x)/2, H = sin(2x)/4,
    #     ellipse V_R^2 + 4H^2 = 1/4 i.e. 4x^2 + 16y^2 = 1, traced 2:1)
    ("d2", r"4x^{2}+16y^{2}=1", "ellipse 4x^2+16y^2=1"),
    ("d2", r"\\left(\\frac{\\cos(2\\pi t)}{2},\\frac{\\sin(2\\pi t)}{4}\\right)",
     "parametric (V_R, H)"),
    ("d2", r"(\\frac{\\sqrt{2}}{4},\\frac{\\sqrt{2}}{8})", "E-contact ellipse point"),
    ("d2", r"(\\frac{1}{2},0)", "boundary point x=0"),
    ("d2", r"(0,\\frac{1}{4})", "boundary point x=45 deg"),
    # d3: Flatwave (caption: 1/urx + 1/uxp with urx = srx - crx, uxp = cxp - sxp;
    #     the embed writes crx = 1/g(x), sxp = 1/f(x))
    ("d3", r"f(x)=\\left|\\frac{1}{\\sin(x)}\\right|+\\frac{\\cos(x)}{\\sin(x)}", "f = srx"),
    ("d3", r"g(x)=\\left|\\frac{1}{\\cos(x)}\\right|+\\frac{\\sin(x)}{\\cos(x)}", "g = cxp"),
    ("d3", r"\\frac{1}{f(x)-\\frac{1}{g(x)}}+\\frac{1}{g(x)-\\frac{1}{f(x)}}",
     "1/(f-1/g) + 1/(g-1/f) = 1/urx + 1/uxp"),
    ("d3", r"y=1", "+1 reference line (Q1/Q3)"),
    ("d3", r"y=-1", "-1 reference line (Q2/Q4)"),
    # d4: paired footprint (caption: cos(4x); zeros at midpoints 22.5+k45 deg;
    #     boundaries +-1, not 0)
    ("d4", r"y=\\cos(4x)", "cos(4x) curve"),
    ("d4", r"(\\frac{\\pi}{8},0)", "zero at 22.5 deg midpoint"),
    ("d4", r"(\\frac{15\\pi}{8},0)", "zero at 337.5 deg midpoint"),
    ("d4", r"(\\frac{\\pi}{4},-1)", "boundary value -1 at 45 deg (IC-4)"),
    # d5: rapidity ladder (caption: w(x) = ln|cot x|; E-contact values +-w0,
    #     w0 = ln(1+sqrt2))
    ("d5", r"y=\\ln\\left|\\frac{\\cos(x)}{\\sin(x)}\\right|", "w(x) = ln|cot x|"),
    ("d5", r"y=\\ln(1+\\sqrt{2})", "+w0 dashed line"),
    ("d5", r"y=-\\ln(1+\\sqrt{2})", "-w0 dashed line"),
    ("d5", r"(\\frac{\\pi}{8},\\ln(1+\\sqrt{2}))", "E-contact +w0 at 22.5 deg"),
    ("d5", r"(\\frac{3\\pi}{8},-\\ln(1+\\sqrt{2}))", "E-contact -w0 at 67.5 deg"),
]
for d, frag, what in checks:
    assert frag in L[d], f"{d}: missing latex for {what}"
print(f"OK [E3] all {len(checks)} latex formula fragments present and match captions")

# expression counts per graph (caption-claimed content must all be embedded)
counts = {"d1": 13,  # 2 curves + 7 dashed octant boundaries + 4 E-contact dots
          "d2": 6,   # ellipse + parametric trace + 2 E dots + 2 boundary dots
          "d3": 5,   # f, g, Flatwave curve, y=+1, y=-1
          "d4": 11,  # cos(4x) + 8 midpoint zeros + 2 labeled boundary values
          "d5": 11}  # w(x) + 2 dashed +-w0 + 8 E-contact dots
for d, want in counts.items():
    got = L[d].count("latex:")
    assert got == want, f"{d}: {got} exprs, expected {want}"
print("OK [E3b] expression counts per graph match the caption-claimed content")

# E4: Desmos loader
assert "https://www.desmos.com/api/" in html and "calculator.js" in html
print("OK [E4] Desmos API loader present")

print("\nAll embed consistency checks passed.")
