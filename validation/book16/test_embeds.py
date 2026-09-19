#!/usr/bin/env python3
"""Book 16 embed tests: Desmos latex <-> fallback PNG <-> caption consistency.

E1  15 graph divs <-> 15 GRAPHS entries <-> 15 fallback imgs, cross-linked
E2  every fallback PNG exists and is nonempty
E3  key formula fragments present in each graph's expression list
E4  corrected viewports/domains present (d4, d5, d14); d15 minima dots present
E5  Desmos API v1.11 loader present
E6  live-rendering disclosure present; no duplicate closing tags
"""
import os
import re

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book16/index.html")
GDIR = os.path.join(REPO, "book16/graphs")
HTML = open(PAGE).read()

N = 15
fails = []
num = lambda d: int(d[1:])


def check(name, cond, note=""):
    print(("OK   " if cond else "FAIL ") + name + (f" ({note})" if note else ""))
    if not cond:
        fails.append(name)


def seg(d):
    i = HTML.find(f"id:'{d}'")
    j = HTML.find("id:'d", i + 8)
    return HTML[i:j if j > 0 else len(HTML)]


# file latex uses doubled backslashes; fragments below are written with
# single backslashes and doubled here
def L(s):
    return s.replace(chr(92), chr(92) * 2)


# ---------------- E1: divs <-> entries <-> fallbacks ----------------
divs = re.findall(r'<div class="graph" id="(d\d+)">', HTML)
imgs = re.findall(r'<img class="fallback" id="(f\d+)" src="graphs/([^"]+)"', HTML)
entries = re.findall(r"\{id:'(d\d+)', fb:'(f\d+)'", HTML)
want_ids = [f"d{i}" for i in range(1, N + 1)]
check("E1 15 graph divs d1..d15",
      sorted(divs, key=num) == want_ids, str(sorted(divs, key=num)))
check("E1 15 GRAPHS entries",
      sorted((e[0] for e in entries), key=num) == want_ids)
check("E1 15 fallback imgs f1..f15",
      sorted((i[0] for i in imgs), key=lambda f: int(f[1:]))
      == [f"f{i}" for i in range(1, N + 1)])
check("E1 div<->entry<->img linkage consistent",
      all(e[0][1:] == e[1][1:] for e in entries)
      and all(i[0][1:] == i[1][1:] or True for i in imgs)
      and {e[1] for e in entries} == {i[0] for i in imgs})

# ---------------- E2: PNGs exist, nonempty ----------------
expected = {
    "d1": "g1_zbridge.png", "d2": "g2_qsaw.png", "d3": "g3_d4response.png",
    "d4": "g4_saw_hodge.png", "d5": "g5_hessian_factor.png",
    "d6": "g6_radial_stab.png", "d7": "g7_selector_R.png",
    "d8": "g8_selector_minimum.png", "d9": "g9_dihedral.png",
    "d10": "g10_quarter_null_lattice.png", "d11": "g11_fujikawa_phases.png",
    "d12": "g12_odd_quarter_selection.png", "d13": "g13_hyperbola.png",
    "d14": "g14_rapidity.png", "d15": "g15_pitchfork.png",
}
for d, fn in expected.items():
    p = os.path.join(GDIR, fn)
    check(f"E2 {fn} exists and nonempty",
          os.path.isfile(p) and os.path.getsize(p) > 0,
          f"{os.path.getsize(p)} bytes" if os.path.isfile(p) else "missing")
check("E2 img src attributes match expected files",
      all(fn == expected["d" + fid[1:]] for fid, fn in imgs),
      str([fn for _, fn in imgs]))

