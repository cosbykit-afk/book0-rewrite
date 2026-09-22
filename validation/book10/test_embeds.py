#!/usr/bin/env python3
"""Book 10 embed consistency: Desmos latex vs fallback PNGs vs captions.

Checks (all must pass, exit 0):
 E1 every <div class="calc" id="dN"> has a GRAPHS entry with matching fb id
 E2 every <img class="fallback" id="fN" src="graphs/..."> file exists, non-empty
 E3 each graph's latex contains the formula its caption/fallback claims
     (incl. the d3 sign fix: dashed curve is +F, not -F; d1 meridian at y=pi)
 E3b viewports cover the plotted data without overreach; d1 meridian inside rect
 E3c captions disclose the live-vs-static panel subsets (d4, d5) and the
     un-browser-verified live Desmos rendering
 E4 Desmos API loader present

Negative control: run with --negativize to corrupt one container id in a temp
copy and show the test catches it.
"""
import os
import re
import sys
import tempfile
import shutil

REPO = os.path.expanduser("~/workspace/r-theory-rewrite")
PAGE = os.path.join(REPO, "book10/index.html")
GRAPHS_DIR = os.path.join(REPO, "book10", "graphs")


def run_test(html_path):
    errs = []
    html = open(html_path).read()

    # E1: calc divs <-> GRAPHS entries <-> fallback imgs
    divs = re.findall(r'<div class="calc" id="(d\d+)">', html)
    imgs = re.findall(r'<img class="fallback" id="(f\d+)" src="(graphs/[^"]+)"', html)
    entries = re.findall(r"\{id:'(d\d+)', fb:'(f\d+)'", html)
    if not divs:
        errs.append("no calc divs found")
    if not (len(divs) == len(imgs) == len(entries) == 5):
        errs.append(f"counts: divs={divs} imgs={imgs} entries={entries} (want 5 each)")
    for d, (eid, fb) in zip(divs, entries):
        if d != eid:
            errs.append(f"div {d} != entry {eid}")
    for (eid, fb), (fid, src) in zip(entries, imgs):
        if fb != fid:
            errs.append(f"entry fb {fb} != img {fid}")

    # duplicate id scan over the whole document
    all_ids = re.findall(r'id="([^"]+)"', html)
    seen = {}
    for i in all_ids:
        seen[i] = seen.get(i, 0) + 1
    dups = {k: v for k, v in seen.items() if v > 1}
    if dups:
        errs.append(f"duplicate ids in document: {dups}")

    # E2: fallback files exist and are non-empty
    for fid, src in imgs:
        p = os.path.join(REPO, "book10", src)
        if not os.path.isfile(p):
            errs.append(f"fallback {fid}: PNG missing at {p}")
        elif os.path.getsize(p) == 0:
            errs.append(f"fallback {fid}: PNG empty at {p}")

    # E3: latex formula fragments per graph
    def latex_of(d):
        m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{[^}]*\}, exprs:\[(.*?)\]\}",
                      html, re.S)
        if not m:
            errs.append(f"no GRAPHS block for {d}")
            return ""
        return m.group(1)

    L = {d: latex_of(d) for d, _ in entries}
    # Note: the HTML holds JS strings, so every latex backslash appears doubled.
    checks = [
        ("d1", r"y=\\pi\\left\\{0<x<2\\pi\\right\\}", "meridian at y=pi (inside rect)"),
        ("d1", r"x=0\\left\\{0<y<2\\pi\\right\\}", "rect left edge"),
        ("d1", r"x=2\\pi\\left\\{0<y<2\\pi\\right\\}", "rect right edge"),
        ("d1", r"y=2\\pi\\left\\{0<x<2\\pi\\right\\}", "rect top edge"),
        ("d2", r"y=\\tanh\\left(\\frac{x}{2}\\right)", "tanh(x/2) curve"),
        ("d2", r"(2.2401,0.8076)", "mass-shell sample point"),
        ("d3", r"0.0198389x^{0.99997337}e^{-0.00729735x}", "normalized ground-state F"),
        ("d4", r"(266.3,0.0339),(305.7,-0.1367)", "P node sign-change bracket"),
        ("d4", r"(701.0,-0.9990)", "P minimum"),
        ("d4", r"(924.3,0.0009)", "Q sample"),
        ("d5", r"y=2\\cos^{2}\\left(x\\right)", "p_sxp = 2F^2"),
        ("d5", r"y=-2\\sin^{2}\\left(x\\right)", "p_srx = -2G^2"),
        ("d5", r"\\left(\\cos\\left(x\\right)-\\sin\\left(x\\right)\\right)^{2}",
         "p_cxp = (F-G)^2"),
        ("d5", r"-\\left(\\cos\\left(x\\right)+\\sin\\left(x\\right)\\right)^{2}",
         "p_crx = -(F+G)^2"),
    ]
    for d, frag, what in checks:
        if L[d] and frag not in L[d]:
            errs.append(f"{d}: missing latex for {what}")
    # d3 sign fix: the dashed rescaled curve must be +F (caption: -G/|G/F| = F),
    # never the negated -F the embed carried before the fix.
    if L.get("d3"):
        if L["d3"].count("0.0198389x^{0.99997337}e^{-0.00729735x}") != 2:
            errs.append("d3: want solid AND dashed exprs both equal to +F")
        if "-0.0198389x" in L["d3"] or "-0.0198363x" in L["d3"]:
            errs.append("d3: negated ground-state curve present (sign bug)")

    # E3b: viewports cover the data, no overreach
    def viewport(d):
        m = re.search(r"\{id:'" + d + r"', fb:'f\d+', vw:\{([^}]*)\}", html)
        if not m:
            errs.append(f"no viewport for {d}")
            return None
        return dict(re.findall(r"(left|right|bottom|top):(-?[\d.]+)", m.group(1)))

    import math
    need = {
        "d1": dict(left=(-1.5, 0.0), right=(2*math.pi, 8.0),
                   bottom=(-1.5, 0.0), top=(2*math.pi, 8.0)),
        "d2": dict(left=(-0.5, 0.0), right=(5.0, 6.0),
                   bottom=(-0.2, 0.0), top=(1.0, 1.2)),
        "d3": dict(left=(-100.0, 0.0), right=(1500.0, 1600.0),
                   bottom=(-0.2, 0.0), top=(1.0, 1.2)),
        "d4": dict(left=(-100.0, 0.0), right=(1400.0, 1500.0),
                   bottom=(-1.2, -1.0), top=(0.55, 1.2)),
        "d5": dict(left=(-1.0, 0.0), right=(2*math.pi, 7.5),
                   bottom=(-2.5, -2.0), top=(2.0, 2.5)),
    }
    for d, bounds in need.items():
        vw = viewport(d)
        if not vw:
            continue
        for k, (lo, hi) in bounds.items():
            v = float(vw[k])
            if not (lo <= v <= hi):
                errs.append(f"{d}: viewport {k}={v} outside [{lo},{hi}]")

    # E3c: caption honesty disclosures
    if "the top panel (F and G) as subsampled points" not in html:
        errs.append("Fig 4 caption must disclose live Desmos shows only the top panel")
    if "the four charts (right panel)" not in html:
        errs.append("Fig 5 caption must disclose live Desmos shows only the right panel")
    if "not</i> verified in a browser" not in html:
        errs.append("page must disclose live Desmos rendering was not browser-verified")

    # E4: Desmos loader
    if "https://www.desmos.com/api/v1.10/calculator.js" not in html:
        errs.append("Desmos API loader missing")
    return errs


