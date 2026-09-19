#!/usr/bin/env python3
"""Static consistency test for book19/index.html Desmos embeds.

Asserts:
  1. Every JS config id (id:'dN') has a matching container element id="dN".
  2. Every JS fallback id (fb:'fN') has a matching element id="fN".
  3. Every fallback <img> src PNG exists under book19/ and is non-empty.
  4. No duplicate id="..." attributes in the HTML.
  5. The Desmos API script tag is present.
  6. Each graph's latex contains the formula its caption claims
     (E3, book0/book1 style).

Exits nonzero on ANY failure.
"""
import os
import re
import sys

HTML = os.path.expanduser("~/workspace/r-theory-rewrite/book19/index.html")
BASE = os.path.dirname(HTML)

failures = []

def fail(msg):
    failures.append(msg)
    print(f"FAIL: {msg}")

with open(HTML, encoding="utf-8") as f:
    html = f.read()

# --- 5. Desmos API script tag present
if "desmos.com/api/v1.11/calculator.js" not in html:
    fail("Desmos API script tag (v1.11) missing")
else:
    print("OK: Desmos API script tag present")

# --- extract JS config ids
cfg_ids = re.findall(r"\{id:'(d\d+)'", html)
fb_ids = re.findall(r"fb:'(f\d+)'", html)
if not cfg_ids:
    fail("no config ids found in GRAPHS")
print(f"config ids: {cfg_ids}")
print(f"fallback ids: {fb_ids}")

# --- 4. duplicate id attributes
all_ids = re.findall(r'id="([^"]+)"', html)
dupes = sorted({i for i in all_ids if all_ids.count(i) > 1})
if dupes:
    fail(f"duplicate id attributes: {dupes}")
else:
    print(f"OK: {len(all_ids)} id attributes, no duplicates")

idset = set(all_ids)

# --- 1. container elements exist for every config id
for cid in cfg_ids:
    if cid not in idset:
        fail(f"config id '{cid}' has no matching container element")
    else:
        # container must be a div.graph
        m = re.search(r'<div class="graph" id="%s">' % re.escape(cid), html)
        if not m:
            fail(f"container '{cid}' is not <div class=\"graph\" id=\"...\">")
if not any(f.startswith("config id") for f in failures):
    print(f"OK: all {len(cfg_ids)} config ids have matching <div class=\"graph\"> containers")

# --- 2. fallback elements exist for every fb id
img_src = {}
for fid in fb_ids:
    if fid not in idset:
        fail(f"fallback id '{fid}' has no matching element")
        continue
    m = re.search(r'<img class="fallback" id="%s" src="([^"]+)"' % re.escape(fid), html)
    if not m:
        fail(f"fallback '{fid}' is not <img class=\"fallback\" id=... src=...>")
    else:
        img_src[fid] = m.group(1)
if not any(f.startswith("fallback") for f in failures):
    print(f"OK: all {len(fb_ids)} fallback ids have matching <img class=\"fallback\"> elements")

# --- 3. fallback PNGs exist and are non-empty
for fid, src in img_src.items():
    p = os.path.normpath(os.path.join(BASE, src))
    if not os.path.isfile(p):
        fail(f"fallback '{fid}' src '{src}' does not exist at {p}")
    elif os.path.getsize(p) == 0:
        fail(f"fallback '{fid}' src '{src}' is empty")
if img_src and not any("src" in f for f in failures):
    print(f"OK: all {len(img_src)} fallback PNGs exist and are non-empty")

# --- cross-check: config ids and fallback ids pair up 1:1
pairs = re.findall(r"\{id:'(d\d+)', fb:'(f\d+)'", html)
if len(pairs) != len(cfg_ids) or len(pairs) != len(fb_ids):
    fail(f"id/fb pairing mismatch: {len(pairs)} pairs vs {len(cfg_ids)} ids vs {len(fb_ids)} fbs")
else:
    print(f"OK: {len(pairs)} id/fb pairs aligned: {pairs}")

if failures:
    print(f"\n{len(failures)} FAILURE(S)")
    sys.exit(1)

# --- 6. latex formula fragments per graph (must match the caption claims)
def latex_of(d):
    m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                  html, re.S)
    if not m:
        fail(f"no GRAPHS block for {d}")
        return ""
    return m.group(1)

L = {d: latex_of(d) for d, _ in pairs}
# Note: the HTML holds JS strings, so every latex backslash appears doubled.
checks = [
    # d1: y = x^4 curve + the three tension points (caption: green (sqrt2)^4=4,
    # red (sqrt2)^8=16, blue V_E^4=638.78)
    ("d1", r"y=x^{4}\\left\\{1\\le x\\le 5.6\\right\\}", "y=x^4 curve"),
    ("d1", r"(\\sqrt{2},4)", "green point (sqrt2,4)"),
    ("d1", r"(2,16)", "red point (2,16)"),
    ("d1", r"\\sqrt{4+2\\sqrt{2}}+1+\\sqrt{2}", "blue point x = V_E form"),
    ("d1", r"(√2)⁴=4 — propagator (CP)", "green label"),
    ("d1", r"(√2)⁸=16 — line-3542's value, IC-18 as 'propagator'", "red label"),
    ("d1", r"V_E⁴=638.78 (NC) — value right; 'factors out of S_F' is MA",
     "blue label"),
    # d2: empty baseline + five OPEN gates (caption: black line Δ_op = ∅,
    # red points S_F, N_1820, ζ_parent, η_-4, c_ord/K_parent — each OPEN)
    ("d2", r"y=0\\left\\{0\\le x\\le 10\\right\\}", "baseline y=0"),
    ("d2", r"(5,0)", "baseline point"),
    ("d2", r"(1,1)", "S_F gate"),
    ("d2", r"(3,1)", "N_1820 gate"),
    ("d2", r"(5,1)", "zeta_parent gate"),
    ("d2", r"(7,1)", "eta_-4 gate"),
    ("d2", r"(9,1)", "c_ord/K_parent gate"),
    ("d2", r"established Δ_op = ∅", "baseline label"),
    ("d2", r"S_F OPEN", "S_F label"),
    ("d2", r"N_1820 OPEN", "N_1820 label"),
    ("d2", r"ζ_parent OPEN", "zeta_parent label"),
    ("d2", r"η_-4 OPEN", "eta_-4 label"),
    ("d2", r"c_ord/K_parent OPEN", "c_ord/K_parent label"),
]
for d, frag, what in checks:
    if frag not in L[d]:
        fail(f"{d}: missing latex for {what}")
if not any("missing latex" in f for f in failures):
    print(f"OK: all {len(checks)} latex formula fragments present and match captions")

# d1 must carry exactly the curve + 3 points the caption describes
assert L["d1"].count("latex:") == 4, "d1 needs 4 exprs (curve + 3 points)"
print("OK: d1 has all 4 expressions (y=x^4 + 3 tension points)")
# d2 must carry the baseline + baseline point + 5 gates
assert L["d2"].count("latex:") == 7, "d2 needs 7 exprs (baseline + point + 5 gates)"
print("OK: d2 has all 7 expressions (baseline + point + 5 OPEN gates)")

if failures:
    print(f"\n{len(failures)} FAILURE(S)")
    sys.exit(1)
print("\nAll embed consistency checks passed.")
