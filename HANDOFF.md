# HANDOFF — 2026-08-24, end of day

*Written at shutdown by the integrator while still holding the board, not reconstructed
from memory. A future session should be able to resume from this file cold. Every claim
here names its commit or its artifact; where something is owed, it names an owner.*

---

## 1. WHAT CLOSED TODAY

**NEWTON IS CLOSED** — under its own criterion, which was always `N-a…N-e green + wild pins
DECLARED on the closing certificate`. Two items landed to get there:
- **N-d** — `546ba51`, `Core/Aggregation.lean` (308 lines): `DependsWithinUpTo`, composition
  with additive error, the horizon, the aggregation warrant with its residual, and the
  `z^d/d!` instance. Correctly a NEW brick rather than a change to `Locality.lean`: N-d is
  Locality's *approximate analogue*, because the discrete boundary residual is exactly zero.
- **The closing certificate** — `48b93f1`, `ciris-sim-core/src/closing.rs`, 16 tests,
  CI-enforced at `.github/workflows/verify.yml:45`.

**Census: 0 Measured · 1 Published · 1 Stipulated · 3 OwedNoSource.** A count-based standard
was withdrawn as the wrong instrument: **WHY a pin is owed is the measurement.** The three
owed pins are **not missing parts of Newton — they are missing parts of the WORLD**, and
declaring them is what the criterion asks for. Structural result, enforced by biconditional:
**for an owed pin the falsifier and the unlock are the same event.**

**K1 and K2 were both already closed-killed** (2026-08-23) and had been mis-reported as open.
**CI stood down permanently** on Eric's directive — suite green, no standing lane.
**R3's first half** landed (`Core/StochasticHabit.lean`): `frameEntropy` and Shannon are the
same quantity on the uniform-on-fiber state; the reset channel drops entropy by exactly
`log 2`, so the deterministic second law **cannot** be repaired by weakening a hypothesis.

---

## 2. THE FIRED KILL — read this before touching N-e

**N-e's multi-resolution claim is REFUTED in the normal channel** (`5fee581`). Not
"unverified" — **measured false**. Full record: `PROGRAM.md`'s N-e entry and
`scratchpad/TRANSITION_MAP/REG_GAPS.md` row `N-e-PATCH`.

- **Instrument:** uniform-strain patch test (Irons & Razzaque 1972) at a refinement
  interface. Reference is the **continuum**, not the engine — which is what makes it not
  `SelfAudit`.
- **Reading:** uniform interior (n=616) max 1.320e-9 — **the control passes**; interface
  (n=78) median 8.149e-2.
- **The signature is the diagnosis:** over a 100× strain drop the uniform floor moves ×100.0
  (round-off) and the interface residual moves **×1.0000 — flat to four digits**. A
  consistency error, not a scale artifact.
- **Scope, not to be widened:** normal channel **only**. The tangential channel is
  rate-integrated, so a static test sees zero shear. **It refutes the half that was never
  supposed to be the problem** and is blind to the suspect half.
- **The four external anchors are untouched** — argued, not assumed: the test measures
  failure of *local equilibrium under an imposed field*, not violation of *pairwise
  action–reaction*, so momentum and the impulse window are structurally safe; the Griffith
  bound sums a material property over broken bonds, not a solver output; the energy
  inequality's margin far exceeds the defect. **The measured fracture threshold is the one
  genuinely touchable** — its value may shift, its zero/nonzero transition is robust.

**Newton stays closed; the close now carries a fired kill inside it, and the spine says so.**

---

## 3. OPEN, WITH OWNER AND NEXT STEP

