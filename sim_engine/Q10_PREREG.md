# Q10 PREREG — the three-legged certificate at scale, and the refusal it exists to make

**STATUS: DRAFT AGAINST A BRANCH POINT. NOT FROZEN.** The hard prerequisite in §0 is
unresolved, and §1's scope is a function of how it resolves. Nothing in this file is staked
until §0 is discharged and the file is re-committed as FROZEN. Published now for attack, per
freeze-design-early.

**Author: research-manager-2. Commissioned by team-lead through chief-of-staff-2, 2026-08-24.**

---

## 0. THE HARD PREREQUISITE, AND THE BRANCH

**Q10 cannot be pre-registered on an engine that is *proved* not to report its own manifold's
optimum.** `Core/Stagnation.lean`'s `not_optimal_of_regression` convicts the `chi=256` run at
N=8, U=16 on **two** witnesses — `chi=16` (`δE = 3.411e-5`, converged) and `chi=32`
(`δE = 8.595e-7`, converged) both beat it, and every MPS manifold embeds in every larger one.
The conviction is of the RUN, not of any mechanism. Three mechanisms remain live and none is
supported: rank-deficiency / loss of canonical form, initial-state trapping, and plain
non-convergence.

**The discriminator, named and not yet run:** same configuration, same `chi`, **different
initial state**, through `dmrg::run_from` (which already takes caller-supplied tensors).
Trapping moves or vanishes; conditioning persists. **It must not route through `pad_to_chi`** —
zero-padding manufactures the rank-deficient bonds the conditioning branch blames, and would
confound the contrast it is meant to settle. Team-lead's conditioning instruments
(`‖A†A − I‖` per bond, `⟨ψ|ψ⟩`, per-bond smallest singular value) characterise whichever
branch survives; the initial-state arm is what separates them.

**THE BRANCH, staked now so neither outcome is a surprise:**

- **BRANCH A — the defect is confirmed and fixed.** Q10 proceeds at its full scope (§1A).
- **BRANCH B — canonical form is NOT the cause.** **Q10's scope shrinks to the validated `chi`
  range, and this prereg says so in those words.** Not a smaller claim dressed as the same
  claim: the deliverable is explicitly bounded, and the bound is reported in the headline.

**VALIDATED CHI RANGE — a derived ruler, not a chosen number.** The maximal contiguous range,
starting from the smallest `chi` on the ladder, over which `E(chi)` is non-increasing. This is
`not_optimal_of_regression` used as an acceptance test rather than as a post-hoc conviction:
the first rung that regresses ends the range, and everything above it is out of scope by
theorem rather than by preference. **It is computed before any Q10 gate runs.**

---

## 1. SCOPE

**1A (Branch A).** `N ~ 100`, or the largest `N` at which the *fixed* engine validates against
`q-seam` at `N ≤ 12` — whichever is smaller. The validation ladder is unchanged from Q8: the
exact reference exists only where `q-seam` reaches, and correctness-against-truth extends only
as far as truth extends.

**1B (Branch B).** The same `N`, restricted to the validated `chi` range of §0. If that range
excludes the `chi` needed to represent the state at `N ~ 100`, **Q10's honest deliverable is
the refusal itself**, and that is a result, not a failure — see §2.

**Family.** The 1D Hubbard chain of `Q_SEAM_PREREG.md` §1, half filling, `Sz = 0`, `t = 1`,
open boundaries. **Same family as Q8 deliberately**: this campaign is about the certificate at
scale, not about a new physics family, and changing both at once would make a null
uninterpretable.

---

## 2. THE PRODUCT CLAIM, STAKED IN THESE WORDS

> **The engine refuses to quote when motion is uninformative.**

That is the deliverable. Not "the engine is accurate at N~100" — which it cannot demonstrate,
because no exact reference exists there — and not "the engine quotes its own error", which
**`Core/Stagnation.lean`'s `error_not_computable_from_motion` forbids**: distance-to-truth does
not factor through the process's own motion ledger.

**A certificate of MOTION is not a certificate of ERROR.** Q10 may report where the engine
declines to answer and why; it may not convert a motion or truncation quantity into an error
bar. **G4's retraction (`Q8_MPS_PREREG.md` A4.2) is the measured face of that theorem** and is
cited, not re-derived.

---

## 3. THE THREE LEGS

