#!/usr/bin/env python3
"""ID-match test for book7/index.html graph embeds.
Checks:
  1. every Desmos config target id exists exactly once as a <div class="calc"> container
  2. every fallback id exists exactly once as an <img class="fallback"> with src
     pointing to an existing, non-empty PNG
  3. no container div is unreferenced by configs (would never initialize)
Negative control: run against a deliberately corrupted copy (config retargeted
to nonexistent 'e4') and confirm the test catches it.
"""
import re, os, sys

HTML = "/home/hatch/workspace/r-theory-rewrite/book7/index.html"
GRAPHDIR = "/home/hatch/workspace/r-theory-rewrite/book7/graphs"

def run_test(html_path, label):
    src = open(html_path).read()
    # config ids from GRAPHS js: {id:'dN', fb:'fN', ...}
    configs = re.findall(r"\{id:'(d\d+)'\s*,\s*fb:'(f\d+)'", src)
    containers = re.findall(r'<div class="calc" id="(d\d+)">', src)
    fallbacks = re.findall(r'<img class="fallback" id="(f\d+)" src="([^"]+)"', src)
    ok = True
    out = [f"--- {label} ---"]
    out.append(f"configs={len(configs)} containers={len(containers)} fallbacks={len(fallbacks)}")
    for cid, fb in configs:
        n = containers.count(cid)
        if n != 1:
            ok = False
            out.append(f"FAIL: config target '{cid}' found {n}x as container (want exactly 1)")
    # every container referenced?
    for c in set(containers):
        if c not in [cid for cid, _ in configs]:
            ok = False
            out.append(f"FAIL: container '{c}' has no config targeting it")
    for fb, fsrc in fallbacks:
        if fb not in [f for _, f in configs]:
            ok = False
            out.append(f"FAIL: fallback '{fb}' not referenced by any config")
        p = os.path.join(GRAPHDIR, os.path.basename(fsrc))
        if not os.path.isfile(p):
            ok = False
            out.append(f"FAIL: fallback '{fb}' src missing: {p}")
        elif os.path.getsize(p) == 0:
            ok = False
            out.append(f"FAIL: fallback '{fb}' PNG empty: {p}")
    out.append("RESULT: " + ("PASS" if ok else "FAIL"))
    return ok, "\n".join(out)

def main():
    ok, report = run_test(HTML, "book7/index.html (as shipped)")
    print(report)
    # negative control: corrupt one config id
    bad = "/tmp/book7_negative.html"
    src = open(HTML).read()
    src_bad = src.replace("{id:'d4', fb:'f4'", "{id:'e4', fb:'f4'", 1)
    assert src_bad != src
    open(bad, "w").write(src_bad)
    ok2, report2 = run_test(bad, "negative control (config d4 -> e4)")
    print(report2)
    if ok and not ok2:
        print("NEGATIVE CONTROL BEHAVED AS EXPECTED: mismatch caught")
        return 0
    print("TEST HARNESS PROBLEM")
    return 1

if __name__ == "__main__":
    sys.exit(main())
