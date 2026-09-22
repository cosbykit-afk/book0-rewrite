# LEDGER — Volume IV v1, chunk 3: §17.18 (doc lines 1492–2770) + continued-calc sweep (411–776)

Script: `~/workspace/vol4/book17/audit_17_18.py`
Run: 2026-09-19. **85 assertions passed, 0 failed, no timeout** (wall 0.2 s;
all computations closed-form or small-numerics).

Published ledger: **CP 83 · NC 2 · IC 7 (IC-5…IC-11) · IN 3 (blocked)**.
No ST/MA/AX beyond the notes below (ST/MA tags used inline where the
manuscript leans on standard math or archive inputs).

Upstream dependencies (not re-derived): chunk-1 primitives, octant
structure, C8 word (E,B,E,O)×2, w₀=ln(1+√2), rapidity products, V_E,
IC-1/IC-2/IC-3 (LEDGER_17_1.md); chunk-2 T-norm/‖Q_F‖²/conversion-chain/
Wick-sign provenance note, IC-4 (LEDGER_17_6.md).

## Verdict summary

§17.18 is exactly what it advertises: the maximal exact reduction the
specified algebra permits, with the missing inputs named. The checkable
algebra (dimensions, combinatorics, conversion chain, formal projector
algebra, skeleton mechanics) verifies; the archive-sourced numbers are
internally consistent but not independently re-derived; the explicit
matrices are honestly OPEN; and the Wolfram skeleton as printed contains
four concrete defects. **S_F remains OPEN** — the honest finding, matching
the manuscript's own status.

## Verified (CP/NC)

### 17.18.2 — the 1820 representation space
- C(16,4) = 1820 exactly (CP); dim Sym²(128) = 8256 (CP);
  1 + 1820 + 6435 = 8256 (CP) — the Sym²(128) = 1 ⊕ 1820 ⊕ 6435
  decomposition is dimensionally exact (irrep structure: ST).
- dim Λ²(128) = 8128 = 120 + 8008 (CP) — the Λ²S = 120 ⊕ 8008
  decomposition used in 17.18.4.1 is dimensionally exact.
- dim Cl(16) = 2¹⁶ = 65536 = 256² (CP) — consistent with
  Cl(16) ≅ Mat(256,ℂ); chiral split 256 = 128 + 128 (CP).
- Formal projector algebra: (I−P₁−P₆₄₃₅)² = I−P₁−P₆₄₃₅ given the
  projector relations, and Tr = 8256−1−6435 = 1820, both exact as formal
  consequences (CP; orthogonality of P₁/P₆₄₃₅ is MA/OPEN in v1 since
  P₆₄₃₅ is unspecified).
- P₁(M) = (Tr_B M / Tr_B I)·I formally idempotent by linearity of Tr_B (CP).

### 17.18.3 — contact operator
- Frobenius internal consistency: 64/128 = 1/2 exactly, and
  (1/2)·128 = 64 matches ⟨Γ,PKPK⟩_F (CP). The numbers themselves are
  archive-sourced (MA); the manuscript carries the "(from archive)"
  qualifier on 17.18.3.1/17.18.3.2/17.18.3.3 and 17.18.6.2 (verified
  present). Note: 17.18.7.1 reframes the contact magnitude, Wick sign,
  and mass dependence as "determined by the specified algebra" under a
  bare "Status: EXACT." — slight qualifier drift; the "specified algebra"
  per the authority order includes archive inputs, so not marked IC.

### 17.18.4/17.18.5 — B and O propagators
- B at C8 positions 2, 6; O at positions 4, 8; E×4/B×2/O×2 (CP).
- (m₂⁻¹)⁴ = m₂⁻⁴ (CP).

### 17.18.6 — cyclic contraction
- Ordered product E₁B₁E₂O₁E₃B₂E₄O₂ = (E,B,E,O)×2 (CP).
- The three perfect matchings of {1,2,5,6} are exactly
  (12)(56), (15)(26), (16)(25) (CP, exhaustive enumeration).
