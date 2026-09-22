# LEDGER — Volume IV v1, chunk 5 (final): Book 19 + Appendices A–C (doc lines 3221–3637)

Script: `~/workspace/vol4/book19/audit_19.py`
Run: 2026-09-19. **108 assertions passed, 0 failed, no timeout** (wall < 1 s;
all computations closed-form, small numerics, or text greps).

Published ledger: **CP 73 · NC 1 · ST 2 · MA 31 · AX 1 · IC 1 new (IC-18) ·
IC-13…IC-16 carried over by reference · IN 0**.
Findings recorded: 23 total — IC 5 (IC-13…IC-16 carry-overs + IC-18),
8 Appendix-A flags, 2 internal contradictions (CONTR-1, CONTR-2),
1 manuscript-assertion note, 2 organization notes, 1 overstatement,
1 unverifiable, 2 v3-contradictions, 1 report-contradiction.

Upstream dependencies (not re-derived): chunk-1 octant structure, C8 word,
rapidity products (E-contact 4, propagator 4, all-eight 16), V_E, IC-1…IC-3
(LEDGER_17_1.md); chunk-2 T-norm, conversion chain, IC-4 (LEDGER_17_6.md);
chunk-3 §17.18 formal algebra, stripped-response definition, IC-5…IC-11,
IN-1…IN-3 (LEDGER_17_18.md); chunk-4 Book 18 dims/branching, IC-12…IC-17,
line-3542 located in Book 19 (LEDGER_18.md).

## Verdict summary

Book 19 is an honest closing book: every gate it names is labeled OPEN /
CONDITIONAL / CONTESTED, Δ_op(Volume IV) = ∅ is stated plainly, and the
falsifiability criteria are sound conditionals. Appendix B's no-go ledger is
accurate against the audit. Appendix C re-presents §18.8's skeleton by
reference, so IC-13…IC-16 carry over. The two defects of the chunk are both
in **Addendum 4.A** (Appendix C): the line-3542 "propagator rapidity product
is 16" is **IC-18** (established value is 4; 16 is the all-eight product),
and the addendum contains **two internal contradictions** against the
manuscript's own no-go ledger (a "Theorem" of the C8↔octant correspondence
vs NO-GO B1; a stated DG "bypass" vs §19.3/NO-GO B2). Appendix A's status
ledger is largely fair but **overstates 5 EXACT rows** relative to the
audit's findings.

## Book 19 §§19.1–19.7 — per-claim verdicts

- **§19.1 (UV footprint classification, self-label CONDITIONAL):** the
  exclusion math verifies — cos(4·22.5°) = cos(90°) = 0 (CP); the
  survive/exclude table is internally consistent (CP). The survival
  criterion (non-zero at E contacts) is a physical choice, not derived —
  the CONDITIONAL label is honest (MA).
- **§19.2 (uniform-action premise, OPEN):** "k₀⁰ = 1 only if k₀ multiplies
  the complete relevant microscopic action uniformly" is a sound
  conditional (CP); "The PCBF relation alone does not establish this
  premise" is honest (CP).
