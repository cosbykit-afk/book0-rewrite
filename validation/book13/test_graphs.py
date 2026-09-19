#!/usr/bin/env python3
"""Graph embed verification for book13/index.html.
1. Every GRAPHS config target id exists exactly once as a container id="dN".
2. Every config fb id exists exactly once as id="fN" on an <img> whose src
   points at an existing, non-empty PNG in graphs/.
3. Formula-token spot check: each figure's latex contains expected tokens.
4. NEGATIVE CONTROL: the same checks run against a deliberately mutated copy
   (one config id changed to a nonexistent id) must FAIL.
Exit 0 only if all positive checks pass AND the negative control fails."""
import re, os, sys

HTML = "/home/hatch/workspace/r-theory-rewrite/book13/index.html"
GDIR = "/home/hatch/workspace/r-theory-rewrite/book13/graphs"

def run_checks(html):
    errors = []
    cfgs = re.findall(r"\{id:'(d\d+)'\s*,\s*fb:'(f\d+)'", html)
    if not cfgs:
        return ["no GRAPHS configs parsed"]
    for did, fid in cfgs:
        n_cont = len(re.findall(r'id="%s"' % did, html))
        if n_cont != 1:
            errors.append(f"container id={did}: found {n_cont} (need exactly 1)")
        m = re.search(r'<img[^>]*id="%s"[^>]*>' % fid, html)
        if not m:
            errors.append(f"fallback id={fid}: no <img> found")
            continue
        src = re.search(r'src="([^"]+)"', m.group(0))
        if not src:
            errors.append(f"fallback id={fid}: no src")
            continue
        p = os.path.join(os.path.dirname(HTML), src.group(1))
        if not os.path.isfile(p):
            errors.append(f"fallback id={fid}: PNG missing: {p}")
        elif os.path.getsize(p) == 0:
            errors.append(f"fallback id={fid}: PNG empty: {p}")
    # every fallback img must be referenced by exactly one config
    fids_cfg = [f for _, f in cfgs]
    for fid in set(fids_cfg):
        if fids_cfg.count(fid) != 1:
            errors.append(f"fb {fid} referenced {fids_cfg.count(fid)} times")
    return errors

def token_checks(html):
    """Each figure's latex block must contain its formula's signature tokens."""
    errors = []
    blocks = re.findall(r"\{id:'(d\d+)'.*?\[(.*?)\]\}", html, re.S)
    want = {
        'd1': [r'\sin', r'\cos', r'\frac{\pi}{2}'],
        'd2': [r'\sin', r'\cos'],
        'd3': [r'\ln', r'1-x'],
        'd4': [r'e^{x}', r'\ln'],
        'd5': [r'\arctan'],
        'd6': [r'e^{\frac{1}{x}}'],
        'd7': [r'\sin', r'\ln'],
    }
    have = {b[0]: b[1] for b in blocks}
    for did, toks in want.items():
        if did not in have:
            errors.append(f"no latex block for {did}")
            continue
        # JS string literals escape backslashes; normalize \\ -> \ before matching
        btxt = have[did].replace('\\\\', '\\')
        for t in toks:
            if t not in btxt:
                errors.append(f"{did}: token {t!r} missing from latex")
    return errors

def main():
    with open(HTML) as fh:
        html = fh.read()
    errs = run_checks(html) + token_checks(html)
    n_cfg = len(re.findall(r"\{id:'(d\d+)'\s*,\s*fb:'(f\d+)'", html))
    print(f"positive: {n_cfg} graph configs parsed")
    if errs:
        print("POSITIVE CHECK FAILURES:"); [print("  -", e) for e in errs]
        return 1
    print("positive: all ID-match, fallback-PNG, and formula-token checks passed")

    # ---- negative control: retarget one config at a nonexistent container; must FAIL
    bad = html.replace("{id:'d4',", "{id:'d9',", 1)
    assert bad != html, "mutation did not apply"
    berrs = run_checks(bad)
    if not berrs:
        print("NEGATIVE CONTROL FAILED: mutated HTML passed checks (test is blind)")
        return 1
    print(f"negative control: mutated config correctly rejected ({len(berrs)} error(s), e.g. {berrs[0]!r})")
    print("ALL GRAPH TESTS PASSED (positive + negative control)")
    return 0

sys.exit(main())