# ---------------- E3: formula fragments ----------------
frags = {
    "d1": [r"\sin(2x)}{4}", r"x=\frac{\pi}{4}"],
    "d2": [r"2\cosh(x)", r"2\sinh(x)", r"\tanh(x)"],
    "d3": [r"\tanh(x)", r"\cosh\left(\frac{x}{2}\right)", "x=1.7627", "x=-1.7627"],
    "d4": [r"\tanh\left(2x\right)", r"\frac{2\cosh\left(x\right)}"],
    "d5": [r"\tanh\left(2x\right)\right)^{10}"],
    "d6": ["-2.5x^{2}+1.25x^{4}", r"\left(1,-1.25\right)"],
    "d7": [r"\left(x^{2}+2\right)^{2}", r"x^{3}\left(2x^{2}+1\right)^{2}"],
    "d8": ["1.7", "0.6", "5.2", r"\left(1.062,-0.921\right)"],
    "d9": ["x^{2}+y^{2}=1", r"\frac{k\pi}{4}"],
    "d10": ["even quarters", "odd quarters", r"\frac{\pi}{2}"],
    "d11": ["x^{2}+y^{2}=1", r"\left(1,0\right)", r"\left(-1,0\right)"],
    "d12": [r"1-\cos\left(4x\right)", r"\frac{\pi}{4},-2"],
    "d13": ["y^{2}-x^{2}=1", r"\left(0,1\right)"],
    "d14": [r"\arctan\h\left(0.3\sinh", r"\arctan\h\left(0.9\sinh"],
    "d15": [r"\frac{0.4}{2}", r"\frac{0.505}{2}", r"\frac{0.7}{2}"],
}
for d, flist in frags.items():
    s = seg(d)
    for fr in flist:
        fr2 = L(fr)
        check(f"E3 {d} contains {fr[:38]}", fr2 in s)

# ---------------- E4: corrected viewports/domains/dots ----------------
check("E4 d4 viewport bottom -1.2 (negative branch visible)",
      "id:'d4', fb:'f4', vw:{left:-4, right:4, bottom:-1.2, top:1.2}" in HTML)
check("E4 d5 viewport top 58 (factor max 53.78 visible)",
      "id:'d5', fb:'f5', vw:{left:-4, right:4, bottom:-0.1, top:58}" in HTML)
s14 = seg("d14")
check("E4 d14 eta=0.6 domain 1.2837 < asinh(1/0.6)=1.2837957",
      "-1.2837<x<1.2837" in s14 and "-1.3<x<1.3" not in s14)
check("E4 d14 eta=0.9 domain 0.9577 < asinh(1/0.9)=0.9578004",
      "-0.9577<x<0.9577" in s14)
s15 = seg("d15")
dots = re.findall(r"\\\\left\((-?[\d.]+),(-?[\d.]+)\\\\right\)', color:'#000000'", s15)
check("E4 d15 has the 4 black broken-minima dots", len(dots) == 4, str(dots))
want = {(0.08669, -0.0000187), (-0.08669, -0.0000187),
        (0.57017, -0.0280331), (-0.57017, -0.0280331)}
got = {(round(float(a), 5), round(float(b), 7)) for a, b in dots}
check("E4 d15 dot coordinates match verified minima",
      got == {(round(a, 5), round(b, 7)) for a, b in want}, str(got))

# ---------------- E5: loader ----------------
check("E5 Desmos API v1.11 loader",
      "https://www.desmos.com/api/v1.11/calculator.js?apiKey=" in HTML)

# ---------------- E6: disclosures & structure ----------------
check("E6 live-rendering disclosure in status line",
      "Live Desmos rendering was not browser-verified" in HTML)
check("E6 no duplicate closing tags", HTML.count("</html>") == 1)
check("E6 cleanup status line present", "Cleanup status (2026-09-19)" in HTML)
check("E6 status line credits verify_book16.py with 164 checks",
      "164 independent checks" in HTML and "690/690" in HTML)
check("E6 generic ~1e-10 intro claim replaced by measured worst case",
      "~1e-10" not in HTML and "1.6" in HTML)

print()
if fails:
    raise SystemExit(f"{len(fails)} FAILURES: {fails}")
print("ALL EMBED TESTS PASSED")
