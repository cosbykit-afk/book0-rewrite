# LEDGER — Volume IV v1, chunk 2: §§17.6–17.9 (doc lines 777–990)

Script: `~/workspace/vol4/book17/audit_17_6.py`
Run: 2026-09-19. **58 assertions passed, 0 failed, no timeout.**
All computations closed-form (total runtime ~1.3 s); per-computation budget
never binding.

Assertion tally: **CP 54 · SC 1 · NC 2 · MA 1**. Claim-level verdicts below;
**one new incorrect-as-stated finding (IC-4)**; no IN (nothing timed out or
went unfinished).

Upstream dependencies (chunk 1, not re-derived): primitives srx/cxp/sxp/crx;
C8 cyclic word (E,B,E,O)×2 with E on decay octants 1,3,5,7, B on growth
octants 2,6 (ε=+1), O on growth octants 4,8 (ε=−1); E contacts at
22.5°/112.5°/202.5°/292.5°; w₀=ln(1+√2), cosh w₀=√2; E-contact rapidity
product (√2)⁴=4; V_E=√(4+2√2)+1+√2; IC-1/IC-2/IC-3 carried forward where
they touch this chunk (noted, not re-counted).

## Verified (CP/SC/NC)

### §17.6.1 — the five footprint types
- Paired footprint cos(4x): even under x→x+π (CP); π/2 is a period, π/4 is
  not (CP) — the "Period π/2 (quadrupole)" bullet is exact, and minimality
  follows since any period T of cos(4x) satisfies 4T∈2πℤ.
- δ-footprint evenness under the 2:1 kernel reduces to contact-set
  invariance, which holds: E {22.5,112.5,202.5,292.5}, B {67.5,247.5},
  O {157.5,337.5} are each invariant under +180° (CP). Balanced footprint 1
  trivially invariant (CP).
- C8 shift by 4 = 4×45° = 180° = the 2:1 kernel map (CP): two of the
  "three Z₂ symmetries" coincide as maps on x (see terminology note).
- Extra (not claimed): the E-contact set is invariant under +90° (CP) —
  the E-localized footprint actually has Z₄ symmetry, stronger than claimed.
- E contacts are exactly the decay-octant midpoints {1,3,5,7}, strictly
  interior to their octants (CP) — §17.6.3's "non-zero precisely at the
  four decay octants" holds in the distributional sense.