### 3a. THE FENCE — a wrongness meter computable without a reference

`Q_SEAM_RESULTS.md`'s lesson: `D_bool`, the chart's own cap-not-Boolean fence, tracked chart
failure where the beyond-pair share did not. Q10's analogue must be **chart-internal**, since
at `N ~ 100` there is nothing to compare against.

**STAKED: the fence is bond-entropy saturation, `S_max / ln(chi)`**, where `S_max` is the
largest von-Neumann entropy over the chain's bonds. It reads 0 for a product state and → 1 as
a bond exhausts the representational budget the ledger declares. **It is not an error estimate
and is never reported as one** (§2); it is the chart's declaration of how close it is to its
own limit.

**Threshold: STAKED at `S_max / ln(chi) ≥ 0.9` ⇒ the fence is UP.** Chosen, not derived, and
declared as chosen.

### 3b. THEOREM-PINNED ANCHORS — DERIVED FOR THE FAMILY, NEVER ASSUMED

Four, each with its warrant named and each holding at every `N` including where no reference
exists:

| anchor | value | warrant |
|---|---|---|
| particle–hole | `⟨n_jσ⟩ = 1/2` per spin-orbital | `Q_SEAM_PREREG.md` §1.1(iii) — **per spin-orbital, not per site**; the per-site total is 1 |
| magnetization | `m_i = 0` | spin-independence of `H` + ground-state uniqueness in the `Sz = 0` sector (`Q7_SEAM_PREREG.md` §2.2) — **not Lieb**, whose heavier hypotheses this family does not need |
| sector lock | `⟨Ŝz⟩ = 0` **and** `⟨(Ŝz)²⟩ = 0` | A1's pin, and it **earned its keep on first contact**: at N=8, U=16 `⟨Ŝz⟩ = 3.2e-3` would have read as noise while `⟨Ŝz²⟩ = 1.9e-2` convicted, 99.95% of it variance |
| particle number | `⟨N̂⟩ = N` | construction; drift is unshifted with the **integer** `N_target` (§2 of Q8), never the measured value |

**BINDING: if Q10's family is ever changed, every anchor is RE-DERIVED for the new family
before use.** An anchor carried across a family change without re-derivation is an assumption
wearing a theorem's clothes.

### 3c. THE MOTION CERTIFICATE

Two clauses, both refusals:

1. **Across `chi`** — `E(chi)` non-monotone ⇒ **REFUSE**, as the instance of
   `not_optimal_of_regression`. The witness point is realized by the warm start (§4), which is
   what makes the manifold inclusion concrete rather than abstract.
2. **Within a run** — `E(sweep)` non-monotone beyond slack ⇒ **REFUSE**. Q8's G3-primary, as a
   refusal rather than a gate.

---

## 4. WARM START IS SUBSPACE EXPANSION, AND IT IS ONE MECHANISM

**Zero-padding is banned as the growth rule.** A zero-padded bond is rank-deficient by
construction and, on the leading hypothesis, is the disease in a syringe. Growth is by
**subspace expansion** (Hubig, McCulloch, Schollwöck, Wolf — density-matrix / environment-drawn
expansion): new bond directions come from `H` applied to the current state, projected
orthogonally to what is already there, so they are non-null and physically relevant.

**Warm-start and perturbation are ONE mechanism, not two arms** — the expansion IS where the
perturbation enters. **Mutation-tested by removal:** an arm with expansion disabled must be
shown to behave *worse*, or the mechanism is not what is doing the work.

---

## 5. WHAT MAY BE REPORTED, AND AS WHAT

**Discarded weight is a PRODUCTION ledger, never an error.** `Core/Habit.lean`: a chart whose
induced rate map is injective has zero production (`production_eq_zero_iff_rate_injective`,
`production_id_eq_zero_of_injective`), and unitary evolution is injective — so a truncating
quantum simulation's production lives **entirely** in its truncation. Reporting accumulated
discarded weight as *production* is exact and honest. Reporting it as *error* is forbidden by
§2's theorem and was measured false by G4.

---

## 6. GATES

