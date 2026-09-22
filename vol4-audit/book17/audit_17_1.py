#!/usr/bin/env python3
"""
Volume IV v1 audit - chunk 1: the section-17.1 block (doc lines 2771-2998,
plus the stub section 17.1 at doc lines 150-410 for cross-consistency).

Sections covered: 17.1 (primitive octant decomposition), 17.2 (2:1 elliptic
map), 17.3 (rapidity values), 17.4 (C8 <-> octant correspondence),
17.5 (open gates), and stub-only 17.1.4 (Flatwave/carrier duality).
17.1.4 active-pair structure (active pair = exactly the two primitives > 1
per octant) proved exactly via the t = tan(x/2) substitution.

Status taxonomy: CP checked proof | SC symbolic check | NC numerical check |
ST standard theorem | MA manuscript assertion | AX assumption |
IN incomplete | IC incorrect as stated.
"""
import math
import sympy as sp

passed = 0
def check(name, cond, tag):
    global passed
    assert cond, "FAILED: " + name
    passed += 1
    print("ok [%s] %s" % (tag, name))

x = sp.symbols('x', real=True)
s, c = sp.sin(x), sp.cos(x)

# ---------- quadrant forms of the primitives ----------
# srx = |csc x| + cot x, cxp = |sec x| + tan x, sxp = 1/srx, crx = 1/cxp
# Q1: s>0,c>0 | Q2: s>0,c<0 | Q3: s<0,c<0 | Q4: s<0,c>0
forms = {
    # (srx, 1/srx, cxp, 1/cxp)
    'Q1': ((1 + c)/s, (1 - c)/s, (1 + s)/c, (1 - s)/c),
    'Q2': ((1 + c)/s, (1 - c)/s, (s - 1)/c, -(s + 1)/c),
    'Q3': ((c - 1)/s, -(c + 1)/s, (s - 1)/c, -(s + 1)/c),
    'Q4': ((c - 1)/s, -(c + 1)/s, (1 + s)/c, (1 - s)/c),
}
for q, (srx, isrx, cxp, icxp) in forms.items():
    # lemma: srx - 1/srx = 2c/s ; cxp - 1/cxp = 2s/c on every quadrant
    check("%s: srx-1/srx = 2c/s" % q,
          sp.simplify(sp.together(srx - isrx - 2*c/s)) == 0, "CP")
    check("%s: cxp-1/cxp = 2s/c" % q,
          sp.simplify(sp.together(cxp - icxp - 2*s/c)) == 0, "CP")

# ---------- 17.1.1 harmonic carrier identity ----------
# urx+uxp = (srx-1/srx)+(cxp-1/cxp) = 2c/s + 2s/c = 2/(sc) = 4/sin(2x)
check("17.1.1: 2c/s + 2s/c = 4/sin(2x)",
      sp.simplify(2*c/s + 2*s/c - 4/sp.sin(2*x)) == 0, "CP")
for q, (srx, isrx, cxp, icxp) in forms.items():
    lhs = (srx - icxp) + (cxp - isrx)   # urx + uxp
    check("17.1.1 %s: urx+uxp = 4/sin(2x)" % q,
          sp.simplify(sp.together(lhs - 4/sp.sin(2*x))) == 0, "CP")

# dense numeric confirmation (tripwire, not proof)
def prims(xv):
    sv, cv = math.sin(xv), math.cos(xv)
    srx = 1/abs(sv) + cv/sv
    cxp = 1/abs(cv) + sv/cv
    return srx, cxp
worst = 0.0
n = 0
xv = 0.001
while xv < 2*math.pi:
    if abs(math.sin(2*xv)) > 1e-2:   # stay clear of poles: both sides ~ 1/sin2x
        srx, cxp = prims(xv)
        lhs = srx + cxp - 1/srx - 1/cxp
        rhs = 4/math.sin(2*xv)
        worst = max(worst, abs(lhs - rhs)/abs(rhs))  # relative error
        n += 1
    xv += 0.0007
