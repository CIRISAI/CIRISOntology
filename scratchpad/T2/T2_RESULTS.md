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
