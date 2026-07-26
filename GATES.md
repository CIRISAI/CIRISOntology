# Gatecraft — the Weirbook

**Gatecraft** is the craft of building, validating and maintaining the gates through which a
reading becomes a claim. `epistemology.md` states the rules; this document is about the
*instruments that enforce them*, which are themselves instruments and get no exemption from
the discipline applied to everything else here.

The gates are **water gates** — weirs, sluices, fords and locks — not city gates and not
logic gates. Nothing here is a wall. Knowledge is water moving through works that somebody
has to maintain, and every structure in this registry exists to gauge that flow, slow it,
divert it, or let it cross safely. The working name is "gatecraft." It is Eric's to change.

A gate is not a virtue. It is a structure with a false-positive rate, a depth beyond which it
reads nothing, and a maintenance cost that somebody pays. A gate that has never been shown to
catch anything is a hypothesis about a gate. The machine-readable form of that position is
`CIRISOntology/Core/Epistemics.lean`, where `GateSpec` refuses to construct a gate that does
not carry its family, its headwaters, its two references, its dye test and its depth — the
same way `Claim` refuses to construct a claim with no kill.

**What this registry is evidence of.** It states what the repository's record shows as of
2026-07-26. An empty cell means *absent from the record*, which may mean the check was never
built or merely never filed. Where the difference is known, it is said; where it is not, the
cell reads NONE-YET rather than guessing in either direction.

---

## The working vocabulary

The Lean field names are neutral and code-stable. The registry's prose uses the older water
words, which say the same things with the right register. Both columns name one object.

| in the Lean | in the Weirbook | what it is |
|---|---|---|
| `family` | **the reach** it guards | the stretch of failure this gate is responsible for |
| `provenance` | **headwaters** | where this gate rose — the incident that cut its channel, with commits |
| `knownGood` | **the plumb line** | the known-true reference a reading is judged against |
| `knownBad` | **the kept taint** | the stored bad case the gate must catch. **This is the gate's own kill** |
| `power` | **the dye test** | put dye in upstream; verify it appears downstream. A gate that cannot see the dye cannot see anything, and its verdicts are void |
| `domain` | **depth** | how deep it reads. Past that, it is **out of its depth**, and the idiom means exactly what it says |

Three kinds of structure, and the difference matters when reading the matrix:

- a **weir** *measures*. In hydrometry a weir is literally an instrument: its geometry
  converts a flow into a height you can read off a staff. Our certificate gates — the LP
  pair-maxent bracket, the IPF-versus-dual comparison, the shuffle floor — are weirs. They
  return a number, and the number is the reading.
- a **sluice** *controls*. It passes or it blocks; it does not tell you how much. The
  occupancy floor and the polarity declaration are sluices.
- a **ford** is a **validated crossing** — a place where it has been established that you can
  get from one side to the other. A bridge between two instruments is a ford only after
  somebody has walked it at depth.
- a **lock** raises a reading between levels, one chamber at a time, and its defining
  discipline is that **both gates are never open at once**. That is what promoting a claim
  from wager to measured to proved is supposed to look like.

**The verdict language.** A reading is **put through the weirs**. It either **runs clear** or
it does not. A reading a gate has caught is **fouled**. A reading taken where no gate with a
current dye test was standing is **ungauged** — hydrology's own word for a catchment with no
station on it, and exactly our VOID: not zero, not a detection, not an all-clear. Ungauged is
a first-class outcome and is reported as loudly as a detection.

A modern water laboratory practices this same craft under duller names, and a practitioner
should read the two columns as one: the plumb line is a method blank, the dye test is a
matrix spike and its recovery, depth is the method detection limit, headwaters is chain of
custody, and a sample measured after its holding time has measured its own decay rather than
its source.

---

## The four design rules

**1. A gate is a typed object with its references, its dye test and its depth.** Six fields,
none optional. Where no stored case exists, the field reads the honest literal
`NONE-YET (recorded gap)`. A visible hole beats a fabricated reference, and it beats silence,
which reads as coverage.

**2. Coverage is a matrix, not a pile.** Gates are counted by *reach × instrument class*,
never by how many there are. A fourth weir on a reach that already has three buys nothing;
the first gate on an ungauged reach buys everything. Counting gates instead of cells is how a
battery comes to feel thorough while whole reaches run unwatched — and that is exactly the
state this repository is in (see the empty cells below).

