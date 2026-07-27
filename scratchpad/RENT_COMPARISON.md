# Rent comparison: the M12/Hadamard family vs the codes

> ## CORRECTION (2026-07-27, sibling commit `4aea70d`): finding 3 is WITHDRAWN — untested, not inverted
>
> Finding 3 read the sweep's automorphism counts as group orders. They were a bounded
> random search saturating at cap 60 — lower bounds, not orders. Exact orders by full
> backtracking: H11 has **7920** automorphisms (not 1), and is the MORE symmetric member
> of its k-matched pair (L11: 768); at k=8 the direction reverses (E8 21504 vs H8 48).
> The automorphism hypothesis is neither confirmed nor inverted by these data — it is
> not tested by them. Findings 1 and 2 (economies of scale; Hadamard cheaper per nat at
> matched k) do not depend on the counts and stand.
>
> The same exact computation delivered an unsought confirmation: the truncated
> Hadamard-12 automorphism orders at k = 11, 10, 9, 8 are 7920, 720, 144, 48 —
> |M11|, |M10|, |M9|, |M8|, the Mathieu stabilizer chain, one point stabilizer per
> deleted column. And it explains the rent-islands G7 lossy finding at the group level:
> by k=8 the surviving M8 has orbits 8+4 on the 12 rows, the decoder's cells go
> unequal, and full upkeep can no longer restore the maximum.


From `maintenance_sweep_results.json` (sweep completed 2026-07-26; prereg 5d597fe;
gates ALL PASS, 7/7). Currency: `cost_erase / share_held` = erased bits per step
per nat of whole-only share retained, at matched (noise ε, retention target).
Structures: linear codes L5,L7,E8,L11,L12,R12 (aut counts 16–60) vs the
Hadamard/M12-symmetry family H8–H11 (aut counts 10,5,2,1).

## The three findings

**1. ECONOMIES OF SCALE dominate everything: bigger habits are cheaper per nat.**
At every matched condition the rent/nat ranking is near-monotone in k:
ε=0.05, hold 10%: H11(k=11) 0.804 … L5(k=5) 1.399. ε=0.20: L12 1.84 … L5 4.44
(2.4×). The densest large structures always sit at the top of the table.

**2. At matched k, the exceptional (Hadamard) structures are CHEAPER than the
codes — modestly and consistently.** H11 beats L11 at all four conditions
(e.g. 0.1677 vs 0.1824; 0.8040 vs 0.9023); H8 beats E8 at all four
(up to 0.97 vs 1.27). Family means (k-confounded, stated as such) at every
condition: HADAMARD < CODE.

**3. The automorphism hypothesis INVERTS.** Predicted: more automorphisms →
more free moves → cheaper maintenance. Measured: H11 has ONE automorphism and
is the cheapest structure in the table; L5/L7/E8 have 60 and are the most
expensive. Even k-matched: H11(aut 1) < L11(aut 16); H8(aut 10) < E8(aut 60).
Automorphism-richness holds share exactly under DRIFT (the AUT arm: max
|Δshare| = 4.4e-16 — confirmed), but noisy rent is governed by PACKING
DENSITY (share per slot), not by symmetry. The M12 family wins through
density despite near-total rigidity.

## Caveats, stated before anyone quotes this
- ε=0.20 rows for targets 0.1 and 0.5 are identical — the controller lands on
  the same feasible operating point at high noise; the two targets are not
  independent measurements there.
- L5 at ε=0.01, target 1.0 reports held=False with q*=NaN while ε=0.05
  target 1.0 holds at q*=1: flagged as a probable controller/root-finding
  boundary artifact, not physics; do not build on the frac=1.0 rows.
- Family means confound k (the code family includes k=5,7). The k-matched
  pairs are the honest comparison; they agree in direction with the means.
- Rent/nat falls from k=5→12 but may be plateauing; no extrapolation beyond
  the measured range is licensed.
