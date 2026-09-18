#!/usr/bin/env python3
"""R = (1/3) O_V, and the proof of the shell criterion that follows from it.

The paper says R is a group and not a ring, which is true, and stops there.  But
3R IS a ring: it is the maximal order of V = Q(sqrt33, i sqrt3), the Q-span of R.
That one fact carries the arithmetic of sections 4 and 6:

  * |z|^2 = z zbar is the relative norm N_{V/F} for F = Q(sqrt33), so a is a
    squared radius of R exactly when 9a is a relative norm of an ALGEBRAIC INTEGER;
  * the two colourings are reduction to the residue fields O_V/pi_i = F_4.  Since
    pi_1, pi_2 are coprime, R/2R = F_4 x F_4; a unit vector has |u|^2 = 1, so it
    is invertible in both factors, and the nine such classes are exactly the nine
    the thirty unit vectors occupy.  A plane missing all nine has every element on
    a coordinate axis, so it is a union of two subgroups, so it IS one of them --
    which is why exactly two index-4 subgroups avoid all thirty, and which one
    each is.  Stability is the wrong invariant: eleven of the 35 planes are
    O-stable;
  * and the shell criterion becomes a theorem, by the Hasse norm theorem.

This checks every ingredient.  The first half needs no external library; the
second uses PARI through cypari for the class numbers, the unit and the splitting.

Run: .venv/bin/python scripts/moser_is_ov.py
"""
from fractions import Fraction as F
import math, sys

FAIL = []
def check(label, got, want):
    ok = got == want
    if not ok: FAIL.append((label, got, want))
    print(f"  {'ok ' if ok else 'BAD'} {label:<54} {str(got):>22}"
          + ("" if ok else f"  expected {want}"))

# ---------------------------------------------------------------- R, exactly
def mul(x, y):                      # basis 1, sqrt33, i sqrt3, i sqrt11
    a1,a2,a3,a4 = x; b1,b2,b3,b4 = y
    return (a1*b1 + 33*a2*b2 - 3*a3*b3 - 11*a4*b4,
            a1*b2 + a2*b1 - (a3*b4 + a4*b3),
            a1*b3 + a3*b1 + 11*(a2*b4 + a4*b2),
            a1*b4 + a4*b1 + 3*(a2*b3 + a3*b2))
ONE=(F(1),F(0),F(0),F(0)); ZETA=(F(1,2),F(0),F(1,2),F(0)); OM=(F(0),F(1,6),F(1,6),F(0))
def powr(x,n):
    r=ONE
    for _ in range(abs(n)): r=mul(r,x)
    return r if n>=0 else (r[0],r[1],-r[2],-r[3])
GENS=[tuple(int(12*c) for c in mul(powr(ZETA,k),powr(OM,j)))
      for k in range(6) for j in (-2,-1,0,1,2)]
def hnf(rows):
    rows=[list(r) for r in rows]; piv=0
    for c in range(4):
        r=next((i for i in range(piv,len(rows)) if rows[i][c]),None)
        if r is None: continue
        rows[piv],rows[r]=rows[r],rows[piv]
        for i in range(piv+1,len(rows)):
            while rows[i][c]:
                q=rows[piv][c]//rows[i][c]
                rows[piv]=[a-q*b for a,b in zip(rows[piv],rows[i])]
                rows[piv],rows[i]=rows[i],rows[piv]
        if rows[piv][c]<0: rows[piv]=[-a for a in rows[piv]]
        piv+=1
    B=rows[:piv]
    for i in range(piv-1,-1,-1):
        c=next(j for j in range(4) if B[i][j])
        for k in range(i):
            q=B[k][c]//B[i][c]
            B[k]=[a-q*b for a,b in zip(B[k],B[i])]
    return B
B=hnf(GENS)
def in_R(v):
    x=list(v)
    for row in B:
        c=next(j for j in range(4) if row[j])
        if x[c]%row[c]: return False
        q=x[c]//row[c]; x=[a-q*b for a,b in zip(x,row)]
    return all(a==0 for a in x)

