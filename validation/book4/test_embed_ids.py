#!/usr/bin/env python3
"""Embed-ID consistency test for book4/index.html.

Asserts:
 1. Every config id in the GRAPHS JS array has a matching container element id.
 2. Every config fb id has a matching fallback element id.
 3. Every fallback <img> has a src pointing at a PNG that exists and is non-empty.
 4. No duplicate id attributes anywhere in the document.
Exits nonzero on ANY failure.
"""
import os, re, sys

HTML = "/home/hatch/workspace/r-theory-rewrite/book4/index.html"
GRAPH_DIR = "/home/hatch/workspace/r-theory-rewrite/book4/graphs"

def fail(msg):
    print("FAIL:", msg)
    sys.exit(1)

with open(HTML, encoding="utf-8") as f:
    html = f.read()

# duplicate ids
ids = re.findall(r'id="([^"]+)"', html)
dupes = sorted({i for i in ids if ids.count(i) > 1})
if dupes:
    fail(f"duplicate id attributes: {dupes}")
print(f"OK: {len(ids)} id attributes, no duplicates.")

# config ids
cfg_ids = re.findall(r"\{id:'([^']+)'", html)
fb_ids = re.findall(r"fb:'([^']+)'", html)
if len(cfg_ids) != 7 or len(fb_ids) != 7:
    fail(f"expected 7 graph configs and 7 fb refs, got {len(cfg_ids)}/{len(fb_ids)}")
print("OK: 7 graph configs parsed:", cfg_ids)

idset = set(ids)
for gid in cfg_ids:
    if gid not in idset:
        fail(f"config id '{gid}' has no matching container element")
    # container must be a div.graph
    m = re.search(r'<div class="graph" id="' + re.escape(gid) + r'"', html)
    if not m:
        fail(f"container '{gid}' is not <div class=\"graph\" id=\"{gid}\">")
for fb in fb_ids:
    if fb not in idset:
        fail(f"fallback id '{fb}' has no matching element")
    m = re.search(r'<img class="fallback" id="' + re.escape(fb) + r'" src="([^"]+)"', html)
    if not m:
        fail(f"fallback '{fb}' is not <img class=\"fallback\" id=\"{fb}\" src=...>")
    src = m.group(1)
    p = os.path.normpath(os.path.join(os.path.dirname(HTML), src))
    if not os.path.isfile(p):
        fail(f"fallback PNG missing: {src} -> {p}")
    if os.path.getsize(p) == 0:
        fail(f"fallback PNG empty: {p}")
    print(f"OK: {gid if False else fb} -> {src} ({os.path.getsize(p)} bytes)")

# cross-check: every .graph div and every .fallback img is referenced by config
graph_divs = re.findall(r'<div class="graph" id="([^"]+)"', html)
fallback_imgs = re.findall(r'<img class="fallback" id="([^"]+)"', html)
if set(graph_divs) != set(cfg_ids):
    fail(f".graph divs {graph_divs} != config ids {cfg_ids}")
if set(fallback_imgs) != set(fb_ids):
    fail(f".fallback imgs {fallback_imgs} != config fb ids {fb_ids}")
print("OK: containers and fallbacks exactly match GRAPHS config (no stale/extra ids).")

# Desmos API script tag present
if "desmos.com/api" not in html:
    fail("Desmos API script tag missing")
print("OK: Desmos API script tag present.")
print("ALL EMBED-ID TESTS PASSED.")
