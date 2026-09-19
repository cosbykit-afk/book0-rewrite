#!/usr/bin/env python3
"""ID-match test for the Book 10 rewrite page.

Checks:
  1. Every GRAPHS config target id appears EXACTLY ONCE as a <div class="calc" id="...">.
  2. Every config fb id appears EXACTLY ONCE as an <img class="fallback" id="...">.
  3. Every fallback img src points to an existing, non-empty PNG.
  4. No duplicate ids anywhere in the document.
Returns exit 0 iff all pass, nonzero otherwise (prints failures).

Negative control: run with --negativize to deliberately corrupt one id in a temp
copy and show the test catches it.
"""
import re, sys, os, tempfile, shutil

HTML = "/home/hatch/workspace/r-theory-rewrite/book10/index.html"
GRAPHS_DIR = "/home/hatch/workspace/r-theory-rewrite/book10/graphs"

def run_test(html_path):
    errs = []
    html = open(html_path).read()
    cfg_ids = re.findall(r"\{id:'(d\d+)'", html)
    fb_ids  = re.findall(r"fb:'(f\d+)'", html)
    if len(cfg_ids) != len(fb_ids):
        errs.append(f"config/fb count mismatch: {len(cfg_ids)} ids vs {len(fb_ids)} fbs")
    for did, fid in zip(cfg_ids, fb_ids):
        n_div = len(re.findall(rf'<div class="calc" id="{did}"', html))
        if n_div != 1:
            errs.append(f"container {did}: found {n_div} <div class=\"calc\"> (want exactly 1)")
        n_img = len(re.findall(rf'<img class="fallback" id="{fid}"', html))
        if n_img != 1:
            errs.append(f"fallback {fid}: found {n_img} <img class=\"fallback\"> (want exactly 1)")
        m = re.search(rf'<img class="fallback" id="{fid}" src="([^"]+)"', html)
        if not m:
            errs.append(f"fallback {fid}: no src attribute found")
            continue
        src = m.group(1)
        base = os.path.basename(src)
        p = os.path.join(GRAPHS_DIR, base)
        if not os.path.isfile(p):
            errs.append(f"fallback {fid}: PNG missing at {p}")
        elif os.path.getsize(p) == 0:
            errs.append(f"fallback {fid}: PNG empty at {p}")
    # duplicate id scan over the whole document
    all_ids = re.findall(r'id="([^"]+)"', html)
    seen = {}
    for i in all_ids:
        seen[i] = seen.get(i, 0) + 1
    dups = {k: v for k, v in seen.items() if v > 1}
    if dups:
        errs.append(f"duplicate ids in document: {dups}")
    return errs, cfg_ids, fb_ids

def main():
    if "--negativize" in sys.argv:
        # NEGATIVE CONTROL: corrupt one CONTAINER id (d3 -> dX) in a temp copy,
        # mimicking the Volume I Book 1 bug (containers vs configs out of sync).
        tmp = tempfile.mkdtemp()
        bad = os.path.join(tmp, "index.html")
        html = open(HTML).read().replace('<div class="calc" id="d3">',
                                         '<div class="calc" id="dX">', 1)
        assert '<div class="calc" id="dX">' in html, "negativize substitution failed"
        open(bad, "w").write(html)
        errs, cfg, fb = run_test(bad)
        shutil.rmtree(tmp)
        print("NEGATIVE CONTROL (container d3 corrupted to dX):")
        if errs:
            print("  test correctly FAILED with:")
            for e in errs:
                print("   -", e)
            return 0  # negative control behaved as intended
        print("  ERROR: test did NOT catch the deliberate mismatch!")
        return 1
    errs, cfg_ids, fb_ids = run_test(HTML)
    print(f"configs: {cfg_ids}")
    print(f"fallbacks: {fb_ids}")
    if errs:
        print("FAIL:")
        for e in errs:
            print(" -", e)
        return 1
    print("PASS: every config id has exactly one container, every fallback id matches "
          "an existing non-empty PNG, no duplicate ids.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
