#!/usr/bin/env python3
"""Book 11 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1  every <div class="calc" id="dN"> has a GRAPHS entry with matching fb id,
     and every entry links to the matching <img class="fallback">
 E2  every fallback PNG exists, is non-empty, and has PNG magic bytes
 E3  each graph's latex contains the formula/points its caption and fallback claim
 E3b color-caption consistency (d1 crx green per caption; d5 purple walk;
     d7 blue pattern / red mirror)
 E3c viewport sanity: d1 stays within a benign margin of the arcsin domain;
     point-graph viewports contain their points
 E4  Desmos API loader present
 E5  negative control: a corrupted copy (d3 -> e3) must be caught
"""
import os
import re

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book11/index.html")
html = open(PAGE).read()

# ---------- E1 ----------
divs = re.findall(r'<div class="calc" id="(d\d+)">', html)
imgs = re.findall(r'<img class="fallback" id="(f\d+)" src="(graphs/[^"]+)"', html)
entries = re.findall(r"\{id:'(d\d+)', fb:'(f\d+)'", html)
assert divs, "no calc divs found"
assert [f"d{i}" for i in range(1, 8)] == divs == [e for e, _ in entries], \
    f"div/entry mismatch: divs={divs} entries={entries}"
assert [f"f{i}" for i in range(1, 8)] == [f for _, f in entries] == [f for f, _ in imgs], \
    "fallback id linkage broken"
print("OK [E1] 7 calc divs <-> GRAPHS entries <-> fallback imgs linked in order")

# ---------- E2 ----------
for fid, src in imgs:
    p = os.path.join(REPO, "book11", src)
    assert os.path.isfile(p), f"missing {p}"
    assert os.path.getsize(p) > 0, f"empty {p}"
    with open(p, "rb") as fh:
        assert fh.read(8) == b"\x89PNG\r\n\x1a\n", f"bad PNG magic: {p}"
print("OK [E2] all 7 fallback PNGs exist, non-empty, valid PNG magic")

# ---------- E3 ----------
def latex_of(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  html, re.S)
    assert m, f"no GRAPHS block for {d}"
    return m.group(1)

L = {f"d{i}": latex_of(f"d{i}") for i in range(1, 8)}
# Note: the HTML holds JS strings, so every latex backslash appears doubled.
checks = [
    # d1: helicity odds; caption: cxp=e^eta (blue) = dashed sqrt, crx=e^-eta (green)
    ("d1", r"\\left|\\frac{1}{\\cos(\\arcsin(x))}\\right|+\\tan(\\arcsin(x))", "cxp curve"),
    ("d1", r"\\sqrt{\\frac{1+x}{1-x}}", "dashed sqrt((1+b)/(1-b))"),
    ("d1", r"\\left|\\frac{1}{\\cos(\\arcsin(x))}\\right|-\\tan(\\arcsin(x))", "crx curve"),
    # d2: six weights 0,+1,+1/6,-2/3,+1/3,-1/2 (caption order)
    ("d2", r"(1,0)", "block (1,1)_0"), ("d2", r"(2,1)", "block (1,1)_{+1}"),
    ("d2", r"(3,\\frac{1}{6})", "block (2,3)"), ("d2", r"(4,-\\frac{2}{3})", "(1,3b)_{-2/3}"),
    ("d2", r"(5,\\frac{1}{3})", "(1,3b)_{+1/3}"), ("d2", r"(6,-\\frac{1}{2})", "(2,1)"),
    # d3: sixteen charges; spot-check distinctive points, count all 16
    ("d3", r"(1,\\frac{2}{3})", "u-type charge"), ("d3", r"(7,-\\frac{2}{3})", "anti-u charge"),
    ("d3", r"(14,-1)", "electron charge"), ("d3", r"(16,1)", "positron charge"),
    # d4: integral lattice 0,6,1,-4,2,-3
    ("d4", r"(1,0)", "x=0"), ("d4", r"(2,6)", "x=6"), ("d4", r"(3,1)", "x=1"),
    ("d4", r"(4,-4)", "x=-4"), ("d4", r"(5,2)", "x=2"), ("d4", r"(6,-3)", "x=-3"),
    # d5: anomaly walk cumulative points + zero line
    ("d5", r"(1,1)", "walk start 1"), ("d5", r"(2,\\frac{37}{36})", "1+1/36"),
    ("d5", r"(3,\\frac{5}{36})", "-8/9 step"), ("d5", r"(4,\\frac{1}{4})", "+1/9 step"),
    ("d5", r"(5,0)", "lands on zero"), ("d5", r"(6,0)", "stays zero"),
    ("d5", r"y=0", "dashed zero line"),
    # d6: unit circle + six roots of unity
    ("d6", r"x^{2}+y^{2}=1", "unit circle"),
    ("d6", r"(\\frac{1}{2},\\frac{\\sqrt{3}}{2})", "primitive 6th root"),
    ("d6", r"(-\\frac{1}{2},-\\frac{\\sqrt{3}}{2})", "conjugate root"),
    # d7: mirror pair, six blue + six sign-reversed red
    ("d7", r"(3,\\frac{1}{6})", "blue weight"), ("d7", r"(3,-\\frac{1}{6})", "red mirror"),
    ("d7", r"(4,\\frac{2}{3})", "red mirror of -2/3"),
]
for d, frag, what in checks:
    assert frag in L[d], f"{d}: missing latex for {what}"