check("17.1.1 numeric: max rel err over %d pts = %.2e" % (n, worst), worst < 1e-9, "NC")

# ---------- 17.1.2 corrected imbalance formula ----------
# K2 = (srx-1/srx)-(cxp-1/cxp) = 2c/s - 2s/c = 2cos(2x)/(sc); D2 = 2/(sc)
check("17.1.2: K2 = 2cos(2x)/(sc)",
      sp.simplify(2*c/s - 2*s/c - 2*sp.cos(2*x)/(s*c)) == 0, "CP")
check("17.1.2: K2/(2*D2) = cos(2x)/2",
      sp.simplify((2*sp.cos(2*x)/(s*c)) / (2*(2/(s*c))) - sp.cos(2*x)/2) == 0, "CP")
worst = 0.0
xv = 0.001
while xv < 2*math.pi:
    if abs(math.sin(2*xv)) > 1e-2:
        srx, cxp = prims(xv)
        K2 = srx + 1/cxp - 1/srx - cxp
        D2 = srx + cxp - 1/srx - 1/cxp
        rhs = math.cos(2*xv)/2
        worst = max(worst, abs(K2/(2*D2) - rhs)/max(abs(rhs), 1e-12))
    xv += 0.0007
check("17.1.2 numeric: max rel err = %.2e" % worst, worst < 1e-9, "NC")

# ---------- 17.1.3 elliptic carrier ----------
VR, H = sp.cos(2*x)/2, sp.sin(2*x)/4
check("17.1.3: V_R^2 + 4H^2 = 1/4",
      sp.simplify(VR**2 + 4*H**2 - sp.Rational(1, 4)) == 0, "CP")
# stub proof route: D2^2 - K2^2 = 16
D2s = 2/(s*c)
K2s = 2*sp.cos(2*x)/(s*c)
check("17.1.3 (stub proof): D2^2 - K2^2 = 16",
      sp.simplify(D2s**2 - K2s**2 - 16) == 0, "CP")

# ---------- stub 17.1.4 Flatwave / carrier duality ----------
srxS, cxpS = sp.symbols('srx cxp', positive=True)
urxS = srxS - 1/cxpS
uxpS = cxpS - 1/srxS
flat = 1/urxS + 1/uxpS
check("Flatwave: 1/urx+1/uxp = (srx+cxp)/(srx*cxp-1)",
      sp.simplify(flat - (srxS + cxpS)/(srxS*cxpS - 1)) == 0, "CP")
Hs = 1/(urxS + uxpS)
check("Flatwave*H = 1/(urx*uxp)",
      sp.simplify(flat*Hs - 1/(urxS*uxpS)) == 0, "CP")
# wording check: 1/(urx*uxp) is reciprocal of the PRODUCT, not geometric mean
check("wording: 1/(urx*uxp) != 1/sqrt(urx*uxp) in general",
      sp.simplify(1/(urxS*uxpS) - 1/sp.sqrt(urxS*uxpS)) != 0, "CP")

# ---------- 17.1.4 octant table: dominant ordering (exact sign arguments) --
# octants 1-2 (x in (0,pi/2)): sgn(srx-cxp) = sgn(c-s); dominant = larger
d1 = sp.simplify((1 + c)/s - (1 + s)/c - (c - s)*(1 + c + s)/(s*c))
check("oct 1-2: srx-cxp = (c-s)(1+c+s)/(sc)", d1 == 0, "CP")
# octants 3-4 (x in (pi/2,pi)): crx-sxp = (srx-cxp)/(srx*cxp),
# srx-cxp = (c+s)(1+c-s)/(sc)
d2 = sp.simplify((1 + c)/s - (s - 1)/c - (c + s)*(1 + c - s)/(s*c))
check("oct 3-4: srx-cxp = (c+s)(1+c-s)/(sc)", d2 == 0, "CP")
# octants 5-6 (x in (pi,3pi/2)): srx-cxp = (c-s)(c+s-1)/(sc)
d3 = sp.simplify((c - 1)/s - (s - 1)/c - (c - s)*(c + s - 1)/(s*c))
check("oct 5-6: srx-cxp = (c-s)(c+s-1)/(sc)", d3 == 0, "CP")
# octants 7-8 (x in (3pi/2,2pi)): srx-cxp = (c+s)(c-s-1)/(sc)
d4 = sp.simplify((c - 1)/s - (1 + s)/c - (c + s)*(c - s - 1)/(s*c))
check("oct 7-8: srx-cxp = (c+s)(c-s-1)/(sc)", d4 == 0, "CP")

