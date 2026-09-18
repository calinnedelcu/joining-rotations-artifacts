#!/usr/bin/env python3
"""Step 5(a) of the divisibility law, on both signs of lambda.

Step 5(a) wrote every rational lambda as -p/q and then used pq >= 1, which is
the assumption lambda < 0.  Positive lambda occurs.  This checks, exactly:

  1. the chart congruences cut out exactly R (index 16 in Z^4), so a chart
     point with the congruences really is a lattice point;
  2. a = 7/19 is odd and of rank 8, and v = 5/6 + i sqrt3/6 lies in R with
     |v|^2 = 7/9, so that u = v + theta_a(v) is a cross unit vector with
     lambda = +1 -- the case the old text did not reach;
  3. that vector is harmless: neither prime divides v, so its diagonal colour
     is non-zero;
  4. the two finite checks that prove v_pi(|v|^2) = 2 v_pi(v): 16 divides
     144|.|^2 in O on the 30 unit vectors and their 435 polarisations, and the
     three non-zero classes of R/piR all sit at norm 1/9;
  5. that identity itself, sampled over the lattice.

No field module: everything is integer arithmetic in the chart
z = (A + B sqrt33)/12 + i(C sqrt3 + D sqrt11)/12.
"""
from fractions import Fraction as F
from itertools import product

# ---- the lattice, from its 30 unit vectors, in chart coordinates -----------
def mul(x, y):                      # basis 1, sqrt33, i sqrt3, i sqrt11
    a1,a2,a3,a4 = x; b1,b2,b3,b4 = y
    return (a1*b1 + 33*a2*b2 - 3*a3*b3 - 11*a4*b4,
            a1*b2 + a2*b1 - (a3*b4 + a4*b3),
            a1*b3 + a3*b1 + 11*(a2*b4 + a4*b2),
            a1*b4 + a4*b1 + 3*(a2*b3 + a3*b2))
one  = (F(1),F(0),F(0),F(0))
zeta = (F(1,2),F(0),F(1,2),F(0))                  # exp(i 60 deg)
om   = (F(0),F(1,6),F(1,6),F(0))                  # exp(i theta_3 / 2)
def powr(x, n):
    r = one
    for _ in range(abs(n)): r = mul(r, x)
    return r if n >= 0 else (r[0], r[1], -r[2], -r[3])
GENS = [tuple(int(12*c) for c in mul(powr(zeta,k), powr(om,j)))
        for k in range(6) for j in (-2,-1,0,1,2)]

def hnf(rows):
    rows = [list(r) for r in rows]; piv = 0
    for c in range(4):
        r = next((i for i in range(piv, len(rows)) if rows[i][c]), None)
        if r is None: continue
        rows[piv], rows[r] = rows[r], rows[piv]
        for i in range(piv+1, len(rows)):
            while rows[i][c]:
                q = rows[piv][c] // rows[i][c]
                rows[piv] = [a-q*b for a,b in zip(rows[piv], rows[i])]
                rows[piv], rows[i] = rows[i], rows[piv]
        if rows[piv][c] < 0: rows[piv] = [-a for a in rows[piv]]
        piv += 1
    B = rows[:piv]
    for i in range(piv-1, -1, -1):
        c = next(j for j in range(4) if B[i][j])
        for k in range(i):
            q = B[k][c] // B[i][c]
            B[k] = [a-q*b for a,b in zip(B[k], B[i])]
    return B

B = hnf(GENS)
def member(lat, v):
    x = list(v)
    for row in lat:
        c = next(j for j in range(4) if row[j])
        if x[c] % row[c]: return False
        q = x[c] // row[c]; x = [a-q*b for a,b in zip(x, row)]
    return all(a == 0 for a in x)
in_R = lambda v: member(B, v)

def cong(v):
    A,Bb,C,D = v
    return (A%2==Bb%2==C%2==D%2) and ((Bb+C+D-A) % 4 == 0)

det = 1
for i,row in enumerate(B): det *= row[i]
mism = [v for v in product(range(-4,5), repeat=4) if in_R(v) != cong(v)]
print(f"1. R has index {det} in the chart lattice; congruences vs membership over")
print(f"   [-4,4]^4: {6561 - len(mism)} of 6561 agree, {len(mism)} mismatches")
assert det == 16 and not mism

# ---- the lambda = +1 witness ----------------------------------------------
def sqfree(x):
    n = x.numerator * x.denominator
    for p in range(2, 200):
        while n % (p*p) == 0: n //= p*p
    return n
v = (10, 0, 2, 0)                                   # 5/6 + i sqrt3 / 6
S = v[0]**2 + 33*v[1]**2 + 3*v[2]**2 + 11*v[3]**2
m = F(S, 144)
a = F(7, 19)
print(f"\n2. v = {v} in R: {in_R(v)};  |v|^2 = {m}")
print(f"   a = {a}: v_2(a) = 0 (odd), 4a-1 = {4*a-1}, squarefree part {sqfree(4*a-1)}"
      f" not in (1,3,11,33), so rank 8")