n_d3 = len(re.findall(r"latex:'\(\d+,", L["d3"]))
assert n_d3 == 16, f"d3 has {n_d3} point exprs, caption claims 16 components"
n_d7 = len(re.findall(r"latex:'\(\d+,", L["d7"]))
assert n_d7 == 12, f"d7 has {n_d7} point exprs, expected 12 (6+6 mirror)"
print(f"OK [E3] all {len(checks)} latex formula fragments present; "
      "d3 has 16 points, d7 has 12")

# ---------- E3b: color-caption consistency ----------
def colors_of(d):
    return re.findall(r"color:'(#[0-9a-f]{6})'", latex_of(d))
c1 = colors_of("d1")
assert c1[0] == "#1f77b4", f"d1 cxp should be blue, got {c1[0]}"   # caption: cxp blue
assert c1[2] == "#2ca02c", f"d1 crx should be green, got {c1[2]}"  # caption: crx green
assert "#9467bd" in colors_of("d5"), "d5 walk should be purple (#9467bd)"
c7 = colors_of("d7")
assert c7[:6] == ["#1f77b4"] * 6 and c7[6:] == ["#d62728"] * 6, \
    f"d7 should be 6 blue + 6 red, got {c7}"  # caption: blue pattern, red mirror
print("OK [E3b] colors match captions (d1 blue/green, d5 purple, d7 blue/red)")

# ---------- E3c: viewport sanity ----------
def viewport(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{([^}]*)\}", html)
    assert m, f"no viewport for {d}"
    return dict(re.findall(r"(left|right|bottom|top):(-?[\d.]+)", m.group(1)))
vw1 = {k: float(v) for k, v in viewport("d1").items()}
# d1 plots over the arcsin domain (-1,1); the viewport keeps a small benign
# margin and shows no region where the caption makes a false claim.
assert -1.1 <= vw1["left"] < -1.0 and 1.0 < vw1["right"] <= 1.1, vw1
for d, xs, ys in [("d2", (1, 6), (-1, 1)), ("d3", (1, 16), (-1.2, 1.2)),
                  ("d4", (1, 6), (-4.5, 6.5)), ("d5", (1, 6), (-0.2, 1.2)),
                  ("d7", (1, 6), (-1.2, 1.2))]:
    vw = {k: float(v) for k, v in viewport(d).items()}
    assert vw["left"] <= xs[0] and vw["right"] >= xs[1], f"{d} clips points in x"
    assert vw["bottom"] <= ys[0] and vw["top"] >= ys[1], f"{d} clips points in y"
vw6 = {k: float(v) for k, v in viewport("d6").items()}
assert vw6["left"] <= -1 and vw6["right"] >= 1 and vw6["bottom"] <= -1 and vw6["top"] >= 1
print("OK [E3c] viewports contain all plotted points; d1 margin benign")

# ---------- E4 ----------
assert "https://www.desmos.com/api/v1.10/calculator.js" in html
print("OK [E4] Desmos API loader present")

# ---------- E5: negative control ----------
bad = html.replace('<div class="calc" id="d3">', '<div class="calc" id="e3">', 1)
open("/tmp/book11_neg.html", "w").write(bad)
neg = open("/tmp/book11_neg.html").read()
divs2 = re.findall(r'<div class="calc" id="(d\d+)">', neg)
entries2 = re.findall(r"\{id:'(d\d+)', fb:'(f\d+)'", neg)
detected = (divs2 != [e for e, _ in entries2])
assert detected, "NEGATIVE CONTROL FAILED TO TRIGGER - TEST IS BROKEN"
print("OK [E5] negative control: deliberate d3->e3 mismatch correctly detected")

print("\nAll embed consistency checks passed (incl. negative control).")
