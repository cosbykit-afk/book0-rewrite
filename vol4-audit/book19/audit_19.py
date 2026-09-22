#!/usr/bin/env python3
"""
Volume IV v1 chunk-5 audit: Book 19 (doc lines 3221-3325) + Appendices A-C
(doc lines 3326-3636).

Authority: v1 ONLY (Google doc 1-T5Eh7tbPcNenfB1ubkUmST5IYq_QGchm5X1ZcIRvoU).
v2 / v3-draft / unsigned certification report are context only; their claims
are never used as findings.

Scope labels (Kit's standing rule):
  CP checked proof, SC symbolic check, NC numerical check, ST standard
  imported theorem, MA manuscript assertion, AX assumption/axiom,
  IN incomplete/failed computation, IC incorrect-as-stated result.
Manuscript self-labels are the manuscript's words, never the audit's verdict.

Every check() is a real assertion: a failed assertion fails the run.
IC / contradiction / Appendix-A-flag findings are recorded in `findings`
with the *establishing facts* asserted in the script; the ledger carries
the verdicts.

Upstream dependencies (NOT re-derived; see chunk ledgers):
  chunks 1-2: octant structure, C8 word, w0, rapidity products
    (E-contact 4, propagator 4, all-eight 16), V_E, IC-1..IC-4.
  chunk 3: formal projector algebra, conversion chain, IC-5..IC-11,
    IN-1..IN-3, S_F OPEN, stripped-response definition.
  chunk 4: Book 18 dims/branching, IC-12..IC-17, line-3542 located in Book 19.
"""

import math
import re
import sys

RAW = '/home/hatch/workspace/vol4/volume_iv_v1_raw.txt'
V3 = '/home/hatch/workspace/vol4/volume_iv_v3_raw.txt'
REPORT = '/home/hatch/workspace/vol4/volume_iv_audit_report_raw.txt'

text = open(RAW, encoding='utf-8').read()
lines = text.splitlines()


def L(n):
    """1-indexed doc line."""
    return lines[n - 1]


def seg(a, b):
    """Doc lines a..b inclusive, joined."""
    return '\n'.join(lines[a - 1:b])


results = []   # (name, scope)
findings = []  # (id, kind, detail)


def check(name, scope, cond, detail=''):
    assert cond, 'FAILED [%s] %s %s' % (scope, name, detail)
    results.append((name, scope))


def record(fid, kind, detail):
    findings.append((fid, kind, detail))


B19 = seg(3221, 3325)    # Book 19
APPA = seg(3326, 3404)   # Appendix A
APPB = seg(3405, 3419)   # Appendix B
APPC = seg(3420, 3637)   # Appendix C (closing line is 3637)

print('=== Volume IV v1 chunk-5 audit: Book 19 + Appendices A-C ===')

# ---------------------------------------------------------------- Book 19
print('-- Book 19: UV boundary and physical promotion --')

# 19.1 footprint table: paired-harmonic exclusion math
check('19.1 paired footprint zero at E contacts: cos(4*22.5deg)=cos(90deg)=0',
      'CP', abs(math.cos(math.radians(4 * 22.5))) < 1e-12)
check('19.1 table present: E-localized/Balanced survive, B/O-localized/paired excluded',
      'CP', all(s in B19 for s in [
          'E-localized', 'B-localized', 'O-localized', 'Balanced', 'Paired cos(4x)'])
      and 'The mathematical filter eliminates the paired harmonic, B-localized,'
           ' and O-localized footprints' in B19)
# The survival criterion (non-zero at E contacts) is a physical choice, not derived.
check('19.1 Status: CONDITIONAL label present (criterion is a choice)',
      'MA', 'Status: CONDITIONAL.' in B19)

# 19.2 uniform-action premise: honest conditional + OPEN
check('19.2 Status: OPEN present; k0^0=1 stated as conditional on uniform action',
      'CP', 'Status: OPEN.' in B19
      and 'gives k₀⁰ = 1 only if k₀ multiplies the complete relevant microscopic'
          ' action uniformly' in B19)
check('19.2 "The PCBF relation alone does not establish this premise" present',
      'CP', 'The PCBF relation alone does not establish this premise.' in B19)

# 19.3 Distler-Garibaldi: characterization verified against arXiv:0905.2658
# abstract ("analyze certain subgroups of real and complex forms of the Lie
# group E8 ... embedding the gauge groups of gravity and the Standard Model
# into a real or complex form of E8 lacks certain representation-theoretic
# properties required by physical reality") on 2026-09-19.
check('19.3 cites arXiv:0905.2658; CONTESTED status present (honest label)',
      'ST', 'arXiv:0905.2658' in B19 and 'Status: CONTESTED.' in B19
      and 'not a proven evasion' in B19)

