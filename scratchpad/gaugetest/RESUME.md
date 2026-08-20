# GAUGE TEST — resume state

Working dir: `/home/emoore/CIRISOntology/scratchpad/gaugetest/`
Governing prereg: `/home/emoore/CIRISOntology/scratchpad/GAUGE_TEST_PREREG.md` (FROZEN).
Pinned operationalisations: `EXECUTION_NOTE.md` (written before any arm ran).

## Files

| file | what |
|---|---|
| `gauge_annotate.py` | panel runner; imports `plane_annotate.py` for everything except the offered label set; asserts arm A's prompt is byte-identical to the original BASE prompt |
| `run_all.sh` | drives arms A→B→C sequentially, 3 retries each, aborts on spend cap |
| `judgments_{A,B,C}.jsonl` | one row per (item, model); resumable — reruns skip rows already present |
| `DONE_{A,B,C}`, `DONE_ALL` | done markers (written only when every (item, model) cell is present) |
| `spend_{ARM}_{ts}.json` | spend booked by that run, read back by later arms for the cap |
| `originals.json` | original BASE modals + the frozen 212-item untouched population |
| `void.json` | the VOID determination — written BEFORE any verdict quantity |
| `gauge_results.json` | primary, secondary, sensitivities |
| `GAUGE_TEST_RESULTS.md` | ../GAUGE_TEST_RESULTS.md — the write-up |

## To resume

```
setsid nohup bash /home/emoore/CIRISOntology/scratchpad/gaugetest/run_all.sh \
  > /home/emoore/CIRISOntology/scratchpad/gaugetest/run_all.log 2>&1 &
```

Idempotent: completed arms are skipped, partial arms fill their gaps.

## Then

```
python3 /home/emoore/CIRISOntology/scratchpad/gaugetest/analyse_gauge.py
```

which writes `void.json` first and refuses to compute a verdict without it.

## State

- [x] prereg read, execution note pinned
- [x] prompt selfcheck passed (arm A byte-identical to original BASE)
- [x] originals computed from `plane_corpus/full_judgments.jsonl` (not re-derived)
- [ ] arm A
- [ ] arm B
- [ ] arm C
- [ ] analysis
