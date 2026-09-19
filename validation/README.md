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
