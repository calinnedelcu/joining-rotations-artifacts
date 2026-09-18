"""Filter 1: a 4-colouring of an entire infinite lattice, by arithmetic alone.

Ducz (arXiv 2606.12325, "A note on geometric colorings of the Moser lattice")
proves that the Moser lattice has a proper 4-colouring given by two linear
functionals mod 2:  with v = a + b w1 + c w3 + d w1 w3,

    l1 = a + b + d,   l2 = a + c + d   (mod 2),   colour = l1 + 2 l2,

and that it and one sibling are the only two.  Read structurally, that is a
group homomorphism

    phi : Lambda ---> G,   |G| = 4,   phi(u) != 0 for every unit vector u,

and the reason it colours properly is one line: if |p - q| = 1 then p - q is a
unit vector of Lambda, so phi(p) != phi(q).  Nothing about radius, depth, or
which ball was built enters anywhere.

WHAT THIS PROVES, AND WHAT IT DOES NOT.

  * phi found  ==>  the WHOLE infinite lattice is 4-colourable, so no subset of
    it is 5-chromatic, at any radius, at any depth, forever.  This is a proof,
    and the certificate is checkable by hand.
  * no phi     ==>  NOTHING.  The lattice may still be 4-colourable by a
    colouring that is not a group homomorphism.  A failure to find one is not
    evidence of 5-chromaticity.

So the filter is a one-sided KILL.  Used the other way round it would be
exactly the kind of test that has already cost this project three wrong
conclusions, so `certify` returns a verdict of "dead" or "unknown" and never
"alive".

Soundness rests entirely on `hn.lattice.Lattice.unit_vectors` being COMPLETE.
If one unit vector were missed, phi could kill it and the certificate would be
worthless.  That is why the enumeration is an exact ellipsoid over the trace
form rather than a search of a ball, and why `verify_on_ball` re-checks the
colouring against the repository's own exact edge finder.
"""
from __future__ import annotations
from .lattice import Lattice


# ---- F_2 linear algebra on bitmasks ---------------------------------------
def _parity(x):
    return bin(x).count("1") & 1


def _solve_affine(rows, rhs, r):
    """All s in F_2^r with <s, rows[i]> = rhs[i], as (particular, nullspace).

    Returns None if inconsistent.  Vectors are bitmasks over r coordinates.
    """
    piv, red = [], []                       # reduced equations
    for a, b in zip(rows, rhs):
        for (pa, pb, pc) in red:
            if a >> pc & 1:
                a ^= pa
                b ^= pb
        if a == 0:
            if b:
                return None
            continue
        c = (a & -a).bit_length() - 1       # lowest set bit as pivot
        red.append((a, b, c))
        piv.append(c)
    part = 0
    for (a, b, c) in reversed(red):
        # back-substitute: value of coordinate c
        v = b
        for k in range(r):
            if k != c and (a >> k & 1):
                v ^= part >> k & 1
        if v:
            part |= 1 << c
    # sanity: the particular solution must satisfy every original equation
    for a, b in zip(rows, rhs):
        assert _parity(part & a) == b, "affine solve is wrong"
    free = [k for k in range(r) if k not in piv]
    null = []
    for f in free:
        s = 1 << f
        for (a, b, c) in reversed(red):
            v = 0
            for k in range(r):
                if k != c and (a >> k & 1):
                    v ^= s >> k & 1
            if v:
                s |= 1 << c
        assert all(_parity(s & a) == 0 for a in rows), "nullspace vector is wrong"
        null.append(s)
    return part, null


def _span(null):
    out = [0]
    for v in null:
        out += [x ^ v for x in out]
    return out


# ---- the search ------------------------------------------------------------
def klein_colourings(units, r, limit=None):
    """Every homomorphism Lambda -> (Z/2)^2 killing no unit vector.

    Returned as canonical kernels: the 2-dimensional subspace <l1, l2> of the
    dual, keyed by its three nonzero functionals.  Two homomorphisms give the
    same colouring up to renaming colours exactly when they have the same
    kernel, so this is the count "up to colour permutation".
    """
    ub = sorted({sum((u[k] & 1) << k for k in range(r)) for u in units})
    if 0 in ub:                      # a unit vector inside 2*Lambda kills it
        return []
    seen = {}
    for l1 in range(1, 1 << r):
        A = [u for u in ub if not _parity(l1 & u)]
        sol = _solve_affine(A, [1] * len(A), r)
        if sol is None:
            continue
        part, null = sol
        for off in _span(null):
            l2 = part ^ off
            if l2 == 0 or l2 == l1:
                continue
            key = tuple(sorted((l1, l2, l1 ^ l2)))
            if key not in seen:
                seen[key] = ("klein", l1, l2)
                if limit and len(seen) >= limit:
                    return list(seen.values())
    return list(seen.values())