- **§19.3 (DG engagement, CONTESTED):** the theorem characterization
  ("applies to any real or complex form of E₈; if SM gauge group and Lorentz
  group embed, fermions must be real or vector-like") was verified against
  the arXiv:0905.2658 abstract on 2026-09-19 (ST). "A proposal under
  investigation, not a proven evasion" + CONTESTED is honest (CP).
- **§19.4 (Airy/Bessel, self-label "J₀ EXACT; jinc CONDITIONAL; Airy
  CONDITIONAL"):** the jinc/Airy conditionality is honestly tied to the
  stated premises (uniform Euclidean disk measure) (CP). The "J₀ EXACT"
  label is the manuscript's own word — the rotational-averaging inheritance
  was not audited in chunks 1–4 (Vol-III/bridge material), so it is MA
  (unverified here), not an audit verdict.
- **§19.5 (Δ_op, OPEN):** "No physical promotion is authorized. Δ_op(Volume
  IV) = ∅." — honest and consistent with the entire audit (CP).
- **§19.6 (falsifiability, STRUCTURAL):** all three criteria are sound
  logical conditionals (R⊥≠0 unabsorbed by T; Z₂-parity-breaching
  cross-terms; ζ_parent couplings vs electroweak precision bounds) (CP).
  Consistent with Addendum item 9 (CP).
- **§19.7 (gate table):** 5 rows — UV footprint selection OPEN, uniform-action
  premise OPEN, DG engagement CONTESTED, Airy/Bessel inheritance
  CONDITIONAL, Δ_op population OPEN — all match Appendix A (CP).

## The line-3542 tension — RESOLVED as IC-18

Exact text (line 3542, Addendum 4.A item 5, "Dominant Function and
Rapidity"):

> "At the four spatial decay octants, the dominant trigonometric envelope
> takes the same value. Its product over the four decay octants is 638.78.
> This factors out of S_F, preserving field-redefinition invariance. The
> propagator rapidity product is 16, assigned to ζ_parent."

Sub-claim verdicts:

1. **"Its product over the four decay octants is 638.78"** — NC ✓.
   V_E⁴ = 638.7823 (recomputed). This is the fourth power of the E-contact
   dominant value, consistent with chunk-1/chunk-2.
2. **"This factors out of S_F, preserving field-redefinition invariance"**
   — MA (unsupported manuscript assertion), with explicit conflicts: no
   derivation exists in v1; it contradicts §17.3.5's honest "its role in the
   Clifford contraction remains to be determined" (line 623); the
   §17.18.6.4 stripped list (line 1853) contains no V_E / dominant-function
   term; "field-redefinition invariance" appears exactly once in v1 (line
   3542) and is never defined or proved. Not IC: S_F is uncomputed, so no
   established result is contradicted.
3. **"The propagator rapidity product is 16"** — **IC-18** (incorrect as
   stated). The established propagator cosh product is (√2)⁴ = 4 (§17.3.4,
   §17.7.2, §17.18.9.3; chunk-1 CP). The value 16 matches the ALL-EIGHT
   product (√2)⁸. Book 17's own terminology forecloses the charitable
   all-eight reading: line 765 says "the total rapidity product is 16, not
   4", and line 771 says "The ancestry count includes only the E contact
   rapidity product (4), not the propagator rapidity product" — i.e. v1
   distinguishes "propagator rapidity product" from the "total rapidity
   product" of 16. As written, the value is wrong; no textual support exists
   for the alternative reading.
4. **"assigned to ζ_parent"** — CP for the agreement: the assignment matches
   §17.5.3's resolution (propagator cosh factors belong to ζ_parent, excluded
   from the stripped response; sweep-verified). The established value so
   assigned is 4, not 16.

Net: the ζ_parent gate keeps its assignment (propagator factors → ζ_parent)
with the corrected value 4; the "16" is a mislabeled all-eight product.

## Appendix A — status-ledger cross-check (43 rows)

Section sizes verified: EXACT 13 / STRUCTURAL IDENTIFICATION 3 /
CONDITIONAL 4 / OPEN 12 / CONTESTED 1 / CLOSED–NO-GO 10.

| Row (ledger label) | Cross-check |
|---|---|
| Harmonic carrier identity (EXACT) | chunk-1 CP — fair |
| Corrected imbalance formula (EXACT) | chunk-1 CP — fair |
| Elliptic carrier relation (EXACT) | chunk-1 CP — fair |
| Octant table (EXACT) | chunk-1 CP — fair |
| Three-bit code (EXACT) | chunk-1 CP — fair |
| 2:1 elliptic map (EXACT) | chunk-1 CP — fair; carries IC-1 caveat (ε-sheet wording) |
| Rapidity values and products (EXACT) | chunk-1 CP — fair for the Book-17 values; carries IC-2 caveat. NOTE: read as covering Addendum item 5 it is contradicted by IC-18 |
| Dominant function values (EXACT) | chunk-1 NC + chunk-2 SC — fair for the values; carries IC-2 caveat (printed §17.3.5 radical) |
| Four-contact magnitude (EXACT) | **FLAG-A1:** overstates — per-contact 1/4 is archive-sourced (MA); its relation to the certified 1/2 projection coefficient is OPEN per Tier 3.1's own warning. Arithmetic CP; input not established. Qualifier missing |
| Wick sign (EXACT) | **FLAG-A2:** overstates — σ_Wick^(t) = −1 not derived anywhere in v1; "(from archive)" qualifier dropped (chunks 2–3 provenance notes). Not independently verified |
| Graded-connection rigidity theorem λ = ±1 (EXACT) | **FLAG-A3:** unverifiable by this audit — bridge-essay §3.2 content, logged unaudited in chunk 2; Vol I–III coverage not established |
| Reduced-matrix-element firewall (EXACT) | **FLAG-A4:** category error — a firewall is a methodological principle (AX), not a proved result; audit treats it as sound, not as a theorem |
| Ancestry criterion (EXACT) | **FLAG-A5:** overstates — contradicts the manuscript's own labels: §17.5.1 CONDITIONAL, §17.5.2 CONDITIONAL on the uniform-action premise, §19.2 premise OPEN |
| C8 ↔ octant correspondence (STRUCTURAL ID) | chunk-1 honest label — fair |
| Four-contact magnitude origin (STRUCTURAL ID) | matches §17.8 EXPLANATORY — fair |
| Veronese condition at octant boundaries (STRUCTURAL ID) | **FLAG-A6:** bridge-essay §1.4 material, logged unaudited — unverified by this audit; soft label does not overclaim |
| Quasi-linear parent magnitude k₀ = β²/(2α) (CONDITIONAL) | **FLAG-A7:** Book-16/bridge import, unaudited — unverified; CONDITIONAL is a fair soft label |
| Functional form 1/S = cosh w (CONDITIONAL) | **FLAG-A8:** bridge import, unaudited — unverified; CONDITIONAL is a fair soft label |
| UV footprint classification (CONDITIONAL) | matches §19.1 — fair |
| Airy/Bessel inheritance (CONDITIONAL) | matches §19.4 — fair |
| C3/C4 forcing (OPEN) | fair |
| S_F numerical value (OPEN) | fair |
| N₁₈₂₀ (OPEN) | fair |
| ζ_parent (k₀ power) (OPEN) | fair |
| η₋₄ (UV selection) (OPEN) | fair |
| Uniform-action premise (OPEN) | fair |
| Parent-action selection (OPEN) | fair |
| Cl(16) gamma matrices (OPEN) | fair |
| 1820 projector (OPEN) | fair |
| 120 embedding (OPEN) | fair |
| 54 projector (OPEN) | fair |
| Δ_op population (OPEN) | fair |
| Distler–Garibaldi evasion (CONTESTED) | matches §19.3 — fair |
| Representation search for physical 54 (CLOSED) | present as stated; Vol-III-preserved, not re-verified |
| Raw/exchange Φ₁ as physical-135 source (CLOSED) | present as stated; not re-verified |
| Generate y₂ from neutral reduced dynamics (CLOSED) | present as stated; not re-verified |
| Internal 120 as determinant character source (CLOSED) | present as stated; not re-verified |
| One-body Saw imbalance Q as C8 defect (CLOSED) | present as stated; not re-verified |
| qSaw labels alone as crossing discriminator (CLOSED) | present as stated; not re-verified |
| Scalar m₀ ≠ m₂ as direct C8 defect origin (CLOSED) | present as stated; not re-verified |
| Common four-contact magnitude as orientation origin (CLOSED) | present as stated; not re-verified |
| Cancel isolated m₂⁻⁴ with other crossing (CLOSED) | present as stated; not re-verified |
| Paired harmonic, B-localized, O-localized UV footprints (CLOSED) | exclusion logic audited CP — fair |

No OPEN/CONDITIONAL/CONTESTED/CLOSED row contradicts the audit. Five EXACT
rows overstate (FLAG-A1…A5); three rows are unverified-but-softly-labeled
(FLAG-A6…A8).

## Appendix B — no-go ledger: verified accurate

- **B1** ("C8 ↔ octant correspondence is not a theorem; C3/C4 OPEN"):
  accurate — matches chunk-1's honest structural-identification verdict (CP).
- **B2** ("The Distler–Garibaldi theorem is not evaded… candidate, not a
  resolution"): accurate — matches §19.3 (CP).
- **B3** ("The uniform-action premise is not established"): accurate —
  matches §19.2 (CP).
- **B4** ("The Airy transition is not established. Only J₀ is
  unconditional"): accurate — matches §19.4 (CP).

## Appendix C — codebase skeleton: defects carry over by reference

Line 3423: "The Wolfram code from §18.8 is the primary computational
artifact." — Appendix C presents no new code; it re-presents the §18.8
skeleton **by reference**. All four defects therefore carry over:

- **IC-13** (recurs IC-8): line 3168
  `P1820 = NullSpace[Transpose[{traceVector}]];` yields {} (nullity 0);
  intended reading gives 8255 ≠ 1820; unfixable within v1 (needs P₆₄₃₅).
- **IC-14** (recurs IC-9): line 3173 KroneckerProduct of four 128×128
  matrices is 128⁴×128⁴, sandwiched by an 1820×8256 P1820 — dimensionally
  incompatible.
- **IC-15** (recurs IC-10): line 3193 `S_F = -(1/256) * S_F_raw;` then
  `nHat54 = -(Sqrt[10]/1536) * S_F * m2^(-4);` counts the contact factor
  twice, violating §17.18.10's "counted exactly once" regression
  requirement.
- **IC-16** (recurs IC-11): line 3189 sums `wickSign * contraction[...]`
  but `wickSign` is never assigned in the skeleton.

(IC-17, the §18.2 gamma-template 256×256-vs-128×128 defect, is not in the
skeleton but is its gamma input; both inputs the bottleneck names — Cl(16)
gammas and the 1820 projector — are honestly OPEN per Appendix A.)

## Addendum 4.A — per-item verdicts

Header: "Status ledger. Δ_op = ∅. Construction exact; numerical closure
open until Module 11 executes." — Δ_op = ∅ and numerical-closure-open are
honest (CP). ("Construction exact" sits uneasily with the four skeleton
defects above, but as a self-label it is read as the algebraic
construction, which chunks 3–4 verified.)

1. **3875 correction:** 135+1820+1920 = 3875 (CP); the erroneous table
   248+135+1820+1920+54 = 4177 (CP); the branching content is standard
   (ST). "This insert supersedes that table" is editorial (CP).
2. **54 witness:** dim 54 = (10×11)/2 − 1 = 54 (CP); T diagonal/traceless
   with fixed norm is chunk-2 CP; Q_F = (6/5)T is posited (MA). NOTE-2: "The
   1820 … projects onto the 54 of SO(10)" is stated as fact while §18.5
   lists the explicit Clebsch–Gordan map P_{1820→54} as a missing input
   (line 3091); P₅₄ location (135 vs 1820) remains unreconciled — MA.
3. **S_F:** NOTE-3 (organization, high severity) — "S_F" is used for three
   different objects in one section: the scalar trace
   S_F = Tr₁₈₂₀(EBEOEBEO); the operator sandwiched as
   M₅₄ = P₁₈₂₀→₅₄ S_F P₁₈₂₀→₅₄†; and the extracted scalar
   S_F = Tr(M₅₄ T)/Tr(T²) — none reconciled with the defined stripped scalar
   S_F := ⟨Q_F, R̃^t_2222⟩ = 3a₂₂₂₂ (§17.18.6.5 line 1863, §18.6 line 3115).
   Contact normalization and Wick sign are listed as bullets but not applied
   to the trace, so dressed-vs-stripped is ambiguous — against §17.18.10's
   "counted exactly once" requirement. "Require R⊥ = 0…" is consistent with
   §19.6 criterion 1 (CP).
4. **N₁₈₂₀:** FLAG-N4 (overstatement) — "isolates N₁₈₂₀ as an exact discrete
   graph invariant" contradicts Appendix A's N₁₈₂₀ OPEN row and §18.7's
   honest OPEN; the B/O per-factors are unspecified ("each B contributes a
   factor" — no values) and "the absorbed witness norm" is undefined (MA).
5. **Dominant function and rapidity:** see line-3542 verdict above
   (638.78 NC; factorization MA with conflicts; "propagator rapidity product
   is 16" IC-18; ζ_parent assignment CP).
6. **C8↔octant "Theorem":** **CONTR-1** (internal contradiction) — states as
   a theorem with "Proof sketch. ∎" that EBEOEBEO is "the unique cyclic word
   preserving parity and boundary continuity," directly contradicting the
   manuscript's own Appendix B NO-GO B1 ("C8 ↔ octant correspondence is not
   a theorem. The C3/C4 forcing question remains OPEN"). The sketch assumes
   E contacts "can only reside at zero-crossing decay nodes" and propagation
   "must alternate B and O" — neither forced in v1; C3/C4 forcing is the
   manuscript's own "immediate structural gate." The octant table itself
   (angles/roles) is consistent with chunks 1–2 (CP).
7. **UV footprint selection:** table consistent with §19.1 (paired excluded
   via cos(90°) = 0) (CP).
8. **Foundational alignment:** **CONTR-2** (internal contradiction) — "The
   real-form E8(−24) framework bypasses this by using: E8(−24) ⊃ A1 + G2 +
   C3 … Minimal left ideals of Cl(8) yield three chiral generations without
   mirror fermions" states the DG bypass as fact, contradicting §19.3 ("not
   a proven evasion") and NO-GO B2 ("not evaded… candidate, not a
   resolution"). The mechanism is at best a proposal (MA); E8(−24) host
   itself is MA per the Vol-III ledger.
9. **Falsifiability:** consistent with §19.6 (CP).
10. **Execution roadmap:** 4 tasks all OPEN, consistent with Appendix A (CP).
11. **Wolfram implementation note:** NOTE-11 — claims about the circulated
    notebook (missing Modules 1–3; slow Module 9) cannot be checked; the
    notebook is not in the audit corpus (MA, unverifiable).
12. **References:** 0905.2658, 2404.18938v2 ("On possible embeddings of the
    standard model of particle physics and gravity in E8"), 2210.06029v1
    ("Chirality in an E8 model of elementary particles") all exist with
    E8-relevant titles (verified via arXiv API 2026-09-19) (CP);
    1411.4317v4 exists but is "Large values of cusp forms on GL(n)"
    [math.NT] — relevance unclear, logged.

FRONTIER SUMMARY's three immediate gates (calculable: Cl(16) gammas + 1820
projector; structural: C3/C4 forcing; conditional: uniform-action premise)
are consistent with Appendix A (CP). Addendum closing: "No empirical
promotion is authorized. Δ_op(Volume IV) = ∅." (CP).

## Terminology notes

- **Flatwave:** no occurrence of "Flatwave"/"FlatWave" anywhere in Book 19
  or the appendices (lines 3221–3637, verified by grep). The CL-002
  (Books 2–3) "FlatWave = sgn(sin 2x)" vs §17.1.4 "Flatwave = 1/urx+1/uxp"
  collision does not recur in chunk 5 — still unresolved at volume level.
- **Title duplication** (§17.18 vs Book 18, "Explicit Construction of the C8
  Contraction Module") — unresolved, carried to volume close.
- **S_F notation collision** (Addendum item 3, NOTE-3 above) — new in this
  chunk.

## v2 / v3 / unsigned-report contradictions touched (labeled, not findings)

- **VX-1:** v3 draft line 118 claims S_F = Tr₁₈₂₀(EBEOEBEO) = 0.48958371 as a
  computed value — contradicts v1 Appendix A (S_F OPEN), §19.5 (Δ_op = ∅),
  and the addendum's "numerical closure open until Module 11 executes."
- **VX-2:** v3 draft line 120 claims N₁₈₂₀ = 3 "exactly calculated" —
  contradicts v1 Appendix A (N₁₈₂₀ OPEN) and §18.7.
- **VX-3:** the unsigned report claims "Status: MASTER CERTIFICATION
  COMPLETE" (line 54) for Books 17–19 — contradicts v1 §19.5 ("No physical
  promotion is authorized. Δ_op(Volume IV) = ∅."), Appendix A's 12 OPEN
  rows, and the addendum's open numerical closure.
- (v3 line 223's retirement of prior snapshots is the previously logged
  authority conflict — Kit directed v1-first auditing.)

## Open gates at volume close

S_F numerical value; N₁₈₂₀ counting (incl. the open 1/2→1/4 per-contact
relation); ζ_parent (uniform-action premise; propagator-factor value now
corrected to 4 per §17.5.3, assignment intact); η₋₄ (UV footprint
selection); c_ord / K_parent values; P₅₄ location (135 vs 1820);
C3/C4 forcing; DG engagement (contested); parent-action selection;
Cl(16) gamma matrices; 1820 projector; 120 embedding; 54 projector;
Δ_op population. Δ_op(Volume IV) = ∅ — no physical promotion authorized.

## Not audited in this chunk (scope boundaries)

- Inter-chunk gap lines 411–776: covered by chunk-3 sweep (no new
  discrepancies).
- Bridge-essay identities (§1.3–§1.5, §3.1–§3.2): logged, not audited
  (chunks 2–3); three Appendix-A rows depending on them are flagged
  accordingly (FLAG-A3, A6–A8).
- The circulated Wolfram notebook (Addendum item 11): not in the corpus.

---

## VOLUME CLOSE — totals across all five chunks

| Chunk | Assertions passed | Failed | Timeout | CP | NC | SC | ST | MA | AX | IC findings | IN |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 (§§17.1–17.5) | 116 | 0 | none | 107 | 9 | – | – | – | – | 3 (IC-1…IC-3) | 0 |
| 2 (§§17.6–17.9) | 58 | 0 | none | 54 | 2 | 1 | – | 1 | – | 1 (IC-4) | 0 |
| 3 (§17.18) | 85 | 0 | none | 83 | 2 | – | – | – | – | 7 (IC-5…IC-11) | 3 |
| 4 (Book 18) | 40 | 0 | none | 31 | 1 | – | – | – | – | 6 (IC-12…IC-17; 8 at assertion level) | 0 |
| 5 (Book 19 + App. A–C) | 108 | 0 | none | 73 | 1 | – | 2 | 31 | 1 | 1 new (IC-18); IC-13…IC-16 carried | 0 |
| **Total** | **407** | **0** | **none** | **348** | **15** | **1** | **2** | **32** | **1** | **18 distinct (IC-1…IC-18)** | **3** |

Distinct incorrect-as-stated findings (18): IC-1 ε/sheet wording; IC-2
§17.3.5 wrong radical; IC-3 reciprocal-of-product wording; IC-4 cos(4x)
zeroes at midpoints not boundaries; IC-5 "four O propagators" (2 exist);
IC-6/IC-12 120-in-Sym²(128) (recurs in Book 18); IC-7 "135 is the adjoint
of SO(16)" (adjoint is 120); IC-8/IC-13 skeleton 1820-basis NullSpace defect
(recurs); IC-9/IC-14 skeleton KroneckerProduct dimension defect (recurs);
IC-10/IC-15 skeleton double-counted −(1/256) (recurs); IC-11/IC-16 skeleton
`wickSign` undefined (recurs); IC-17 §18.2 gamma template 256×256 vs
required 128×128; IC-18 line-3542 "propagator rapidity product is 16"
(established: 4).

Incomplete/blocked computations (3, all chunk 3): IN-1 Frobenius-norm
recomputation (needs explicit γ_i, B, Π_− + parent-action conventions);
IN-2 explicit 1820 projector matrix (blocked at P₆₄₃₅); IN-3 S_F numerical
value (OPEN — manuscript's own label).

New finding classes in chunk 5: 2 internal contradictions (CONTR-1: Addendum
item-6 "Theorem" vs NO-GO B1; CONTR-2: Addendum item-8 DG "bypass" vs
§19.3/NO-GO B2); 8 Appendix-A ledger flags (5 EXACT overstatements, 3
unverified-but-softly-labeled rows); 1 N₁₈₂₀ overstatement (Addendum item 4);
2 organization notes (S_F notation triple-use; 1820→54 projection stated
while map is a missing input); 1 unverifiable (notebook claims).

Unresolved at volume close: title duplication (§17.18 vs Book 18);
Flatwave terminology collision (CL-002 vs §17.1.4); P₅₄ location (135 vs
1820); N₁₈₂₀ 1/2→1/4 gap; 638.78 role in S_F; dangling "§17.11" reference
(line 2077); v2/v3/report contradictions (V4 chain OI-24…OI-29).

**Bottom line:** the volume's checkable mathematics verifies (348 CP
assertions, 0 failures, no timeouts across all five chunks); the
manuscript's open gates are honestly labeled with the exceptions recorded
above (5 overstated EXACT rows in its own status ledger, 2 addendum
passages contradicting its own no-go ledger, 1 new incorrect value at line
3542). Δ_op(Volume IV) = ∅: the audit confirms no physical promotion is
established anywhere in the volume — which is also what the manuscript
itself says.
