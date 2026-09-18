# Which pools 509 has already been proved minimum over

A proof here is identified by its **pool**, and every log prints it in its first
three lines.  Route 58 spent a morning re-proving two of the entries below because
nobody looked.  One grep avoids it:

```bash
grep -h "^pool [0-9]" results/*.log | sed 's/, [0-9]* edges.*//' | sort -u
```

## Both parts free, bound 508

| pool | how it was built | log |
|---|---|---|
| 556 | record + 47 candidates at degree >= 8, radius 2.53 | `proof_509_joint_both_parts_free.log` |
| 556 | the same, depth-complete | `proof_509_joint_depth_complete.log` |
| 585 | record + 76 candidates at degree >= 7, radius 2.53 | `proof_509_joint_degree7.log` |

`ball(W, 4, 2.53) u theta_4(ball)` is the ambient in each; the candidate set does
not change if that ball is built from a **finer lattice** of the tower
(`results/finer_lattice/README.md`), so these are the pools of that shape that
exist, not merely the ones tried.

**The next one out is 704** -- the same construction at degree >= 6, 195
candidates, 72% density.  Not proved, and running.  Since 585 is proved, any
answer in it must use one of the **119** candidates of degree exactly 6, which
`drive_down.py --proved-degree 7` puts on the master as a single clause.

## Other pools in results/

524, 538, 541, 547, 548, 553, 571, 573, 577, 583, 589, 594, 682 (single-side and
window searches), 1092, 1145, 1179, 1204 (unions of record graphs), 2365 (the
asymmetric pool).

## The density rule that decides which are worth attempting

Route 13: the answer must be roughly **90%** of the pool for the master to
converge.  509 of 556 is 92%, of 585 is 87% -- both proved.  509 of 704 is 72%,
which is below where any of these has converged before.
