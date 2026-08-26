# Pre-registration — the two DISCRIMINATING arms: reciprocal, and joint-view restoration

**2026-08-26, frozen before the instrument is written and before any reading.** Raw:
`restoration_<jobid>.json`. Results: `RESTORATION_RESULTS.md`.

## 0. Why these two and not the first two

The pilot and τ sweep ran the **independent** and **one-way** arms. Both outcomes were
expected before they ran, and `OBJECT.md` records them as instrument validation rather
than support. These two are the arms where the closure language can be **wrong**.

`Core/MatterCoupling.lean` claims a specific 2×2:

- neither marginal view closes under coupling (`matter_not_closed`, `flux_not_closed`),
- **but a LOSSY joint view can still be `Held`** (`gauss_held`), with `gauss_is_lossy`
  proving that view genuinely discards information so the closure is not the identity
  view in disguise.

The second half is the recursion's own claim: **non-closure is resolved by refinement.**
Nothing in the campaign has tested it.

## 1. The instrument, and why the joint view is non-vacuous

Same preparation-based transition matrix as the pilot (input known by preparation,
output measured; no mid-circuit measurement), same pair (95, 99), same `D_JS` statistic
in nats, τ = 64 ns.

The joint view is **total excitation number** `n = a + b ∈ {0,1,2}`. It is LOSSY by
construction: `|01⟩` and `|10⟩` both read `n = 1`. **That is what makes the test
non-vacuous** — the full joint state closes trivially (`exists_closed_view`: every step
closes the identity view), so testing it would prove nothing. `n` throws information
away, and closure asks whether what it threw away matters for its own future:

> `Δ_joint = D_JS( P(n_out | in = 01) ‖ P(n_out | in = 10) )`

The two inputs share a value of the view and differ inside its fiber. If the view is
Closed, they must agree.

## 2. The two arms, one job, interleaved

| arm | gate | number-conserving? |
|---|---|---|
| **J** — hop | `XXPlusYY(π/2)` | **yes**, exactly |
| **R** — reciprocal | `CRX(π/2, 0→1)` then `CRX(π/2, 1→0)` | **no** |

Both couple in both directions, so both must break the marginals. They differ only in
whether the lossy joint view survives.

## 3. Frozen predictions, computed from the ideal unitaries BEFORE running

| arm | `Δ_A→B` | `Δ_B→A` | `Δ_joint` |
|---|---|---|---|
| **J** | above floor | above floor | **AT FLOOR** — ideal `P(n_out)` is `[0,1,0]` from BOTH `n=1` inputs |
| **R** | above floor | above floor | **ABOVE FLOOR** — ideal `[0,.75,.25]` vs `[0,.5,.5]`, `D_JS ≈ 0.034` nats, ≈100× the floor |

## 4. Correction, declared in advance

Six quantities (2 arms × 3 statistics). Per-test floor is the **99.167th** percentile
(`1 − 0.05/6`, Bonferroni FWER 0.05) of 2000 permutation replicates. The permutation for
`Δ_joint` shuffles the WITHIN-FIBER label (which of `01`/`10` a shot came from),
preserving the `n=1` pooled output distribution.

## 5. Outcomes, all named

| outcome | criterion | reading |
|---|---|---|
| **RESTORATION** | both marginals above floor in both arms; `Δ_joint` at floor in **J** and above in **R** | The 2×2 holds. A lossy joint view restores closure exactly where a conserved quantity exists and not otherwise. This is the first hardware test of the recursion's own claim, and it passes. |
| **RESTORATION FAILS** | `Δ_joint` ABOVE floor in **J** | The enlarged view does NOT restore closure where the theory says it must. **The recursion claim takes damage on this substrate** and the results file says so in its title line. Most likely mechanism is T1 decay, which does not conserve `n` — that is an explanation, not a rescue, and it must be measured (τ sweep) rather than asserted. |
| **JOINT CLOSURE IS GENERIC** | `Δ_joint` at floor in **R** as well | Joint closure proves nothing: it holds whether or not a conserved quantity exists, so it cannot be evidence for restoration. Kills the arm's discriminating power. |
| **MARGINALS SURVIVE** | either marginal at floor in either arm | The coupling did not take. Instrument failure, reported VOID, not a physics result. |
| **VOID** | job error, drift, screening failure | Reported as VOID. |

## 6. No rescue

One job. No refit of `θ` or τ, no dropped preparation, no re-run to chase a verdict, no
switching the joint view to something else if `n` fails. **If RESTORATION FAILS fires, it
is reported as the headline**, and any decoherence explanation is a follow-up
measurement rather than a reinterpretation.

## 7. Cost

8 circuits × 4096 shots, ≈10–15 s against 554 s remaining.

## 8. What a pass buys, stated narrowly

A conserved quantity surviving a coupling that conserves it is **ordinary quantum
mechanics**. The claim on trial is narrower: that the object's closure predicate,
frozen in advance, correctly separates the case where refinement restores prediction
from the case where it does not — with no per-arm refitting. That is one 2×2, on one
device, on one pair. It is not the maximal ontology, which by
`OBJECT_PRIOR_ART.md` needs one structure predicting all arms with fewer freedoms than
separate models.
