# LEDGER — Volume IV v1, chunk 4: Book 18 (doc lines 2999–3220)

Script: `~/workspace/vol4/book18/audit_18.py`
Run: 2026-09-19. **40 assertions passed, 0 failed, no timeout** (wall 0.16 s;
all checks closed-form, small numerics, or text greps).

Published ledger: **CP 31 · NC 1 · IC 6 (IC-12…IC-17, two with sub-assertions)**.
No SC/ST/MA/AX beyond the notes below. No IN: every computation in this
chunk closed; all numerical claims either recompute or are admitted OPEN by
the manuscript.

Upstream dependencies (not re-derived): chunk-1 octant structure, C8 word,
rapidity products, V_E, IC-1/IC-2/IC-3 (LEDGER_17_1.md); chunk-2 T-norm,
conversion chain, Wick-sign provenance, IC-4 (LEDGER_17_6.md); chunk-3
§17.18 formal algebra, IC-5…IC-11, IN-1…IN-3, open-gate list (LEDGER_17_18.md).

## Verdict summary

Book 18 is exactly what §18.1 advertises: an implementation book that
specifies the algebraic setup, names the missing inputs, and reprints the
Wolfram skeleton — it provides no numerical S_F and honestly labels all
six gates OPEN. The checkable algebra (dimensions, branching, conversion
chain, projector idempotency condition) verifies. The skeleton is a
**structural duplicate of §17.18.8.2 carrying all four defects verbatim**
(IC-13…IC-16 = recurrences of IC-8…IC-11), with the Step-5 sum ranges
further abbreviated away. Two more errors recur as IC-12 (120 in
Sym²(128), = IC-6) and IC-17 (new: the §18.2 gamma template is
dimensionally inconsistent with the section's own 128×128 requirement).
The §18.5 tension the task asked to resolve is a **location error**:
Book 18 §18.5 is "The 54 Projector" — it makes no rapidity-product or
638.78 claim; those claims live at line 3542 in **Book 19**.

## Verified (CP/NC)

### 18.1 / 18.9 — honest scope
- §18.1's self-description verifies: it states no numerical S_F is
  provided and the explicit 1820×1820 matrices are not yet in the
  codebase (CP).
- §18.9's gate table lists exactly the six gates (Cl(16) gamma
  matrices, 1820 projector, 120 embedding, 54 projector, S_F numerical
  value, N₁₈₂₀), all OPEN — consistent with §§18.2–18.7 (CP).

### Dimensions / combinatorics (§§18.2–18.5)
- C(16,4) = 1820 (CP); 128·129/2 = 8256 = dim Sym²(128) (CP);
  1 + 1820 + 6435 = 8256 (CP); 2⁷ = 128 (CP).
- Branching arithmetic: 54 + 20 + 10·6 + 1 = 135 (CP);
  Sym²₀(10): 55 − 1 = 54 (CP).
- §18.5's branching formula 135|_{SO(10)×SU(4)} = (54,1)⊕(1,20')⊕(10,6)⊕(1,1)
  is dimensionally exact (CP); the SO(10)/SU(4) content is standard
  representation theory (ST, not derived here).

### Conversion chain (§18.6)
- S_F = 3a₂₂₂₂ from (6/5)(5/2) = 3 (CP); a = (6/5)c inverts to
  c_ord = 5S_F/18 (CP); −(1/256)(√10/6) = −√10/1536 exactly (CP).
- γ_17² = +1 under Clifford relations (sign (−1)^{120} = +1), so
  Π_± = (1±γ_17)/2 is idempotent — CP as a conditional inference; the
  γ_i relations themselves are OPEN in v1.
- Missing-input lines (§18.6: explicit 1820×1820 E, B, O matrices)
  are present and honest (CP).

### Tension arithmetic (recorded for Book 19)
- (√2)⁴ = 4 (established propagator cosh product, CP);
  (√2)⁸ = 16 (all-eight product, CP) — the value 16 at line 3542
  matches the all-eight product, not the propagator product.
- V_E⁴ ≈ 638.78: 5.0273⁴ = 638.76, within 0.05 (NC).

## Incorrect as stated (IC) — 6 findings

