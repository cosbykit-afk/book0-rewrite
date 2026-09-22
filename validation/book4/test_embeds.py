#!/usr/bin/env python3
"""Book 4 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1 every <div class="graph" id="gN"> has a GRAPHS entry with matching fb id,
    and every <img class="fallback" id="fN"> is referenced (no stale/extra ids,
    no duplicate id attributes)
 E2 every <img class="fallback" src="graphs/..."> file exists, non-empty
 E3 each graph's embedded latex contains the formula its caption claims
    (the HTML holds JS strings, so every latex backslash appears doubled)
 E4 Desmos API loader present (v1.11, as embedded on the page)
"""
import os
import re

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book4/index.html")
html = open(PAGE, encoding="utf-8").read()

# E0: no duplicate id attributes
ids = re.findall(r'id="([^"]+)"', html)
dupes = sorted({i for i in ids if ids.count(i) > 1})
assert not dupes, f"duplicate id attributes: {dupes}"
print(f"OK [E0] {len(ids)} id attributes, no duplicates")

# E1: graph divs <-> GRAPHS entries <-> fallback imgs
divs = re.findall(r'<div class="graph" id="(g\d+)">', html)
imgs = re.findall(r'<img class="fallback" id="(fb\d+)" src="(graphs/[^"]+)"', html)
entries = re.findall(r"\{id:'(g\d+)', fb:'(fb\d+)'", html)
assert divs, "no graph divs found"
assert len(divs) == len(imgs) == len(entries) == 7, \
    f"counts: divs={divs} imgs={imgs} entries={entries}"
for d, (eid, fb) in zip(divs, entries):
    assert d == eid, f"div {d} != entry {eid}"
for (eid, fb), (fid, src) in zip(entries, imgs):
    assert fb == fid, f"entry fb {fb} != img {fid}"
graph_divs = re.findall(r'<div class="graph" id="([^"]+)"', html)
fallback_imgs = re.findall(r'<img class="fallback" id="([^"]+)"', html)
assert set(graph_divs) == {e[0] for e in entries}, "stale/extra .graph div"
assert set(fallback_imgs) == {e[1] for e in entries}, "stale/extra fallback img"
print("OK [E1] 7 graph divs <-> GRAPHS entries <-> fallback imgs linked, "
      "no stale/extra ids")

# E2: fallback files exist and are non-empty
for fid, src in imgs:
    p = os.path.join(REPO, "book4", src)
    assert os.path.isfile(p), f"missing {p}"
    assert os.path.getsize(p) > 0, f"empty {p}"
print("OK [E2] all 7 fallback PNGs exist and are non-empty")

# E3: latex formula fragments per graph (must match make_graphs.py formulas)
def latex_of(g):
    m = re.search(r"\{id:'" + g + r"', fb:'fb\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  html, re.S)
    assert m, f"no GRAPHS block for {g}"
    return m.group(1)

L = {g: latex_of(g) for g, _ in entries}
checks = [
    # g1: six native sectors, synthetic right angle (caption: OA north,
    # OB/OC at +/-30 deg, D = (sqrt3, 0), OD perp OA)
    ("g1", r"x^{2}+y^{2}=1", "unit circle"),
    ("g1", r"(x-\\frac{\\sqrt{3}}{2})^{2}+(y-\\frac{1}{2})^{2}=1", "circle at B"),
    ("g1", r"(x-\\frac{\\sqrt{3}}{2})^{2}+(y+\\frac{1}{2})^{2}=1", "circle at C"),
    ("g1", r"(\\cos(\\frac{\\pi}{2})t,\\sin(\\frac{\\pi}{2})t)", "OA ray north"),
    ("g1", r"(\\sqrt{3}t,0)", "OD ray east"),
    ("g1", r"(\\sqrt{3},0)", "D point"),
    ("g1", r"\\operatorname{Polygon}((0.12,0),(0.12,0.12),(0,0.12))",
     "right-angle marker"),
    # g2: Flower grid (u = const: y = sqrt3 (x+k); v = const: horizontal)
    ("g2", r"x^{2}+y^{2}=1", "unit circle"),
    ("g2", r"y=\\sqrt{3}x", "u = 0 line"),
    ("g2", r"y=\\sqrt{3}(x+3)", "u = -3 line"),
    ("g2", r"y=\\frac{\\sqrt{3}}{2}", "v = 1 line"),
    # g3: tetrahedron; dashed altitude OG ends at the verified projection
    # of the centroid G (V13: (0.7891, 0.472))
    ("g3", r"\\operatorname{Segment}((0,0),(1,0))", "edge OA"),
    ("g3", r"\\operatorname{Segment}((0,0),(0.7891,0.472))", "dashed altitude OG"),
    ("g3", r"(0.8674,0.55)", "C point"),
    ("g3", r"(0.7891,0.472)", "G point"),
    # g4: polar coframe (circles r = 0.8, 1.6; red area parallelogram)
    ("g4", r"x^{2}+y^{2}=0.64", "circle r=0.8"),
    ("g4", r"x^{2}+y^{2}=2.56", "circle r=1.6"),
    ("g4", r"\\operatorname{Polygon}((0.5,0.866),(0.7,1.2124),"
            r"(0.3103,1.4374),(0.1103,1.091))", "red parallelogram"),
    ("g4", r"label:'e_r,e_φ'", "frame label"),
    # g5: unit circle, rotating frame spokes (orange), transported vector (blue)
    ("g5", r"x^{2}+y^{2}=1", "unit circle"),
    ("g5", r"\\operatorname{Segment}((1,0),(1,0.28))", "frame spoke e_phi"),
    ("g5", r"\\operatorname{Segment}((0.62,0),(0.92,0))", "transported vector"),
    ("g5", r"label:'frame e_φ'", "frame caption label"),
    ("g5", r"label:'transported vector'", "transport caption label"),
    # g6: z = 0 boundary; equal proper-radius circles rho*z0/L at
    # z0 = 0.6, 1.2, 2.2 with rho = 0.5, L = 1 (caption's radii)
    ("g6", r"y=0", "z = 0 boundary"),
    ("g6", r"x^{2}+(y-0.6)^{2}=0.09", "z0=0.6 circle (0.3^2)"),
    ("g6", r"x^{2}+(y-1.2)^{2}=0.36", "z0=1.2 circle (0.6^2)"),
    ("g6", r"x^{2}+(y-2.2)^{2}=1.21", "z0=2.2 circle (1.1^2)"),
    ("g6", r"label:'z₀=0.6'", "z0 label"),
    # g7: two ordered frames, e3 reflected (labels carry the volume sign)
    ("g7", r"\\operatorname{Segment}((-2.2,0),(-1.2,0))", "left e1"),
    ("g7", r"\\operatorname{Segment}((2.2,0),(2.75,0.55))", "right -e3"),
    ("g7", r"label:'+e₃ vol>0'", "positive-class label"),
    ("g7", "label:'\u2212e₃ vol<0'", "mirror-class label"),
]
for g, frag, what in checks:
    assert frag in L[g], f"{g}: missing latex for {what}"
print(f"OK [E3] all {len(checks)} latex formula fragments present and match "
      "captions/fallbacks")

# E4: Desmos loader
assert "https://www.desmos.com/api/v1.11/calculator.js" in html
print("OK [E4] Desmos API v1.11 loader present")

print("\nAll embed consistency checks passed.")
