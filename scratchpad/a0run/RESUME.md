# A0 RUN — RESUME

Run root: `/home/emoore/CIRISOntology/scratchpad/a0run/`
Prereg (GOVERNS): `/home/emoore/CIRISOntology/scratchpad/A0_PREREG.md` (FROZEN, §18)
Results target: `/home/emoore/CIRISOntology/scratchpad/A0_RESULTS.md`
Venv: `/home/emoore/CIRISOntology/scratchpad/temporal-share/qenv/bin/python`
Judge key: `/home/emoore/.deepinfra_key` — NEVER printed/logged/written.
Spend cap: HARD_CAP_USD = 8.00, ledger `out/spend_ledger.jsonl` (append-only, summed at process start).

## THE SEAL
`action_was_overridden` is SEALED for every OB-stage. `src/a0lib.py:load_traces()` strips the
column unless `allow_outcome=True`, which only analysis-stage scripts pass. Every OB stage
writes its done-marker in `markers/` BEFORE any analysis stage runs.

## Stage table (stage -> done-marker -> resume command)

| stage | what | marker | resume command |
|---|---|---|---|
| OB0 | provenance pins verified | `markers/OB0_pins.done` | `$PY src/ob0_pins.py` |
| OB1 | frames, clusters, discretizations, scrub, judge inputs | `markers/OB1_frames.done` | `$PY src/ob1_frames.py` |
| OB2 | MC2 dye test (120x3) + V1 | `markers/OB2_mc2.done` | `$PY src/ob2_mc2.py` |
| OB3 | MC1 lang check (150+50 x3) + V2 | `markers/OB3_mc1.done` | `$PY src/ob3_mc1.py` |
| OB4 | main judging pass (716x3) + V3/V4/V15 | `markers/OB4_panel.done` | `$PY src/ob4_panel.py` |
| OB5 | adversarial leak probe CALLS (716x3) | `markers/OB5_probe.done` | `$PY src/ob5_probe.py` |
| OB6 | diff-arm secondary (chain pairs) | `markers/OB6_diff.done` | `$PY src/ob6_diff.py` |
| AN1 | **OUTCOME OPENS** CP-FACT complete | `markers/AN1_cpfact.done` | `$PY src/an1_cpfact.py` |
| AN2 | column 1 (leak arm, V7/V7b/V6/V12, Delta+CI) | `markers/AN2_col1.done` | `$PY src/an2_col1.py` |
| AN3 | CP-KIND bands | `markers/AN3_cpkind.done` | `$PY src/an3_cpkind.py` |
| AN4 | tautology diagnostic (LAST) | `markers/AN4_taut.done` | `$PY src/an4_taut.py` |
| AN5 | verdict table + A0_RESULTS.md | `markers/AN5_results.done` | write-up |

`$PY` = `/home/emoore/CIRISOntology/scratchpad/temporal-share/qenv/bin/python`

## Rules for the resumer
1. Read this file first. Run the first stage whose marker is missing; markers are only
   written after the stage's outputs are fsynced.
2. Judge stages replay `out/judgments.jsonl` (append-only cache keyed by
   sha256(model||prompt)) and re-issue only missing keys. Safe to re-run any judge stage.
3. Long/judge stages run detached: `setsid nohup $PY src/X.py >> logs/X.log 2>&1 &`.
   Poll with `pgrep -f "[s]rc/X.py"` (self-excluding bracket pattern).
4. Deviations go to `AMENDMENTS.md` BEFORE the deviating computation runs, timestamped,
   append-only, never edited in place.
5. NO git operations anywhere in this campaign.

## STATUS LOG (append-only)
- 2026-08-20 — run dir created; RESUME.md written; sha256 pins verified against §2: all three MATCH.
- OB1 DONE. Every pinned count reproduces EXACTLY: frames 2148/1398/1885/1270/2662/1154,
  clusters 526/410/480/378/580, distinct normalised inputs 716/625/408, tiers 2148/1928/2389,
  language am566/es535/en477/zh337 + 233 unrecoverable, actions 1084/604/430 + 30 corrupted,
  dual-confirmed 1334 with 1334 agreements, cluster language/version purity 0 exceptions.
  ZERO mismatches.
- OB2 DONE. MC2/V1 PASS (macro-F1 0.412, depth/surface BA 0.694, DEEP sens 0.4125, surface 0.608)
  — but DEEP sensitivity and surface collapse each clear by about ONE ITEM. Marginal pass; §13.5
  says that weakness must propagate into everything downstream.
- OB3 DONE. MC1/V2 PASS: 136/150 = 90.7%, CP lower bound 0.858 > 0.80. zh leg 48/50.
- OB4 running (716x3 kind judgments).
- AMENDMENTS A0-NOTE-3 records an ANALYTIC PROOF, written before the chain runs, that N1c is
  degenerate by construction (every accepted move leaves the 3-way table unchanged). Its pinned
  NON-MIXING fallback (N2 + margin drift printed) is what the verdict uses.
- OB5 DONE (probe calls). OB6 DONE (diff arm; key-name bug `fires`->`fired` fixed and re-run).
- SEAL BROKEN after all six OB markers present. AN1 (CP-FACT) -> FOULED. AN2 (col 1) -> VOID.
  AN3 (CP-KIND) -> VOID. AN4 (tautology, last) -> AUC 0.916 < 0.98, changes nothing.
  AN5 -> §10.3 row 9 (any x FOULED): NO KILL, NO VERDICT on the applied branch.
- A0_RESULTS.md WRITTEN at /home/emoore/CIRISOntology/scratchpad/A0_RESULTS.md
- Spend $0.6507 of $8.00. No git operations performed.
- RUN COMPLETE.
