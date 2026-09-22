# LEDGER — Volume IV v1, chunk 1: §§17.1–17.5 (doc lines 2771–2998 + stub 150–410)

Script: `~/workspace/vol4/book17/audit_17_1.py`
Run: 2026-09-19. **116 assertions passed, 0 failed, no timeout.**

Published ledger: **CP 107 · NC 9 · IC 3** (incorrect-as-stated findings below).
No ST / MA / AX / IN in this chunk beyond terminology notes.

## Verified (CP)

- **§17.1.1** Harmonic carrier identity `sin(2x)/4 = 1/(urx+uxp)`: proved in all
  four quadrants. Key lemma (all quadrants): `srx − 1/srx = 2c/s`,
  `cxp − 1/cxp = 2s/c`, so `urx + uxp = 2/(sc) = 4/sin(2x)`.
  The printed proof ("combining over the common denominator cxp·srx − 1") is a
  sketch; the quadrant sign analysis is doing the real work. Domain is the
  common domain sin x ≠ 0, cos x ≠ 0 (stated in the stub, implied in the full
  version). `srx, cxp > 0` wherever defined, so all reciprocals are safe.
- **§17.1.2** Imbalance formula: `K₂ = 2cos(2x)/(sc)`, `D₂ = 2/(sc)`,
  `K₂/(2D₂) = cos(2x)/2`. Exact in all quadrants.
- **§17.1.3** Elliptic carrier `V_R² + 4H² = 1/4`: exact (also via the stub's
  route `D₂² − K₂² = 16`, verified).
- **§17.1.4 (octant table)**: dominant/recessive ordering proved per octant
  pair via exact sign factorizations
  (e.g. oct 1–2: `srx−cxp = (c−s)(1+c+s)/(sc)`);
  phase column = sgn(sin 2x) at all eight midpoints; Decay/Growth proved via
  exact derivative-sign analysis on each octant (8 derivative formulae
  verified symbolically; signs elementary on each interval).
  Verified structural observation: the "active pair" members are exactly the
  two primitives > 1 in each octant; the inactive pair are both in (0,1).
  Exact proof, 24 new script assertions: with t = tan(x/2),
  sin x = 2t/(1+t²), cos x = (1−t²)/(1+t²) (both verified exactly), and
  tan(x/2) strictly increasing on each octant, t ranges over exact open
  intervals — oct1 (0,√2−1), oct2 (√2−1,1), oct3 (1,√2+1), oct4 (√2+1,∞),
  oct5 (−∞,−(√2+1)), oct6 (−(√2+1),−1), oct7 (−1,−(√2−1)), oct8 (−(√2−1),0)
  (boundary values tan(kπ/8) verified exactly; 0 and ±∞ are limits).
  The script verifies exactly, per octant, srx−1 and cxp−1 in factored
  t-form — 16 identities, e.g. oct1: srx−1 = (1−t)/t, cxp−1 = 2t/(1−t);
  oct3: srx−1 = (1−t)/t, cxp−1 = −2/(t+1); oct5: srx−1 = −(t+1),
  cxp−1 = −2/(t+1); oct7: srx−1 = −(t+1), cxp−1 = 2t/(1−t) (octant pairs
  sharing a quadrant verify the same identity, stated per octant for
  explicitness). Constant facts 0 < √2−1 < 1 and √2+1 > 1 verified exactly
  as (√2)² = 2 > 1 and (√2)² = 2 < 4 (√2 > 0 principal root). Signs are then
  elementary on each interval — every factor is linear with roots in
  {0, ±1}, none inside the corresponding open t-interval: oct1,2:
  (1−t)/t > 0 and 2t/(1−t) > 0, so srx > 1, cxp > 1 (active pair (srx,cxp)
  per the manuscript table); oct3,4: (1−t)/t < 0, −2/(t+1) < 0 with
  srx,cxp > 0, so srx,cxp ∈ (0,1), i.e. crx = 1/cxp > 1, sxp = 1/srx > 1
  (active pair (crx,sxp)); oct5,6: −(t+1) > 0, −2/(t+1) > 0, so srx > 1,
  cxp > 1; oct7,8: −(t+1) < 0, 2t/(1−t) < 0 with srx,cxp > 0, so
  srx,cxp ∈ (0,1), i.e. crx > 1, sxp > 1. Exactly two primitives exceed 1
  on each open octant: the active pair.
- **§17.1.5/17.1.6 (three-bit code)**: the 8 codes are all of Z₂³; every
  octant decodes correctly under (half-quadrant, sgn cos 2x, sgn cos x).
- **Stub §17.1.4 (Flatwave/carrier duality)**: `1/urx + 1/uxp =
  (srx+cxp)/(srx·cxp−1)` and `Flatwave·H = 1/(urx·uxp)` are pure algebra,
  exact. (Wording note below.)
