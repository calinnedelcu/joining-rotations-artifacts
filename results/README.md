# Machine proofs produced here

`AUDIT.txt` is the output of `scripts/audit.py`, which re-reads every log here,
reports the bound each one claims, and re-verifies every graph the repository
ships straight from its coordinates: the unit-distance edges are recomputed
exactly in the field and compared against the stored edge list, the graph is
re-checked for non-4-colourability in a fresh solver with no assumptions, and its
minimum degree is reported, since a vertex-critical 5-chromatic graph must have
minimum degree at least 4. All ten graphs pass and all seventeen bounds are
consistent.

What the audit cannot do is re-check an UNSAT answer from the master without
redoing the search. Emitting an LRAT certificate from the final master call, so
that a reader can check it with cake_lpr rather than trusting this code, is the
piece still missing and is the first thing a referee would ask for.

Each log is the complete output of `scripts/parts_side.py`: the pool, the
bootstraps (vertex-critical colourings, essential vertices, size-2 correction
sets), every master proposal with the cut learned from it, and the final
`master UNSAT at bound B` line, which means: no choice of at most B free
vertices from the pool, together with the fixed part, induces a graph that is
not 4-colourable.

| log | fixed part | pool | statement |
|---|---|---|---|
| `proof_S136_minimum_for_L374_over_parts_region.log` | L_374 (`data/parts/v374e1860.vtx`) | the 182 small-part candidates in the union of Parts' S files | no 5-chromatic choice with <= 134 free vertices: S_136 (135 free + origin) is minimum |
| `proof_S136_minimum_for_L374_over_parts_region_via_patterns.log` | the 28 colour patterns of L_374 (`scripts/pattern_hitting.py`) | same 182 candidates | the same statement, proven independently with per-pattern oracles (69 master calls, 77 min) |
| `proof_S_at_least_131_for_L374_over_parts_region.log` | L_374 | same | the weaker bound 130, proven first |
| `proof_509_joint_both_parts_free.log` | **nothing fixed** | the 509 graph plus every lattice point with at least 8 neighbours in it, 556 points of which 12 appear in no file Parts published | no 5-chromatic subgraph with <= 508 vertices, with **both parts free to change at once**: the joint statement the one-sided proofs cannot make |
| `proof_509_union_510_517.log`, `proof_509_union_517_529.log` | nothing fixed | the UNION of two different published record graphs, 548 and 547 points | no 5-chromatic subgraph with <= 508 vertices, so combining two records' structures does not beat either |
| `proof_L374_minimum_for_S136_over_A412.log` | S_136 (`data/parts/v136e564.vtx`) | Parts' accumulative large graph A_412, which is the union of all 1092 of his minimal 374-vertex large parts | no 5-chromatic choice with <= 372 free vertices: **509 is the minimum over this pool**, both sides together |
| `proof_no_510_beater_over_A403.log` | S_136 | Parts' other accumulative graph A_403, the union of his 375-vertex large parts | no choice with <= 373 free vertices, so that family stops at 510 |
| `proof_L374_minimum_outside_parts_region.log` | S_136 | L_374 plus every lattice point with at least 7 neighbours in the graph, 438 points of which **22 appear in no file Parts published** | no choice with <= 372 free vertices, so the result survives leaving his region |
| `scan_forced_relations_10369.log` | — | a 10369-point lattice ball | the complete list of colour relations the lattice forces on the origin: 378 virtual edges, and mono-pairs at exactly one distance, 8/3 |
| `scan_all_joining_rotations_83_fields.log` | — | the Moser-spindle lattice, joined to a rotated copy of itself | across all 83 multiquadratic fields Q(sqrt3,sqrt11,sqrt m) with m <= 200, and about 2700 rotations, **exactly one** join gives a 5-chromatic graph: arccos(7/8) |
| `scan_eight_other_fields.log` | — | eight other fields with their own generators | 218 (field, lattice) pairs, no 5-chromatic union |
| `scan_all_73_rotations.log` | — | every unit direction of the field with denominator at most 32, as a joining rotation | exactly ONE of the 73 gives a 5-chromatic union, and it is theta_4 |
| `proof_two_wings_are_worse.log` | two mirror wings theta_4(S_136) and theta_4^{-1}(S_136) | A_412 | the large part still needs 374, so a second wing costs 135 vertices and saves none: total 645 |
| `proof_L374_minimum_even_with_S166.log`, `..._S172.log` | S_166 and S_172, stronger small parts | A_412 | the large part still needs 374, so the minimum is flat in the strength of the small part |

The two sides together now say that 509 is a genuine local optimum, not a
heuristic stopping point: the small part cannot shrink for Parts' large part,
and the large part cannot shrink for his small part, both proven exactly over
the regions he searched.

The searches converge only when the answer is DENSE in the pool. Choosing 135
of 182 or 373 of 412 works and takes minutes. The same code on the 811-point
union of every large-part file, where 373 must be chosen from 810, ran four
hours without the master ever becoming constrained. Pool density, not pool
size, is what decides.

`scan_forced_relations_10369.log` is a scan, not a proof of optimality, and
it closes the cheapest conceivable route to a record. A graph forcing two
points at distance sqrt(i) to share a colour would give a 5-chromatic graph of
2|G|-1 vertices when glued to its own theta_i-rotated copy, so |G| <= 254
would beat 509 outright. Over a 10369-point ball the lattice forces agreement
at exactly one distance, 8/3, which reproduces Parts' own mono-pair
independently -- and 8/3 cannot be spindled here, because its rotation needs
sqrt247. No sqrt(i) distance forces agreement at all.

Soundness rests on: cuts derived only from explicit 4-colourings of the pool
(edge cuts) or from explicitly 4-colourable sets (vertex cuts, essential
vertices), the degree >= 4 constraint (valid for any minimum solution, which
is vertex-critical), the 4-core pruning, and CaDiCaL's UNSAT answer on the
master. The candidate 5-chromatic graphs along the way were all re-verified
in a fresh solver. Not yet done: logging a DRAT proof of the final master
call, which is what a referee would want.
