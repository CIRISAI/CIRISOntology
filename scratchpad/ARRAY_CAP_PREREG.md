# PRE-REGISTRATION — CIRISArray cap-compliance + ceiling fraction (frozen before any result)

Written and committed BEFORE any hardware run. Two jobs, both new, both staked against
theorems in `CIRISOntology/Core/ShareK.lean`.

## What this experiment is, and is NOT

**JOB 1 — CAP COMPLIANCE: an instrument control for the published Bell-test claim.**
`ShareK.lean` proves `shareK_le_of_pair_uniform`: every classical k-slot state with a
uniform pair marginal has share ≤ (k−2)·log 2, and the deviation-robust
`shareK_le_log_sub_pair`: share ≤ k·log 2 − H(any pair marginal), with no uniformity
assumed. The published Bell claim rests on a *quantum* state exceeding the classical cap.
The matched control that has never been run: drive a genuinely **classical physical
substrate**, read k channels, push them through the **same share pipeline**, and confirm
it never reports above the proved cap. A pipeline that hallucinated super-classical values
on classical hardware would void the Bell claim. This is an audit of the instrument, not a
discovery.

**JOB 2 — CEILING FRACTION: how much of the proved classical ceiling real coupled
dynamics actually uses.** Report share / cap as a fraction, at k = 3 and k = 5, across the
coupling dial. New because the ceiling is machine-checked and the substrate is real; it
does not require the numerator to be surprising.

**NOT CLAIMED, PRE-COMMITTED HERE.** This experiment does **not** claim to discover
order-3 / whole-only structure in the array, and no result of it may be so framed. The
2026-07-24 hunt established that (a) order-3 temporal structure in a coupled-logistic
lattice is **expected** — nonlinear/chaotic dynamics generically carry it, so its presence
is not news; (b) it is **implementation-sensitive** — clip boundary gave C3 = 0.0065 where
wrap gave 0.0000 at the same coupling, and this kernel's own
`fminf(fmaxf(x,0.001f),0.999f)` *is* that clip; (c) a clip artifact **survives an IAAFT
null at z = 86**, so IAAFT survival certifies nothing. A positive ceiling fraction in a
temporal reading is therefore the expected outcome and is reported as a magnitude, never
as a finding.

## Substrate — the REAL runtime

The ACTUAL CIRISArray GPU kernel: `/home/emoore/CIRISArray/src/runtime.py`,
`Ossicle.KERNEL_CODE` / `Ossicle.measure`, driven on the RTX 4090 Laptop GPU exactly as
`bench_results.md` drove it. No numpy reimplementation. If the kernel cannot be driven,
the run is abandoned and reported as such — no substitute.

Held at the validated stochastic-resonance operating point (Eric's standing instruction):
`r_base = 3.70`, `r_spacing = 0.03`, `twist_deg = 1.1`, `n_cells = 64`, `iterations = 100`,
array 3 × 64 = 192 ossicles, additive `sigma = 1e-3` Gaussian noise on the oscillator
states between the kernel's 100-iteration bursts (the kernel has no per-iteration noise
hook — same caveat as the bench).

**The device's actual coupling graph, stated up front** (read off the kernel, lines
175–177): within one ossicle and one cell index, the three oscillators form a **chain
a — b — c**: `new_a += κ·cos(twist)·(b−a)`, `new_b += κ·(a+c−2b)`, `new_c +=
κ·cos(2·twist)·(b−c)`. Cells do **not** couple to one another, and ossicles do **not**
couple to one another. Consequently the array has exactly one native coupled spatial
structure — the 3-node chain — and **no native 5-node spatial structure**. This is stated
before the run so that the k = 5 spatial reading's expected floor result cannot be
retrofitted as a finding.

`κ` (coupling) is the dial: **κ ∈ {0.00, 0.02, 0.05, 0.10, 0.20, 0.35, 0.50}**, with 0.05
the validated bench operating point.

## The boundary discriminator — MANDATORY, pre-registered as decisive

Every condition is run under **both** boundary treatments, compiled from the **same**
`KERNEL_CODE` string with **only** the three clamp lines replaced, nothing else touched:

- **CLIP** (native, as shipped): `a = fminf(fmaxf(new_a, 0.001f), 0.999f);`
- **FOLD** (reflecting): a continuous triangular fold of the same interval — no flat
  region, no pile-up, no ties manufactured at the boundary.

