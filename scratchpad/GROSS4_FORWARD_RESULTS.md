# GROSS4 FORWARD RESULTS — the traffic split predicts forward

Run 2026-08-19 against `GROSS4_FORWARD_PREREG.md` (frozen the same day, before any
sampling code contacted the stream). Stream: **Stack Exchange post revision history**,
sites `superuser` + `english` + `diy`. **n = 60**, BASE x 3 judge families, 180
judgments, **$0.02**.

**All three stakes land. The kill did not fire. No VOID gate tripped.**

## The stakes, each beside its measured value

| # | stake, as frozen | staked | measured | verdict |
|---|---|---|---|---|
| 1 | PRIMARY: gross-four share (Facts+Rules+Manner+Identity) of modal labels | in **[0.78, 0.97]** (point 0.89); **KILL if < 2/3** | **53/60 = 0.8833** | **LANDS**; kill **not fired** |
| 2 | SHARP SECONDARY: Model + Premises modal labels | **at most 2** | **0** (Model 0, Premises 0) | **LANDS** |
| 3 | ORDERING: modal #1 kind | **Facts or Manner** | **Manner** (45) | **LANDS** |

Per the prereg's frozen meanings: *"All three land -> the 4+7 traffic claim gains its
first forward confirmation; promotion of the observation to a measured stance-claim
becomes eligible (steward decision, not automatic)."* That condition is met. The
promotion decision is the steward's and is not taken here.

The point prediction was 0.89; the measurement is 0.8833. Wilson 95% interval
[0.778, 0.942]. Against the 279-item baseline rate 0.9140, the forward reading is
statistically indistinguishable (P(X<=53 | n=60, p=0.9140) = 0.256) — the split did not
merely survive, it reproduced its magnitude on a stream it had never seen.

### VOID gates (all clear)

| gate | threshold | measured | |
|---|---|---|---|
| usable n | >= 45 | **60** | ok |
| off-taxonomy / NO-FIT modal rate | <= 10% | **1/60 = 1.67%** | ok |
| judge models available | all three | all three answered on all 60 items | ok |

## Modal distribution (the panel-traffic measurement)

| kind | modal count | share |
|---|---|---|
| **Manner** | 45 | 75.0% |
| **Facts** | 7 | 11.7% |
| Confidence | 3 | 5.0% |
| Process | 2 | 3.3% |
| Circumstances | 1 | 1.7% |
| **Identity** | 1 | 1.7% |
| NO FIT | 1 | 1.7% |
| **Rules** | 0 | 0 |
| Priorities, Structure, Model, Premises, Record | 0 | 0 |

Gross four in bold-adjacent terms: **Manner 45 + Facts 7 + Identity 1 + Rules 0 = 53.**

Per sub-community (free analysis, not staked):

| sub-community | n | gross-four | profile |
|---|---|---|---|
| superuser | 22 | 21/22 = 0.955 | Manner 19, Facts 2, Circumstances 1 |
| english | 16 | 14/16 = 0.875 | Manner 12, Confidence 2, Facts 2 |
| diy | 22 | 18/22 = 0.818 | Manner 14, Facts 3, Process 2, Confidence 1, Identity 1, NO FIT 1 |

All three sub-communities clear the kill line independently, and each clears the band's
lower edge independently.

## The caveat that matters, stated plainly

**The aggregate landed; the internal composition did not reproduce.** On the 279-item
baseline the gross four were spread — Facts 103, Rules 78, Manner 40, Identity 34. Here
they are one kind: Manner carries 45 of the 53, Rules contributes **zero** modal labels
(one judge-level vote in 180), Identity one. What has been confirmed forward is the
**aggregate share** the prereg staked, on a stream whose edit traffic is dominated by
copyediting. It is not evidence that the four-way internal balance is stream-invariant,
and nothing here should be read as such. The ORDERING stake anticipated the direction
(it predicted Facts-or-Manner as a "technical-prose genre prediction") but the *degree*
of concentration is new information, and it is the honest limit on how much this run
buys.

## Robustness: the tie-break cannot move the verdict

The frozen modal rule (`Counter(votes).most_common(1)[0][0]`, ties to first-encountered
— the rule that produced the 91.4%) leaves **6 of 60 items** decided by a three-way
1-1-1 split. On all six, the first-written model (Llama-4-Scout) voted a gross-four
label, so the frozen convention sits at the **top** of the tie-break range. Both ends
were computed:

- frozen convention (the verdict): **53/60 = 0.8833**
- adversarial worst case (every tie resolved AGAINST the gross four wherever possible): **48/60 = 0.8000**
- ties dropped entirely: **47/54 = 0.8704**

All three are inside [0.78, 0.97] and all three are far above the 2/3 kill. The primary
verdict does not depend on the tie rule. The six tied items are `sx-00, sx-20, sx-34,
sx-37, sx-49, sx-51`.

Scorer calibration: the same script, run on the archived judgment files, recomputes the
baseline as **255/279 = 0.9140** — the published figure to four places. The modal
convention used here is therefore the same one that produced the number being tested.

## The single off-taxonomy modal is a resolution-floor datum, not a thirteenth kind

