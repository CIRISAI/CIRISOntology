# Gatecraft — the registry of gates

**Gatecraft** is the craft of building, validating and maintaining the gates through which a
reading becomes a claim. `epistemology.md` states the rules; this document is about the
*instruments that enforce them*, which are themselves instruments and get no exemption from
the discipline applied to everything else here.

The working name is "gatecraft." It is Eric's to change.

A gate is not a virtue. It is a detector with a false-positive rate, a false-negative rate,
a domain outside which it says nothing, and a maintenance cost. A gate that has never been
shown to catch anything is a hypothesis about a gate. The machine-readable form of that
position is `CIRISOntology/Core/Epistemics.lean`, where `GateSpec` refuses to construct a
gate that does not carry its family, its provenance, its two anchors, its power certificate
and its domain — the same way `Claim` refuses to construct a claim with no kill.

**What this registry is evidence of.** It states what the repository's record shows as of
2026-07-26. An empty cell means *absent from the record*, which may mean the check was never
built or merely never filed. Where the difference is known, it is said; where it is not, the
cell reads NONE-YET rather than guessing in either direction.

---

## The four design rules

**1. A gate is a typed object with anchors, power and domain.** Six fields, none optional:

| field | what it is | why it is mandatory |
|---|---|---|
| `family` | the failure mode it catches | a gate that cannot name its family cannot be placed in the matrix, so its coverage cannot be counted |
| `provenance` | the incident that discovered or validated it, with commits | a gate with no incident is a guess about how we fail |
| `knownBad` | **the gate's own kill** — the stored case it MUST catch | if it passes its known-bad, the gate is dead. This is the whole of gatecraft in one field |
| `knownGood` | the case it must pass | without it, a false alarm has nothing to be diagnosed against |
| `power` | what planted signal it has been *shown* to detect | a null reading from an uncalibrated detector is not an all-clear |
| `domain` | where it stops being valid | gates overclaim scope by default; the alphabet boundary is the standing example |

Where no stored case exists, the field reads the honest literal `NONE-YET (recorded gap)`.
A visible hole beats a fabricated anchor, and it beats silence, which reads as coverage.

**2. Coverage is a matrix, not a pile.** Gates are counted by *failure family × instrument
class*, never by how many there are. A fourth gate on a family that already has three buys
nothing; the first gate on an uncovered family buys everything. Counting gates instead of
cells is how a battery comes to feel thorough while leaving whole rows open — and that is
exactly the state this repository is in (see the empty cells below).

**3. Lifecycle, with the trust economics stated.** *A gate that cries wolf gets switched
off* — this is written in `epistemology.md` §5 as an observation, and it is a **rent
statement**. A gate rents its authority from the people who have to act on its alarms, and
it pays that rent with precision. A gate whose false-fire rate exceeds what its catches are
worth is in arrears, and it will be defaulted on — quietly, by being ignored, which is worse
than retiring it loudly. The lifecycle below exists to make that default visible.

**4. The axiological layer is explicit and contestable.** What counts as a failure worth
gating, and how a false alarm trades against a missed artifact, are *value choices*. They
are stated in their own section below, marked as choices, and cross-referenced to
`axiomology.md`. They are not smuggled in as technical necessities.

---

## Philology: three ancestors

The pattern is old, and naming its ancestors is not decoration — each one contributes a
piece the others lack.

**Docimasia** (δοκιμασία), Athens, classical period. Before an official could take up an
office he had drawn or been elected to, he was examined — before the Boule or a court — on
whether he was qualified to hold it at all: citizenship, obligations discharged, treatment
of parents, and the rest. It was a **pre-deployment audit**, not a performance review. The
official was examined *before* he held office, and separately from any allegation that he
had failed in it. Applied here: a gate is examined before it is trusted, on the question
*could this thing do the job at all*, and that examination is not the same event as noticing
it missed something later. Every `power` field in this registry is a docimasia, and the ones
that read UNVERIFIED are officials who took office unexamined.

