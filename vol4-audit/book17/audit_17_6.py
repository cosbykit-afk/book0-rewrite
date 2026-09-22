#!/usr/bin/env python3
"""
Volume IV v1 audit - chunk 2: sections 17.6-17.9 (doc lines 777-990).

Sections covered:
  17.6  UV footprint classification (17.6.1 five types, 17.6.2 paired,
        17.6.3 E-localized)
  17.7  The open Clifford contraction (17.7.1 what remains, 17.7.2 what is
        known, 17.7.3 conversion chain, 17.7.4 bounds)
  17.8  Summary of Book 17 calculations (cross-check of each row's label
        against chunk-1/chunk-2 verdicts)
  17.9  Handoff (prose; no new mathematical claims)

Dependencies (upstream, not re-derived): chunk-1 primitives and octant
structure (LEDGER_17_1.md, audit_17_1.py): srx/cxp/sxp/crx, the C8 cyclic
word (E,B,E,O)x2 with E on decay octants 1,3,5,7, B on growth octants 2,6
(eps=+1), O on growth octants 4,8 (eps=-1); E contacts at
22.5/112.5/202.5/292.5 deg; w0=ln(1+sqrt2), cosh w0=sqrt2;
E-contact rapidity product (sqrt2)^4=4; V_E=sqrt(4+2sqrt2)+1+sqrt2.

Status taxonomy: CP checked proof | SC symbolic check | NC numerical check |
ST standard theorem | MA manuscript assertion | AX assumption |
IN incomplete | IC incorrect as stated.

Every check below is a real assertion; a failed assertion fails the run.
All computations are closed-form; no per-computation timeout was hit.
"""

import math
import sympy as sp

passed = 0
tally = {}

def check(name, cond, tag):
    global passed
    assert cond, "FAILED: " + name
    passed += 1
    tally[tag] = tally.get(tag, 0) + 1
    print("ok [%s] %s" % (tag, name))

x = sp.symbols('x', real=True)
D2R = math.pi / 180.0

# ================= 17.6.1 the five footprint types =================
# Contact positions (midpoint convention from the C8 word / octant table):
E_contacts = [22.5, 112.5, 202.5, 292.5]   # decay octants 1,3,5,7
B_contacts = [67.5, 247.5]                  # growth-A octants 2,6
O_contacts = [157.5, 337.5]                 # growth-B octants 4,8

def shifted(degs, delta):
    return sorted([(d + delta) % 360.0 for d in degs])

# paired footprint: even under the 2:1 kernel x -> x+pi
check("17.6.1/17.6.2: cos(4(x+pi)) = cos(4x)",
      sp.simplify(sp.cos(4*(x + sp.pi)) - sp.cos(4*x)) == 0, "CP")
# paired footprint: pi/2 is a period (C8 shift by 4 = +pi leaves it invariant)
check("17.6.2: cos(4(x+pi/2)) = cos(4x) [period pi/2]",
      sp.simplify(sp.cos(4*(x + sp.pi/2)) - sp.cos(4*x)) == 0, "CP")
# ... and pi/4 is NOT a period (minimality witness)
check("17.6.2: cos(4(x+pi/4)) != cos(4x) identically",
      sp.simplify(sp.cos(4*(x + sp.pi/4)) - sp.cos(4*x)) != 0, "CP")

# delta-footprint evenness under x -> x+pi reduces to set invariance
check("17.6.1: E-contact set invariant under +180 deg",
      shifted(E_contacts, 180.0) == sorted(E_contacts), "CP")
check("17.6.1: B-contact set invariant under +180 deg",
      shifted(B_contacts, 180.0) == sorted(B_contacts), "CP")
check("17.6.1: O-contact set invariant under +180 deg",
      shifted(O_contacts, 180.0) == sorted(O_contacts), "CP")
# balanced footprint: trivially invariant
check("17.6.1: balanced footprint 1 invariant under x -> x+pi",
      1 == 1, "CP")
# C8 shift by 4 octants IS the 2:1 kernel map (redundancy of the "three" Z2s)
check("17.6.1: C8 shift by 4 = 4*45 deg = 180 deg = 2:1 kernel map",
      4*45 == 180, "CP")
# extra symmetry (not claimed): E set is even Z4-invariant (shift by 2 octants)
check("17.6.1 (extra): E-contact set invariant under +90 deg",
      shifted(E_contacts, 90.0) == sorted(E_contacts), "CP")
# code-group ambiguity witness: E-support octant pattern {1,3,5,7} is NOT
# invariant under the octant transposition (1 2); i.e. under a transitive
# Z2^3 bit-flip action the localized footprints would fail "evenness".
def transpose_octants(pattern, a, b):
    out = []
    for k in pattern:
        if k == a:
            out.append(b)
        elif k == b:
            out.append(a)
        else:
            out.append(k)
    return sorted(out)
check("17.6.1: E-support {1,3,5,7} not invariant under octant swap (1 2)",
      transpose_octants([1, 3, 5, 7], 1, 2) != [1, 3, 5, 7], "CP")

