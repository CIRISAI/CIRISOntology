# PLANE STUDY RESULTS — the verdict is 11+1, by three convergent lines, at seventy cents

Run 2026-08-18 per `PLANE_PREREG.md` + §5b. 258 items (248 corpus + 10 Babel) × 7 conditions
× 3 model families = **5,418 judgments + 72 manipulation-check + 504 pilot = 5,994 total.
Spend: $0.63.** Parse rates: Gemma 1.000, Llama 0.994, gpt-oss 0.875→(patched)~0.95.
**VOID check: mean pairwise κ = 0.687 on clear items at BASE — PASSES the 0.6 floor.**

## Staked vs measured — the honest table

| stake | measured | verdict |
|---|---|---|
| `testimonial` frame-mobile | **0/40 under frame — its most STABLE axis** | **NOT CONFIRMED** (unpinned outcome; see §3) |
| `contingent` design-mobile | 6/40 = 0.15 vs floor 0.20 — **flat** | **RETRACTED per the prereg's own pinned row** |
| ten base kinds flat | all flat at p < 0.01 (worst: structural-design +0.12, p = 0.057) | **CONFIRMED** |
| `pragmatic` the at-risk label | flat everywhere (0.00–0.05) | survives cleanly |
| W-labels do not move (gauge) | W-mobility 0.095 ≈ frame 0.067 ≈ design 0.107 | see §2 — W is the common perturbation floor |

**At the pre-registered threshold, no kind is coordinate-mobile on any axis.** The base
plane is flat — *flatter than staked*, twelve labels wide at the panel level.

## §1 The verdict: 11 + 1, three lines converging

Per the prereg's pinned outcome row, `contingent`'s design-dependence is **retracted**: it
is an artifact-local kind; the design-relativity lives in its DISPOSITION (the out-of-scope
verdict is the design's call), not its label. Executed in the Lean: `basePlane_card` is now
**11**, `zero_design_dependent` replaces `one_design_dependent`, build green.

The final shape — **eleven artifact-local kinds + Record as the one relation** — is exactly
`Generator.lean`'s image (eleven site-generated kinds; Record provably not site-generatable),
and exactly what the panel measured. **Prereg outcome row, generator model, and measurement
agree on the count independently.** The 10+1+1 conjecture was wrong in the pretty direction:
the two "+1"s were not symmetric, and the asymmetry the disposition table hinted at was real.

## §2 The mechanism finding — resolved by the post-hoc manipulation check

The null was ambiguous: labels intrinsic, or panel context-blind? **The manipulation check
(labeled post-hoc — the original design lacked one, my omission) decides it:** asked the
relational question DIRECTLY ("can it still be established?"), the panel reads the frame —
**36/36 correct at full retention, 23/36 correct flips at sole-copy** — yet none of that
routes into kind labels (0/40). **Classification is site-cue-driven; the relational
computation runs beside it, on demand.** This is the two-stage architecture `Generator.lean`
formalizes and the v0 instruments implement: sites → kinds; frames → repairability verdicts.
The panel behaves like the model. The claim-table's frame/design entries are RE-SCOPED
accordingly: predicate-arity claims (theorem-backed, unchanged), not label-mobility claims
(refuted for this instrument class).

## §3 Deviations and gaps, named

* **W-as-floor is an ANALYSIS DEVIATION**: the prereg staked mobility against a test-retest
  floor; with three models there is one triple per cell and no test-retest existed. The
  warrant conditions (theorem-blind for the formal classifier) were substituted as the
  perturbation floor. Defensible, post-hoc, and labeled.
* **No manipulation check in the frozen design** — added post-hoc, labeled, and decisive.
  Filed as a gate candidate: *a null on a context-manipulation is uninterpretable without a
  manipulation check staked in the design.*
* `testimonial`-frame-flat was an **unanticipated outcome** — the prereg pinned meanings for
  the other cells but not this one. Reported without post-hoc promotion; the Lean re-scope
  note carries it.

## §4 Babel and the boundaries

**Babel: 7/10 edits kind-constant across all seven conditions.** The three violations are
UNIFORM misassignments — Premises→Facts in all seven conditions, Structure→Manner in all
seven, Model↔Facts flickering — i.e. even when wrong the panel is constantly wrong:
**no coordinate-driven label motion, in error or in truth.** No forbidden-count violation
observable at the label level.

**The boundary geometry replicated at every scale** (pilot 24 → full 248 → Babel):
Premises→Facts, Structure→Manner, Model↔Facts dominate all confusion, all
condition-independent — the same three the lay-anchor exercise predicted, plus
Priorities→Rules and Confidence↔Manner as minor lines. The taxonomy's error pattern IS its
adjacency structure, reproduced by three model families that never saw the theory.

## §5 What this buys the instrument suite

The two-stage architecture is validated as the DESCRIPTION of how classifiers behave, not
just a design choice: kind-instruments may be site-cue machines (cheap), and the relational
instruments (Record, and Circumstances' disposition) MUST be separate computations taking
their coordinates explicitly — which is what the v0 implementations already do and the
`Reading` type already enforces. The adjudicated corpus (κ 0.687 baseline, boundary map in
hand) is now the bake-off validation set the suite was waiting for.

**Next:** the ecological challenge (wild streams, NO-FIT + clustering) runs on the same
panel; the exhaustiveness question then stands on three witnesses: our search, the world's
streams, the standing bounty.
