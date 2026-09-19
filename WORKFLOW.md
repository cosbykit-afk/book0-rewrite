# How this series is made

This file describes the workflow behind the R Theory rewrite series: how the
mathematics is checked, how the pages are built, and what the claims on them mean.

## 0. Project control

This project is managed under the Drive-based control framework. The control
documents live in Google Drive at
`Projection Craft & R-Theory (Active) / Control & Ledgers` and are read-only
to this workflow — they are never edited without Kit's explicit confirmation.

- **Governing protocol** — "Governmer: Workflow & Honesty Protocol — The
  Engineering Standard." Radical transparency and strict epistemic hygiene
  outrank any incentive to give a convenient answer: zero simulation (never
  generate mock outputs or placeholder runs; an unexecuted computation does
  not exist), explicit uncertainty ("Unknown"/"Unverified" rather than
  inference), hard stops with exact boundaries when a tool runs out of
  capacity, provenance for every claim and status label, and unfiltered
  negative results (a zero trace, a failed projection, a no-go theorem is a
  successful outcome, reported raw).
- **Master ledger** — "Projection Craft — Research Control & Master Ledger
  Audit (V3)." The project's state of record: the critical-path ledger
  (CP-01 … CP-09), the claim ledger (CL-001 … CL-013), module certification
  results, and the verification matrix (V-001 … V-006). Every audit chunk
  cross-references the ledger entries it touches, and no claim is stated
  beyond its ledger state.

The scope labels in §2 map onto the ledger's states: checked proof and
completed symbolic check correspond to [CERTIFIED]/[EXACT]; completed
numerical check, standard imported theorem, and manuscript assertion stay
below certification; assumption/axiom, incorrect result, and incomplete
computation are tracked as [OPEN], [CONDITIONAL], or failed — never
promoted.

## 1. The manuscript is read-only

The source is "R Theory — Volume I" (a Google Doc). It is never edited by this
workflow. All checking and rewriting happens on independent copies. The same
applies to every source volume and to the Drive control documents above.

## 2. Audit before rewrite

Before a book is rewritten, its mathematics is checked independently (numerical
checks with NumPy, symbolic checks where feasible, Wolfram modules where the
engine is licensed). Every result is labeled with exactly one scope:

- **checked proof** — established by rigorous argument
- **completed symbolic check** — a finished exact computation
- **completed numerical check** — a finished floating-point measurement, not a proof
- **standard imported theorem** — a cited result from the literature
- **manuscript assertion** — stated in the source, not independently established
- **assumption or axiom** — taken as given
- **incorrect result** — a check that failed or contradicted the claim
- **incomplete or failed computation** — timed out, errored, or never finished

Nothing is promoted: a manuscript label, a partial calculation, a visual
impression, or an expectation is never presented as a proved result. If a tool
runs out of time, the result is reported as incomplete.

## 3. Rewrites are intuition-first, not proofs

Each book's page explains the ideas in plain language with pictures first.
Formal statements carry their scope label. Anything the audit has not
established is labeled a manuscript assertion, not a finding.

## 4. Graphs are tested, not decorative

Every figure is a live Desmos embed with a static PNG fallback. Each plotted
expression is executed and numerically verified where a number is claimed; the
verification scripts use real assertions, and sampled-point agreement is
reported as a completed numerical check — never as a proof.

## 5. Publishing

Static HTML/CSS/JS, no build step, no tracking. Each book lives in its own
directory (`book0/`, `book1/`, …) with its graphs alongside it. Corrections are
committed with the full history preserved.

## 6. Audit chunks and the ledger trail

Large or issue-dense volumes are audited in small sequential chunks, in
dependency order — never raced. Each chunk produces two artifacts, both
committed to this repo (e.g. `vol4-audit/book17/`):

- the **audit script** (`audit_<chunk>.py`): every check is a real assertion
  with a scope tag; a failed assertion fails the run, and the run reports
  pass/fail counts and any timeout explicitly;
- the **chunk ledger** (`LEDGER_<chunk>.md`): the per-claim verdicts in the
  §2 taxonomy, plus incorrect-as-stated findings, terminology notes, and
  open gates.

Chunk ledgers cross-reference the Master Ledger's claim IDs (CL-…) where the
chunk touches them, and flag terminology collisions across books. The Drive
control documents remain the state of record; this repo's `*-audit/`
directories are the reproducible evidence trail behind them.
