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

---

# WHAT THE GATE MEASURED — everything above this line was written before the instrument existed

Collected 2026-08-24 by `calib_length.py` on all five judges the campaign has touched, on the
92 arm-A responses of `responses_soft92.jsonl`. Raw run record: `calib_length.log`; per-judge
judgments: `judge_soft92_<tag>_calib_length.jsonl`. Every number below is recomputed from
those jsonl files by `calib3.score`, not read out of the log.

| judge | padded rate | n | two-sided p | gate | padded-in-slot-1 | padded-in-slot-2 | slot-1 pick |
|---|---|---|---|---|---|---|---|
| `gemma3:12b` (primary) | 0.505 | 91 | 1 | **ADMIT** | 0.595 | 0.429 | 0.582 |
| `llama3.1:8b` (second judge) | 0.783 | 92 | 4.6e-08 | **REJECT** | 0.619 | 0.920 | 0.326 |
| `phi4:14b` | 0.696 | 92 | 2.2e-04 | **REJECT** | 0.405 | 0.940 | 0.217 |
| `mistral-nemo:12b` | 0.272 | 92 | 1.4e-05 | ADMIT (prefers intact) | 0.548 | 0.040 | 0.772 |
| `qwen3:14b` | 0.478 | 92 | 0.755 | ADMIT | 0.405 | 0.540 | 0.435 |

**The forward prediction was confirmed on both judges that matter.** The ADMIT/REJECT column
staked above — from the real-pair length marginals, written before this instrument existed —
is what the instrument returned, on constructed pairs that consumed no real pair: the primary
admitted at 0.505 with p = 1, the second judge rejected at 0.783 with p = 4.6e-08. The
pre-committed embarrassment did not occur, but it was live: nothing about the construction
protected `gemma3:12b`, and its 0.505 is a reading, not a design.

**One correction to the first implementation, and it moved a verdict.** The gate's first cut
failed on |deviation from 0.5| rather than on the padded direction, which disqualified
`mistral-nemo:12b` at 0.272 — the exact case the staked text says *passes* ("a judge that
prefers the intact one is penalising padding, which is desirable and passes"). The code, not
the bar, was wrong; it is fixed in `calib3.score`, and `gate_calib3.sh` pins that judge as the
direction control so the symmetric reading cannot come back. No threshold moved: alpha stays
0.05, n stays 92, and a judge above 0.5 fails at exactly the rate fixed above.

**A degeneracy in the randomisation, disclosed rather than patched.** `calib_length.py` draws
its per-item flip from `Random(20260822)` in the same order `judge.py`'s `calib_sens` does, so
the padded response lands in exactly the slot Calibration 2 put the *degraded* response in —
measured identical on 92/92 items for all five judges. Consequence: for a **slot-locked**
judge, Calibration 3's rate is the exact complement of its Calibration 2 sensitivity and
carries no new information. `mistral-nemo:12b` is that case — sensitivity 0.728, padded 0.272,
complementary to the item, picking slot 2 on 4% of the pairs where the padding sat there — so
its ADMIT here is **uninformative, not a demonstration that it penalises padding**, and it
stays disqualified on sensitivity (0.728 < 0.90). The rejections are not vulnerable to this:
`llama3.1:8b` prefers the padded response in **both** slots (0.619 and 0.920), and the primary
is not slot-locked (slot-1 pick 0.582), so its admission is a genuine reading. Nor can the
degeneracy manufacture a rejection: the flip split is 42/50, so slot-locking *alone* yields
0.457 or 0.543, both far short of the ~0.60 the bar needs at n = 92. The seed is kept because
the five collected artifacts must stay reproducible from the code; the hazard is handled by
reporting the per-slot split on every reading, which is what makes a slot-locked judge visible.
`phi4:14b`'s rejection is the one that leans on it (0.405 / 0.940, slot-1 pick 0.217) and
should be read as slot-driven; that judge was already disqualified on sensitivity (0.859).

**Deviation from the staked construction, recorded not reworded.** The text above specifies "a
fixed, neutral, on-topic sentence pair"; the implementation uses **one** 128-character
sentence. The binding constraint in the staked text is the *sizing* — median padded/intact
ratio near the measured arm C/A ratio of 1.448 — and one sentence achieved 1.459, so a second
would have overshot the regime the gate is supposed to probe.

## Where the gate lives, and what makes it unskippable

| file | role |
|---|---|
| `calib3.py` | the padding text, the seed, the bar, the scorer. No inference, no network, no imports from the collector — which is what lets the interlock read a verdict without a cycle. |
| `calib_length.py` | collection driver; imports `judge.ask` so the request shape is the sealed one byte for byte. `--score <file>` rescoring runs offline. |
| `judge.py` → `require_calib3` | **the interlock.** `judge.py pairs` refuses to judge a real pair for a model that has not passed Calibration 3, and fails **closed** on a missing artifact. |
| `gate_calib3.sh` | 11 checks: all five readings pinned in both directions, the padding text pinned by sha256, the interlock proven reached, proven to reject a failing judge, and proven inert on the admitted primary. |

The gate is itself mutation-tested — four mutations, each verified to make it fail: making the
bar symmetric again, deleting the interlock call from `judge.py`, changing one letter of the
padding text without changing its length (which is why the pin is a hash and not a length —
the first cut of that check tested `len(PAD)==128` and the mutation walked through it), and
making a missing calibration artifact return a pass.

**What this does to the closed record: nothing.** The interlock was added *after* the K2 and
second-judge verdicts were produced. The sealed pre-interlock `judge.py` is preserved in git at
`d74496b`, sha256 `0a876c3d6fe5cafa24e80ad9a074d26291bfabf1eac770e0c281ef039913afdd`. The
interlock touches only a preflight above `main`'s body; it reads stored files, writes nothing,
and returns without effect for an admitted judge — proven by calling it directly rather than by
re-running 736 closed pairs. `llama3.1:8b`'s readings stand exactly as reported in
`RESULTS_K2_SECOND_JUDGE.md`; what changes is that a judge like it can no longer be admitted.

---

## Relationship to Calibration 1, which is being narrowed in the same pass

Calibration 1's identical-pair number is **not** a position-bias predictor: measured, it
*reverses* on real pairs (`gemma3` 0.868 → 0.362; `llama3.1` 0.967 → 0.247). It is retained
as a **tie-break diagnostic** only. See the correction in `JUDGE_PROTOCOL.md`. Calibration 3
is not a replacement for it — it measures a different failure, and unlike Calibration 1 it is
measured on pairs whose content genuinely differs only in the dimension being probed.
