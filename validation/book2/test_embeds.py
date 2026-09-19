#!/usr/bin/env python3
"""Static consistency test for book2/index.html Desmos embeds.

Asserts:
  1. Every JS config id (id:'dN') has a matching container element id="dN".
  2. Every JS fallback id (fb:'fN') has a matching element id="fN".
  3. Every fallback <img> src PNG exists under book2/ and is non-empty.
  4. No duplicate id="..." attributes in the HTML.
  5. The Desmos API script tag is present.

Exits nonzero on ANY failure.
"""
import os
import re
import sys

HTML = os.path.expanduser("~/workspace/r-theory-rewrite/book2/index.html")
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
print("\nAll embed consistency checks passed.")