def main():
    if "--negativize" in sys.argv:
        # NEGATIVE CONTROL: corrupt one CONTAINER id (d3 -> dX) in a temp copy.
        tmp = tempfile.mkdtemp()
        bad = os.path.join(tmp, "index.html")
        html = open(PAGE).read().replace('<div class="calc" id="d3">',
                                         '<div class="calc" id="dX">', 1)
        assert '<div class="calc" id="dX">' in html, "negativize substitution failed"
        open(bad, "w").write(html)
        errs = run_test(bad)
        shutil.rmtree(tmp)
        print("NEGATIVE CONTROL (container d3 corrupted to dX):")
        if errs:
            print("  test correctly FAILED with:")
            for e in errs:
                print("   -", e)
            return 0
        print("  ERROR: test did NOT catch the deliberate mismatch!")
        return 1
    errs = run_test(PAGE)
    if errs:
        print("FAIL:")
        for e in errs:
            print(" -", e)
        return 1
    print("OK [E1] 5 calc divs <-> GRAPHS entries <-> fallback imgs linked, "
          "no duplicate ids")
    print("OK [E2] all 5 fallback PNGs exist and are non-empty")
    print("OK [E3] all latex formula fragments present and match captions/fallbacks "
          "(d3 sign fix, d1 meridian at y=pi)")
    print("OK [E3b] all 5 viewports cover the plotted data without overreach")
    print("OK [E3c] caption panel-subset + live-Desmos-unverified disclosures present")
    print("OK [E4] Desmos API loader present")
    print("\nAll embed consistency checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