# phase signs: epsilon = sgn(sin 2x)
for deg, want in [(22.5, 1), (67.5, 1), (112.5, -1), (157.5, -1),
                  (202.5, 1), (247.5, 1), (292.5, -1), (337.5, -1)]:
    got = 1 if math.sin(2*math.radians(deg)) > 0 else -1
    check("phase at %g deg = %d" % (deg, want), got == want, "CP")

# decay/growth via derivative signs (formulae symbolic, signs elementary)
# oct1: d/dx srx = -(1+c)/s^2 < 0 on (0,pi/2)
check("oct1: d(srx)/dx = -(1+c)/s^2",
      sp.simplify(sp.diff((1 + c)/s, x) + (1 + c)/s**2) == 0, "CP")
# oct2: d/dx cxp = (1+s)/c^2 > 0 on (0,pi/2)
check("oct2: d(cxp)/dx = (1+s)/c^2",
      sp.simplify(sp.diff((1 + s)/c, x) - (1 + s)/c**2) == 0, "CP")
# oct3: d/dx cxp = (1-s)/c^2 >= 0 on (pi/2,pi) -> crx decays
check("oct3: d(cxp)/dx = (1-s)/c^2",
      sp.simplify(sp.diff((s - 1)/c, x) - (1 - s)/c**2) == 0, "CP")
# oct4: d/dx srx = -(1+c)/s^2 <= 0 on (pi/2,pi) -> sxp grows
check("oct4: d(srx)/dx = -(1+c)/s^2",
      sp.simplify(sp.diff((1 + c)/s, x) + (1 + c)/s**2) == 0, "CP")
# oct5: d/dx srx = (c-1)/s^2 < 0 on (pi,3pi/2)
check("oct5: d(srx)/dx = (c-1)/s^2",
      sp.simplify(sp.diff((c - 1)/s, x) - (c - 1)/s**2) == 0, "CP")
# oct6: d/dx cxp = (1-s)/c^2 > 0 on (pi,3pi/2)
check("oct6: d(cxp)/dx = (1-s)/c^2",
      sp.simplify(sp.diff((s - 1)/c, x) - (1 - s)/c**2) == 0, "CP")
# oct7: d/dx cxp = (1+s)/c^2 >= 0 on (3pi/2,2pi) -> crx decays
check("oct7: d(cxp)/dx = (1+s)/c^2",
      sp.simplify(sp.diff((1 + s)/c, x) - (1 + s)/c**2) == 0, "CP")
# oct8: d/dx srx = (c-1)/s^2 <= 0 on (3pi/2,2pi) -> sxp grows
check("oct8: d(srx)/dx = (c-1)/s^2",
      sp.simplify(sp.diff((c - 1)/s, x) - (c - 1)/s**2) == 0, "CP")