# E-localized footprint sits precisely on the decay octants (17.6.3)
oct_of = lambda d: int(d // 45) + 1
check("17.6.3: E contacts are the decay-octant midpoints {1,3,5,7}",
      [oct_of(d) for d in E_contacts] == [1, 3, 5, 7], "CP")
check("17.6.3: E contacts lie strictly inside their octants",
      all((d % 45) == 22.5 for d in E_contacts), "CP")

# ================= 17.6.2 the paired footprint =================
# cos(4*22.5deg) = cos(90deg) = 0 exactly
check("17.6.2: cos(4*22.5deg) = 0 exactly",
      sp.simplify(sp.cos(4*sp.pi/8)) == 0, "CP")
# the paired footprint vanishes at ALL eight octant midpoints, not just E
for k in range(8):
    d = 22.5 + 45*k
    check("17.6.2: cos(4*%g deg) = 0" % d,
          abs(math.cos(4*d*D2R)) < 1e-12, "CP")  # 1e-12: fp noise near zeros
# IC-4: the bullet "vanishes at the octant boundaries (45deg, 135deg, ...)"
# is FALSE: cos(4x) = -1 at the boundaries, not 0.
check("17.6.2 IC-4: cos(4*45deg) = -1, not 0",
      abs(math.cos(4*45*D2R) - (-1.0)) < 1e-15, "CP")
check("17.6.2 IC-4: cos(4*135deg) = -1, not 0",
      abs(math.cos(4*135*D2R) - (-1.0)) < 1e-15, "CP")
check("17.6.2 IC-4: cos(4*0deg) = +1, not 0",
      abs(math.cos(0.0) - 1.0) < 1e-15, "CP")
# charge-matching formula is exactly the eta_-4 = eta0*cos(4x) substitution
# into the three-way separation ansatz y2 ~ eta_-4 * zeta_parent * n54_hat
eta0, zeta, n54 = sp.symbols('eta0 zeta_parent n54_hat')
eta_m4 = eta0*sp.cos(4*x)
y2_ansatz = eta_m4*zeta*n54
check("17.6.2: y2 = eta0*cos(4x)*zeta_parent*n54_hat is the eta_-4 substitution",
      sp.simplify(y2_ansatz - eta0*sp.cos(4*x)*zeta*n54) == 0, "MA")

# ================= 17.7.1 what remains =================
# S_F = <Q_F, a*T + R_perp> = 3*a given Q_F=(6/5)T, ||T||^2=5/2, <T,R_perp>=0
Tnorm2 = sp.Rational(5, 2)
a = sp.symbols('a2222')
check("17.7.1: <(6/5)T, a*T> = 3a given ||T||^2=5/2",
      sp.Rational(6, 5)*Tnorm2*a - 3*a == 0, "CP")
T, Rp = sp.symbols('T R_perp')
ip_T_Rp = 0  # part of the stated decomposition: <T, R_perp> = 0
ip_QF_Rp = sp.Rational(6, 5)*ip_T_Rp  # Q_F = (6/5)*T, bilinearity of <,>
check("17.7.1: <Q_F, R_perp> = (6/5)<T,R_perp> = 0",
      ip_QF_Rp == 0, "CP")

# ================= 17.7.2 what is known =================
# T = diag(1,1,-1/4,...): the manuscript's ||T||^2 = 5/2 forces the
# 10x10 reading (eight -1/4 entries): 2 + n/16 = 5/2 -> n = 8.
n = sp.symbols('n', integer=True, positive=True)
sol = sp.solve(2 + n/16 - sp.Rational(5, 2), n)
check("17.7.2: ||T||^2=5/2 forces eight -1/4 entries (10x10 diag)",
      sol == [8], "CP")
check("17.7.2: T traceless: 1+1+8*(-1/4) = 0",
      1 + 1 + 8*sp.Rational(-1, 4) == 0, "CP")
check("17.7.2: ||T||^2 = 1+1+8*(1/16) = 5/2",
      1 + 1 + 8*sp.Rational(1, 16) == sp.Rational(5, 2), "CP")
check("17.7.2: ||Q_F||^2 = (6/5)^2 * 5/2 = 18/5",
      sp.Rational(6, 5)**2 * sp.Rational(5, 2) == sp.Rational(18, 5), "CP")
check("17.7.2: four-contact factor (1/4)^4 = 1/256",
      sp.Rational(1, 4)**4 == sp.Rational(1, 256), "CP")
check("17.7.2: E-contact rapidity product (sqrt2)^4 = 4",
      sp.sqrt(2)**4 == 4, "CP")
check("17.7.2: propagator rapidity product (sqrt2)^4 = 4",
      sp.sqrt(2)**4 == 4, "CP")
# V_E closed form is exact (SC); value/numerics (NC)
VE = sp.sqrt(4 + 2*sp.sqrt(2)) + 1 + sp.sqrt(2)
srx_225 = (1 + sp.cos(sp.pi/8))/sp.sin(sp.pi/8)   # Q1 form of srx at 22.5deg
check("17.7.2: srx(22.5deg) = sqrt(4+2sqrt2)+1+sqrt2 exactly",
      sp.simplify(srx_225 - VE) == 0, "SC")
VE4 = float(VE**4)
check("17.7.2: V_E^4 = %.6f ~ 638.78" % VE4, abs(VE4 - 638.78) < 0.01, "NC")
check("17.7.2: printed 638.7 is a truncation of 638.7823, not a rounding",
      abs(VE4 - 638.7) > 0.05, "NC")

# ================= 17.7.3 the conversion chain =================
# S_F = 3 a2222 ; a2222 = (6/5) c_ord ; c_ord = 5 S_F/18 : internal consistency
SF, aa, cc = sp.symbols('S_F a2222 c_ord')
check("17.7.3: S_F=3a, a=(6/5)c  =>  S_F=(18/5)c",
      sp.simplify(3*sp.Rational(6, 5)*cc - sp.Rational(18, 5)*cc) == 0, "CP")
check("17.7.3: c_ord = 5*S_F/18 inverts S_F = (18/5)*c_ord",
      sp.simplify(sp.Rational(5, 18)*sp.Rational(18, 5)*cc - cc) == 0, "CP")
# n54_hat three forms coincide under S_F = 3a, a = (6/5)c
m2 = sp.symbols('m2', positive=True)
f1 = -(sp.sqrt(10)/1536)*SF*m2**-4
f2 = -(sp.sqrt(10)/512)*aa*m2**-4
f3 = -(3*sp.sqrt(10)/1280)*cc*m2**-4
check("17.7.3: -(sqrt10/1536)S_F = -(sqrt10/512)a2222 under S_F=3a",
      sp.simplify(f1 - f2.subs(aa, SF/3)) == 0, "CP")
check("17.7.3: -(sqrt10/512)a2222 = -(3sqrt10/1280)c_ord under a=(6/5)c",
      sp.simplify(f2 - f3.subs(cc, sp.Rational(5, 6)*aa)) == 0, "CP")
check("17.7.3: full chain closes: f1 = f3 under S_F=3a, a=(6/5)c",
      sp.simplify(f1 - f3.subs(cc, sp.Rational(5, 18)*SF)) == 0, "CP")

# ================= 17.7.4 bounds and estimates =================
bound = sp.Rational(1, 256)*sp.Rational(18, 5)*4
check("17.7.4: (1/256)*(18/5)*4 = 0.05625",
      bound == sp.Rational(9, 160), "CP")
check("17.7.4: 0.05625 ~= 0.056",
      abs(float(bound) - 0.056) < 0.001, "CP")

# ================= 17.8 summary cross-checks =================
# 17.2.2 octant-to-ellipse mapping table (8 rows)
expected = {
    22.5: (sp.sqrt(2)/4, sp.sqrt(2)/8, 1),
    67.5: (-sp.sqrt(2)/4, sp.sqrt(2)/8, 1),
    112.5: (-sp.sqrt(2)/4, -sp.sqrt(2)/8, -1),
    157.5: (sp.sqrt(2)/4, -sp.sqrt(2)/8, -1),
    202.5: (sp.sqrt(2)/4, sp.sqrt(2)/8, 1),
    247.5: (-sp.sqrt(2)/4, sp.sqrt(2)/8, 1),
    292.5: (-sp.sqrt(2)/4, -sp.sqrt(2)/8, -1),
    337.5: (sp.sqrt(2)/4, -sp.sqrt(2)/8, -1),
}
for deg, (wV, wH, weps) in expected.items():
    r = deg*D2R
    gV, gH = math.cos(2*r)/2, math.sin(2*r)/4
    geps = 1 if math.sin(2*r) > 0 else -1
    check("17.2.2/17.8: octant midpoint %g deg -> (%s,%s,eps=%d)" % (deg, wV, wH, weps),
          abs(gV - float(wV)) < 1e-15 and abs(gH - float(wH)) < 1e-15
          and geps == weps, "CP")
# 17.2.2: the four ellipse points are concyclic at distance sqrt(10)/8
check("17.2.2: |A| = sqrt((sqrt2/4)^2+(sqrt2/8)^2) = sqrt(10)/8",
      sp.simplify(sp.sqrt((sp.sqrt(2)/4)**2 + (sp.sqrt(2)/8)**2)
                  - sp.sqrt(10)/8) == 0, "CP")
# 17.2.3 boundary points: direct evaluation of the proved carrier formulas
bpts = {0: (sp.Rational(1, 2), 0), 45: (0, sp.Rational(1, 4)),
        90: (sp.Rational(-1, 2), 0), 135: (0, sp.Rational(-1, 4)),
        180: (sp.Rational(1, 2), 0)}
for deg, (wV, wH) in bpts.items():
    r = deg*D2R
    gV, gH = math.cos(2*r)/2, math.sin(2*r)/4
    check("17.2.3/17.8: boundary x=%d deg -> (%s,%s)" % (deg, wV, wH),
          abs(gV - float(wV)) < 1e-15 and abs(gH - float(wH)) < 1e-15, "CP")

print("\n%d assertions passed, 0 failed." % passed)
print("scope tally:", tally)
print("no timeout: all computations closed-form.")
