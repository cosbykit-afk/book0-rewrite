#!/usr/bin/env python3
"""Book 7 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1 every <div class="calc" id="dN"> has a GRAPHS entry with matching fb id,
    and vice versa (negative control: deliberately corrupted copy must fail)
 E2 every <img class="fallback" id="fN" src="graphs/..."> file exists,
    is non-empty, and has valid PNG dimensions
 E3 each graph's latex contains the formula its caption/fallback claims,
    including the d2 orange-dotted bare-imbalance curve (added 2026-09-19:
    the caption claimed it but the embed lacked it)
 E3b d1/d2 viewports stay on the principal chart (caption requirement:
    left >= 0, right <= pi/2 + margin)
 E4 Desmos API loader present (v1.10)

Subsumes validation/book7/test_graph_ids.py (its ID-match checks and its
negative control are E1 here).
"""
import os
import re
import struct
import sys

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book7/index.html")
GRAPHDIR = os.path.join(REPO, "book7/graphs")
html = open(PAGE).read()

# ---------- E1: calc divs <-> GRAPHS entries <-> fallback imgs ----------
def id_match(src, graphdir, label):
    configs = re.findall(r"\{id:'(d\d+)'\s*,\s*fb:'(f\d+)'", src)
    containers = re.findall(r'<div class="calc" id="(d\d+)">', src)
    fallbacks = re.findall(r'<img class="fallback" id="(f\d+)" src="([^"]+)"', src)
    ok = True
    out = [f"--- {label} ---",
           f"configs={len(configs)} containers={len(containers)} fallbacks={len(fallbacks)}"]
    if not (len(configs) == len(containers) == len(fallbacks) == 7):
        ok = False
        out.append("FAIL: expected 7 configs / 7 containers / 7 fallbacks")
    for cid, fb in configs:
        if containers.count(cid) != 1:
            ok = False
            out.append(f"FAIL: config target '{cid}' found {containers.count(cid)}x as container (want 1)")
    for c in set(containers):
        if c not in [cid for cid, _ in configs]:
            ok = False
            out.append(f"FAIL: container '{c}' has no config targeting it")
    for fb, fsrc in fallbacks:
        if fb not in [f for _, f in configs]:
            ok = False
            out.append(f"FAIL: fallback '{fb}' not referenced by any config")
        p = os.path.join(graphdir, os.path.basename(fsrc))
        if not os.path.isfile(p):
            ok = False
            out.append(f"FAIL: fallback '{fb}' src missing: {p}")
        elif os.path.getsize(p) == 0:
            ok = False
            out.append(f"FAIL: fallback '{fb}' PNG empty: {p}")
    # div order <-> entry order <-> img order
    divs = re.findall(r'<div class="calc" id="(d\d+)">', src)
    for d, (eid, fb) in zip(divs, configs):
        if d != eid:
            ok = False
            out.append(f"FAIL: div order {d} != config order {eid}")
    for (eid, fb), (fid, fsrc) in zip(configs, fallbacks):
        if fb != fid:
            ok = False
            out.append(f"FAIL: entry fb {fb} != img id {fid}")
    out.append("RESULT: " + ("PASS" if ok else "FAIL"))
    return ok, "\n".join(out)

ok, report = id_match(html, GRAPHDIR, "book7/index.html (as shipped)")
print(report)
assert ok, "E1 failed on the shipped page"
print("OK [E1] 7 calc divs <-> GRAPHS entries <-> fallback imgs linked")

# negative control: corrupt one config id; the same check must fail
bad = "/tmp/book7_negative.html"
src_bad = html.replace("{id:'d4', fb:'f4'", "{id:'e4', fb:'f4'", 1)
assert src_bad != html, "negative-control corruption did not apply"
open(bad, "w").write(src_bad)
ok2, report2 = id_match(open(bad).read(), GRAPHDIR,
                        "negative control (config d4 -> e4)")
print(report2)
assert not ok2, "E1 negative control did NOT fail: test harness is blind"
print("OK [E1b] negative control correctly fails (Book 1-class mismatch caught)")

# ---------- E2: fallback PNGs exist, non-empty, valid dimensions ----------
def png_size(path):
    with open(path, "rb") as f:
        sig = f.read(8)
        assert sig == b"\x89PNG\r\n\x1a\n", f"{path}: not a PNG"
        while True:
            raw = f.read(8)
            assert len(raw) == 8, f"{path}: truncated"
            ln, typ = struct.unpack(">I4s", raw)
            data = f.read(ln + 4)
            if typ == b"IHDR":
                w, h = struct.unpack(">II", data[:8])
                return w, h
            if typ == b"IEND":
                raise AssertionError(f"{path}: no IHDR found")

imgs = re.findall(r'<img class="fallback" id="(f\d+)" src="(graphs/[^"]+)"', html)
for fid, src in imgs:
    p = os.path.join(REPO, "book7", src)
    assert os.path.isfile(p), f"missing {p}"
    assert os.path.getsize(p) > 0, f"empty {p}"
    w, h = png_size(p)
    assert w > 0 and h > 0, f"{p}: bad dimensions {w}x{h}"
    print(f"  {fid}: {src} {w}x{h}")
print("OK [E2] all 7 fallback PNGs exist, non-empty, valid dimensions")

# ---------- E3: latex formula fragments per graph ----------
def latex_of(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  html, re.S)
    assert m, f"no GRAPHS block for {d}"
    return m.group(1)