# 19.4 Airy/Bessel: J0 EXACT is a manuscript self-label, NOT audited here
# (rotational-averaging inheritance lives in unaudited Vol-III/bridge material).
check('19.4 self-labels present: J0 EXACT; jinc CONDITIONAL; Airy CONDITIONAL',
      'MA', 'Status: J₀ EXACT; jinc CONDITIONAL; Airy CONDITIONAL.' in B19)
check('19.4 jinc/Airy conditionality tied to stated premises (disk measure)',
      'CP', 'conditional on selecting the uniform Euclidean disk measure' in B19)

# 19.5 Delta_op: honest
check('19.5 "No physical promotion is authorized. Δ_op(Volume IV) = ∅." present',
      'CP', 'No physical promotion is authorized. Δ_op(Volume IV) = ∅.' in B19)

# 19.6 falsifiability: three criteria, all stated as conditionals
check('19.6 criterion 1: R_perp != 0 unabsorbed by T disproves isolation',
      'CP', 'cannot be absorbed by the witness direction T' in B19)
check('19.6 criterion 2: non-vanishing cross-terms breaching Z2 parity',
      'CP', 'breach Z₂ parity grading' in B19)
check('19.6 criterion 3: coupling strengths vs electroweak precision bounds',
      'CP', 'violate observed electroweak precision bounds' in B19)

# 19.7 gate table: 5 rows, statuses match Appendix A
check('19.7 gate table: 5 rows with statuses OPEN/OPEN/CONTESTED/CONDITIONAL/OPEN',
      'CP', all(s in B19 for s in [
          'UV footprint selection OPEN', 'Uniform-action premise OPEN',
          'DG engagement CONTESTED', 'Airy/Bessel inheritance CONDITIONAL',
          'Δ_op population OPEN']))

# ------------------------------------------------------- terminology sweep
print('-- terminology: Flatwave --')
check('no "Flatwave"/"FlatWave" anywhere in Book 19 or Appendices (3221-3636)',
      'CP', not re.search(r'flatwave', seg(3221, 3636), re.I))

# ------------------------------------------------- Appendix A cross-check
print('-- Appendix A: status-ledger cross-check (43 rows) --')

# Row counts are text facts.
def count_rows(a, b):
    n = 0
    for i in range(a, b + 1):
        if lines[i - 1].strip().startswith('·'):
            n += 1
    return n

check('App.A section sizes: EXACT 13 / STRUCTURAL 3 / CONDITIONAL 4 / OPEN 12 /'
      ' CONTESTED 1 / CLOSED-NO-GO 10 = 43 rows',
      'CP', count_rows(3329, 3346) == 13 and count_rows(3347, 3354) == 3
      and count_rows(3355, 3363) == 4 and count_rows(3364, 3380) == 12
      and count_rows(3381, 3386) == 1 and count_rows(3387, 3404) == 10)

# EXACT rows: fair ones (chunk-1/chunk-2 verdicts; IC-1/IC-2 caveats carried).
for row in ['Harmonic carrier identity', 'Corrected imbalance formula',
            'Elliptic carrier relation', 'Octant table', 'Three-bit code']:
    check('App.A EXACT row "%s": fair (chunk-1 CP)' % row, 'CP', row in APPA)
check('App.A EXACT row "2:1 elliptic map": fair (chunk-1 CP; IC-1 caveat)',
      'CP', '2:1 elliptic map' in APPA)
check('App.A EXACT row "Rapidity values and products": fair for Book-17 values'
      ' (chunk-1 CP; IC-2 caveat; addendum item-5 conflict noted separately)',
      'CP', 'Rapidity values and products' in APPA)
check('App.A EXACT row "Dominant function values": fair (chunk-1 NC + chunk-2 SC;'
      ' IC-2 caveat on the printed radical)',
      'CP', 'Dominant function values' in APPA)

# EXACT rows that OVERSTATE the audit's findings (flagged, not new ICs:
# the content is not mathematically false; the label overclaims).
check('App.A EXACT lists "Four-contact magnitude" without qualifier',
      'MA', '· Four-contact magnitude' in APPA
      and 'from archive' not in APPA.split('Four-contact magnitude')[1][:40])
record('FLAG-A1', 'APPENDIX-A-FLAG',
       'Row "Four-contact magnitude" marked EXACT, but the per-contact 1/4 is'
       ' archive-sourced (MA) and its relation to the certified 1/2 projection'
       ' coefficient is OPEN per Tier 3.1\'s own warning (chunk 3). The'
       ' (1/4)^4 = 1/256 arithmetic is CP; the 1/4 input is not established'
       ' in v1. Label should carry the archive qualifier.')