**Basanos** (βάσανος), the touchstone. A dark fine-grained stone against which gold is
streaked; the streak is compared to streaks made by needles of *known* alloy. The lesson is
the one the `knownGood`/`knownBad` fields carry: **you cannot assay a sample without a
reference**. The word's later Athenian legal sense — evidence extracted from slaves under
torture, treated as more reliable than free testimony — is worth naming rather than eliding,
because it is the same word for a test that had lost its reference: a procedure that
produced confident, worthless output, and was believed *because* it was a procedure.

**The Trial of the Pyx**, Royal Mint, since roughly 1282 — about 750 years in continuous
operation, which makes it the longest-running gate battery anyone has run. Coins are drawn
at random *during* production and sealed into the pyx (a boxwood chest). At trial they are
assayed against **trial plates** of known-good standard, by the Company of Goldsmiths, before
an independent jury, presided over by the King's Remembrancer, with the verdict delivered
months later. Four properties, all of them gatecraft:

- **random sampling during production**, not a hand-picked exhibit at the end;
- **a known-good reference** — the plates are the basanos, institutionalised;
- **an independent assayer and jury** — the body that mints is not the body that judges;
- **a tolerance fixed in advance** — the "remedy" is pre-registered, so a marginal result
  cannot be argued into compliance after the fact.

The institutional pairing is **mint and assay**, held apart on purpose. This repository now
has mint theorems of its own — one application of a code's repair map to pure noise mints
exactly that code's whole-only share (`repair_mints_from_noise`, `parityRepair_pays_one_bit`
in `Core/Creation.lean`) — so the pairing is a real mirror and not a pun. We mint; the gates
assay. The Pyx's answer to "who checks the mint" is *not the mint*, and the corresponding
weakness in our arrangement is that here they are the same people. The compensating
mechanism is the fourth axiological commitment below: disagreements are settled against
cases where the truth is known, not by whoever is senior.

---

## The coverage matrix

Rows are failure families. **Polarity** says which direction the alarm points — which is a
real, recorded failure mode in its own right (9180c6a). **Enforcement** says machine or
human, matching `Gate.mechanized`; a gate implemented in an analysis script but not in CI is
*human*, because nothing fails a build when it is skipped.

Commit hashes are this repository's history unless noted.

### 1. Estimator bias — a finite-sample floor read as signal

| | |
|---|---|
| **gate** | shuffle/permutation floor, computed and subtracted before any reading is believed. Lean: `biasControl` |
| **polarity** | fires HIGH — alarm when the shuffled floor reaches the claimed effect |
| **known-bad** | b6527a8 — a shot-noise-only run reading **130% of the deliverable** |
| **known-good** | 03cee87 — the sign-symmetric column, whose true share is **exactly zero** (1b40fc4, machine-checked). Held live; not pinned as a fixed regression case |
| **power** | PARTIAL — validated at the 130% scale. No planted-amplitude sweep, so the smallest signal it can see through its own floor is unmeasured |
| **enforcement** | human |
| **provenance** | b6527a8, 2161bee |

### 2. Boundary / static nonlinearity — clip vs fold

| | |
|---|---|
| **gate** | run every reading under both boundary conventions; a reading that moves is transduced by the boundary, not by the coupling |
| **polarity** | differential — fires on DISAGREEMENT between conventions; needs no null |
| **known-bad** | 30718a8 — the adversary-channel bench demo collapses **259×** under a fold boundary. The readout runs through the kernel clamp |
| **known-good** | NONE-YET (recorded gap) — no reading is stored as certified boundary-stable under both conventions |
| **power** | VERIFIED at 259×, which is unmissable. UNVERIFIED at small differentials, where it matters more |
| **enforcement** | human |
| **provenance** | 30718a8 (a correction on a live *measured* claim); the ARRAY_CAP compliance results |

### 3. Mixture / manufacture — a null that cannot produce the data's structure