- **§17.2**: the map is 2:1 (`V_R, H` π-periodic), ellipse traced twice; the
  four midpoint carrier values `(±√2/4, ±√2/8)` exact.
- **§17.3**: `w₀ = ln(1+√2)`, `sinh w₀ = 1`, `cosh w₀ = √2` exact;
  all eight midpoint rapidities `±w₀` exact; products `(√2)⁴ = 4`,
  `(√2)⁸ = 16` exact; rapidity sums 0 at every level exact;
  `dw/dx = −2/sin(2x) = −2εcosh w` exact (per-quadrant symbolic).
- **§17.4**: the cyclic word is exactly (E,B,E,O)×2; E sits on the four decay
  octants, B on the two growth octants with ε=+1, O on the two growth
  octants with ε=−1 — tables internally consistent. The manuscript is
  explicit that this is STRUCTURAL IDENTIFICATION and that C3/C4 forcing is
  OPEN: the status label is honest.
- **§17.5**: gate list; no mathematical claims.

## Numerical checks (NC)

- Dense-grid tripwires for §§17.1.1–17.1.2 (relative error < 1e-9 away from
  poles; pole neighborhoods excluded). Disclosure: an initial absolute-error
  dense-grid test FAILED near the poles — both sides blow up like 1/sin 2x,
  so absolute error there measures floating-point cancellation noise, not
  truth. It was replaced by relative-error tripwires with pole neighborhoods
  excluded, after the exact symbolic quadrant proofs above had already
  passed. The committed script contains only the relative-error version.
- `dw/dx` finite-difference tripwire (rel err 6.1e-10).
- `V_E = √(4+2√2)+1+√2 ≈ 5.0273`, `V_E⁴ ≈ 638.78` (manuscript: 638.78 /
  638.7 in the two copies — consistent rounding).
- The four E-contact dominant values are equal (≈ 5.02734).

## Incorrect as stated (IC)

1. **§17.2, "ε records the sheet."** ε = sgn(sin 2x) is invariant under the
   deck transformation x → x+π (verified: sin 2(x+π) = sin 2x), so it
   cannot record which sheet of the 2:1 cover a point came from. ε records
   upper vs. lower half of the ellipse. The 2:1 claim itself is correct.
2. **§17.3.5 (continued-calc block): the printed radical for crx(112.5°).**
   `1/(2/√(2+√2) + (√2−1))` evaluates to ≈ 0.6682, not ≈ 5.027. The correct
   value is `1/cxp(112.5°) = √(4+2√2)+1+√2 ≈ 5.0273` (verified); the final
   equality of the four E-contact values is correct — only the printed
   intermediate radical is wrong (looks like 67.5°/112.5° values mixed).
3. **Stub §17.1.4 wording:** "Their product is the reciprocal of the
   geometric mean." `Flatwave·H = 1/(urx·uxp)` is the reciprocal of the
   *product*, not of the geometric mean `1/√(urx·uxp)`. Minor.

## Terminology / organization notes (not errors)

- "Active pair", "dominant/recessive", "Decay/Growth" are never formally
  defined, but their extensions are fully fixed by the table and every entry
  verifies exactly (see above). Terminology: MA; content: CP.
- The stub (lines 150–410) and the full §17.1 (lines 2771–2998) are
  consistent; the stub additionally carries 17.1.4 Flatwave duality,
  FIREWALLS, NEGATIVE RESULTS (N17.1–N17.5), and the opening gate list.
  The full version renumbers (its 17.1.4 = octant table, 17.1.5 = code).
- The manuscript's own firewalls are epistemically sound: Δ_op(Book 17) = ∅
  is asserted as a status claim (MA), the C8↔octant correspondence is
  labeled structural rather than derived, and S_F / N₁₈₂₀ / ζ_parent / η₋₄
  / C3-C4 forcing are all admitted OPEN.

## Not yet touched (later chunks)

§§17.6–17.9 (continued calc), §17.18 (C8 contraction module), Book 18,
Book 19. The wrong-radical IC-2 sits in §17.3.5, which belongs to the
continued-calc block — flagged here since it concerns §17.3 content.

## Addendum (2026-09-19): Flatwave on Q1/Q3

Verified structural observation, not claimed by the manuscript: with
`Flatwave = 1/urx + 1/uxp`, we have **Flatwave ≡ 1 exactly on quadrants 1
and 3** (where sin x and cos x share sign) — proved symbolically from the
quadrant forms. On quadrants 2 and 4 it is not identically 1 (numeric
deviation up to 2.0 near the poles). CP on Q1/Q3; NC (counterexample
points) on Q2/Q4.

Terminology collision flagged for the Master Ledger: CL-002 defines
"FlatWave = sgn(sin 2x) on raw domain" (Books 2–3), while Volume IV §17.1.4
defines "Flatwave(x) = 1/urx(x) + 1/uxp(x)". Same name, different
definitions in different books — needs disambiguation, not a correction.