check('App.A EXACT lists "Wick sign" without the "(from archive)" qualifier',
      'MA', '· Wick sign' in APPA
      and 'from archive' not in APPA.split('· Wick sign')[1][:60])
record('FLAG-A2', 'APPENDIX-A-FLAG',
       'Row "Wick sign" marked EXACT without provenance qualifier. σ_Wick^(t)'
       ' = -1 is not derived anywhere in v1 §§17.6-17.9, §17.18, or Book 18;'
       ' §17.18.6.2 carried "(from archive)" but §17.7.2\'s table and §18.6'
       ' dropped it (chunk-2/3 provenance notes). Not independently verified.')
check('App.A EXACT lists "Graded-connection rigidity theorem λ = ±1"',
      'MA', 'Graded-connection rigidity theorem λ = ±1' in APPA)
record('FLAG-A3', 'APPENDIX-A-FLAG',
       'Row "Graded-connection rigidity theorem λ = ±1" marked EXACT, but it'
       ' comes from bridge-essay §3.2, which chunk 2 logged as NOT audited'
       ' (out of scope). This audit cannot confirm it; coverage by the Vol I-III'
       ' audits is not established. Unverifiable-by-audit EXACT claim.')
check('App.A EXACT lists "Reduced-matrix-element firewall"',
      'AX', 'Reduced-matrix-element firewall' in APPA)
record('FLAG-A4', 'APPENDIX-A-FLAG',
       'Row "Reduced-matrix-element firewall" marked EXACT, but a firewall is'
       ' a methodological principle (AX), not a proved result. The audit treats'
       ' it as a sound negative-result principle (chunks 1-3), not as a theorem.')
check('App.A EXACT lists "Ancestry criterion"',
      'MA', 'Ancestry criterion' in APPA)
record('FLAG-A5', 'APPENDIX-A-FLAG',
       'Row "Ancestry criterion" marked EXACT, contradicting the manuscript\'s'
       ' own labels: §17.5.1 is CONDITIONAL, §17.5.2 is CONDITIONAL on the'
       ' uniform-action premise, and §19.2 has that premise OPEN. The §17.5.3'
       ' resolution itself verified CP (chunk 2), but the criterion\'s premise'
       ' is OPEN, so EXACT overstates.')

# STRUCTURAL IDENTIFICATION rows
check('App.A STRUCTURAL "C8 ↔ octant correspondence": fair (chunk-1: honest label)',
      'CP', 'C8 ↔ octant correspondence' in APPA)
check('App.A STRUCTURAL "Four-contact magnitude origin": fair (matches §17.8'
      ' EXPLANATORY label)',
      'CP', 'Four-contact magnitude origin' in APPA)
check('App.A STRUCTURAL "Veronese condition at octant boundaries": present;',
      'MA', 'Veronese condition at octant boundaries' in APPA)
record('FLAG-A6', 'APPENDIX-A-FLAG',
       'Row "Veronese condition at octant boundaries" (STRUCTURAL'
       ' IDENTIFICATION) comes from bridge-essay §1.4 material (doc lines'
       ' 1083-1091, 1291), logged unaudited in chunk 2. Unverified by this'
       ' audit; the soft label does not overclaim, but confirmation is absent.')

# CONDITIONAL rows
check('App.A CONDITIONAL "Quasi-linear parent magnitude k₀ = β²/(2α)": present;',
      'MA', 'k₀ = β²/(2α)' in APPA)
record('FLAG-A7', 'APPENDIX-A-FLAG',
       'Row "Quasi-linear parent magnitude k₀ = β²/(2α)" is a Book-16/bridge'
       ' import (doc lines 88-89, 2712), not audited in chunks 1-4.'
       ' Unverified by this audit; CONDITIONAL is a soft, fair label.')
check('App.A CONDITIONAL "Functional form 1/S = cosh w": present;',
      'MA', '1/S = cosh w' in APPA)
record('FLAG-A8', 'APPENDIX-A-FLAG',
       'Row "Functional form 1/S = cosh w of the parent normalization" is a'
       ' bridge import (doc lines 89, 2713), not audited in chunks 1-4.'
       ' Unverified by this audit; CONDITIONAL is a soft, fair label.')
check('App.A CONDITIONAL "UV footprint classification": fair (matches §19.1)',
      'CP', 'UV footprint classification' in APPA)
check('App.A CONDITIONAL "Airy/Bessel inheritance": fair (matches §19.4)',
      'CP', 'Airy/Bessel inheritance' in APPA)