- t-channel slot identification: (15) ↔ positions 1,5 = E₁,E₃;
  (26) ↔ positions 2,6 = B₁,B₂ (CP).
- (1/4)⁴ = 1/256 (CP); S_F = 3a₂₂₂₂ from (6/5)(5/2) = 3 (CP).

### 17.18.7/17.18.9/17.18.10 — reduction and conversion chain
- S_F = (18/5)c_ord from S_F = 3a, a = (6/5)c (CP);
  a₂₂₂₂ = (6/5)c_ord inverts consistently (CP).
- n̂₅₄ = −(√10/1536)S_Fm₂⁻⁴ = (−1)(1/256)(√10/6)S_Fm₂⁻⁴ (CP).
- "S_F = 12a₂₂₂₂ must be rejected": 12 ≠ 3, consistent (CP).
- Honest OPEN: "c_ord = 1, N₁₈₂₀ = 2, K_parent = 1 have not been
  established by the ordered contraction" (17.18.9.3) — the manuscript
  does not promote these; verified present.

### Low-Hanging Fruit (Tiers 1–5, lines 2163–2626)
- Tier 2.1 branching dimension check: 54+20+60+1 = 135 (CP).
- Tier 2.4 decomposition dimension check: 135+1820+1920 = 3875 (CP).
- Tier 2.2: P₆₄₃₅ = I−P₁−P₁₈₂₀ consistent with P₁₈₂₀ = I−P₁−P₆₄₃₅ (CP).
- Tier 4.1: the carrier V_R²+4H² = 1/4 is a smooth conic (gradient
  vanishes only at (0,0), off the curve) — genus-0 claim is ST (CP for
  smoothness).
- Tier 3.1's warning ("Do not infer (1/2)⁴ from one certified component")
  is present and epistemically sound: (1/2)⁴ = 1/16 ≠ 1/256 = (1/4)⁴
  (CP) — the 1/2→1/4 per-contact relation is not derived in v1, and the
  manuscript says so itself.
- Tiers 3–5 are prose plans honestly labeled; no mathematical
  overclaiming beyond the two ICs below.

## Incorrect as stated (IC) — 7 new findings

- **IC-5 (§17.18.5.2, line 1747): "all four O propagators."** The C8 word
  (E,B,E,O)×2 contains exactly **two** O propagators (positions 4, 8;
  verified). §17.18.4.2 correctly says "all four B/O propagators at
  grade 2" (2B+2O). The sentence as written claims four O's — a wording
  error; the intended meaning (all four propagators at grade 2) is clear.
- **IC-6 (Tier 1.3, line 2239): "The 120 = Λ²(16) sits inside Sym²(128)
  via the Clifford map."** This contradicts v1's own §17.18.4.1
  (line 1694): the 120 is "realized as Λ²(16) inside the fermion-pair
  decomposition Λ²S = 120 ⊕ 8008" — i.e. in the **antisymmetric** square.
  The text then admits "The image is antisymmetric in the spinor
  indices," confirming the Λ²(128) location. As written, the target
  space (Sym²(128)) and the admitted image (antisymmetric) are
  incompatible; §17.18.4.1 has the correct location. (The charitable
  reading — the 120's *induced operator action* on End(1820) — is not
  what is written.)
- **IC-7 (Tier 2.4, line 2330): "The 135 is the adjoint of SO(16)."**
  The adjoint of SO(16) has dimension 16·15/2 = **120**, not 135
  (verified). The 135 is Sym²₀(16), the traceless symmetric square of
  the vector. (Same sentence also appears in the bridge essay, line
  1006 — logged there, not audited.)
- **IC-8 (§17.18.8.2 skeleton Step 1): the 1820-basis construction.**
  `P1820 = NullSpace[Transpose[{traceVector}]]; (* 1820-dim basis *)`:
  Transpose[{v}] for a length-8256 list is an 8256×1 matrix; for any
  nonzero column, rank = 1 so nullity = 1−1 = **0** (verified by
  rank-nullity and a numeric analogue) — the code as written yields {},
  not an 1820-dim basis. Under the intended reading
  NullSpace[{traceVector}] (1×8256), nullity = 8256−1 = **8255** ≠ 1820.
  The comment is false under every reading; moreover the correct
  construction needs P₆₄₃₅, which v1 says is not in the authoritative
  documents — Step 1 cannot be repaired within v1's specified inputs.
