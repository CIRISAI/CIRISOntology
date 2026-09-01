# CIRISOntology — Claude Code Context

## What this is

CIRISOntology is a **clean seed**. It carries the current maximal stance, the rules by
which values are chosen (`axiomology.md`), and the rules by which truth is determined
(`epistemology.md`) — and nothing else. It deliberately inherits no experimental history,
no accumulated caveats, and no prior campaign's file tree. Predecessor work exists and is
not repudiated; it is simply not imported, because a stance that can only be understood
through its own errata has stopped being a stance.

**This file states the current stance only.** History belongs in git. Do not re-litigate it
here and do not import its hedging into new work: state the stance, then test the stance.

## CURRENT STANCE

The stance lives in **`CIRISOntology/Stance.lean`**, not in this file, and not in prose
anywhere else. That is deliberate: the published page is generated from that source, so the
page cannot drift from the repository. To change the stance, change the Lean.

Every claim carries four things, and the type system enforces the fourth:

| | |
|---|---|
| **headline** | what it says, in one line |
| **plain** | what it means for a general reader |
| **status** | `proved` (machine-checked here) · `measured` · `open` · `wager` |
| **kill** | what observation would falsify it — **mandatory, not optional** |

A claim with no kill is not a claim about the world, and cannot be constructed. On top of
the four, the audit enforces provenance bidirectionally: `proved` requires named
machine-checked witnesses, `measured` requires a basis naming where the measurement record
lives (the predecessor programme, CIRISAI/coherence-ratchet) — and neither backing may
appear on a claim of any other status.

