# POLARITY run — resume state

Governed by `/home/emoore/CIRISOntology/scratchpad/POLARITY_PREREG.md` (FROZEN).
Operationalisations pinned in `EXECUTION_NOTE.md` **before** any scoring.

Working dir: `/home/emoore/CIRISOntology/scratchpad/polarity/`

## Stages and done-markers

| stage | script | output | marker |
|---|---|---|---|
| 1 build corpus | `build_corpus.py` | `scoring_corpus.jsonl` (272 rows) | `DONE_build` |
| 2 smoke | `polarity_score.py --corpus smoke.jsonl` | `smoke_judgments.jsonl` (9) | `DONE_smoke` |
| 3 panel | `polarity_score.py` | `polarity_judgments.jsonl` (252×3 = 756) | `DONE_panel` |
| 4 power | `analyse_power.py` | `power.json`, `counts.json` — **NO p-value** | `DONE_power` |
| 5 p-value | `analyse_p.py` | `pvalues.json` — refuses to run without `power.json` | `DONE_p` |
| 6 write-up | (by hand) | `../POLARITY_RESULTS.md` | — |

Stage 3 is resumable: rerunning skips `(id, model)` pairs already on disk.
Stage 5 must not be run before stage 4's output has been read (prereg §3: the UNDERPOWERED
condition is evaluated BEFORE any p-value).

## Scope reminders

- 20 `Record` items are NOT scored — the frozen §1 table defines eleven axes and omits
  Record. See EXECUTION_NOTE D10. Scored corpus = 252.
- CONJ items (12) take axis `Rules` per their own `author_note`. Sensitivity without them
  is reported.
- Spend cap $0.30, enforced in the runner; per-run spend in `spend_this_run.json`.
- No git operations. No key printing.

## Log

- 2026-08-20: stages 1–2 complete. Stage 3 launched detached (`panel.log`).
- 2026-08-20: stage 3 complete (756 judgments, $0.0608). Stage 4 complete —
  UNDERPOWERED = true via clause (a), 3 qualifying kinds, written to `power.json`
  BEFORE any p-value existed. Stage 5 complete (`pvalues.json`). Stage 6 complete:
  `../POLARITY_RESULTS.md`. Total spend $0.0615 of $0.30. ALL STAGES DONE.
- 2026-08-20: AMENDMENT A1 secondaries S1/S2/S3 computed from judgments already on disk
  (`analyse_secondaries.py` -> `secondaries.json`). NO rescoring, NO new spend. S2 is
  numerically identical to the primary and identical BY CONSTRUCTION (zeros are fixed
  points of the sign flip). Written up as §6 of `../POLARITY_RESULTS.md`. Marker
  `DONE_secondaries`.
