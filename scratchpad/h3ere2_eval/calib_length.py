#!/usr/bin/env python3
"""Calibration 3 — LENGTH PREFERENCE, collection driver. Implements AMENDMENT_J2_LENGTH_GATE.md.

Pairs each arm-A response against a PADDED variant of ITSELF: identical text plus a fixed,
neutral, on-topic sentence that adds no information about the change. Content therefore
differs only in length, so a judge that reliably prefers the padded response is rewarding
length as such.

Deliberately a SEPARATE script that imports `judge.py`'s `ask` rather than a new mode inside
it: judge.py is the sealed instrument the K2 verdict was produced with, and the request shape
must be byte-for-byte the same as the one used for the real pairs. Importing it guarantees
that.

The BAR, the padding text and the scoring live in `calib3.py`, which imports nothing and runs
no inference -- that is what lets `judge.py`'s admission interlock read the verdict without a
circular import. This file only collects.

Usage:
  calib_length.py <model> <responses.jsonl> <out.jsonl> [corpus.jsonl]   collect + score
  calib_length.py --score <out.jsonl> [<out.jsonl> ...]                  score only, no inference
"""
import json, os, random, sys, statistics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from judge import ask, load_items, load_resp          # sealed request shape, reused verbatim
from calib3 import PAD, SEED, score, format_verdict   # the staked bar, one definition only


def main():
    if sys.argv[1] in ("--score", "score"):
        for a in sys.argv[2:]:
            print(f"==== {a}")
            print(format_verdict(score([json.loads(l) for l in open(a)])))
        return

    model, respfile, out = sys.argv[1], sys.argv[2], sys.argv[3]
    corpus = sys.argv[4] if len(sys.argv) > 4 else None
    items, R = load_items(corpus), load_resp(respfile)
    rng = random.Random(SEED)                          # same seed discipline as judge.py
    rows, ratios = [], []

    for iid in sorted(R):
        a = R[iid].get("A")
        if not a:
            continue
        full = a["response"]
        padded = full.rstrip() + PAD
        ratios.append(len(padded) / len(full))
        flip = rng.random() < 0.5                      # randomise which slot is padded
        r1, r2 = (padded, full) if flip else (full, padded)
        pick = ask(model, items[iid], r1, r2)
        chose_padded = None
        if pick in ("1", "2"):
            chose_padded = (pick == "1") if flip else (pick == "2")
        # `model` added 2026-08-24 so the artifact names its own judge. The five files
        # collected before that lack the field; they are resolved by filename instead
        # (calib3.artifact_for), and nothing reads this field for the verdict.
        rows.append({"id": iid, "mode": "calib_length", "model": model, "pick": pick,
                     "padded_slot": 1 if flip else 2, "chose_padded": chose_padded,
                     "len_intact": len(full), "len_padded": len(padded)})

    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    print(f"wrote {len(rows)} judgments -> {out}")
    print(f"  pad chars={len(PAD)}  median padded/intact ratio={statistics.median(ratios):.3f} "
          f"(measured arm C/A ratio = 1.448)")
    print(format_verdict(score(rows)))


if __name__ == "__main__":
    main()