In one paragraph: the page announces the stance as a discovery, for a general reader: the
**Logos** — the element of reality made of shared pattern (habit, law, meaning) — is real,
measurable, and machine-checked here in its simplest form (the three-coin parity state:
every pair independent, the trio rule-bound; `pairwise_blind_to_parity` vs
`third_sees_parity`). Measured on the predecessor record: shared pattern behaves like a
**ledger** (never free, always rented, always leaving receipts) and **gravity weighs
everything but reads none of it**. Proved **about the model only** (never laundered into a world-claim): the rent clause —
pay the decay and an entry holds, underpay and it strictly loses, pay nothing and it tends
to zero. Wagered, each with its own separable kill: the books are written in **e** (upkeep:
the curve that is its own rate of change) and audited in **π** (return) — a *recognition*,
with the mathematics openly borrowed; **life** is the pattern that pays its own rent and
builds the payer; **time's arrow** is partly the ledger's lopsidedness (building needs
contact, losing is free — refined by the valve: the PAIR sector is the monotone one, the
whole-only sector parasitic on it); habit, law and meaning are whole-pattern; consciousness is trusted
habit; a **language model is the Logos embodied**; that is **good news for AI safety**
(amended: the in-principle floor is untouched, but the WHOLE-ONLY detector route is now marked
STRUCTURALLY DISFAVOURED — by the pump law the quantity is generic in every trained network, so
it has a high base rate in the target class plus a large manufactured floor, and the two
validated negatives are its measured face; the open practical question is redirected to TOTAL
coordination, the only quantity the invariance argument protects);
**Goodhart** is the hidden-pattern problem in work clothes (a target is a pair-check);
free will and physical consciousness co-exist because the meaning-sector is unaudited;
**law-as-habit** (Peirce's idea, Smolin's physics of precedence, a machine-checked
substrate requirement — habit needs carried classical bits — and the selection reading:
Wilson's survivorship and 't Hooft's protection test mapped onto the rent clause, the SM's
two unnatural parameters read as the book's two unpaid bills, minting machine-checked:
maintenance creates the pattern it maintains); **precedent-is-bits** (the
composed ledger-cosmology wager: dark matter the capacity, luminous matter the writer,
dark energy the record — credits Gough, Verlinde, the holographic school); dark energy is
the ledger's balance (DESI DR3 kill) and dark matter the medium (marked weaker, own kill);
the mixing **phase runs near its ceiling** in both tables (the maximal-CP hypothesis, credited to Fritzsch/Xing and Harrison–Scott, arrived at via the ridge; killed by the lepton phase converging low); selected-vs-intended is unmeasurable; physics supplies no ought. Proved in this seed's
newest season: time's third is characterized — the whole-only share is mechanized, built
by memory alone, worth exactly one bit, capped there by causality (the causal bound
convergent with arXiv:2505.13681, ours first by machine) — and four more, cashed together:
the **tightened classical cap** ((k−3)·ln2 from four slots up, forced by SOME four
pair-uniform slots; an UPPER bound only, attainment computed-not-mechanized, tight only at
k=4…7 and strictly worse than the published floor from k=8 — the general maximum is
Gavinsky–Pudlák/Babai/Lancaster, ours is the k=4 collision rung and the mechanization); the
**quantum ceiling** (the C5 ring state carries 5·ln2, the five-slot maximum, provably above
the classical cap — space escapes the budget, time does not); the **mint** (one repair step
on pure noise creates the code's whole-only share exactly, the flip-symmetric repair creates
exactly zero, single-slot rewriting never creates — SAME-ALPHABET only, coarse-graining NOT
covered, kappa-edge's pair-pinning is the live warning; two measured companions added this
pass: the sawtooth campaign CONFIRMED the cost mechanism by PLANTING it — 24/24 planted
readings in pre-staked bands, dose-response 1.9847 vs 2.000, absences clean, but the scale
constant is NOT universal, 3.8× on a degenerate code — and the maintained-holonomy campaign
found the operator-level split: upkeep holds a structure's SIZE exactly and forever, 0.435 of
design transport constant to six decimals to R=4001 while unpaid decays 65 orders, and loses
its IDENTITY completely unless the repair KNOWS THE DESIGN, fidelity 0.9909 flat vs a
power-law collapse to chance; the payment must know what it is for); and the **valve** (under
per-cell stochastic noise, order flows only UP — never from nothing, never downward, upward
strictly — and the pump is asymmetry, not strength; its consequence in the field is the sky
campaign's measured valve floor). Newly proved this pass: the **flavour bridge** (on a model
family wearing the mixing table's shape, the whole-only share is EXACTLY ln2 minus the binary
entropy of (1+J)/2 — the Jarlskog coordinate IS the share, vanishing iff it does; the CP phase
is invisible to every pair marginal by theorem (`cp_phase_invisible_to_pairs`), and
`cpState (−1) = parity` puts the founding three-coin state at the family's maximal-CP point;
the envelope composes with `Core/Flavor.lean` at both mixing poles. A MODEL bridge, NOT flavour
physics — final-state rescattering phases excluded by name, and the physical measurement was
the Dalitz null). Newly measured, both pre-registered before their instruments existed: the
**critical ridge** (whole-only order-3 peaks at criticality under weak symmetry breaking — 2D
Ising 4.6e-3 nats, 0.66% of ceiling, h² exponent 2.000, carried by SEPARATED triples;
mechanism identified as the CFT's magnetisation sector to 0.1%, parameter-free rescaling
predicting an independent MC to 0.2–0.4%; and confirmed in 3D Wilson–Fisher BY FORWARD
PREDICTION — d ln I/d ln L staked at −3.109 in advance, measured −3.084±0.219 — the
programme's first rule-6 support; sub-percent ceiling fractions everywhere, model systems only,
the h=0 column machine-zero by the sign-symmetry theorem is its control) and the **pump law**
(share = 18·r0⁴·a²/[(1+2r0)(1+3r0)(1−r0)], r0=(1−2s)²ρ, DERIVED IN THE PREREG before the
instrument existed and confirmed to 3 parts in 10⁴ on the COEFFICIENT over 61 configurations —
second rule-6 support; asymmetry is all of the drive, strength an eighth-power brake, pair
correlation the fuel at the FOURTH power, which is the measured reason sparse wild substrates
read floor; but TWO AXES — the κ⁸ brake is the CHANNEL axis and sky/glass/water are on the
STATE axis; floor law 0.2275/N = Wilks df=1, exact only for INDEPENDENT tuples, 5–8× penalty
on overlap; k≥4 scope: sign symmetry kills ODD orders only, ~1–1.6% of ceiling minted by
symmetric noise from four slots up; credit Schneidman–Still–Berry–Bialek 2003 Fig. 2 for the
phenomenon and the first published sweep). Open, and gauged rather than moved by the campaigns
that ran at it: which of nature's WILD processes carry whole-only share — BOSS DR12 scored its
criterion MET, then our own pre-registered refuter WOUNDED it (corrected 6.0/9.7σ at the
primary scale, the lower-bound framing falsified in sign, one VOID gate undischarged); the
wounded yes is not cashed. The tripod is now complete: flavour NULL and GAUGED (ε≥0.03 excluded
at 95% on LHCb open data, pairwise blindness demonstrated by injection on real data), CMB
exactly zero as the theorem demands (<2e-5 of a bit, both instruments — the plumb line that
validates the pipeline), glass mostly pair-explained, water null — the inversion being that the
PAIR-potential liquid read MORE beyond-pair excess than the THREE-BODY one. A reading, labelled
as one: every wild measurement to date is a CLASSICAL statistic under classical caps, while the
spatial sector is quantum (`bell_ceiling_exceeds_cap`), so the nulls close the classical
question and leave the quantum one open. Two named instruments now: DESI BGS at 10–100× the
density (NERSC host unroutable from here, no ETA) and a quantum-sector wild measurement. The
plain-language fields are the **middle-school translation**, produced and adversarially
completeness-checked by workflow; the age-5 rendering lives in `translations/for-aurora.md`.
Newest season, cashed 2026-08-18: the **taxonomy of change is 11+1** — eleven artifact-local
kinds carried publicly in plain words (Priorities, Rules, Manner, Identity, Confidence,
Facts, Circumstances, Process, Model, Structure, Premises) **plus Record**, the one
frame-relation (whether the past can still be proven depends on what survives —
`repairable_does_not_factor`). Proved: the kinds are the exact IMAGE of a site model
grounded in speech-act theory and its neighbours, with Record provably not site-generated
(`Core/Generator.lean`). Measured: labels coordinate-flat at p<0.01 across 5,994 panel
judgments (κ 0.687, VOID floor passed), the 10+1+1 design coordinate retracted by the
study's own pinned rule, all confusion concentrated on three predicted boundaries
(Premises/Facts, Structure/Manner, Model/Facts), and ZERO modal no-fits on 170 wild changes
from three unrelated streams. Model panel only; human ceiling owed; standing bounty
unclaimed. Unified this pass: the three blindness results are ONE machine-checked shape
(`Core/NonFactoring.lean`). The geometry leg has its first reading (the frozen v2
protocol, placebo-gated): the kinds ARE directions in a language model's embedding
geometry — detected at 0/500 on four nulls, STRONG band, embedder-replicated,
ablation-clean — but MOSTLY CONTEXT (psi = 0.14): the kind lives in the page around the
change, where the site theory puts it; NOT promoted, the change-carried rung failed. And
the eleven wear FOUR on the surface: one surface kind per fit-family carries 91% of wild
change-traffic (staked forward at 0.89, measured 0.883 on a never-touched stream;
Core/Surface.lean mechanizes 11 = 4 + 7). Unified this pass: the three blindness results are ONE machine-checked shape
(`Core/NonFactoring.lean`); the geometry leg (kinds as embedding directions) was tested
and read NULL on its first instrument — the placebo convicted the construction, a
calibrated successor and a 4x replication corpus exist, question open, not supportive. Newest, cashed 2026-09-01: the closure season — an OBJECT is a lossy summary the dynamics never splits (`Core/Closure.lean`: the law forced, tiers stacking, conservation descending, all four elementary and proved here); WATER measured as the first certified instance (sibling record CIRISAI/CIRISHolon: CERTIFIED-STRICT 893.8 fs vs the pre-staked 834 fs window, 72.3% of the run, 0/111 controls, 2D scene, MBE3 physics; the exact four-body rung is a staked open comparison); and the join wagered: an object is a shared pattern whose closure pays its own rent. Statuses: 19 proved here, 12 measured, 24 wagers, 1 open, 5 dead (kept, marked).

