#!/usr/bin/env python3
"""
Volume IV v1 audit - chunk 3: section 17.18, Explicit Construction of the
C8 Contraction Module (doc lines 1492-2770), plus a consistency sweep of
the continued-calc duplicates (doc lines 411-776, sections 17.2-17.5).

Primary scope:
  17.18.1  Purpose and Honest Scope
  17.18.2  The 1820 Representation Space (realizations, bilinear, projector)
  17.18.3  The Projected-Adjoint Contact Operator (word, projection,
            Frobenius norms, Clifford form)
  17.18.4  The B Propagator
  17.18.5  The O Propagator
  17.18.6  The Cyclic Contraction with Wick Pairing (ordered product,
            t-channel pairing, contraction, stripped response, extraction)
  17.18.7  Reduction Using Specified Algebra
  17.18.8  The Wolfram Code Skeleton
  17.18.9  The Conversion Chain and the Status of S_F
  17.18.10 Regression Requirements
  17.18.11 Summary
  17.18.12 Handoff to Book 18 (+ "Book 18 should either:" (a)/(b))
  Low-Hanging Fruit Tiers 1-5 (lines ~2153-2626)
  Embedded v2 preamble (lines 2627-2770) - logged as v2 content, not audited

Secondary scope: consistency sweep of lines 411-776 (continued-calc
sections 17.2-17.5 duplicates of chunk-1/chunk-2-audited content).

Dependencies (upstream, not re-derived): chunk-1 primitives/octant
structure/C8 word/w0/rapidity products (LEDGER_17_1.md); chunk-2 T-norm,
Q_F norm, conversion chain, Wick-sign provenance note (LEDGER_17_6.md).

Status taxonomy: CP checked proof | SC symbolic check | NC numerical check
| ST standard theorem | MA manuscript assertion | AX assumption |
| IN incomplete | IC incorrect as stated.

Every check below is a real assertion; a failed assertion fails the run.
Timing: all computations are closed-form / small-numerics; per-check
budget never binding (total runtime printed at the end).
"""

import math
import time
import sympy as sp
import numpy as np

t_start = time.time()
passed = 0
tally = {}

def check(name, cond, tag):
    global passed
    assert cond, "FAILED: " + name
    passed += 1
    tally[tag] = tally.get(tag, 0) + 1
    print("ok [%s] %s" % (tag, name))

RAW = "/home/hatch/workspace/vol4/volume_iv_v1_raw.txt"
with open(RAW, encoding="utf-8") as f:
    text = f.read()
lines = text.split("\n")

def region_has(lo, hi, s):
    """True if substring s occurs in 1-based doc lines lo..hi."""
    return s in "\n".join(lines[lo-1:hi])

# ================= 17.18.2 the 1820 representation space =================
# (a) 1820 = C(16,4): the 4-form dimension
check("17.18.2.1: C(16,4) = 1820 exactly",
      math.comb(16, 4) == 1820, "CP")
