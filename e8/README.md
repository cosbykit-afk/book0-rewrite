# E8 weight table — 30,380-dimensional representation

Full weight/multiplicity table for the irreducible E8 representation with
highest Dynkin label `(0,0,0,0,0,0,1,0)` (Bourbaki labeling: chain
1-3-4-5-6-7-8, node 2 attached to 4).

## Scope

**Completed exact computation** (exact integer arithmetic, Freudenthal
recursion). Not a proof of a manuscript claim; a computed table.

## Contents

- `table_30380_full.csv` — 9,121 distinct weights: Dynkin labels (a1..a8),
  multiplicity. Header row included.
- `table_30380_dominant.csv` — the 4 dominant weights with multiplicity and
  Weyl-orbit size.
- `table_30380_summary.json` — dimension, counts, tripwire results.

## Result

| Dominant labels | Multiplicity | Orbit size | Contribution |
|---|---|---:|---:|
| `(0,0,0,0,0,0,1,0)` | 1 | 6720 | 6720 |
| `(1,0,0,0,0,0,0,0)` | 7 | 2160 | 15120 |
| `(0,0,0,0,0,0,0,1)` | 35 | 240 | 8400 |
| `(0,0,0,0,0,0,0,0)` | 140 | 1 | 140 |

Exact reconciliation: 6720 + 15120 + 8400 + 140 = 30380.

Tripwires passed: exact divisibility and positivity at every Freudenthal
step; Weyl dimension formula = 30380; dominant enumeration complete by the
box bound b·A⁻¹·bᵀ ≤ (λ,λ) = 6; orbit sizes independently re-verified via
|W|/|W_stab| (stabilizers E6×A1, D7, E7, E8).

Generating script: `~/workspace/e8/freudenthal_30380.py` (exact integer
arithmetic, exit 0).