| item | owner | exact next step |
|---|---|---|
| **§3.4 Byerlee inversion** | team-lead | Adjudicate against the sources. The PINNED specimen violates the criterion (LAC_DU_BONNET R = 29.0, μ = 1.16) while `DEMO_CALIBRATION` — the preset §3.4 says is NOT granite — sits inside the bracket at 15.8, μ = 0.74. |
| **Shear-half pin** (N-e) | research-manager-2 | REG_GAPS pin, deliberately **NOT** on the closing certificate — its discharge is internal, so it is a project debt, not one of the world's absences. Discharged when the tangential channel is reformulated configurationally, or shown path-independent over a quasi-static protocol. |
| **Asleep-cell momentum drop** | holon-mesh-2 | **Engine-side non-conservation, not an accounting gap** — a projectile contact against an asleep cell applies no force, so momentum is dropped rather than delivered. 1.3e-4 J of the sandbox's 1.34e-2; 8.3e5 J of the landscape's 6.4e7. Not separably sized — it overlaps the damping channel. **The most serious engine-side item left.** |
| **D-ledger chart-relativity** | unassigned | Energy conservation is **chart-relative**. The COSMIC tier carries an expansion background — no time-translation symmetry, so total vacuum energy grows with volume (predicted and observed). The balance gate must **declare its inapplicability** there rather than pass or fail. State the static-curved case with its argument: a static metric has a timelike Killing vector, so conserved energy exists there. *A gate that cannot hold should refuse, not report.* |
| **Projectile contact potential** absent from `E(t)` | holon-mesh-2 | Accounting gap, named and sized. |
| **Q8 REG_GAPS row** | research-manager-2 | Files at closeout, after the four-outcome adjudication. |
| **Q10 §9 probes** | research-manager-2 | Waits on the grid and §0's canonical-form verdict. |
| **.gitignore evidence exemption** | unassigned | See §6. Force-adds done; the negation pattern is owed. |
| **K2 second qualified judge** | unassigned | *Firming a fired kill, not re-running one.* After Q9. |
| **`h3ere2-eval` build in CI** | — | Gate 14 exists and passes; the crate builds again as of `db6b4b7`. |

---

## 4. Q10 — NOT FROZEN, and what it waits on

`Q10_PREREG.md` is published for attack and **deliberately unfrozen**. A1–A9 discharged
(`962f954`); M1–M6 **AUTHORED, not recovered** (`7ee1ef7`) — the originals were message-only
and unrecoverable, and a reconstruction presented as recovery would have been the
phantom-citation defect committed one paragraph after naming it.

**Two real blockers, neither an edit:** §9's two-solve probes are unrun, and §0's branch is
undischarged. **Both wait on physics** — the canonical-form verdict and the q8 grid — **not
on the lane.**

Standing design constraints already ruled: the **spectrum floor is the PRIMARY fence**, not a
fallback (it is a production-ledger quantity, which `Habit.lean` licenses; an entropy-ratio
fence drifts toward the error-bar reading the prereg forbids); warm-start is **subspace
expansion, not zero-padding** — a zero-padded bond is rank-deficient by construction and
would reproduce the disease; the product claim is *the engine refuses to quote when motion is
uninformative*, and **discarded weight may be reported as production, never as error**
(`error_not_computable_from_motion`).

**Q8's own state:** the sweep kill is FIRED; the four-outcome table is committed at
`3123000` *before* any reading; N=8 U=16 classified **(a) oscillation** and adjudicated
**VOID, not KILLED** — a config that did not converge cannot testify about correctness
(`Posed.adjudicate_void_iff`). **(d), if it ever fires, escalates.** The chi ladder is
machine-checkable via `Stagnation.not_optimal_of_regression` — chi=16 *and* chi=32 both
converge and both beat 64/128/256, two witnesses, and the transfer needs G3-primary's floor
(`worst_margin = −1.526e-11`) to put every rung above the exact energy.

---

## 5. THE K2 RECORD AS IT NOW STANDS

**The fired kill is unchanged**: C over B 0.531, p = 0.7754 — and it now additionally
**passes** the §5 length guard.

**The secondary is restated and softened.** The quotable line is **"C is worse, or at best no
better, and costs ~40% more tokens and wall time"** — *not* the unqualified 0.303. A second
judge reversed it in sign; the reversal is a **length artifact**, established with the
protocol's own §5 logistic guard — **which `analyze.py` had never implemented, so the
conjunction the protocol specified had never been run for ANY judge, the primary included.**
Signs are genuinely opposite (second judge's arm coefficients all positive, primary's
negative), so it is real tension rather than underpowered corroboration — but the second
judge's *length* coefficients are roughly double the primary's, and the primary shows **no**
length preference at all. Real in sign, weak in magnitude.

