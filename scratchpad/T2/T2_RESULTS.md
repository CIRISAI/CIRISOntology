# T2 — THE DIT++/ISO MAPPING: VOID, INSTRUMENT NOT ACHIEVED (2026-08-20)

Two runs, both below the frozen κ=0.4 floor. Per [D] §T2.5's VOID band and A4's pinned
constraint, T2 delivers NO VERDICT in any direction, and no further instrument repair is
permitted without steward review.

| run | question | κ (Fleiss, 17 items, 3 families) | D | verdict |
|---|---|---|---|---|
| 1 | frozen §T2.2 wording | −0.0698 | 0 | VOID (construal defect: all three families classified edits to the standard's definitions — A4, with quoted evidence) |
| 2 | A4-repaired wording | **0.3805** | 1 | **VOID — 0.02 under the floor** |

## Observations on a void instrument (reported as such; NOT findings; no prediction is
scored, per the frozen band "no verdict in any direction")

- The repair moved κ by +0.45: the construal diagnosis was right, and the instrument
  NEARLY achieved. The residual disagreement concentrates on the feedback/communication-
  management items, split between Record and Manner.
- On the void run, Auto-Feedback went 3/3 to Record (information about the speaker's own
  processing of PRIOR utterances), and Record is modal on 7 of 17 items. Had the run been
  valid, P2.2 ("nothing in ISO maps to Record") would have been under direct pressure —
  recorded so a future valid instrument knows where to look. The SURVIVES-OUTSIDE field
  (the A2 MAJOR-4 criterion) was unanimous-YES on NOTHING, so the RECORD-ANALOGUE band's
  own trigger never fired even on the void data: kind-votes for Record and the frame-
  relation criterion dissociate, which is itself worth a future design's attention.
- All three ISO structural devices (functional dependence, feedback dependence, rhetorical
  relations) went 3/3 Structure; sentiment went 3/3 Manner; certainty went 2/3 Confidence
  (Llama-4: Record) — the P2.1 convergence was one vote short of unanimity on a void run.
- One off-vocabulary answer in run 1 ("Scope", gemma) recorded as PARSE-FAIL.

## Costs and artifacts

102 mapping calls total (~$0.02). Raw: t2_raw.json (run 1), t2_raw_run2.json (run 2);
scored: t2_scored.json, t2_scored_run2.json; scripts committed beside them. Instrument
notes: gpt-oss reasoning-token truncation at max_tokens=600, repaired at 2500 (A4).

## Status

T2 = VOID — INSTRUMENT NOT ACHIEVED. The frozen order proceeds to T3+T4. Steward review
requested on whether a third T2 instrument (different design, not a wording tweak — e.g.
concrete change-vignettes per ISO item instead of definition-level mapping) is authorized
as a numbered amendment, or T2 closes VOID for this registration.

# RUN 3 (A5 vignette instrument): VALID, and the verdict is WEAK / DIVERGENT

κ = 0.4725 (> 0.4): the instrument ACHIEVED on the third design. D = 1 of 9. Frozen band:
**WEAK / DIVERGENT — the two taxonomies are about different objects; the DIT++ threat to
the novelty framing shrinks, and so does the corroboration, in the same sentence.**

Predictions, scored on the valid run:
- P2.1 certainty → Confidence unanimously: **FAILED as staked** (one vignette 3/3
  Confidence, the other not unanimous — the signal exists, the unanimity bar was not met).
- P2.2 nothing maps to Record: **HOLDS** (no item determinate on Record; two single
  vignettes hit 3/3 Record but their pairs did not — counts to nothing by A5's rule).
- P2.3 Task indeterminate: **HIT**. P2.6 Social Obligations → Manner: **HIT, determinate**.
- P2.8 sentiment → NO-FIT: **MISSED, cleanly** — both vignettes 3/3 **Manner**. The panel
  says affect-qualification is Manner traffic, against our stake. Reported at full volume.
- P2.4/P2.5/P2.7: not cleanly scorable at D=1 (indeterminate is neither prong); per-item
  table stands as the record.
- RECORD-ANALOGUE trigger: never fired (no dual 3/3 SURVIVES-OUTSIDE). CLUSTERED NO-FIT:
  no determinate NO-FIT anywhere — no candidate missing kind from this leg.
- Determinate cluster worth one sentence: Social Obligations, Contact Management and the
  sentiment qualifier all land Manner — the dialogue standard's social/phatic layer reads
  as our Manner, and nothing else crosses cleanly. The kinds and ISO's dimensions carve
  different objects; where they touch, they touch at Manner.

T2 CLOSES: valid instrument, WEAK/DIVERGENT, P2.2 holds, P2.8 dies, K3/K3b do not fire.