def z4_colourings(units, r, limit=None):
    """Every homomorphism Lambda -> Z/4 killing no unit vector.

    Writing m = l + 2s with l in {0,1}^r, phi(u) = <l,u> + 2<s,u> (mod 4).  If
    <l,u> is odd the value is odd and automatically nonzero; if it is even the
    condition becomes the F_2 equation <s, u> = 1 + <l,u>/2, so each l costs one
    affine solve rather than a sweep over 2^r choices of s.
    """
    seen = {}
    for l in range(1, 1 << r):
        rows, rhs = [], []
        for u in units:
            P = sum(u[k] for k in range(r) if l >> k & 1)
            if P % 2:
                continue
            rows.append(sum((u[k] & 1) << k for k in range(r)))
            rhs.append((1 + P // 2) & 1)
        sol = _solve_affine(rows, rhs, r)
        if sol is None:
            continue
        part, null = sol
        for off in _span(null):
            s = part ^ off
            m = tuple((l >> k & 1) + 2 * (s >> k & 1) for k in range(r))
            neg = tuple((-x) % 4 for x in m)
            key = min(m, neg)
            if key not in seen:
                seen[key] = ("z4", m)
                if limit and len(seen) >= limit:
                    return list(seen.values())
    return list(seen.values())


def apply_colouring(cert, coord):
    """The colour (0..3) a certificate gives to a lattice point's coordinates."""
    if cert[0] == "klein":
        _, l1, l2 = cert
        a = _parity(l1 & sum((c & 1) << k for k, c in enumerate(coord)))
        b = _parity(l2 & sum((c & 1) << k for k, c in enumerate(coord)))
        return a + 2 * b
    _, m = cert
    return sum(x * c for x, c in zip(m, coord)) % 4


# ---- the filter -------------------------------------------------------------
class Verdict:
    """The outcome of the filter on one candidate.

    `dead` means proved 4-colourable as an infinite lattice.  `unknown` means
    exactly that -- never "5-chromatic".
    """

    def __init__(self, lattice, units, certs, periodic=None):
        self.lattice = lattice
        self.units = units
        self.certs = certs
        self.periodic = periodic          # (table, m) from a Cayley colouring

    @property
    def dead(self):
        return bool(self.certs) or self.periodic is not None

    @property
    def verdict(self):
        return "DEAD (4-colourable)" if self.dead else "unknown"

    def __repr__(self):
        return (f"<Verdict {self.verdict} rank={self.lattice.rank} "
                f"units={len(self.units)} certs={len(self.certs)}>")


def certify(points, limit=None, groups=("klein", "z4"), moduli=()):
    """Run filter 1 on the additive group generated by `points`.

    `points` are the generators: for a join candidate, the lattice's unit
    vectors together with their images under the joining map.
    """
    L = Lattice(points)
    units = L.unit_vectors()
    coords = [c for c, _ in units]
    certs = []
    if "klein" in groups:
        certs += klein_colourings(coords, L.rank, limit)
    if "z4" in groups and not (limit and len(certs) >= limit):
        certs += z4_colourings(coords, L.rank, limit)
    per = None
    for m in moduli:                      # strictly stronger; only ever adds kills
        if certs:
            break
        per = periodic_certificate(L, coords, m)
        if per is not None:
            break
    # A modulus skipped for size, like every modulus that simply fails, leaves the
    # verdict at "unknown" -- which is not a claim about the lattice either way.
    v = Verdict(L, units, certs, per)
    for c in certs:                       # never hand back an unchecked claim
        assert all(apply_colouring(c, u) != 0 for u in coords), \
            "certificate kills a unit vector"
    if per is not None:
        table, m = per
        assert all(apply_periodic(table, m, L.rank, u)
                   != apply_periodic(table, m, L.rank, (0,) * L.rank)
                   for u in coords), "periodic certificate kills a unit vector"
    return v


def verify_on_ball(cert, lattice, points, edges):
    """Independent check: no edge of a real point set is monochromatic.

    The certificate is already proved correct against the unit-vector set; this
    re-derives the same conclusion through the repository's own exact edge
    finder, so a mistake in the lattice machinery cannot pass unnoticed.
    """
    colour = {}
    for i, p in enumerate(points):
        c = lattice.coords(p)
        assert c is not None, "point outside the lattice the certificate covers"
        colour[i] = apply_colouring(cert, c)
    bad = [(a, b) for a, b in edges if colour[a] == colour[b]]
    return bad, colour


def verify_verdict(v, points, edges):
    """`verify_on_ball` for whichever certificate a Verdict actually holds."""
    if v.certs:
        return verify_on_ball(v.certs[0], v.lattice, points, edges)
    assert v.periodic is not None, "verdict carries no certificate to check"
    table, m = v.periodic
    colour = {}
    for i, p in enumerate(points):
        c = v.lattice.coords(p)
        assert c is not None, "point outside the lattice the certificate covers"
        colour[i] = apply_periodic(table, m, v.lattice.rank, c)
    return [(a, b) for a, b in edges if colour[a] == colour[b]], colour


# ---- the same idea at larger index ----------------------------------------
def periodic_certificate(lattice, units, m, k=4, max_cosets=300000,
                         conf_budget=200000):
    """4-colour the finite Cayley graph on Lambda/m*Lambda; a proper one lifts.

    The index-4 homomorphisms above are the smallest case of a general fact: if
    H <= Lambda has finite index and the Cayley graph of Lambda/H with
    connection set U mod H is k-colourable, then pulling the colouring back
    along p -> p mod H properly k-colours ALL of Lambda, because p - q = u in U
    moves p mod H to an adjacent vertex.  Taking H = m*Lambda makes the quotient
    (Z/m)^rank, so the whole test is one SAT call on m^rank vertices.

    This strictly extends the homomorphism search: a homomorphism onto a group
    of order 4 is exactly a colouring of Lambda/H that is linear, and most
    colourings are not.  It is what kills theta_12 over Q(sqrt3,sqrt11,sqrt47),
    which has no order-4 homomorphism but is 4-colourable at m = 4.

    Only a SAT answer is ever acted on, so the solver runs under a CONFLICT
    BUDGET: a refutation and a timeout are both reported as "no certificate",
    which is the same non-claim.  Without the budget a candidate that really is
    5-chromatic makes the m = 4 call refute a 65536-vertex graph, and the filter
    stops being cheap exactly on the candidates worth keeping.

    Returns (colour_table, m) on success, or None.  Success is a PROOF; failure
    says nothing, about that m or about anything else.
    """
    from pysat.solvers import Solver
    r = lattice.rank
    n = m ** r
    if n > max_cosets:                       # quotient bigger than the budget
        return None
    S = set()
    for u in units:
        idx = 0
        for j in range(r - 1, -1, -1):
            idx = idx * m + u[j] % m
        if idx == 0:
            return None                      # a unit vector inside m*Lambda
        S.add(idx)
    if not S:
        return None

    def add(a, b):
        out, x, y = 0, a, b
        da, db = [], []
        for _ in range(r):
            da.append(x % m); x //= m
            db.append(y % m); y //= m
        for j in range(r - 1, -1, -1):
            out = out * m + (da[j] + db[j]) % m
        return out

    adj = [[] for _ in range(n)]
    edges = set()
    for v in range(n):
        for s in S:
            w = add(v, s)
            if w != v:
                e = (v, w) if v < w else (w, v)
                if e not in edges:
                    edges.add(e)
                    adj[v].append(w)
                    adj[w].append(v)

    def var(v, c):
        return k * v + c + 1

    cls = [[var(v, c) for c in range(k)] for v in range(n)]
    for u, v in edges:
        for c in range(k):
            cls.append([-var(u, c), -var(v, c)])
    # break the colour symmetry on a triangle: worth a factor of about 30 here
    # for the same reason it is in hn/sat.py
    nb0 = set(adj[0])
    tri = next(((0, x, y) for x in adj[0] for y in adj[x] if y in nb0), None)
    if tri:
        for c, v in enumerate(tri[:k]):
            cls.append([var(v, c)])
    else:
        cls.append([var(0, 0)])

    solver = Solver(name="cadical153", bootstrap_with=cls)
    if conf_budget:
        solver.conf_budget(conf_budget)
        ok = solver.solve_limited(expect_interrupt=False)
    else:
        ok = solver.solve()
    table = None
    if ok:
        mset = set(l for l in solver.get_model() if l > 0)
        table = [next(c for c in range(k) if var(v, c) in mset) for v in range(n)]
    solver.delete()
    return (table, m) if ok else None


def apply_periodic(table, m, rank, coord):
    idx = 0
    for j in range(rank - 1, -1, -1):
        idx = idx * m + coord[j] % m
    return table[idx]
