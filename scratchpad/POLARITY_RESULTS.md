# POLARITY RESULTS — the sign is scoreable, the corpus cannot test it, and one kind never moves along its own axis

Run 2026-08-20 per `POLARITY_PREREG.md` (FROZEN 2026-08-20, before any item was scored).
Operationalisations the prereg left open were pinned in
`polarity/EXECUTION_NOTE.md` **before** the panel ran; they are listed as deviations in §7.
**Amendment A1** (appended to the prereg and committed before the lead read any result of this
run) adds labelled secondaries in **§6**; they sit beside the primary and displace nothing.

**272 corpus items → 252 scored (20 `Record` items have no axis in the frozen table) × 3
model families = 756 judgments. Spend: $0.0615 of a $0.30 cap.**

## Headline

| stake | staked band | measured | verdict |
|---|---|---|---|
| **P1** polarity is scoreable | AMBIGUOUS modal ≤ 25% | **20.6%** (52/252) | **CONFIRMED** — but 26.5% counting `Record`; see §1 |
| **P2** confusion matrix polarity-symmetric | p < 0.01 → structural; p ≥ 0.01 with power → bookkeeping; < 4 qualifying kinds → UNDERPOWERED | **3 kinds** clear the 8-per-polarity bar | **UNDERPOWERED — no verdict either way, and no kill** |
| **P3** twin asymmetry survives conditioning on sign | survives / vanishes (vanishing retracts a claim in `TWO_WAY_READING.md`) | **cannot be conditioned**: `Circumstances` has 1 scoreable item of 20 | **NOT DECIDED — undefined, not negative.** No retraction is triggered; no support either |
| **P4** per-kind ambiguity | name any kind > 50% | **`Circumstances` 95.0%** — the only one | **`Circumstances`'s polarity is undefined in a majority of its items** (A1's split refines the mechanism: it is ZERO, not inapplicable — §6) |

**VOID checks (§4), all clear:** P1 not above 40%; all three judge models available; parse
failure **1.19%** (9/756, all Llama-4-Scout — Gemma and gpt-oss 0.000) against a 5% VOID
threshold, and no item lost a usable modal; **200 scoreable items** against a 150 floor.
The test is not VOID. Its primary question is simply unanswerable on this corpus, and the
reason is itself the most useful thing it produced.

## §1 P1 — polarity IS scoreable, at 20.6%

52 of 252 axis-defined items come back AMBIGUOUS: **20.6%**, inside the staked ≤ 25% band.
Panel agreement is high — **133 unanimous, 102 at 2–1, 17 three-way ties** (ties → AMBIGUOUS
per §2 of the prereg; so 35 of the 52 are a genuine AMBIGUOUS plurality, 17 are ties).

**The honest caveat, at full volume:** the frozen §1 table defines polarity for **eleven**
kinds and has **no row for `Record`**, while the corpus the prereg names contains **20 Record
items**. Inventing a twelfth axis after freeze would be unfreezing the prereg, so those 20
were not scored (`EXECUTION_NOTE` D10, pinned in advance). Counting them as
undefined-by-construction, the rate over the full 272 is **26.5%**, which lands in the
prereg's 25–40% "scoreable but weak; exploratory only" band. **The P1 verdict therefore
depends on a denominator that the prereg did not pin.** The primary reading (20.6%) is the
one pinned in advance and is the one reported as the verdict, because P1 asks whether the
*construct* is scoreable and the construct exists only for the eleven kinds that have a row.
A reader who prefers the 272 denominator should read everything downstream as exploratory.

## §2 P2 — UNDERPOWERED, determined before any p-value was computed

The prereg requires the UNDERPOWERED condition to be evaluated **before** reading a p-value.
This was enforced mechanically, not by intention: `analyse_power.py` computes the cell counts
and the permutation null, writes `power.json`, and computes **no** observed statistic and
**no** p-value; `analyse_p.py` refuses to run if `power.json` is absent. The determination is
on disk with a timestamp earlier than the file containing the p-value.

**Only 3 kinds clear the "≥ 8 scoreable items in both polarities" bar: `Facts` (10/11),
`Identity` (15/9), `Rules` (21/13). The bar is 4.** Verdict per the frozen text:
*"no verdict either way, and no kill."* The holonomy/loop question neither gains its
necessary condition nor loses it.