print("\n1. R is not a ring, but 3R is")
def prod_over12(u, v, scale):
    w = mul(tuple(F(t) for t in u), tuple(F(t) for t in v))     # numerators over 144
    w = tuple(t / 12 * scale for t in w)
    return None if any(t.denominator != 1 for t in w) else tuple(int(t) for t in w)
def closed(scale):
    for u in B:
        for v in B:
            w = prod_over12(tuple(u), tuple(v), scale)
            if w is None or not in_R(w): return False
    return True
check("products of unit vectors that land back in R", 
      sum(1 for u in GENS for v in GENS if (lambda w: w is not None and in_R(w))(prod_over12(u,v,1))), 684)
check("R closed under multiplication", closed(1), False)
check("3R closed under multiplication", closed(3), True)
check("1/3 lies in R, so 1 lies in 3R", in_R((4,0,0,0)), True)

print("\n2. 3R is the MAXIMAL order: disc = disc(F)^2")
bas = [tuple(F(t,4) for t in row) for row in B]      # 3R's elements
trace = lambda x: 4*x[0]
G = [[trace(mul(bi,bj)) for bj in bas] for bi in bas]
def det4(M):
    from itertools import permutations
    s=F(0)
    for p in permutations(range(4)):
        q=list(p); sgn=1
        for i in range(4):
            for j in range(i+1,4):
                if q[i]>q[j]: sgn=-sgn
        t=F(1)
        for i in range(4): t*=M[i][p[i]]
        s+=sgn*t
    return s
check("disc of the trace form on 3R", det4(G), 1089)
check("and disc(Q(sqrt33))^2", 33*33, 1089)
# the basis and the matrix the paper prints, checked against what is derived here
check("the Z-basis Proposition 8 prints",
      [tuple(str(x) for x in b) for b in bas],
      [('1/4','1/4','1/4','-1/4'), ('0','1/2','0','-7/2'),
       ('0','0','1/2','1/2'),      ('0','0','0','1')])
check("the trace matrix Proposition 8 prints", [[int(x) for x in row] for row in G],
      [[5,-22,4,11], [-22,-506,77,154], [4,77,-14,-22], [11,154,-22,-44]])
def _coords(v):
    x = list(v); out = []
    for row in bas:
        j = next(k for k in range(4) if row[k])
        q = x[j] / row[j]; out.append(q); x = [p - q*t for p, t in zip(x, row)]
    assert all(t == 0 for t in x)
    return out
check("all 16 products b_i b_j are integral over that basis",
      [(i, j) for i in range(4) for j in range(4)
       if any(c.denominator != 1 for c in _coords(mul(bas[i], bas[j])))], [])

print("\n3. why exactly two colourings: R/2R = F_4 x F_4")
# classes of R/2R in the Hermite basis B, bit i = coefficient of b_{i+1}
def coords(v):
    x=list(v); c=[]
    for row in B:
        j=next(k for k in range(4) if row[k])
        q=x[j]//row[j]; c.append(q); x=[a-b*q for a,b in zip(x,row)]
    assert all(a==0 for a in x)
    return c
cls = lambda v: sum((c % 2) << i for i, c in enumerate(coords(v)))
P1, P2 = {0,5,9,12}, {0,3,4,7}
check("pi_1 R / 2R is a subgroup of order 4", 
      len(P1) == 4 and all((a^b) in P1 for a in P1 for b in P1), True)
check("pi_2 R / 2R likewise", 
      len(P2) == 4 and all((a^b) in P2 for a in P2 for b in P2), True)
check("they meet in 0 and span: CRT, R/2R = R/pi_1 x R/pi_2",
      P1 & P2 == {0} and len({a^b for a in P1 for b in P2}) == 16, True)

U = sorted({cls(g) for g in GENS})
check("the 30 unit vectors fall into 9 classes", len(U), 9)
check("and those 9 are exactly the classes off both coordinate lines",
      U, sorted(set(range(16)) - P1 - P2))