**3. Lifecycle, with the trust economics stated.** *A gate that cries wolf gets switched
off* — this is written in `epistemology.md` §5 as an observation, and it is a **rent
statement**. A gate rents its standing from the people who have to act on its alarms, and it
pays that rent in precision. A gate whose false-fire rate exceeds what its catches are worth
is in arrears, and it will be defaulted on quietly, by being ignored, which is worse than
being torn out loudly.

There is a governance ancestor for this and it is not a metaphor. Magna Carta 1215, clause
33: *all fish-weirs shall be removed from the Thames, the Medway, and throughout all England,
except on the sea coast.* A weir that served its owner while blocking the common flow was old
enough to be a constitutional grievance in 1215. Manorial court rolls are full of the smaller
version — presentments against millers whose weirs stood too high and whose dams drowned a
neighbour's meadow. Those mill-and-weir records are the ancestor ledgers this registry is
named after, and the standing question they ask is the right one: **does this structure serve
the flow, or the person who built it?**

**4. The axiological layer is explicit and contestable.** What counts as a failure worth
gating, and how a false alarm trades against a missed artifact, are *value choices*. They are
stated in their own section below, marked as choices, and cross-referenced to
`axiomology.md`. They are not smuggled in as technical necessities.

---

## The ancestors

**Docimasia** (δοκιμασία), Athens, classical period. Before an official could take up an
office he had drawn or been elected to, he was examined — before the Boule or a court — on
whether he was qualified to hold it at all. It was a **pre-deployment examination**, not a
performance review: the official was examined *before* he held office, and separately from
any later allegation that he had failed in it. Applied here, and applied to agents as much as
to instruments: a gate is examined before it is trusted, on the question *could this thing do
the job at all*, and that examination is not the same event as noticing later that it missed
something. Every dye test in this registry is a docimasia, and the ones that read UNVERIFIED
are officials who took office unexamined.

**The plumb line**, Amos 7:7-8 — the Lord stands on a wall built with a plumb line, with a
plumb line in his hand, and sets it in the midst of the people. The point of the image is
that the wall is not judged against opinion about the wall; it is judged against a reference
that does not care. Note the root: *plumbum* is lead, which gives us both the plumb line and
**plumbing** — the reference and the waterworks come from the same word, and the plumb line
was always a water-worker's tool. Every `knownGood` in this registry is a plumb line, and the
six reaches that have none are walls we are currently judging by eye.

(The gold assay has a famous battery of its own, and we are not borrowing it. Gold is prized
for being inert.)

---

## The coverage matrix

Rows are reaches — failure families. **Polarity** says which direction the alarm points,
which is a real recorded failure mode in its own right (9180c6a). **Enforcement** says machine
or human, matching `Gate.mechanized`; a gate implemented in an analysis script but not in CI
is *human*, because nothing fails a build when it is skipped.

Commit hashes are this repository's history unless noted.

### 1. Estimator bias — a finite-sample floor read as signal

| | |
|---|---|
| **gate** | a **weir**: the shuffle/permutation floor, computed and subtracted before any reading is believed. Lean: `biasControl` |
| **polarity** | fires HIGH — alarm when the shuffled floor reaches the claimed effect |
| **kept taint** | b6527a8 — a shot-noise-only run reading **130% of the deliverable** |
| **plumb line** | 03cee87 — the sign-symmetric column, whose true share is **exactly zero** (1b40fc4, machine-checked). This is our one true plumb line: a known-clean sample sent through the identical pipeline, where the right answer is not estimated but proved. Held live; not pinned as a fixed regression case |
| **dye test** | PARTIAL — validated at the 130% scale. No planted-amplitude sweep, so the smallest dye it can still see through its own floor is unmeasured |
| **enforcement** | human |
| **headwaters** | b6527a8, 2161bee |

### 2. Boundary / static nonlinearity — clip vs fold

| | |
|---|---|
| **gate** | a **weir**: run every reading under both boundary conventions and read the difference |
| **polarity** | differential — fires on DISAGREEMENT between conventions; needs no null |
| **kept taint** | 30718a8 — the adversary-channel bench demo collapses **259×** under a fold boundary. The readout runs through the kernel clamp, so the boundary is transducing the coupling |
| **plumb line** | NONE-YET (recorded gap) — no reading is stored as certified boundary-stable under both conventions |
| **dye test** | VERIFIED at 259×, which is unmissable. UNVERIFIED at small differentials, where it matters more |
| **enforcement** | human |
| **headwaters** | 30718a8 (a correction on a live *measured* claim); the ARRAY_CAP compliance results |

