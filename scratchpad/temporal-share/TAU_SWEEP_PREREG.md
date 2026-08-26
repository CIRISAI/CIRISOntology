# Pre-registration — τ SWEEP: is the idle residual dynamical or preparational?

**2026-08-26, written and committed BEFORE the instrument is extended and before any
reading.** Sequel owed by `CLOSURE_PILOT_RESULTS.md`. Raw:
`tau_sweep_<jobid>.json`. Results: `TAU_SWEEP_RESULTS.md`.

## 0. The question, and why it has a clean answer

The pilot returned DIRTY BASELINE: at τ = 64 ns the idle pair read
`Δ_{B→A} = 1.67×` its floor. Three explanations were named and not separated —
chance, preparation/readout correlation, or dynamical coupling.

**τ separates them, because independent decay is a product map.** If A and B each relax
under their own channel, `A_out` depends only on `A_in` and `B_out` only on `B_in`. That
is a product map, and `Core/MatterCoupling.independent_views_closed` proves both views
are `Closed` for **every** product map. So decoherence, however severe, cannot manufacture
a cross-residual. A residual that GROWS with τ is coupling; one that is FLAT is fixed
cost at preparation or readout.

## 1. The correction I owed, declared in advance

`CLOSURE_PILOT_RESULTS.md` recorded a defect in its own frozen design: no
family-wise correction, four quantities tested, ≈19% family-wise false-positive rate.
That defect is not repeated.

**This sweep tests 12 quantities** (2 directions × 6 delays). The per-test floor is the
**99.583rd percentile** of the permutation null — `1 − 0.05/12`, Bonferroni at
family-wise α = 0.05 — not the 95th. 2000 permutation replicates, up from 500, so the
upper tail is resolved. **Declared here, before data.**

## 2. Design

Idle arm only — no CRX. Same pair (95, 99) and same screening as the pilot, so the sweep
is comparable to it. Same statistic (`D_JS`, nats), same permutation scheme (shuffle the
other input's label within each stratum of the target's input).

τ ∈ {16, 64, 256, 1024, 4096, 16384} dt = {64 ns, 256 ns, 1.02 µs, 4.10 µs, 16.4 µs,
65.5 µs}, spanning three orders and reaching T1 scale. 4 basis preparations per τ,
4096 shots, **one job, all delays interleaved**.

## 3. Outcomes, all named

| outcome | criterion | reading |
|---|---|---|
| **DYNAMICAL** | `Δ_{B→A}` exceeds the corrected floor at ≥1 τ **and** rises with τ (Spearman ρ > 0, p < 0.05 over the 6 points) | The pair is genuinely coupled. The four-arm's independent arm must carry a measured, τ-dependent baseline. |
| **PREPARATIONAL** | exceeds the corrected floor at ≥1 τ **and** shows no rise (ρ not significant) | Fixed cost at preparation or readout. Subtractable as a constant; the four-arm's independent arm carries a measured CONSTANT baseline. |
| **CLEAN** | no τ exceeds the corrected floor | The pilot's 1.67× was the ≈19% family-wise chance its own results file flagged. **DIRTY BASELINE is retracted, and the retraction is recorded next to the original.** |
| **VOID** | job error, drift, or screening failure | Reported as VOID, never as any of the above. |

**CLEAN is a live outcome, not a formality.** The pilot's own results file predicted it
as consistent with chance, and this design is powered to say so.

## 4. No rescue

One job. No refitting τ, no dropping delays, no switching statistic, no re-running to
chase a trend. If the Spearman test sits at the boundary it is reported at the boundary.

## 5. Cost

24 circuits × 4096 shots, budgeted ≈25–35 s against 583 s remaining. The long delays
dominate: 65.5 µs × 4096 shots × 4 preparations is ≈1.1 s of pure idle in the longest
cell alone.

## 6. What this does NOT buy

This is instrument characterisation. It decides what the four-arm's baseline must be. It
tests nothing in the stance, and a DYNAMICAL reading would be ordinary two-qubit
crosstalk — a known property of superconducting hardware, not a discovery.