### §17.6.2 — the paired footprint
- cos(4·22.5°)=0 exactly (CP); cos(4x)=0 at **all eight** octant midpoints
  22.5°+k·45° (CP) — stronger than the manuscript's E-contacts-only
  statement. The exclusion note ("if the UV datum must be non-zero at the
  E contacts, the paired footprint is excluded") is logically sound given
  the true zero set; it also excludes paired on B/O-nonvanishing grounds.
- y₂ = η₀·cos(4x)·ζ_parent·n̂₅₄ is exactly the η₋₄=η₀cos(4x) substitution
  into the three-way-separation ansatz (MA — no independent content beyond
  the ansatz; the charge resides in η₀ by hypothesis).

### §17.7.1 — what remains
- S_F = ⟨Q_F, a₂₂₂₂T⟩ = 3a₂₂₂₂ follows from Q_F=(6/5)T and ‖T‖²=5/2
  ((6/5)(5/2)=3) (CP); ⟨Q_F,R_perp⟩=(6/5)⟨T,R_perp⟩=0 from the stated
  decomposition (CP). The four missing pieces are listed as OPEN — honest.

### §17.7.2 — what is known
- T=diag(1,1,−1/4,…): the manuscript's ‖T‖²=5/2 **forces** the 10×10
  reading (eight −1/4 entries: 2+n/16=5/2 → n=8) (CP). Then traceless
  (1+1−8/4=0) (CP) and ‖T‖²=5/2 (CP) are exact. (v1 never writes "eight"
  or "10×10"; the 54 = traceless symmetric square of the SO(10) 10 at
  lines 2271/3083 supports this reading, and the norm value disambiguates.)
- ‖Q_F‖²=(6/5)²·(5/2)=18/5 (CP); four-contact factor (1/4)⁴=1/256 (CP);
  E-contact and propagator rapidity products (√2)⁴=4 (CP).
- srx(22.5°)=√(4+2√2)+1+√2 **exactly** (SC — sympy simplification to 0).
  V_E⁴=638.782272… ≈638.78 (NC). The §17.7.2 table's "≈638.7" is a
  truncation of 638.7823, not a rounding (NC; presentation note below).

### §17.7.3 — the conversion chain ("EXACT as definitions")
- Internal algebra closes: S_F=3a, a=(6/5)c ⇒ S_F=(18/5)c (CP);
  c_ord=5S_F/18 inverts it (CP); the three n̂₅₄ forms
  −(√10/1536)S_F = −(√10/512)a₂₂₂₂ = −(3√10/1280)c_ord (times m₂⁻⁴)
  coincide under S_F=3a, a=(6/5)c (CP). The defined content — the
  −(√10/1536) prefactor (Wick −1 × 1/256 × √10/6), a₂₂₂₂=(6/5)c_ord —
  is MA (see below). "The numerical value of S_F remains OPEN" — honest.

### §17.7.4 — bounds and estimates ("OPEN")
- Arithmetic exact: (1/256)(18/5)(4)=0.05625≈0.056 (CP). The bound's
  *form* is heuristic — the manuscript says so itself ("This is not a
  calculation; it is a dimensional estimate") — so the OPEN label is
  honest. No derivation of the form is given in v1.

### §17.8 cross-check spot-verifications (17.2.2, 17.2.3)
- All eight 17.2.2 octant→ellipse rows verify: (V_R,H,ε) at the midpoints
  (CP); the four ellipse points are concyclic at |A|=√10/8≈0.3953 (CP).
- All five 17.2.3 boundary points verify by direct substitution into the
  chunk-1-proved carrier formulas (CP).

## Incorrect as stated (IC)

**IC-4 (§17.6.2, new): "Vanishes at the octant boundaries (45°, 135°,
etc.)" is false.** cos(4·45°)=cos(180°)=−1, cos(4·135°)=cos(540°)=−1,
cos(0°)=+1 (all CP). cos(4x) vanishes at the octant **midpoints**
(22.5°+k·45°), not the boundaries. The manuscript contradicts itself:
bullet 2 claims vanishing at boundaries while bullet 5 correctly states
zero at the E contacts (which are midpoints, cos(4·22.5°)=cos90°=0).
The exclusion logic is unaffected (it rests on the true zero set), but
the bullet as printed is wrong — it reads like a boundaries/midpoints
mix-up.

Carried forward (touching this chunk, not re-counted):
- IC-1 recurs verbatim in the continued-calc §17.2.1 (line ~432):
  "The orientation sign ε = sgn(sin 2x) records the sheet." Same finding
  as chunk 1 — ε is deck-invariant, records ellipse halves. Not a new IC.
- IC-2 caveat attaches to the §17.8 row "Dominant function values EXACT":
  the *values* are exact (SC above; chunk-1 NC), but the printed §17.3.5
  intermediate radical for crx(112.5°) was wrong. The summary row does not
  claim the derivation, only the values — label fair with this caveat.

## Manuscript assertions / assumptions (MA/AX — not verified here)

- **Code-group evenness (17.6.1): unverifiable as stated.** The "code
  group" is defined (lines 317, 2882) as "Z₂³ acting on the octant
  lattice" with "no physical interpretation asserted" — it is never given
  as a map on x, so "even under the code group" has no checkable meaning
  for a function Φ(x). Demonstrated ambiguity (CP): the E-support octant
  pattern {1,3,5,7} is NOT invariant under the octant transposition
  (1 2), so under the natural transitive bit-flip reading the localized
  footprints would *fail* evenness. The table's "Yes" for the code-group
  leg is therefore not earned by anything defined in v1. (Not marked IC:
  an undefined claim cannot be falsified; it is MA with an explicit gap.)
- **"Three Z₂ symmetries" redundancy:** as maps on x, the 2:1 kernel
  (x→x+π) and the C8 shift by 4 (4 octants = 180°) coincide. The list
  names two distinct x-maps at most, one of which (code group) is
  undefined as an x-map.
- **η₀ is never defined in v1** (only used: η₋₄=η₀·geometric). "All five
  carry q_F=−4 if η₀ does" is explicitly conditional and consistent with
  the UV firewall (charge is external input, not derived) — honest, but
  η₀'s charge is AX, not established.
- **"Compatible with the 1/256 contact structure" (17.6.3):** no
  compatibility criterion is defined in v1 — MA (within a CONDITIONAL
  section; not false, just undefined).
- **Q_F=(6/5)T** is posited in §17.7; its justification (the 54
  projection) lives in §17.18 — MA pending the later chunk.
- **Wick sign −1:** archive-cited. §17.8's "EXACT (from archive)" carries
  the provenance qualifier; §17.7.2's "What is known / EXACT" table lists
  "Wick sign −1" **without** it. The number is not derived anywhere in
  v1 §§17.6–17.9. Provenance note, not IC — but the qualifier should
  travel with the claim.
- **Per-contact 1/4** (behind the (1/4)⁴=1/256): posited inside the
  projected-adjoint contact construction (§17.18, not yet audited). The
  arithmetic is CP; the input is MA.
- **−(√10/1536) prefactor** in the conversion chain: definitionally
  consistent (CP above); its full derivation needs the "inherited
  invariant bilinear," which §17.7.1 lists as a missing piece — MA.

## Terminology / presentation notes (not errors)

- **638.7 vs 638.78:** V_E⁴=638.782272…. §17.3.5/§17.7.2's bridge copy
  says 638.78 (correct rounding); the §17.7.2 table says ≈638.7 — a
  truncation, not a rounding (chunk 1 called these "consistent rounding";
  corrected here: 638.78→638.7 is truncation). Exact value recorded above.
- **T's ellipsis:** "diag(1,1,−1/4,…)" never states the entry count; the
  manuscript's own ‖T‖²=5/2 forces eight −1/4's (10×10). Self-consistent
  once disambiguated; the disambiguation is doing work the text doesn't.
- **δ(x−x_E) singular vs sum:** the §17.6.1 table writes δ(x−x_E) but
  §17.6.3 defines the sum Σ_{E contacts}δ(x−x_E). Minor.
- **No "Flatwave" in §§17.6–17.9** (grep): the CL-002 vs §17.1.4
  terminology collision does not recur in this chunk.
- **Triple numbering:** Book 17 material appears under three overlapping
  schemes — stub §§17.2–17.6 (lines 384–396, summaries), continued-calc
  §§17.2–17.9 (lines 414–990), full §§17.1–17.5 (lines 2771–2998).
  The §17.8 summary rows map across these; cross-references below use
  continued-calc numbers.

## §17.8 summary-table cross-check (row → verdict)

| Row (self-label) | Cross-check |
|---|---|
| Harmonic carrier identity (EXACT) | chunk-1 CP — fair |
| Corrected imbalance formula (EXACT) | chunk-1 CP — fair |
| Elliptic carrier relation (EXACT) | chunk-1 CP — fair |
| Octant table (EXACT) | chunk-1 CP — fair |
| 3-bit code (EXACT) | chunk-1 CP — fair |
| Octant-to-ellipse mapping (EXACT) | chunk-1 §17.2 CP + this chunk re-verified all 8 rows of 17.2.2 and \|A\|=√10/8 — fair; carries IC-1 caveat (ε-sheet wording, same finding) |
| Boundary points (EXACT) | 17.2.3 (line 488, inter-chunk gap); verified here by substitution into proved formulas — fair |
| E contact rapidities (EXACT) | chunk-1 CP — fair |
| Propagator rapidities (EXACT) | chunk-1 CP — fair |
| Rapidity products (EXACT) | chunk-1 CP — fair |
| Dominant function values (EXACT) | chunk-1 NC + this-chunk SC (closed form exact) — fair for the *values*; carries IC-2 caveat (printed §17.3.5 radical wrong) |
| C8 ↔ octant correspondence (STRUCTURAL IDENTIFICATION) | chunk-1: internally consistent, honestly labeled; C3/C4 forcing OPEN — fair |
| Four-contact magnitude origin (EXPLANATORY) | arithmetic CP; per-contact 1/4 input pending §17.18; soft label doesn't overclaim — fair with dependency noted |
| Wick pairing (EXACT from archive) | provenance qualifier present — honest; NOT independently verified in chunks 1–2; qualifier missing in §17.7.2's table (note above) |
| Ancestry scenarios (CONDITIONAL) | matches §17.5 self-labels (17.5.1 CONDITIONAL; 17.5.2 CONDITIONAL on uniform-action premise); content at lines 716–752 not audited in chunks 1–2 |
| UV footprint classification (CONDITIONAL) | matches §17.6.1 self-label — fair |
| Paired footprint ansatz (CONDITIONAL) | matches §17.6.2 self-label — fair; carries IC-4 |
| S_F / N₁₈₂₀ / ζ_parent / η₋₄ (OPEN) | match v1's explicit admissions — fair |

No summary row overstates its chunk-1/chunk-2 verdict. Two rows
("Boundary points", "Ancestry scenarios") recap content from the
inter-chunk gap (lines 411–776) not systematically audited in either
chunk; their labels were checked against the source's own self-labels
plus spot-verifications here.

## §17.9 handoff

Prose only; no new mathematical claims. "The E contact rapidity product
is exactly 4" — chunk-1 CP ✓. "The Clifford half requires the explicit
ordered contraction" — OPEN, consistent with §17.7.1. "Four
projected-adjoint contacts and the two B and two O propagators into the
1820×1820→54 output" — matches the C8 word (E×4, B×2, O×2) ✓.

## Bridge essay (lines 986–1490) — logged, not audited

"Algebraic Symmetry Reduction and the Computational-Foundational Frontier
in Real-Form E₈₍₋₂₄₎ Unification (continued)": recap of Volumes I–III +
Book 17, in six parts: (1) representation-theoretic architecture (3875
decomposition, two-slot fermionic origin, qSaw determinant, C8 even scalar
shadow, four-fermion pairing); (2) C8 graph and octant decomposition;
(3) normalization cascade (transfer geometry, graded-connection rigidity
theorem, reduced-matrix-element firewall, one-witness reduction); (4)
charge firewall and UV matching (U(1)_F grading, ancestry criterion,
three-way separation, footprint classification); (5) open gates; (6)
conclusion. §4.4's footprint table is consistent with §17.6 (adds the
non-zero-at-E-contacts column; same exclusion conclusion).