The other UNDERPOWERED clause did **not** fire: the null's spread does not exceed the
observable range (null mean 0.1039, sd 0.0335, against a statistic maximum of 1).

### Why the power is absent — a design finding, not a sample-size accident

The corpus was authored to load **kinds**, never signs, so its polarity marginals are lopsided
by construction. Minority-polarity counts per kind: `Structure` **2**, `Priorities` **5**,
`Process` **5**, `Manner` **6**, `Model` **6**, `Confidence` **7**, `Premises` **7**,
`Circumstances` **0**. Four kinds miss the bar by one or two items. **A corpus authored
without regard to sign cannot test the sign.** Testing P2 properly needs a corpus authored
balanced in polarity per kind — which is a cheap, well-specified next instrument, and is the
one thing this run establishes about what to do next.

### The descriptive numbers, which carry NO verdict

Reported because the discipline says report, and labelled because the prereg's UNDERPOWERED
clause fired before they were computed. **Nothing may be promoted from this table.**

| pooled statistic | obs | null mean (sd) | p |
|---|---|---|---|
| primary (full rows, unweighted over 3 kinds) | 0.1222 | 0.1039 (0.0335) | 0.332 |
| n-weighted (sensitivity) | 0.1000 | — | 0.319 |
| CONJ excluded (2 kinds only) | 0.1833 | — | 0.306 |
| errors-only (sensitivity) | **not computable** — no kind clears 8-per-polarity once correct reads are removed | | |

Per kind, the two read distributions:

| kind | n `+` / n `-` | TVD | reads of `+` items | reads of `-` items |
|---|---|---|---|---|
| Rules | 21 / 13 | **0.000** | Rules 21 | Rules 13 |
| Identity | 15 / 9 | 0.067 | Identity 14, Circumstances 1 | Identity 9 |
| Facts | 10 / 11 | 0.300 | Facts 7, Rules 2, Circumstances 1 | Facts 9, Confidence 2 |

`Rules` is exactly polarity-symmetric: 34 scoreable Rules items, every one read as Rules
whichever way it moves — tightening and loosening confuse identically, which is to say not at
all. The `Facts` row is the only one with visible structure (increases leaking to `Rules`,
decreases leaking to `Confidence`), and it rests on **3 errors against 2** with p = 0.24.
That is a residual, and per discipline rule 6 a residual is never support.

## §3 P3 — the twin test cannot be run, and the reason is the finding

The staked test was: does the Structure-vs-Circumstances asymmetry survive conditioning on
sign? **It cannot be conditioned. `Circumstances` has one scoreable item out of twenty**
(19/20 AMBIGUOUS). One of the two twins has no polarity to condition on.

The unconditional asymmetry reproduces `TWO_WAY_READING.md` exactly, which validates this
pipeline against the earlier one:

| target ↓ read → | to Facts | to Manner | (own label) | other |
|---|---|---|---|---|
| Structure (n=20) | **0** | **7** | 9 | Process 2, Rules 2 |
| Circumstances (n=18 with a non-tie BASE modal) | **9** | **1** | 7 | Identity 1 |

Conditioned on sign, every stratified table is degenerate — `Circumstances` contributes 1
item to the `+` stratum and 0 to the `-` stratum. The stratified tests return
CMH p = 0.724 and a stratified-permutation p = 1.000 for the →Manner channel, and these
numbers mean **nothing**: they are the arithmetic of an empty cell, not evidence of absence.

**Stated at the volume the prereg demands:** the asymmetry **did not vanish** under
conditioning, so **no claim in `TWO_WAY_READING.md` is retracted**. But it did not survive
either — it was never tested. `TWO_WAY_READING.md`'s twin-asymmetry claim stands exactly
where it stood, with one addition it must now carry: **we cannot currently rule out that it is
a polarity artifact, because one of the two twins has no definable polarity.** Anyone citing
the Structure/Circumstances asymmetry should cite that caveat with it.

One observation, recorded and explicitly **not** offered as support for anything: the twins
now differ in a third way — `Structure` has a strongly populated axis (17/2), `Circumstances`
has none. That converges with `TWO_WAY_READING.md` §3, where `Circumstances` is already the
unique anomaly (`assertsContent = false`, disposition `outOfScope`). Convergence of a residual
with a prior residual is not a confirmed advance prediction and is not counted as one.

## §4 P4 — per-kind ambiguity, and the kind that never moves

