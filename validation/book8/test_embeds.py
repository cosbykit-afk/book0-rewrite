#!/usr/bin/env python3
"""Book 8 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1 every <div class="calc" id="dN"> has a GRAPHS entry with matching fb id,
    paired with the <img class="fallback" id="fN">
 E2 every <img class="fallback" src="graphs/..."> file exists, non-empty
 E3 each graph's latex contains the formula its caption/fallback claims
 E4 Desmos API loader present
 E5 every plotted expression stays inside its declared viewport
    (the book7 d1/d2 viewport-overreach precedent)
 E6 NEGATIVE CONTROL: corrupted copies must FAIL

Subsumes validation/book8/test_ids_book8.py (removed 2026-09-19).
"""
import os
import re
import sys

import numpy as np

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book8/index.html")
GRAPHDIR = os.path.join(REPO, "book8/graphs")
html = open(PAGE).read()

# E1: calc divs <-> GRAPHS entries <-> fallback imgs
divs = re.findall(r'<div class="calc" id="(d\d+)">', html)
imgs = re.findall(r'<img class="fallback" id="(f\d+)" src="(graphs/[^"]+)"', html)
entries = re.findall(r"\{id:'(d\d+)',\s*fb:'(f\d+)'", html)
assert divs, "no calc divs found"
assert len(divs) == len(imgs) == len(entries) == 8, \
    f"counts: divs={divs} imgs={imgs} entries={entries}"
for d, (eid, fb) in zip(divs, entries):
    assert d == eid, f"div {d} != entry {eid}"
for (eid, fb), (fid, src) in zip(entries, imgs):
    assert fb == fid, f"entry fb {fb} != img {fid}"
print("OK [E1] 8 calc divs <-> GRAPHS entries <-> fallback imgs linked")

# E2: fallback files exist and are non-empty
for fid, src in imgs:
    p = os.path.join(REPO, "book8", src)
    assert os.path.isfile(p), f"missing {p}"
    assert os.path.getsize(p) > 0, f"empty {p}"
print("OK [E2] all 8 fallback PNGs exist and are non-empty")

# E3: latex formula fragments per graph.
# (The HTML holds JS strings, so every latex backslash appears doubled.)
def latex_of_in(h, d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  h, re.S)
    return m.group(1) if m else ""

def latex_of(d):
    blk = latex_of_in(html, d)
    assert blk, f"no GRAPHS block for {d}"
    return blk

def run_e3(h):
    errs = []
    cfgs = re.findall(r"\{id:'(d\d+)',\s*fb:'(f\d+)'", h)
    L = {d: latex_of_in(h, d) for d, _ in cfgs}
    for d, frag, what in FRAG_CHECKS:
        if d not in L or frag not in L[d]:
            errs.append(f"{d}: missing latex for {what}")
    if L.get("d1", "").count(r"y=\\cos(x)") != 2:
        errs.append("d1: needs both the green and red cos(x)")
    return errs

FRAG_CHECKS = [
    # d1: gauge redundancy — caption claims A1=sin x dy, A2=x dx+sin x dy, B=cos x dx^dy
    ("d1", r"y=\\sin(x)", "A1 = sin x dy (blue)"),
    ("d1", r"y=x", "A2 x-component x dx (orange)"),
    ("d1", r"y=\\cos(x)", "B = cos x dx^dy (green + red dashed)"),
    ("d1", "lineStyle:'dashed'", "dA2 dashed copy"),
    # d2: Hodge quarter-turn — caption claims F -> *F -> **F=-F
    ("d2", r"x^{2}+y^{2}=1", "unit circle"),
    ("d2", "(1,0)", "F point"), ("d2", "(0,1)", "*F point"),
    ("d2", "(-1,0)", "**F=-F point"),
    ("d2", r"0.55\\cos(t)", "quarter-turn arcs"),
    # d3: {+-1} in U(1)
    ("d3", r"x^{2}+y^{2}=1", "U(1) circle"),
    ("d3", "lineStyle:'dashed'", "dashed circle"),
    ("d3", "'+1'", "+1 dot"), ("d3", "'-1'", "-1 dot"),
    # d4: pure gauge — caption claims chi=sin2x, A=2cos2x dx, F=0
    ("d4", r"y=\\sin(2x)", "chi = sin 2x (blue)"),
    ("d4", r"y=2\\cos(2x)", "A = 2cos 2x dx (orange)"),
    ("d4", r"y=0", "F = 0 flat (green)"),
    # d5: theta boundary cartoon — caption claims b=e^{-x^2}, db/dx=-2x e^{-x^2}
    ("d5", r"y=e^{-x^{2}}", "bump b(x) (blue)"),
    ("d5", r"y=-2xe^{-x^{2}}", "theta density db/dx (orange)"),
    # d6: symmetric potentials — caption claims 1-cos4phi, 1+cos4phi, vacua
    ("d6", r"y=1-\\cos(4x)", "1-cos4phi (blue)"),
    ("d6", r"y=1+\\cos(4x)", "1+cos4phi (orange)"),
    ("d6", r"0\\le x\\le\\pi", "domain restriction to [0,pi]"),
    ("d6", r"(\\frac{\\pi}{2},0)", "vacuum dot at pi/2"),
    ("d6", r"(\\frac{\\pi}{4},0)", "vacuum dot at pi/4"),
    # d7: Bloch meridian + ceiling — caption claims arc, 4x(1-x) ceiling, (0.5,1)
    ("d7", r"2\\sqrt{t(1-t)}", "meridian arc (blue)"),
    ("d7", r"y=4x(1-x)", "coherency ceiling (orange dashed)"),
    ("d7", "lineStyle:'dashed'", "dashed ceiling"),
    ("d7", "(0.5,1)", "lambda=1/2 point"),
    # d8: witness circle vs failed invariant
    ("d8", r"\\cos(2t),\\sin(2t)", "witness circle (blue)"),
    ("d8", r"y=-\\cos(4x)", "direct-quadrature invariant (orange dashed)"),
    ("d8", "lineStyle:'dashed'", "dashed invariant"),
]
e3errs = run_e3(html)
assert not e3errs, f"E3 failures: {e3errs}"
print(f"OK [E3] all {len(FRAG_CHECKS)} latex formula fragments present and match "
      "captions/fallbacks")

