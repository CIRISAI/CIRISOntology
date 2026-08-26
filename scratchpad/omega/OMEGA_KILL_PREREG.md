# Pre-registration — Ω-KILL: the square against three substrates, binary exit

**2026-08-26, frozen before any instrument is extended.** The successor the
falsification earned, with every repair inherited: data-closable exits, in-job
anchors, realized arrows, μ load-bearing (observational arms only on stochastic
substrates), interventional arms where determinism lives, gauges with a
DETECTABLE-VIOLATION check (a ruler that cannot fire is decoration).

**Claim on trial:** the SQUARE (`OBJECT.md`) — its five theorem-backed laws hold
with measured parameters, cross-substrate, zero refits. **CONFIDENCE ⇔ all staked
arms pass. FALSIFICATION ⇔ any posable arm misses.** VOID only for double device
failure or gauge STOP; the test VOIDs if fewer than two substrates stay posable.

## S1 — QPU, one job (~30 s), floors and references in-job

| arm | stake |
|---|---|
| A1 idle @τ₀ | both directional defects ≤ 3× floor |
| A2 one-way CRX | fwd ≥ 50× floor ∧ asymmetry ≥ 5× |
| A3 hop `XXPlusYY(π/2)` | both ≥ 10× floor ∧ asymmetry ≤ 3× |
| A4 common-driver (X⊗X pooled 50/50) | both ≤ 3× floor ∧ created ≥ 50× its floor — **replication of the discriminator** |
| **A5 THE MIXING BOUND, theorem-to-hardware** | idle at delays {τ₀, 2τ₀, 3τ₀, 4τ₀}: α̂ = Dobrushin coefficient of the measured 1-step 4-state kernel; staked: **defect(m) ≤ α̂^m + 3σ_boot at m ∈ {2,3,4}** (`defect_le_alpha_pow` on the realized channel). Kill = violation at any staked m: the channel breaks the Markov structure the theorem needs — an honest boundary of the mixing rung on this hardware |

## S2 — engine, INTERVENTIONAL ONLY (the falsification's lesson), per the 8 requirements

| arm | stake |
|---|---|
| B1 sham (twin sessions, no probe) | divergence **exactly 0** at every recorded frame — deterministic twins; nonzero = identity instability, arm fails |
| B2 pre-probe window | **exactly 0** before the probe frame |
| B3 sector response | probe in the LEFT sector: response onset in the left sector strictly earlier than in the right (light-cone ordering, integer frames) |
| B4 K, honest instrument | pedestal-free K (sham-subtracted by design) ≤ 1.05 |

## S3 — tweezer trace, fresh stake on wild data

| arm | stake |
|---|---|
| **M1 THE MIXING BOUND in the wild** | empirical (bit × 4-fiber)-state kernel at lag 1 from the train split; α̂ its Dobrushin coefficient; staked: **held-out defect(m) ≤ α̂^m + 3σ at m ∈ {2, 4, 8}**. Fresh — never computed on this data |

## Gauges (before any unblind; shared machinery)

G1: synthetic Markov chain with known α — the estimator must land α̂ within CI and
the bound must HOLD. G2 **the violation check**: a planted NON-Markov chain (hidden
regime) where the true lag-m defect EXCEEDS α̂₁^m — the instrument must FIRE. If it
cannot detect a planted violation, STOP (S1-A5 and S3-M1 unposable). S2's sham arm
is its own gauge.

## Tree

Family-wise: floors at the 99.5th pct; the A5/M1 σ from 500 bootstrap resamples;
Bonferroni across the 10 staked arms where p decides. S1 job VOID on device error →
one unchanged resubmission. No rescue; misses are final; the two verdict sentences
are `COMPOSITION2_PREREG.md` §0's, with "square" for "closure model".
