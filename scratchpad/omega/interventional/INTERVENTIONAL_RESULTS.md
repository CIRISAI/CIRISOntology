# INTERVENTIONAL SIGNATURE — results

**Verdict: the signature separates all four planted cases. 15/18 frozen arms landed;
the three misses were in the COMPARISON apparatus, and all three were repaired by
`INTERVENTIONAL_AMENDMENT_1.md` (10/10, staked before it ran). Every arm testing the
signature itself landed on the first pass.**

Theory `INTERVENTIONAL_SIGNATURE.md`; stakes `INTERVENTIONAL_STAKES.md` (frozen before
`interventional.py` existed — mtimes 17:05 / 17:07 / 17:09); amendment
`INTERVENTIONAL_AMENDMENT_1.md` (frozen before `interventional_a1.py` existed). Raw:
`interventional_results.json`, `interventional_a1_results.json`, `.log` files beside them.

## 1. The planted nulls read EXACTLY zero — ten arms, 1501 lags each

Not "below a floor". Exactly `0.0` in IEEE double at every lag, `n_nonzero_lags = 0`:

| planted null | arms | reading |
|---|---|---|
| (a) one-way A→B, probe B read A | a3 | 0/1501 nonzero |
| (b) independent pair, both directions | b1 | 0/1501, 0/1501 |
| (c) common driver, both directions | c1 | 0/1501, 0/1501 |
| (c′) STRONG common driver (r = 1.000), both directions | e3 | 0/1501, 0/1501 |
| (f) B1 replica (shared clock), both directions | f2 | 0/1501, 0/1501 |
| (d) stochastic one-way, probe B read A | d2 | 0/1501 |
| sham probe `δ = id`, every case, every direction (16 arms) | K-I1 | all exactly 0.0 |

That is Theorem 3 measured: **a common driver contributes exactly nothing to the
probe-response in either direction**, at correlations up to `r = 1.000`, because the twin
run holds the driver fixed by construction.

## 2. The arrows were found, and every light-cone integer landed exactly

Staked as integers before the instrument existed, all hit with no free parameter:

| prediction | staked | measured |
|---|---|---|
| P1 — probe driver site 8 → driven sector | 8 | **8** |
| P2 — probe A site 8 → A itself | 0 | **0** |
| P3 — probe hidden driver C site 8 → A and B | 8, 8 | **8, 8** |
| e4 — site-wise driver C → A, B (interface probe) | 1, 1 | **1, 1** |
| g4 — interface probe (site 15) → B, stochastic | 1 | **1** |

Response magnitudes saturate the state space (`max_raw ≈ 0.95`, `max_view` 14–16 of 16
bits), so the coarse VIEW registers the intervention, not only the microstate (a4).

## 3. The crux: intervention separates what observation confounds

Case **(f), the B1 replica** — two autonomous rings, same law, no state coupling, sharing
one exogenous deterministic clock. This is COMPOSITION-2's B1 in miniature.

| | A ← B | B ← A |
|---|---|---|
| observational cross-defect (the s2 estimator) | **+0.07052** | **+0.05071** |
| its 99th-pct permutation floor | −0.00320 | −0.00319 |
| **observational verdict** | **COUPLED (false)** | **COUPLED (false)** |
| interventional probe-response, all 1501 lags | **exactly 0.0** | **exactly 0.0** |

Pearson `r = −0.985`. **The observational detector false-fires an order of magnitude above
its own floor on a pair with no causal arrow, in both directions, while the interventional
signature reads exact zero.** That is COMPOSITION-2's B1 miss reproduced in a system whose
truth is known by construction, and it is the demonstration the brick was for.

