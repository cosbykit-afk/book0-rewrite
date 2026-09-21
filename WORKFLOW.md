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
  Audit (V4)" (V3 superseded 2026-09-18; V3 untouched). The project's state
  of record: the critical-path ledger (CP-01 … CP-13), the claim ledger
  (CL-001 … CL-013), the open-issue dependency chain (OI-01 … OI-29),
  incorrect-as-stated findings (IC-1 … IC-18), module certification results,
  and the verification matrix (V-001 … V-006). Every audit chunk
  cross-references the ledger entries it touches, and no claim is stated
  beyond its ledger state.
- **Project board** — a Notion workspace ("R Theory — Project Board",
  connected 2026-09-19) mirroring the ledger: Open Issues (OI-01 … OI-29),
  Critical Path (CP-01 … CP-13), and Incorrect Findings (IC-1 … IC-18)
  databases with a kanban view. Working surface for triage; the Drive
  ledger remains the state of record.

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

Before a book is rewritten, its mathematics is checked independently with the
compute stack inventoried in §9: numerical checks in NumPy, symbolic checks
in SymPy where feasible, the Wolfram 12-module computation in Wolfram Engine
15.0 (extracted at `~/workspace/wolfram/engine-root`, run through the
`~/workspace/wolframscript.sh` wrapper on the free on-demand entitlement),
and exact integer arithmetic in Python (arbitrary-precision big ints — e.g.
the Freudenthal recursion behind the E8 30380 weight table). Pre-computed
tables live at `~/workspace/tables/` (`TABLES.md` catalog plus
`manifest.json` with tuning provenance) and are consumed via symlinks. Every
result is labeled with exactly one scope:

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
reported as a completed numerical check — never as a proof. Embed consistency
is checked per book by `validation/book<N>/test_embeds.py`: every Desmos
calculator id links to its fallback image, every fallback file exists, and the
embedded LaTeX contains the formula the caption and the fallback claim.
Fallback PNGs are rendered with matplotlib (Agg backend) by each book's
`validation/book<N>/make_graphs.py` (or `gen_graphs.py`) from the exact
expressions embedded in Desmos, so each PNG doubles as verification of the
embedded formula; Volume IV fallbacks are rendered at 240 dpi (2026-09-19).
Further visual restyling is deferred. Live Desmos rendering cannot be
browser-verified from the build machine; the validation suite checks embed
consistency instead (see `test_embeds.py` above).

## 5. Publishing

Static HTML/CSS/JS, no build step, no tracking. Each book lives in its own
directory (`book0/`, `book1/`, …; the Volume 0 salvage pages use internal
dirs `book20/`–`book22/` but carry no user-facing book numbers, per Kit's
decision) with its graphs alongside it. Corrections are committed with git
and the full history is preserved. Books ship to GitHub one at a time over
the persistent SSH key (`~/.ssh/id_ed25519`), with the remote verified after
every push: a book is pushed only after it completes the cleanup cycle in
§7. Kit has given standing approval (2026-09-19) for pushing cleaned books
this way — the temporary-key procedure is retired. Only cleaned books ship;
never push uncleaned work.

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

## 7. Book cleanup and release cycle

After the audit chunks, each book goes through a cleanup pass before release.
The pass is per book, in series order unless Kit directs otherwise, and a book
is declared clean only when every item below is done:

1. **Claim verification.** `validation/book<N>/verify_book<N>.py` checks every
   checkable mathematical claim on the book's page — one numbered check per
   claim, each a real assertion with a §2 scope tag. The run exits 0 only if
   all checks pass; failures, errors, and timeouts are reported, never
   absorbed. (Book 0: 15 checks, all passing.)
2. **Embed consistency.** `validation/book<N>/test_embeds.py` (see §4).
3. **Notation.** Every symbol the book defines or uses is entered in the
   **notation ledger** (`~/workspace/vol4/NOTATION_LEDGER.md`, series-wide):
   its definition, where it is defined, its audit standing, and any collision
   or misuse. Collisions are resolved in the ledger before the book ships —
   e.g. the FlatWave/Flatwave dual characterization was verified as one
   object, not two names.
4. **Tooling hygiene.** Generator scripts must point at the real output paths
   and contain no neutered assertions.

When a book is clean, its changes are committed and pushed to GitHub under
the §5 push discipline. Book 0 completed this cycle 2026-09-19 and is the
reference implementation for the rest of the series. Books 0–19 completed
the cycle 2026-09-19.