# E4: Desmos loader
assert "https://www.desmos.com/api/v1.10/calculator.js" in html
print("OK [E4] Desmos API loader present")

# E5: viewport containment — plotted expressions must fit their vw box.
def viewport(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{left:([^,]+), right:([^,]+), "
                  r"bottom:([^,]+), top:([^}]+)\}", html)
    assert m, f"no viewport for {d}"
    return tuple(float(v) for v in m.groups())

def check_vw(d, xs, ys_list):
    l, r, b, t = viewport(d)
    assert np.min(xs) >= l and np.max(xs) <= r, f"{d}: x-range overruns viewport"
    for ys in ys_list:
        ys = np.asarray(ys, dtype=float)
        assert np.min(ys) >= b and np.max(ys) <= t, \
            f"{d}: y-range [{np.min(ys):.3f},{np.max(ys):.3f}] overruns [{b},{t}]"

x1 = np.linspace(-7, 7, 2001)
check_vw("d1", x1, [np.sin(x1), x1, np.cos(x1)])
th = np.linspace(0, 2*np.pi, 721)
check_vw("d2", np.concatenate([np.cos(th), [1., 0., -1.], 0.55*np.cos(th)]),
             [np.sin(th), np.array([0., 1., 0.]), 0.55*np.sin(th)])
check_vw("d3", np.concatenate([np.cos(th), [1., -1.]]),
             [np.sin(th), np.array([0., 0.])])
check_vw("d4", x1, [np.sin(2*x1), 2*np.cos(2*x1), np.zeros_like(x1)])
x5 = np.linspace(-3.5, 3.5, 2001)
check_vw("d5", x5, [np.exp(-x5**2), -2*x5*np.exp(-x5**2)])
x6 = np.linspace(0, np.pi, 2001)
check_vw("d6", x6, [1-np.cos(4*x6), 1+np.cos(4*x6), np.zeros_like(x6)])
lam7 = np.linspace(0, 1, 2001)
check_vw("d7", lam7, [2*np.sqrt(lam7*(1-lam7)), 4*lam7*(1-lam7)])
check_vw("d8", np.cos(2*th), [np.sin(2*th), -np.cos(4*np.linspace(-1.4, 1.4, 2001))])
print("OK [E5] all 8 graphs' plotted expressions fit their viewports")

# E6: negative control — corrupted copies must FAIL
bad = html.replace("{id:'d3', fb:'f3'", "{id:'d9', fb:'f3'", 1)
bad = bad.replace('src="graphs/b8_g4_puregauge.png"', 'src="graphs/NOPE.png"', 1)
bad = bad.replace("y=-\\\\cos(4x)", "y=-\\\\cos(5x)", 1)
errs = []
cfgs = re.findall(r"\{id:'(d\d+)',\s*fb:'(f\d+)'", bad)
for cid, fb in cfgs:
    if len(re.findall(r'id="%s"' % cid, bad)) != 1:
        errs.append(f"container {cid}")
for m in re.finditer(r'<img[^>]*id="(f\d+)"[^>]*src="([^"]+)"', bad):
    p = os.path.join(GRAPHDIR, os.path.basename(m.group(2)))
    if not os.path.isfile(p):
        errs.append(f"missing {m.group(2)}")
# the d8 latex corruption must be caught by the E3 fragment check
e3bad = run_e3(bad)
if not any(e.startswith("d8:") for e in e3bad):
    print("NEGATIVE CONTROL FAILED: d8 latex corruption not detected")
    sys.exit(2)
errs.append("d8 latex corrupted (E3 fragment check)")
assert errs, "NEGATIVE CONTROL FAILED: corrupted page passed (test is blind)"
print(f"OK [E6] negative control: corrupted page rejected ({len(errs)} errors)")

print("\nAll embed consistency checks passed.")