| kind | n | `+` | `-` | AMBIGUOUS | rate |
|---|---|---|---|---|---|
| **Circumstances** | 20 | 1 | 0 | **19** | **95.0%** |
| Process | 20 | 5 | 6 | 9 | 45.0% |
| Premises | 24 | 7 | 12 | 5 | 20.8% |
| Manner | 20 | 10 | 6 | 4 | 20.0% |
| Facts | 26 | 10 | 11 | 5 | 19.2% |
| Priorities | 20 | 5 | 12 | 3 | 15.0% |
| Identity | 27 | 15 | 9 | 3 | 11.1% |
| Model | 20 | 12 | 6 | 2 | 10.0% |
| Structure | 20 | 17 | 2 | 1 | 5.0% |
| Rules | 35 | 21 | 13 | 1 | 2.9% |
| Confidence | 20 | 13 | 7 | 0 | 0.0% |
| **Record** | 20 | — | — | — | **no axis in the frozen table** |

**`Circumstances` is named, per the prereg, as a kind without a well-defined axis** — the only
kind above 50%. (Amendment A1's finer split, §6, corrects the *mechanism* below while leaving
this verdict standing: the judges say the axis applies and the move along it is nil, so the
accurate reading is ZERO rather than inapplicable.) The panel's reasons converge on one mechanism without being prompted toward
it: a Circumstances change is a **substitution of one instance for another**, not a move along
a specificity axis. Verbatim: *"Changing a specific date within a circumstance doesn't make the
circumstance more or less specific; it's a different instance of the same kind"*; *"Changing
the location of the trial order from Delford to Marwick doesn't make the circumstance more or
less specific; it simply alters where the circumstance occurred."* The §1 rule
(`+` = instance made MORE specific) presupposes a change of grain; the corpus's Circumstances
items change the value, not the grain.

`Process` at 45.0% sits below the naming threshold but has the same shape: the panel reports
that a **re-ordering** neither adds nor removes steps, so the "steps ADDED / order made
stricter" axis does not pick out a direction. Reported, not named, because 45% < 50% and the
threshold was frozen.

**`Record` is a gap in the prereg, not a measurement.** §1's table has eleven rows; the corpus
§2 names has twelve kinds. This is an error in the frozen document, found by executing it, and
it is reported rather than patched.

## §5 What this cannot do — reproduced verbatim from the prereg

> It cannot establish a holonomy. A polarity-asymmetric confusion matrix would show the sign
> carries structural information — a NECESSARY condition for the loop question to be
> meaningful, not a sufficient one. No claim about phases, projective representations or the
> tenfold way follows from any outcome here, and the results document must say so.

It says so. And since the outcome here is UNDERPOWERED rather than asymmetric, even the
necessary condition is unestablished: **nothing about phases, projective representations or
the tenfold way follows, in either direction, from this run.**

## §6 AMENDMENT A1 — the secondaries, reported BESIDE the primary

`AMENDMENT A1` was appended to the prereg and committed **before any result of this run was
read**, and says so in its own heading. Everything in this section is computed from the 756
judgments already on disk: **no rescoring, no new spend.** Nothing here displaces §§1–4.

A1's objection is correct and its defect is real: **AMBIGUOUS conflated three things** —
ZERO (a genuine point on {+1, 0, −1}), N/A (the axis does not apply — missing data), and TIE
(judges split `+`/`-` — measurement failure, which frozen §2 wrongly turned into a reading).

### S1 — the three counts

| case | n | share of 252 |
|---|---|---|
| **signed** (`+` 116, `-` 84) | **200** | 79.4% |
| **ZERO family** (judges agreed on ambiguity) | **35** | 13.9% |
| **TIE** (measurement failure) | **17** | 6.7% |

Within the ZERO family, separated by the judges' stated reasons where those permit:
**ZERO-marked 18, N/A-marked 2, INDISTINGUISHABLE 15.** Within TIE: **14 genuine `+` vs `-`
splits** and **3 direction-vs-ambiguous splits** (two-vote items, after a Llama parse
failure). The separation rule is a published keyword list in
`polarity/analyse_secondaries.py`; it is **post-hoc and single-rater**, written after the
reasons were read, and carries no verdict.

**This sharpens P1 rather than disturbing it.** The 20.6% AMBIGUOUS rate decomposes into
**13.9% genuine zero-family and 6.7% measurement failure**. A third of what the frozen
protocol recorded as a reading was not one.

