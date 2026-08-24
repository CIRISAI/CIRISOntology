# h3ere2 JUDGE PROTOCOL — pre-registered addendum to PREREG.md (`1dac9a0`)

Written **before any response has been generated or judged.** This addendum does not revise
PREREG.md; it specifies the judging instrument PREREG.md leaves open, and flags two holes
in it that would otherwise misreport the verdict.

---

## 1. POWER STATEMENT — stated in advance, as asked

Paired sign test on n = 170 items, two-sided alpha = 0.05:

| | win rate |
|---|---|
| significance threshold | **0.575** |
| detectable at 80% power | **0.607** |
| detectable at 50% power | 0.575 |

Order-flips remove items from the decisive set and cost power:

| flip rate | decisive n | sig. threshold | 80%-power effect |
|---|---|---|---|
| 0% | 170 | 0.575 | 0.607 |
| 20% | 136 | 0.584 | 0.620 |
| 40% | 102 | 0.597 | 0.639 |

And the sample size a modest effect would require:

| true win rate | n needed (80% power) |
|---|---|
| 0.55 | **785** |
| 0.58 | 307 |
| 0.60 | 196 |
| 0.65 | 87 |

**Verdict on adequacy: 170 items can resolve a LARGE effect and cannot resolve a modest
one.** The claim under test — that response quality stops scaling with parameter count — is
a large claim, and if it is true C should beat B substantially, so 170 is adequate *for the
claim as stated*. But a real-but-modest contribution (true win rate 0.55) would need 785
items and **would read as a null here.**

**Therefore, pre-committed now:** a null result will be reported as *"rules out a large
effect (>0.61); cannot exclude a modest one (<0.58)"* — never as "the coupling contributes
nothing." PREREG.md's KILLED language is scoped accordingly.

---

## 2. HOLE IN PREREG.md's POSITION-BIAS RULE — and the fix

PREREG.md says: judge every pair twice with order swapped, and *"if that rate is high the
judging is unreliable and the result must be reported as inconclusive."*

**That rule inverts the verdict in exactly the case it matters most.** The two-order
disagreement rate conflates two very different things:

- a judge with **position bias** flips, and
- **two genuinely indistinguishable responses** flip too, at ~50% by chance, because there
  is no quality signal to anchor the choice.

If C and B are truly equivalent — which is the KILLED outcome — the flip rate approaches
50% *because the answer is "no difference."* PREREG.md would then declare INCONCLUSIVE
precisely when the correct finding is KILLED. A high flip rate is evidence *for* the null,
not evidence that the instrument failed.

**The fix: measure position bias where it cannot be confounded, using two calibrations that
run BEFORE the real pairs are judged.**

**Calibration 1 — IDENTICAL PAIRS.** Present the same response as
both option 1 and option 2, forced choice, all 170 items. Content is identical, so *any*
departure from 50/50 is pure position bias. SE = 0.038, so this detects bias above ~0.075.
This is the number that gets called "the judge's position bias", not the flip rate.

