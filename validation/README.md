# Validation scripts

The scripts used to generate and verify the figures and live-graph embeds for
the Volume I rewrite pages (`book0/`–`book6/`). They are published so anyone
can see exactly what was checked and re-run the checks.

## Scope

These scripts perform **completed numerical checks** and structural tests
(embed ID consistency, fallback PNG presence). They are not proofs. See
`../WORKFLOW.md` for the scope labels used across this series.

## Contents

| Book | Scripts | What they check |
|------|---------|-----------------|
| book0 | `make_graphs.py` | Generates the 7 PNG fallbacks; asserts the plotted identities numerically |
| book1 | `make_graphs.py` | Generates the 7 PNG fallbacks; asserts the plotted identities numerically |
| book2 | `verify_figures.py`, `test_embeds.py` | Assertion-verified numerical checks of all figure identities; embed ID consistency |
| book3 | `verify_figures.py`, `gen_graphs.py`, `test_ids.py` | Assertion-verified numerical checks; PNG generation; embed ID consistency |
| book4 | `verify_figures.py`, `test_embed_ids.py` | Numerical + one symbolic (sympy) check of figure identities; embed ID consistency |
| book5 | `test_ids.py` | Embed ID consistency (6 figures). See provenance note below |
| book6 | `verify_book6.py`, `gen_figs_book6.py`, `test_ids.py` | 201 assertions over the figure identities; PNG generation; embed ID consistency |

## Provenance notes

- Scripts are copied verbatim from the working environment where they ran.
  Several hardcode absolute paths (`~/workspace/...` or
  `/home/hatch/workspace/...`); adjust the path variables at the top of each
  script to run them elsewhere.
- `book5/test_ids.py` was **regenerated after publication** from the pattern
  used for Books 3, 4 and 6 — no standalone Book 5 script was saved from the
  original run, and no figure-verification script for Book 5 was found in the
  working records. Its header says so. It passes against the published page.
- The embed ID tests exist because Book 1 once shipped with container IDs
  (`d1`–`d7`) that did not match the JavaScript config IDs (`e1`–`e7`), so its
  live graphs could not initialize. That bug is fixed, and every book's page
  now carries an automated ID-consistency test.
- Live Desmos rendering was never verified in a real browser from the build
  environment; the checks here are static (ID matching, expression sanity,
  non-empty fallbacks). Each page falls back to its PNGs and says so.

## Volume II (Books 7–13)

The same arrangement for the second volume. Audit scripts are included
alongside the figure and embed tests, since the Volume II pipeline audited
each book's mathematics (not only its figures).

| Book | Scripts | What they check |
|------|---------|-----------------|
| book7 | `audit_book7.py`, `audit_book7_symbolic.py`, `make_graphs.py`, `test_graph_ids.py` | 78 numerical + 23 SymPy assertions; figure generation; embed ID consistency |
| book8 | `audit_book8.py`, `gen_figs_book8.py`, `test_ids_book8.py` | 46 assertions (incl. symbolic covariance, F∧F=d(A∧F)); figure generation; embed ID consistency |
| book9 | — | No scripts were saved from the Book 9 run (17 numerical assertions + SymPy checks were reported, brief + source retained in the working records) |
| book10 | `audit_book10.py`, `gen_figures.py`, `test_ids.py` | Assertion checks incl. symbolic du∧dv=2dF∧dG; figure generation; embed ID consistency |
| book11 | `audit_checks.py`, `embed_test.py`, `make_figs.py` | 37 assertions incl. exact anomaly-coefficient arithmetic; embed test; figure generation |
| book12 | `audit_book12.py`, `make_figs.py`, `test_graphs.py` | 55 assertions incl. symbolic checks through 12.III–12.XI; figure generation; graph tests |
| book13 | `audit_book13.py`, `make_figs.py`, `test_graphs.py` | 80 assertions; figure generation; graph tests |

The audits found incorrect results and gaps; these are flagged on the
book pages themselves with their scope labels, not silently corrected.
