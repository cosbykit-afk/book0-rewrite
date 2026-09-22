# PDF snapshots

This directory holds frozen PDF snapshots of the rewrite-series volumes that
have passed the qualification check, plus the pipeline that builds them.

## Qualification

A volume gets a PDF here only when **all of its issues are closed and all of
its content is proven**:

1. Zero open items on the project's Open Issues board for that volume.
2. Zero unretracted incorrect-as-stated findings.
3. Every load-bearing claim on the volume's pages is proved / symbolically
   checked / numerically checked / a standard imported theorem — or an exact
   conditional theorem with a complete proof, or a proved obstruction.
   Declared imports must be standard background physics/mathematics
   (the ST scope), never manuscript assertions, assumptions, or incomplete
   computations carrying conclusions.

Qualification is re-checked by hand before (re)building. The build script
does not decide qualification; it only renders.

## Qualified as of 2026-09-19

- **Volume 0** (books 20–22): no open issues, no incorrect findings,
  per-book Δ_op = ∅. Content is exact theorems, exact conditional theorems,
  and proved obstructions; imports (special relativity, Dirac spinor,
  Standard-Model P_L, Fermi function, nuclear matrix elements) are declared
  standard physics. Book 21's E8(−24) appendix claims are firewalled,
  ledger-cited only, explicitly not stated as established, and no theorem
  depends on them.
- Volumes I, II, III, IV do **not** qualify (open issues / incorrect
  findings / open premises documented per volume; see the build log).

## Files

- `volume-0-overview.pdf`, `volume-0-book20.pdf`, `volume-0-book21.pdf`,
  `volume-0-book22.pdf` — one PDF per page.
- `volume-0-complete.pdf` — the four merged in reading order.
- `cdp_print.py` — HTML→PDF renderer (headless Chromium via DevTools
  protocol, pure stdlib; no `--print-to-pdf` flag, which this Chromium
  build ignores).
- `build.py` — builds the PDFs above and merges the complete volume.

## Rebuilding

`python3 build.py` (needs `pypdf`; Chromium at `/opt/meta-chromium/chrome`).
After rebuilding, update the generation date next to the download links on
the volume overview page.
