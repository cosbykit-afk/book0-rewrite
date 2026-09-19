#!/usr/bin/env python3
"""Book 14 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1 every <div class="graph" id="dN"> has a GRAPHS entry with matching fb id
 E2 every <img class="fallback" id="fN" src="graphs/..."> file exists, non-empty
 E3 each graph's latex contains the formula its caption/fallback claims
 E4 Desmos API loader present (v1.11)
 E5 each graph's viewport covers every expression's plotted x-domain
    (book7 d1/d2 viewport-overreach precedent)
"""
import os
import re

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book14/index.html")
html = open(PAGE).read()

# E1: graph divs <-> GRAPHS entries <-> fallback imgs
divs = re.findall(r'<div class="graph" id="(d\d+)">', html)
imgs = re.findall(r'<img class="fallback" id="(f\d+)" src="(graphs/[^"]+)"', html)
entries = re.findall(r"\{id:'(d\d+)', fb:'(f\d+)'", html)
assert divs, "no graph divs found"
assert len(divs) == len(imgs) == len(entries) == 6, \
    f"counts: divs={divs} imgs={imgs} entries={entries}"
for d, (eid, fb) in zip(divs, entries):
    assert d == eid, f"div {d} != entry {eid}"
for (eid, fb), (fid, src) in zip(entries, imgs):
    assert fb == fid, f"entry fb {fb} != img {fid}"
print("OK [E1] 6 graph divs <-> GRAPHS entries <-> fallback imgs linked")

# E2: fallback files exist and are non-empty
for fid, src in imgs:
    p = os.path.join(REPO, "book14", src)
    assert os.path.isfile(p), f"missing {p}"
    assert os.path.getsize(p) > 0, f"empty {p}"
print("OK [E2] all 6 fallback PNGs exist and are non-empty")

# E3: latex formula fragments per graph (must match the caption claims)
def latex_of(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  html, re.S)
    assert m, f"no GRAPHS block for {d}"
    return m.group(1)

L = {d: latex_of(d) for d, _ in entries}
# Note: the HTML holds JS strings, so every latex backslash appears doubled.
checks = [
    ("d1", r"y=\\frac{x-1}{x+1}", "(x-1)/(x+1)"),
    ("d1", r"\\tanh\\left(\\frac{\\ln\\left(x\\right)}{2}\\right)",
     "tanh(ln x / 2) dashed"),
    ("d2", r"\\cosh\\left(\\ln\\left(4\\right)\\right)",
     "cosh(ln 4): q_m=0.6 -> lam_m=ln 4 exactly"),
    ("d2", r"1-0.36\\tanh\\left(\\frac{x}{2}\\right)^{2}",
     "rational form, q_m^2=0.36, dashed"),
    ("d3", r"\\frac{1+0.36x^{2}}{1+x^{2}}", "(1+0.36u^2)/(1+u^2)"),
    ("d4", r"\\frac{x\\left(4-x\\right)}{\\left(2-x\\right)^{2}}",
     "u^2 = B(4-B)/(2-B)^2"),
    ("d4", r"y=x\\left\\{0<x<1.8\\right\\}", "reduced-mass line y=x dashed"),
    ("d5", r"\\frac{\\left(x+1\\right)^{2}-\\left(x+0.3\\right)^{2}}"
           r"{\\left(x+0.3\\right)^{2}-\\left(x-1\\right)^{2}}",
     "u^2(m1), M=m1+0.3, m2=1"),
    ("d5", r"y=\\frac{0.7}{1.3}", "limit (m2-E)/(m2+E) = 0.7/1.3 dashed"),
    ("d6", r"y=\\cos\\left(2x\\right)", "cos 2a"),
    ("d6", r"y=\\sin\\left(2x\\right)", "sin 2a"),
]
for d, frag, what in checks:
    assert frag in L[d], f"{d}: missing latex for {what}"
print(f"OK [E3] all {len(checks)} latex formula fragments present and match captions")

# dashed-style counts must match the captions: d1,d2,d4,d5 one dashed each; d3,d6 none
expected_dashed = {"d1": 1, "d2": 1, "d3": 0, "d4": 1, "d5": 1, "d6": 0}
for d, n in expected_dashed.items():
    got = L[d].count("lineStyle:'dashed'")
    assert got == n, f"{d}: {got} dashed exprs, caption implies {n}"
print("OK [E3b] dashed styles match captions (d1,d2,d4,d5 dashed; d3,d6 solid)")

# E4: Desmos loader
assert "https://www.desmos.com/api/v1.11/calculator.js" in html
print("OK [E4] Desmos API loader present (v1.11)")

# E5: viewport covers every expression domain
def num(tok):
    # tok comes from the raw HTML (JS string): backslashes are doubled and a
    # domain bound may carry a trailing "\\right\\" from "\\right\\}".
    if tok.endswith("\\\\right\\\\"):
        tok = tok[:-len("\\\\right\\\\")]
    tok = tok.replace("\\\\", "\\")
    if tok == r"\pi":
        return 3.141592653589793
    return float(tok)

for d, _ in entries:
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{left:([^,]+), right:([^,]+),",
                  html)
    left, right = float(m.group(1)), float(m.group(2))
    doms = re.findall(r"\{([^{}]+)<x<([^{}]+)\}", L[d])
    assert doms, f"{d}: no x-domain found in latex"
    for a, b in doms:
        a, b = num(a), num(b)
        assert left <= a and right >= b, \
            f"{d}: viewport [{left},{right}] does not cover domain [{a},{b}]"
print("OK [E5] all 6 viewports cover their expression x-domains")

print("\nAll embed consistency checks passed.")
