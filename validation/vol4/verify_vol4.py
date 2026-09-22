#!/usr/bin/env python3
"""Structural/data assertions for the Volume IV overview page.

Checks: every referenced page exists, links from vol4/index.html resolve,
chunk totals add to 407, IC-1..IC-18 all appear, the four-version table is
present, v1 authority is stated, and the open-issue chain is complete.
"""
import os, re, sys

ROOT = os.path.expanduser("~/workspace/r-theory-rewrite")
fail = []
def check(cond, msg):
    print(("OK  " if cond else "FAIL") + " " + msg)
    if not cond:
        fail.append(msg)

def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()

# ---------- pages exist ----------
for p in ["vol4/index.html", "book17/index.html", "book18/index.html", "book19/index.html"]:
    check(os.path.isfile(os.path.join(ROOT, p)), f"exists: {p}")

vol4 = read("vol4/index.html")

# ---------- links from the overview resolve ----------
for target in ['href="../book17/"', 'href="../book18/"', 'href="../book19/"']:
    check(target in vol4, f"vol4 overview links {target}")

# ---------- chunk totals ----------
totals = [int(x) for x in re.findall(r"<td>(\d+)</td>\s*<td>CP", vol4)]
check(totals == [116, 58, 85, 40, 108], f"chunk totals {totals} == [116,58,85,40,108]")
check(sum(totals) == 407, f"sum of chunks = {sum(totals)} == 407")
check("407 assertions passed, 0 failed" in vol4, "407/0 assertion record stated")
check("18 distinct IC findings" in vol4 or "18 distinct IC" in vol4, "18 distinct ICs stated")
check("no timeouts" in vol4, "no timeouts stated")

# ---------- IC-1..IC-18 all present ----------
missing = [i for i in range(1, 19) if not re.search(rf"IC-{i}\b", vol4)]
check(not missing, f"IC-1..IC-18 all present (missing: {missing})")

# ---------- Δ_op = ∅ ----------
check("= ∅" in vol4 or "= ∅" in vol4.replace("&#8709;", "∅"),
      "Delta_op(Volume IV) = empty stated")
check("v1 is the sole audit authority" in vol4 or "sole audit authority" in vol4,
      "v1 authority stated")

# ---------- four-version table ----------
for vid in ["1-T5Eh7tbPcNenfB1ubkUmST5IYq_QGchm5X1ZcIRvoU",
            "1V3YwJZivcAtrcLs7IkT4zYlPkqGtBixZqSQjR22LxNc",
            "1sUOU-DDV_r9-sZXj13JUUgEFATZLI5eW7YBw2rcQ0mk",
            "1IiANYug3ISdG0GNApO-5T5jMl2EfsYN_LM5ZYqzPp0g"]:
    check(vid in vol4, f"version id present: {vid[:20]}...")
check("N_{1820}" in vol4 or "N_1820" in vol4, "v3 N_1820=3 claim contrast present")

# ---------- OI chain ----------
for oi in ["OI-01", "OI-23", "OI-24", "OI-29"]:
    check(oi in vol4, f"open-issue chain marker present: {oi}")

# ---------- open gates ----------
for g in ["S_F", "ζ_{parent}" if "ζ_{parent}" in vol4 else "ζ_parent",
          "η_{-4}" if "η_{-4}" in vol4 else "η_-4", "P_{6435}" if "P_{6435}" in vol4 else "P_6435"]:
    check(g in vol4, f"open gate present: {g}")

# ---------- Flatwave resolution recorded ----------
check("Resolved 2026-09-19" in vol4 or "resolved 2026-09-19" in vol4.lower(),
      "Flatwave identity resolution recorded with date")

# ---------- book pages cross-link the overview ----------
for b in ["book17", "book18", "book19"]:
    pg = read(f"{b}/index.html")
    check("../vol4/" in pg or "vol4" in pg, f"{b} page links the volume overview")

# ---------- per-book embed tests pass (rerun) ----------
import subprocess
for b in ["book17", "book18", "book19"]:
    r = subprocess.run([sys.executable, f"validation/{b}/test_embeds.py"],
                       cwd=ROOT, capture_output=True, text=True)
    check(r.returncode == 0, f"validation/{b}/test_embeds.py passes")

print()
if fail:
    print(f"{len(fail)} CHECK(S) FAILED")
    sys.exit(1)
print("All Volume IV structural/data checks passed.")
