#!/usr/bin/env python3
"""Book 13 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1 every <div class="graph" id="dN"> has a GRAPHS entry with matching fb id,
    in order, linked to its <img class="fallback" id="fN" src="graphs/...">
 E2 every fallback PNG exists and is non-empty
 E3 each graph's latex contains the formula its caption and fallback claim
 E3b d6 carries the dashed λ(T) curve the caption claims
 E4 Desmos API loader present (v1.11, as pinned on the page)
 E5 NEGATIVE CONTROL: the same checks run against a deliberately mutated copy
    (one config id changed to a nonexistent id) must FAIL
"""
import os
import re
import sys

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book13/index.html")
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
print("OK [E1] 7 graph divs <-> GRAPHS entries <-> fallback imgs linked, in order")

# E2: fallback files exist and are non-empty
for fid, src in imgs:
    p = os.path.join(REPO, "book13", src)
    assert os.path.isfile(p), f"missing {p}"
    assert os.path.getsize(p) > 0, f"empty {p}"
print("OK [E2] all 7 fallback PNGs exist and are non-empty")

# E3: latex formula fragments per graph (must match make_figs.py formulas
# and the caption's claimed formula).
def latex_of(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  html, re.S)
    assert m, f"no GRAPHS block for {d}"
    return m.group(1)

L = {d: latex_of(d) for d, _ in entries}
# Note: the HTML holds JS strings, so every latex backslash appears doubled.
checks = [
    ("d1", r"\\frac{1+\\sin\\left(x\\right)-\\cos\\left(x\\right)}{2}", "λ(x)"),
    ("d1", r"\\frac{1-\\sin\\left(x\\right)+\\cos\\left(x\\right)}{2}", "1−λ(x)"),
    ("d1", r"\\frac{\\pi}{2}", "domain restriction"),
    ("d2", r"\\frac{2}{1+\\sin\\left(x\\right)-\\cos\\left(x\\right)}", "urx=1/λ"),
    ("d2", r"\\frac{2}{1-\\sin\\left(x\\right)+\\cos\\left(x\\right)}", "uxp=1/(1−λ)"),
    ("d3", r"x\\ln\\left(x\\right)+\\left(1-x\\right)\\ln\\left(1-x\\right)", "Bernoulli entropy"),
    ("d3", r"x\\left(1-x\\right)", "|H|=λ(1−λ)"),
    ("d4", r"\\ln\\left(1+e^{x}\\right)", "A(v)"),
    ("d4", r"\\frac{e^{x}}{1+e^{x}}", "λ(v)"),
    ("d4", r"\\frac{e^{x}}{\\left(1+e^{x}\\right)^{2}}", "A''(v)"),
    ("d5", r"2\\arctan\\left(e^{\\frac{x}{2}}\\right)", "φ_F(v)"),
    ("d6", r"\\left(\\frac{1}{x}\\right)^{2}\\frac{e^{\\frac{1}{x}}}{\\left(1+e^{\\frac{1}{x}}\\right)^{2}}", "C/kB Schottky"),
    ("d6", r"\\frac{e^{\\frac{1}{x}}}{1+e^{\\frac{1}{x}}}", "λ(T) dashed"),
    ("d7", r"\\sin\\left(x\\right)", "λ(x) substitution"),
    ("d7", r"\\ln\\left(\\frac{1+\\sin", "entropy of λ(x)"),
]
for d, frag, what in checks:
    assert frag in L[d], f"{d}: missing latex for {what}"
print(f"OK [E3] all {len(checks)} latex formula fragments present and match captions/fallbacks")

# E3b: d6 must carry the dashed λ(T) curve the caption claims
assert L["d6"].count("latex:") == 2, "d6 needs exactly 2 exprs"
assert "lineStyle:'dashed'" in L["d6"], "d6 λ(T) must be dashed per caption"
print("OK [E3b] d6 has both curves with λ(T) dashed as captioned")

# E4: Desmos loader (v1.11, pinned on the page)
assert "https://www.desmos.com/api/v1.11/calculator.js" in html
print("OK [E4] Desmos API loader v1.11 present")

# E5: negative control — retarget one config at a nonexistent container; must FAIL
def run_checks(h):
    errors = []
    cfgs = re.findall(r"\{id:'(d\d+)'\s*,\s*fb:'(f\d+)'", h)
    for did, fid in cfgs:
        n_cont = len(re.findall(r'id="%s"' % did, h))
        if n_cont != 1:
            errors.append(f"container id={did}: found {n_cont} (need exactly 1)")
        m = re.search(r'<img[^>]*id="%s"[^>]*>' % fid, h)
        if not m:
            errors.append(f"fallback id={fid}: no <img> found")
            continue
        src = re.search(r'src="([^"]+)"', m.group(0))
        p = os.path.join(REPO, "book13", src.group(1)) if src else None
        if not p or not os.path.isfile(p):
            errors.append(f"fallback id={fid}: PNG missing")
        elif os.path.getsize(p) == 0:
            errors.append(f"fallback id={fid}: PNG empty")
    return errors

errs = run_checks(html)
assert not errs, f"positive checks failed: {errs}"
bad = html.replace("{id:'d4',", "{id:'d9',", 1)
assert bad != html, "mutation did not apply"
berrs = run_checks(bad)
assert berrs, "NEGATIVE CONTROL FAILED: mutated HTML passed checks (test is blind)"
print(f"OK [E5] negative control: mutated config correctly rejected "
      f"({len(berrs)} error(s), e.g. {berrs[0]!r})")

print("\nAll embed consistency checks passed.")
