# Pre-registration — the closure defect against thermodynamic ground truth (STAGE-1 FREEZE)

**2026-08-26, frozen while the 8.43 GB archive downloads and before any trajectory byte
is READ.** Target: Zenodo 13829200, *Learning efficient erasure protocols for an
underdamped memory* (Barros, Whitelam, Ciliberto, Bellon; arXiv:2409.15050;
md5 `4e90d7c3fcb4b280ba13e03a7b7b43ab`). This is the H1′/rent bridge on data with real
thermodynamic ground truth — the reason the fiber battery was run at all.

## 0. What is already known, declared so blindness is honest

The PAPER has been read (it is the codebook): system = underdamped cantilever with a
feedback double-well; four protocols (basic, velocity-kick, learned-single,
learned-repeated); per-trajectory work `W = ∫∂ₜU dx dt`; success = `x(t_f) < 0` AND
remaining in-well through a quiescent period; T_eff from velocity distributions;
~4×10³ experimental single-erasure trajectories, 665–10³ repeated. **Therefore
protocol-LEVEL outcomes are not blind** (the paper reports which protocols win) and no
protocol-level claim is staked. **Per-trajectory relations within a protocol are blind**
— the paper does not report witness–work or witness–survival correlations — and every
stake below lives there.

## 1. The analysis, frozen unchanged from the validated chain

The battery-validated estimator (`fiber_pilot.py` pipeline, `battery.py` machinery):
coarse view = the BIT (`sign(x)`); fibers = within-well position rank × velocity rank;
gains in held-out bits/sample with block CIs; state-conditional AR(2) surrogate gate;
the instrument floor rule (any cell < 5× the gauge floor reports BELOW-FLOOR).
**A fresh planted-truth gauge on synthetic underdamped Langevin (matched f₀, Q) runs
BEFORE unblinding — E0d — because the floor is substrate-dependent.**

## 2. The stakes, separable, each with its kill

- **E1 — the memory's bit view is not closed at short times.** During the quiescent
  period, within-fiber witness improves prediction of the future bit above the gauged
  floor at horizons ≪ the relaxation time, and the gain CONTRACTS.
  *Kill:* nothing above floor ⇒ the closure defect is unmeasurable on the best
  available substrate; the field arm of the hunt records a null.
- **E2 — the contraction time is PHYSICAL and PARAMETER-FREE (the rule-6 stake).**
  τ_c during quiescence equals the cantilever's energy relaxation time τ_R = Q/(π f₀)
  **within a factor of 2**, with Q and f₀ pinned from the dataset's own metadata at
  stage-2, before unblinding. *Kill:* τ_c off by >2× either way — the estimator reads
  something other than the physical memory of the fiber.
- **E3 — the closure defect predicts SURVIVAL (the decisive bridge).** At
  end-of-protocol, witness (in-well position rank, velocity rank) predicts survival
  through quiescence BEYOND the bit itself, > 5× floor; and the VELOCITY component
  exceeds the position component (the underdamped signature — v decides recrossing).
  *Kill:* no witness gain on survival ⇒ closure-defect-predicts-outcome dies here, on
  the substrate best equipped to show it.
- **E4 — the work bridge (H1′/rent).** Within each protocol, mean per-trajectory work
  is monotone in the initial velocity-magnitude quartile (kinetic energy must be
  dissipated to settle: more initial witness ⇒ more work). Direction staked, derived
  from the physics, not fitted. *Kill:* flat or non-monotone in EVERY protocol.
- **E5 — temperature, measured companion only.** T_eff (repeated runs) vs witness
  content is REPORTED with no staked direction and no kill: no derivation exists, and
  an undirected stake would be decoration.

## 3. THE TREE (pre-committed branches; nothing else runs)

- **E0a** md5 verify → *fail:* refetch once; twice ⇒ VOID.
- **E0b** extraction (tooling via the no-sudo micromamba route if needed) → *fail:* VOID.
- **E0c** STRUCTURE inventory ONLY — file names, shapes, README, metadata (f₀, Q,
  sampling rate, protocol labels). **No trajectory values are analyzed.** Produces the
  STAGE-2 FREEZE: exact field mapping, τ_R computed and written down, sample counts,
  and per-stake n declared. Committed before any value is read.
- **E0d** planted-truth gauge on synthetic underdamped Langevin (matched f₀, Q, planted
  witness→switch coupling + null) → *floor gauged; if the planted effect is NOT
  recovered:* STOP — the estimator does not transfer to underdamped dynamics, recorded
  as an instrument boundary, no stake is adjudicated.
- **E1 fails** → E2/E3/E4 still run (separable); the null is the finding.
- **E2 fails with E1 passing** → branch E2′: recompute τ_c per protocol; if it matches
  the PROTOCOL duration instead of τ_R, the witness is protocol-imprinted, reported as
  such (a finding, not a rescue — the stake stays failed).
- **E3 velocity < position** → the underdamped signature is absent: report INVERTED,
  stake failed, and check (pre-committed) whether the sampling rate resolves velocity
  at all (metadata question, answerable without new stakes).
- **E4 monotone in some protocols only** → report per-protocol; the stake passes only
  on EVERY-protocol failure of the kill, i.e. it fails as staked unless all four are
  flat/non-monotone... stated precisely: the STAKE passes if ≥3 of 4 protocols are
  monotone increasing; kill fires if 0 are.
- **Family-wise:** four staked claims ⇒ CIs at 98.75 % (Bonferroni 0.05/4) wherever a
  CI decides; surrogate gates at the 95th percentile as validated.

## 4. No rescue beyond the tree. Stage-2 freeze is the only permitted amendment,
and it may pin mappings and counts only — never move a stake, a band, or a kill.
