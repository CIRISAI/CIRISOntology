#!/usr/bin/env python3
"""Calibration 3 — LENGTH PREFERENCE: the padding text, the bar, and the verdict.

Implements `AMENDMENT_J2_LENGTH_GATE.md`. **No inference, no network, no randomness.**

Split out of `calib_length.py` (which collects) so that `judge.py` can import the VERDICT
without importing the collector — the collector imports `judge.ask`, so putting the scorer
there would make the interlock a cycle. Dependencies run one way:

    calib3.py  <-  calib_length.py  ->  judge.ask        (collection)
    calib3.py  <-  judge.require_calib3                  (admission interlock)

THE BAR, quoted from the amendment so the code cannot drift from what was staked:

    "A judge FAILS if it prefers the padded response significantly more often than chance
     -- two-sided binomial against 0.5, alpha = 0.05, n = 92."
    "A judge that prefers the intact one is penalising padding, which is desirable and passes."

So the criterion is DIRECTIONAL: significance alone is not failure, it must be significance
in the padded direction. The p-value reported is the two-sided one the amendment names; the
direction test is a separate conjunct, not a switch to a one-sided test, so no threshold is
loosened -- a judge above 0.5 fails at exactly the rate the amendment fixed (~0.60 at n=92).
The first implementation of this gate (2026-08-24, uncommitted) failed on |deviation| and so
disqualified `mistral-nemo:12b` at 0.272 for penalising padding, which the amendment says
passes. That is corrected here; see AMENDMENT_J2 section "What the gate measured".
"""
import json, os
from math import comb

# Sized so the median padded/intact char ratio lands near the MEASURED arm C/A ratio of
# 1.448 -- the gate must probe the regime the C-vs-A comparison actually rides on, not an
# arbitrary inflation. Achieved median across the 92 arm-A responses: 1.459.
PAD = (" It is worth noting that this particular change should be considered in its wider "
       "context before any firm conclusions are drawn.")

# Same seed discipline as judge.py. KNOWN DEGENERACY, disclosed rather than silently fixed:
# judge.py's calib_sens draws its per-item flip from Random(20260822) in the same order, so
# the padded response lands in exactly the slot calib_sens put the DEGRADED response in. A
# slot-locked judge therefore reads as the exact complement of its own sensitivity, and
# Calibration 3 tells you nothing new about it. The seed is kept because the five collected
# artifacts were produced under it and must stay reproducible from this file; the hazard is
# handled by REPORTING the per-slot breakdown, which makes a slot-locked judge visible. A
# pure slot lock cannot by itself fail the gate: the flip split is 42/50, so slot-locking
# alone yields 0.457 or 0.543, both far short of the ~0.60 the bar requires at n = 92.
SEED = 20260822
ALPHA = 0.05


def binom_two_sided(k, n, p=0.5):
    """Exact two-sided binomial p-value by the total-probability (Sterne) definition."""
    if n == 0:
        return 1.0
    probs = [comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(n + 1)]
    obs = probs[k]
    return min(1.0, sum(pr for pr in probs if pr <= obs * (1 + 1e-12)))


def score(rows):
    """Verdict from collected Calibration 3 judgments. Returns a dict; never raises on an
    empty or all-undecided file -- that is reported as n = 0 and FAILS CLOSED at the caller."""
    d = [r for r in rows if r.get("chose_padded") is not None]
    n = len(d)
    k = sum(bool(r["chose_padded"]) for r in d)
    rate = (k / n) if n else float("nan")
    p = binom_two_sided(k, n) if n else 1.0
    # per-slot breakdown: the disclosed-degeneracy diagnostic, always reported
    slots = {}
    for s in (1, 2):
        ds = [r for r in d if r.get("padded_slot") == s]
        slots[s] = (sum(bool(r["chose_padded"]) for r in ds), len(ds))
    slot1_pick = sum(r.get("pick") == "1" for r in d) / n if n else float("nan")
    fail = bool(n and rate > 0.5 and p < ALPHA)
    return {"n": n, "k": k, "rate": rate, "p": p, "fail": fail,
            "slots": slots, "slot1_pick_rate": slot1_pick,
            "verdict": "FAIL" if fail else "PASS"}


def tag_for(model):
    """Artifact tag from a model string. Deterministic and total: `gemma3:12b` -> `gemma3`,
    `llama3.1:8b` -> `llama31`, `mistral-nemo:12b` -> `mistral-nemo`."""
    return model.split(":")[0].replace(".", "")


def artifact_for(model, here=None):
    """Path of the Calibration 3 output for `model`, or None if it has never been run.
    Two accepted names: the one the five collected files already use, and the forward one."""
    here = here or os.path.dirname(os.path.abspath(__file__))
    t = tag_for(model)
    for name in (f"judge_soft92_{t}_calib_length.jsonl", f"calib3_{t}.jsonl"):
        p = os.path.join(here, name)
        if os.path.exists(p):
            return p
    return None


def verdict_for(model, here=None):
    """Scored verdict for `model`, or None if Calibration 3 has never been run for it.
    None is NOT a pass -- callers must fail closed on it."""
    p = artifact_for(model, here)
    if p is None:
        return None
    v = score([json.loads(l) for l in open(p)])
    v["artifact"] = p
    v["model"] = model
    return v


def format_verdict(v):
    s1k, s1n = v["slots"][1]
    s2k, s2n = v["slots"][2]
    lines = [f"LENGTH PREFERENCE: judge picked the PADDED response {v['rate']:.3f} "
             f"(n={v['n']}, two-sided p={v['p']:.4g})",
             f"  per slot (disclosed degeneracy diagnostic): padded-in-slot-1 "
             f"{(s1k/s1n if s1n else float('nan')):.3f} (n={s1n}), padded-in-slot-2 "
             f"{(s2k/s2n if s2n else float('nan')):.3f} (n={s2n}); "
             f"overall slot-1 pick rate {v['slot1_pick_rate']:.3f}"]
    if v["fail"]:
        lines.append("  -> FAILED - judge rewards length as such; DISQUALIFIED per AMENDMENT J2")
    elif v["n"] and v["rate"] < 0.5 and v["p"] < ALPHA:
        lines.append("  -> PASS - judge significantly prefers the INTACT response "
                     "(penalising padding passes, per the amendment); check the per-slot "
                     "line above before reading this as a preference about length")
    else:
        lines.append("  -> PASS - no significant preference for length that adds nothing")
    return "\n".join(lines)


if __name__ == "__main__":                      # score stored files, no inference
    import sys
    for a in sys.argv[1:]:
        v = score([json.loads(l) for l in open(a)])
        print(f"==== {a}")
        print(format_verdict(v))
