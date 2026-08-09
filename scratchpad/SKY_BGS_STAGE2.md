# STAGE 2 (partial) — occupancy PASSES at the surviving cell, G9 passes, and **RULE S2-A FAILS**

Stage 1 left exactly one admissible cell: `R = 10`, `b = 4`. Stage 2 is the floor model and the
**G10 closure, which the prereg names the go/no-go**. This document reports the two Stage-2 rules
that run *before* G10, and one of them fires.

**Still blind.** Every number here is from N-body mock realizations. No DESI galaxy statistic has
been computed.

---

## S2.1 The suite question, answered by measurement — and it removes a rule

The prereg's §11 assumed both suites would serve. They do not, and which one serves is not a
choice:

| suite | ships | in-shell N | vs the S0-A sample | usable here? |
|---|---|---|---|---|
| **AbacusSummit** bright/v1, 25 realizations, **N-body** | `BGS_BRIGHT` *and* `BGS_BRIGHT-21.5` | 2 106 346 | **0.968 of data** | **yes** |
| **EZmock** bright/v1, 1000 realizations, approximate | `BGS_ffa` only | 218 203 total | **1.0027 of `-21.5`**, 0.075 of `BGS_BRIGHT` | **no** |

EZmock's `BGS_ffa` matches `BGS_BRIGHT-21.5` to **0.27 %** over the identical `z` span
(0.100–0.400). **It models the sample S0-A did not choose.** A floor model built from it would be
a floor model for a 13× sparser catalogue.

**Consequence: RULE S2-B — the cross-suite `σ` closure — is NOT RUNNABLE on this sample.**
Recorded as not-runnable, never as passed. The prereg contemplated the inverse case ("*if only
EZmock exists… recorded, not fatal*"); the measured case is that only **AbacusSummit** exists for
the chosen sample. It is the *better* suite (N-body, which BOSS's Amendment 4 could not obtain)
and the *smaller* one, and the smallness is the problem below.

---

## S2.2 Occupancy and G9 — both PASS at the surviving cell

| | |
|---|---|
| occupancy at `R = 10`, `b = 4` | **263.3** against a floor of 100 — **PASS** |
| G9 IPF certificate, worst across 8 realizations × 3 configs | **1.4 × 10⁻¹²** against `< 1e-9` — **PASS** |

Stage 1's projection was 186; the measured 263 is higher because the grid here is fitted to the
randoms alone rather than to the union of two random halves. Either way the cell clears the floor
with room, and **Stage 1's corrected verdict — "the primary scale is dead, one registered
extension cell survives" — is confirmed by measurement.**

---

## S2.3 RULE S2-A — **FAILS**, on all three configurations

*"Measure the per-realisation scatter of `I_C⁽³⁾` on the first 8 DESI mocks before committing to a
suite size. If the scatter exceeds 3 % of the floor mean, the transported argument fails and the
required `n` is recomputed and recorded in an amendment."*

| config | mean `I` | sd | scatter | S2-A |
|---|---|---|---|---|
| folded | 7.814 × 10⁻⁴ | 4.42 × 10⁻⁵ | **5.66 %** | **FAIL** |
| equilateral | 2.197 × 10⁻³ | 7.36 × 10⁻⁵ | **3.35 %** | **FAIL** |
| squeezed | 1.330 × 10⁻³ | 4.28 × 10⁻⁵ | **3.22 %** | **FAIL** |

**All three exceed the threshold; `folded` by nearly double.** The transported argument — that a
small suite suffices because per-realisation scatter is small — does not hold on DESI BGS
geometry, and the required `n` must be recomputed.

**What the suite can deliver, at the worst-config scatter of 5.66 %:**

| `n` | floor mean known to | `σ` known to |
|---|---|---|
| 8 (run) | 2.00 % | ±26.7 % |
| **25 (the entire suite)** | **1.13 %** | **±14.4 %** |
| 100 | 0.57 % | ±7.1 % |
| 1000 | 0.18 % | ±2.2 % |

**25 is the whole suite. There is no 100 and no 1000 for this sample.** The prereg's own §5
warned that a `σ` carrying ±14 % from ensemble size alone is *"repeating BOSS's weakest habit"* —
and ±14.4 % is precisely what the complete available suite delivers.

---

## S2.4 Where this leaves the campaign, stated without a verdict I am not entitled to give

**Passed so far:** occupancy at the surviving cell, G9 at every realization and configuration,
the geometry gate of Stage 1, and every Stage-0 rule.

**Fired so far:** RULE S2-A (all three configs). **Not runnable:** RULE S2-B.

**Not yet run: G10, the go/no-go.** It needs the full 25-realization suite split into
model-building and held-out halves, and it is the gate the prereg says this measurement *"most
plausibly fails"* given a floor that ran 100–130 % of signal in BOSS.

**The honest arithmetic before running it.** G10 requires the floor model to reproduce held-out
mocks to **10 % of the signal**. The floor mean is knowable to 1.13 % at `n = 25` — comfortable.
But the closure is tested against a *held-out half*, so the comparison carries roughly
`5.66 % / √12 ≈ 1.6 %` on each side. That is inside 10 % of the floor. **Whether it is inside
10 % of the *signal* cannot be known while blind**, and that is exactly the quantity G10 exists to
decide.

**What must be recorded in an amendment before Stage 3, per RULE S2-A's own text:** the
recomputed `n` is **25 — the entire available suite** — and the campaign therefore proceeds, if it
proceeds, with a `σ` uncertain by **±14.4 %** from ensemble size alone. Any significance this
campaign ever quotes inherits that, and must carry it on the same line.

**Next, in order:** download realizations 8–24; run G10 on the 12/13 split; then Stage 3 only if
G10 passes. **If G10 fails, the campaign is VOID by the prereg's own table** — and that is a
clean, pre-registered ending, not a disappointment.