### 3. Mixture / manufacture — a null that cannot produce the data's structure

| | |
|---|---|
| **gate** | a **weir**: the mixture null must be able to *manufacture* the data's generative structure, or it gauges nothing. Lean: `nullTypeMatch` |
| **polarity** | fires HIGH — alarm when the null reproduces the effect |
| **kept taint** | 9630d81 — the ECA order-3 spike: survives an iid null, collapses **1886×** under a mixture null |
| **plumb line** | the parity state (`share_parity`) — one bit of whole-only share that no pair-preserving null can manufacture |
| **dye test** | VERIFIED for the mixture family (1886×) and for autocorrelation (phase randomisation, after iid nulls false-fired at +42σ). UNVERIFIED for non-stationary and heavy-tailed structure |
| **enforcement** | human |
| **headwaters** | 9630d81; 00bcd4e and 4f3092d (P5 retracted — a no-dynamics mixture beat the noise peak by up to 3.3×) |

### 4. Pair-pinning — a "whole-only" reading fixed by the pair marginals

| | |
|---|---|
| **gate** | a **weir**, and the clearest one we have: the LP / pair-maxent certificate solves for the range of the whole-only quantity consistent with the observed pair marginals. If the range collapses to a point, the reading is pair-determined and is not whole-only |
| **polarity** | fires on a COLLAPSED feasible set — fouls the whole-only reading without touching the number itself |
| **kept taint** | 3026a68 — κ = 0.16 resolved: the b=2 median split is pinned by the fine-grained pair marginals; 70535d4 — the array headline re-scoped a third time on the same finding |
| **plumb line** | the parity state: uniform pair marginals, a wide feasible range, and a share of exactly one bit that survives the certificate |
| **dye test** | VERIFIED — it caught a live headline and forced a re-scoping. UNVERIFIED near degeneracy, where the LP is ill-conditioned |
| **enforcement** | human, with a machine-checked companion (`shareK_le_of_pair_uniform`) |
| **headwaters** | 3026a68, 70535d4 |

### 5. Coarse-graining / binarization minting — the bins mint the structure

| | |
|---|---|
| **gate** | a **weir**: vary the binarization (b, threshold, edges) and show the reading is not created by the coarse-graining. The κ-edge instrument is the general-b form, with a two-sided pair-maxent certificate |
| **polarity** | fires on b-dependence the underlying quantity cannot have |
| **kept taint** | 958bb6d — the habit lifespan read as 2 because the tail had been binarized away. The true value was 8 |
| **plumb line** | NONE-YET (recorded gap) — no b-stable reading is stored as the must-pass reference |
| **dye test** | PARTIAL — it caught a 4× lifespan error. No planted bin-artifact sweep |
| **enforcement** | human |
| **headwaters** | 72694f7 (retraction: the κ-edge control IS constructible, declared before it was run), 4a1caaa, 958bb6d |

### 6. Geometric artifact — including a tight error bar on the wrong quantity

