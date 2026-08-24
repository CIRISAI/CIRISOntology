#!/usr/bin/env python3
"""Faithfulness check for the re-reconstructed `Session::generate`.

The fired kill's responses were produced by a reconstruction of `Session::generate` that
was never committed and was subsequently lost. The rebuilt method is only trustworthy if it
reproduces those responses EXACTLY -- a plausible-but-different generator would silently
change what the K2 verdict was computed over.

Generation is greedy, hence deterministic, so byte equality is the right bar (and arm A was
already known to be byte-identical across the two original runs, 92/92).

Regenerate with:
  cd sim_engine/crates/h3ere2-eval && cargo build --release
  ./target/release/generate <Qwen3-0.6B-Q4_K_M.gguf> \
      scratchpad/h3ere2_eval/encoded_soft92.jsonl <out.jsonl> 5
then: verify_repro.py <out.jsonl> scratchpad/h3ere2_eval/responses_soft92.jsonl
"""
import json, sys, collections

new = [json.loads(l) for l in open(sys.argv[1])]
old = {(r["id"], r["arm"], r.get("scramble_id")): r
       for r in (json.loads(l) for l in open(sys.argv[2]))}
by = collections.defaultdict(lambda: [0, 0])
missing = bad = 0
for r in new:
    k = (r["id"], r["arm"], r.get("scramble_id"))
    if k not in old:
        missing += 1
        continue
    o = old[k]
    same = (r["response"] == o["response"] and r.get("path") == o.get("path")
            and r.get("gen_tokens") == o.get("gen_tokens"))
    by[r["arm"]][1] += 1
    by[r["arm"]][0] += same
    if not same:
        bad += 1
        if bad <= 3:
            print(f"MISMATCH {k}\n  old={o['response'][:160]!r}\n  new={r['response'][:160]!r}")
n = sum(v[1] for v in by.values())
m = sum(v[0] for v in by.values())
for arm in sorted(by):
    print(f"  arm {arm}: {by[arm][0]}/{by[arm][1]} identical")
print(f"TOTAL {m}/{n} identical (response + path + gen_tokens); missing from reference: {missing}")
print("FAITHFUL" if m == n and n and not missing else "NOT FAITHFUL")
