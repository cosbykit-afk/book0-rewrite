#!/usr/bin/env python3
"""
Audit chunk 4: Volume IV v1, Book 18 — "THE COMPUTATIONAL FRONTIER:
EXPLICIT CONSTRUCTION OF THE C8 CONTRACTION MODULE"
(doc lines 2999-3220 of volume_iv_v1_raw.txt).

Every check is a real assertion with a scope tag:
  CP checked proof | SC completed symbolic check | NC completed numerical check
  ST standard imported theorem | MA manuscript assertion | AX assumption/axiom
  IN incomplete/failed computation | IC incorrect result

A failed assertion fails the run (exit 1) and is printed.
Prints total pass count, scope tallies, and an explicit timeout report.
"""
import math
import sys
import time
from fractions import Fraction

import numpy as np

RAW = "/home/hatch/workspace/vol4/volume_iv_v1_raw.txt"
B18_LO, B18_HI = 2999, 3220  # 1-based inclusive

t0 = time.time()
passed = []   # (name, scope, detail)
failed = []   # (name, scope, detail)

def check(name, cond, scope, detail=""):
    """Record a scoped assertion; failure fails the run."""
    if cond:
        passed.append((name, scope, detail))
    else:
        failed.append((name, scope, detail))
        print("FAILED [%s] %s %s" % (scope, name, detail), flush=True)

# ---------------------------------------------------------------- text ---
lines = open(RAW, encoding="utf-8").read().split("\n")
b18 = "\n".join(lines[B18_LO - 1:B18_HI])          # Book 18 exact text
s1718 = "\n".join(lines[1937 - 1:2012])            # 17.18.8.2 skeleton region
sk18 = "\n".join(lines[3148 - 1:3200])             # 18.8 skeleton region

# ============================================================ §18.1, §18.9 honesty
check("18.1 states no numerical S_F is provided",
      "It does not provide a numerical value for S_F" in b18, "CP",
      "descriptive accuracy of the book's own scope")
check("18.1 states explicit 1820x1820 matrices are not in codebase",
      "are not yet in the codebase" in b18, "CP")
check("18.9 gate table lists exactly the six OPEN gates",
      all(("Cl(16) gamma matrices OPEN" in b18, "1820 projector OPEN" in b18,
           "120 embedding OPEN" in b18, "54 projector OPEN" in b18,
           "S_F numerical value OPEN" in b18, "N\u2081\u2088\u2082\u2080 OPEN" in b18)),
      "CP", "gate table matches section statuses 18.2-18.7")