| | |
|---|---|
| **gate** | a **sluice**: post-pipeline sanity. An error bar too tight for the quantity is the tell. Lean: `residualNeverSupport` |
| **polarity** | fires on IMPLAUSIBLE PRECISION — the alarm is triggered by the result being *too good*, which is the opposite of where attention goes by default |
| **kept taint** | c348c02 — Stage 2 withdrawn: the first production run measured survey geometry at **σ = 176** |
| **plumb line** | NONE-YET (recorded gap) — no confirmed advance prediction is stored, so this gate has never been shown to let a real result *through* |
| **dye test** | UNVERIFIED as an automated check. c348c02 was caught by a human noticing the error bar, not by a gate |
| **enforcement** | human |
| **headwaters** | c348c02; 2df2748 (headline magnitude withdrawn — 19 of the 20 largest readings outside the bridge's validity regime); f6515b2 (two artifact gates promoted) |

### 7. Dose-vs-rate / run-length — the statistic tracks a nuisance, not the driver

| | |
|---|---|
| **gate** | a **weir**: does the effect scale with the claimed driver, or with total exposure, run length, sample size? The water-lab form of this reach is the holding-time violation — **a sample measured too late measures its own decay, not its source** |
| **polarity** | fires when the effect tracks the nuisance dose |
| **kept taint** | 7454647 — gravity's excess scales with D and the GAP does not, so the deliverable statistic was not measuring gravity; 9630d81 — the dose-vs-rate leg of the same adjudication that killed the ECA spike |
| **plumb line** | NONE-YET (recorded gap) |
| **dye test** | PARTIAL — it has fired correctly twice, both times on real headlines. No planted dose-confound has been put through it |
| **enforcement** | human |
| **headwaters** | 00bcd4e (staked in advance, so it *could* retract P5), 9630d81, 7454647 |

### 8. Probe polarity — the gate points the wrong way

| | |
|---|---|
| **gate** | a **sluice**: declare, before the run, which direction of the diagnostic means PASS. The instance is the mask-sensitivity check (Gate B) |
| **polarity** | this row *is* the polarity question; the gate fires when the declared direction and the implemented direction disagree |
| **kept taint** | c348c02's withdrawn run — the corrected Gate B fires on it, and the uncorrected one did not |
| **plumb line** | NONE-YET (recorded gap) — no clean run is stored as the case the corrected gate must leave alone |
| **dye test** | VERIFIED in one direction against one stored case (9180c6a) |
| **enforcement** | human |
| **headwaters** | 9180c6a — "Gate B had its polarity inverted; corrected with the reasoning on the record", corrected against c348c02 |

### 9. Sampling / shot noise — the valve

| | |
|---|---|
| **gate** | a **weir**: what the estimator reads under sampling noise alone, at the *actual* shot count of the run |
| **polarity** | fires HIGH — alarm when the shot-noise-only floor reaches the deliverable |
| **kept taint** | b6527a8 — shot noise minting **130% of the deliverable**, with the pre-registered null revealed as having no dye test at all |
| **plumb line** | analytic only: `valve_from_nothing` — a product state in, whole-only share exactly zero out. No *data* case is stored (recorded gap) |
| **dye test** | VERIFIED at 130% |
| **enforcement** | human, with machine-checked companions in `Core/Valve.lean` |
| **headwaters** | 2161bee (the pump is the asymmetry, and the alphabet boundary is stated), b6527a8 |

### 10. Textual / use-position — a check matching the word, not the use

| | |
|---|---|
| **gate** | a **sluice**: CI layer 1 matches `:= sorry`, `by sorry`, a sorry-only line — use positions, never the bare word |
| **polarity** | fires on a match; the failure mode is *false*-firing, on prose that describes the rule |
| **kept taint** | all four invocation forms, each still caught after the fix |
| **plumb line** | a843840 — this repository's own documentation, which contains the keyword in every file and must NOT fire. The gate failed exactly this case before the fix |
| **dye test** | VERIFIED in both directions at a843840, and re-run on every build. The only gate here whose dye was deliberately put in rather than encountered |
| **enforcement** | **machine** (CI layer 1). The semantic backstop is `assert_no_sorry` in the audit — Lean gate `noSorry` |
| **headwaters** | a843840 — "Fix the gate that cried wolf on its own documentation" |

### 11. Occupancy / sparsity — ties and empty cells read as structure

| | |
|---|---|
| **gate** | a **sluice**: a minimum count per cell before an estimator may be read at all, declared in advance. This reach is **depth** stated as a rule — *a reading below the validated detection limit is not a detection*, which covers occupancy and the floor gates in one phrase. Companion: tied-fraction disclosure. Lean: `tiedFractionDisclosed` |
| **polarity** | fires LOW — below the floor the reading is **ungauged**, which is neither zero nor positive |
| **kept taint** | 8b0c108 — the b=16 advance exclusion, which fired correctly on occupancy grounds *before* the run; 95d1b3c — IPF is unsafe on sparse data; the untrained-model control that fires on tied activations alone |
| **plumb line** | the configurations retained at Stage 0 (8b0c108), which the same gate passed |
| **dye test** | PARTIAL — it fired correctly in advance once. No planted-sparsity sweep, so the fraction at which it is *obliged* to alarm is unset |
| **enforcement** | human, pre-registered |
| **headwaters** | a340eda (pre-registration), 8b0c108, 95d1b3c |

### 12. Solver / relaxation gap — the certificate is one-sided

| | |
|---|---|
| **gate** | a **weir**, and a two-sided one: bracket the quantity between a primal solution and a dual bound rather than reporting a single fitted solution. This is the split-sample discipline — the same water read at two weirs, and they must agree |
| **polarity** | fires when the bracket is wide, or when the fitted solution sits outside it |
| **kept taint** | the IPF drift: on near-deterministic states, iterative proportional fitting *one-sidedly overstates* the share — 9.8e-6 against a true 1.2e-10, roughly five orders of magnitude, always in the same direction |
| **plumb line** | the exact 1-D k=3 solver, whose answer the bracket must contain |
| **dye test** | VERIFIED at five orders of magnitude on near-deterministic states. UNVERIFIED in the interior, where the drift is smaller and the temptation to use IPF is higher |
| **enforcement** | human |
| **headwaters** | 95d1b3c (the IPF lesson), 4a1caaa (the two-sided pair-maxent certificate) |

### 13. Power of the control itself — the dye test applied to the weirs

| | |
|---|---|
| **gate** | not a weir; the **dye test itself**, turned on the battery. Every control must be shown to detect a *planted* signal of the size that matters before its null reading is allowed to mean anything |
| **polarity** | fires when the control FAILS to see the dye. The null reading is then **ungauged** — not an all-clear, not a refutation |
| **kept taint** | 0885182 — the doped control failed W3, and the doping was the wrong probe (POWER-2, a dye test that came back invisible); a586449 — K-VOID fired on our own solver; b611a5b — a gate that certified the bridge along the wrong axis |
| **plumb line** | cad514e — the forecast machinery, where all gates passed *and* caught four real bugs: a battery simultaneously clean and demonstrably live |
| **dye test** | this is the structure that issues dye tests, and it does not hold one. It has fired on our own probe (VERIFIED, once, in the direction that hurt us). As a general scheme, UNVERIFIED |
| **enforcement** | human |
| **headwaters** | 0885182, a586449, b611a5b |

---

## The empty cells, stated as findings

The matrix above has thirteen reaches. The finding is not in the rows; it is in what the rows
do not reach.

**A. The Lean enumeration covers four reaches out of thirteen.** `Gate.all` carries the
claim-level epistemic rules. Of the instrument reaches above, only **mixture/manufacture**
(`nullTypeMatch`), **estimator bias** (`biasControl`), **occupancy/sparsity**
(`tiedFractionDisclosed`) and **geometric artifact** (`residualNeverSupport`) have a
counterpart in the type. Boundary, pair-pinning, coarse-graining, dose-vs-rate, probe
polarity, shot noise and solver gap have **no typed gate at all** — they live in analysis
scripts and in this document. That is the largest single gap and it is structural: what is not
in `Gate` is not on the published page, and what is not on the page is not something a reader
can hold us to.

**B. Only two reaches are machine-enforced, and both are about proofs, not readings.**
Textual/use-position and artifact-vs-description (the axiom audit) fail a build. Every gate
standing between a *measurement* and a *claim* is upheld by a person. This is honest —
`Gate.mechanized` says so, and the audit fails if that stops being true — but it means the
mechanization figure on the published page should not be read as coverage of the measurement
works. It is coverage of the proof works, which is a different and much easier problem.

**C. Six of the thirteen dye tests read PARTIAL or UNVERIFIED, including the one that is
supposed to issue them.** Estimator bias, coarse-graining, geometric artifact, dose-vs-rate,
occupancy, and power-of-the-control. Of the seven that lead with VERIFIED, five state their
own unverified region (boundary at small differentials, mixture for non-stationary structure,
pair-pinning near degeneracy, probe polarity in the untested direction, solver gap in the
interior).

Sharper, and worse: **only three gates have ever seen dye that was deliberately put in** —
the textual gate (four planted invocation forms, a843840), the solver-gap bracket
(near-deterministic states with an exactly computable share), and the estimator-bias floor's
plumb line (the sign-symmetric column, exactly zero by 1b40fc4). Every other VERIFIED in this
registry means *the gate fired on one real incident*. That is evidence the structure is not
inert. It is not a dye test, it cannot be turned into a false-negative rate, and so this
registry cannot say what the battery is missing — only that the answer is not zero.

**D. Six of thirteen reaches have no plumb line.** Boundary, coarse-graining, geometric
artifact, dose-vs-rate, probe polarity, and shot noise (data case). A gate with a kept taint
and no plumb line can be made arbitrarily sensitive at no visible cost — the pressure is all
in one direction, and nothing in the record would show it tightening until it started crying
wolf and got switched off. That is the failure mode of design rule 3, and it is how a weir
ends up serving its builder.

**E. By instrument class.** Naming the classes this repository actually reads:

- **Lean proof artifacts** — two reaches, both machine-enforced. The other eleven do not
  apply, and their absence here is correct rather than a gap.
- **Synthetic discrete sources** (ECA, Ising, spin models) — the best-gauged class: mixture
  null, dose-vs-rate, occupancy, solver gap, and the sign-symmetry anchor (1b40fc4, 03cee87),
  which is the only place in the repository where a gate's plumb line is *proved* rather than
  assumed.
- **Real hardware** (CIRISArray, QPU) — has the boundary weir (30718a8) and cap compliance
  (124/124 readings within `ShareK.lean`'s cap). Has **no mixture null** and **no validated
  shot-noise floor for the phase-metric readout** in the record. Given that the readout is
  clamp-mediated, the boundary weir carries this class almost alone.
- **Neural / LLM activations** — has the tied-activation control (which fires) and the
  cross-architecture comparison. Has **no boundary gate** and **no mixture null** in the
  record.
- **Neuroimaging timeseries** (fMRI) — has the phase-randomisation null, and that null's dye
  test is explicitly **insufficient**: a clip artifact survives IAAFT at z = 86. This class is
  currently gauged by a weir known to pass at least one taint.
- **Survey / sky pipeline** — the richest battery built this week (pre-registration with
  mocks-only eyes, unblinding criteria, occupancy exclusion, mask-sensitivity polarity,
  post-pipeline sanity) and also the class that produced the σ = 176 withdrawal. Both facts
  belong in the same sentence: the works were built, and it still took a human to notice the
  error bar.
- **Cosmological fits** (the dark-energy ledger) — **no gate of any reach in the record.**
  Those claims were killed by parameter-free budget arguments and a normalisation check, not
  by any reusable structure. A kill is not a weir: it fired once, on one claim, and left
  nothing standing in the channel that a future fit would have to pass.

---

## The axiological layer

**These are value choices, not results.** They decide what a gate is *for*, and a different
set would produce a different battery from the same evidence. They are stated here so they can
be argued with. The determination procedure is `axiomology.md`; the cross-references below are
to its sections.

The stock-and-flow commitment underneath all four is old: *they have forsaken the fountain of
living waters, and hewed them out cisterns — broken cisterns, that can hold no water*
(Jeremiah 2:13). A hoarded stock leaks; the flow lives. What this registry certifies is not an
inventory of results held in a vessel, it is a channel that has to be maintained, and the
maintenance is the value rather than an overhead on it. That is the same rent clause the
repository proves on the model, applied to its own instruments.

**(1) Instrument honesty is prior to verdict preference.** **Ungauged** is a first-class
outcome, reported as loudly as a detection. A run that cannot be read is *information about
the works*, and suppressing it in favour of a readable-but-wrong number is the one failure
this whole apparatus exists to prevent. Precedent on the record: K-VOID fired on our own
solver (a586449) and was published; run 1 came back ungauged on readout (4ec64b2) and was
re-registered on measured calibration rather than quietly re-run. *Cross-reference:*
`axiomology.md` §3 (values fixed by refusal) and §6 (the metric is reported with its own
limitations attached). **Contestable:** a reviewer could hold that an ungauged-heavy record is
unreadable, and that filtering to interpretable runs serves readers better. We take the
opposite side, and the cost is a noisier record.

**(2) Asymmetric loss, bounded by the wolf constraint.** A missed taint is worse than a false
alarm — a false alarm costs a day, a missed taint costs a published claim and the credibility
of everything filed beside it. So gates are set to fire. **But** the asymmetry is bounded, and
the bound is the rent statement in design rule 3: alarms may be raised only by gates holding a
current dye test. An unvalidated gate that fires often is not being cautious; it is spending
standing it never earned, and it will be torn out exactly when it is needed.
*Cross-reference:* `axiomology.md` §2 (evaluate at the weakest point — a battery is worth what
its weakest gate is worth) and §6 (when a metric and the goal diverge, the metric is replaced,
not defended). **Contestable:** the exchange rate between a false alarm and a missed taint is
asserted, not measured. We have no false-fire rate for any gate in this registry, which means
the bound in rule 3 is currently unenforceable.

**(3) Separability.** A firing gate fouls the **minimum necessary** — the reading, or the run,
or the claim, but never the whole catchment by association. Precedent: 5789f7e, where the
run-2 simulator gate was filed separately and run 1's reading was restored; 30718a8, where a
boundary correction landed on one live measured claim and did not propagate. This is the same
commitment as separable kills in `epistemology.md` §2, applied to gates instead of claims, and
it cuts against the natural instinct after a bad catch, which is to distrust everything
downstream. *Cross-reference:* `axiomology.md` §7. **Contestable:** a reviewer could argue that
a gate firing on one run is evidence about the whole pipeline, and that minimum-necessary
fouling systematically under-reacts. That is a real risk and we accept it deliberately,
because the alternative destroys the record's ability to say which specific thing was wrong.

**(4) Adjudicability over authority.** Disagreements about a gate are settled against cases
where the truth is known — the plumb line, the planted dye, the machine-checked anchor — and
never by seniority or by who built the structure. The case on the record is 9180c6a: a
reviewer's own gate had its polarity inverted, the disagreement was resolved against the
withdrawn run c348c02 where the right answer was known, and **the reviewer's gate was the one
that was wrong**. The correction is in the history with its reasoning, which is the point — an
adjudication that is not written down is indistinguishable from a concession to rank. This
also carries a weight it should not have to: in the manorial arrangement the miller who built
the weir and the jury who presented it were different people, and here they are the same
people. Until that is fixed, every dispute terminating in a case with a known answer is the
only available substitute. *Cross-reference:* `axiomology.md` §5 (deferral to properly licensed
authority is first-class) and §4 (values as a symmetry — the rule binding the reviewer binds
the reviewed). **Contestable:** it is slow, and it is unavailable exactly when no case with a
known answer exists — which, per finding D above, is six reaches out of thirteen.

---

## Lifecycle

A gate moves through five states, and the transitions are events on the record, not moods.
A lock is the right image for the whole sequence: a reading rises one chamber at a time, and
both gates are never open at once.

**Proposed.** A reach is named and an incident is attached. A proposal with no incident is a
guess about how we fail; it may still be right, but it is filed as a hypothesis about a gate,
not as a gate.

**Validated.** The plumb line and the dye test are supplied: a stored kept taint the gate
catches, a known-true reference it passes, and a planted signal at a stated size that it has
been shown to see. This is the docimasia, and it is the transition this repository most often
skips. Applying the definition strictly to the matrix above, **only four reaches are actually
validated** — mixture, pair-pinning, textual, and solver gap, each holding both a plumb line
and a dye test that leads with VERIFIED. The other **nine are sitting in *proposed* while
being used as though validated**, six of them missing the plumb line and six the dye test.
That is the state of the works, and it is the reason this document exists.

**Deployed.** Standing in the channel, with `mechanized` flagged honestly. CI or a human,
stated, with no rounding up: a gate that lives in an analysis script is human-enforced,
because nothing fails when someone forgets to run it.

**Monitored.** The false-fire rate is tracked, because it is the rent. Every false alarm
spends standing drawn from the people who have to act on it, and a gate in arrears gets
defaulted on silently — ignored rather than removed, which leaves the matrix claiming a reach
that nothing actually guards. **We do not currently monitor any gate's false-fire rate.** That
is a gap in this lifecycle, not a step we have completed.

**Corrected or torn out, with reasoning on the record.** A gate that fails its own kept taint
is dead and is marked dead, exactly as a dead claim is (`epistemology.md` §7). A gate that was
wrong and is fixed keeps its history: 9180c6a corrected Gate B's polarity *with the reasoning
attached*, and a843840 corrected the textual gate rather than the prose it had falsely accused
— matching the artifact to its documentation, never the reverse. A removed gate stays in the
Weirbook, marked removed, because the reach it was aimed at does not go away with it.