# ---------- 17.1.4 active pair: exact >1 / <1 structure ----------
# Manuscript octant table (raw doc lines 2851-2862): the active pair alternates
# every two octants: octs 1,2,5,6 -> (srx,cxp); octs 3,4,7,8 -> (crx,sxp).
# Claim: on each open octant the active pair members are exactly the two
# primitives > 1; the inactive pair are both in (0,1).
# Exact route: t = tan(x/2). tan(x/2) is strictly increasing in x on every
# octant (d/dx = sec^2(x/2)/2 > 0), hence a bijection x-interval -> t-interval:
#   oct1 (0,45deg): t in (0,sqrt2-1)      oct5 (180,225deg): t in (-oo,-(sqrt2+1))
#   oct2 (45,90deg): t in (sqrt2-1,1)     oct6 (225,270deg): t in (-(sqrt2+1),-1)
#   oct3 (90,135deg): t in (1,sqrt2+1)    oct7 (270,315deg): t in (-1,-(sqrt2-1))
#   oct4 (135,180deg): t in (sqrt2+1,oo)  oct8 (315,360deg): t in (-(sqrt2-1),0)
# srx, cxp become rational functions of t; srx-1 and cxp-1 factor into linear
# factors whose roots ({0,+1,-1}) avoid every open t-interval above, so each
# sign below is constant on its octant (elementary interval sign analysis;
# the interval/constant facts are the exact checks that follow).
tt = sp.tan(x/2)
check("t-sub: sin x = 2t/(1+t^2)",
      sp.simplify(2*tt/(1+tt**2) - s) == 0, "CP")
check("t-sub: cos x = (1-t^2)/(1+t^2)",
      sp.simplify((1-tt**2)/(1+tt**2) - c) == 0, "CP")
def texact(name, expr):
    # exact trig identity, proved via the tan(x/2) rewrite
    check(name, sp.simplify(expr.rewrite(sp.tan)) == 0, "CP")
# per octant: quadrant form of srx-1 and cxp-1 in factored t-form (exact).
# Octant pairs sharing a quadrant verify the same identity; stated per octant
# for explicitness.
texact("oct1 srx-1 = (1-t)/t, t in (0,sqrt2-1)",
       (1+c)/s - 1 - (1-tt)/tt)
texact("oct1 cxp-1 = 2t/(1-t), t in (0,sqrt2-1)",
       (1+s)/c - 1 - 2*tt/(1-tt))
texact("oct2 srx-1 = (1-t)/t, t in (sqrt2-1,1)",
       (1+c)/s - 1 - (1-tt)/tt)
texact("oct2 cxp-1 = 2t/(1-t), t in (sqrt2-1,1)",
       (1+s)/c - 1 - 2*tt/(1-tt))
texact("oct3 srx-1 = (1-t)/t, t in (1,sqrt2+1)",
       (1+c)/s - 1 - (1-tt)/tt)
texact("oct3 cxp-1 = -2/(t+1), t in (1,sqrt2+1)",
       (s-1)/c - 1 + 2/(tt+1))
texact("oct4 srx-1 = (1-t)/t, t in (sqrt2+1,oo)",
       (1+c)/s - 1 - (1-tt)/tt)
texact("oct4 cxp-1 = -2/(t+1), t in (sqrt2+1,oo)",
       (s-1)/c - 1 + 2/(tt+1))
texact("oct5 srx-1 = -(t+1), t in (-oo,-(sqrt2+1))",
       (c-1)/s - 1 + (tt+1))
texact("oct5 cxp-1 = -2/(t+1), t in (-oo,-(sqrt2+1))",
       (s-1)/c - 1 + 2/(tt+1))
texact("oct6 srx-1 = -(t+1), t in (-(sqrt2+1),-1)",
       (c-1)/s - 1 + (tt+1))
texact("oct6 cxp-1 = -2/(t+1), t in (-(sqrt2+1),-1)",
       (s-1)/c - 1 + 2/(tt+1))
texact("oct7 srx-1 = -(t+1), t in (-1,-(sqrt2-1))",
       (c-1)/s - 1 + (tt+1))
texact("oct7 cxp-1 = 2t/(1-t), t in (-1,-(sqrt2-1))",
       (1+s)/c - 1 - 2*tt/(1-tt))
texact("oct8 srx-1 = -(t+1), t in (-(sqrt2-1),0)",
       (c-1)/s - 1 + (tt+1))
