#!/usr/bin/env python3
"""Book 3 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1 every <div class="graph" id="dN"> has a GRAPHS entry with matching fb id
     and a matching <img class="fallback" id="fN">
 E2 every fallback <img src="graphs/..."> file exists and is non-empty
 E3 each graph's latex contains the formula its caption/fallback claims
 E4 Desmos API loader present (v1.11, as pinned on the page)

This SUBSUMES validation/book3/test_ids.py (container/fallback linkage,
no-duplicate-ids, PNG existence, loader presence are all re-checked here).

Run: python3 ~/workspace/r-theory-rewrite/validation/book3/test_embeds.py
"""
import os
import re

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book3/index.html")
html = open(PAGE).read()

# E1: graph divs <-> GRAPHS entries <-> fallback imgs
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

# no duplicate id attributes anywhere in the document
ids = re.findall(r'id="([^"]+)"', html)
dupes = {i for i in ids if ids.count(i) > 1}
assert not dupes, f"duplicate id attributes: {sorted(dupes)}"
print(f"OK [E1b] no duplicate id attributes ({len(ids)} ids)")

# E2: fallback files exist and are non-empty
for fid, src in imgs:
    p = os.path.join(REPO, "book3", src)
    assert os.path.isfile(p), f"missing {p}"
    assert os.path.getsize(p) > 0, f"empty {p}"
print("OK [E2] all 7 fallback PNGs exist and are non-empty")

# E3: latex formula fragments per graph (must match gen_graphs.py formulas
# and the caption claims). The HTML holds JS strings, so every latex
# backslash appears doubled.
def latex_of(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  html, re.S)
    assert m, f"no GRAPHS block for {d}"
    return m.group(1)

L = {d: latex_of(d) for d, _ in entries}
checks = [
    # d1: Mobius cophase maps; caption: Q+, Q-, two steps = -1/t (green)
    ("d1", r"\\frac{1+x}{1-x}", "Q+"),
    ("d1", r"\\frac{x-1}{1+x}", "Q-"),
    ("d1", r"-\\frac{1}{x}", "half-turn map -1/t"),
    # d2: four canonical primitives; caption: srx/cxp/crx/sxp dominance
    ("d2", r"\\left|\\frac{1}{\\sin(x)}\\right|+\\frac{\\cos(x)}{\\sin(x)}", "srx"),
    ("d2", r"\\left|\\frac{1}{\\sin(x)}\\right|-\\frac{\\cos(x)}{\\sin(x)}", "sxp"),
    ("d2", r"\\left|\\frac{1}{\\cos(x)}\\right|+\\frac{\\sin(x)}{\\cos(x)}", "cxp"),
    ("d2", r"\\left|\\frac{1}{\\cos(x)}\\right|-\\frac{\\sin(x)}{\\cos(x)}", "crx"),
    # d3: reciprocal transform; caption: f(u), f(-u)=1/f(u), unit line s=1
    ("d3", r"\\sqrt{1+x^{2}}-x", "f(u)"),
    ("d3", r"\\sqrt{1+x^{2}}+x", "f(-u)=1/f(u)"),
    ("d3", r"y=1", "unit threshold"),
    # d4: FlatWave; caption: sgn(sin 2x), eps orbit dots at pi/8 + k pi/2
    ("d4", r"\\operatorname{sign}(\\sin(2x))", "FlatWave"),
    ("d4", r"(\\frac{\\pi}{8},1)", "orbit dot eps"),
    ("d4", r"(\\frac{5\\pi}{8},-1)", "orbit dot -eps"),
    # d5: Rodrigues bridge; caption: rho=tan(th/2), sxp coincides, seam dot
    ("d5", r"\\tan\\left(\\frac{x}{2}\\right)", "rho=tan(x/2)"),
    ("d5", r"\\left|\\frac{1}{\\sin(x)}\\right|-\\frac{\\cos(x)}{\\sin(x)}", "sxp dashed"),
    ("d5", r"(\\frac{\\pi}{2},1)", "seam dot rho=1"),
    # d6: double cover sheets; caption: +-cos(x/2), 4pi return points
    ("d6", r"\\cos\\left(\\frac{x}{2}\\right)", "sheet q0=cos(x/2)"),
    ("d6", r"-\\cos\\left(\\frac{x}{2}\\right)", "sheet -cos(x/2)"),
    ("d6", r"(2\\pi,-1)", "deck point -q"),
    ("d6", r"(4\\pi,1)", "4pi return point q"),
    # d7: comparison; caption: sgn(t(1-t^2))+1.2 vs sgn(t)-1.2 offsets
    ("d7", r"\\operatorname{sign}(x(1-x^{2}))+1.2", "FlatWave pullback"),
    ("d7", r"\\operatorname{sign}(x)-1.2", "tautological pullback"),
]
for d, frag, what in checks:
    assert frag in L[d], f"{d}: missing latex for {what}"
print(f"OK [E3] all {len(checks)} latex formula fragments present and match captions")

# expression counts: d4 and d6 carry marker points as well as curves
assert len(re.findall(r"\{latex:'", L["d4"])) == 5, "d4 needs 5 exprs (curve + 4 dots)"
assert len(re.findall(r"\{latex:'", L["d6"])) == 5, "d6 needs 5 exprs (2 sheets + 3 dots)"
print("OK [E3b] d4/d6 expression counts correct (curves + marker points)")

# every config expression has a color (avoids invisible traces)
n_exprs = len(re.findall(r"\{latex:'", html))
n_colors = len(re.findall(r"color:'#", html))
assert n_exprs > 0 and n_colors >= n_exprs, \
    f"exprs={n_exprs} colors={n_colors}: every expression needs a color"
print(f"OK [E3c] {n_exprs} Desmos expressions, all colored")

# E4: Desmos loader
assert "https://www.desmos.com/api/v1.11/calculator.js" in html
print("OK [E4] Desmos API loader present (v1.11)")

print("\nAll embed consistency checks passed.")