- **IC-12 (§18.4): "The 120 = Λ²(16) sits inside Sym²(128)."**
  Recurrence of IC-6 (Tier 1.3). Contradicts v1's own §17.18.4.1
  (line 1692): the 120 is "realized as Λ²(16) inside the fermion-pair
  decomposition Λ²S = 120 ⊕ 8008" — the antisymmetric square. Moreover
  Sym²(128) = 1 ⊕ 1820 ⊕ 6435 contains no 120 subrep. The section
  self-labels "OPEN (formal construction EXACT)"; the target space
  makes the "formal construction" claim false. The map
  e_i∧e_j ↦ (1/2)[γ_i,γ_j] is written Λ²(16) → Sym²(128); the domain is
  antisymmetric in i,j while the codomain is symmetric in spinor
  indices — incompatible as written.
- **IC-13 (§18.8 Step 1, recurs IC-8):**
  `P1820 = NullSpace[Transpose[{traceVector}]];` — Transpose[{v}] for a
  length-8256 vector is 8256×1; nullity = 1 − 1 = 0 (verified by
  rank-nullity on a numeric analogue), so the code yields {}, not an
  1820-dim basis. Under the intended reading NullSpace[{traceVector}]
  (1×8256), nullity = 8255 ≠ 1820. Unfixable within v1: needs P_6435,
  which v1 says is not in the authoritative documents.
- **IC-14 (§18.8 Steps 2–3, recurs IC-9):**
  `KroneckerProduct[gammaI[i], gammaL[mu], gammaI[j], gammaL[nu]]`
  of four 128×128 matrices is 128⁴×128⁴ = 268,435,456×268,435,456,
  but Step 3 sandwiches it as `P1820 . GammaContact . Transpose[P1820]`
  with P1820 an 1820×8256 basis — dimensionally incompatible.
- **IC-15 (§18.8 Steps 6–7, recurs IC-10):**
  `S_F = -(1/256) * S_F_raw;` then
  `nHat54 = -(Sqrt[10]/1536) * S_F * m2^(-4);` with
  −(√10/1536) = −(1/256)(√10/6) (verified exact). But §18.6 defines
  S_F := ⟨Q_F, R̃^t_2222⟩ = 3a₂₂₂₂ — the *stripped* scalar. The −(1/256)
  is applied twice, violating §17.18.10's regression requirement
  ("counted exactly once").
- **IC-16 (§18.8 Step 5, recurs IC-11):**
  `S_F_raw = Sum[wickSign * contraction[...], {...}];` — `wickSign` is
  never assigned anywhere in the skeleton (verified by text search).
- **IC-17 (§18.2, NEW): the gamma template is dimensionally
  inconsistent with the section's own requirement.**
  The "standard construction" γ_i = σ_x^{⊗(i−1)} ⊗ σ_a ⊗ I^{⊗(8−i)}
  has 8 qubit factors → 256×256 matrices, but the section requires
  "the explicit 128×128 matrices" acting on the 128-dimensional
  chiral spinor. Additionally: σ_a is never defined (no assignment in
  Book 18), only i = 1,…,8 is shown for 16 matrices, and the
  "appropriate extensions for i = 9,…,16" are undefined. The OPEN
  status keeps the missing-inputs admission honest, but the printed
  template cannot produce what the section asks for.

## Skeleton diff: §17.18.8.2 vs §18.8 (verified in script)

- All four defect-bearing constructs are textually duplicated:
  the NullSpace line, the KroneckerProduct line, the
  `S_F = -(1/256) * S_F_raw;` line, and `wickSign * contraction`.
- Differences: (a) §18.8's required-inputs header drops
  `pPlus, pMinus, selectorPairs` (present in §17.18.8.1's Appendix A
  list); (b) Step 1 comment drops "as traceless symmetric square";
  (c) Step 4's explicit index signature is abbreviated to
  `contraction[...] := ...`; (d) Step 5's explicit sum ranges
  `{i1,16},{mu1,4},…` (16⁴·4⁴ = 16,777,216 tuples, infeasible naive —
  chunk-3 caveat) are replaced by `{...}`; (e) Step 7 comment changed
  to "Convert". None of these change the defects.

## The §18.5 tension — verdict: misattribution, corrected

