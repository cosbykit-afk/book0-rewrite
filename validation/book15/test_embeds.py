#!/usr/bin/env python3
"""Embed consistency for book15/index.html.

Checks: 6 graph divs <-> fallback imgs <-> captions; each div's Desmos
expressions match the pictured (and fallback) formulas; d5 carries the two
s_Omega sign-marker dots the caption claims; d1/d4 stay on the principal
chart; d2's dashed hyperbola is the right branch only; loader pinned v1.11.

Note on backslashes: the HTML stores Desmos latex inside JS strings, so the
file holds doubled backslashes (e.g. ``\\\\frac`` on disk = ``\\frac`` in the
JS string = ``\\frac`` for Desmos). Fragments below are raw strings matching
the on-disk form.

Live Desmos rendering is NOT browser-verified (stated on the page); this
suite checks static ID/expression/formula consistency only.

Exit 0 iff every assertion passes.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "..", "..", "book15", "index.html")
GRAPH_DIR = os.path.join(HERE, "..", "..", "book15", "graphs")

passed = []


def ok(name):
    passed.append(name)
    print(f"OK {name}")


def fail(name, detail=""):
    print(f"FAIL {name} {detail}")
    sys.exit(1)


src = open(PAGE, encoding="utf-8").read()

# ---------- E1: exactly 6 graph divs, ids d1..d6 ----------
divs = re.findall(r'<div class="graph" id="(d\d+)">', src)
if divs != [f"d{i}" for i in range(1, 7)]:
    fail("E1 six graph divs d1..d6", f"found {divs}")
ok("E1 six graph divs d1..d6")

# ---------- E2: exactly 6 fallback imgs, ids f1..f6, PNGs exist+nonempty ----------
imgs = re.findall(r'<img class="fallback" id="(f\d+)" src="graphs/(g\d+_\w+\.png)"', src)
expect = [(f"f{i}", n) for i, n in enumerate(
    ["g1_primitives.png", "g2_hyperbola.png", "g3_phasor.png",
     "g4_saw.png", "g5_meridian.png", "g6_exterior.png"], start=1)]
if imgs != expect:
    fail("E2 six fallback imgs f1..f6", f"found {imgs}")
for fid, png in imgs:
    p = os.path.join(GRAPH_DIR, png)
    if not (os.path.isfile(p) and os.path.getsize(p) > 0):
        fail("E2 fallback PNG exists+nonempty", p)
ok("E2 six fallback imgs f1..f6, PNGs exist and nonempty")

# ---------- E5: GRAPHS table pairs dN <-> fN ----------
entries = re.findall(r"\{id:'(d\d)', fb:'(f\d)', vw:\{([^}]*)\}, exprs:\[(.*?)\]\}",
                     src, re.S)
if len(entries) != 6:
    fail("E5 six GRAPHS entries", f"found {len(entries)}")
for did, fid, vw, exprs in entries:
    if did[1:] != fid[1:]:
        fail("E5 dN<->fN pairing", f"{did} vs {fid}")
ok("E5 dN<->fN pairing in GRAPHS table")
exprs_by = {did: exprs for did, fid, vw, exprs in entries}

# ---------- E3a: loader initializes every GRAPHS entry by id ----------
# (this page's loader is generic: document.getElementById(g.id); combined
# with E5's per-div table entries this covers all six divs)
if "document.getElementById(g.id)" not in src:
    fail("E3a loader initializes GRAPHS entries by id")
ok("E3a loader initializes all GRAPHS entries by id (generic loop + E5 table)")


def latex_of(did):
    return re.findall(r"\{latex:'((?:[^'\\]|\\.)*)'", exprs_by[did])


# ---------- E3b d1: four primitives with correct source names/forms ----------
d1 = " ".join(latex_of("d1"))
for frag, why in [
    (r"\\frac{1+\\cos\\left(x\\right)}{\\sin\\left(x\\right)}", "srx=cot(x/2)"),
    (r"\\frac{1-\\cos\\left(x\\right)}{\\sin\\left(x\\right)}", "sxp=tan(x/2)"),
    (r"\\frac{1+\\sin\\left(x\\right)}{\\cos\\left(x\\right)}", "cxp=tan(pi/4+x/2)"),
    (r"\\frac{1-\\sin\\left(x\\right)}{\\cos\\left(x\\right)}", "crx=tan(pi/4-x/2)"),
    (r"\\left\\{0<x<\\frac{\\pi}{2}\\right\\}", "principal-chart domain"),
]:
    if frag not in d1:
        fail("E3b d1 primitives", why)
ok("E3b d1: four primitives with correct source forms, principal chart")
# caption names must match the source convention (the 2026-09-19 fix)
if "srx = cot(x/2), sxp = tan(x/2), cxp = tan(π/4+x/2), crx = tan(π/4−x/2)" not in src:
    fail("E3b d1 caption names")
ok("E3b d1 caption carries corrected source names")

# ---------- E3b d2: parametric UNA curve + right-branch-only dashed hyperbola ----------
d2 = " ".join(latex_of("d2"))
for frag, why in [
    (r"\\frac{4}{\\sin\\left(2t\\right)}", "D2=4/sin2t"),
    (r"\\frac{4\\cos\\left(2t\\right)}{\\sin\\left(2t\\right)}", "K2=4cot2t"),
    (r"y=\\sqrt{x^{2}-16}\\left\\{x>4\\right\\}", "right branch dashed"),
    (r"y=-\\sqrt{x^{2}-16}\\left\\{x>4\\right\\}", "right branch dashed (lower)"),
]:
    if frag not in d2:
        fail("E3b d2 hyperbola", why)
if "x<-4" in d2:
    fail("E3b d2 no left branch", "left-branch dashed hyperbola present")
ok("E3b d2: parametric curve + right-branch-only dashed hyperbola")

# ---------- E3b d3: phasor ----------
d3 = " ".join(latex_of("d3"))
for frag, why in [
    ("x^{2}+y^{2}=1", "unit circle"),
    (r"\\cos\\left(2t\\right)", "Z2 real part"),
    (r"\\sin\\left(2t\\right)", "Z2 imag part"),
]:
    if frag not in d3:
        fail("E3b d3 phasor", why)
ok("E3b d3: unit circle + double-angle phasor")

# ---------- E3b d4: saw shares + ln Omega, principal chart ----------
d4 = " ".join(latex_of("d4"))
for frag, why in [
    (r"y=\\cos^{2}\\left(x\\right)\\left\\{0<x<\\frac{\\pi}{2}\\right\\}", "sawup=lam"),
    (r"y=\\sin^{2}\\left(x\\right)\\left\\{0<x<\\frac{\\pi}{2}\\right\\}", "sawdown=1-lam"),
    (r"y=\\ln\\left(\\frac{1}{\\tan^{2}\\left(x\\right)}\\right)", "ln Omega"),
]:
    if frag not in d4:
        fail("E3b d4 saw", why)
# lineStyle sits outside the latex:'...' match; check against full exprs text
if "lineStyle:'dashed'" not in exprs_by["d4"]:
    fail("E3b d4 saw", "ln Omega not dashed")
ok("E3b d4: saw shares + dashed ln Omega on principal chart")

# ---------- E3b d5: meridian circle, arc, and BOTH sign dots ----------
d5 = latex_of("d5")
d5j = " ".join(d5)
if "x^{2}+y^{2}=1" not in d5j:
    fail("E3b d5 circle", "Bloch circle missing")
if r"\\left(\\sin\\left(t\\right),-\\cos\\left(t\\right)\\right)" not in d5j:
    fail("E3b d5 arc", "parametric arc missing")
# sign dots: (sin t, -cos t) for s=+1 (right), (-sin t, -cos t) for s=-1;
# dots are the point expressions containing \frac (the arc uses plain t)
n_plus = sum(1 for e in d5
             if e.startswith(r"\\left(\\sin") and r"\\frac" in e)
n_minus = sum(1 for e in d5 if r"(-\\sin" in e and r"\\frac" in e)
if n_plus == 0:
    fail("E3b d5 s=+1 dots", "no right-side dots")
if n_minus == 0:
    fail("E3b d5 s=-1 dots", "no left-side dots")
ok(f"E3b d5: meridian + arc + s=+1 dots ({n_plus}) + s=-1 dots ({n_minus})")

# ---------- E3b d6: even-exterior ratio ----------
d6 = " ".join(latex_of("d6"))
if r"\\frac{x^{2}+x^{-2}+6}{4}\\left\\{x>0\\right\\}" not in d6:
    fail("E3b d6 ratio", "Q_M/4r^2 formula missing")
ok("E3b d6: even-exterior ratio on x>0")

# ---------- E4: loader pinned to v1.11 ----------
if "desmos.com/api/v1.11/calculator.js" not in src:
    fail("E4 loader v1.11", "pin missing")
ok("E4 loader pinned to Desmos API v1.11")

# ---------- E6: no empty expression lists; 6 captions ----------
if any(len(latex_of(f"d{i}")) == 0 for i in range(1, 7)):
    fail("E6 nonempty exprs", "empty exprs list")
if len(re.findall(r'<div class="caption">', src)) != 6:
    fail("E6 six captions", "")
ok("E6 six nonempty expression lists, six captions")

print(f"\nAll {len(passed)} embed checks passed.")