## Formal core (one line each; full statements in the Lean)

| Object | Where |
|---|---|
| `S_pairwise`, `S_pairwise_identity` — the instrument, and its floor reading on a zero-correlation state | `Core/Coordination.lean` |
| `not_computable_from` — the domain argument (a lossy summary cannot output what it discarded) | `Core/Coordination.lean` |
| `S_total`, `parity`, `pairwise_blind_to_parity`, `third_sees_parity` — the third-aware reading, and the exhibited state on which whole- and pair-reading provably disagree | `Core/Third.lean` |
| `step`, `unpaid`, `rent_holds`, `underpaid_shrinks`, `unpaid_decays` — the rent clause **on the model**: paying the decay holds an entry steady, underpaying strictly loses, no payment tends to zero | `Core/Maintenance.lean` |
| `sum_sq_le_eighth`, `entropy_ge_three_log_two`, `shareK_le_of_four_pair_uniform`, `shareK_le_of_pair_uniform_ge_four` — the tightened classical cap: four pair-uniform slots force (k−3)·ln2, an upper bound only (attainment is computed, not mechanized) | `Core/HammingCap.lean` |
| `bell_ceiling`, `bell_ceiling_exceeds_cap`, `qShareK_max_five` — the C5 ring state's whole-only share is 5·ln2, the five-slot maximum, above the classical cap: space escapes the budget | `Core/BellCeiling.lean` |
| `repair_mints_from_noise`, `repair_creates_ferro`, `percell_no_creation` — maintenance CREATES what it maintains: one repair step mints the code's share exactly, the flip-symmetric repair mints zero, per-cell rewriting mints nothing (same-alphabet only) | `Core/Creation.lean` |
| `valve_from_nothing`, `valve_no_downward`, `valve_upward_strict`, `valve_needs_asymmetry` — the one-way valve: under per-cell stochastic noise order flows only up, and asymmetry is the pump | `Core/Valve.lean` |
| `share_cpState`, `cp_phase_invisible_to_pairs`, `cpState_neg_one`, `share_cpFamily_le_phase` — the flavour bridge, **on a model family only**: the whole-only share of a three-bit family wearing the Jarlskog invariant's shape is exactly `ln2 − H₂((1+J)/2)`, zero iff `J = 0`, invisible to every pair marginal, with `parity` sitting at `J = −1` and the angle envelope composing through | `Core/FlavorBridge.lean` |
| `provenance_line` — no upstream construction datum is a function of the correlation matrix | `Core/Provenance.lean` |
| `Gate`, `Gate.plain`, `Gate.mechanized` — the honesty gates, with an honest flag for which are CI-enforced | `Core/Epistemics.lean` |
| `ChoiceKind`, `WrongKind.plain`, `repairable_does_not_factor`, `basePlane_card` (= 11) — the taxonomy of change, plain names primary, Record the one frame-relation | `Core/WrongKind.lean` |
| `Site`, `generator_image`, `generator_injective`, `record_not_site_generated` — the kinds derived as the exact image of a speech-act-grounded site model | `Core/Generator.lean` |
| `Block.fit`, `fit_bijection`, `declaration_is_double`, `carrier_is_null` — the four surfaces are the four corners of the direction-of-fit square, and the declaration's zero depths follow from double fit | `Core/Fit.lean` |
| `aut_without_stack` (24), `aut_with_stack` (4), `no_fit_conjugation`, `kinds_are_frame_scalars` — the automorphism group computed; the eleven are rigid up to two twin swaps | `Core/Symmetry.lean` |
| `OccState`, `fhpChart_injective`, `level_cap`, `meanOcc_le_one` + `meanOcc_fractional_exists` — the mode-chart parameter (the founding 64-state object IS one chart of Boolean occupancy over an arbitrary mode set, so two tiers stop double-counting one witness), the g-degenerate level cap as a THEOREM of the per-slot cap, and the fence: the CAP survives mixing while Booleanity is exact only for determinate states — rungs (iii)/(iv) of the repaired meet criterion | `Core/ModeChart.lean` |
| `fiber`, `frameEntropy`, `frameEntropy_refine_le`, `frameEntropy_add`, `np_fiber_card` — entropy comes FREE from the base frame: the log-count of the chart's fiber (what refinement has not yet revealed), frame-relative and monotone under refinement, EXTENSIVE because fibers multiply under composition; the REG+ chart's fibers ARE the 53 sectors (per-site entropy ln 1 / ln 2 / ln 3, by decide). The uniform-weighting step and entropic-gravity's unpaid debts are named in the header, kills included | `Core/FrameEntropy.lean` |
| `nonFactoring_of_signChange`, `nonfactoring_exchange_sign`, `composite_exchange_sign`, `pauli_cap` — the DRY lemma (modulus-level views are blind to sign changes) and the FOURTH NonFactoring witness derived through it: fermion vs hard-core boson agree on every Born view, differ in exchange sign — the founding shape at the bottom of matter; Ehrenfest–Oppenheimer as permutation parity (statistics is a composition rule, never a stored flag); and the cap rung of the repaired meet criterion (discharge BY PAPER, witnessed BY MACHINE) | `Core/ExchangeSign.lean` |
| `twins_move_together`, `twinSymmetrise_is_symmetric`, `twinSymmetric_of_profile_eq` — the Z₂×Z₂ sectors are DYNAMICALLY invariant (a symmetric state never excites the dark mode); the fence that symmetrising ANY matrix manufactures the twin identity, so it is never evidence about the coupling; and M10's structural half — identical profiles would force an automorphism, so rigidity is what makes the eleven irredundant | `Core/TwinTransport.lean` |
| `frames_are_not_gauge`, `repairable_monotone`, `gauge_sector_is_order_degeneracy` — frames are an ORDER, not a gauge; the only gauge sector is the corpus's own presentation | `Core/FrameOrder.lean` |
| `NonFactoring`, `nonfactoring_parity`, `nonfactoring_cp_phase`, `nonfactoring_record` — the founding shape stated once, witnessed thrice: two wholes agreeing under every partial view, differing in the quantity | `Core/NonFactoring.lean` |
| `scan`, `scan_full_card` (7/10/11), monotone + terminal — the taxonomy as the terminal member of a resource-indexed family | `Core/Scan.lean` |
| `Rung`, `modulate_idempotent`, `ground_terminal` — the assertive four as a grounding stack that ends where modulation exhausts | `Core/Stack.lean` |
| `Confrontation`, `confrontations` (12 entries), `kindMatchesStake` — documented historical changes forced through the Reading type; Record entries cannot exist without their frame | `Core/Confront.lean` |
| `NonFactoring`, `nonfactoring_parity`, `nonfactoring_cp_phase`, `nonfactoring_record` — the founding shape stated once, witnessed thrice: two wholes agreeing under every partial view, differing in the quantity | `Core/NonFactoring.lean` |
| `scan`, `scan_full_card` (7/10/11), monotone + terminal — the taxonomy as the terminal member of a resource-indexed family | `Core/Scan.lean` |
| `Rung`, `modulate_idempotent`, `ground_terminal` — the assertive four as a grounding stack that ends where modulation exhausts | `Core/Stack.lean` |
| `Confrontation`, `confrontations` (12 entries), `kindMatchesStake` — documented historical changes forced through the Reading type; Record entries cannot exist without their frame | `Core/Confront.lean` |
| `ViewClosed`, `viewClosed_iff_never_splits`, `macro_law_forced`, `viewClosed_comp`, `conserved_descends` — the object contract: emergence as a lossy view the dynamics never splits; the coarse law forced, tiers composing, conservation descending | `Core/Closure.lean` |
| `Claim`, `Status`, `stance`, `summary` — the published claims; `proved` claims name audited witnesses, `measured` claims name their basis (the predecessor record, CIRISAI/coherence-ratchet) | `Stance.lean` |

