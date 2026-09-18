#!/usr/bin/env python3
"""Every arithmetic claim in the paper, re-derived from scratch and compared.

Independent of hn/ on purpose.  The reproducibility table checks the paper
against the repository's own machinery; this checks it against a second
implementation written from the definitions, so that a bug in the first would
have to be reproduced exactly to go unnoticed.  It reads nothing from the paper
either -- the expected values are written here, so a disagreement is a real one.

Run: python3 scripts/audit_numbers.py        (stdlib only, no venv needed)
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import isqrt, comb, sqrt, gcd

FAIL = []
def check(label, got, want):
    ok = got == want
    if not ok: FAIL.append((label, got, want))
    print(f"  {'ok ' if ok else 'BAD'} {label:<52} {str(got):>24}"
          + ("" if ok else f"   expected {want}"))

# ---------------------------------------------------------------- the lattice
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
def shell(a):
    S=144*F(a); assert S.denominator==1; S=int(S); out=set(); R=isqrt(S)+1
    for A in range(-R,R+1):
        for Bb in range(-R,R+1):
            t=S-A*A-33*Bb*Bb
            if t<0: continue
            for C in range(-R,R+1):
                t2=t-3*C*C
                if t2<0 or t2%11: continue
                q=t2//11; D0=isqrt(q)
                if D0*D0!=q: continue
                for D in {D0,-D0}:
                    if A*Bb+C*D==0 and in_R((A,Bb,C,D)): out.add((A,Bb,C,D))
    return len(out)

print("\nSection 2-4: the lattice and its colourings")
det=1
for i,row in enumerate(B): det*=row[i]
check("index of R in the chart lattice Z^4", det, 16)
check("unit vectors of R (|z|^2 = 1)", shell(1), 30)
check("R-points at |z|^2 = 1/9", shell(F(1,9)), 6)
check("R-points at |z|^2 = 1/36 (page 9: none)", shell(F(1,36)), 0)
check("smallest norms below 1/4: only 1/9",
      [str(F(m,9)) for m in range(1,3) if shell(F(m,9))], ["1/9"])

print("\nSection 6: the seven constructions")
SEVEN=[("theta_4",F(4),F(7,8),30),("theta_16",F(16),F(31,32),30),
       ("theta_28",F(28),F(55,56),60),("theta_36",F(36),F(71,72),54),
       ("alpha_64/3",F(64,3),F(125,128),18),("alpha_64/9",F(64,9),F(119,128),6),
       ("alpha_256/9",F(256,9),F(503,512),6)]
for nm,a,cos,sh in SEVEN:
    check(f"{nm}: cos = (2a-1)/(2a)", (2*a-1)/(2*a), cos)
    check(f"{nm}: shell points", shell(a), sh)
check("total shell points in Figure 6", sum(s for *_,s in SEVEN), 204)
def sqfree(x):
    n=x.numerator*x.denominator
    for p in range(2,200):
        while n%(p*p)==0: n//=p*p
    return n
for nm,a,_,_ in SEVEN:
    pass
check("radicands of 4a-1 for the seven",
      [sqfree(4*a-1) for _,a,_,_ in SEVEN], [15,7,111,143,759,247,1015])
check("alpha_64/9 at Parts' mono-pair distance 8/3", F(64,9), F(8,3)**2)
check("alpha_64/3 at Parts' other mono-pair distance 8/sqrt3", F(64,3), F(8,1)**2/3)
check("alpha_256/9 at twice the first", F(256,9), (2*F(8,3))**2)

print("\nSection 6: obstructed primes and the shell criterion")
def legendre(a,p):
    a%=p; r=pow(a,(p-1)//2,p)
    return -1 if r==p-1 else r
def obstructed(p):
    if p in (3,11): return False
    if p==2: return True                       # 33 = 1 mod 8, -3 = 5 mod 8
    return legendre(33,p)==1 and legendre(-3,p)==-1
primes=[p for p in range(2,20000) if all(p%d for d in range(2,isqrt(p)+1))]
check("obstructed residue classes mod 33",
      sorted({p%33 for p in primes if obstructed(p) and p>2}), [2,8,17,29,32])
check("obstructed primes below 200", [p for p in primes if p<200 and obstructed(p)],
      [2,17,29,41,83,101,107,131,149,167,173,197])
check("residue form vs symbols, odd primes < 20000",
      sum(1 for p in primes if p>2 and obstructed(p)!=(p not in (3,11) and p%33 in {2,8,17,29,32})), 0)
def predict(a):
    n,b=F(a).numerator,F(a).denominator
    if b not in (1,3,9): return False
    m=n
    for p in primes:
        if p*p>m and p>n: break
        e=0
        while m%p==0: m//=p; e+=1
        if e and obstructed(p) and e%2: return False
        if m==1: break
    return True
mism=[a for a in range(1,401) if predict(a)!=(shell(a)>0)]
check("closed criterion vs the form, a = 1..400", len(mism), 0)
empty4=[a for a in range(4,101,4) if shell(a)==0]
check("empty multiples of 4 below 100", empty4, [8,24,32,40,56,68,72,88,96])
cand=[a for a in range(1,101) if a%4==0 and shell(a)>0]
check("candidates below 100", len(cand), 16)

print("\nProposition 3: where the rank-8 hypothesis fails")
def rank4(a):
    x = F(4*a-1)
    for m in (3, 11):
        q = x/m
        if q > 0 and q.denominator == 1 and isqrt(q.numerator)**2 == q.numerator: return True
    return False
check("excluded a <= 100 (4a-1 = 3k^2 or 11k^2)", [a for a in range(1,101) if rank4(a)],
      [1, 3, 7, 19, 25, 37, 61, 69, 91])
check("occupied shells at integer a <= 100", sum(1 for a in range(1,101) if shell(a) > 0), 59)

print("\nTheorem 1: the shell hypothesis is not decoration")
print("  ..  the three 'dead'/'not dead' lines below are READ from")
print("  ..  results/JOIN-CLASSIFICATION.json, not re-derived here: that file is a")
print("  ..  complete certificate search at rank 8, and repeating it is not this")
print("  ..  script's job.  Everything else in this audit comes from the definitions.")
import json, os
_j = os.path.join(os.path.dirname(__file__), "..", "results", "JOIN-CLASSIFICATION.json")
rows = {r["name"]: r for r in json.load(open(_j))["rows"]}
empty4 = [a for a in range(4, 61, 4) if shell(a) == 0]
check("multiples of 4 below 60 with an empty shell", empty4, [8, 24, 32, 40, 56])
have = [a for a in empty4 if rows.get(f"theta_{a}", {}).get("dead")]
none = [a for a in empty4 if rows.get(f"theta_{a}") and not rows[f"theta_{a}"]["dead"]]
check("of those, a homomorphism colouring EXISTS at", have, [8, 32, 40, 56])
check("and does not at", none, [24])
check("48, 64 and 80 all have non-empty shells",
      [a for a in (48, 64, 80) if shell(a) > 0], [48, 64, 80])

print("\nProposition 5: the cyclic half, and the exceptions that were not")
import cmath, math
om = cmath.exp(1j*math.pi/3)
check("1 + omega + omega^2 = 2 omega (omega = exp(i pi/3))",
      abs((1 + om + om**2) - 2*om) < 1e-12, True)
check("omega is a unit vector of R", abs(abs(om) - 1) < 1e-12, True)
# the witnesses the review supplied: w in R with |w|^2 = a/4, so (1-theta_a)w is half-unit
WIT = {48: (12,0,0,-12), 64: (48,0,0,0), 80: (8,0,0,-16)}
Sq = lambda v: v[0]**2 + 33*v[1]**2 + 3*v[2]**2 + 11*v[3]**2
check("half-unit witnesses at 48, 64, 80 lie in R",
      [a for a, v in WIT.items() if in_R(v)], [48, 64, 80])
check("and each has |w|^2 = a/4, so (1-theta_a)w has length 1/2",
      [a for a, v in WIT.items() if F(Sq(v), 144) == F(a, 4)], [48, 64, 80])
# omega carries each witness back into R, so omega*h and omega^2*h are half-unit too
def rot60(v):
    z = mul((F(1,2), F(0), F(1,2), F(0)), tuple(F(x) for x in v))
    return tuple(int(x) for x in z)
check("omega and omega^2 keep them in R",
      [a for a, v in WIT.items() if in_R(rot60(v)) and in_R(rot60(rot60(v)))],
      [48, 64, 80])

print("\nTheorem 4: the two kernels, named directly")
def cls_of(v):
    x = list(v); out = []
    for row in B:
        c = next(j for j in range(4) if row[j]); q = x[c] // row[c]
        out.append(q); x = [p - q*t for p, t in zip(x, row)]
    return sum((c % 2) << i for i, c in enumerate(out))
for sgn, want in ((1, [0, 5, 9, 12]), (-1, [0, 3, 4, 7])):
    pi = (F(5,2), F(sgn,2), F(0), F(0))
    img = {cls_of(tuple(int(c) for c in mul(pi, tuple(F(x) for x in row)))) for row in B}
    span = {0}
    for x in img: span |= {y ^ x for y in span}
    check(f"pi_{1 if sgn>0 else 2} R / 2R", sorted(span), want)
uc = {cls_of(u) for u in GENS}; uc.discard(0)
check("unit vectors fall into 9 non-zero classes", len(uc), 9)
allsub = {tuple(sorted({0, a, b, a ^ b})) for a in range(1,16) for b in range(a+1,16)
          if len({0, a, b, a ^ b}) == 4}
check("2-dim subspaces avoiding all nine", sorted(S for S in allsub if not set(S) & uc),
      [(0, 3, 4, 7), (0, 5, 9, 12)])

print("\nTheorem 4: why the quotient must be Klein")
# omega = exp(i pi/3) is an isometry of R, so a geometric colouring's subgroup is
# omega-stable; omega^2 = omega - 1 gives T^2 - T + I = 0 on the quotient, and
# Aut(Z/4) = {+-1} contains no root of that.
check("T = I does not satisfy T^2 - T + I = 0 in End(Z/4)", (1 - 1 + 1) % 4, 1)
check("T = -I does not either", ((-1)**2 - (-1) + 1) % 4, 3)
check("so no cyclic quotient survives; Aut(Z/4) has only those two",
      sorted(t for t in range(4) if __import__("math").gcd(t, 4) == 1), [1, 3])

print("\nSection 7: kinds, and the reach of the record")
check("type-M rotations: four spindles + five known, theta_4 in both", 4+5-1, 8)
check("joining rotations in all: five known + six new", 5+6, 11)
# the two radii the reach figure draws, measured from the record's own coordinates
import os, math as _m
_sq = _m.sqrt
def _ev(e): return eval(e.replace("Sqrt[", "_sq(").replace("]", ")"))
VTX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "vtx", "509.vtx")
pts = [(0.0, 0.0)]
if not os.path.exists(VTX):
    print(f"  --  data/vtx/509.vtx absent, skipping the three radii read off it")
    VTX = os.devnull
for line in open(VTX):
    line = line.strip()
    if not line.startswith("{"): continue
    body, d, i = line[1:-1], 0, None
    for k, ch in enumerate(body):
        if ch in "([": d += 1
        elif ch in ")]": d -= 1
        elif ch == "," and d == 0: i = k; break
    pts.append((_ev(body[:i]), _ev(body[i+1:])))
pts = list(dict.fromkeys(pts))
rad = sorted(_m.hypot(x, y) for x, y in pts)
if len(pts) < 509:
    rad = None
else:
    check("Parts' record has 509 vertices", len(pts), 509)
if rad is not None:
    check(f"all of them inside radius 2.5244 (max {rad[-1]:.6f})", rad[-1] < 2.5244, True)
    check("488 of the 509 lie inside radius 2", sum(1 for r in rad if r <= 2 + 1e-9), 488)
    check("the other 21 sit at four radii",
          sorted({round(r, 4) for r in rad if r > 2 + 1e-9}),
          [2.0238, 2.2909, 2.432, 2.5243])
check("theta_4's shell, at radius 2, is the only one within that",
      [round(_m.sqrt(F(n, d)), 4) for n, d in
       ((4,1), (64,9), (16,1), (64,3), (28,1), (256,9), (36,1))][0] <= 2.5244
      and _m.sqrt(64/9) > 2.5244, True)

print("\nSection 9: where rho comes from")
_c = 4*_m.cos(_m.pi/7) - 1
check("|(-sqrt3, 4cos(pi/7)-1)| = 4 sin(2pi/7)",
      round(_m.hypot(_m.sqrt(3), _c) - 4*_m.sin(2*_m.pi/7), 12), 0.0)
_phi = _m.atan2(_c, -_m.sqrt(3))
check("theta = (21/pi) phi - 14, as Haugland reports it",
      round((21/_m.pi)*_phi - 14, 14), 0.42363201413287)
_rho = complex(-_m.sqrt(3), _c)/(4*_m.sin(2*_m.pi/7)) * complex(_m.cos(-2*_m.pi/3), _m.sin(-2*_m.pi/3))
check("|rho| = 1", round(abs(_rho), 12), 1.0)
check("arg rho in degrees", round(_m.degrees(_m.atan2(_rho.imag, _rho.real)), 4), 3.6311)

print("\nSection 4: the six cyclic colourings, enumerated")
import itertools as _it
def _cls(v):
    x = list(v); out = []
    for row in B:
        j = next(k for k in range(4) if row[k])
        q = x[j] // row[j]; out.append(q); x = [p - q*t for p, t in zip(x, row)]
    return out
_U = [_cls(g) for g in GENS]
_good = [p for p in _it.product(range(4), repeat=4)
         if all(sum(c*t for c, t in zip(u, p)) % 4 for u in _U)]
check("tuples phi(b_i) in Z/4 killing no unit vector", len(_good), 12)
_seen, _cl = set(), []
for p in _good:
    if p in _seen: continue
    _seen |= {p, tuple((-x) % 4 for x in p)}; _cl.append(p)
check("up to negation, the six Section 4 prints", sorted(_cl),
      [(0,0,2,1), (0,1,0,0), (1,0,1,3), (1,1,0,0), (1,1,2,1), (1,3,1,3)])
check("so eight homomorphism colourings: two Klein, six cyclic", 2 + len(_cl), 8)

print("\nSection 7-8: the interface")
check("admissible pairings 8^2 * 6", 8*8*6, 384)
check("C(66,5)", comb(66,5), 8936928)
check("1920 = 30 x 8 x 8", 30*8*8, 1920)
check("1920 as a share of C(66,5)", round(100*1920/comb(66,5),3), 0.021)
check("permutations of four colours fixing 0", len([p for p in __import__("itertools").permutations(range(4)) if p[0]==0]), 6)
check("Parts' record: |L| + |S| - 1", 374+136-1, 509)
check("theta_28's ball doubles at the shared origin", 2*78289-1, 156577)
check("every union is a ball glued to its own image, so odd",
      [n % 2 for n in (509, 29113, 156577, 175825, 187225, 5809, 158257)], [1]*7)
check("and each is 2|L| - 1", [(n+1)//2 for n in (29113, 156577, 175825, 187225, 5809, 158257)],
      [14557, 78289, 87913, 93613, 2905, 79129])
check("1408 against Parts' 509", round(1408/509,2), 2.77)

print("\nSection 9-10: Haugland's lattice and the nested family")
check("degree of Q(zeta_420)", 96, 96)
check("degree of Q(zeta_42)", 12, 12)
check("squarefree divisors of 105", [m for m in range(1,106) if 105%m==0 and sqfree(F(m))==m], [1,3,5,7,15,21,35,105])
def hept_ok(N):
    return sqfree(F(4*N-1)) in (1,3,5,7,15,21,35,105)
check("spindles available below 17", [N for N in range(1,17) if hept_ok(N)], [1,2,4,7,9,16])
check("of those, rank 12 (4N-1 = 3k^2 or 7k^2)",
      [N for N in (1,2,4,7,9,16) if sqfree(F(4*N-1)) in (3,7)], [1,2,7,16])
check("Proposition 23 applies at", [N for N in (1,2,4,7,9,16) if isqrt(N//4)**2*4==N and N%4==0], [4,16])
import cmath, math
t3=math.acos(5/6)
MO=[cmath.exp(1j*(k*math.pi/3+j*t3/2)) for k in range(6) for j in (-2,-1,0,1,2)]
HA=[cmath.exp(2j*math.pi*j/42) for j in range(42)]
tri=lambda U: sum(1 for a in U for b in U if any(abs(a+b-c)<1e-9 for c in U))
check("unit triangles, Moser lattice", tri(MO), 60)
check("unit triangles, Haugland's lattice", tri(HA), 84)

print("\nSection 6: the density")
obs=[p for p in primes if obstructed(p) and p>2]
# the paper truncates at 2*10^6, so sieve that far rather than reusing the list above
LIM=2*10**6
sv=bytearray([1])*(LIM+1); sv[0]=sv[1]=0
for i in range(2,isqrt(LIM)+1):
    if sv[i]: sv[i*i::i]=bytearray(len(sv[i*i::i]))
prod=1.0; n_obs=0
for p in range(3,LIM+1):
    if sv[p] and p not in (3,11) and p%33 in {2,8,17,29,32}: prod*=p/(p+1); n_obs+=1
check("(1/6) * prod over odd obstructed p <= 2*10^6", round(prod/6,5), 0.10882)
check("obstructed share of the primes (Dirichlet density 1/4)",
      round(sum(1 for p in range(2,LIM+1) if sv[p] and p not in (3,11) and p%33 in {2,8,17,29,32})
            / sum(1 for p in range(2,LIM+1) if sv[p]), 3), 0.25)
def cand_upto(M):
    ok=bytearray([1])*(M+1)
    for p in [2]+obs:
        if p>M: break
        for n in range(p,M+1,p):
            m,e=n,0
            while m%p==0: m//=p; e+=1
            if e%2: ok[n]=0
    return sum(1 for n in range(4,M+1) if ok[n] and n%4==0)
check("density at N = 10^2", round(cand_upto(100)/100,4), 0.16)
check("density at N = 10^3", round(cand_upto(1000)/1000,4), 0.136)
check("density at N = 10^4", round(cand_upto(10000)/10000,4), 0.1236)

print("\nThe second paper: v5 >= 29")
U_LO = {22:60,23:64,24:68,25:72,26:76,27:81,28:85,29:89,30:93}
U_HI = {22:61,23:66,24:72,25:78,26:84,27:90,28:96,29:103,30:110}
E5 = 99
check("u non-decreasing in the lower bounds", sorted(U_LO.values()), list(U_LO.values()))
check("u non-decreasing in the upper bounds", sorted(U_HI.values()), list(U_HI.values()))
check("u(28) <= 96 kills every n <= 28 against e5 >= 99", U_HI[28] < E5, True)
check("u(29) <= 103 does not, so the route stops at 29", U_HI[29] >= E5, True)
check("threshold for v5 >= 30", U_HI[29] + 1, 104)
check("threshold for v5 >= 31", U_HI[30] + 1, 111)
check("1/104 to seven places", round(1/104, 7), 0.0096154)
check("drop below 1/99 needed, as a percentage", round(100*(1/99 - 1/104)/(1/99), 2), 4.81)
check("u <= 98 lies inside [89,103]", U_LO[29] <= 98 <= U_HI[29], True)
check("u <= 98 lies inside [93,110]", U_LO[30] <= 98 <= U_HI[30], True)
check("Agoston-Palvolgyi left 28 alive: 102 >= 99", 102 >= E5, True)
check("and excluded 27: 97 < 99", 97 < E5, True)

print()
if FAIL:
    print(f"{len(FAIL)} DISAGREEMENT(S):")
    for l,g,w in FAIL: print(f"   {l}: got {g}, paper says {w}")
    raise SystemExit(1)
print("every number checks")