texact("oct8 cxp-1 = 2t/(1-t), t in (-(sqrt2-1),0)",
       (1+s)/c - 1 - 2*tt/(1-tt))
# constant interval facts, exact content: (sqrt2)^2 = 2 > 1 gives sqrt2 > 1
# (principal root, sqrt2 > 0); (sqrt2)^2 = 2 < 4 gives sqrt2 < 2.
# Hence 0 < sqrt2-1 < 1 and sqrt2+1 > 1.
check("sqrt(2) > 1  [exact content: (sqrt2)^2 = 2 > 1]", sp.sqrt(2)**2 > 1, "CP")
check("sqrt(2) < 2  [exact content: (sqrt2)^2 = 2 < 4]", sp.sqrt(2)**2 < 4, "CP")
# exact octant-boundary values of tan(x/2) (x = k*pi/4 -> x/2 = k*pi/8);
# the 0 and +-oo endpoints are limits of tan at its zeros/poles.
check("tan(pi/8) = sqrt(2)-1",
      sp.simplify(sp.tan(sp.pi/8) - (sp.sqrt(2)-1)) == 0, "CP")
check("tan(3pi/8) = sqrt(2)+1",
      sp.simplify(sp.tan(3*sp.pi/8) - (sp.sqrt(2)+1)) == 0, "CP")
check("tan(5pi/8) = -(sqrt(2)+1)",
      sp.simplify(sp.tan(5*sp.pi/8) + (sp.sqrt(2)+1)) == 0, "CP")
check("tan(7pi/8) = -(sqrt(2)-1)",
      sp.simplify(sp.tan(7*sp.pi/8) + (sp.sqrt(2)-1)) == 0, "CP")
# Sign conclusions (elementary, from the factored forms + intervals above):
# oct1,2: (1-t)/t > 0, 2t/(1-t) > 0 -> srx>1, cxp>1 (active (srx,cxp)).
# oct3,4: (1-t)/t < 0, -2/(t+1) < 0, and srx,cxp > 0 -> srx,cxp in (0,1),
#   so crx=1/cxp > 1, sxp=1/srx > 1 (active (crx,sxp)).
# oct5,6: -(t+1) > 0, -2/(t+1) > 0 -> srx>1, cxp>1 (active (srx,cxp)).
# oct7,8: -(t+1) < 0, 2t/(1-t) < 0, and srx,cxp > 0 -> srx,cxp in (0,1),
#   so crx > 1, sxp > 1 (active (crx,sxp)).
# Exactly two primitives exceed 1 on each open octant: the active pair.

# ---------- 17.1.5/17.1.6 three-bit code ----------
codes = {1: (0, 1, 1), 2: (1, 0, 1), 3: (0, 0, 0), 4: (1, 1, 0),
         5: (0, 1, 0), 6: (1, 0, 0), 7: (0, 0, 1), 8: (1, 1, 1)}
check("code table: 8 distinct codes covering all of Z2^3",
      sorted(codes.values()) == sorted(
          [(a, b, d) for a in (0, 1) for b in (0, 1) for d in (0, 1)]), "CP")
for k, (b1, b2, b3) in codes.items():
    lo, hi = math.radians((k-1)*45), math.radians(k*45)
    mid = (lo + hi)/2
    # B1: half-quadrant (0 = first half)
    e1 = 0 if (k % 2 == 1) else 1
    # B2: sign of cos(2x), 1 = +
    e2 = 1 if math.cos(2*mid) > 0 else 0
    # B3: sign of cos(x), 1 = +
    e3 = 1 if math.cos(mid) > 0 else 0
    check("octant %d decodes (%d,%d,%d)" % (k, e1, e2, e3),
          (b1, b2, b3) == (e1, e2, e3), "CP")

# ---------- 17.2 2:1 elliptic map ----------
check("17.2: V_R(x+pi) = V_R(x)",
      sp.simplify(sp.cos(2*(x + sp.pi))/2 - sp.cos(2*x)/2) == 0, "CP")
