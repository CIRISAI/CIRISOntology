# WATER — AMENDMENT 12: arm A's pre-registered sweep fails its own §5.6 gate, and the label saturates on the control

**Written after `WATER_PREREG.md` was frozen and after amendments 1–11. `mW` configurations now
exist — the `λ` sweep of `WATER_ARM_A_GATE.md` ran to completion — and this amendment is written
BEFORE any share has been computed on any of them.** No share, on mW or on anything else, exists
at the moment of writing. The pre-registration is not edited.

**Occasion.** `WATER_PREREG.md` §5.6 fixes four equilibration checks and declares in advance:
*"Any state point failing any of the four is NOT RUN, not a null … a cavitated configuration reads
a large share that is a reading on a bubble."* **Check 4 was run on the completed sweep before the
estimator was, and it fires on six of the eight pre-registered `λ` points.** A second failure,
independent of the first and not fixed by moving the density, is found in the same measurement.

**This amendment changes what arm A can be scored on. It does not change P1–P4, P6–P8, or any
kill other than K1's gauge status.**

---

## L1. THE GATE FIRED — six of eight state points are two-phase

`water_homog.py`, over 11 frames per state point spanning the whole 500 ps production window, at
the pre-registered matched density `ρ = 0.997 g/cm³`, 298 K, NVT. **No share is computed in it;**
every quantity is a density or a geometric quantity the instrument is blind to, plus `p₁`, which
§5.4 already requires per cell.

| `λ` | cell over-dispersion | Poisson value | min cell count | max void (Å) | `⟨n⟩` at 3.50 Å | ideal-gas `⟨n⟩` | `p₁` | verdict |
|---|---|---|---|---|---|---|---|---|
| 0 | **0.875** | 0.179 | 0.0 | **13.06** | **12.61** | 5.99 | **1.000** | **CAVITATED** |
| 2 | **0.773** | 0.179 | 0.0 | **14.08** | **12.21** | 5.99 | **1.000** | **CAVITATED** |
| 5 | **0.603** | 0.179 | 0.0 | **11.96** | **11.85** | 5.99 | **1.000** | **CAVITATED** |
| 8 | **0.512** | 0.179 | 0.0 | **14.99** | **10.01** | 5.99 | **1.000** | **CAVITATED** |
| 11 | **0.426** | 0.179 | 0.0 | **13.37** | 8.69 | 5.99 | **0.996** | **CAVITATED** |
| 14 | **0.344** | 0.179 | 0.0 | **11.76** | 7.54 | 5.99 | **0.989** | **CAVITATED** |
| 18 | 0.235 | 0.179 | 1.5 | **9.08** | 6.27 | 5.99 | 0.950 | **CAVITATED** (void clause, L5) |
| **23.15** | **0.071** | 0.179 | **25.7** | **3.13** | 5.11 | 5.99 | 0.743 | **PASS** |

**Three independent diagnostics agree and none of them is marginal at the failing points.**

* **Over-dispersion.** A homogeneous liquid is *more* ordered than a Poisson process and must read
  **below** the Poisson value; mW at `λ = 23.15` reads `0.071` against `0.179`, i.e. `0.40 ×`, as
  it should. The `λ = 0` point reads `4.9 ×` Poisson.
* **Voids.** For a Poisson process at this number density the largest empty sphere over a `24³`
  grid exceeds `4.66 Å` with probability `0.01`. A real liquid produces *fewer* such voids. The
  failing points carry voids of **12–15 Å radius** — a bubble of ~25 Å diameter in a 39.15 Å box.
* **Coordination against the box mean.** At `ρ = 0.997 g/cm³` the mean number density implies
  `⟨n⟩ = 5.99` for an ideal gas and mW reads `5.11`. The `λ = 0` point reads **12.61** — the
  close-packed value. **The particles are not at the density the box says they are at.**

**Per §5.6, these six state points are NOT RUN. They are not nulls and no verdict is scored on
them.**

## L2. THE MECHANISM WAS MEASURED IN ADVANCE AND THE WRONG CONCLUSION WAS DRAWN FROM IT

`WATER_ARM_A_GATE.md` §4 measured G3 — removing the three-body term at fixed *pressure* makes the
liquid **2.40 × denser** — and concluded, correctly, that the sweep must be run at matched density
rather than matched pressure. It then disclosed the cost:

> *"at matched density `ρ = 1.0 g/cm³` the `λ = 0` liquid sits at a large **negative** pressure — it
> is being held open at a density its own potential does not want. **That is legitimate in NVT**
> and it is what 'matched density' costs."*