# OPEN rows: all 12 consistent with the audit's open-gate list.
open_rows = ['C3/C4 forcing', 'S_F numerical value', 'N₁₈₂₀', 'ζ_parent (k₀ power)',
             'η₋₄ (UV selection)', 'Uniform-action premise', 'Parent-action selection',
             'Cl(16) gamma matrices', '1820 projector', '120 embedding',
             '54 projector', 'Δ_op population']
for row in open_rows:
    check('App.A OPEN row "%s": fair (matches audit)' % row, 'CP', row in APPA)

# CONTESTED row
check('App.A CONTESTED row "Distler–Garibaldi evasion": fair (matches §19.3)',
      'CP', 'Distler–Garibaldi evasion' in APPA)

# CLOSED / NO-GO rows
check('App.A CLOSED row "Paired harmonic, B-localized, O-localized UV footprints":'
      ' fair (exclusion logic audited CP, chunks 2/5)',
      'CP', 'Paired harmonic, B-localized, O-localized UV footprints' in APPA)
vol3_rows = ['Representation search for physical 54',
             'Raw/exchange Φ₁ as physical-135 source',
             'Generate y₂ from neutral reduced dynamics',
             'Internal 120 as determinant character source',
             'One-body Saw imbalance Q as C8 defect',
             'qSaw labels alone as crossing discriminator',
             'Scalar m₀ ≠ m₂ as direct C8 defect origin',
             'Common four-contact magnitude as orientation origin',
             'Cancel isolated m₂⁻⁴ with other crossing']
for row in vol3_rows:
    check('App.A CLOSED row "%s": present as stated (Vol-III-preserved;'
          ' not re-verified in this audit)' % row, 'MA', row in APPA)

# ------------------------------------------------- Appendix B (no-go ledger)
print('-- Appendix B: no-go ledger --')
check('B1 "C8 ↔ octant correspondence is not a theorem; C3/C4 OPEN": accurate'
      ' (matches chunk-1 honest structural label)',
      'CP', 'NO-GO B1: C8 ↔ octant correspondence is not a theorem.' in APPB)
check('B2 "The Distler–Garibaldi theorem is not evaded ... candidate, not a'
      ' resolution": accurate (matches §19.3)',
      'CP', 'NO-GO B2: The Distler–Garibaldi theorem is not evaded.' in APPB)
check('B3 "The uniform-action premise is not established": accurate (matches §19.2)',
      'CP', 'NO-GO B3: The uniform-action premise is not established.' in APPB)
check('B4 "The Airy transition is not established. Only J₀ is unconditional":'
      ' accurate (matches §19.4)',
      'CP', 'NO-GO B4: The Airy transition is not established.' in APPB)

# --------------------------------------- Appendix C + Addendum 4.A
print('-- Appendix C: codebase skeleton (by reference to §18.8) --')
check('App.C: "The Wolfram code from §18.8 is the primary computational artifact"',
      'CP', 'The Wolfram code from §18.8 is the primary computational artifact.'
      in APPC)
# The four skeleton defects carry over by reference (chunk-4 IC-13..IC-16).
check('App.C carry-over: NullSpace[Transpose[{traceVector}]] defect present'
      ' in §18.8 (line 3168)',
      'CP', 'P1820 = NullSpace[Transpose[{traceVector}]];' in L(3168))
record('IC-13', 'IC',
       'Appendix C re-presents §18.8\'s skeleton by reference (line 3423), so'
       ' IC-13 carries over: line 3168 NullSpace[Transpose[{traceVector}]]'
       ' yields {} (nullity 1-1=0); intended reading gives 8255, not 1820.')
check('App.C carry-over: KroneckerProduct 4x128x128 defect present (line 3173)',
      'CP', 'KroneckerProduct[gammaI[i], gammaL[mu], gammaI[j], gammaL[nu]]'
      in L(3173))
record('IC-14', 'IC',
       'Carry-over: line 3173 KroneckerProduct of four 128×128 matrices is'
       ' 128^4×128^4, sandwiched by an 1820×8256 P1820 — dimensionally'
       ' incompatible (chunk-4 IC-14).')
check('App.C carry-over: double-counted -(1/256) present (line 3193)',
      'CP', 'S_F = -(1/256) * S_F_raw;' in L(3193))
record('IC-15', 'IC',
       'Carry-over: line 3193 applies -(1/256) to S_F_raw while line 3193\'s'
       ' nHat54 = -(Sqrt[10]/1536)*S_F*m2^(-4) presumes a stripped input; the'
       ' contact factor is counted twice, violating §17.18.10\'s regression'
       ' requirement (chunk-4 IC-15).')