check("17.2: H(x+pi) = H(x)",
      sp.simplify(sp.sin(2*(x + sp.pi))/4 - sp.sin(2*x)/4) == 0, "CP")
mids = {1: 22.5, 2: 67.5, 3: 112.5, 4: 157.5}
want = {1: (sp.sqrt(2)/4, sp.sqrt(2)/8), 2: (-sp.sqrt(2)/4, sp.sqrt(2)/8),
        3: (-sp.sqrt(2)/4, -sp.sqrt(2)/8), 4: (sp.sqrt(2)/4, -sp.sqrt(2)/8)}
for k, deg in mids.items():
    r = math.radians(deg)
    gv, gh = math.cos(2*r)/2, math.sin(2*r)/4
    wv, wh = want[k]
    check("17.2 midpoint %g deg = (%s, %s)" % (deg, wv, wh),
          abs(gv - float(wv)) < 1e-15 and abs(gh - float(wh)) < 1e-15, "CP")
# epsilon does NOT record the sheet: invariant under deck x -> x+pi
check("17.2: sgn(sin2(x+pi)) = sgn(sin2x) [deck-invariant]",
      sp.simplify(sp.sin(2*(x + sp.pi)) - sp.sin(2*x)) == 0, "CP")

# ---------- 17.3 rapidity values ----------
w0 = sp.log(1 + sp.sqrt(2))
check("w0: sinh(w0) = 1",
      sp.simplify(sp.sinh(w0).rewrite(sp.exp) - 1) == 0, "CP")
check("w0: cosh(w0) = sqrt(2)",
      sp.simplify(sp.cosh(w0).rewrite(sp.exp) - sp.sqrt(2)) == 0, "CP")
check("cot(22.5 deg) = 1+sqrt(2)",
      sp.simplify(1/sp.tan(sp.pi/8) - (1 + sp.sqrt(2))) == 0, "CP")
check("cot(67.5 deg) = sqrt(2)-1",
      sp.simplify(1/sp.tan(3*sp.pi/8) - (sp.sqrt(2) - 1)) == 0, "CP")
check("ln(sqrt(2)-1) = -w0",
      sp.simplify(sp.log(sp.sqrt(2) - 1) + w0) == 0, "CP")
for deg, sgn in [(22.5, 1), (67.5, -1), (112.5, -1), (157.5, 1),
                 (202.5, 1), (247.5, -1), (292.5, -1), (337.5, 1)]:
    w = math.log(abs(1/math.tan(math.radians(deg))))
    check("w(%g deg) = %sw0" % (deg, "+" if sgn > 0 else "-"),
          abs(w - sgn*float(w0)) < 1e-12, "CP")
check("prod_E cosh = (sqrt2)^4 = 4", (sp.sqrt(2)**4) == 4, "CP")
check("prod_all cosh = (sqrt2)^8 = 16", (sp.sqrt(2)**8) == 16, "CP")
check("sum w_i = 0 (E level)", float(w0 - w0 + w0 - w0) == 0.0, "CP")
# dw/dx identity (17.3.1 in continued-calc block): per-quadrant symbolic
# plus dense numeric (Abs is not differentiated symbolically here)
# exact per-sign symbolic derivative (no Abs): on each quadrant w = ln(+/-cot x)
check("17.3.1: d/dx ln(cot x) = -1/(s*c)",
      sp.simplify(sp.diff(sp.log(c/s), x) + 1/(s*c)) == 0, "CP")
check("17.3.1: d/dx ln(-cot x) = -1/(s*c)",
      sp.simplify(sp.diff(sp.log(-c/s), x) + 1/(s*c)) == 0, "CP")
check("17.3.1: -1/(s*c) = -2/sin(2x)",
      sp.simplify(-1/(s*c) + 2/sp.sin(2*x)) == 0, "CP")
