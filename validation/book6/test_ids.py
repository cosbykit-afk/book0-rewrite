"""ID-consistency test for ~/workspace/r-theory-rewrite/book6/index.html.

Asserts (exit nonzero on ANY failure):
  1. every GRAPHS config id has a matching container element in the HTML
  2. every config fb id has a matching element in the HTML
  3. every fallback img src points to an existing, non-empty PNG
  4. no duplicate id attributes anywhere in the HTML
  5. every container/fallback element id is referenced by exactly one config
  6. GRAPHS config count matches container count (7 figures)
"""
import os, re, sys

HTML = "/home/hatch/workspace/r-theory-rewrite/book6/index.html"
BASE = "/home/hatch/workspace/r-theory-rewrite/book6"
fails = []

def fail(msg):
    fails.append(msg)
    print("FAIL:", msg)

src = open(HTML).read()

# --- collect ids from HTML ---
ids = re.findall(r'id="([^"]+)"', src)
seen, dupes = set(), set()
for i in ids:
    if i in seen:
        dupes.add(i)
    seen.add(i)
if dupes:
    fail(f"duplicate id attributes: {sorted(dupes)}")

# --- collect GRAPHS configs ---
configs = re.findall(r"\{id:'([^']+)', fb:'([^']+)'", src)
if not configs:
    fail("no GRAPHS configs parsed")
print(f"configs parsed: {len(configs)}")

cfg_ids = [c[0] for c in configs]
cfg_fbs = [c[1] for c in configs]
if len(set(cfg_ids)) != len(cfg_ids):
    fail(f"duplicate config ids: {cfg_ids}")
if len(set(cfg_fbs)) != len(cfg_fbs):
    fail(f"duplicate config fb ids: {cfg_fbs}")

# --- 1. every config id has a matching container element ---
for cid in cfg_ids:
    if f'id="{cid}"' not in src:
        fail(f"config id '{cid}' has no matching container element")
    m = re.search(rf'<div[^>]*id="{cid}"[^>]*>', src)
    if not m:
        fail(f"config id '{cid}' container is not a <div>")

# --- 2. every fb id has a matching element ---
for fb in cfg_fbs:
    m = re.search(rf'<img[^>]*id="{fb}"[^>]*>', src)
    if not m:
        fail(f"fallback id '{fb}' has no matching <img> element")

# --- 3. every fallback PNG exists and is non-empty ---
img_srcs = re.findall(r'<img[^>]*id="f\d+"[^>]*src="([^"]+)"', src)
if len(img_srcs) != len(configs):
    fail(f"img src count {len(img_srcs)} != config count {len(configs)}")
for s in img_srcs:
    p = os.path.join(BASE, s)
    if not os.path.isfile(p):
        fail(f"fallback PNG missing: {s}")
    elif os.path.getsize(p) == 0:
        fail(f"fallback PNG empty: {s}")
    else:
        print(f"  png ok: {s} ({os.path.getsize(p)} bytes)")

# --- 5. every dN/fN element id is referenced by a config ---
for i in sorted(seen):
    if re.fullmatch(r"[df]\d+", i) and i not in cfg_ids and i not in cfg_fbs:
        fail(f"element id '{i}' is not referenced by any GRAPHS config")

# --- 6. figure count ---
if len(configs) != 7:
    fail(f"expected 7 figure configs, found {len(configs)}")

if fails:
    print(f"\n{len(fails)} FAILURE(S) — see above")
    sys.exit(1)
print("\nALL ID TESTS PASSED: 7 configs, 7 containers, 7 fallbacks, 7 PNGs, no dupes")