Case **(c′)**, the strong site-wise common driver, fires the observational detector too,
but **degenerately, and it is reported as such**: gains `−0.00014` / `−0.00015` against
floors `−0.00131` / `−0.00135`. Both gain and floor are negative — the pair synchronises to
`r = 1.000`, so B's context is redundant given A's, and the "firing" is only *less negative
than the permutation null*. This is not a technicality to be waved away: it is exactly the
shape of B1's first direction in COMPOSITION-2 (`−0.00018` vs floor `−0.00027`), while (f)
matches B1's second direction (`+0.00074` vs `+0.00031`) in kind and 90× in size. The two
synthetic cases between them reproduce both halves of the real miss.

Case **(b)**, genuinely independent rings with no shared clock: the observational detector
correctly read null (gains `−0.0031` / `−0.0030`, below floors). **The false fire needs a
common driver — it is not a generic property of the estimator**, which is the correct and
non-obvious control.

## 4. Stochastic: the pathwise/distributional split, with the trap caught

**(d)** stochastic one-way A→B, A-blind noise stream, coupled twins: pathwise arrow found
at the exact staked latency, reverse direction exactly zero at every lag.

**(d′)** the planted trap of theory §4.1 — no causal link at all, but B's noise slot is
selected by A's state (the kernel is A-independent, so the causal effect is *exactly* zero
by construction):

| arm | (d) true arrow | (d′) trap |
|---|---|---|
| pathwise coupled-twin response | fires, `max_raw = 0.949` | **fires, `max_raw = 0.957`** ← planted defect, observable |
| noise-selector differs between twins | — | 38% of steps |
| distributional arm, `p` (perm, N = 400+400) | **5.0e−5**, effect 9.0 sd | **0.073**, effect 0.13 sd |
| **two-arm rule (pathwise ∧ distributional)** | **COUPLED** ✓ | **NOT COUPLED** ✓ |

The pre-registered rule separates them. Note the honest reading of `p = 0.073`: it clears
the staked `> 0.05` but is not a comfortable null; the theorem says the effect is exactly
zero, so 0.13 sd is sampling fluctuation, and the number is quoted rather than described.

**The design law recovered from the d3 miss** (the frozen run read `p = 0.83` at lag 20 —
a saturated instrument, not a null result). With per-step noise `σ`, local Lyapunov
exponent `λ`, probe amplitude `A` and light-cone `ℓ`, the distributional arm has a
two-sided window and a fixed headroom:

> **`ℓ ≤ lag ≲ ℓ + ln(1/σ)/λ`,  headroom `= A·e^{−λℓ}/σ`.**

At `ℓ = 8`, `A = 0.4`, `σ = 1e−3`, `λ ≈ ln2` the headroom is ≈ 1.6 and no ensemble size
rescues it; at the interface (`ℓ = 1`) it is ≈ 200 and the arm reads 9.0 sd. **A probe far
from the interface is exponentially expensive in ensemble size.** This is a statement about
any chaotic substrate and it belongs in every engine and hardware design that follows.

## 5. The engine demonstration reading — `scratchpad/composition/s2/arm_K.csv`

**Labelled a DEMONSTRATION. It stakes nothing and passes nothing.** The series is a
whole-state divergence over one probed/unprobed twin pair, with no sector view and no
pre-probe window, so by construction it cannot carry a directional reading. What it can do
is exhibit the shape of a real interventional response and expose what is missing.

| quantity | value |
|---|---|
| frames | 23760 (240 → 23999), probe at frame 240 |
| `div_pos` at the probe frame — theory §4.3 demands **exactly 0** | **122.61** |
| `div_px` at the probe frame | 1.921e−3 |
| pedestal ÷ median of B4's window (frames 245–1199) | **0.738** |
| fraction of B4's window below 2× the pedestal | **0.765** |
| `K` reproduced exactly as `s2_analyze.py` computes it | **1.001241** (published: 1.0012 ✓) |
| `K` on the **pedestal-subtracted** series | **1.004740** |
| `K` on `div_px` | 0.999396 |
| growth over the full run, `div_pos` / `div_px` | 39.1× / 391.9× |
| early log-slope, pedestal-subtracted, first 600 frames | 0.00786 /frame (e-fold ≈ 127 frames ≈ 2.1 s) |