Ongoing maintenance runs on a schedule, not by hand: the
`rewrite-polish-scanner` cron (daily ~03:47 PT) sweeps one book per run,
book0 → book19 then wraps, proofreading text, checking links and figures,
and verifying status discipline. It pushes polish fixes itself under a
standing approval and logs to `scanner/scan.log` (pointer in
`scanner/pointer.json`). It stays silent unless a fix — or an unfixable
issue — is worth Kit's attention.

## 8. Research closure and the dependency chain

The cleaning pipeline (§7) ships books that are *honest* — every page claim
is verified and every open item is labeled. It does not close the research:
the items the audit marks OPEN / IN / CONDITIONAL stay open on a clean page,
correctly labeled. Closing them is a separate track with its own map.

**Closure** means establishing the open items — turning the manuscript's
"remains OPEN" admissions into earned values. The audit's headline measure
is Δ_op: the set of operational differences the work establishes. Today
Δ_op(Volume IV) = ∅. Closure moves it.

The map is the **dependency chain** (`~/workspace/vol4/DEPENDENCY_CHAIN.md`),
derived from the notation ledger: six layers from the atomic missing inputs
(explicit γ_i, B, Π_−, conventions, SO(16) branching rules) up through the
C8 contraction, the S_F numerical value, the physical choices (ζ_parent,
η_−4), to the y_2 physical matching — plus the side calculations that are
needed in the end but sit off the critical path (M/B recomputation, V_E⁴
role, S_F normalization settlement, A_y Module 32, and others).

Rules for this track:

1. **It never gates a book.** A book ships when it is clean (§7), open
   research underneath it notwithstanding. The chain is background work;
   it must not slow the workflow.
2. **The critical path jumps around.** The chain names the current
   bottleneck (today: the Layer 0 Clifford inputs, per v1 §18.6), but as
   layers close the bottleneck moves — first to the contraction execution,
   then to the physical choices. The chain's §4 pointer is re-pointed each
   time a layer closes; the layer map itself stays.
3. **No new mathematics is asserted in the chain.** Every dependency
   traces to a ledger entry or a cited v1 line. The chain is planning, not
   proof.
4. **Physical choices are flagged as choices.** ζ_parent (parent action)
   and η_−4 (UV footprint) are not closable by computation — the chain
   records them as gates, not as gaps to be computed through.
5. **Proving ground first.** Calculations advance from what is already
   proved or exactly established (CP theorems, CLEAN identities, SC
   tables) rather than speculatively hunting for connections — e.g.
   sweeping the archive for the missing contraction inputs. Per Kit
   2026-09-20; speculative searches are deprioritized.

## 9. Tool inventory

Every stage above names its tools here in one place.

- **Sources (read-only).** Google Docs (the "R Theory" manuscripts) and
  Google Drive ("Projection Craft & R-Theory (Active) / Control & Ledgers"),
  both read-only — never edited without Kit's explicit confirmation; Notion
  ("R Theory — Project Board": Open Issues, Critical Path, Incorrect
  Findings databases) as the triage surface.
- **Computation.** Python 3 with NumPy (numerical checks), SymPy (symbolic
  checks), and arbitrary-precision integers (exact tables — e.g. the E8 30380
  Freudenthal recursion); Wolfram Engine 15.0 via
  `~/workspace/wolframscript.sh` (free on-demand entitlement); pre-computed
  tables at `~/workspace/tables/` (`TABLES.md` catalog, `manifest.json`
  provenance), consumed through symlinks. Everything runs from the shell
  (`muse.exec`); long computations run in the background and report only on
  completion, with timeouts disclosed, never absorbed.
- **Figures.** Desmos embeds with PNG fallbacks; fallbacks rendered by
  `validation/book<N>/make_graphs.py` with matplotlib (Agg) + NumPy from the
  exact embedded expressions; per-book `validation/book<N>/test_embeds.py`
  checks embed consistency.
- **Pages.** Static HTML/CSS/JS authored directly (`muse.write`,
  `muse.edit`); one directory per book with its graphs alongside it.
- **Publishing.** git + GitHub over the persistent SSH key
  (`~/.ssh/id_ed25519`); remote verified after every push; only cleaned
  books ship, under Kit's standing push approval.
- **Orchestration.** Independent parallel verification is delegated to
  subagents (`subagent.spawn`); recurring work runs on cron (`cron.add`,
  `cron.list` — e.g. the daily `rewrite-polish-scanner`); commitments are
  tracked (`tracking.create`, `tracking.set_status`) and durable research
  goals live under `user_goal`; theory work stays routed to the R Theory
  side chat (`chat.*`).
- **Verification discipline.** Every check is a real assertion in a script
  that exits nonzero on failure; scope labels from §2 are attached at the
  point of the check; nothing is promoted beyond what the check established.