Distinct mathematical claims stated as exact whose coverage by the
completed Vol I–III audits is not established from memory and which were
**not** re-verified in this chunk (out of scope per task): the qSaw
identity C²−AB=W² (§1.3); Δ_C8=(β²−αγ)/64 and the (4,2coshδ,1) evaluation
to (1/16)sinh²δ (§1.4); the Plücker relation p_u−p_t+p_s=0 (§1.5); the
graded-connection rigidity theorem λ²=1 proof sketch (§3.2). §5.4
(falsifiability) makes no mathematical claim.

## Could not resolve in this chunk (open / out-of-scope)

- Code-group evenness leg (undefined x-map) — §17.6.1.
- "Compatible with the 1/256 contact structure" criterion — §17.6.3.
- η₀'s definition and charge — assumed input (UV firewall explicit).
- Q_F=(6/5)T; per-contact 1/4; −(√10/1536) prefactor's full derivation;
  Wick sign −1's archive computation — all depend on §17.18 or the
  archive (later chunks).
- Cross-section tension for the §17.18 chunk: a later v1 section
  (~line 3542) says "The propagator rapidity product is 16, assigned to
  ζ_parent," while §17.7.2 lists "Propagator rapidity product 4" and
  §17.5.3 assigns only the propagator cosh factors (not the E-contact 4)
  to ζ_parent. Also (~line 3542): "Its product over the four decay
  octants is 638.78. This factors out of S_F" — while §17.7.4's bound
  contains no 638.78 factor. Whether these are consistent depends on
  conventions in §17.18/Book 18 — flagged, not resolved here.

## Not yet touched (later chunks)

- Inter-chunk gap lines 411–776 (continued-calc §§17.2–17.5 duplicates):
  not systematically audited in chunk 1 (which covered the full versions
  at 2771–2998 + stub 150–410) or here (spot-checks only: 17.2.2, 17.2.3,
  17.5.1–17.5.3 read for the §17.8 cross-check).
- §17.18 (C8 contraction module, from line 1492), Book 18, Book 19.
- Bridge-essay identities (§1.3–§1.5, §3.1–§3.2) per the log above.