### S2 — the primary statistic with ZERO as a fixed point, beside the pre-registered number

| | qualifying kinds | obs | p |
|---|---|---|---|
| **pre-registered primary** | 3 (Facts, Identity, Rules) | 0.122222 | 0.332 |
| **S2** (ZERO retained as a fixed point, TIE/N/A excluded) | 3 (Facts, Identity, Rules) | 0.122222 | 0.332 |

**S2 and the primary agree exactly — to machine precision — and they agree by construction,
not by luck.** The sign flip σ is `+ ↔ −` with `σ(0) = 0`. A fixed point cannot witness an
asymmetry of the thing that fixes it, so the zeros contribute no evidence to TVD(`+`,`-`);
TIE and N/A were already outside the comparison. The corrected treatment moves **0 items**
into or out of the signed groups: 200 signed items before, 200 after.

The consequence is worth stating plainly, because it is the one thing S2 settles:
**treating AMBIGUOUS as a real point cannot rescue P2's power.** The points it adds are
exactly the ones the sign flip cannot distinguish. The UNDERPOWERED verdict is robust to
A1's correction, and a polarity-balanced corpus remains the only route to an answer.

**Descriptive extra, beyond A1's letter and carrying no verdict:** the zeros *can* speak
through one channel — do zero-moves confuse differently from signed moves? Pooled over the
three kinds with ≥4 in both groups (Facts, Premises, Process; the bar was lowered from 8
because zeros are scarce, which is itself a post-hoc choice): **TVD 0.364 against a null mean
of 0.305, p = 0.145.** Not significant, tiny groups (4–5 zeros per kind), post-hoc bar. The
largest cell is Facts, whose 5 zero-moves read as Identity 2 / Facts 2 / Model 1 against 16
of 21 signed moves reading as Facts. Per discipline rule 6 that is a residual, and a residual
is never support.

### S3 — per-kind zero rate

| kind | n | zero family | (ZERO / N/A / indist.) | TIE | signed | zero rate | excl. ties |
|---|---|---|---|---|---|---|---|
| **Circumstances** | 20 | **17** | 17 / 0 / 0 | 2 | 1 | **85.0%** | **94.4%** |
| Process | 20 | 5 | 0 / 0 / 5 | 4 | 11 | 25.0% | 31.2% |
| Facts | 26 | 5 | 0 / 2 / 3 | 0 | 21 | 19.2% | 19.2% |
| Premises | 24 | 4 | 0 / 0 / 4 | 1 | 19 | 16.7% | 17.4% |
| Identity | 27 | 2 | 1 / 0 / 1 | 1 | 24 | 7.4% | 7.7% |
| Manner | 20 | 1 | 0 / 0 / 1 | 3 | 16 | 5.0% | 5.9% |
| Structure | 20 | 1 | 0 / 0 / 1 | 0 | 19 | 5.0% | 5.0% |
| Confidence | 20 | 0 | — | 0 | 20 | 0.0% | 0.0% |
| Model | 20 | 0 | — | 2 | 18 | 0.0% | 0.0% |
| Priorities | 20 | 0 | — | 3 | 17 | 0.0% | 0.0% |
| Rules | 35 | 0 | — | 1 | 34 | 0.0% | 0.0% |

**`Circumstances` is the only kind that is mostly ZERO**, and A1's finer split **corrects the
mechanism I gave in §4.** All 17 of its zero-family items are ZERO-marked and none is
N/A-marked: the judges do not say the specificity axis fails to apply — they say it applies
and the move along it is nil. *"Both office names are equally specific, so the change does not
alter specificity."* So the accurate statement is **not** "Circumstances has no axis" but
**"Circumstances changes sit at zero on their axis"**: they are lateral substitutions at
constant grain. §4's *verdict* stands as pre-registered (>50% AMBIGUOUS → named); §4's
*explanation* is superseded by this line.

`Process` is the other correction: its 45% ambiguity is **not** mostly zeros. Five zero-family
against four TIEs — nearly half of it was judges disagreeing about direction, i.e. the
measurement failure A1 identifies, not a property of the kind. All five of its zeros are
INDISTINGUISHABLE, so whether a re-ordering is a zero-move or an off-axis move is exactly the
question these reasons cannot settle.