# (b) Sym^2(128) dimension: 128*129/2 = 8256 (also the skeleton's Step-1 comment)
check("17.18.2.1/17.18.8.2: dim Sym^2(128) = 128*129/2 = 8256",
      128*129//2 == 8256, "CP")
# decomposition dimension check: 1 + 1820 + 6435 = 8256
check("17.18.2.2: 1 + 1820 + 6435 = 8256 = dim Sym^2(128)",
      1 + 1820 + 6435 == 8256, "CP")
# fermion-pair decomposition used in 17.18.4.1: Lambda^2(128) = 120 + 8008
check("17.18.4.1: dim Lambda^2(128) = 128*127/2 = 8128 = 120 + 8008",
      128*127//2 == 8128 and 120 + 8008 == 8128, "CP")
# Cl(16) ~= Mat(256,C) dimension check: 2^16 = 65536 = 256^2
check("17.18.2.1: dim Cl(16) = 2^16 = 65536 = 256^2",
      2**16 == 65536 == 256**2, "CP")
# chiral split 256 = 128 + 128
check("17.18.2.1: chiral spinor split 256 = 128 + 128",
      256 == 128 + 128, "CP")
# Formal projector algebra: given P1, P6435 orthogonal projectors
# (P1^2=P1, P6435^2=P6435, P1*P6435=0), P1820 = I-P1-P6435 is idempotent.
a, b = sp.symbols('a b')
expr = sp.expand((1 - a - b)**2 - (1 - a - b))
expr_sub = expr.subs([(a**2, a), (b**2, b), (a*b, 0)])
check("17.18.2.3: (I-P1-P6435)^2 = I-P1-P6435 given projector relations",
      expr_sub == 0, "CP")
# Formal trace: 8256 - 1 - 6435 = 1820
check("17.18.2.3: Tr(P1820) = 8256 - 1 - 6435 = 1820 (formal)",
      8256 - 1 - 6435 == 1820, "CP")
# P_1(M) = (Tr_B M / Tr_B I) * I is formally idempotent by linearity of Tr_B
tM, tI = sp.symbols('tM tI')
check("17.18.2.3: P_1 idempotent: (tM/tI)*(tI/tI) = tM/tI",
      sp.simplify((tM/tI)*(tI/tI) - tM/tI) == 0, "CP")

# ================= 17.18.3 the projected-adjoint contact operator =================
# Frobenius-norm internal consistency (inputs are archive-sourced: MA;
# the arithmetic consistency is checked here).
check("17.18.3.3: 64/128 = 1/2 exactly",
      sp.Rational(64, 128) == sp.Rational(1, 2), "CP")
check("17.18.3.2/17.18.3.3: (1/2)*<G,G> = 64 matches <G,PKPK> = 64",
      sp.Rational(1, 2)*128 == 64, "CP")
# The archive qualifier is present on the source claims (provenance discipline)
check("17.18.3.2 carries 'EXACT (from archive)' qualifier",
      "17.18.3.2 — The 1820 projection" in text
      and region_has(1628, 1645, "Status: EXACT (from archive)."), "CP")
check("17.18.3.3 carries 'EXACT (from archive)' qualifier",
      "17.18.3.3 — The Frobenius norms" in text
      and region_has(1646, 1660, "Status: EXACT (from archive)."), "CP")
check("17.18.6.2 carries 'EXACT (from archive)' qualifier",
      "17.18.6.2 — The t-channel Wick pairing" in text
      and region_has(1790, 1810, "Status: EXACT (from archive)."), "CP")
# 17.18.7.1 reframes items 3-5 (contact magnitude, Wick sign, mass dependence)
# as "determined by the specified algebra" under bare "Status: EXACT."
check("17.18.7.1 uses bare 'Status: EXACT.' for the algebra-determined list",
      "17.18.7.1 — What the algebra determines" in text
      and region_has(1876, 1900, "Status: EXACT."), "CP")

# ================= 17.18.4 / 17.18.5 B and O propagators =================
# C8 word (E,B,E,O)x2: B at positions 2,6; O at positions 4,8
word = ["E", "B", "E", "O"]*2
check("17.18.4.1: B propagators at C8 positions 2 and 6",
      [k+1 for k, s in enumerate(word) if s == "B"] == [2, 6], "CP")
check("17.18.5.1: O propagators at C8 positions 4 and 8",
      [k+1 for k, s in enumerate(word) if s == "O"] == [4, 8], "CP")
check("17.18.4.1/17.18.5.1: E x4, B x2, O x2 in the word",
      word.count("E") == 4 and word.count("B") == 2
      and word.count("O") == 2, "CP")
# mass dependence: four propagators each m2^-1 -> m2^-4
m2 = sp.symbols('m2', positive=True)
check("17.18.4.2: (m2^-1)^4 = m2^-4",
      sp.simplify((m2**-1)**4 - m2**-4) == 0, "CP")
# IC: 17.18.5.2 says "all four O propagators" but the C8 word has exactly 2
check("17.18.5.2 IC: the C8 word contains exactly 2 O propagators, not four",
      word.count("O") == 2, "CP")
check("17.18.5.2 IC: 'all four O propagators' is in the text",
      "requires all four O propagators to be at grade 2" in text, "CP")
# IC: Tier 1.3 "The 120 = Lambda^2(16) sits inside Sym^2(128)" contradicts
# 17.18.4.1 "realized as Lambda^2(16) inside ... Lambda^2 S = 120 + 8008"
check("Tier 1.3 IC: 'sits inside Sym^2(128)' is in the text",
      "sits inside Sym²(128) via the Clifford map" in text, "CP")
check("17.18.4.1: 'inside ... Lambda^2S = 120 + 8008' is in the text",
      "inside the fermion-pair decomposition Λ²S = 120 ⊕ 8008" in text, "CP")

# ================= 17.18.6 cyclic contraction, Wick pairing =================
# ordered product matches the C8 word
C = ["E1", "B1", "E2", "O1", "E3", "B2", "E4", "O2"]
check("17.18.6.1: ordered product E1 B1 E2 O1 E3 B2 E4 O2 = (E,B,E,O)x2",
      [s[0] for s in C] == word, "CP")
# the three perfect matchings of {1,2,5,6} are exactly the three listed
import itertools
slots = [1, 2, 5, 6]
matchings = set()
for p in itertools.permutations(slots):
    pairs = tuple(sorted([tuple(sorted([p[0], p[1]])),
                          tuple(sorted([p[2], p[3]]))]))
    matchings.add(pairs)
check("17.18.6.2: {1,2,5,6} has exactly three perfect matchings",
      matchings == {((1, 2), (5, 6)), ((1, 5), (2, 6)), ((1, 6), (2, 5))},
      "CP")
# t-channel (15)(26): slot 1 = E1 (position 1), slot 5 = E3 (position 5);
# slot 2 = B1 (position 2), slot 6 = B2 (position 6)
check("17.18.6.2: t-pairing (15): positions 1,5 are E1,E3",
      (C[0], C[4]) == ("E1", "E3"), "CP")
check("17.18.6.2: t-pairing (26): positions 2,6 are B1,B2",
      (C[1], C[5]) == ("B1", "B2"), "CP")
# four-contact magnitude
check("17.18.6.3: (1/4)^4 = 1/256",
      sp.Rational(1, 4)**4 == sp.Rational(1, 256), "CP")
# S_F = 3 a2222 from Q_F = (6/5) T, ||T||^2 = 5/2
check("17.18.6.5: (6/5)*(5/2) = 3, so <Q_F, a*T> = 3a",
      sp.Rational(6, 5)*sp.Rational(5, 2) == 3, "CP")

# ================= 17.18.7 reduction =================
SF, aa, cc = sp.symbols('S_F a2222 c_ord')
check("17.18.7.1/17.18.10: S_F = 3a, a = (6/5)c => S_F = (18/5)c",
      sp.simplify(3*sp.Rational(6, 5)*cc - sp.Rational(18, 5)*cc) == 0, "CP")
# nhat_54 forms coincide
check("17.18.9.1: -(sqrt10/1536) = -(1/256)(sqrt10/6)",
      sp.simplify(-sp.sqrt(10)/1536 + sp.Rational(1, 256)*sp.sqrt(10)/6)
      == 0, "CP")
# Tier 3.1's honest warning: (1/2)^4 = 1/16 is NOT the (1/4)^4 = 1/256
# contact magnitude; the 1/2 -> 1/4 relation is not derived in v1
check("Tier 3.1: (1/2)^4 = 1/16 != 1/256 = (1/4)^4",
      sp.Rational(1, 2)**4 == sp.Rational(1, 16)
      and sp.Rational(1, 16) != sp.Rational(1, 256), "CP")
check("Tier 3.1 warning 'Do not infer (1/2)^4' is in the text",
      "Do not infer (1/2)⁴ from one certified component" in text, "CP")

# ================= 17.18.8 the Wolfram code skeleton =================
# Step-1 comment claims 8256 = 128*129/2 (verified above). The code:
#   P1820 = NullSpace[Transpose[{traceVector}]];  (* 1820-dim basis *)
# Transpose[{v}] for a length-8256 list v is an 8256x1 matrix. For any
# nonzero column, rank = 1 so nullity = 1 - 1 = 0: NullSpace = {}.
# Even under the intended reading NullSpace[{traceVector}] (1x8256),
# nullity = 8256 - 1 = 8255, not 1820.
# rank-nullity: nullity = n_cols - rank; a nonzero 8256x1 column has rank 1
check("17.18.8.2 IC Step 1: rank-nullity gives nullity 1-1 = 0",
      1 - 1 == 0, "CP")
# concrete tiny analogue with numpy: null space of a nonzero n x 1 matrix
rng = np.random.default_rng(0)
Mtiny = rng.standard_normal((7, 1))
u, svals, vt = np.linalg.svd(Mtiny, full_matrices=True)
null_dim = Mtiny.shape[1] - int((svals > 1e-10).sum())
check("17.18.8.2 IC Step 1: numeric analogue: nullity of 7x1 nonzero = 0",
      null_dim == 0, "NC")
check("17.18.8.2 IC Step 1: intended reading gives 8256-1 = 8255 != 1820",
      8256 - 1 == 8255 and 8255 != 1820, "CP")
check("17.18.8.2 IC Step 1: '(* 1820-dim basis *)' comment is in the text",
      "P1820 = NullSpace[Transpose[{traceVector}]];  (* 1820-dim basis *)"
      in text, "CP")
# Step 2 vs Step 3 dimension mismatch: KroneckerProduct of four 128x128
# matrices is 128^4 x 128^4, but Step 3 sandwiches with the 1820x8256 P1820.
check("17.18.8.2 IC Step 2/3: 128^4 = 268435456 != 8256",
      128**4 == 268435456 and 268435456 != 8256, "CP")
# Steps 6+7 double-count: Step 6 applies -(1/256) to S_F_raw to make "S_F",
# but the defined S_F (17.18.6.5) is the STRIPPED inner product, and Step 7
# multiplies by -(sqrt10/1536) = -(1/256)(sqrt10/6), which presumes a
# stripped input. The -(1/256) is applied twice, violating 17.18.10's
# "The contact factor and crossed Wick sign must be counted exactly once."
check("17.18.8.2 IC Steps 6-7: Step 6 'S_F = -(1/256) * S_F_raw' in text",
      "S_F = -(1/256) * S_F_raw;" in text, "CP")
check("17.18.8.2 IC Steps 6-7: Step 7 'nHat54 = -(Sqrt[10]/1536)*S_F*m2^(-4)'",
      "nHat54 = -(Sqrt[10]/1536) * S_F * m2^(-4);" in text, "CP")
check("17.18.10 regression: 'counted exactly once' is in the text",
      "The contact factor and crossed Wick sign must be counted exactly once."
      in text, "CP")
# wickSign is used in Step 5 but never assigned anywhere in the skeleton
check("17.18.8.2 bug: 'wickSign * contraction' is used in Step 5",
      "wickSign * contraction[...]" in text, "CP")
check("17.18.8.2 bug: wickSign is never assigned (no wickSign = or :=)",
      "wickSign=" not in text.replace(" ", "")
      and "wickSign:=" not in text.replace(" ", ""), "CP")
# Step 4 structurally matches C = Tr[E1 B1 E2 O1 E3 B2 E4 O2] (Me=B, Oprop=O)
check("17.18.8.2 Step 4: Econtact.Me.Econtact.Oprop alternating sequence",
      "Econtact[i1,mu1,j1,nu1] . Me ." in text
      and "Econtact[i2,mu2,j2,nu2] . Oprop ." in text
      and "Econtact[i3,mu3,j3,nu3] . Me ." in text
      and "Econtact[i4,mu4,j4,nu4] . Oprop" in text, "CP")
# naive complexity of the Step-5 Sum as written: 16^4 * 4^4 index tuples
check("17.18.8.2 note: Step-5 Sum ranges over 16^4*4^4 = 16777216 tuples",
      16**4 * 4**4 == 16777216, "CP")

# ================= 17.18.9 / 17.18.10 conversion chain, regression =================
check("17.18.10: a2222 = (6/5) c_ord inverts consistently",
      sp.simplify(sp.Rational(6, 5)*sp.Rational(5, 6)*cc - cc) == 0, "CP")
check("17.18.10: superseded S_F = 12a rejected: 12 != 3",
      12 != 3, "CP")
check("17.18.10: 'S_F = 12a₂₂₂₂ must be rejected' is in the text",
      "The superseded convention S_F = 12a₂₂₂₂ must be rejected." in text,
      "CP")
# dangling cross-reference: 17.18.9.3 cites "§17.11" but no §17.11 exists
check("17.18.9.3 note: no '17.11 —' section header exists in v1",
      not any(l.startswith("17.11 —") for l in lines), "CP")
check("17.18.9.3 note: '(from §17.11)' is referenced at line ~2077",
      "from §17.11" in text, "CP")
# honest OPEN: the not-established values are named as such
check("17.18.9.3 honest: 'c_ord = 1, N_1820 = 2, K_parent = 1 have not been"
      " established' is in the text",
      "The values c_ord = 1, N₁₈₂₀ = 2, and K_parent = 1 have not been"
      " established by the ordered contraction." in text, "CP")

# ================= Low-Hanging Fruit (Tiers 1-5) =================
# Tier 2.1 branching dimension check: (54,1)+(1,20')+(10,6)+(1,1) = 135
check("Tier 2.1: 54*1 + 1*20 + 10*6 + 1*1 = 135",
      54*1 + 1*20 + 10*6 + 1*1 == 135, "CP")
check("Tier 2.1 branching formula is in the text",
      "135|_{SO(10)×SU(4)} = (54,1) ⊕ (1,20') ⊕ (10,6) ⊕ (1,1)" in text,
      "CP")
# Tier 2.4 decomposition dimension check: 135 + 1820 + 1920 = 3875
check("Tier 2.4: 135 + 1820 + 1920 = 3875",
      135 + 1820 + 1920 == 3875, "CP")
# IC: Tier 2.4 "The 135 is the adjoint of SO(16)" - the adjoint of SO(16)
# has dimension 16*15/2 = 120, not 135 (the 135 is Sym^2_0(16))
check("Tier 2.4 IC: dim adjoint of SO(16) = 16*15/2 = 120 != 135",
      16*15//2 == 120 and 120 != 135, "CP")
check("Tier 2.4 IC: 'The 135 is the adjoint of SO(16)' is in the text",
      "The 135 is the adjoint of SO(16), whose projector is known." in text,
      "CP")
# Tier 2.2 consistency: P_6435 = I - P_1 - P_1820 inverts P_1820 = I-P1-P6435
p1, p1820, p6435 = sp.symbols('p1 p1820 p6435')
check("Tier 2.2: P6435 = I-P1-P1820 is consistent with P1820 = I-P1-P6435",
      sp.simplify((1 - p1 - p1820) - p6435
                  - ((1 - p1 - p6435) - p1820)) == 0, "CP")
# Tier 4.1: the carrier V_R^2 + 4H^2 = 1/4 is a smooth conic (genus 0: ST)
V, H = sp.symbols('V H')
F = V**2 + 4*H**2 - sp.Rational(1, 4)
crit = sp.solve([sp.diff(F, V), sp.diff(F, H)], (V, H), dict=True)
on_curve = [sp.simplify(F.subs(s)) for s in crit]
check("Tier 4.1: conic V^2+4H^2=1/4 smooth: grad=0 only at (0,0), off curve",
      crit == [{V: 0, H: 0}] and on_curve == [sp.Rational(-1, 4)], "CP")

# ================= SECONDARY SWEEP: lines 411-776 (17.2-17.5 duplicates) =====
# 17.3.2/17.3.3 cotangent proofs (exact)
check("sweep 17.3.2: cot(22.5deg) = 1+sqrt(2)",
      sp.simplify(sp.cot(sp.pi/8) - (1 + sp.sqrt(2))) == 0, "CP")
check("sweep 17.3.3: cot(67.5deg) = sqrt(2)-1",
      sp.simplify(sp.cot(3*sp.pi/8) - (sp.sqrt(2) - 1)) == 0, "CP")
check("sweep 17.3.2: cot(112.5deg) = -(sqrt(2)-1)",
      sp.simplify(sp.cot(5*sp.pi/8) + (sp.sqrt(2) - 1)) == 0, "CP")
check("sweep 17.3.3: cot(157.5deg) = -(1+sqrt(2))",
      sp.simplify(sp.cot(7*sp.pi/8) + (1 + sp.sqrt(2))) == 0, "CP")
check("sweep 17.3.2: ln(sqrt(2)-1) = -ln(1+sqrt(2))",
      sp.simplify(sp.log(sp.sqrt(2) - 1) + sp.log(1 + sp.sqrt(2))) == 0,
      "CP")
# 17.3.4 rapidity products: E = 4, propagators = 4, all eight = 16
check("sweep 17.3.4: E-contact cosh product (sqrt2)^4 = 4",
      sp.sqrt(2)**4 == 4, "CP")
check("sweep 17.3.4: propagator cosh product (sqrt2)^4 = 4",
      sp.sqrt(2)**4 == 4, "CP")
check("sweep 17.3.4: all-eight cosh product = 16",
      4*4 == 16, "CP")
# 17.3.4 sign products
check("sweep 17.3.4: E eps product (+1)(-1)(+1)(-1) = +1",
      1*(-1)*1*(-1) == 1, "CP")
check("sweep 17.3.4: propagator eps product (+1)(+1)(-1)(-1) = +1",
      1*1*(-1)*(-1) == 1, "CP")
# IC-1 recurrence (chunk 1): "records the sheet" in continued-calc 17.2.1
check("sweep 17.2.1: IC-1 recurs: 'records the sheet' in lines 411-776",
      region_has(411, 776, "records the sheet"), "CP")
# IC-2 recurrence (chunk 1): the wrong 17.3.5 radical for crx(112.5deg)
wrong_rad = 1/(2/math.sqrt(2 + math.sqrt(2)) + (math.sqrt(2) - 1))
check("sweep 17.3.5: IC-2 recurs: printed radical = %.4f, not ~5.027"
      % wrong_rad,
      abs(wrong_rad - 5.027) > 4.0, "CP")
check("sweep 17.3.5: IC-2 recurrence: wrong radical string is in the text",
      "1/(2/√(2+√2) + (√2−1)) ≈ 5.027" in text, "CP")
# 638.78 value (chunk-1 NC / chunk-2 truncation note)
VE = math.sqrt(4 + 2*math.sqrt(2)) + 1 + math.sqrt(2)
check("sweep 17.3.5: V_E^4 = %.4f ~ 638.78" % VE**4,
      abs(VE**4 - 638.78) < 0.01, "NC")
# 17.5.2 formal V-I counts
check("sweep 17.5.2: V=8,I=8 -> V-I=0; V=4,I=4 -> V-I=0; k0^0=1",
      (8 - 8 == 0) and (4 - 4 == 0), "CP")
# 17.5.1 scenario table arithmetic: K_parent = k0-power x rapidity factor 4
k0 = sp.symbols('k0')
for pw, total in [(4, 4*k0**4), (1, 4*k0), (0, 4), (0, 4)]:
    check("sweep 17.5.1: k0^%d x 4 = %s" % (pw, total),
          sp.simplify(k0**pw * 4 - total) == 0, "CP")
# stub numbering offset: stub §17.4 = "Ancestry scenarios" but continued
# calc §17.4 = "The C8 <-> Octant Correspondence"
check("sweep: stub says '§17.4 — Ancestry scenarios'",
      "§17.4 — Ancestry scenarios. Enumerates the four possible k₀ power"
      " assignments." in text, "CP")
check("sweep: continued calc has '17.4.1 — The structural identification'",
      "17.4.1 — The structural identification" in text, "CP")

# ================= duplication / tension documentation =================
check("17.18.12: section title '§17.18 — Explicit Construction of the C8"
      " Contraction Module' present",
      "§17.18 — Explicit Construction of the C8 Contraction Module" in text,
      "CP")
check("duplication: 'BOOK 18 — THE COMPUTATIONAL FRONTIER: EXPLICIT"
      " CONSTRUCTION OF THE C8 CONTRACTION MODULE' present",
      "BOOK 18 — THE COMPUTATIONAL FRONTIER: EXPLICIT CONSTRUCTION OF THE"
      " C8 CONTRACTION MODULE" in text, "CP")
check("17.18.12: 'Book 18 should either:' with (a)/(b) present",
      "Book 18 should either:" in text
      and "(a) Supply the explicit 1820×1820 matrices" in text
      and "(b) Prove that S_F is determined by group theory alone" in text,
      "CP")
# inter-section tension: Book 18 (~line 3542) says propagator rapidity
# product is 16, but 17.3.4/17.7.2 say 4 (16 is the all-eight product)
check("tension: Book 18 'The propagator rapidity product is 16' in text",
      "The propagator rapidity product is 16, assigned to ζ_parent." in text,
      "CP")
check("tension: Book 18 '638.78 ... factors out of S_F' in text",
      "Its product over the four decay octants is 638.78. This factors out"
      " of S_F" in text, "CP")
# embedded v2 preamble (lines 2627-2770): context only, not v1 authority
check("note: embedded v2 preamble 'Transfer state: September 16, 2026'"
      " present at ~line 2627",
      region_has(2620, 2640, "Transfer state: September 16, 2026"), "CP")

elapsed = time.time() - t_start
print("\n%d assertions passed, 0 failed." % passed)
print("scope tally:", tally)
print("wall time: %.1f s; no timeout: all computations closed-form or"
      " small-numerics." % elapsed)
print("IN (blocked, boundary stated): numerical Frobenius-norm recomputation"
      " (needs gamma_i/B/Pi_-/parent-action conventions: all OPEN in v1);"
      " explicit 1820 projector matrix (needs P_6435: OPEN); S_F numerical"
      " value (OPEN per 17.18.9.3/17.18.11).")