# ============================================================ dimension checks (CP)
check("C(16,4) = 1820", math.comb(16, 4) == 1820, "CP")
check("dim Sym^2(128) = 128*129/2 = 8256", 128 * 129 // 2 == 8256, "CP")
check("1 + 1820 + 6435 = 8256", 1 + 1820 + 6435 == 8256, "CP")
check("2^7 = 128 (chiral spinor dim)", 2 ** 7 == 128, "CP")
check("branching sum 54+20+60+1 = 135",
      54 + 20 + 10 * 6 + 1 == 135, "CP", "135|_{SO(10)xSU(4)}")
check("Sym^2_0(10): 55-1 = 54", 10 * 11 // 2 - 1 == 54, "CP")

# ============================================================ conversion chain (§18.6)
check("S_F = 3 a from (6/5)(5/2) = 3",
      Fraction(6, 5) * Fraction(5, 2) == 3, "CP")
check("a = (6/5) c inverts to c = 5S/18",
      Fraction(3) * Fraction(6, 5) == Fraction(18, 5) and
      Fraction(18, 5) ** -1 == Fraction(5, 18), "CP",
      "S=3a, a=(6/5)c => S = (18/5)c => c = (5/18)S")
check("-(1/256)(sqrt10/6) = -sqrt10/1536 (exact float)",
      (1 / 256) * (math.sqrt(10) / 6) == math.sqrt(10) / 1536, "CP",
      "division by 256 exact in binary; Step 7 prefactor = Step-6 factor x (sqrt10/6)")

# ============================================================ chirality projector (CP conditional)
check("gamma_17^2 = +1 under Clifford relations",
      (-1) ** (16 * 15 // 2) == 1, "CP",
      "conditional on {gamma_i,gamma_j}=2 delta_ij (OPEN in v1): Pi_pm idempotent")

# ============================================================ rapidity numbers for tension record
check("propagator cosh product (sqrt2)^4 = 4 (established)",
      abs(math.sqrt(2) ** 4 - 4) < 1e-12, "CP")
check("all-eight cosh product (sqrt2)^8 = 16",
      abs(math.sqrt(2) ** 8 - 16) < 1e-12, "CP",
      "16 matches the all-eight product, not the propagator product")
check("V_E^4 ~ 638.78", abs(5.0273 ** 4 - 638.78) < 0.05, "NC",
      "V_E ~ 5.0273 from chunk 1; 5.0273^4 = %.4f" % (5.0273 ** 4))

# ============================================================ §18.2 gamma template (IC-17)
check("18.2 template line present with i=1..8 only",
      "\u03c3_x^{\u2297(i\u22121)} \u2297 \u03c3_a \u2297 I^{\u2297(8\u2212i)}" in b18 and
      "for i = 1,...,8, with appropriate extensions for i = 9,...,16" in b18,
      "CP", "text grounding for IC-17")
check("IC-17: 8 qubit factors give 256x256, not the required 128x128",
      2 ** 8 == 256 and 256 != 128, "IC",
      "template yields 256x256 matrices; section requires 'explicit 128x128 matrices' "
      "acting on the 128-dim chiral spinor. Also: sigma_a undefined (no assignment in "
      "Book 18), only i=1..8 shown for 16 matrices, 'extensions' undefined. "
      "OPEN status keeps missing-inputs honest, but the printed template is "
      "dimensionally inconsistent with the requirement.")
check("sigma_a never defined in Book 18",
      "\u03c3_a" in b18 and not any(s in b18 for s in
          ["\u03c3_a =", "\u03c3_a:=", "\u03c3_a :="]), "IC",
      "subsumed in IC-17")

# ============================================================ §18.4 120 embedding (IC-12)
check("18.4 claims 120 sits inside Sym^2(128)",
      "The 120 = \u039b\u00b2(16) sits inside Sym\u00b2(128)" in b18 and
      "\u039b\u00b2(16) \u2192 Sym\u00b2(128)" in b18, "CP", "text grounding for IC-12")
check("17.18.4.1 places the 120 in Lambda^2 S = 120 + 8008",
      "inside the fermion-pair decomposition \u039b\u00b2S = 120 \u2295 8008" in
      "\n".join(lines), "CP", "v1's own location, line 1692")
check("IC-12: 120 in Sym^2(128) contradicts v1 17.18.4.1",
      ("The 120 = \u039b\u00b2(16) sits inside Sym\u00b2(128)" in b18) and
      ("inside the fermion-pair decomposition \u039b\u00b2S = 120 \u2295 8008" in "\n".join(lines)),
      "IC", "recurrence of IC-6 (Tier 1.3): Sym^2(128) = 1+1820+6435 contains no 120; "
      "the 120 is the antisymmetric-square branch per 17.18.4.1. Section self-labels "
      "'formal construction EXACT'.")

# ============================================================ §18.8 skeleton defect recurrences
# IC-13: Step 1 NullSpace
check("skeleton Step 1 line present in 18.8",
      "P1820 = NullSpace[Transpose[{traceVector}]];" in sk18, "CP")
rng = np.random.default_rng(0)
v = rng.standard_normal(8256)
# Wolfram NullSpace of an m x n matrix: nullity = n - rank (variables = columns).
# Transpose[{v}] is 8256 x 1 -> n = 1; intended reading {v} is 1 x 8256 -> n = 8256.
nullity_as_written = 1 - np.linalg.matrix_rank(np.atleast_2d(v).T)   # 8256x1
nullity_intended = 8256 - np.linalg.matrix_rank(np.atleast_2d(v))    # 1x8256
check("IC-13: NullSpace[Transpose[{v}]] nullity = 0, not 1820",
      nullity_as_written == 0, "IC",
      "rank(8256x1 nonzero) = 1 -> nullity 0; code yields {}, not an 1820-dim basis. "
      "Recurrence of IC-8.")
check("IC-13b: intended reading gives 8255, not 1820",
      nullity_intended == 8255 and nullity_intended != 1820, "IC",
      "NullSpace[{traceVector}] (1x8256) nullity = 8255; correct construction needs "
      "P_6435 which v1 says is not in the authoritative documents (unfixable in v1). "
      "Recurrence of IC-8.")
# IC-14: Step 2-3 dimension mismatch
check("IC-14: KroneckerProduct of four 128x128 is 128^4 x 128^4",
      128 ** 4 == 268435456 and 128 ** 4 not in (1820, 8256), "IC",
      "Step 2 product is 268435456x268435456; Step 3 sandwiches with P1820 as an "
      "1820x8256 basis -- dimensionally incompatible as written. Recurrence of IC-9.")
check("skeleton Step 2/3 lines present in 18.8",
      "KroneckerProduct[gammaI[i], gammaL[mu], gammaI[j], gammaL[nu]]" in sk18 and
      "P1820 . GammaContact[i, mu, j, nu] . Transpose[P1820]" in sk18, "CP")
# IC-15: Steps 6-7 double count
check("skeleton Step 6 and Step 7 lines present in 18.8",
      "S_F = -(1/256) * S_F_raw;" in sk18 and
      "nHat54 = -(Sqrt[10]/1536) * S_F * m2^(-4);" in sk18, "CP")
check("IC-15: -(1/256) applied twice across Steps 6-7",
      ("S_F = -(1/256) * S_F_raw;" in sk18) and
      ("nHat54 = -(Sqrt[10]/1536) * S_F * m2^(-4);" in sk18) and
      ((1 / 256) * (math.sqrt(10) / 6) == math.sqrt(10) / 1536),
      "IC", "Step 6 dresses S_F with -(1/256); Step 7's -(sqrt10/1536) = -(1/256)(sqrt10/6) "
      "presumes a stripped input per 17.18.9.1/18.6 (S_F := <Q_F, R~^t_2222> = 3a). "
      "Violates 17.18.10 regression 'counted exactly once'. Recurrence of IC-10.")
# IC-16: wickSign undefined
check("IC-16: wickSign used in Step 5, never assigned",
      "wickSign * contraction" in sk18 and
      not any(s in sk18 for s in ["wickSign =", "wickSign:=", "wickSign :="]), "IC",
      "used at 18.8 Step 5; no assignment in the skeleton. Recurrence of IC-11.")

# ============================================================ skeleton diff vs §17.18.8.2
check("four defect-bearing constructs duplicated from 17.18.8.2",
      all(("P1820 = NullSpace[Transpose[{traceVector}]];" in s1718,
           "KroneckerProduct[gammaI[i], gammaL[mu], gammaI[j], gammaL[nu]]" in s1718,
           "S_F = -(1/256) * S_F_raw;" in s1718,
           "wickSign * contraction" in s1718)), "CP",
      "Book 18 skeleton is a structural duplicate of 17.18.8.2")
check("Book 18 skeleton drops the explicit Step-5 sum ranges",
      "{i1,16},{mu1,4}" in s1718 and
      "S_F_raw = Sum[wickSign * contraction[...], {...}];" in sk18, "CP",
      "17.18.8.2 ranges over 16^4*4^4 = 16777216 tuples (infeasible naive); "
      "18.8 replaces ranges with {...} -- further abbreviation, same defects")
check("Book 18 header drops pPlus/pMinus/selectorPairs",
      "pPlus, pMinus, selectorPairs, P3875" in s1718 and
      "pPlus" not in sk18, "CP", "18.8 header: only roots, simple, coords, "
      "bb[i,j], killingChevalley, P3875")

# ============================================================ §18.5 tension verdict (task item 3)
check("Book 18 contains no 'propagator rapidity product is 16'",
      "propagator rapidity product is 16" not in b18, "CP")
check("Book 18 contains no '638.78'",
      "638.78" not in b18, "CP")
check("claims live at line 3542, inside Book 19 (starts line 3221)",
      "propagator rapidity product is 16" in lines[3542 - 1] and
      "638.78" in lines[3542 - 1] and
      lines[3221 - 1].startswith("BOOK 19"), "CP",
      "chunk-3 misattribution to 'Book 18 section 18.5' corrected: 18.5 is 'The 54 "
      "Projector'. The tension is Book-19-vs-Book-17, out of this chunk's scope; "
      "flagged for the Book 19 chunk.")

# ============================================================ terminology / notes
check("no Flatwave/FlatWave in Book 18",
      "flatwave" not in b18.lower(), "CP",
      "CL-002 vs 17.1.4 collision does not recur in Book 18")
check("P54 location tension present: 'inside the 135' vs 'embedding of 54 in 1820'",
      "It sits inside the 135 of SO(16)" in b18 and
      "P54 : 54x54 or embedding of 54 in 1820" in sk18, "CP",
      "open tension recorded (same as chunk-3 note); v1 does not reconcile")
check("18.6 states sigma_Wick^(t) = -1 with no 'from archive' qualifier",
      "\u03c3_Wick^(t) = \u22121" in b18 and "archive" not in "\n".join(lines[3096:3145]).lower(),
      "CP", "qualifier drift vs 17.18.6.2 which carried '(from archive)'; "
      "authority order includes archive inputs so not marked IC (as in chunk 3)")
check("18.6 missing-input line present for E, B, O matrices",
      "Missing input: The explicit 1820\u00d71820 matrices for E, B, O." in b18, "CP")

# ============================================================ report
elapsed = time.time() - t0
tally = {}
for _, s, _ in passed:
    tally[s] = tally.get(s, 0) + 1
print("=" * 70)
print("Book 18 audit: %d passed, %d failed (wall %.2fs)" % (len(passed), len(failed), elapsed))
print("scope tallies:", {k: tally[k] for k in sorted(tally)})
print("timeout: none (all checks closed-form/small numerics/text greps)")
if failed:
    print("FAILURES:")
    for n, s, d in failed:
        print(" - [%s] %s :: %s" % (s, n, d))
    sys.exit(1)
print("ALL ASSERTIONS PASSED")