A third, **instrumented** CLIP kernel counts how often the clamp actually binds, reported
as the **clip-binding rate** per coupling. This matters and is pre-registered as an
interpretation rule: at couplings where the binding rate is **zero**, CLIP and FOLD are
*the same function on the data that occurred*, so agreement there is **trivial and must be
labelled trivial** — it is not evidence of robustness. Only agreement at couplings where
the clamp demonstrably binds is a robustness pass.

**Stability criterion (only STABLE numbers may be quoted as measurements of the
substrate):** for the same reading and coupling, with ceiling fractions `CF_clip`,
`CF_fold`,
- **STABLE**: (|CF_clip − CF_fold| ≤ 0.02 absolute OR ≤ 0.20 × max(|CF_clip|,|CF_fold|))
  AND both agree on whether the reading clears its surrogate floor at z > 5.
- **ARTIFACT**: they disagree on clearing the floor at z > 5, OR the relative difference
  exceeds 1.0 (a factor of two). Reported as an implementation artifact, per the standing
  trap, and never quoted as a property of the substrate.
- **MARGINAL**: anything in between. Reported, not quoted.
- **TRIVIAL**: clip-binding rate is exactly zero at that coupling — agreement carries no
  information and is labelled so.

## Readings (all binarized at each channel's OWN median, b = 2; tied fraction disclosed)

From one recorded trajectory per (κ, boundary): states `[N, 192, 3, 64]` plus the kernel's
`phase` outputs `[N, 192]`. N = 400 bursts after 50 settle bursts.

COUPLED readings (the substrate measurement):
- **S3-state** — SPATIAL k = 3: channels = the three oscillators (a, b, c) at one cell and
  one time. Samples = all 192 × 64 = 12 288 (ossicle, cell) units, pooled over every 8th
  time slice. The array's only native coupled spatial structure.
- **T3-state** — TEMPORAL k = 3: channel = oscillator **b** (the chain's centre node) raw
  cell state at times t, t+1, t+2. Non-overlapping stride-k windows (primary); overlapping
  windows reported as a secondary, with the overlap disclosed.
- **T5-state** — TEMPORAL k = 5: same, times t … t+4.
- **X5-state** — SPATIOTEMPORAL k = 5: (a_t, b_t, c_t, b_{t+1}, b_{t+2}). The only k = 5
  reading on this device in which all five slots are causally connected.

ARCHITECTURALLY-UNCOUPLED controls (the lead's literal group-mean-of-phase specification;
independent by construction, so expected at the estimator floor):
- **S3-phase** — SPATIAL k = 3: group-means of the kernel's `phase` metric over 3 disjoint
  ossicle groups, exactly as in `bench_results.md`. Separate 8 000-burst loop.
- **S5-phase** — SPATIAL k = 5: same over 5 disjoint ossicle groups.

CAP-SATURATING STRESS TEST (the sharpest possible instrument control — the cap is tested
*at* its boundary, not in a regime where compliance is trivial):
- **P3-inject** — the bench's f = 1 parity injection at k = 3 (`bench_experiment.py`
  construction: a, b independent uniform, c = a ⊕ b, injected as coupling modulation). The
  three-coin parity state **exactly saturates** the k = 3 cap (`share_parity` = log 2 =
  (3−2)·log 2). The pipeline must approach it and must never exceed it.

## GATE — machinery self-test, BEFORE any hardware. FAIL ⇒ stop, no run.

The k-slot share is `shareK(p) = H(pairwise-maxent(p)) − H(p)`, the maxent computed by
iterative proportional fitting to all C(k,2) pair marginals from the uniform start (the
I-projection of uniform, hence the maximum-entropy member of the pair envelope).

1. k = 3 exact parity → share = log 2 = 0.693147 (saturates its cap exactly).
2. k = 3 exact independent uniform → share = 0.
3. k = 5 exact **pair-uniform code state**: uniform on the 8 points
   (x₁, x₂, x₃, x₁⊕x₂, x₁⊕x₂⊕x₃). All 10 pair marginals are uniform, so its share is
   5·log 2 − 3·log 2 = **2·log 2 = 1.386294** — which is exactly the known exact classical
   maximum at k = 5 (`scratchpad/temporal-share/CLASSICAL_MAX_K5.md`, exact-computed, not
   mechanized). Must reproduce to 1e-9, and must sit below the proved cap 3·log 2.