The task's "line-~3542 tension" (Book 18 §18.5 reportedly saying
"propagator rapidity product is 16, assigned to ζ_parent" and
"638.78 factors out of S_F") is a **location error**:
- Book 18 §18.5 (lines 3077–3094) is "The 54 Projector"; it contains
  neither claim (verified: no "propagator rapidity product is 16",
  no "638.78" anywhere in lines 2999–3220).
- Both claims are at **line 3542, in Book 19** (BOOK 19 header at
  line 3221), §19 item "5. Dominant Function and Rapidity":
  "Its product over the four decay octants is 638.78. This factors out
  of S_F… The propagator rapidity product is 16, assigned to ζ_parent."
- Arithmetic record for the Book 19 chunk: established propagator
  cosh product = (√2)⁴ = 4 (§17.3.4, §17.7.2); all-eight product =
  (√2)⁸ = 16; line 3542's value 16 matches the all-eight product, so
  the *value* contradicts the established 4 while the *assignment to
  ζ_parent* agrees with §17.5.3's resolution (sweep-verified CP).
  The "638.78 factors out of S_F" assertion has no support in Book 17
  (§17.18.6.4's stripped list contains no V_E⁴ term; §17.3.5 says its
  role "remains to be determined").
- Verdict within this chunk's scope: no IC against Book 18 — Book 18
  makes no such claim. The tension is Book-19-vs-Book-17 and belongs
  to the Book 19 chunk.

## Manuscript assertions / assumptions (MA/AX — not verified here)

- (1/4)⁴ contact magnitude, σ_Wick^(t) = −1, m₂⁻⁴ mass dependence,
  Frobenius norms, Clifford word — archive inputs per chunk 3 (MA).
- Note: §18.6 states σ_Wick^(t) = −1 **without** the "(from archive)"
  qualifier that §17.18.6.2 carried — qualifier drift, logged, not
  marked IC (authority order includes archive inputs).
- Bγ_iB⁻¹ = −γ_iᵀ: standard charge-conjugation relation (ST); the
  γ_i themselves are OPEN.
- SO(16) irrep content (Sym²(128) = 1⊕1820⊕6435, Λ²S = 120⊕8008):
  standard (ST).

## Terminology / organization notes (not errors)

- **Title duplication (recorded, unresolved):** §17.18 "Explicit
  Construction of the C8 Contraction Module" vs Book 18 "THE
  COMPUTATIONAL FRONTIER: EXPLICIT CONSTRUCTION OF THE C8
  CONTRACTION MODULE" — same construction under two headings.
- **P₅₄ location unreconciled (recurs from chunk 3):** §18.5 says the
  54 "sits inside the 135"; §18.8's required inputs say
  "P54 : 54x54 or embedding of 54 in 1820"; §18.5's missing input is
  "the explicit Clebsch–Gordan map P_{1820→54}". A map *from* the
  1820 *to* the 54 sits oddly with a 54 "inside the 135" — v1 does not
  reconcile.
- **No "Flatwave"/"FlatWave" in Book 18** (verified): the CL-002 vs
  §17.1.4 terminology collision does not recur here.
- §18.7 (N₁₈₂₀ counting) is prose honestly labeled OPEN; no new math
  claims.

## Open gates after this chunk (unchanged from §18.9)

1. S_F numerical value — needs explicit matrices + repaired skeleton
   (IC-13…IC-16 must be fixed first) or group-theory proof.
2. N₁₈₂₀ counting (1/2→1/4 per-contact relation still open).
3. ζ_parent — uniform-action premise; value-16-vs-4 tension now
   located in Book 19 (Book 19 chunk's scope).
4. η₋₄ — UV footprint selection.
5. c_ord, K_parent numerical values — not established.
6. P₅₄ location reconciliation (135 vs 1820); new: P_{1820→54}
   notation vs "embedding of 54 in 1820".
7. Whether 638.78 factors out of S_F — asserted at Book 19 line 3542,
   not established in Book 17.

## Not yet touched (later chunks)

- Book 19 (doc lines 3221–3637), including the line-3542 rapidity
  claims and the 16-vs-4 / 638.78 verdicts.
- Appendices A–C (line 3420: "Appendix C — Computational Codebase
  Skeleton" — inside Book 19's line range).
- v2 / v3-draft / unsigned certification report in ~/workspace/vol4/:
  context only; none of their claims are audit findings.
