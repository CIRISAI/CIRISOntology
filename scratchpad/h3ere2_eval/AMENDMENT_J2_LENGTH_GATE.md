# AMENDMENT J2 — a THIRD calibration gate: length preference

**Written 2026-08-24, before the instrument exists and before any candidate has been run
through it.** Addendum to `JUDGE_PROTOCOL.md`. It adds a gate; it moves no existing one.

## The hole this closes

`llama3.1:8b` **passed both** of the protocol's calibration gates — identical-pair position
bias, and known-gap sensitivity at 0.935, *above* the primary's own 0.902 — and then turned
out to have **length as its dominant decision variable**, which only became visible after it
had judged 736 real pairs and produced a reversal that had to be diagnosed post hoc.

Two gates that a length-dominated judge walks straight through is a gate-shaped hole. The
existing gates ask *does it have a side?* and *can it see a real gap?* Neither asks *what is
it actually deciding on?*

## This is not a bar raised to fit a result — and it must prove that on its face

The gate separates the two judges on a property visible in data that already exists, and it
separates them **the way the post-hoc diagnosis already did**:

| judge | picked the LONGER response, real pairs (soft) | this gate would |
|---|---|---|
| `gemma3:12b` (primary) | 0.466, p = 0.210 — no preference | **ADMIT** |
| `llama3.1:8b` (second) | 0.595, p = 0.0003 | **REJECT** |

Stated precisely, because the distinction matters: those two marginals come from the verdict
runs. **The gate itself consumes no real pairs at all** — it runs on constructed calibration
pairs only, which is exactly what lets it run *before* a judge is admitted rather than after
it has produced a verdict. The corroboration above is what makes the gate credible; it is not
the gate.

**The threshold is fixed on principle, not tuned to this pair of judges** (below), and I am
pre-committing to the outcome that would embarrass this lane: **this gate can reject the
primary.** If `gemma3:12b` fails it, K2's instrument is impeached and that will be reported
as plainly as a pass — not suppressed, not re-thresholded. Saying so before running it is the
only thing that makes the threshold binding, and it is the same standard applied when the
0.90 sensitivity bar was left alone through three consecutive candidate failures.

## Calibration 3 — LENGTH-PREFERENCE PAIRS

**Construction.** For each of the 92 items, take the arm-A response and build a **padded**
variant of *itself*: the same text plus a fixed, neutral, on-topic sentence pair that adds
**no information** about the change. Present intact vs padded, forced choice, **order
randomised per item** and recorded, exactly as Calibration 2 does.

Content is identical apart from contentless filler, so a judge that reliably prefers the
padded response is rewarding **length as such**. A judge that prefers the intact one is
penalising padding, which is desirable and passes.

**Padding is sized to the regime that actually matters.** Arm C is longer than arm A by a
measured median char ratio of **1.448**, and that gap is what the C-vs-A comparison rides on.
The pad is therefore sized so the median padded/intact ratio lands near 1.45 rather than at
some arbitrary inflation. The achieved per-item ratio distribution is reported.

**Statistic.** The rate at which the judge picks the **padded** response.

**Bar, fixed now.** A judge **FAILS** if it prefers the padded response **significantly more
often than chance** — two-sided binomial against 0.5, alpha = 0.05, n = 92. The bar is a
significance criterion rather than a round number precisely so it cannot be accused of having
been chosen to sort these two candidates; at n = 92 it corresponds to roughly 0.60. The rate
and its p-value are reported for every candidate whether it passes or fails.

**Placement.** Runs **before** any real pair is judged, alongside Calibrations 1 and 2. A
judge that fails is a recorded disqualification, exactly as `qwen3:14b` and `mistral-nemo:12b`
are.

**What a failure does NOT mean.** It does not void work a failing judge has already done; it
means that judge's comparisons must carry the section-5 length guard's verdict, which is now
run by default in `analyze.py`. The two are the same concern caught at two different stages —
this gate before admission, section 5 after analysis.

## Relationship to Calibration 1, which is being narrowed in the same pass

Calibration 1's identical-pair number is **not** a position-bias predictor: measured, it
*reverses* on real pairs (`gemma3` 0.868 → 0.362; `llama3.1` 0.967 → 0.247). It is retained
as a **tie-break diagnostic** only. See the correction in `JUDGE_PROTOCOL.md`. Calibration 3
is not a replacement for it — it measures a different failure, and unlike Calibration 1 it is
measured on pairs whose content genuinely differs only in the dimension being probed.