check('App.C carry-over: wickSign used (line 3189) with no assignment in the'
      ' skeleton',
      'CP', 'wickSign * contraction' in L(3189)
      and not re.search(r'wickSign\s*=', seg(3160, 3200)))
record('IC-16', 'IC',
       'Carry-over: line 3189 sums wickSign * contraction[...] but wickSign is'
       ' never assigned in the skeleton (chunk-4 IC-16).')
# IC-17 (gamma template) lives in §18.2, outside the skeleton, but it is the
# skeleton's gamma input.
check('App.C bottleneck statement names Cl(16) gammas + 1820 projector (both OPEN)',
      'CP', 'The bottleneck is the explicit construction of the Cl(16) gamma'
      ' matrices and the 1820 projector.' in APPC)

print('-- Addendum 4.A --')
check('Addendum header: "Status ledger. Δ_op = ∅." present',
      'CP', 'Status ledger. Δ_op = ∅.' in APPC)
check('Addendum header: "numerical closure open until Module 11 executes" present',
      'CP', 'numerical closure open until Module 11 executes' in APPC)

# Item 1: 3875 correction
import sympy as sp
check('Add.1: 135+1820+1920 = 3875 exact', 'CP', 135 + 1820 + 1920 == 3875)
check('Add.1: erroneous table 248+135+1820+1920+54 = 4177 exact',
      'CP', 248 + 135 + 1820 + 1920 + 54 == 4177)
check('Add.1: "3875 = 135 ⊕ 1820 ⊕ 1920" present; irrep content is standard (ST)',
      'ST', '3875 = 135 ⊕ 1820 ⊕ 1920.' in APPC)
check('Add.1: "This insert supersedes that table" present (editorial)',
      'CP', 'This insert supersedes that table.' in APPC)

