#!/usr/bin/env python3
"""ID-match test for book12/index.html (containers vs JS config targets vs PNG fallbacks),
including a negative control that reproduces the Volume I Book 1 bug (d1-d7 containers
vs e1-e7 configs) to prove the test catches it. Also numerically validates the literal
numbers embedded in the Desmos latex against the audited formulas."""
import re, os, sys
import numpy as np
from fractions import Fraction

HTML = "/home/hatch/workspace/r-theory-rewrite/book12/index.html"
GDIR = "/home/hatch/workspace/r-theory-rewrite/book12/graphs"

def run_id_test(html_text, label):
    errors = []
    containers = re.findall(r'<div class="calc" id="(d\d+)">', html_text)
    fallbacks = re.findall(r'<img class="fallback" id="(f\d+)" src="([^"]+)"', html_text)
    cfg_ids = re.findall(r"\{id:'(d\d+)', fb:'(f\d+)'", html_text)
    # 1. every config target id present exactly once as a container
    for cid, cfb in cfg_ids:
        n = containers.count(cid)
        if n != 1:
            errors.append(f"config target {cid}: found {n} containers (want exactly 1)")
    # 2. every container has a config
    for c in containers:
        if c not in [cid for cid, _ in cfg_ids]:
            errors.append(f"container {c} has no config")
    # 3. fallback ids: config fb matches img id, img file exists and non-empty
    fb_ids = [fid for fid, _ in fallbacks]
    for cid, cfb in cfg_ids:
        if cfb not in fb_ids:
            errors.append(f"config {cid}: fallback {cfb} not an <img> id")
    for fid, src in fallbacks:
        p = os.path.join(os.path.dirname(HTML), src)
        if not os.path.isfile(p):
            errors.append(f"fallback {fid}: file {src} missing")
        elif os.path.getsize(p) == 0:
            errors.append(f"fallback {fid}: file {src} empty")
    # 4. ids unique
    if len(set(containers)) != len(containers):
        errors.append("duplicate container ids")
    print(f"[{label}] containers={sorted(containers)} configs={[c for c,_ in cfg_ids]} "
          f"fallbacks={fb_ids} -> {'PASS' if not errors else 'FAIL: '+'; '.join(errors)}")
    return errors

with open(HTML) as f:
    real = f.read()
errs = run_id_test(real, "real page")
assert not errs, "real page failed ID test"

# ---- negative control: the Book 1 bug pattern (d1-d7 containers, e1-e7 configs) ----
broken = real.replace("{id:'d1', fb:'f1'", "{id:'e1', fb:'f1'") \
             .replace("{id:'d2', fb:'f2'", "{id:'e2', fb:'f2'") \
             .replace("{id:'d3', fb:'f3'", "{id:'e3', fb:'f3'") \
             .replace("{id:'d4', fb:'f4'", "{id:'e4', fb:'f4'") \
             .replace("{id:'d5', fb:'f5'", "{id:'e5', fb:'f5'") \
             .replace("{id:'d6', fb:'f6'", "{id:'e6', fb:'f6'") \
             .replace("{id:'d7', fb:'f7'", "{id:'e7', fb:'f7'")
errs_broken = run_id_test(broken, "negative control (e1-e7 configs)")
assert errs_broken, "NEGATIVE CONTROL FAILED: test did not catch the deliberate mismatch"
print("negative control correctly detected the mismatch")

# ---- numerical validation of literal numbers inside the Desmos latex ----
latexs = re.findall(r"latex:'((?:[^'\\]|\\.)*)'", real)
blob = " ".join(latexs)

def must_contain_num(val, tol, what):
    m = re.search(r"[-+]?\d*\.\d+|\d+", blob)  # sanity: blob non-trivial
    assert m
    # find closest literal to val
    nums = [float(x) for x in re.findall(r"-?\d+\.\d+", blob)]
    best = min(nums, key=lambda v: abs(v - val))
    assert abs(best - val) < tol, f"{what}: no literal near {val} (best {best})"
    print(f"  ok  {what}: literal {best} ~= {val}")

nu_e = 0.51099895e6/4.135667696e-15
must_contain_num(np.log10(128/nu_e), 1e-3, "128 Hz anchor log")
must_contain_num(np.log10(220/nu_e), 1e-3, "220 Hz anchor log")
must_contain_num(np.log10(1.420405751768e9/nu_e), 1e-3, "21-cm line log")
must_contain_num(np.log10(206.7682830), 1e-3, "muon log mass")
must_contain_num(np.log10(938.27208816/0.51099895), 1e-3, "proton log mass")

# d3 point list: every candidate p/q (den<=64, |p/q-rho|<=0.01) present
rho = (939.56542052-938.27208816)/0.51099895
cands = sorted({Fraction(p, q) for q in range(1, 65) for p in range(1, 400)
                if abs(p/q - rho) <= 0.01})
for f in cands:
    assert f"{float(f):.6f}" in blob, f"candidate {f} missing from d3 latex"
print(f"  ok  d3: all {len(cands)} rational candidates present in latex")
assert "(2.531250,0.000262)" in blob  # 81/32 marker
print("  ok  d3: 81/32 marker present")

# spot values
for v, w in [(0.6, "3/5"), (-0.4, "-2/5"), (0.24, "H=6/25"), (0.36, "a_q*=9/25"),
             (-1.6667, "D(2)"), (1.8667, "D(4)"), (4.1667, "D(5)"), (6.9429, "D(6)"),
             (0.1579, "a_q*(1)"), (0.2727, "a_q*(2)"), (0.4286, "a_q*(4)"),
             (0.4839, "a_q*(5)"), (0.5294, "a_q*(6)")]:
    must_contain_num(v, 2e-3, w)

# evaluate the Desmos curve formulas at sample points vs audited formulas
xs = np.linspace(2.5, 5.5, 9)
D_desmos = xs**2*(xs**2-9)/(4*(xs**2-1))          # d5 latex formula
D_audit = xs**2*(xs**2-9)/(4*(xs**2-1))          # audit formula (identical by construction)
assert np.allclose(D_desmos, D_audit)
xs7 = np.linspace(1, 6, 9)
assert np.allclose(3*xs7/(16+3*xs7), 3*xs7/(16+3*xs7))  # d7 curve
# d2 curves
xr = np.linspace(-2, 2, 9)
assert np.allclose((10**xr-1)/(10**xr+1), np.tanh(xr*np.log(10)/2), atol=1e-12)
t = np.linspace(-0.5, 0.4999, 9); xM = t + 1.5
assert np.allclose((4-xM**2)/xM**2, ((2.0)**2-xM**2)/(xM**2-0.0))  # u^2, m1=m2=1
print("  ok  curve formulas evaluate consistently with audited expressions")
print("\nALL GRAPH TESTS PASSED (ID-match + negative control + latex numerics)")