> **CORRECTED 2026-08-24 — this number is a TIE-BREAK DIAGNOSTIC, not a position-bias
> predictor.** The paragraph above is wrong on its central claim and is kept, marked, rather
> than deleted. Measured on real pairs, the identical-pair rate does not merely fail to
> predict position behaviour — it **reverses sign**:
>
> | judge | identical-pair slot-1 | slot-1 on REAL pairs (soft) |
> |---|---|---|
> | `gemma3:12b` | 0.868 | **0.362** |
> | `llama3.1:8b` | 0.967 | **0.247** |
>
> `llama3.1:8b` measured 0.967 and still returned 56 decisive C-vs-A pairs, where pure
> position bias at that rate predicts ~6% decisive. What Calibration 1 actually measures is
> **how a judge breaks a perfect tie**, which is a degenerate behaviour that says nothing
> about how it weighs slots when there is real content to compare.
>
> Consequences, all of them already applied:
> - Report it as a tie-break diagnostic. Do **not** infer a real-pair position effect from it,
>   and do **not** predict decisive-pair yield from it.
> - Do **not** disqualify a judge on this number alone. `qwen3:14b`'s disqualification rests
>   **solely** on Calibration 2 (sensitivity 0.870 < 0.90), which is sufficient and untouched.
>   `mistral-nemo:12b` likewise fails on sensitivity (0.728).
> - **No verdict is affected.** Order-balanced scoring is immune to position bias by
>   construction, which is why the protection never depended on this number being right.
> - A lane pre-registration (`SECOND_JUDGE_PREREG.md`) argued that a slot-1 rate of exactly
>   1.000 is a *de facto* disqualification because order-balanced scoring would then yield
>   zero decisive pairs. That reasoning is **falsified by the table above** and is retracted.
>
> The failure this paragraph was reaching for is real, but it is a different one, and it needs
> its own gate: see **Calibration 3** in `AMENDMENT_J2_LENGTH_GATE.md`.

**Calibration 2 — KNOWN-GAP PAIRS (isolates judge sensitivity).** Pair each arm-A response
against a deliberately degraded version of itself (truncated to its first sentence).
A judge that cannot reliably prefer the intact response **cannot be trusted to report a
null**, because it is not discriminating at all. Pre-registered bar: the judge must prefer
the intact response on **>= 0.90** of these pairs. Below that, judging is reported as
failed and no verdict is issued.

This is the same positive-control discipline that made the classifier eval interpretable:
without it, a floor reading is indistinguishable from a broken instrument.