| gate | statement | STAKED threshold |
|---|---|---|
| **H0** validated-`chi` ruler | `E(chi)` non-increasing over the reported range | exact, by theorem |
| **H1** correctness vs `q-seam` | at every `N ≤ 12` in range: energy, density, double-occupancy | Q8's G2 bands, unchanged |
| **H2** anchors | all four of §3b, at **every** `N` including `N ~ 100` | `≤ 1e-6` each |
| **H3** fence separates | the fence must take both values across the sweep | ≥ 3 configs up, ≥ 3 down |
| **H4** refusal fires and discriminates | mutation-tested: `Typed` refuses, `Silent` does not, same numerics | joint, both halves |
| **H5** speed | total wall-clock | §7 |

---

## 7. SPEED IS A STAKED GATE

**STAKED: total wall-clock, on the grid sized by the cost probe, ≤ 4× the probe's
extrapolation.** The probe is run **before** the grid is fixed, and the grid is sized from it —
not the reverse.

**Scheduling is serialized by default** (Q8 Amendment 2's binding rule), and the environment is
probed with one timing under load before any launch. **The two-solve rule applies to every
staked contrast, compute cost included: both arms in ONE run, in ONE environment.** This is not
a formality — a load-average-23 measurement of this campaign's own gate was disowned on
2026-08-24 for exactly this defect, by its author.

---

## 8. THE KILLS — separable, each taking down its own claim

> **K1 CORRECTNESS.** Fires if H1 fails at any validated `N`. Fatal to the deliverable; no
> `N ~ 100` number may be reported. STOP.

> **K2 FENCE.** Fires if H3 fails — the fence reads the same everywhere, or never moves. Kills
> the fence leg only: the anchors and the refusal are untouched. **A fence that never fences is
> decoration**, and this is the clause that says so in advance.

> **K3 ANCHOR.** Fires if any anchor of §3b fails where the reference says the state is right,
> **or** if no anchor ever fires anywhere across the sweep. The first is unsoundness, the second
> is uselessness, and they are reported as different findings.

> **K4 REFUSAL.** Fires if H4's joint condition fails. Kills the refusal feature only; energies
> may still be reported, flagged that undetected non-optimality is unmitigated.

> **K5 SPEED.** Fires if H5 fails. A scheduling and sizing result, not a correctness one.

None implies another. All are reported in the results file's title line, as loudly as a
survival.

---

## 9. TWO-SOLVE PROBES REQUIRED BEFORE FREEZE

Every staked contrast gets a two-point probe **before** this file is frozen. Non-negotiable,
and the reason is Q7: *"the physics varies along this axis" does NOT imply "the error varies
along it."* Q7 VOIDed at its family gate because nobody measured the spread first.

1. **The fence must be shown to VARY** across the intended sweep — H3's precondition, measured,
   not hoped. If it does not vary, the family does not pose the question and Q10 is
   **VOID-not-killed**.
2. **The anchors must be shown to be violable** — at least one configuration where an anchor
   fires. An anchor that cannot fail on this family proves nothing here.
3. **Cost**: both arms of every timed contrast, one run, one environment (§7).
4. **The §0 discriminator** — different initial state, not through `pad_to_chi`.

---

## 10. CARRIED FORWARD

Misfit fixes M1–M6 carry over from Q9's brief unchanged. Q8's Amendment 2 scheduling rule,
Amendment 3's VOID-configs-are-diagnostic ruling, and Amendment 4's declaration discipline for
in-code filters all bind here. **Every filter, floor, or exclusion applied to any Q10 fit is
declared IN THIS FILE before it is written in code** — A4's defect, not repeated.

## 11. CREDITS

DMRG — White 1992. MPS formulation and sweep/SVD machinery — Schollwöck 2011. Subspace
expansion — Hubig, McCulloch, Schollwöck & Wolf. Area laws — Hastings 2007. Jordan–Wigner 1928.
The Hubbard exact solution — Lieb & Wu 1968. **This programme's own**: the ledger reading of
bond dimension; the refusal discipline of `GrainFloor.lean` applied to a new resource; the
motion certificate as an instance of `not_optimal_of_regression`; and the production reading of
discarded weight via `Core/Habit.lean`.

## 12. FILES AND DETACHED COMPUTE

Prereg: this file. Crate: `sim_engine/crates/q8-mps` (extended, not forked). Every run over the
house-rule wall-clock line gets `setsid` + done-marker + `RESUME.md`, and **every detached
launch asserts its binary's provenance at launch time** (`/proc/<pid>/exe` against the build's
mtime — a launch-time assertion, which is where that check is sound; mid-run it is a detector,
not a verdict).
