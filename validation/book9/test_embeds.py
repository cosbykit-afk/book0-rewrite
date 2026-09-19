#!/usr/bin/env python3
"""Book 9 embed consistency: Desmos latex vs fallback PNGs vs captions.

Subsumes the earlier test_ids.py (ID-consistency checks are folded in as
E5 below); test_ids.py has been removed. (test_ids.py's docstring referenced
~/workspace/vol2_book7/test_graph_ids.py, a stale path in another book's old
file; that reference is gone with the subsumed file.)

Checks (all must pass, exit 0):
 E1 every <div class="graph" id="dN"> has a GRAPHS entry with matching fb id
 E2 every <img class="fallback" id="fN" src="graphs/..."> file exists, non-empty
 E3 each graph's latex contains the formula its caption/fallback claims
 E3b fallback alt text matches the formula the caption claims
 E4 Desmos API loader present (book9 pins v1.11 with an apiKey)
 E5 ID consistency: no duplicate id attributes; every dN/fN element id is
    referenced by exactly one GRAPHS config; 4 figures total
"""
import os
import re

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book9/index.html")
html = open(PAGE).read()

# E1: graph divs <-> GRAPHS entries <-> fallback imgs (book9 uses class="graph")
divs = re.findall(r'<div class="graph" id="(d\d+)">', html)
imgs = re.findall(r'<img class="fallback" id="(f\d+)" src="(graphs/[^"]+)"', html)
entries = re.findall(r"\{id:'(d\d+)', fb:'(f\d+)'", html)
assert divs, "no graph divs found"
assert len(divs) == len(imgs) == len(entries) == 4, \
    f"counts: divs={divs} imgs={imgs} entries={entries}"
for d, (eid, fb) in zip(divs, entries):
    assert d == eid, f"div {d} != entry {eid}"
for (eid, fb), (fid, src) in zip(entries, imgs):
    assert fb == fid, f"entry fb {fb} != img {fid}"
print("OK [E1] 4 graph divs <-> GRAPHS entries <-> fallback imgs linked")

# E2: fallback files exist and are non-empty
for fid, src in imgs:
    p = os.path.join(REPO, "book9", src)
    assert os.path.isfile(p), f"missing {p}"
    assert os.path.getsize(p) > 0, f"empty {p}"
print("OK [E2] all 4 fallback PNGs exist and are non-empty")

# E3: latex formula fragments per graph (must match the caption-claimed formulas)
def latex_of(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  html, re.S)
    assert m, f"no GRAPHS block for {d}"
    return m.group(1)

L = {d: latex_of(d) for d, _ in entries}
# Note: the HTML holds JS strings, so every latex backslash appears doubled.
checks = [
    # d1: cxp = e^eta, crx = e^-eta, product line y=1 (Fig 1)
    ("d1", r"e^{x}", "cxp = e^eta"),
    ("d1", r"e^{-x}", "crx = e^-eta"),
    ("d1", r"y=1", "product = 1 dashed"),
    # d2: hyperbola branch x^2-y^2=4 traced by (2cosh(3t-1.5), 2sinh(3t-1.5)) (Fig 2)
    ("d2", r"x^{2}-y^{2}=4", "hyperbola Er^2-Or^2=4"),
    ("d2", r"\\cosh(3t-1.5)", "drawn curve 2cosh(3t-1.5)"),
    ("d2", r"\\sinh(3t-1.5)", "drawn curve 2sinh(3t-1.5)"),
    # d3: defect N^2 = 1-4a/r (a=1), asymptotic y=1, horizon x=4 (Fig 3)
    ("d3", r"1-\\frac{4}{x}", "defect f = 1-4a/r"),
    ("d3", r"y=1", "asymptotic flatness dashed"),
    ("d3", r"x=4", "horizon r=4a dashed"),
    # d4: chart q = (1-N)/(1+N), vacuum line sigma = 0 (Fig 4)
    ("d4", r"\\frac{1-x}{1+x}", "chart q = (1-N)/(1+N)"),
    ("d4", r"y=0", "vacuum line sigma = 0 dashed"),
]
for d, frag, what in checks:
    assert frag in L[d], f"{d}: missing latex for {what}"
print(f"OK [E3] all {len(checks)} latex formula fragments present and match captions")

# E3b: fallback alt text carries the caption-claimed formula
alts = dict(re.findall(r'<img class="fallback" id="(f\d+)" src="[^"]+" alt="([^"]*)"', html))
expected_alt = {
    "f1": ("cxp=e^eta", "crx=e^-eta"),
    "f2": ("Er^2-Or^2=4",),
    "f3": ("f=1-4a/r",),
    "f4": ("q=(1-N)/(1+N)", "sigma=0"),
}
for fid, keys in expected_alt.items():
    assert fid in alts, f"fallback {fid} has no alt text"
    for key in keys:
        assert key in alts[fid], f"{fid}: alt text missing '{key}': {alts[fid]!r}"
print("OK [E3b] all 4 fallback alt texts carry the caption-claimed formulas")

# E4: Desmos loader (book9 pins v1.11 with an apiKey)
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
