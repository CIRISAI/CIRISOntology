# AMENDMENT 1 — three arms missed, and they missed for reasons in the CONFIGURATION, not the signature

*2026-08-26, written after `interventional.py`'s frozen run and before
`interventional_a1.py` exists. The frozen verdict stands as recorded: 15 of 18 arms
landed, `c3`, `d3`, `dp3` missed. This file diagnoses each miss, states what a repaired
configuration must do, and stakes it before running. Everything here is POST-HOC in
origin and PRE-REGISTERED in execution, and it is labelled that way wherever it is read.*

## The frozen run's standing (unchanged by anything below)

| arm | result |
|---|---|
| K-I1 sham floor (all 11 arms, δ = id) | **PASS** — exact 0.0 |
| P1 / P2 / P3 light-cone integers (8 / 0 / 8) | **PASS**, all three exact |
| a1 arrow found, a2 latency 8, a3 reverse exact zero, a4 view registers | **PASS ×4** |
| b1 independent pair exact zero both ways | **PASS** |
| c1 common driver exact zero both ways, c2 driver positive control | **PASS ×2** |
| d1 stochastic arrow + latency, d2 reverse exact zero | **PASS ×2** |
| dp1 planted trap fires pathwise, dp2 trap's causal effect null | **PASS ×2** |
| **c3** observational detector fires on the common-driver pair | **MISS** |
| **d3** distributional arm fires on the true stochastic arrow | **MISS** |
| **dp3** the two-arm rule separates (d) from (d′) | **MISS, inherited from d3** |

**Every arm that tests the interventional signature itself landed.** The three misses are
all in the *comparison* apparatus — the observational rival and the distributional
adjudicator. That is the honest shape of the result and it is not being smoothed.

## Diagnosis 1 — c3: the planted common driver was too weak to confound anything

Measured: Pearson `r = +0.031` between the A and B scalar summaries, and the
observational cross-defect read **below** its permutation floor in both directions
(`−0.00096` vs `−0.00040`; `−0.00193` vs `−0.00149`). The rival detector did not
false-fire because there was nothing to false-fire on: driving one site of a 16-site
chaotic ring injects a shared component that the ring destroys within a few steps.

The stake was written without first measuring the correlation the configuration would
produce — the repo's own recurring defect (*measure the boundary spread first*). The claim
"intervention separates what observation confounds" needs a configuration where
observation is actually confounded.

Case (b) tells the same story from the other side: on genuinely independent rings the
observational detector correctly read null. **So the frozen run demonstrated no
observational false fire at all**, and the crux comparison is currently unmade.

## Diagnosis 2 — d3: the distributional arm was read outside its window

Measured: `p = 0.83`, effect `0.0` pooled sd. Not a null result about causation — a
saturated instrument. With per-step noise `σ` and local Lyapunov exponent `λ`, the
ensemble spread at lag `t` after the probe grows like `σ e^{λt}` and saturates at the
attractor scale after `≈ ln(1/σ)/λ` steps; the probe's own effect, injected at the read
sector after the light-cone `ℓ`, grows like `A·e^{λ(t−ℓ)}`. Their ratio is
**`A · e^{−λℓ} / σ`, constant in `t` and set entirely by the light-cone the probe has to
cross**. With `A = 0.4`, `σ = 1e−3`, `λ ≈ ln 2` and `ℓ = 8` that ratio is `≈ 1.6` — the
signal never separates from the spread, and by `t = 20` both have saturated onto the same
invariant measure, so the two ensemble means coincide.

**The general design law, which is the actual finding here:** the distributional arm has a
two-sided window,

> `ℓ ≤ lag ≲ ℓ + ln(1/σ)/λ`,  with headroom `A·e^{−λℓ}/σ`.

A probe far from the interface is exponentially expensive in ensemble size. The remedy is
not more samples; it is to **probe at the interface** (make `ℓ` small) and read inside the
window. Nothing about this is special to the synthetic — it is a statement about any
chaotic substrate, and it belongs in the engine/hardware requirements.

## Diagnosis 3 — dp3 is entirely inherited

