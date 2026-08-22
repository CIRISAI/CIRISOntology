# h3ere2 response-quality PREREG
**Written 2026-08-22, before the pipeline's missing pieces exist and before any response
is generated or judged.** Nothing below may be revised after a result is seen.

## The claim under test

h3ere2 puts the SLM on perception and articulation and the **physics engine on the
reasoning**. A 0.6B model reads the situation into a state and writes the answer out; the
multi-step constrained inference between them is done by an exact, deterministic,
machine-checked dynamical system on the 11-kind graph.

**If that works, response quality stops scaling with parameter count.** That is the claim,
and it is worth trying to kill.

## Arms

| arm | pipeline | purpose |
|---|---|---|
| **A — base** | Qwen3-0.6B, single call, direct answer | the engineering baseline |
| **B — scrambled** | full h3ere2, **coupling matrix scrambled** | **the placebo** |
| **C — real** | full h3ere2, real coupling | the construction |

**B is the load-bearing arm.** A vs C conflates two things — extra structure and extra
compute — so it cannot tell us whether *the object* contributes. B holds architecture, call
count, token budget, renderer and prompt identical and changes only whether the graph is
the real one. This is the same trap that has caught this programme before: every
change-blind control cleared the label floor too, and selection has to be on the
construction-minus-placebo gap, not on the construction's own score.

### Scramble construction (fixed now)
Randomly permute the **off-diagonal entries** of `COUPLING`, preserving symmetry. This
holds the weight multiset **exactly** — same values, same degree sum, same spectrum-scale —
and destroys only *which pair carries which weight*. A node relabelling would NOT do: that
is a graph isomorphism and the physics is identical under it.

**Run 10 independent scrambles**, not one. A single draw can be lucky; the comparison is
against the scramble *distribution*.

## Substrate
The **170 wild changes** from three unrelated streams (`plane_corpus/eco_corpus.jsonl`).
Chosen because they are real-world, never trained on, and carry `kind_target: "WILD"` — no
gold labels, which is fine here: we judge **responses**, not labels. Their lack of gold is
what made them useless for the classification eval and makes them ideal for this one.

Task per item: given the change, produce a short recommendation/analysis.

## Judging
- Judge is **NOT** the generator. Use a substantially larger model.
- **Pairwise, blind**: two responses, no arm identity, judge picks the better.
- **Randomize presentation order per item** and record it. LLM judges have strong position
  bias; unrandomized order alone can manufacture a win.
- Every pair judged **twice with order swapped**. Disagreement between the two orders is
  measured and reported as the judge's position-bias rate. If that rate is high the judging
  is unreliable and the result must be reported as inconclusive rather than as a win.

## Pre-registered outcomes

**Primary (the scientific claim): C vs B.**
- **SUPPORTED** iff C's win rate over the scramble distribution exceeds 0.5 at p < 0.05
  (two-sided, paired by item).
- **KILLED** iff C does not beat B. Then the coupling structure contributes nothing to
  response quality, the physics is decorative in this pipeline, and that is the finding —
  reported as plainly as a success would be.

**Secondary (the engineering claim): C vs A.** Reported, but it cannot rescue a failed
primary. C > A with C ≈ B means we built a scaffold that helps, not a physics that reasons.

**Stated in advance:** a null here does NOT falsify the engine, the taxonomy, or the
classifier. It falsifies *this pipeline's use of them for response generation*. Scope the
conclusion to that.

## Failure modes to guard, named before they can be rationalised
1. **Compute confound.** Report tokens generated and wall time per arm. If C uses more, say so.
2. **Renderer doing the work.** If the renderer is the same SLM call in B and C, any gap is
   attributable to the path it was handed — which is the point. But if C's paths are
   systematically *longer*, the gap may be verbosity. Report path length per arm and
   check whether the judge simply prefers longer answers.
3. **Degenerate paths.** If the engine returns near-identical paths for most items, C and B
   converge trivially. Report path diversity.
4. **Judge preferring structure-flavoured prose.** Both B and C are rendered from paths, so
   this affects them equally — which is another reason B, not A, is the control.