- **IC-9 (§17.18.8.2 skeleton Steps 2–3): dimension mismatch.**
  Step 2's `KroneckerProduct[gammaI[i], gammaL[mu], gammaI[j],
  gammaL[nu]]` of four 128×128 matrices is 128⁴×128⁴ = 268,435,456 ×
  268,435,456 (verified), but Step 3 sandwiches it as
  `P1820 . GammaContact . Transpose[P1820]` with P1820 an 1820×8256
  basis — dimensionally incompatible as written.
- **IC-10 (§17.18.8.2 skeleton Steps 6–7): double-counting.**
  Step 6: `S_F = -(1/256) * S_F_raw;` — but the defined S_F
  (§17.18.6.5) is the **stripped** inner product ⟨Q_F, R̃⟩ (stripped of
  the −1 and 1/256). Step 7: `nHat54 = -(Sqrt[10]/1536) * S_F *
  m2^(-4);` with −(√10/1536) = −(1/256)(√10/6) (verified), which
  presumes a stripped input per §17.18.9.1. Feeding Step 6's dressed
  S_F into Step 7 applies the −(1/256) **twice**, violating §17.18.10's
  regression requirement "The contact factor and crossed Wick sign must
  be counted exactly once" (verified present).
- **IC-11 (§17.18.8.2 skeleton Step 5): `wickSign` undefined.**
  Step 5 sums `wickSign * contraction[...]` but `wickSign` is never
  assigned anywhere in the skeleton (verified: used at line 1996, no
  assignment). (Bugs IC-8/IC-9/IC-10/IC-11 also appear verbatim in the
  Book 18 duplicate of the skeleton at lines ~3189–3193 — out of scope,
  noted.)

## Incomplete / blocked (IN) — exact boundaries

- **IN-1: numerical Frobenius-norm recomputation — BLOCKED.**
  ⟨Γ,Γ⟩_F = 128 and ⟨Γ,PKPK⟩_F = 64 cannot be recomputed in v1: the
  explicit γ_i, B, Π_− are OPEN, and the "exact ordering and chirality
  restriction are determined by the convention of the parent action"
  (17.18.3.4) — the parent action is not in v1. Boundary: needs
  Tier 1.1 inputs + parent-action conventions. Internal consistency of
  the stated numbers verified (CP above); the numbers remain
  archive-sourced (MA).
- **IN-2: explicit 1820 projector matrix — BLOCKED at P₆₄₃₅.**
  v1: "The explicit form of P₆₄₃₅ requires the SO(16) branching rules
  for Sym²(128). This is contained in the literature but not in the
  current authoritative documents." (17.18.2.3). Formal construction
  verified (CP); explicit matrix OPEN.
- **IN-3: S_F numerical value — OPEN (manuscript's own label).**
  The audit confirms the gate is real: the symbolic setup closes
  (conversion chain, stripped response, regression requirements all
  verify), and the numerical evaluation awaits the explicit
  1820×1820 matrices per 17.18.12(a) or the group-theory proof per
  17.18.12(b). No numerical closure is promoted — honest.
- Ancillary: the Step-5 Sum as written ranges over 16⁴·4⁴ = 16,777,216
  index tuples (verified) — infeasible as a naive sum even with the
  inputs; any real implementation needs the factored structure. Noted
  as a feasibility caveat, not an IC (the manuscript presents it as a
  skeleton, and names Steps 1–4 as the bottleneck).

## Manuscript assertions / assumptions (MA/AX — not verified here)

- Clifford word P_iK_μP_jK_ν = Γ_(iμjν)Π_−; projection coefficient 1/2;
  Frobenius norms 128/64; t-channel pairing selection; σ_Wick^(t) = −1;
  (1/4)⁴ contact magnitude; m₂⁻⁴ mass dependence — all "EXACT (from
  archive)" per the manuscript; not independently derived in v1
  (qualifier discipline verified present except the 17.18.7.1 note above).
- Per-contact 1/4: the arithmetic (1/4)⁴ = 1/256 is CP; the 1/4 input
  and its relation to the certified 1/2 projection coefficient are
  archive/OPEN (Tier 3.1's warning is the honest statement).
- Q_F = (6/5)T (chunk-2 MA, pending §17.18 — §17.18 does not derive it;
  it is used as input at 17.18.6.5).
- "The 54 is the traceless symmetric square of the 10 of SO(10)"
  (Tier 2.1): standard (ST); the branching formula itself is
  dimensionally consistent (CP).
- 17.18.12(b)'s conditional ("if group theory alone fixed S_F it would
  contradict the reduced-matrix-element firewall") — honest
  conditional, no claim made.

## Terminology / organization notes (not errors)

- **Dangling cross-reference (line 2077):** 17.18.9.3 cites "§17.11"
  ("the E contact rapidity product is exactly 4 (from §17.11)") — no
  §17.11 exists in v1 (verified by header inventory). The value 4 is
  correct (chunk-1 CP, from §17.3); only the section number is wrong.
- **P₅₄ location unreconciled:** the preamble and Tier 2.1 place the
  physical 54 "inside the 135" of SO(16); §17.18.8.1's required inputs
  list "P54 : 54x54 or embedding of 54 in 1820." v1 does not reconcile
  these (a 54 could in principle appear in both branchings, but the
  manuscript never shows it).
- **Frobenius-norm ambiguity:** 17.18.3.3 states the norms without saying
  whether they are per fixed index tuple (i,μ,j,ν) or summed — the
  ratio argument works either way, but the statement is ambiguous.
- **Stub numbering offset:** the stub's "STRUCTURE OF THE REMAINDER OF
  BOOK 17" (lines 384–396) labels §17.4 = "Ancestry scenarios" and
  §17.5 = "UV footprint classification," but the continued calc has
  §17.4 = C8↔octant correspondence, §17.5 = ancestry, §17.6 = UV
  footprint — off by one from §17.4 onward (verified). Organization
  note, not a mathematical error.
- No "Flatwave" in §17.18 or the sweep region (grep): the CL-002 vs
  §17.1.4 terminology collision does not recur here.

## The line-2151 / Book-18-duplication note (recorded, not resolved)

- **Line 2151 "Book 18 should either:"** (verified present with (a)/(b)):
  (a) supply the explicit 1820×1820 matrices (γ_i, B, Π_−, M_e, Oprop,
  P₅₄) and execute the Wolfram skeleton to produce a numerical S_F; or
  (b) prove S_F is fixed by group theory alone — which "would contradict
  the reduced-matrix-element firewall and would require a new structural
  principle." Until one is done, "S_F remains OPEN and the physical
  matching y₂ ∝ η₋₄ ζ_parent n̂₅₄ remains formal in its neutral
  coefficient."
- **Title duplication (flagged):** §17.18 is titled "Explicit
  Construction of the C8 Contraction Module"; Book 18 (line 2999) is
  titled "THE COMPUTATIONAL FRONTIER: EXPLICIT CONSTRUCTION OF THE C8
  CONTRACTION MODULE" — the same construction under two headings, with
  the skeleton (including IC-8…IC-11) duplicated at lines ~3189–3193.
  Recorded; resolution belongs to a later chunk.

## Inter-section tension (recorded, not resolved — Book 18 is out of scope)

- **Propagator rapidity product:** §17.3.4 (sweep-verified) and §17.7.2
  (chunk-2 CP) give the **propagator** cosh product as (√2)⁴ = **4**
  (16 is the all-eight product). Book 18 §18.5 (~line 3542) states
  "**The propagator rapidity product is 16**, assigned to ζ_parent."
  The *assignment* to ζ_parent agrees with §17.5.3's resolution; the
  *value* (16 vs 4) contradicts it — Book 18's 16 matches the all-eight
  product, suggesting a mislabeled product.
- **638.78:** Book 18 §18.5 states "Its product over the four decay
  octants is 638.78. **This factors out of S_F**." In Book 17,
  §17.7.4's bound contains no 638.78 factor, §17.18.6.4's stripped
  list contains no V_E⁴ term, and the continued calc §17.3.5 says of
  638.78 only "its role in the Clifford contraction remains to be
  determined." Whether 638.78 factors out of S_F is therefore asserted
  in Book 18 but not established anywhere in Book 17.

## Secondary sweep: lines 411–776 (§§17.2–17.5 duplicates) — no new discrepancies

Systematic spot-check against the chunk-1/chunk-2 verdicts:
- **No contradictions** with the full-version audits. The duplicate text
  neither adds to nor relabels any chunk-1/chunk-2 verdict.
- **IC-1 recurs verbatim** (§17.2.1, line 440): "ε = sgn(sin 2x)
  records the sheet." Same finding as chunk 1 (ε is deck-invariant;
  records ellipse halves). Not a new IC.
- **IC-2 recurs verbatim** (§17.3.5): the printed radical
  `1/(2/√(2+√2) + (√2−1)) ≈ 5.027` for crx(112.5°) — verified it
  evaluates to ≈ 0.6682, not 5.027. Same finding; the four equal
  values themselves re-verify (V_E⁴ = 638.7823 ≈ 638.78, NC).
- 638.78 vs 638.7: truncation, per chunk 2 (not a rounding).
- Re-verified exactly (new CP assertions): cot(22.5°) = 1+√2,
  cot(67.5°) = √2−1, cot(112.5°) = −(√2−1), cot(157.5°) = −(1+√2);
  ln(√2−1) = −ln(1+√2); E/propagator/all-eight cosh products 4/4/16;
  ε sign products +1; §17.5.2 V−I = 0 in both countings; §17.5.1
  scenario table arithmetic (4k₀⁴, 4k₀, 4, 4).
- §17.4.3's Wick-pairing octant-language mapping is consistent with
  §17.18.6.2: octant labels coincide with the 8-product positions, so
  (15)(26) ↔ E₁–E₃ / B₁–B₂ in both tellings (CP).
- §17.5.3's resolution (propagator cosh factors → ζ_parent, excluded
  from the stripped response) is consistent with §17.18.6.4's stripped
  list (CP); it is the Book 18 "16" (above) that breaks the agreement.

## Open gates after this chunk

1. S_F numerical value — needs Book 18(a) (explicit matrices + skeleton
   execution, with IC-8…IC-11 repaired) or 18(b) (group-theory proof).
2. N₁₈₂₀ counting (Tier 3.1) — including the open 1/2→1/4 per-contact
   relation the manuscript honestly flags.
3. ζ_parent — uniform-action premise (Tier 3.3); propagator-product
   4-vs-16 tension with Book 18.
4. η₋₄ — UV footprint selection (Tier 5.1; physical choice).
5. c_ord, K_parent numerical values — not established (17.18.9.3).
6. P₅₄ location reconciliation (135 vs 1820).
7. Whether 638.78 factors out of S_F (Book 18 asserts; Book 17 does not).

## Not yet touched (later chunks)

- Book 18 (doc lines 2999–3637), including the duplicated skeleton and
  the §18.5 claims behind the tension above.
- Book 19.
- Bridge-essay identities (§1.3–§1.5, §3.1–§3.2) — logged in chunk 2,
  not audited.
- Embedded v2 preamble (lines 2627–2770, "Transfer state: September 16,
  2026"): v2 content physically present in the v1 raw file; treated as
  context only per audit authority, not audited.
- v2 / v3-draft / unsigned certification report in ~/workspace/vol4/:
  context only; none of their claims are used as findings (in
  particular v3's S_F = 0.48958371 / N_1820 = 3 "certified" numbers are
  not audit findings — v1 honestly records S_F OPEN).
