#!/usr/bin/env python3
"""Book 18 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1 every <div class="graph" id="dN"> has a GRAPHS entry with matching fb id
 E2 every <img class="fallback" id="fN" src="graphs/..."> file exists, non-empty
 E3 each graph's latex contains the formula its caption/fallback claims
 E3b expression counts per graph match the captioned content
 E3c every Desmos viewport contains its claimed points (no viewport overreach)
 E4 Desmos API loader present
"""
import os
import re

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book18/index.html")
html = open(PAGE).read()

# E1: calc divs <-> GRAPHS entries <-> fallback imgs
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
    p = os.path.join(REPO, "book18", src)
    assert os.path.isfile(p), f"missing {p}"
    assert os.path.getsize(p) > 0, f"empty {p}"
print("OK [E2] all 6 fallback PNGs exist and are non-empty")

# E3: latex formula fragments per graph (must match the caption-claimed formulas)
# Note: the HTML holds JS strings, so every latex backslash appears doubled.
def latex_of(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  html, re.S)
    assert m, f"no GRAPHS block for {d}"
    return m.group(1)

L = {d: latex_of(d) for d, _ in entries}
checks = [
    # d1: C(n,4) curve + (16,1820) dot (caption: C(n,4)=n(n-1)(n-2)(n-3)/24)
    ("d1", r"\\frac{x(x-1)(x-2)(x-3)}{24}", "C(n,4) curve"),
    ("d1", r"(16,1820)", "green dot (16,1820)"),
    ("d1", "C(16,4)=1820", "dot label"),
    # d2: Sym^2 / Alt^2 curves, dots, 120 line (caption: dims, IC-12 exhibit)
    ("d2", r"\\frac{x(x+1)}{2}", "dim Sym^2 curve"),
    ("d2", r"\\frac{x(x-1)}{2}", "dim Alt^2 curve"),
    ("d2", r"(128,8256)", "Sym^2(128)=8256 dot"),
    ("d2", r"(128,8128)", "Alt^2(128)=8128 dot"),
    ("d2", r"y=120", "red dashed y=120"),
    ("d2", r"(135,120)", "120 marker point"),
    ("d2", "not in Sym", "IC-12 label"),
    # d3: branching staircase 54 -> 74 -> 134 -> 135 (caption: partial sums)
    ("d3", r"y=54", "staircase 54"),
    ("d3", r"y=74", "staircase 74"),
    ("d3", r"y=134", "staircase 134"),
    ("d3", r"y=135", "staircase 135"),
    ("d3", "(54,1)", "branch (54,1)"),
    ("d3", "(1,20')", "branch (1,20')"),
    ("d3", "(10,6)", "branch (10,6)"),
    ("d3", "(1,1)", "branch (1,1)"),
    # d4: conversion chain lines a=S_F/3, c=5S_F/18 (caption: algebraic closure)
    ("d4", r"\\frac{x}{3}", "a = S_F/3 line"),
    ("d4", r"\\frac{5x}{18}", "c = 5S_F/18 line"),
    ("d4", r"(3,1)", "a marker"),
    ("d4", r"(3,\\frac{5}{6})", "c marker"),
    ("d4", "a=S_F/3", "a label"),
    ("d4", "c=5S_F/18", "c label"),
    # d5: projector lines Pi_pm (caption: values {0,1} at gamma_17=+-1)
    ("d5", r"\\frac{1+x}{2}", "Pi_+ line"),
    ("d5", r"\\frac{1-x}{2}", "Pi_- line"),
    ("d5", r"(-1,0)", "corner dot"),
    ("d5", r"(-1,1)", "corner dot"),
    ("d5", r"(1,1)", "corner dot"),
    ("d5", r"(1,0)", "corner dot"),
    ("d5", "conditional", "conditional label"),
    # d6: C8 word circle + E/B/O markers + NOT-established center
    # (caption: (E,B,E,O)x2, E on 1,3,5,7; B on 2,6; O on 4,8)
    ("d6", r"(\\cos(2\\pi t),\\sin(2\\pi t))", "unit circle"),
    ("d6", "E1", "E1 marker"), ("d6", "B2", "B2 marker"),
    ("d6", "E3", "E3 marker"), ("d6", "O4", "O4 marker"),
    ("d6", "E5", "E5 marker"), ("d6", "B6", "B6 marker"),
    ("d6", "E7", "E7 marker"), ("d6", "O8", "O8 marker"),
    ("d6", r"(0,0)", "center point"),
    ("d6", "NOT established", "center label"),
]
for d, frag, what in checks:
    assert frag in L[d], f"{d}: missing latex for {what}"
print(f"OK [E3] all {len(checks)} latex formula fragments present and match captions")

# E3b: expression counts per graph match the captioned content
expected_counts = {"d1": 2, "d2": 6, "d3": 8, "d4": 4, "d5": 6, "d6": 10}
for d, n in expected_counts.items():
    got = L[d].count("latex:")
    assert got == n, f"{d}: {got} exprs, expected {n}"
print("OK [E3b] expression counts per graph: " +
      ", ".join(f"{d}={n}" for d, n in expected_counts.items()))

# E3c: every viewport contains its claimed points (no viewport overreach)
vws = {}
for d, _ in entries:
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{([^}]*)\}", html)
    assert m, f"no viewport for {d}"
    vw = dict(re.findall(r"(left|right|bottom|top):(-?[\d.]+)", m.group(1)))
    vws[d] = {k: float(v) for k, v in vw.items()}

def inside(d, x, y, what):
    vw = vws[d]
    assert vw["left"] <= x <= vw["right"] and vw["bottom"] <= y <= vw["top"], \
        f"{d}: point {what}=({x},{y}) outside viewport {vw}"

inside("d1", 16, 1820, "(16,1820)")
inside("d1", 20, 4845, "C(20,4) curve end")   # curve must fit the frame
inside("d2", 128, 8256, "(128,8256)")
inside("d2", 128, 8128, "(128,8128)")
inside("d2", 135, 120, "(135,120)")
inside("d2", 140, 9870, "Sym^2(140) curve end")
inside("d3", 0.5, 54, "staircase")
inside("d3", 3.5, 135, "staircase top")
inside("d4", 3, 1, "a marker")
inside("d4", 3, 5/6, "c marker")
inside("d5", -1, 0, "corner"); inside("d5", -1, 1, "corner")
inside("d5", 1, 1, "corner"); inside("d5", 1, 0, "corner")
import math as _math
for k in range(8):  # d6: circle markers + 1.18x label offsets
    a = _math.pi/8 + k*_math.pi/4
    inside("d6", _math.cos(a), _math.sin(a), f"marker {k+1}")
    inside("d6", 1.18*_math.cos(a), 1.18*_math.sin(a), f"label {k+1}")
print("OK [E3c] all viewports contain their claimed points (no overreach)")

# E4: Desmos loader
assert "https://www.desmos.com/api/" in html and "calculator.js" in html
print("OK [E4] Desmos API loader present")

print("\nAll embed consistency checks passed.")