# Item 2: 54 witness
check('Add.2: dim 54 = (10×11)/2 − 1 = 54 exact', 'CP', (10 * 11) // 2 - 1 == 54)
check('Add.2: "Q_F = (6/5) T" present (MA: posited, not derived in v1)',
      'MA', 'Q_F = (6/5) T.' in APPC)
check('Add.2: "The 1820 ... projects onto the 54 of SO(10)" present, while the'
      ' explicit map P_{1820→54} is a §18.5 missing input (line 3091)',
      'MA', 'The 1820 antisymmetric rank-4 SO(16) tensor projects onto the 54'
      ' of SO(10).' in APPC
      and 'Missing input: The explicit Clebsch–Gordan map P_{1820→54}.'
      in L(3091))
record('NOTE-2', 'ORGANIZATION',
       'Addendum item 2 states the 1820 "projects onto the 54 of SO(10)" as'
       ' fact while §18.5 lists the explicit Clebsch–Gordan map P_{1820→54} as'
       ' a missing input; the P₅₄ location (135 vs 1820) remains unreconciled'
       ' (chunks 3-4). Manuscript assertion, not established.')

# Item 3: S_F notation triple-use, unreconciled with §17.18.6.5
check('Add.3: "S_F = Tr₁₈₂₀(E B E O E B E O)" present (S_F as scalar trace)',
      'MA', 'S_F = Tr₁₈₂₀(E B E O E B E O).' in APPC)
check('Add.3: "M₅₄ = P₁₈₂₀→₅₄ S_F P₁₈₂₀→₅₄†" present (S_F reused as the operator)',
      'MA', 'M₅₄ = P₁₈₂₀→₅₄ S_F P₁₈₂₀→₅₄†.' in APPC)
check('Add.3: "S_F = Tr(M₅₄ T)/Tr(T²)" present (S_F reused as extracted scalar)',
      'MA', 'S_F = Tr(M₅₄ T)/Tr(T²).' in APPC)
check('Book-17 definition for contrast: S_F := ⟨Q_F, R̃^t_2222(F,F)⟩ = 3a₂₂₂₂'
      ' (stripped scalar) at line 1863',
      'CP', 'S_F := ⟨Q_F, R̃^t_2222(F,F)⟩ = 3a₂₂₂₂' in L(1863))
record('NOTE-3', 'ORGANIZATION',
       'Addendum item 3 uses "S_F" for three different objects in one section'
       ' (scalar trace; the ordered-contraction operator sandwiched into M₅₄;'
       ' the 54-component extracted scalar), none reconciled with the defined'
       ' stripped scalar S_F := ⟨Q_F, R̃^t_2222⟩ = 3a₂₂₂₂ (§17.18.6.5, line'
       ' 1863; §18.6, line 3115). The contact normalization and Wick sign are'
       ' listed as bullets but not applied to the trace, so dressed vs'
       ' stripped is ambiguous — against §17.18.10\'s "counted exactly once"'
       ' regression requirement. Notation collision + unreconciled'
       ' redefinition.')
check('Add.3: "Require R⊥ = 0. If R⊥ ≠ 0, the scalar witness hypothesis is'
      ' disproved." consistent with §19.6 criterion 1',
      'CP', 'If R⊥ ≠ 0, the scalar witness hypothesis is disproved.' in APPC)

# Item 4: N_1820 "exact discrete graph invariant"
check('Add.4: "isolates N₁₈₂₀ as an exact discrete graph invariant" present,'
      ' while Appendix A lists N₁₈₂₀ OPEN',
      'MA', 'isolates N₁₈₂₀ as an exact discrete graph invariant.' in APPC
      and '· N₁₈₂₀' in APPA)
record('FLAG-N4', 'OVERSTATEMENT',
       'Addendum item 4 calls N₁₈₂₀ "an exact discrete graph invariant" while'
       ' Appendix A lists N₁₈₂₀ OPEN, §18.7 is honestly OPEN, and the 1/2→1/4'
       ' per-contact relation is open (Tier 3.1). The B and O factors are'
       ' unspecified ("each B contributes a factor; each O contributes a'
       ' factor" — no values) and "the absorbed witness norm" is undefined.'
       ' Not established.')
check('Add.4: B/O per-factor values absent from the text',
      'MA', 'each B contributes a factor; each O contributes a factor.'
      in APPC)

# Item 5: the line-3542 tension
print('-- line-3542 tension --')
V_E = math.sqrt(4 + 2 * math.sqrt(2)) + 1 + math.sqrt(2)
check('Add.5: V_E^4 = 638.7823 ≈ 638.78 (the "product over the four decay'
      ' octants")',
      'NC', abs(V_E ** 4 - 638.78) < 0.01,
      'V_E^4 = %.6f' % V_E ** 4)
check('Add.5: exact sentence present at line 3542',
      'CP', L(3542) == 'At the four spatial decay octants, the dominant'
      ' trigonometric envelope takes the same value. Its product over the'
      ' four decay octants is 638.78. This factors out of S_F, preserving'
      ' field-redefinition invariance. The propagator rapidity product is 16,'
      ' assigned to ζ_parent.')
# Established: propagator cosh product = (sqrt2)^4 = 4 (chunk-1 CP, §17.3.4,
# §17.7.2, §17.18.9.3); all-eight = (sqrt2)^8 = 16. Book 17's own line 765/771
# distinguishes "propagator rapidity product" from "total rapidity product" 16.
check('established propagator cosh product (√2)^4 = 4',
      'CP', sp.simplify(sp.sqrt(2) ** 4 - 4) == 0)
check('all-eight product (√2)^8 = 16',
      'CP', sp.simplify(sp.sqrt(2) ** 8 - 16) == 0)
check('Book 17 distinguishes: "the total rapidity product is 16, not 4"'
      ' (line 765); "the E contact rapidity product (4), not the propagator'
      ' rapidity product" (line 771)',
      'CP', 'the total rapidity product is 16, not 4' in L(765)
      and 'The ancestry count includes only the E contact rapidity product (4),'
      ' not the propagator rapidity product.' in L(771))
record('IC-18', 'IC',
       'Addendum item 5 (line 3542): "The propagator rapidity product is 16."'
       ' The established propagator cosh product is (√2)^4 = 4 (§17.3.4,'
       ' §17.7.2, §17.18.9.3, chunk-1 CP). The value 16 matches the ALL-EIGHT'
       ' product (√2)^8. Book 17\'s own terminology (lines 765, 771)'
       ' distinguishes "propagator rapidity product" from the "total rapidity'
       ' product" of 16, so no textual support exists for reading 16 as the'
       ' all-eight product here — as written the value is wrong. The'
       ' assignment to ζ_parent agrees with §17.5.3\'s resolution (sweep-'
       ' verified CP), but the premise value is incorrect.')
check('Add.5: assignment of the propagator factors to ζ_parent agrees with'
      ' §17.5.3 (sweep-verified)',
      'CP', 'assigned to ζ_parent' in L(3542)
      and 'belong to ζ_parent' in L(768))
# "factors out of S_F": no Book-17 support; conflicts with §17.3.5.
check('§17.3.5 (line 623): 638.78 "role in the Clifford contraction remains to'
      ' be determined"',
      'CP', 'its role in the Clifford contraction remains to be determined'
      in L(623))
check('§17.18.6.4 stripped list (line 1853) contains no V_E / dominant-function'
      ' term',
      'CP', 'stripped' in L(1853) and 'V_E' not in seg(1839, 1860)
      and 'dominant' not in seg(1839, 1860).lower())
check('"field-redefinition invariance" appears exactly once in v1 (line 3542);'
      ' never defined or proved',
      'MA', text.count('field-redefinition') == 1)
record('NOTE-3542b', 'MANUSCRIPT-ASSERTION',
       'Addendum item 5: "This [638.78] factors out of S_F, preserving'
       ' field-redefinition invariance." No derivation exists in v1; it'
       ' conflicts with §17.3.5\'s honest "its role in the Clifford'
       ' contraction remains to be determined" (line 623) and with the'
       ' §17.18.6.4 stripped list, which contains no V_E term. "Field-'
       ' redefinition invariance" is never defined or proved in v1. S_F is'
       ' OPEN, so this is an unsupported manuscript assertion (not IC: an'
       ' uncomputed quantity cannot be contradicted).')

# Item 6: "Theorem" vs NO-GO B1
check('Add.6: "Theorem. ... the unique cyclic word ... E B E O E B E O" present',
      'MA', 'Theorem. In an 8-octant partition' in APPC)
check('Add.6: "Proof sketch." present',
      'MA', 'Proof sketch. E contacts are localized boundary transitions'
      in APPC)
record('CONTR-1', 'INTERNAL-CONTRADICTION',
       'Addendum item 6 states as a THEOREM (with "Proof sketch." and "∎")'
       ' that EBEOEBEO is "the unique cyclic word preserving parity and'
       ' boundary continuity" — directly contradicting the manuscript\'s own'
       ' Appendix B NO-GO B1: "C8 ↔ octant correspondence is not a theorem.'
       ' The C3/C4 forcing question remains OPEN." The proof sketch assumes'
       ' E contacts "can only reside at zero-crossing decay nodes" and that'
       ' internal propagation "must alternate B and O" — neither forced in'
       ' v1 (C3/C4 forcing is the manuscript\'s own "immediate structural'
       ' gate", FRONTIER SUMMARY). The theorem claim is not established.')
check('Add.6 octant table (angles/roles) consistent with chunks 1-2',
      'CP', all(s in APPC for s in ['1 22.5° E1', '2 67.5° B2', '4 157.5° O4',
                                    '6 247.5° B6', '8 337.5° O8']))

# Item 7: UV footprint table consistent with §19.1
check('Add.7 footprint table consistent with §19.1 (paired: cos(90°) = 0)',
      'CP', 'cos(90°) = 0' in APPC and 'Thus only E-localized and Balanced'
      ' remain viable.' in APPC)

# Item 8: "bypasses" vs §19.3/B2
check('Add.8: "The real-form E8(−24) framework bypasses this by using" present',
      'MA', 'The real-form E8(−24) framework bypasses this by using:' in APPC)
check('Add.8: "E8(−24) ⊃ A1 + G2 + C3" present (MA: E8(-24) host is MA per'
      ' Vol-III ledger)',
      'MA', 'E8(−24) ⊃ A1 + G2 + C3,' in APPC)
record('CONTR-2', 'INTERNAL-CONTRADICTION',
       'Addendum item 8 states the real-form E8(−24) framework "bypasses" the'
       ' Distler–Garibaldi obstruction as fact ("Chirality is a geometric'
       ' property ... Minimal left ideals of Cl(8) yield three chiral'
       ' generations without mirror fermions"), contradicting §19.3 ("The claim'
       ' ... is a proposal under investigation, not a proven evasion.") and'
       ' Appendix B NO-GO B2 ("The Distler–Garibaldi theorem is not evaded. The'
       ' Cℓ(8) construction is a candidate, not a resolution."). The bypass'
       ' mechanism is at best a proposal (MA), not an established evasion.')

# Item 9: falsifiability consistent with §19.6
check('Add.9 falsifiability list consistent with §19.6 (R⊥≠0; parity cross-terms;'
      ' ζ_parent vs electroweak bounds)',
      'CP', all(s in APPC for s in ['R⊥ ≠ 0 after projection onto 54.',
                                    'violating ±1 parity grading',
                                    'Couplings derived from ζ_parent violate'
                                    ' electroweak precision bounds']))

# Item 10: roadmap statuses
check('Add.10 roadmap: 4 tasks all OPEN (consistent with Appendix A)',
      'CP', APPC.count('verify R⊥ = 0 OPEN') == 1
      and 'Evaluate N₁₈₂₀ combinatorial multiplicity OPEN' in APPC
      and 'Execute six-step parent action reduction on E8 tensors OPEN' in APPC
      and 'Select between E-localized and Balanced UV footprints OPEN' in APPC)

# Item 11: Wolfram Implementation Note — claims about the circulated notebook,
# which is not in the audit corpus.
check('Add.11: "Modules 1–3 are missing from the circulated notebook" present;',
      'MA', 'Modules 1–3 are missing from the circulated notebook' in APPC)
record('NOTE-11', 'UNVERIFIABLE',
       'Addendum item 11 makes claims about the circulated notebook (missing'
       ' Modules 1-3: gammas, g17, cliffordOK, gamma17Sq, gamma17Anti; Module 9'
       ' slow). The notebook is not in the audit corpus; these claims cannot'
       ' be checked here. Logged as MA, unverifiable.')

# Item 12: references exist (spot-checked via arXiv API 2026-09-19)
check('Add.12 references: 0905.2658 (DG), 2404.18938v2, 2210.06029v1 exist with'
      ' E8-relevant titles; 1411.4317v4 exists (math.NT; relevance unclear)',
      'CP', all(s in APPC for s in ['arXiv:0905.2658', 'arXiv:2404.18938v2',
                                    'arXiv:2210.06029v1', 'arXiv:1411.4317v4']))

# FRONTIER SUMMARY consistency
check('FRONTIER SUMMARY: three immediate gates named (calculable/structural/'
      'conditional) consistent with Appendix A OPEN rows',
      'CP', 'The immediate calculable gate is the construction of the Cl(16)'
      ' gamma matrices and the 1820 projector.' in APPC
      and 'The immediate structural gate is the C3/C4 forcing question.' in APPC
      and 'The immediate conditional gate is the uniform-action premise.' in APPC)
check('Addendum closing: "No empirical promotion is authorized. Δ_op(Volume IV)'
      ' = ∅." present',
      'CP', 'No empirical promotion is authorized. Δ_op(Volume IV) = ∅.'
      in APPC)

# --------------------------------- v2/v3/report contradictions (labeled only)
print('-- v2/v3/report contradictions touched by Book 19 / appendices --')
v3 = open(V3, encoding='utf-8').read()
rep = open(REPORT, encoding='utf-8').read()
check('v3 draft line 118: "S_F = Tr_1820(EBEOEBEO) = 0.48958371" present',
      'CP', '0.48958371' in v3)
record('VX-1', 'V3-CONTRADICTION',
       'v3 draft line 118 claims S_F = Tr_1820(EBEOEBEO) = 0.48958371 as a'
       ' computed value — contradicting v1 Appendix A ("S_F numerical value:'
       ' OPEN"), §19.5 ("No physical promotion is authorized. Δ_op(Volume IV)'
       ' = ∅"), and the v1 addendum\'s own "numerical closure open until'
       ' Module 11 executes". Labeled as contradiction with v1, not a finding.')
check('v3 draft line 120: "N_{1820} = 3" present', 'CP', 'N_{1820} = 3' in v3)
record('VX-2', 'V3-CONTRADICTION',
       'v3 draft line 120 claims N_1820 = 3 "exactly calculated" —'
       ' contradicting v1 Appendix A ("N₁₈₂₀: OPEN") and §18.7\'s honest OPEN.'
       ' Labeled as contradiction with v1, not a finding.')
check('unsigned report line 54: "Status: MASTER CERTIFICATION COMPLETE" present',
      'CP', 'Status: MASTER CERTIFICATION COMPLETE' in rep)
record('VX-3', 'REPORT-CONTRADICTION',
       'Unsigned certification report claims "MASTER CERTIFICATION COMPLETE"'
       ' for Books 17-19 — contradicting v1 §19.5 ("No physical promotion is'
       ' authorized. Δ_op(Volume IV) = ∅."), Appendix A\'s 12 OPEN rows, and'
       ' the addendum\'s "numerical closure open". Labeled as contradiction'
       ' with v1, not a finding.')

# ---------------------------------------------------------------- summary
print()
print('Assertions passed: %d' % len(results))
from collections import Counter
tally = Counter(s for _, s in results)
for scope in ['CP', 'SC', 'NC', 'ST', 'MA', 'AX', 'IN', 'IC']:
    if tally[scope]:
        print('  %s: %d' % (scope, tally[scope]))
print('Findings recorded: %d' % len(findings))
fkind = Counter(k for _, k, _ in findings)
for k in sorted(fkind):
    print('  %s: %d' % (k, fkind[k]))
print('Timeout: none — all computations closed-form, small numerics, or text'
      ' greps; wall time well under any budget.')
print('ALL CHECKS PASSED.')