### One conceptual line, stated as an observation and claimed no further

With ZERO measured as a populated point rather than a disposal bin, the sign flip on **moves**
is an involution **with fixed points**, and the fixed points are the zeros. That is the same
three-valued shape as the Frobenius–Schur indicator (+1 real / −1 pseudoreal / 0 not
self-dual) and the Altland–Zirnbauer slots (present +1 / present −1 / absent).
`N18_BRIDGE_NOTE.md` asserts, in its section now marked `[SUPERSEDED]`, that *"their
classifying data is two involutions with THREE states each … ours is two fit conditions with
TWO states each"*. **On this measurement that binary characterisation is wrong at the level of
MOVES**, whatever it does at the level of kinds and fit conditions, and the note should be
corrected there. Nothing further follows: that note's own CORRECTION section already reopened
the projective direction on independent group-cohomology grounds (the Klein four-group's
Schur multiplier), so this observation is not needed to reopen anything and is not offered as
support for anything. **The §5 fence applies to this paragraph in full.**

## §7 Deviations, all labelled, all pinned before scoring

Pinned in `polarity/EXECUTION_NOTE.md` before the panel was invoked (D1–D10 there):

1. **Span extraction (D1).** Longest-common-prefix/suffix decomposition on word tokens. All
   272 items yield a single non-degenerate span; **none dropped**. 88 items have 2–6
   *interleaved* word-level blocks inside that one span (re-orderings, unit factorings,
   formula rewrites); block count is reported as a diagnostic and **not** used as a drop rule,
   since dropping on it would delete most of Priorities, Process and Structure — whose axes
   are re-ordering axes by definition.
2. **Which kind frames the polarity question (D2).** The item's **authored target kind**, not
   the BASE panel modal. Framing the polarity prompt by the panel's read would entangle the
   new variable with P2's outcome variable.
3. **CONJ items (D3).** `kind_target` is the placeholder `"TEST"`; each item's own
   `author_note` reads "Deontic modal strength only", so their axis is `Rules`. A sensitivity
   excluding all CONJ items is reported in §2.
4. **P2 statistic (D5).** "Error distribution" is read as the prereg glosses it — *"which kind
   the panel read it as"* — i.e. the full confusion-matrix row. Pooling is the unweighted mean
   over qualifying kinds. Errors-only and n-weighted variants were pre-specified as
   sensitivities and are reported whatever they show.
5. **UNDERPOWERED clause (b) operationalised (D6)** as `sd(null) > 1 − mean(null)`. It did not
   fire; clause (a) did.
6. **P3 operationalisation (D7):** CMH + per-stratum Fisher + a stratified permutation test.
   All degenerate, for the reason given in §3.
7. **`Record` unscored (D10)**, with the P1 denominator consequence reported in §1.
8. **Spend:** $0.0608 panel + $0.0007 smoke = **$0.0615** against the $0.30 cap. No cap event.
   **Amendment A1's secondaries added no spend** — S1/S2/S3 are recomputations over judgments
   already on disk.
9. **A1's ZERO/N-A separation rule (§6)** is post-hoc and single-rater: a keyword list written
   after the reasons were read. It is published in `polarity/analyse_secondaries.py` so it can
   be attacked, and it carries no verdict. The `Facts`/`Premises`/`Process` bar of 4-per-group
   in §6's descriptive extra is likewise post-hoc, and labelled where it appears.

## §8 What to do next, if anything

The one actionable output: **P2 needs a polarity-balanced corpus.** Authoring ~10 items per
polarity per kind, for the kinds that have a working axis, is a small, well-specified job, and
it is the only way the primary question gets an answer. Two of the twelve kinds are excluded
from that build by this run's own findings — `Circumstances` (no axis: 95% AMBIGUOUS) and
`Record` (no row in the frozen table) — which means a signed taxonomy, if it exists, is at
most **ten** axes wide, not twelve. `Process` (45% AMBIGUOUS, below the naming threshold)
should be treated as at risk in that build, for the same substitution-vs-grain reason: a
re-ordering has no direction along "steps added / order made stricter".

Artifacts: `scratchpad/polarity/` — `scoring_corpus.jsonl` (272 with spans and BASE modals),
`polarity_judgments.jsonl` (756), `power.json` (written first, no p-value), `pvalues.json`,
`EXECUTION_NOTE.md`, `RESUME.md`.
