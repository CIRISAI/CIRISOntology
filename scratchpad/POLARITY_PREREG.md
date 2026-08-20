# Polarity pre-registration — FROZEN 2026-08-20, before any item is scored

The eleven kinds are AXES; every recorded change is a signed move along one. We have never
used the sign. This tests whether the sign is STRUCTURAL (the taxonomy behaves differently
in the two directions) or BOOKKEEPING (it does not).

Nothing here has been run. No polarity has been assigned to any item at freeze time.

## 1. What polarity means, defined per kind BEFORE scoring

Polarity is the direction of the change along its kind's axis, scored from (before, after)
by a rule fixed here. `+` and `-` are labels, not value judgments.

| kind | `+` means | `-` means |
|---|---|---|
| Rules | binding MORE (may->must, wider scope, added obligation) | binding LESS |
| Confidence | MORE certain (hedge removed, precision tightened) | LESS certain |
| Facts | value/claim INCREASED or added | DECREASED or removed |
| Priorities | the named item moves UP the order | moves DOWN |
| Process | steps ADDED or order made stricter | REMOVED or loosened |
| Premises | assumption made STRONGER/wider-scoped | weaker/narrower |
| Model | framework made MORE specific/constraining | less |
| Structure | encoding made MORE explicit/structured | less |
| Manner | register made MORE formal | less formal |
| Identity | reclassified to a WIDER/higher-status category | narrower/lower |
| Circumstances | instance made MORE specific | less specific |

**AMBIGUOUS is a permitted third value** and is scored, not forced. A kind whose polarity is
undefinable in a majority of its items is a FINDING ABOUT THAT KIND, reported as such.

## 2. Corpus and scorer

`plane_corpus/corpus_full.jsonl` (248 authored) + `part_d.jsonl` (12) + `conj_items.jsonl`
(12) = 272 items with before/after already recorded. Scoring is by LLM panel, BASE-style,
3 models, one question: the polarity of the single changed span per the table above, with
AMBIGUOUS allowed. Modal by plurality; ties -> AMBIGUOUS. Spend cap $0.30.

Kind labels for the analysis are the EXISTING BASE-condition panel modals already on disk —
not re-derived — so polarity is the only new variable.

## 3. Staked predictions and their meanings

**P1 — polarity is scoreable.** AMBIGUOUS modal on <= 25% of items overall.
- above 40% -> the construct is not well posed on this corpus; VOID, and the note says so.
- 25-40% -> scoreable but weak; results reported as exploratory only.

**P2 — THE PRIMARY: is the confusion matrix polarity-symmetric?** For each kind with >= 8
scoreable items in both polarities, compare the error distribution (which kind the panel
read it as) between `+` and `-` items. Statistic: total variation distance between the two
error distributions, pooled across kinds, against a label-permutation null (2,000
permutations of the polarity labels within kind).
- **p < 0.01 -> POLARITY IS STRUCTURAL.** The taxonomy behaves differently in the two
  directions; the sign is not bookkeeping. This is the result that licenses the loop/holonomy
  question and it is the ONLY outcome that does.
- p >= 0.01 with adequate power -> POLARITY IS BOOKKEEPING on this corpus. The sign records
  direction but carries no structural information the confusion matrix can see. The
  holonomy/phase direction loses its cheapest support and is reported as such.
- **UNDERPOWERED** (fewer than 4 kinds clear the 8-per-polarity bar, or the null's spread
  exceeds the observable range) -> no verdict either way, and no kill.

**P3 — the twins under sign.** Structure and Circumstances already behave differently
WITHOUT polarity (Structure->Manner 7 vs Circumstances->Manner 1). Staked: their asymmetry
is NOT explained by polarity imbalance — i.e. it survives conditioning on sign. If it
vanishes under conditioning, the measured twin-asymmetry was a polarity artifact, which
would retract a claim made in TWO_WAY_READING.md and must be reported at full volume.

**P4 — per-kind ambiguity.** Report each kind's AMBIGUOUS rate. Any kind above 50% is named
as a kind without a well-defined axis — a finding about the taxonomy, not the method.

## 4. VOIDs

- P1 above 40% AMBIGUOUS -> whole test VOID.
- Any judge model unavailable, or parse failure > 5% -> VOID (protocol must match the panel
  convention used for the kind labels).
- Fewer than 150 scoreable items -> VOID.

## 5. What this cannot do

It cannot establish a holonomy. A polarity-asymmetric confusion matrix would show the sign
carries structural information — a NECESSARY condition for the loop question to be
meaningful, not a sufficient one. No claim about phases, projective representations or the
tenfold way follows from any outcome here, and the results document must say so.

---

## AMENDMENT A1 — 2026-08-20, written BEFORE any result of this run was read

**The steward's objection: "isn't ambiguous just a 0?"** It exposes a defect in §1 of the
frozen text, and the defect is real: **AMBIGUOUS conflates three distinguishable things.**

1. **ZERO** — the change genuinely makes no net move along the axis (it moves both ways, or
   moves neither). That is a POINT ON THE SCALE: the signed value set is {+1, 0, -1}.
2. **N/A** — the kind's axis does not apply to this change at all. That is MISSING DATA.
3. **TIE** — the three judges split between `+` and `-`. That is MEASUREMENT FAILURE, not a
   value, and §2's "ties -> AMBIGUOUS" wrongly turned a disagreement into a reading.

Why it matters beyond tidiness: with ZERO as a real point, the sign flip (`+` <-> `-`) is an
INVOLUTION WITH FIXED POINTS, and the fixed points are the zeros. That is the same shape as
the Frobenius-Schur indicator (+1 real / -1 pseudoreal / 0 not-self-dual) and the
Altland-Zirnbauer slots (present-+1 / present--1 / absent). The N18 bridge note claims our
conditions are BINARY where physics' are TERNARY, and that this is why we get four classes
where they get ten. If polarity is genuinely ternary, that claim is wrong at the level of
MOVES even if it stands at the level of KINDS — and it must be corrected there either way.

**Disposition, chosen before reading any number.** The PRE-REGISTERED analysis stands as the
PRIMARY and is reported first, whatever it says: no result may be displaced by an analysis
chosen after the fact. The zero-treatment is added as a LABELLED SECONDARY:

- **S1** — separate the three cases from data already collected, without rescoring:
  item-modal AMBIGUOUS where judges AGREED on ambiguity = **ZERO**; items where judges split
  `+`/`-` = **TIE** (excluded as missing); N/A distinguished from ZERO by the judges' stated
  reasons where those permit, and reported as indistinguishable where they do not.
- **S2** — re-run the primary statistic with ZERO retained as a fixed point of the sign flip
  and TIE/N/A excluded, and report it BESIDE the pre-registered number, never in place of it.
- **S3** — report the zero rate per kind. A kind that is mostly ZERO is a kind whose changes
  do not move along its own axis, which is a finding about that kind.

If S2 and the primary disagree, the disagreement is the headline and neither is suppressed.
