#!/usr/bin/env python3
"""Book 6 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1 every <div class="graph" id="dN"> has a GRAPHS entry with matching fb id
 E2 every <img class="fallback" id="fN" src="graphs/..."> file exists, non-empty
 E3 each graph's latex contains the formula its caption/fallback claims
 E4 Desmos API loader present
 E5 ID consistency (subsumes the former test_ids.py, removed 2026-09-19):
    no duplicate id attributes; every dN/fN element id is referenced by
    exactly one GRAPHS config; 7 figures total
"""
import os
import re

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book6/index.html")
html = open(PAGE).read()

# E1: graph divs <-> GRAPHS entries <-> fallback imgs (book6 uses class="graph")
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
print("OK [E1] 7 graph divs <-> GRAPHS entries <-> fallback imgs linked")

# E2: fallback files exist and are non-empty
for fid, src in imgs:
    p = os.path.join(REPO, "book6", src)
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
    # d1: block split (caption: E-block O(2) lower left, V-block O(3) upper
    # right, off-diagonal "no primitive maps"; Aut_blk = O(2)xO(3))
    ("d1", r"y=2\\left\\{0\\le x\\le5\\right\\}", "blue y=2 block boundary"),
    ("d1", r"x=2\\left\\{0\\le y\\le5\\right\\}", "blue x=2 block boundary"),
    ("d1", r"E: O(2)", "E-block label"),
    ("d1", r"V: O(3)", "V-block label"),
    ("d1", r"no primitive maps", "off-diagonal labels"),
    # d2: bivector sectors (caption: 1 + 6 + 3 = 10)
    ("d2", r"x=0\\left\\{0\\le y\\le1\\right\\}", "L^2E sector height 1"),
    ("d2", r"x=1\\left\\{0\\le y\\le6\\right\\}", "E cross V sector height 6"),
    ("d2", r"x=2\\left\\{0\\le y\\le3\\right\\}", "L^2V sector height 3"),
    ("d2", r"L^2E: 1", "sector label 1"),
    ("d2", r"E cross V: 6", "sector label 6"),
    ("d2", r"L^2V: 3", "sector label 3"),
    # d3: CHI weights (caption: w_U = cos^2 chi, w_U# = sin^2 chi)
    ("d3", r"y=\\left(\\cos\\left(x\\right)\\right)^{2}", "w_U = cos^2"),
    ("d3", r"y=\\left(\\sin\\left(x\\right)\\right)^{2}", "w_U# = sin^2"),
    ("d3", r"y=\\frac{1}{2}", "dashed 1/2 line"),
    ("d3", r"chi=0: one-copy", "chi=0 label"),
    ("d3", r"chi=pi/4: equal", "chi=pi/4 label"),
    ("d3", r"full transfer", "chi=pi/2 label"),
    # d4: traceless line (caption: 2a+3b = 0, normalization (1/2,-1/3))
    ("d4", r"2x+3y=0", "traceless line"),
    ("d4", r"\\left(\\frac{1}{2},-\\frac{1}{3}\\right)", "(1/2,-1/3) point"),
    ("d4", r"(1/2, -1/3)", "normalization label"),
    # d5: balance (caption: y=2x vs y=x(x-1)/2, meet at n=5 dim 10)
    ("d5", r"y=2x", "2n curve"),
    ("d5", r"y=\\frac{x\\left(x-1\\right)}{2}", "n(n-1)/2 curve"),
    ("d5", r"\\left(5,10\\right)", "n=5 point"),
    ("d5", r"n=5: dim 10", "n=5 label"),
    # d6: exterior pattern (caption: 1,5,10,10,5,1)
    ("d6", r"x=0\\left\\{0\\le y\\le1\\right\\}", "grade-0 bar height 1"),
    ("d6", r"x=2\\left\\{0\\le y\\le10\\right\\}", "grade-2 bar height 10"),
    ("d6", r"x=4\\left\\{0\\le y\\le5\\right\\}", "grade-4 bar height 5"),
    # d7: regular 2-simplex (caption: centered vertices, |v_A|^2=2/3)
    ("d7", r"\\frac{1}{\\sqrt{2}}-t\\frac{2}{\\sqrt{2}}", "top edge"),
    ("d7", r"-\\frac{1}{\\sqrt{2}}+t\\frac{1}{\\sqrt{2}}", "left edge"),
    ("d7", r"t\\frac{1}{\\sqrt{2}},-\\frac{2}{\\sqrt{6}}", "right edge"),
    ("d7", r"v1", "v1 label"),
    ("d7", r"v2", "v2 label"),
    ("d7", r"v3", "v3 label"),
]
for d, frag, what in checks:
    assert frag in L[d], f"{d}: missing latex for {what}"
print(f"OK [E3] all {len(checks)} latex formula fragments present and match captions")

# expression counts per graph (caption-claimed content is all present)
exp_counts = {"d1": 16, "d2": 6, "d3": 8, "d4": 2, "d5": 17, "d6": 12, "d7": 7}
for d, n in exp_counts.items():
    got = L[d].count("latex:")
    assert got == n, f"{d}: {got} exprs, expected {n}"
print("OK [E3b] expression counts match (16/6/8/2/17/12/7)")

# E4: Desmos loader (book6 pins v1.11 with an apiKey, like book1)
assert "https://www.desmos.com/api/v1.11/calculator.js" in html
print("OK [E4] Desmos API loader present (v1.11)")

# E5: ID consistency (from test_ids.py)
ids = re.findall(r'id="([^"]+)"', html)
seen, dupes = set(), set()
for i in ids:
    if i in seen:
        dupes.add(i)
    seen.add(i)
assert not dupes, f"duplicate id attributes: {sorted(dupes)}"
cfg_ids = [c[0] for c in entries]
cfg_fbs = [c[1] for c in entries]
assert len(set(cfg_ids)) == len(cfg_ids), f"duplicate config ids: {cfg_ids}"
assert len(set(cfg_fbs)) == len(cfg_fbs), f"duplicate config fb ids: {cfg_fbs}"
for cid in cfg_ids:
    assert re.search(rf'<div[^>]*id="{cid}"[^>]*>', html), \
        f"config id '{cid}' container is not a <div>"
for fb in cfg_fbs:
    assert re.search(rf'<img[^>]*id="{fb}"[^>]*>', html), \
        f"fallback id '{fb}' has no matching <img>"
for i in sorted(seen):
    if re.fullmatch(r"[df]\d+", i) and i not in cfg_ids and i not in cfg_fbs:
        raise AssertionError(f"element id '{i}' not referenced by any config")
assert len(entries) == 7, f"expected 7 figure configs, found {len(entries)}"
print("OK [E5] ID consistency: 7 configs, 7 containers, 7 fallbacks, no dupes, no orphans")

print("\nAll embed consistency checks passed.")