entries = re.findall(r"\{id:'(d\d+)', fb:'(f\d+)'", html)
L = {d: latex_of(d) for d, _ in entries}
# Note: the HTML holds JS strings, so every latex backslash appears doubled.
checks = [
    # d1: saw balance product (caption: lam green, 1-lam red, |H| orange, H blue dashed)
    ("d1", r"y=\\frac{1+\\sin(x)-\\cos(x)}{2}', color:'#2ca02c'", "lam green"),
    ("d1", r"y=1-\\frac{1+\\sin(x)-\\cos(x)}{2}', color:'#d62728'", "1-lam red"),
    ("d1", r"\\left(\\frac{1+\\sin(x)-\\cos(x)}{2}\\right)\\left(1-\\frac{1+\\sin(x)-\\cos(x)}{2}\\right)', color:'#ff7f0e'", "|H|=lam(1-lam) orange"),
    ("d1", r"y=\\frac{\\sin(2x)}{4}', color:'#1f77b4', lineStyle:'dashed'", "H=sin(2x)/4 blue dashed"),
    # d2: companion cosine (caption: cos2x blue, imbalance x envelope orange dashed,
    # bare imbalance orange dotted, envelope green dashed)
    ("d2", r"L(x)=\\frac{1+\\sin(x)-\\cos(x)}{2}', color:'#999999'", "L(x) helper"),
    ("d2", r"y=\\cos(2x)', color:'#1f77b4'", "cos(2x) blue"),
    ("d2", r"\\left(1-2L(x)\\right)\\sqrt{1+4L(x)\\left(1-L(x)\\right)}', color:'#ff7f0e', lineStyle:'dashed'", "imbalance x envelope orange dashed"),
    ("d2", r"y=1-2L(x)', color:'#ff7f0e', lineStyle:'dotted'", "bare imbalance orange dotted"),
    ("d2", r"y=\\sqrt{1+4L(x)\\left(1-L(x)\\right)}', color:'#2ca02c', lineStyle:'dashed'", "envelope + green dashed"),
    ("d2", r"y=-\\sqrt{1+4L(x)\\left(1-L(x)\\right)}', color:'#2ca02c', lineStyle:'dashed'", "envelope - green dashed"),
    # d3: carrier phasor
    ("d3", r"\\left(\\cos(2t),\\sin(2t)\\right)', color:'#1f77b4'", "phasor unit circle blue"),
    # d4: transfer-circle squaring map
    ("d4", r"A(t)=\\frac{\\left|\\sin(t)\\right|+\\left|\\cos(t)\\right|}{\\sqrt{2}}", "a(t) helper"),
    ("d4", r"B(t)=\\frac{\\operatorname{sign}(\\sin(t))\\cos(t)-\\operatorname{sign}(\\cos(t))\\sin(t)}{\\sqrt{2}}", "b(t) helper"),
    ("d4", r"\\left(A(t),B(t)\\right)', color:'#1f77b4'", "zeta blue"),
    ("d4", r"\\left(\\sin(2t),\\cos(2t)\\right)', color:'#ff7f0e'", "quadratic image orange"),
    # d5: primitive decomposition
    ("d5", r"r(x)=\\left|\\frac{1}{\\sin(x)}\\right|+\\frac{\\cos(x)}{\\sin(x)}", "r=srx helper"),
    ("d5", r"c(x)=\\left|\\frac{1}{\\cos(x)}\\right|+\\frac{\\sin(x)}{\\cos(x)}", "c=cxp helper"),
    ("d5", r"y=\\frac{1}{r(x)-\\frac{1}{c(x)}+c(x)-\\frac{1}{r(x)}}', color:'#1f77b4'", "P=1/(urx+uxp) blue"),
    ("d5", r"y=\\frac{\\sin(2x)}{4}', color:'#1f77b4', lineStyle:'dashed'", "sin(2x)/4 blue dashed"),
    ("d5", r"y=2\\left(\\frac{1}{\\left(c(x)+\\frac{1}{c(x)}\\right)^{2}}-\\frac{1}{\\left(r(x)+\\frac{1}{r(x)}\\right)^{2}}\\right)', color:'#2ca02c'", "V green"),
    ("d5", r"y=\\frac{\\cos(2x)}{2}', color:'#2ca02c', lineStyle:'dashed'", "cos(2x)/2 green dashed"),
    # d6: carrier flow + conserved ellipse
    ("d6", r"4x^{2}+y^{2}=\\frac{1}{4}', color:'#1f77b4'", "ellipse blue"),
    ("d6", r"\\left(\\frac{\\sin(2t)}{4},\\frac{\\cos(2t)}{2}\\right)', color:'#d62728'", "orbit red"),
    # d7: hyperbolic parent
    ("d7", r"x^{2}-y^{2}=16', color:'#1f77b4'", "hyperbola blue"),
    ("d7", r"y=x', color:'#999999', lineStyle:'dashed'", "asymptote +"),
    ("d7", r"y=-x', color:'#999999', lineStyle:'dashed'", "asymptote -"),
]
for d, frag, what in checks:
    assert frag in L[d], f"E3 {d}: missing latex for {what}"
print(f"OK [E3] all {len(checks)} latex formula fragments present and match captions/fallbacks")

# ---------- E3b: d1/d2 viewports stay on the principal chart ----------
for d in ("d1", "d2"):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{left:([^,]+), right:([^,]+),", html)
    assert m, f"no viewport for {d}"
    left, right = float(m.group(1)), float(m.group(2))
    assert left >= 0, f"{d}: viewport left={left} < 0 leaves the principal chart"
    assert right <= 1.58, f"{d}: viewport right={right} > pi/2 leaves the principal chart"
print("OK [E3b] d1/d2 viewports confined to the principal chart (captions hold)")

# ---------- E4: Desmos loader ----------
assert "https://www.desmos.com/api/v1.10/calculator.js" in html
print("OK [E4] Desmos API v1.10 loader present")

print("\nAll embed consistency checks passed.")