`dp3` is the conjunction "the two-arm rule accepts (d) and rejects (d′)". Its rejection
half **passed**: the trap fired pathwise (`max_raw = 0.957`, selector differed on 38% of
steps) and read null distributionally (`p = 0.677`, effect `0.03` sd). Only the acceptance
half failed, and only because `d3` did. `dp3` lands iff `d3` lands.

## The amendment, staked before `interventional_a1.py` is written

Three new arms. Frozen parameters as in `INTERVENTIONAL_STAKES.md` except where named.

### (c′) STRONG common driver — site-wise drive

Topology: hidden ring `C` autonomous; `A` and `B` each driven **site-wise** by `C`,
`a_i ← (1−XC)·ring(A)_i + XC·f(C_i)`, same for `B`, `XC = 0.4`. `A` and `B` never read each
other. Light-cone from `C` into `A` or `B` is now **1**, not 8.

* **e1** `|Pearson r(A,B)| ≥ 0.5` — the configuration is actually confounded. **PASS/MISS**
* **e2** the observational cross-defect **fires** (exceeds its 99th-pct permutation floor)
  in at least one direction. **PASS/MISS**
* **e3** interventional: probe A read B, and probe B read A, `R_raw == 0.0` at **every**
  lag, both directions. **PASS/MISS**
* **e4** positive control: probe C, read A and B — onset latency `== 1` exactly, both.
  **PASS/MISS**

**e2 ∧ e3 is the crux of this brick.** If e2 misses again the comparison is not made on a
common-driver substrate and I record that a second time rather than tuning a third.

### (f) THE B1 REPLICA — shared deterministic clock, no state coupling

Topology: two autonomous rings `A`, `B`, plus an **exogenous deterministic schedule**
`m(t) = 0.5 + 0.4·cos(2πt/400)` entering every site of both:
`u_i ← (1−0.3)·ring(u)_i + 0.3·m(t)`. This is COMPOSITION-2's B1 in miniature — two
causally disconnected systems running the same law under the same clock. There is no
`A→B` or `B→A` arrow, and the clock is not part of the state, so no probe can move it.

* **f1** the observational cross-defect **fires** in at least one direction — the B1 false
  fire, reproduced. **PASS/MISS**
* **f2** interventional: `R_raw == 0.0` at every lag, both directions. **PASS/MISS**

### (d″) the distributional arm read inside its window

Same topologies (d) and (d′). Changes, both forced by the design law above and both
declared now:

* probe site for the **distributional** arms moves to the interface, `site = 15`
  (`LINK_FROM`), so `ℓ = 1`; predicted headroom `A·e^{−λ}/σ ≈ 0.4·0.5/1e−3 ≈ 200`.
* distributional lag `DIST_LAG = 6`, inside `[ℓ, ℓ + ln(1/σ)/λ] ≈ [1, 11]`.
* the (d′) trap keeps its probe at site 0 — that is where its selector lives — and is read
  at the same lag 6.

* **g1** (d) distributional arm: permutation `p < 0.01`. **PASS/MISS**
* **g2** (d′) distributional arm: permutation `p > 0.05` — still null, i.e. the fix does
  not manufacture an effect where there is no causation. **PASS/MISS**
* **g3** the two-arm rule (pathwise **and** distributional) accepts (d) and rejects (d′).
  **PASS/MISS**

* **g4** (reported, not staked) the pathwise onset latency for the interface probe in (d),
  predicted `== 1`.

## What a miss means, written now

* **e2 or f1 misses** → this synthetic family cannot make the observational detector
  false-fire, and the claim "intervention separates what observation confounds" is
  supported here only by theory (Theorem 3) plus COMPOSITION-2's own B1, not by this
  instrument. I say exactly that and stop.
* **e3 or f2 misses** → the interventional signature itself has failed a planted null, and
  the brick fails. This is the arm that would actually hurt.
* **g1 misses** → the distributional adjudicator is not usable at these noise levels, and
  the stochastic version of the signature is recorded as pathwise-only, with the trap
  unresolved. That is a real limitation and it would be reported as one.
* **g2 misses** → the fix manufactured an effect; the design law is wrong and the whole
  distributional apparatus is void until repaired.