u2 = m * (4*a - 1) / a                              # |(1 + theta_a) v|^2
print(f"   lambda = +1, u = v + theta_a(v):  |u|^2 = {u2}")
assert in_R(v) and m == F(7,9) and u2 == 1 and sqfree(4*a-1) == 19

# ---- both primes, and the valuation identity ------------------------------
def mpi(w, s):                                      # multiply by (5 + s sqrt33)/2
    A,Bb,C,D = w
    n = (5*A + s*33*Bb, s*A + 5*Bb, 5*C + s*11*D, s*3*C + 5*D)
    return None if any(x % 2 for x in n) else tuple(x//2 for x in n)
PI = {}
for s in (1,-1):
    rows = []
    for b in B:
        w = mpi(tuple(b), s) or tuple(2*x for x in mpi(tuple(2*c for c in b), s))
        rows.append(w)
    PI[s] = hnf(rows)
print(f"\n3. pi_1 | v: {member(PI[1], v)},  pi_2 | v: {member(PI[-1], v)}"
      f"  -> the diagonal colour is non-zero, so the vector kills nothing")
assert not member(PI[1], v) and not member(PI[-1], v)

def div1(g,h): return (-(3*g-8*h)//2, -(2*h-g)//2)  # O = Z[w], w=(1+sqrt33)/2
def div2(g,h): return (-(2*g+8*h)//2, -(g+3*h)//2)  # pi_1 = w+2, pi_2 = 3-w
def val(g, h, which):
    k = 0
    while True:
        if not ((g % 2 == 0) if which == 1 else ((g+h) % 2 == 0)): return k
        g, h = (div1 if which == 1 else div2)(g, h); k += 1
def vlat(w, which):
    # largest k with w in pi^k R -- membership in R, not mere chart-integrality
    k = 0; s = 1 if which == 1 else -1
    while k < 12:
        if not member(PI[s], w): return k
        A,Bb,C,D = w
        n = (5*A - s*33*Bb, -s*A + 5*Bb, 5*C - s*11*D, -s*3*C + 5*D)
        w = tuple(-x//4 for x in n); k += 1
    return k

# ---- the two finite checks behind v_pi(|v|^2) = 2 v_pi(v) ------------------
from itertools import combinations
QT = lambda v: (v[0]**2 + 33*v[1]**2 + 3*v[2]**2 + 11*v[3]**2, v[0]*v[1] + v[2]*v[3])
BL = lambda x,y: (2*(x[0]*y[0] + 33*x[1]*y[1] + 3*x[2]*y[2] + 11*x[3]*y[3]),
                  x[0]*y[1] + x[1]*y[0] + x[2]*y[3] + x[3]*y[2])
# 16 | S + 2T sqrt33 in O = Z[w], w = (1+sqrt33)/2:  S + 2T sqrt33 = (S-2T) + 4T w
ok16 = lambda ST: (ST[0] - 2*ST[1]) % 16 == 0 and ST[1] % 4 == 0
ng = sum(1 for w in GENS if not ok16(QT(w)))
np_ = sum(1 for i,j in combinations(range(30),2) if not ok16(BL(GENS[i], GENS[j])))
print(f"\n4. 144|.|^2 divisible by 16 in O: {30-ng}/30 unit vectors,"
      f" {435-np_}/435 polarisations -> 9|x|^2 in O throughout R")
assert ng == 0 and np_ == 0
reps = []
for w in sorted((v for v in product(range(-4,5), repeat=4) if in_R(v) and any(v)),
                key=lambda v: QT(v)[0]):
    if member(PI[1], w) or member(PI[-1], w): continue
    if all(not (member(PI[1], tuple(a-b for a,b in zip(w,x))) or
                member(PI[-1], tuple(a-b for a,b in zip(w,x)))) for x in reps):
        reps.append(w)
    if len(reps) == 3: break
print(f"   three non-zero classes of R/pi R: {reps}, all of norm 16/144 = 1/9,"
      f" where 144|v|^2 = 16 = (pi_1 pi_2)^4 has valuation exactly 4")
assert len(reps) == 3 and all(QT(w)[0] == 16 for w in reps)

bad = 0; tested = 0
for A in range(-14, 15):
  for Bb in range(-4, 5):
    for C in range(-14, 15):
      for D in range(-8, 9):
        w = (A,Bb,C,D)
        if w == (0,0,0,0) or not in_R(w): continue
        Sw = A*A + 33*Bb*Bb + 3*C*C + 11*D*D; T = A*Bb + C*D
        for which in (1,2):
            tested += 1
            if val(Sw - 2*T, 4*T, which) - 4 != 2*vlat(w, which): bad += 1
print(f"\n5. v_pi(|v|^2) = 2 v_pi(v): {tested//2} lattice points, both primes,"
      f" {bad} mismatches")
assert bad == 0
print("\nall five checks pass")