**Two readings, both plain.**

1. **The response is unmistakably real and unmistakably interventional**: a tiny probe throw
   moves the settled grains by nearly two orders of magnitude in momentum divergence over
   the run, on a substrate where every observational arm read floor or worse. B4 was the
   right kind of measurement.
2. **The instrument has an unadjudicated pedestal, and it was carrying most of B4's
   window.** The twins are identical until frame 240 and the divergence is summed over
   pre-existing nodes only, so theory says the probe-frame value must be exactly zero. It is
   122.61 — about 0.6 grain spacings per node — which is the signature of the probe changing
   the *code path*: `Session::throw` calls `certify_at`, which can re-certify and refine the
   mesh, and the compared node indices then no longer name the same grains.
   **74% of the median divergence in B4's window is that constant**, and 77% of the window's
   frames sit below twice it.

   **B4's verdict survives the diagnostic**: pedestal-subtracted `K = 1.00474`, still well
   inside the staked `≤ 1.05`. But the published `1.0012` understates the per-step excess by
   3.8× — the pedestal diluted it — so the number should be quoted with the correction, and
   `Aggregation`'s non-expansiveness is measured true with more margin consumed than the
   headline suggests. This is a diagnostic, not a kill: it says look, not conclude.

## 6. What a hardware or engine version would need

Eight requirements, each traceable to a theorem or a measured miss above:

1. **A pre-probe window, recorded.** On a deterministic engine the twin divergence before
   the probe must be bitwise exactly zero. `arm_K.csv` starts *at* the probe frame and
   therefore cannot see its own pedestal. (§4.3; §5 reading 2.)
2. **A sham arm run to completion** (`δ = id`), required to read exact zero. K-I1 caught
   nothing in the synthetic because the synthetic is clean; on an engine it is the arm that
   would have caught the pedestal.
3. **Identity-stable degrees of freedom.** The probe must not trigger re-certification,
   refinement, insertion, renumbering, spatial-hash reordering or parallel-reduction
   reordering. If it must, compare by persistent grain ID, never by array index.
4. **Sector views, not whole-state divergence.** The response has to be read in `v_B` for a
   direction to exist at all. `arm_K` sums over every base node and has no `A`/`B` split;
   the S2 `arms_NI.csv` file already carries a left/right split and could supply one.
5. **Both directions, equal probes.** Probe-left-read-right and probe-right-read-left with
   identical amplitude. One direction is an observation; two are a detector.
6. **Onset latency as the primary statistic.** Magnitude mixes coupling strength with
   Lyapunov amplification; latency is the causal light-cone and is amplification-free
   (§4.2). Report magnitude only normalised by the within-sector A→A response.
7. **If the substrate is stochastic**: an A-blind RNG (stream indexed by (time, sector,
   site) and consumed in that order — anything state-dependent manufactures theory §4.1's
   counterexample), the distributional arm read inside `[ℓ, ℓ + ln(1/σ)/λ]`, and the
   two-arm rule (claim coupling only when pathwise **and** distributional fire).
8. **Probe cost, if `g_c` is to be priced.** `Session::throw` re-baselines
   `opening_energy_j` and resets the dissipation ledger, so the probe's energetic cost is
   not currently readable from `arm_K`. A `g_c`-costed probe needs an injection channel that
   the ledger accounts for rather than zeroes.

## 7. Scope

Synthetic planted truth and one demonstration reading. No claim about nature, no promotion,
no Lean touched. What is established: **the splitting clause of Ω(c) has an operational form
that is exact on deterministic substrates, directional, immune to common drivers by
construction, and equal to the closure predicate the lake already machine-checked** — plus a
proof (Proposition 5) that its observational form was never identifiable from the data
COMPOSITION-2 gave it, and a measured pedestal in the one arm that passed.