**It is not legitimate.** A liquid held at 42 % of its own liquid-branch density at 298 K is not
under tension; it is **inside the two-phase region**, and the constant-volume ensemble does not
prevent phase separation — it is the ensemble in which phase separation is *hosted*. The system
does the only thing available to it: it condenses into a droplet at ~2.4 g/cm³ and leaves a void.

**This is a warrant-reach instance (`GATES.md`, PROPOSED) of a variety not yet in that
registry's list.** The measurement was right (2.40 ×), the number was right, and the *inference
drawn from the right number* was wrong. And the refutation was already inside this campaign's own
battery: **§5.6 check 4 exists precisely to catch this, was pre-registered as mandatory "on every
negative-pressure point", and the sweep was run without it.** The campaign's gate battery
contradicted the campaign's own design document, and the contradiction survived because nobody ran
the gate before the instrument.

> **Recorded as the sharpest procedural finding of this campaign: a pre-registered gate is worth
> nothing at the moment it is most needed if the run order lets the measurement precede it.**
> §11's order of operations put `water_mw.py` (stage 2) before `WATER_RESULTS.md` (stage 5) but
> never fixed a stage at which §5.6 runs. It is fixed now: **§5.6 runs immediately after the
> configurations exist and before the estimator is imported**, and that ordering is what produced
> this document.

## L3. THE SECOND FAILURE — the label saturates, and moving the density does not fix it

Independent of cavitation, and more consequential: **at every `λ ≤ 14` the label composition is
`p₁ = 0.99–1.00`.** Every particle carries `n ≥ 5`. The `2×2×2` table collapses into a single
cell, the label entropy goes to zero, and with it the `ThirdCap` ceiling — `share_le_grouping_gaps`
bounds the share by a mutual information between a slot pair and the third slot, and that is
**exactly zero** on a constant label.

**A zero read from a collapsed table is outcome (g) CEILING-COLLAPSED — UNGAUGED — and it is not
the statement "the pair-potential liquid reads floor".** §5.4's rule is explicit: *a cell whose
ceiling is below 10 × its own floor is UNGAUGED*. A ceiling of exactly zero is below every floor.

**And this is not an artifact of the chosen density.** A *homogeneous* pair-potential liquid is
close-packed: at any density at which it exists as a liquid it carries ~12 neighbours inside
3.50 Å, so `p₁ = 1` there as well. The arm now running at each `λ`'s **own ambient density**
(NPT, 1 atm — `water_mw_amb.json`) measures this rather than arguing it, and its result is reported
in `WATER_RESULTS.md` whichever way it comes out.

> **THE FINDING, stated plainly because it is the substantive one: the `n ≥ 5` coordination label
> is not neutral between the two ends of the dose it was built to sweep. It is itself a
> tetrahedrality detector — it has variance only where a three-body term holds an open network
> open. P5 asked this label to compare a tetrahedral liquid against a close-packed one, and on the
> close-packed one it saturates.**

**Why stage 0 could not have caught it, stated so the failure is attributable rather than
diffuse.** `water_feasibility.py` bracketed the design with two synthetic proxies — an LDL-like
diamond/ice-Ic network and an HDL-like version of the same network with interstitials. **Both are
tetrahedral networks.** The *control* end of the dose — a close-packed liquid with no tetrahedral
term at all — was never proxied, so the one configuration that breaks the label was outside the
bracket that was built to test the label. This is `GATES.md` reach 13 (power of the control) in
its design-stage form: **the feasibility study gauged the instrument only over the range where it
works.**

## L4. WHAT P5 AND K1 CAN NOW BE SCORED ON — and K1 is UNGAUGED, which is not a pass

**P5 has two clauses and they now have different fates.**

| clause | status |
|---|---|
| *"at `λ = 0` it reads floor"* | **UNGAUGED.** The `λ = 0` point is cavitated (L1) and its label is degenerate (L3). Both failures are disqualifying on their own |
| *"the share increases monotonically with `λ`"* | testable **only** over the range where the configurations are homogeneous and the label has variance |

> **K1 — the campaign's premise kill — CANNOT FIRE AND CANNOT BE SURVIVED on the pre-registered
> design, and is recorded UNGAUGED.** K1 reads: *"if the mW share does not increase with `λ`, and
> in particular if the `λ = 0` pair-potential liquid does not read floor, then 'the pairwise-blind
> share reads three-body interaction physics' is refuted."* Its distinguishing observation is a
> floor reading at `λ = 0`, and that observation is unavailable: the state point does not exist as
> a homogeneous liquid at the pre-registered conditions, and where it does exist the label cannot
> resolve it. **An UNGAUGED premise test is reported as loudly as a fired one and is not
> convertible into a pass** (`GATES.md`, axiological layer 1).