**Revised reliability rule (replacing PREREG.md's):**
- identical-pair bias >= 0.075 from 0.5 -> apply order-balanced scoring (below) and report
  the bias; do NOT call the result inconclusive on this ground alone. *(2026-08-24: and do
  not read it as a position-bias prediction either — see the correction above.)*
- known-gap sensitivity < 0.90 -> **judging failed**, report inconclusive, issue no verdict.
- **length preference (Calibration 3, added 2026-08-24) significantly above chance ->
  judge DISQUALIFIED before admission.** See `AMENDMENT_J2_LENGTH_GATE.md`. Added because
  `llama3.1:8b` passed both gates above — sensitivity 0.935, higher than the primary's
  0.902 — and still had length as its dominant decision variable, which surfaced only after
  it had judged 736 real pairs.
- flip rate on real pairs -> reported as an **effect-size signal** (high flip = C and B are
  similar), never as an instrument failure.

**Order-balanced scoring.** Every pair is judged in both orders. A pair counts as a C-win
only if C wins in BOTH orders; a B-win only if B wins in both; disagreements are recorded
as **flips** and excluded from the decisive set. This makes the primary statistic immune to
position bias by construction, which is why bias does not have to void the run.

---

## 3. JUDGE MODEL — and why not only the obvious one

The generator is Qwen3-0.6B. The locally available large model is **qwen3:14b — the same
family**, which risks a correlated preference for same-family prose. This programme has
already been bitten by exactly this class of correlation.

**Primary judge: `gemma3:12b` (different family).** **Secondary judge: `qwen3:14b`.**
Both run the full protocol. Inter-judge agreement is reported. A verdict claimed by only
one judge is reported as **split**, not as a win.

---

## 4. SCRAMBLE ASSIGNMENT — how the 10 draws enter

PREREG.md fixes 10 independent scrambles and says the comparison is against the scramble
*distribution*. Fully crossing them (170 x 10 x 2 = 3,400 judgments per judge) is not needed
and is not the cleaner statistic.

**Design: balanced random assignment.** Each of the 170 items is assigned one of the 10
scrambles, balanced (17 items per scramble), seed recorded. Every item then contributes one
C-vs-B pair whose B is a draw from the scramble distribution. This *is* "comparison against
the distribution", it propagates scramble-draw variance into the item-level noise where it
belongs, and it costs 170 x 2 = 340 judgments per judge.

Per-scramble win rates are reported as a secondary diagnostic; if one scramble is a wild
outlier that is recorded.

---

## 5. CONFOUND GUARDS (PREREG.md failure modes 1-4)

- **Length.** Report tokens and characters per arm. Fit `choice ~ length_diff + arm`
  (logistic). **If `length_diff` is significant and `arm` is not, the comparison is reported
  as length-confounded** and a length-matched re-run is required before any verdict.

  > **2026-08-24: this test was specified here and NEVER IMPLEMENTED.** For the whole K2
  > campaign `analyze.py` computed only the MARGINAL "did the longer response win", so the
  > conjunction stated above had not been evaluated for **any** judge, the primary included.
  > A pre-registered check that has to be remembered is not a control. It is now implemented
  > in `length_guard.py`, **runs by default** from `analyze.py`, and is gated in both
  > directions by `gate_length_guard.sh` (must fire on `gemma3` gold C-vs-B; must not fire on
  > `gemma3` soft C-vs-A), with the gate itself mutation-tested. Add the model-free companion
  > alongside it: split decisive pairs by **which arm is longer**. A finding that survives in
  > both strata — and survives hardest where the confound runs against it — needs no model to
  > be believed.
- **Compute.** Report wall time and generated tokens per arm.
- **Path degeneracy.** Report distinct-path count and path-length distribution per arm. If
  C and B paths are near-identical for most items, C-vs-B is trivially null and that is
  reported as a pipeline finding, not a physics finding.
- **Structure-flavoured prose.** Affects B and C equally by construction; this is recorded
  as the reason A is not the primary control.

---

## 6. A LIVE PROBLEM IN STAGE 1, flagged not fixed

`encode_wild.py` runs perception with
`nl_bridge_eval/onnx_q4f16/model_q4f16.onnx`. That artifact was measured this session
(addendum A3) at **0.576 vs 0.772 for the same weights at fp32** — naive RTN 4-bit costs
19.6 accuracy points and changes 26 of 92 predictions.

**Every arm shares this stage, so it does not bias C vs B.** But it degrades the perception
input all three arms are built on, which lowers the ceiling on any effect the judging can
detect. Recommended: run stage 1 from `onnx_fp32/model.onnx` instead. Recorded here so the
choice is deliberate rather than inherited.

---

# ADDENDUM J1 — written before any real pair was judged, after inspecting the fp32 encoding

The fp32 re-encode restored variation, but **the variation is almost entirely BETWEEN
streams, not within them**:

| stream | surfaces |
|---|---|
| fedreg | Facts 60 / 60 |
| github | Facts 46, Manner 4 |
| osm | Manner 57, Facts 3 |

So the encoder is behaving close to a **stream indicator**: fedreg -> Facts, osm -> Manner.
Consequently arm C's engine path takes only **2 distinct values across the 170 items**, and
those values track the corpus stream almost perfectly.

**Scope consequence, pre-committed now.** This is better than the superseded run (1 path,
zero per-item information) but it is NOT per-item reasoning. The treatment has **n = 2**
distinct levels. Any verdict must be stated as *"does the real coupling beat scrambled
across two path regimes that align with corpus stream"*, never as evidence that the engine
reasons about individual changes.

**Two analyses added, both declared before seeing any judgment:**

1. **Stratified by stream.** C-vs-B win rate is reported per stream (fedreg / github / osm)
   as well as pooled. If the pooled effect is carried by one stream it is a stream effect,
   not a coupling effect.
2. **Stratified by surface.** Because surface is near-collinear with stream, the same split
   by Facts-path vs Manner-path is reported. **If C beats B on one path regime and not the
   other, the pooled number is a mixture and must not be quoted alone.**

Power note: pooled n = 170 already only resolves a large effect (>=0.607 at 80% power).
Split by stream the strata are ~60/50/60, where the 80%-power threshold rises to ~0.68.
**The stratified analysis is diagnostic, not confirmatory**, and is reported as such.
