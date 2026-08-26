"""ADDENDUM A2's MANDATORY CONTROL, applied to my own harness before I trust its verdict.

A2 requires the transformers-side harness to land within +/-0.08 of the ollama figure
0.467, i.e. in [0.387, 0.547], or "the two harnesses do not measure the same thing and
the comparison is reported as invalid rather than explained away."

My first harness put the unquantised reference at 0.2935 -- outside the band. The
prompt is NOT malformed (chat template applied, `<|im_start|>` present, empty think
block as ollama's think:false produces, and 0.99+ of the next-token mass sits on the
four label tokens). So the gap is in how the answer is ELICITED, not in the prompt.

This sweeps the elicitation choices against the reference model only. Whichever
variant lands in the band is the one the A/B gate should be re-run on; if none does,
the task-level result stays labelled invalid.
"""
import json, sys, time
import numpy as np, torch
from transformers import AutoTokenizer, AutoModelForCausalLM

EVAL = "/home/emoore/CIRISOntology/scratchpad/nl_bridge_eval"
TOK = "/home/emoore/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca"
M = json.load(open(f"{EVAL}/surface_map.json")); K2B, SURF = M["kind2block"], M["surface_plain"]
LABELS = ["Facts", "Rules", "Identity", "Manner"]
FT = {"Facts": 37, "Rules": 26008, "Identity": 18558, "Manner": 44}
FAM = [("Facts", "the assertive family: what is claimed, how strongly, under what rule, on what premise"),
       ("Rules", "the directive family: what is required, in what preference order, in what step order"),
       ("Identity", "the declarative family: what counts as what"),
       ("Manner", "the force-neutral carrier family: how it is encoded, how it is presented or registered, which instance it is")]
SYS = ("You classify what FAMILY of change was made to a document. "
       "Answer with exactly one label from this list:\n"
       + "\n".join(f"- {n}: {g}" for n, g in FAM)
       + "\nPick the single family the change belongs to.")


def trunc(s, n=1400):
    s = s or ""
    return s if len(s) <= n else s[:n] + "\n[...truncated]"


def pf(o):
    return (f"BEFORE:\n{trunc(o['before'])}\n\nAFTER:\n{trunc(o['after'])}\n\n"
            f"WHAT CHANGED: {o.get('variation_site','')}\n\nWhich family of change is this?")


tok = AutoTokenizer.from_pretrained(TOK)
print("loading reference...", flush=True)
ref = AutoModelForCausalLM.from_pretrained(TOK, dtype=torch.float32).eval()

VARIANTS = [
    ("A json prefix, space   (current)", '{"family": "', False),
    ("B json prefix, no space",          '{"family":"',  False),
    ("C no prefix, free answer",         '',             False),
    ("D no prefix, thinking enabled",    '',             True),
]

items = [json.loads(l) for l in open(f"{EVAL}/test_split.jsonl")]
kept = [o for o in items if o["kind_target"] in K2B]
print(f"{len(kept)} items; control band for the reference is [0.387, 0.547]\n", flush=True)

results = {}
for tag, suffix, think in VARIANTS:
    t0 = time.time(); correct = 0; picks = []
    for o in kept:
        msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": pf(o)}]
        text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                       enable_thinking=think) + suffix
        ids = torch.tensor([tok(text, add_special_tokens=False)["input_ids"]])
        with torch.no_grad():
            lg = ref(ids).logits[0, -1]
        pick = max(LABELS, key=lambda l: float(lg[FT[l]]))
        picks.append(pick)
        correct += pick == SURF[K2B[o["kind_target"]]]
    acc = correct / len(kept)
    band = "IN BAND" if 0.387 <= acc <= 0.547 else "out of band"
    from collections import Counter
    print(f"{tag:34} acc={acc:.4f} ({correct}/{len(kept)})  {band:12} "
          f"{dict(Counter(picks))}  {time.time()-t0:.0f}s", flush=True)
    results[tag] = dict(acc=acc, picks=picks)
json.dump(results, open("variant_sweep.json", "w"))
