# validation/book9 — reconstruction note (2026-09-19)

## Status

The scripts in this directory are **RECONSTRUCTED, not original**.

The original Book 9 audit run (2026-09-19) reported 17 numerical assertions
(max error ≤ 5.7e−14), 2 SymPy derivations, and a passing ID-match test, but
no scripts were saved from that run. The scripts below were reconstructed
after publication from the Book 9 source span
(volume2_full.txt lines 2094–2264) and the section brief. They are new,
independently written checks of the same identities — they must NOT be cited
as the original audit scripts.

## Files

| File | What it does | Result (2026-09-19 reconstruction) |
|---|---|---|
| `audit_book9.py` | 17 numerical assertions N1–N17 (§§9.1, 9.3, 9.4, 9.6) | ALL PASS, max error 1.705e−13 (N16, gradient-based) |
| `audit_book9_symbolic.py` | 2 SymPy derivations S1–S2 (§9.5) | BOTH PASS (see finding below) |
| `test_ids.py` | Desmos config↔container↔PNG fallback ID consistency for book9/index.html (d1–d4 / f1–f4), with negative control | PASS; negative control caught |

## Reconciliation with the published page

The page `book9/index.html` ("Rewrite status") claims "17 numerical
assertions (max error ≤ 5.7e−14)". The reconstruction covers 17 numerical
assertions, all passing, with max error 1.705e−13 — one order looser than
the claimed 5.7e−14 (the loosest is N16, `d[r(1−f)]/dr = 0` via numerical
gradient). The original 5.7e−14 figure cannot be substantiated from any
saved record; the reconstructed figure is stated here instead.

## One finding from the reconstruction

S1 as quoted in the brief/page — "G^t_t/N² + G^r_r/A² = 2(NA)′/(rNA³)
exactly" with mixed components — is **incorrect as stated** (symbolic
residual nonzero; numeric spot check: residual ~4.5e−3). The correct
identity is `G^r_r − G^t_t = 2(NA)′/(rNA³)` (equivalently, covariant
`G_rr/A² + G_tt/N²` = same RHS). The downstream conclusion (vacuum ⟹
(NA)′ = 0 ⟹ AN = 1 after normalization) is unaffected. Recorded in
`~/workspace/vol2_book9/corrections_manifest.md`; the script
`audit_book9_symbolic.py` checks the corrected form.

## Recommended README update

`validation/README.md` row for book9 currently reads:

> | book9 | — | No scripts were saved from the Book 9 run (17 numerical assertions + SymPy checks were reported, brief + source retained in the working records) |

Suggested update:

> | book9 | validation/book9/ | Originals were not saved. Reconstructed scripts (RECONSTRUCTED 2026-09-19, not originals): audit_book9.py (17 numerical assertions, all pass, max err 1.7e−13), audit_book9_symbolic.py (2 SymPy derivations, both pass; S1 identity corrected — see note), test_ids.py (embed consistency, pass). |