**Consequence for the arms below it, stated so the separability is explicit.** §7's order of
operations justified running arm A first on the ground that *"if P5 fails on mW, no atomistic water
arm is worth starting."* **P5 has not failed; it has come back ungauged**, so that clause does not
fire and arms B–D are neither authorised nor cancelled by this document. Their own feasibility
verdicts (§7) stand exactly as frozen.

## L5. THE RESCOPE — declared here, with its polarity, before any share is read

Two gates, with thresholds fixed **now**:

> **G-HOMOG** (this amendment's instantiation of §5.6 check 4). A state point is read only if
> **both**: cell over-dispersion over `(L/4)³` cells `≤ 1.5 ×` the Poisson value `1/√⟨count⟩`;
> **and** the largest empty-sphere radius over a `24³` grid is below `r_void^max`, the radius a
> Poisson process at the same mean number density would exceed with probability `0.01` over the
> same grid (`4.66 Å` at `ρ = 0.997 g/cm³`, computed from the density, not assumed).
>
> **G-LABEL.** A state point is read only if `0.02 ≤ p₁ ≤ 0.98`. Outside that band the cell is
> **UNGAUGED** by §5.4's existing ceiling rule and is reported, never scored.

**On the pre-registered eight-point grid, `λ = 18` fails G-HOMOG on the void clause** (9.08 Å
against 4.66 Å) while passing the over-dispersion clause at `1.31 ×`. **The two clauses disagree
and the void clause is the one taken**, because it is calibrated against a computed Poisson
reference rather than against a factor chosen here; the disagreement is disclosed rather than
resolved by picking the answer that keeps a point.

> **P5′ — THE RESCOPED DOSE, staked before any share exists.** Over the `λ` range in which the mW
> liquid at `ρ = 0.997 g/cm³`, 298 K passes **both** G-HOMOG and G-LABEL, the floor-subtracted
> share **increases monotonically with `λ`**.
>
> **G-POL, declared:** a **PASS** is the share **rising** with `λ`. Flat or falling **fires the
> rescoped premise**, and is reported as the premise firing.
>
> **REACH, declared with the prediction rather than after it: P5′ tests the three-body dose
> WITHIN the tetrahedral regime. It does not reach the pair-potential limit, it is not a
> substitute for K1, and no reading of it may be reported as reaching either.**

> **P5″ — the density-ladder extension, declared now so it is not a post-hoc rescue.** The `λ`
> window that survives both gates at one density may be widened by *compressing* rather than
> stretching, since a compressed liquid cannot cavitate. A `ρ` ladder is run, **both gates applied
> byte-identically at every `(λ, ρ)`**, and the dose is scored **at fixed `ρ` across `λ`**, never
> along a path that moves both. If no density admits a `λ` window of at least three points passing
> both gates, **P5′ is reported NOT RUN on a two-point or one-point ladder rather than scored**,
> per §8 outcome (i).

## L6. WHAT DID NOT CHANGE

P1–P4 and P6–P8; K2, K3, K4, K-VOID, K-PIN, K-MINT, K-DOSE, K-CEIL, K-DYE; the feasibility verdict
(the LLCP remains out of reach by two to four orders of magnitude in wall time, and arms C, D, E
are untouched by this document); the floor law `0.43/N_tri` and the overlap penalty `1.9 ×`; the
primary template and the primary label; the template exclusions; amendments 1–11 entire. **K1 is
not withdrawn — it is marked UNGAUGED with the reason measured.**

Scope unchanged: simulated water models only; nothing bears on `wild-share`; `Stance.lean`
untouched; no Lean file opened; `lake` not run; nothing pushed.

## L7. FILES

| | |
|---|---|
| `water_homog.py` | the §5.6 equilibration/cavitation gate; computes no share |
| `water_homog.json`, `water_homog.log` | its readings on the completed `λ` sweep |
| `water_mw.py` | arm A instrument; extended here to record the production-averaged **pressure** (promised by `WATER_ARM_A_GATE.md` §4 and not previously recorded) and to support the §5.6 check-1 **cold start** |
| `water_arm_a.py` | the arm A analysis instrument. **A defect is recorded: as committed at `feae80c`-plus-working-tree it mis-parsed the LAMMPS dump header (`ITEM: ATOMS` unconsumed) and could not have run at all.** Fixed here; the fix is the reason no share existed before this amendment |
| `water_arm_a_queue.sh` | the supplementary run driver (fill, ambient, cold-start) |

Primary seed **20260727**.