**Calibration 3 is implemented and GATING** (`3406079`) — `require_calib3` fails **closed**;
11/11 gate checks including both direction mutations. **It would now refuse the second
judge.** **THE RECORD STANDS**: a gate built from a finding does not retroactively invalidate
the finding that produced it (§6). Also: `RESULTS_K2.md`'s gold C-vs-B line **is**
length-confounded and may not be quoted clean.

**Reproducibility: the generator was recoverable and the rebuild is PROVEN byte-identical** —
60/60 records across three arms and ten scramble draws (`db6b4b7`, `verify_repro.py`).

---

## 6. RULES ESTABLISHED TODAY, each with the instance that paid for it

1. **A one-directional check reported as though it established both directions.** Four
   instances: content-adjacency taken as authorship; a truncated log read as absence (three
   variants, incl. a pipeline's `$?` measuring `head` rather than the command); `(deleted)`
   on `/proc/<pid>/exe` read as *stale* rather than *replaced*; checking what DECLARES a
   module without checking what CALLS it. **Enforcement is a question asked BEFORE reporting:
   *what would this command NOT catch?***
2. **A check that cannot distinguish two causes is a DETECTOR, not a verdict.** Name the
   discriminator and run it before you kill, discard, or report.
3. **A cross-reference is a warrant only if its target exists** — three claims rested on
   documents never written. **Message-only content is not record**, and four lane deaths
   destroyed exactly that.
4. **A gate built from a finding does not retroactively invalidate the finding that produced
   it.** The warrant for the improvement lives in the data you would be deleting —
   `repairable_does_not_factor` in the campaign coordinate. **A record is a HISTORY, not a
   current-best-state.**
5. **A pathspec commit protects the INDEX, not a SHARED FILE.** It takes the working-tree
   copy. **Diff a shared file before committing it** — you are committing what is in the
   tree, not what you wrote. And **verify a repair from a detached worktree, never a dirty
   one.**
6. **Gates self-verifying, not self-describing**; a gate whose scope lives in prose is a gate
   whose scope drifts. **Keep mechanical gates that look redundant** — the artifact gate had
   six true positives today, two of which no human was looking for.
7. **A CI suite is done when main is green, the gates can fail, and the artifact matches its
   source.** Refinement of a working gate script is the cheapest place to spend attention and
   the easiest to mistake for progress.
8. **One ledger per quantity** — dissipated energy and produced entropy are two quantities.
   Broken hours after adoption by citing injectivity (an *information* property) as a warrant
   about *energy*; an injective map can create joules freely.
9. **An allowlist entry is legitimate only when the break has an OWNER and an EXIT.** Without
   both it is suppression.
10. **The failure is invisibility, not absence of enforcement.** A gitignored file appears in
    `git status` as neither modified nor untracked, so a lane sees a clean tree and correctly
    concludes its work is committed. **Fix the mechanism, not the behaviour.**

**The pre-commit hook (`214ee90`) has now refused a bare commit from both team-lead and the
integrator.** It works on its authors.

---

## 7. STATE AT SHUTDOWN

`origin/main` — see the final commit reported in the shutdown message. Gate suite green
(28 checks) at the last full run. **The viewer wasm must be rebuilt at the FINAL tip before
any push whenever `ciris-sim-core` or `holon-sandbox` changed** — it statically embeds them,
and this fired twice today. **Re-verify last, do not rebuild mid-stack.**

Four lanes died on session limits (holon-cracktip, route-gauge-kill, h3ere2-verdict,
holon-curvature) and three more hit limits mid-evening; **all orphaned diffs were verified
and rescued** rather than left in the tree. Disk hit 0 bytes once and was recovered by
deleting build caches *inside* worktrees — **never delete a worktree to reclaim space; it is
authored work with a cache's file signature.**
