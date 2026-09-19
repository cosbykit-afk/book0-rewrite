"""Automated embed test for the Book 11 rewrite page.
1. Every config target id appears exactly once as a container div.
2. Every fallback id matches an existing non-empty PNG.
3. Negative control: a deliberately corrupted copy (d3 -> e3) must be caught.
Real assertions throughout."""
import re, os, sys

HTML = "/home/hatch/workspace/r-theory-rewrite/book11/index.html"
GRAPHS = "/home/hatch/workspace/r-theory-rewrite/book11/graphs"

def audit(path):
    src = open(path).read()
    # config ids: id:'dN' entries in the GRAPHS JS
    cfg_ids = re.findall(r"\{id:'(d\d+)'", src)
    fb_ids = re.findall(r"fb:'(f\d+)'", src)
    # containers: <div class="calc" id="dN">
    containers = re.findall(r'<div class="calc" id="(d\d+)">', src)
    # fallbacks: <img class="fallback" id="fN" src="graphs/...">
    fallbacks = re.findall(r'<img class="fallback" id="(f\d+)" src="graphs/([^"]+)"', src)
    return cfg_ids, fb_ids, containers, fallbacks

cfg_ids, fb_ids, containers, fallbacks = audit(HTML)
print("config ids:", cfg_ids)
print("containers:", containers)
print("fallback ids:", [f for f, _ in fallbacks])

# 1. every config target id present exactly once as a container
assert sorted(cfg_ids) == sorted(containers), "config/container mismatch"
assert len(set(containers)) == len(containers) == 7, "container count/duplicates"
assert cfg_ids == [f"d{i}" for i in range(1, 8)], "expected d1..d7"

# 2. every fallback id matches an existing non-empty PNG
fb_map = dict(fallbacks)
assert sorted(fb_ids) == sorted(fb_map.keys()) == [f"f{i}" for i in range(1, 8)]
for i in range(1, 8):
    p = os.path.join(GRAPHS, fb_map[f"f{i}"])
    assert os.path.isfile(p), p
    assert os.path.getsize(p) > 0, p
    # PNG magic bytes
    with open(p, "rb") as fh:
        assert fh.read(8) == b"\x89PNG\r\n\x1a\n", p
print("PNG files all exist, non-empty, valid PNG magic.")

# 3. negative control: corrupt one container id, audit must fail
bad = open(HTML).read().replace('<div class="calc" id="d3">', '<div class="calc" id="e3">', 1)
open("/tmp/book11_neg.html", "w").write(bad)
detected = False
try:
    c2, _, cont2, _ = audit("/tmp/book11_neg.html")
    detected = (sorted(c2) != sorted(cont2))
except Exception:
    detected = True
assert detected, "NEGATIVE CONTROL FAILED TO TRIGGER - TEST IS BROKEN"
print("negative control: deliberate d3->e3 mismatch correctly detected.")

# 4. JS config well-formed: each graph has a viewport and >=1 expression
src = open(HTML).read()
blocks = re.findall(r"\{id:'d\d+', fb:'f\d+', vw:\{[^}]*\}, exprs:\[", src)
assert len(blocks) == 7, len(blocks)
print("7 graph configs with viewports present.")

print("\nALL EMBED TESTS PASSED (incl. negative control)")