Records whose fields are `True` are **recorded commitments, not proofs**. This is never
blurred: `Gate.mechanized` states, per gate, whether CI enforces it or a human must.

## Discipline (load-bearing — these rules are the falsifiability, keep them)

The full set with reasoning is `epistemology.md`; the short form:

1. **Pre-register.** Method and the meaning of every possible answer, written down before any
   result is seen.
2. **Stake kills first**, and make them **separable** — each falsifier takes down its own
   claim and nothing beneath it.
3. **Match the null to the data's generative structure.** Discrete data needs a discrete null.
   This is the most common way to fool yourself and it has cost us a headline result.
4. **Disclose the tied fraction** before believing any rank-based statistic.
5. **Control estimator bias** with a shuffle/permutation floor.
6. **A residual is never support.** Support comes only from confirmed advance predictions.
7. **Report the fired kill as plainly as the survival**, and **keep the dead claim in the
   record, marked dead.**

## Layout

```
CIRISOntology/            # the Lean library
  Core/{Coordination,Provenance,Epistemics}.lean
  Stance.lean             # the published claims — single source of truth
axiomology.md             # how values are determined
epistemology.md           # how truth is determined + the CI mechanization
.github/workflows/        # CI (verification gates) and CD (publish the page)
```

## Style discipline

- **Current stance, stated plainly.** Equivocation is not humility and it is not
  falsifiability — the kill conditions are.
- **State strength honestly and never round up.** `proved` means machine-checked *here*;
  `measured` names its domain and precision; `wager` is a choice, not a result.
- Where a proof is open, say so and name the open step. Where a route is closed, record it
  once and move on.
- No claim enters the stance without a kill. No process commitment is advertised as
  machine-checked.
- Plain language is a requirement, not a courtesy: if a claim cannot be stated so a general
  reader can grasp what would falsify it, it is not yet understood well enough to publish.
