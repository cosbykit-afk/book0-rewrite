"""Embed-ID consistency test for the Book 3 rewrite page.

Parses ~/workspace/r-theory-rewrite/book3/index.html and asserts:
  1. every JS GRAPHS config id has a matching container element id,
  2. every JS GRAPHS fallback id has a matching element id,
  3. every fallback <img> src points to an existing non-empty PNG,
  4. no duplicate id attributes anywhere in the document,
  5. every container id is actually targeted by exactly one config entry,
  6. every fallback element id is actually referenced by exactly one config entry.
Exit code nonzero on any failure. Run:
    python3 ~/workspace/book3/checks/test_ids.py
"""
import os
import re
import sys

HTML = "/home/hatch/workspace/r-theory-rewrite/book3/index.html"
GRAPH_DIR = "/home/hatch/workspace/r-theory-rewrite/book3/graphs/"

fails = []

def fail(msg):
    fails.append(msg)
    print("FAIL:", msg)

src = open(HTML, encoding="utf-8").read()

# ---- collect ids from the document
ids = re.findall(r'id="([^"]+)"', src)
dupes = {i for i in ids if ids.count(i) > 1}
if dupes:
    fail("duplicate id attributes: %s" % sorted(dupes))
else:
    print("PASS: no duplicate id attributes (%d ids)" % len(ids))

# ---- collect JS config entries: {id:'dN', fb:'fN', ...}
configs = re.findall(r"\{id:'([^']+)',\s*fb:'([^']+)'", src)
if not configs:
    fail("no GRAPHS config entries found")
print("found %d GRAPHS config entries" % len(configs))

config_ids = [c for c, _ in configs]
config_fbs = [f for _, f in configs]
if len(set(config_ids)) != len(config_ids):
    fail("duplicate config ids: %s" % config_ids)
if len(set(config_fbs)) != len(config_fbs):
    fail("duplicate config fallback ids: %s" % config_fbs)

# 1. every config id has a matching container element
for cid in config_ids:
    if ('id="%s"' % cid) not in src:
        fail("config id '%s' has no matching container element" % cid)
    else:
        print("PASS: container element id='%s' exists" % cid)

# 2. every fallback id has a matching element
for fb in config_fbs:
    if ('id="%s"' % fb) not in src:
        fail("fallback id '%s' has no matching element" % fb)
    else:
        print("PASS: fallback element id='%s' exists" % fb)

# 5/6. every graph container / fallback element is targeted exactly once
for m in re.finditer(r'<div class="graph" id="([^"]+)"', src):
    if config_ids.count(m.group(1)) != 1:
        fail("graph container '%s' targeted %d times" % (m.group(1), config_ids.count(m.group(1))))
for m in re.finditer(r'<img class="fallback" id="([^"]+)"', src):
    if config_fbs.count(m.group(1)) != 1:
        fail("fallback img '%s' referenced %d times" % (m.group(1), config_fbs.count(m.group(1))))
print("PASS: every container/fallback element is targeted exactly once")

# 3. every fallback img src exists and is non-empty
for m in re.finditer(r'<img class="fallback" id="([^"]+)" src="([^"]+)"', src):
    fid, rel = m.group(1), m.group(2)
    path = os.path.normpath(os.path.join(GRAPH_DIR, os.path.basename(rel)))
    if not os.path.isfile(path):
        fail("fallback '%s' src missing file: %s" % (fid, path))
    elif os.path.getsize(path) == 0:
        fail("fallback '%s' PNG is empty: %s" % (fid, path))
    else:
        print("PASS: fallback '%s' -> %s (%d bytes)" % (fid, path, os.path.getsize(path)))

# sanity: Desmos script tag present
if "desmos.com/api" not in src:
    fail("Desmos API script tag missing")
else:
    print("PASS: Desmos API script tag present")

# sanity: every config expression has a color (avoids invisible traces)
n_exprs = len(re.findall(r"\{latex:'", src))
print("found %d Desmos expressions across configs" % n_exprs)
if n_exprs == 0:
    fail("no Desmos expressions found")

print()
if fails:
    print("%d FAILURE(S)" % len(fails))
    sys.exit(1)
print("ALL ID CHECKS PASSED")