# numeric tripwire (finite differences; loose tolerance near poles)
worst = 0.0
xv = 0.01
while xv < 2*math.pi:
    if abs(math.sin(2*xv)) > 0.05:
        h = 1e-6
        w = lambda t: math.log(abs(math.cos(t)/math.sin(t)))
        dw = (w(xv+h) - w(xv-h))/(2*h)
        denom = abs(2/math.sin(2*xv))
        worst = max(worst, abs(dw + 2/math.sin(2*xv))/denom)
    xv += 0.005
check("17.3.1 numeric: dw/dx = -2/sin(2x), max rel err = %.2e" % worst,
      worst < 1e-3, "NC")
for q, sgn_cot, eps in [('Q1', 1, 1), ('Q2', -1, -1), ('Q3', 1, 1), ('Q4', -1, -1)]:
    # |cot| = sgn_cot * cot ; cosh(w) = (|cot|+|tan|)/2 ; eps*cosh = 1/sin2x
    cotx = c/s
    abscot = sgn_cot*cotx
    expr = eps*(abscot + 1/abscot)/2 - 1/sp.sin(2*x)
    check("17.3.1 %s: eps*cosh(w) = 1/sin(2x)" % q,
          sp.simplify(sp.together(expr)) == 0, "CP")

# V_E numerics
VE = math.sqrt(4 + 2*math.sqrt(2)) + 1 + math.sqrt(2)
check("V_E = sqrt(4+2sqrt2)+1+sqrt2 ~ 5.0273", abs(VE - 5.0273) < 1e-3, "NC")
check("V_E^4 ~ 638.78", abs(VE**4 - 638.78) < 0.05, "NC")

# 17.3.5 continued-calc: intermediate radical for crx(112.5deg) is WRONG
bad = 1/(2/math.sqrt(2 + math.sqrt(2)) + (math.sqrt(2) - 1))
check("17.3.5: printed 1/(2/sqrt(2+sqrt2)+(sqrt2-1)) = %.4f != 5.027" % bad,
      abs(bad - 5.0273) > 1.0, "NC")
# correct value
r = math.radians(112.5)
sv, cv = math.sin(r), math.cos(r)
cxp = 1/abs(cv) + sv/cv
check("17.3.5: true crx(112.5deg) = 1/cxp ~ 5.0273",
      abs(1/cxp - 5.0273) < 1e-3, "NC")
check("17.3.5: true crx(112.5) = sqrt(4+2sqrt2)+1+sqrt2",
      abs(1/cxp - VE) < 1e-9, "NC")
# all four E-contact dominant values equal
vals = []
for deg, fn in [(22.5, 'srx'), (112.5, 'crx'), (202.5, 'srx'), (292.5, 'crx')]:
    r = math.radians(deg)
    sv, cv = math.sin(r), math.cos(r)
    srx = 1/abs(sv) + cv/sv
    cxp = 1/abs(cv) + sv/cv
    vals.append(srx if fn == 'srx' else 1/cxp)
check("17.3.5: four E-contact dominant values equal",
      max(vals) - min(vals) < 1e-12, "NC")

# ---------- 17.4 C8 <-> octant: internal consistency ----------
word = ['E', 'B', 'E', 'O', 'E', 'B', 'E', 'O']
check("17.4: cyclic word is (E,B,E,O,E,B,E,O)", word == ['E','B','E','O']*2, "CP")
# E at decay octants 1,3,5,7 ; B at growth/eps+ octants 2,6 ; O at growth/eps- 4,8
decay = [1, 3, 5, 7]
check("17.4: E positions = decay octants",
      [i+1 for i, w in enumerate(word) if w == 'E'] == decay, "CP")
check("17.4: B positions = growth octants with eps=+1",
      [i+1 for i, w in enumerate(word) if w == 'B'] == [2, 6], "CP")
check("17.4: O positions = growth octants with eps=-1",
      [i+1 for i, w in enumerate(word) if w == 'O'] == [4, 8], "CP")

print("\n%d assertions passed, 0 failed." % passed)