| | |
|---|---|
| **gate** | mixture null: the null must be able to *manufacture* the data's generative structure, or it tests nothing. Lean: `nullTypeMatch` |
| **polarity** | fires HIGH — alarm when the null reproduces the effect |
| **known-bad** | 9630d81 — the ECA order-3 spike: survives an iid null, collapses **1886×** under a mixture null |
| **known-good** | the parity state (`share_parity`) — one bit of whole-only share that no pair-preserving null can manufacture |
| **power** | VERIFIED for the mixture family (1886×) and for autocorrelation (phase randomisation, after iid nulls false-fired at +42σ). UNVERIFIED for non-stationary and heavy-tailed structure |
| **enforcement** | human |
| **provenance** | 9630d81; 00bcd4e and 4f3092d (P5 retracted — a no-dynamics mixture beat the noise peak by up to 3.3×) |

### 4. Pair-pinning — a "whole-only" reading fixed by the pair marginals

| | |
|---|---|
| **gate** | LP / pair-maxent certificate: solve for the range of the whole-only quantity consistent with the observed pair marginals. If the range collapses to a point, the reading is pair-determined and is not whole-only |
| **polarity** | fires on a COLLAPSED feasible set — voids the whole-only reading without touching the number itself |
| **known-bad** | 3026a68 — κ = 0.16 resolved: the b=2 median split is pinned by the fine-grained pair marginals; 70535d4 — the array headline re-scoped a third time on the same finding |
| **known-good** | the parity state: uniform pair marginals, a wide feasible range, and a share of exactly one bit that survives the certificate |
| **power** | VERIFIED — it caught a live headline and forced a re-scoping. UNVERIFIED near degeneracy, where the LP is ill-conditioned |
| **enforcement** | human, with a machine-checked companion (`shareK_le_of_pair_uniform`) |
| **provenance** | 3026a68, 70535d4 |

### 5. Coarse-graining / binarization minting — the bins mint the structure

| | |
|---|---|
| **gate** | binmint: vary the binarization (b, threshold, edges) and show the reading is not created by the coarse-graining. The κ-edge instrument is the general-b form, with a two-sided pair-maxent certificate |
| **polarity** | fires on b-dependence the underlying quantity cannot have |
| **known-bad** | 958bb6d — the habit lifespan read as 2 because the tail had been binarized away. The true value was 8 |
| **known-good** | NONE-YET (recorded gap) — no b-stable reading is stored as the must-pass reference |
| **power** | PARTIAL — it caught a 4× lifespan error. No planted bin-artifact sweep |
| **enforcement** | human |
| **provenance** | 72694f7 (retraction: the κ-edge control IS constructible, declared before it was run), 4a1caaa, 958bb6d |

### 6. Geometric artifact — including a tight error bar on the wrong quantity

