#!/usr/bin/env python3
"""Book 5 embed consistency: Desmos latex vs fallback PNGs vs captions.

Subsumes the earlier test_ids.py (ID-consistency checks are folded in as
E5 below); test_ids.py has been removed.

Checks (all must pass, exit 0):
 E1 every <div class="graph" id="dN"> has a GRAPHS entry with matching fb id
 E2 every <img class="fallback" id="fN" src="graphs/..."> file exists, non-empty
 E3 each graph's latex contains the formula its caption/fallback claims
 E4 Desmos API loader present
 E5 ID consistency: no duplicate id attributes; every dN/fN element id is
    referenced by exactly one GRAPHS config; 6 figures total
"""
import os
import re

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book5/index.html")
html = open(PAGE).read()

# E1: graph divs <-> GRAPHS entries <-> fallback imgs (book5 uses class="graph")
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
    p = os.path.join(REPO, "book5", src)
    assert os.path.isfile(p), f"missing {p}"
    assert os.path.getsize(p) > 0, f"empty {p}"
print("OK [E2] all 6 fallback PNGs exist and are non-empty")

# E3: latex formula fragments per graph (must match the caption-claimed formulas)
def latex_of(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  html, re.S)
    assert m, f"no GRAPHS block for {d}"
    return m.group(1)

L = {d: latex_of(d) for d, _ in entries}
# Note: the HTML holds JS strings, so every latex backslash appears doubled.
checks = [
    # d1: E rank-2 / V rank-3 disjoint blocks, no E-V identification (Fig 1)
    ("d1", "E rank 2", "E rank-2 block label"),
    ("d1", "V rank 3", "V rank-3 block label"),
    ("d1", "no E-V identification", "crossed-out identification label"),
    # d2: U and U-sharp with block pairing iota; off-diagonals not active (Fig 2)
    ("d2", "U rank 5", "U block label"),
    ("d2", "U-sharp rank 5", "U-sharp block label"),
    ("d2", "iota block pairing", "pairing arrow label"),
    ("d2", "off-diagonal: not active", "noncoupling label"),
    ("d2", "I(u,v)=(-iota^-1 v, iota u), I^2=-1", "complex-structure label"),
    # d3: rank number line 5 / 10 / 10+2 / 10+4 with 10+2m ladder label (Fig 3)
    ("d3", "U rank 5", "U at 5 label"),
    ("d3", "W rank 10, complex rank 5", "W at 10 label"),
    ("d3", "10+2", "first extension label"),
    ("d3", "10+4", "second extension label"),
    ("d3", "W_ext: dim = 10 + 2m", "ladder formula label"),
    # d4: rival overlap completions k=0,2,4 -> ranks 10,8,6 (Fig 4)
    ("d4", "k=0 -> 10 (Axiom Zero)", "k=0 label"),
    ("d4", "k=2 -> 8", "k=2 label"),
    ("d4", "k=4 -> 6", "k=4 label"),
    # d5: y=2x against y=x(x-1)/2 meeting at (5,10) (Fig 5)
    ("d5", "y=2x", "doubled-n-space curve"),
    ("d5", r"\\frac{x\\left(x-1\\right)}{2}", "bivector-space curve"),
    ("d5", "n=5: both 10", "intersection label"),
    # d6: exterior-algebra bars at heights 1,5,10,10,5,1 (Fig 6)
    ("d6", r"\\left(0,1t\\right)", "Lambda^0 bar height 1"),
    ("d6", r"\\left(1,5t\\right)", "Lambda^1 bar height 5"),
    ("d6", r"\\left(2,10t\\right)", "Lambda^2 bar height 10"),
    ("d6", r"\\left(3,10t\\right)", "Lambda^3 bar height 10"),
    ("d6", r"\\left(4,5t\\right)", "Lambda^4 bar height 5"),
    ("d6", r"\\left(5,1t\\right)", "Lambda^5 bar height 1"),
    ("d6", "Lambda^0: 1", "Lambda^0 label"),
    ("d6", "Lambda^2: 10", "Lambda^2 label"),
    ("d6", "Lambda^5: 1", "Lambda^5 label"),
]
for d, frag, what in checks:
    assert frag in L[d], f"{d}: missing latex for {what}"
print(f"OK [E3] all {len(checks)} latex formula fragments present and match captions")

# E4: Desmos loader (book5 pins v1.11 with an apiKey)
assert "https://www.desmos.com/api/v1.11/calculator.js" in html
print("OK [E4] Desmos API v1.11 loader present")

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
for i in sorted(seen):
    if re.fullmatch(r"[df]\d+", i) and i not in cfg_ids and i not in cfg_fbs:
        raise AssertionError(f"element id '{i}' is not referenced by any GRAPHS config")
print("OK [E5] no duplicate ids; every dN/fN element referenced by exactly one config")

print("\nAll embed consistency checks passed.")