`sx-27` is modal **NO FIT** (2 of 3 judges). Its whole change is the deletion of one
word: "most of **these** ground rod drivers" -> "most ground rod drivers". Both refusing
judges gave the same reason — *"the text is identical in both versions"*. They did not
reject the taxonomy; they failed to see a one-word edit. The third judge classified it
without difficulty (Identity: the referent moves from a specific set to a generic class).

This reproduces `wiki2-10` exactly — the wild programme's only other modal NO-FIT, whose
whole change was one glyph (a curly apostrophe straightened). Two streams, two modal
NO-FITs, both of them minimal edits misread as no-edits. Wild modal NO-FIT tally after
this run: **2 on 339 wild changes (0.6%)**, both at the smallest edit the instrument can
be asked about.

## Sampler yield

`eco_sample_stackex.py`, seed **20260819** pinned before any fetch. Output
`plane_corpus/eco_stackex.jsonl` (60 items), funnel counters
`plane_corpus/eco_stackex_funnel.json`.

| funnel stage | superuser | english | diy | total |
|---|---|---|---|---|
| posts returned by `/posts?sort=activity` | 200 | 200 | 200 | 600 |
| ...carrying a `last_edit_date` | 136 | 139 | 108 | 383 |
| ...whose last body-changing revision is in the size window (3..400 chars) | 63 | 47 | 54 | 164 |
| ...cleaned-paragraph counts match before/after | 43 | 26 | 39 | 108 |
| ...**exactly one cleaned paragraph differs** | 22 | 16 | 22 | 60 |
| accepted (after the 1500-char cap, which never bit) | **22** | **16** | **22** | **60** |

**20 API requests total** (1 filter creation, 6 post-listing pages of 100, 13 revision
batches of 20 post ids = up to 260 posts examined at revision level; the final batch was
cut short the moment n=60 was reached). Quota remaining 277 of 300; no 429, no backoff
directive received. Target n=60 was **reached, not padded**.

Yield: **60/600 = 10% of recently-active posts**, or 60/260 = 23% of posts actually
examined at revision level. The 10% figure is the same rate wiki2's one-clean-paragraph
gate produced (49 from 500), which is the expected behaviour of an unchanged gate.

## Spend

**$0.02** against the prereg's **$0.25** cap. 180 judgments (60 items x BASE x 3 models).
The cap was enforced in code: `run_stackex_panel.py` sets
`plane_annotate.HARD_CAP_USD = 0.25` before calling the runner's `main()`, so the frozen
instrument itself is unmodified.

## Deviations, labelled

1. **Gate translation, wikitext -> HTML (mechanical; no threshold changed).** wiki2 built
   its paragraph list by dropping structural lines (`=heading`, `{|table`, `|row`,
   `*bullet`, `#list`, `{{template`, `[[File`, `[[Category`) and keeping prose. Stack
   Exchange bodies are HTML, so the same drop is `<pre>`, `<blockquote>`, `<ul>`, `<ol>`,
   `<table>`, `<h1..h6>`, `<hr>`, `<img>`, and prose is the `<p>` blocks. **Every
   numeric threshold is byte-identical to wiki2**: cleaned length >= 120, alphabetic
   fraction >= 0.6, differing pair capped at 1500 chars, candidate size window
   3 <= |len(body) - len(last_body)| <= 400, paragraph counts must match, exactly one
   paragraph may differ.
2. **wiki2's wikitext table-junk check (`'||' in c or '|-' in c`) is inapplicable** and
   was dropped; HTML tables are already removed as blocks upstream of it.
3. **Seed role.** wiki2 used its seed to randomise the recentchanges time window; there
   is no such window on this endpoint, so seed 20260819 sets the per-site page order over
   `/posts` pages 1-8. Same function (deterministic sampling spread), different endpoint.
4. **Two of 180 judgments failed to parse** (both `max_tokens` truncations mid-JSON:
   `sx-16` Llama, `sx-22` gpt-oss). Those two items were scored on their two surviving
   votes, which were unanimous in both cases (Manner, Manner; Facts, Facts) — so neither
   item's modal is in doubt. This is **not** the VOID condition, which is a judge model
   being *unavailable*: all three models were available and answered all 60 items.
   58/60 items carry a full three-model panel.
5. **`sx-51` contains a bare URL naming the source site**, pasted by the post's own
   author inside the prose being edited. It was **not scrubbed**: the frozen gate
   contains no in-text provenance edit, wiki2's cleaner likewise leaves bare URLs
   standing, and rewriting wild item text after seeing it is exactly the liberty the
   prereg exists to prevent. The BASE condition supplies no attribution to the judges,
   and knowing the host site does not favour any of the twelve kinds. Disclosed rather
   than repaired.

No other deviation. Nothing in the protocol was changed after data was seen.

## Files

- prereg (governing): `scratchpad/GROSS4_FORWARD_PREREG.md`
- sampler: `scratchpad/eco_sample_stackex.py`
- corpus: `scratchpad/plane_corpus/eco_stackex.jsonl` (60 items)
- funnel: `scratchpad/plane_corpus/eco_stackex_funnel.json`
- panel wrapper: `scratchpad/run_stackex_panel.py` (runner `plane_annotate.py`, unmodified)
- judgments: `scratchpad/plane_corpus/stackex_judgments.jsonl` (180)
- scorer: `scratchpad/score_gross4_forward.py`
- scores: `scratchpad/plane_corpus/stackex_score.json`