| | |
|---|---|
| **gate** | post-pipeline sanity: an error bar too tight for the quantity is the tell. Lean: `residualNeverSupport` |
| **polarity** | fires on IMPLAUSIBLE PRECISION — the alarm is triggered by the result being *too good*, which is the opposite of where attention goes by default |
| **known-bad** | c348c02 — Stage 2 withdrawn: the first production run measured survey geometry at **σ = 176** |
| **known-good** | NONE-YET (recorded gap) — no confirmed advance prediction is stored, so this gate has never been shown to let a real result *through* |
| **power** | UNVERIFIED as an automated check. c348c02 was caught by a human noticing the error bar, not by a gate |
| **enforcement** | human |
| **provenance** | c348c02; 2df2748 (headline magnitude withdrawn — 19 of the 20 largest readings outside the bridge's validity regime); f6515b2 (two artifact gates promoted) |

### 7. Dose-vs-rate / run-length — the statistic tracks a nuisance, not the driver

| | |
|---|---|
| **gate** | dose-vs-rate adjudication: does the effect scale with the claimed driver, or with total exposure / run length / sample size? |
| **polarity** | fires when the effect tracks the nuisance dose |
| **known-bad** | 7454647 — gravity's excess scales with D and the GAP does not, so the deliverable statistic was not measuring gravity; 9630d81 — the dose-vs-rate leg of the same adjudication that killed the ECA spike |
| **known-good** | NONE-YET (recorded gap) |
| **power** | PARTIAL — it has fired correctly twice, both times on real headlines. No planted dose-confound has been run past it |
| **enforcement** | human |
| **provenance** | 00bcd4e (staked in advance, so it *could* retract P5), 9630d81, 7454647 |

### 8. Probe polarity — the gate points the wrong way

| | |
|---|---|
| **gate** | polarity declaration: state, before the run, which direction of the diagnostic means PASS. The instance is the mask-sensitivity check (Gate B) |
| **polarity** | this row *is* the polarity question; the gate fires when the declared direction and the implemented direction disagree |
| **known-bad** | c348c02's withdrawn run — the corrected Gate B fires on it, and the uncorrected one did not |
| **known-good** | NONE-YET (recorded gap) — no clean run is stored as the case the corrected gate must leave alone |
| **power** | VERIFIED in one direction against one stored case (9180c6a) |
| **enforcement** | human |
| **provenance** | 9180c6a — "Gate B had its polarity inverted; corrected with the reasoning on the record", corrected against c348c02 |

### 9. Sampling / shot noise — the valve

| | |
|---|---|
| **gate** | shot-noise floor: what the estimator reads under sampling noise alone, at the *actual* shot count of the run |
| **polarity** | fires HIGH — alarm when the shot-noise-only floor reaches the deliverable |
| **known-bad** | b6527a8 — shot noise minting **130% of the deliverable**, with the pre-registered null revealed as a power failure |
| **known-good** | analytic only: `valve_from_nothing` — a product state in, whole-only share exactly zero out. No *data* case is stored (recorded gap) |
| **power** | VERIFIED at 130% |
| **enforcement** | human, with machine-checked companions in `Core/Valve.lean` |
| **provenance** | 2161bee (the pump is the asymmetry, and the alphabet boundary is stated), b6527a8 |

### 10. Textual / use-position — a check matching the word, not the use

| | |
|---|---|
| **gate** | CI layer 1: match `:= sorry`, `by sorry`, a sorry-only line — use positions, never the bare word |
| **polarity** | fires on a match; the failure mode is *false*-firing, on prose that describes the rule |
| **known-bad** | all four invocation forms, each still caught after the fix |
| **known-good** | a843840 — this repository's own documentation, which contains the keyword in every file and must NOT fire. The gate failed exactly this case before the fix |
| **power** | VERIFIED in both directions at a843840, and re-run on every build |
| **enforcement** | **machine** (CI layer 1). The semantic backstop is `assert_no_sorry` in the audit — Lean gate `noSorry` |
| **provenance** | a843840 — "Fix the gate that cried wolf on its own documentation" |

### 11. Occupancy / sparsity — ties and empty cells read as structure

| | |
|---|---|
| **gate** | occupancy floor: a minimum count per cell before an estimator may be read at all, declared in advance. Companion: tied-fraction disclosure. Lean: `tiedFractionDisclosed` |
| **polarity** | fires LOW — below the floor the reading is **VOID**, which is neither zero nor positive |
| **known-bad** | 8b0c108 — the b=16 advance exclusion, which fired correctly on occupancy grounds *before* the run; 95d1b3c — IPF is unsafe on sparse data; the untrained-model control that fires on tied activations alone |
| **known-good** | the configurations retained at Stage 0 (8b0c108), which the same gate passed |
| **power** | PARTIAL — it fired correctly in advance once. No planted-sparsity sweep, so the fraction at which it is *obliged* to alarm is unset |
| **enforcement** | human, pre-registered |
| **provenance** | a340eda (pre-registration), 8b0c108, 95d1b3c |

### 12. Solver / relaxation gap — the certificate is one-sided

| | |
|---|---|
| **gate** | two-sided dual certificate: bracket the quantity between a primal solution and a dual bound rather than reporting a single fitted solution |
| **polarity** | fires when the bracket is wide, or when the fitted solution sits outside it |
| **known-bad** | the IPF drift: on near-deterministic states, iterative proportional fitting *one-sidedly overstates* the share — 9.8e-6 against a true 1.2e-10, roughly five orders of magnitude, always in the same direction |
| **known-good** | the exact 1-D k=3 solver, whose answer the certificate must bracket |
| **power** | VERIFIED at five orders of magnitude on near-deterministic states. UNVERIFIED in the interior, where the drift is smaller and the temptation to use IPF is higher |
| **enforcement** | human |
| **provenance** | 95d1b3c (the IPF lesson), 4a1caaa (the two-sided pair-maxent certificate) |

### 13. Power of the control itself — the meta-gate

| | |
|---|---|
| **gate** | power certificate: every control must be shown to detect a *planted* signal of the size that matters before its null reading is allowed to mean anything |
| **polarity** | fires when the control FAILS to detect the plant. The null reading is then UNINTERPRETABLE — not an all-clear, not a refutation |
| **known-bad** | 0885182 — the doped control failed W3, and the doping was the wrong probe (POWER-2); a586449 — K-VOID fired on our own solver; b611a5b — a gate that certified the bridge along the wrong axis |
| **known-good** | cad514e — the forecast machinery, where all gates passed *and* caught four real bugs: a battery that is simultaneously clean and demonstrably live |
| **power** | this is the gate that issues power certificates, and it does not hold one. It has fired on our own probe (VERIFIED, once, in the direction that hurt us). As a general scheme, UNVERIFIED |
| **enforcement** | human |
| **provenance** | 0885182, a586449, b611a5b |

---

## The empty cells, stated as findings

The matrix above has thirteen rows. The finding is not in the rows; it is in what the rows
do not reach.

**A. The Lean enumeration covers four families out of thirteen.** `Gate.all` carries the
claim-level epistemic rules — pre-registration, kills staked first, separable kills,
null-type match, tied-fraction disclosure, bias control, residual-never-support, report the
kill, floor-is-not-absence, no-sorry, axiom audit. Of the instrument families above, only
**mixture/manufacture** (`nullTypeMatch`), **estimator bias** (`biasControl`),
**occupancy/sparsity** (`tiedFractionDisclosed`) and **geometric artifact**
(`residualNeverSupport`) have a counterpart in the type. Boundary, pair-pinning,
coarse-graining, dose-vs-rate, probe polarity, shot noise and solver gap have **no typed
gate at all** — they live in analysis scripts and in this document. That is the largest
single gap and it is structural: what is not in `Gate` is not on the published page, and
what is not on the page is not something a reader can hold us to.

**B. Only two families are machine-enforced, and both are about proofs, not readings.**
Textual/use-position and artifact-vs-description (the axiom audit) fail a build. Every gate
that stands between a *measurement* and a *claim* is upheld by a person. This is honest —
`Gate.mechanized` says so, and the audit fails if that stops being true — but it means the
mechanization figure on the published page should not be read as coverage of the measurement
pipeline. It is coverage of the proof pipeline, which is a different and much easier problem.

**C. Six of the thirteen power certificates read PARTIAL or UNVERIFIED, including the
meta-gate that is supposed to issue them.** Estimator bias, coarse-graining, geometric
artifact, dose-vs-rate, occupancy, and power-of-the-control. Of the seven that lead with
VERIFIED, five state their own unverified region (boundary at small differentials, mixture
for non-stationary structure, pair-pinning near degeneracy, probe polarity in the untested
direction, solver gap in the interior).

Sharper, and worse: **only three gates have been validated against a constructed case whose
answer was known in advance** — the textual gate (four planted invocation forms, a843840),
the solver-gap bracket (near-deterministic states with an exactly computable share), and the
estimator-bias floor's known-good (the sign-symmetric column, exactly zero by 1b40fc4).
Every other VERIFIED reading in this registry means *the gate fired on one real incident*.
That is evidence it is not inert. It is not a power certificate, and it cannot be turned into
a false-negative rate, so this registry cannot say what the battery is missing — only that
the answer is not zero.

**D. Six of thirteen families have no stored known-good.** Boundary, coarse-graining,
geometric artifact, dose-vs-rate, probe polarity, and shot noise (data case). A gate with a
known-bad and no known-good can be made arbitrarily sensitive at no visible cost — the
pressure is all in one direction, and nothing in the record would show it tightening until
it started crying wolf and got switched off. This is the failure mode of rule 3.

**E. By instrument class.** Naming the classes this repository actually reads:

- **Lean proof artifacts** — two families, both machine-enforced. The other eleven do not
  apply, and their absence here is correct rather than a gap.
- **Synthetic discrete sources** (ECA, Ising, spin models) — the best-covered class: mixture
  null, dose-vs-rate, occupancy, solver gap, and the exact sign-symmetry anchor (1b40fc4,
  03cee87), which is the only place in the repository where a gate's known-good is *proved*
  rather than assumed.
- **Real hardware** (CIRISArray, QPU) — has the boundary gate (30718a8) and cap compliance
  (124/124 readings within `ShareK.lean`'s cap). Has **no mixture null** and **no validated
  shot-noise floor for the phase-metric readout** in the record. Given that the readout is
  clamp-mediated, the boundary gate carries this class almost alone.
- **Neural / LLM activations** — has the tied-activation control (which fires) and the
  cross-architecture comparison. Has **no boundary gate** and **no mixture null** in the
  record.
- **Neuroimaging timeseries** (fMRI) — has the phase-randomisation null, and that null's
  power certificate is explicitly **insufficient**: a clip artifact survives IAAFT at z = 86.
  This class is currently gated by an instrument known to pass at least one artifact.
- **Survey / sky pipeline** — the richest gate battery built this week (pre-registration with
  mocks-only eyes, unblinding criteria, occupancy exclusion, mask-sensitivity polarity,
  post-pipeline sanity) and also the class that produced the σ = 176 withdrawal. Both facts
  belong in the same sentence: the battery was built, and it still took a human to notice
  the error bar.
- **Cosmological fits** (the dark-energy ledger) — **no gate of any family in the record.**
  Those claims were killed by parameter-free budget arguments and a normalisation check, not
  by any reusable instrument gate. A kill is not a gate: it fired once, on one claim, and
  left nothing behind that a future fit would have to pass.

---

## The axiological layer

**These are value choices, not results.** They decide what a gate is *for*, and a different
set would produce a different battery from the same evidence. They are stated here so they
can be argued with. The determination procedure is `axiomology.md`; the cross-references
below are to its sections.

**(1) Instrument honesty is prior to verdict preference.** VOID and UNINTERPRETABLE are
first-class outcomes, reported as loudly as a detection. A run that cannot be read is
*information about the instrument*, and suppressing it in favour of a readable-but-wrong
number is the one failure this whole apparatus exists to prevent. Precedent on the record:
K-VOID fired on our own solver (a586449) and was published; run 1 VOIDed on readout (4ec64b2)
and was re-registered on measured calibration rather than quietly re-run.
*Cross-reference:* `axiomology.md` §3 (values fixed by refusal) and §6 (the metric is
reported with its own limitations attached). **Contestable:** a reviewer could hold that
VOID-heavy reporting is unreadable, and that filtering to interpretable runs serves readers
better. We take the opposite side, and the cost is a noisier record.

**(2) Asymmetric loss, bounded by the wolf constraint.** A missed artifact is worse than a
false alarm — a false alarm costs a day, a missed artifact costs a published claim and the
credibility of everything filed beside it. So gates are set to fire. **But** the asymmetry is
bounded, and the bound is the rent statement in design rule 3: alarms may be raised only by
gates that hold a current power certificate. An uncalibrated gate that fires often is not
being cautious; it is spending trust it never earned, and it will be switched off exactly
when it is needed. *Cross-reference:* `axiomology.md` §2 (evaluate at the weakest point — a
battery is worth what its weakest gate is worth) and §6 (when a metric and the goal diverge,
the metric is replaced, not defended). **Contestable:** the exchange rate between a false
alarm and a missed artifact is asserted, not measured. We have no false-fire rate for any
gate in this registry, which means the bound in rule 3 is currently unenforceable.

**(3) Separability.** A firing gate invalidates the **minimum necessary** — the reading, or
the run, or the claim, but never the surrounding programme by association. Precedent:
5789f7e, where the run-2 simulator gate was filed separately and run 1's reading was
restored; 30718a8, where a boundary correction landed on one live measured claim and did not
propagate. This is the same commitment as separable kills in `epistemology.md` §2, applied
to gates instead of claims, and it cuts against the natural instinct after a bad catch,
which is to distrust everything nearby. *Cross-reference:* `axiomology.md` §7. **Contestable:**
a reviewer could argue that a gate firing on one run is evidence about the whole pipeline,
and that minimum-necessary invalidation systematically under-reacts. That is a real risk and
we accept it deliberately, because the alternative destroys the record's ability to say
which specific thing was wrong.

**(4) Adjudicability over authority.** Disagreements about a gate are settled against cases
where the truth is known — the known-good, the planted signal, the machine-checked anchor —
and never by seniority or by who proposed the gate. The case on the record is 9180c6a: a
reviewer's own gate had its polarity inverted, the disagreement was resolved against the
withdrawn run c348c02 where the right answer was known, and **the reviewer's gate was the
one that was wrong**. The correction is in the history with its reasoning, which is the point
— an adjudication that is not written down is indistinguishable from a concession to rank.
This is also the compensating mechanism for the structural weakness named in the Pyx section
above: mint and assay are the same people here, so the only available substitute for
institutional separation is that every dispute has to terminate in a case with a known
answer. *Cross-reference:* `axiomology.md` §5 (deferral to properly licensed authority is
first-class) and §4 (values as a symmetry — the rule that binds the reviewer binds the
reviewed). **Contestable:** it is slow, and it is unavailable exactly when no case with a
known answer exists — which, per finding D above, is six families out of thirteen.

---

## Lifecycle

A gate moves through five states, and the transitions are events on the record, not moods.

**Proposed.** A failure family is named and an incident is attached. A proposal with no
incident is a guess about how we fail; it may still be right, but it is filed as a
hypothesis about a gate, not as a gate.

**Validated.** Anchors and power are supplied: a stored known-bad the gate catches, a stored
known-good it passes, and a planted signal at a stated size that it has been shown to detect.
This is the docimasia, and it is the transition this repository most often skips — seven of
thirteen rows above are sitting in *proposed* while being used as though validated.

**Deployed.** In the pipeline, with `mechanized` flagged honestly. CI or a human, stated,
with no rounding up: a gate that lives in an analysis script is human-enforced, because
nothing fails when someone forgets to run it.

**Monitored.** The false-fire rate is tracked, because it is the rent. Every false alarm
spends trust drawn from the people who have to act on it, and a gate in arrears gets
defaulted on silently — ignored rather than retired, which leaves the coverage matrix
claiming a cell that is no longer real. **We do not currently monitor any gate's false-fire
rate.** That is a gap in this lifecycle, not a step we have completed.

**Corrected or retired, with reasoning on the record.** A gate that fails its own known-bad
is dead and is marked dead, exactly as a dead claim is (`epistemology.md` §7). A gate that
was wrong and is fixed keeps its history: 9180c6a corrected Gate B's polarity *with the
reasoning attached*, and a843840 corrected the textual gate rather than the prose it had
falsely accused — matching the artifact to its documentation, never the reverse. A retired
gate stays in the registry, marked retired, because the failure family it was aimed at does
not retire with it.
