# How this series is made

This file describes the workflow behind the R Theory rewrite series: how the
mathematics is checked, how the pages are built, and what the claims on them mean.

## 1. The manuscript is read-only

The source is "R Theory — Volume I" (a Google Doc). It is never edited by this
workflow. All checking and rewriting happens on independent copies.

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