4. k = 5 exact independent uniform → share = 0.
5. IPF convergence residual < 1e-12 on every gate case.
6. Sampled versions of 1–4 at hardware-scale T, through the full pipeline including the
   surrogate null.

## The two caps, and the tiers kept unblurred

| k | machine-checked cap (k−2)·log 2 | exact classical max (computed, NOT mechanized) |
|---|---|---|
| 3 | 0.693147 | 0.693147 (parity saturates — same number) |
| 5 | 2.079442 | 1.386294 |

At k = 5 the proved cap is **not tight**; both are reported, each labelled with its tier.
Only the machine-checked number may be cited as proved.

## Nulls (and what is deliberately not used)

- **Matched pairwise-maxent multinomial surrogate** (the bench's `surrogate_null`,
  generalized to k slots): draw T samples from the order-3-free maxent distribution
  carrying the observed pair marginals; recompute share. This is the **estimator bias
  floor**. 60 draws; mean ± sd; z = (share_obs − mean) / sd.
- **Shuffle floor**: independently permute each channel across samples, destroying all
  cross-channel structure; recompute share.
- **IAAFT is NOT used and would not certify anything.** Stated plainly per the standing
  trap: a clip artifact survived IAAFT at z = 86 on 2026-07-24. Its survival is not
  evidence, so it is not run and its absence is not a gap.

## Pre-registered meaning of EVERY outcome

**JOB 1 (cap compliance).** Primary statistic per reading:
`cap_robust = k·log 2 − max_{i<j} H(p̂_ij)` (the tightest proved bound over pairs, valid
with no uniformity assumption); `cap_headline = (k−2)·log 2`.

- **COMPLIANT**: every reading — all couplings, both boundaries, both k, controls, and the
  cap-saturating stress test — satisfies `share_obs ≤ cap_robust + 1e-9`; and the two
  engine steps hold numerically for every pair: `H(pushforward to pair) ≤ H(whole)`
  (`entropy_map_le`) and `H(maxent) ≤ k·log 2`. ⇒ the share pipeline does not manufacture
  super-classical values on classical hardware; the Bell-claim instrument passes its
  matched control. This is a control passing, not a discovery, and will be reported as
  such.
- **VOID — reported loudly**: ANY reading exceeds `cap_robust` by more than 1e-9. The
  proved theorem forbids it for any probability distribution, so any occurrence is a
  pipeline defect (IPF non-convergence, binning, or estimator). On VOID: nothing about the
  substrate may be quoted from this run, and the Bell claim's instrument is reported as
  broken pending repair.
- **CAUTION, not VOID**: a reading exceeds `cap_headline` = (k−2)·log 2 while its pair
  marginals are measurably non-uniform. The theorem permits this — the headline form has a
  uniformity hypothesis. It is reported as a warning against citing the headline cap on
  hardware, together with the measured pair-entropy deficit. Exceeding `cap_headline`
  while all pair marginals are uniform **within sampling error** is instead a VOID.

**JOB 2 (ceiling fraction).** `CF = (share_obs − null_mean) / cap`, bias-corrected;
raw `share_obs / cap` reported alongside. Both caps at k = 5.

- Reported as a table: reading × κ × boundary, with CF, z vs the surrogate floor, tied
  fraction, clip-binding rate, and the clip/fold **stability verdict** column.
- **Only STABLE (and non-TRIVIAL) entries are quoted as measurements of the substrate.**
- **No entry, at any value, is a discovery of order-3 structure.** Pre-committed above.
- A CF near zero in the architecturally-uncoupled controls (S3-phase, S5-phase) is the
  **expected** result and doubles as the estimator-floor check; if those controls instead
  fire at z > 5, the run is **VOID** for the same reason as above (false positive on
  channels that cannot physically be coupled).

## Reproducibility and discipline

Primary seed 20260725; headline conditions replicated at seeds 99 and 7. Tied fraction
disclosed for every reading; a reading with tied fraction > 0.01 is flagged
tie-contaminated and reported separately rather than quoted. Scratchpad only: nothing
touches `Stance.lean`, the Lean library, or the audit; no `lake`. Prereg committed before
the run; results and script committed after. Research → scratchpad memo → Eric's review.