# The paper's letters: ZETA here is omega = e^{i pi/3}, OM is the half-angle phi.
# omega^3 = -1 = 1 and phi^-1 = phi^2 modulo 2R, so the 30 classes collapse to 3x3
def diff2R(u, v):
    d = tuple(a-b for a,b in zip(u,v))
    return all(c % 2 == 0 for c in d) and in_R(tuple(c//2 for c in d))
num = lambda x: tuple(int(12*c) for c in x)
check("omega^3 = 1 mod 2R", diff2R(num(powr(ZETA,3)), (12,0,0,0)), True)
check("phi^-1 = phi^2 mod 2R", diff2R(num(powr(OM,-1)), num(powr(OM,2))), True)
check("so the classes are the nine omega^k phi^j, k,j in {0,1,2}",
      sorted({cls(num(mul(powr(ZETA,k), powr(OM,j)))) for k in range(3) for j in range(3)}),
      U)

# the finish: a plane meeting no unit class lies in a coordinate line
import itertools
planes = {frozenset({0, a, b, a^b}) for a, b in itertools.combinations(range(1,16), 2)}
planes = {W for W in planes if len(W) == 4}
check("two-dimensional subspaces of F_2^4", len(planes), 35)
check("those avoiding all nine unit classes are exactly the two prime reductions",
      sorted(sorted(W) for W in planes if not (W & set(U))),
      [sorted(P2), sorted(P1)])
# and stability is the wrong invariant: eleven of the 35 survive it, not two
HALF = (F(1,2), F(1,2), F(0), F(0))                       # (1 + sqrt33)/2
img = [cls(num(mul(HALF, tuple(F(t,12) for t in r)))) for r in B]
def act(w):                                               # F_2-linear, by bits
    out = 0
    for i in range(4):
        if (w >> i) & 1: out ^= img[i]
    return out
check("sqrt33 acts as the identity on R/2R", 
      [cls(num(mul((F(0),F(1),F(0),F(0)), tuple(F(t,12) for t in r)))) for r in B],
      [cls(tuple(r)) for r in B])
check("subspaces stable under (1+sqrt33)/2: eleven, not two",
      sum(1 for W in planes if all(act(w) in W for w in W)), 11)

# Step 4 needs each phi_i's image to be the WHOLE Klein group, not a subgroup of
# order 2.  Two independent reasons, both finite:
_hyp = [{w for w in range(16) if bin(w & a).count("1") % 2 == 0} for a in range(1, 16)]
check("index-2 subgroups of R containing 2R (hyperplanes of F_2^4)", len(_hyp), 15)
check("  none of them avoids all nine unit classes",
      [i for i, H in enumerate(_hyp) if not (H & set(U))], [])
check("  a hyperplane holds 7 non-zero classes, and only 6 non-zero ones are free",
      (7, len((P1 | P2) - {0})), (7, 6))
check("and 1 + omega + omega^2 = 2 omega kills it again: 3x != 0 in an order-2 group",
      3 % 2, 1)

try:
    from cypari import pari
except ImportError:
    print("\n(cypari not installed: skipping the PARI half)")
    raise SystemExit(1 if FAIL else 0)

print("\n4. the arithmetic that turns the shell criterion into a theorem")
pol = 'x^4 - x^3 - 2*x^2 - 3*x + 9'
check("h(F) for F = Q(sqrt33)", int(pari('bnfinit(x^2-33,1).no')), 1)
# the paper proves h(F) = 1 by Minkowski rather than citing this; check the bound
# it uses, and that the only ideals below it are principal
check("Minkowski bound for F is below 3 (so only primes above 2 matter)",
      round(0.5 * 33 ** 0.5, 4), 2.8723)
check("  and the primes above 2 are principal: N((5+sqrt33)/2)", (25 - 33) // 4, -2)
check("eps = 23 - 4 sqrt33 is a unit of norm +1", 23*23 - 33*16, 1)
check("  and is totally positive", 23 - 4*33**0.5 > 0 and 23 + 4*33**0.5 > 0, True)
check("  and is fundamental (PARI agrees)",
      str(pari('bnfinit(x^2-33,1).fu[1]')), "Mod(-4*x + 23, x^2 - 33)")
check("disc(V)", int(pari(f'nfdisc({pol})')), 1089)
check("so V/F is unramified at every finite prime", int(pari(f'nfdisc({pol})')) == 33*33, True)
check("h(V)", int(pari(f'bnfinit({pol},1).no')), 1)
# the paper proves h(V) = 1 by Minkowski rather than citing PARI; check every
# ingredient of that argument
_mb = (4/math.pi)**2 * math.factorial(4)/4**4 * 1089**0.5
check("Minkowski bound for V is below 5.02", round(_mb, 4), 5.0154)
_norms = sorted(int(pari(f'{p}')**int(pari(f'idealprimedec(nfinit({pol}),{p})[{k}].f')))
                for p in (2, 3, 5)
                for k in range(1, int(pari(f'#idealprimedec(nfinit({pol}),{p})')) + 1))
check("norms of the primes above 2, 3 and 5", _norms, [3, 3, 4, 4, 25, 25])
check("  so the only ideals of norm <= 5 are 1 and those four",
      [n for n in _norms if n <= 5], [3, 3, 4, 4])
check("33 is a non-residue mod 5, so 5 is inert in F", 33 % 5 in (1, 4), False)
# w = (1 + i(2 sqrt3 + sqrt11))/2 generates a prime above 3
W = (6, 0, 12, 6)                                  # chart point, over 12
check("w = (1 + i(2sqrt3 + sqrt11))/2 lies in 3R = O_V",
      in_R(tuple(c // 3 for c in W)), True)
_S = W[0]**2 + 33*W[1]**2 + 3*W[2]**2 + 11*W[3]**2
_T = W[0]*W[1] + W[2]*W[3]
check("  |w|^2 rational part = 6", F(_S, 144), 6)
check("  and its sqrt33 part = 1", F(2*_T, 144), 1)
check("  so N_{V/Q}(w) = 36 - 33 = 3", 36 - 33, 3)
check("V is totally imaginary, signature (0,2)", str(pari(f'nfinit({pol}).sign')), "[0, 2]")
eta = pari(f'bnfinit({pol},1).fu[1]')
emb = pari(f'nfeltembed(nfinit({pol}), bnfinit({pol},1).fu[1])')
n1 = abs(complex(emb[0]))**2; n2 = abs(complex(emb[1]))**2
e1, e2 = 23 - 4*math.sqrt(33), 23 + 4*math.sqrt(33)
check("N_{V/F}(eta) = 23 - 4 sqrt33, F's fundamental unit",
      abs(n1 - e1) < 1e-9 and abs(n2 - e2) < 1e-9, True)
check("that unit is totally positive", e1 > 0 and e2 > 0, True)

# the same unit written down explicitly, so the proof needs no computer algebra:
# eta = i(2 sqrt3 - sqrt11), chart point (0,0,24,-12), purely imaginary
E = (0, 0, 24, -12)
S_e = E[0]**2 + 33*E[1]**2 + 3*E[2]**2 + 11*E[3]**2
T_e = E[0]*E[1] + E[2]*E[3]
check("explicit eta = i(2sqrt3 - sqrt11): |eta|^2 rational part", F(S_e, 144), 23)
check("  and its sqrt33 part", F(2*T_e, 144), -4)
check("  N_{V/Q}(eta) = 1, so eta is a unit", 23*23 - 16*33, 1)
check("  eta/3 lies in R, so eta lies in 3R = O_V",
      in_R(tuple(c // 3 for c in E)), True)

OBS = {2,8,17,29,32}
obstructed = lambda p: p not in (3,11) and (p == 2 or p % 33 in OBS)
bad = []
for p in range(2, 200):
    if any(p % d == 0 for d in range(2, int(p**.5)+1)): continue
    nF = int(pari(f'#idealprimedec(nfinit(x^2-33), {p})'))
    nV = int(pari(f'#idealprimedec(nfinit({pol}), {p})'))
    inert = (nV == nF)
    if inert != (obstructed(p) or p == 11): bad.append(p)
check("primes of F inert in V = the obstructed ones, plus 11", bad, [])
print("      (11 ramifies in F, so rational valuations there are even anyway)")

print()
if FAIL:
    print(f"{len(FAIL)} DISAGREEMENT(S):")
    for l,g,w in FAIL: print(f"   {l}: got {g}, expected {w}")
    raise SystemExit(1)
print("every ingredient of the proof checks")
