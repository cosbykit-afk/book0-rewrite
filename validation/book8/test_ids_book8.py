"""ID-match test for book8/index.html Desmos embeds.

Checks:
  1. Every GRAPHS config id (d1..d8) exists exactly once as a container element.
  2. Every GRAPHS fb id (f1..f8) exists exactly once as an <img> fallback.
  3. Every fallback img src points to an existing non-empty PNG in graphs/.
  4. Every plotted Desmos latex string is non-empty.
  5. NEGATIVE CONTROL: the same checks run against a deliberately corrupted copy
     (config id renamed d9 with no container) must FAIL, proving the test detects
     the Volume I Book 1 class of bug (containers d1-d7 vs configs e1-e7).
"""
import re, os, sys

HTML = "/home/hatch/workspace/r-theory-rewrite/book8/index.html"
GRAPHDIR = "/home/hatch/workspace/r-theory-rewrite/book8/graphs"

def run_checks(html_text, label):
    errors = []
    # extract GRAPHS entries: {id:'dN', fb:'fN', ...}
    configs = re.findall(r"\{id:'(d\d+)'\s*,\s*fb:'(f\d+)'", html_text)
    if not configs:
        errors.append("no GRAPHS configs parsed")
        return errors, configs
    for cid, fb in configs:
        n_cont = len(re.findall(r'id="%s"' % cid, html_text))
        if n_cont != 1:
            errors.append(f"{label}: container id={cid} found {n_cont}x (want exactly 1)")
        n_fb = len(re.findall(r'id="%s"' % fb, html_text))
        if n_fb != 1:
            errors.append(f"{label}: fallback id={fb} found {n_fb}x (want exactly 1)")
    # fallback img srcs exist and are non-empty
    for m in re.finditer(r'<img[^>]*id="(f\d+)"[^>]*src="([^"]+)"', html_text):
        fid, src = m.group(1), m.group(2)
        p = os.path.join(GRAPHDIR, os.path.basename(src))
        if not os.path.isfile(p):
            errors.append(f"{label}: fallback {fid} src {src} -> missing file {p}")
        elif os.path.getsize(p) == 0:
            errors.append(f"{label}: fallback {fid} file {p} is empty")
    # every latex non-empty
    for i, lx in enumerate(re.findall(r"latex:'((?:[^'\\]|\\.)*)'", html_text)):
        if not lx.strip():
            errors.append(f"{label}: empty latex at expr {i}")
    return errors, configs

def main():
    text = open(HTML).read()
    errors, configs = run_checks(text, "REAL")
    print(f"parsed {len(configs)} graph configs: {[c[0] for c in configs]}")
    assert len(configs) == 8, f"expected 8 configs, got {len(configs)}"
    if errors:
        print("REAL PAGE FAILURES:")
        for e in errors: print("  -", e)
        sys.exit(1)
    print("REAL PAGE: all ID-match checks passed (8 containers, 8 fallbacks, 8 PNGs)")

    # ---- negative control: corrupt a copy ----
    bad = text.replace("{id:'d3', fb:'f3'", "{id:'d9', fb:'f3'", 1)  # config with no container
    bad = bad.replace('src="graphs/b8_g4_puregauge.png"', 'src="graphs/NOPE.png"', 1)
    errs2, _ = run_checks(bad, "CORRUPTED")
    if not errs2:
        print("NEGATIVE CONTROL FAILED: corrupted page passed checks (test is blind)")
        sys.exit(2)
    print(f"NEGATIVE CONTROL: corrupted page correctly rejected ({len(errs2)} errors), e.g.:")
    for e in errs2[:3]: print("  -", e)
    print("ALL TESTS PASSED (positive + negative control)")

if __name__ == "__main__":
    main()
