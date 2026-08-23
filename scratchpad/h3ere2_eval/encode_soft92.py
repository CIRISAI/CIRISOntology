#!/usr/bin/env python3
"""h3ere2 stage 1 for the A1.2/A2 runs: the fp32 4-way classifier over the 92-item
frozen test split, computing the FULL 4-way softmax (A2's seeding input), not just the
argmax or the decision-point pair.

Protocol identical to softmax_entropy.py / encode_wild.py: same system prompt, same chat
template, same ' "{label}"' continuations, sequence logprob summed over each label's
tokens (the full-distribution method A2's viability check used). Corpus is
test_split.jsonl minus the 8 testimonial (Record) items -- the same 92 items every
pred4_* instrument used. Gold surface comes from surface_map.json (Lean-derived).

Deterministic; the output is a pipeline stage boundary.
"""
import json, os, sys, time, math, collections
import numpy as np, onnxruntime as ort
from transformers import AutoTokenizer

HERE = os.path.dirname(os.path.abspath(__file__))
NL = os.path.expanduser("~/CIRISOntology/scratchpad/nl_bridge_eval")
LABELS = ["Facts", "Rules", "Identity", "Manner"]
FAM = [("Facts","the assertive family: what is claimed, how strongly, under what rule, on what premise"),
       ("Rules","the directive family: what is required, in what preference order, in what step order"),
       ("Identity","the declarative family: what counts as what"),
       ("Manner","the force-neutral carrier family: how it is encoded, how it is presented or registered, which instance it is")]
SYS = ("You classify what FAMILY of change was made to a document. "
       "Answer with exactly one label from this list:\n"
       + "\n".join(f"- {n}: {g}" for n,g in FAM) + "\nPick the single family the change belongs to.")
JSON_OPEN = '{"family":'

def trunc(s, n=1400):
    s = s or ""; return s if len(s) <= n else s[:n] + "\n[...truncated]"
def um(o):
    return (f"BEFORE:\n{trunc(o['before'])}\n\nAFTER:\n{trunc(o['after'])}\n\n"
            f"WHAT CHANGED: {o.get('variation_site','')}\n\nWhich family of change is this?")

def main(model_path):
    M = json.load(open(f"{NL}/surface_map.json"))
    K2B, SURF = M["kind2block"], M["surface_plain"]
    tok = AutoTokenizer.from_pretrained(f"{NL}/onnx_fp32")
    so = ort.SessionOptions(); so.log_severity_level = 3
    s = ort.InferenceSession(model_path, so, providers=["CPUExecutionProvider"])
    opts = {l: tok(f' "{l}"', add_special_tokens=False).input_ids for l in LABELS}
    items = [o for o in (json.loads(l) for l in open(f"{NL}/test_split.jsonl"))
             if o["kind_target"] in K2B]
    print(f"  {len(items)} items (test_split minus testimonial)", flush=True)
    rows = []; t0 = time.time()
    for i, o in enumerate(items, 1):
        msgs = [{"role":"system","content":SYS},{"role":"user","content":um(o)}]
        pre = tok(tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                  enable_thinking=False) + JSON_OPEN).input_ids
        tot = {}
        for l, lid in opts.items():
            ids = pre + lid; n = len(ids)
            lg = s.run(["logits"], {"input_ids": np.array([ids], dtype=np.int64),
                "attention_mask": np.ones((1, n), dtype=np.int64),
                "position_ids": np.arange(n, dtype=np.int64)[None, :]})[0][0]
            lp = 0.0
            for k, t in enumerate(lid):
                row = lg[len(pre) - 1 + k].astype(np.float64)
                row = row - row.max(); lp += float(row[t] - np.log(np.exp(row).sum()))
            tot[l] = lp
        v = np.array([tot[l] for l in LABELS]); v = v - v.max()
        p = np.exp(v); p = p / p.sum()
        H = float(-(p * np.log(p + 1e-300)).sum())
        rows.append({"id": o["id"], "stream": o.get("domain"),
                     "surface": LABELS[int(p.argmax())],
                     "gold_surface": SURF[K2B[o["kind_target"]]],
                     "probs": {l: float(x) for l, x in zip(LABELS, p)},
                     "seq_logprobs": tot, "entropy": H, "pmax": float(p.max()),
                     "before": o.get("before",""), "after": o.get("after",""),
                     "variation_site": o.get("variation_site","")})
        if i % 25 == 0: print(f"  {i}/{len(items)} {time.time()-t0:.0f}s", flush=True)

    with open(f"{HERE}/encoded_soft92.jsonl", "w") as f:
        for r in rows: f.write(json.dumps(r) + "\n")
    # the gold-hard (A1.2) encoding is the same rows with surface := gold
    with open(f"{HERE}/encoded_gold92.jsonl", "w") as f:
        for r in rows:
            g = dict(r); g["surface"] = r["gold_surface"]; g.pop("probs")
            f.write(json.dumps(g) + "\n")

    pm = np.array([r["pmax"] for r in rows]); H = np.array([r["entropy"] for r in rows])
    print(f"\nN={len(rows)}   max entropy possible = ln4 = {math.log(4):.3f}")
    print(f"  entropy   mean={H.mean():.3f} median={np.median(H):.3f} min={H.min():.3f} max={H.max():.3f}")
    print(f"  p(max)    mean={pm.mean():.3f} median={np.median(pm):.3f}")
    for thr in (0.99, 0.95, 0.90, 0.80):
        print(f"  items with p(max) >= {thr}: {int((pm>=thr).sum()):3d}/{len(rows)} = {(pm>=thr).mean():.1%}")
    print(f"  items with entropy < 0.10 (effectively one-hot): {(H<0.10).sum()}/{len(rows)} = {(H<0.10).mean():.1%}")
    print("  argmax spread:", dict(collections.Counter(r["surface"] for r in rows)))
    print("  gold spread:  ", dict(collections.Counter(r["gold_surface"] for r in rows)))
    agree = sum(r["surface"] == r["gold_surface"] for r in rows)
    print(f"  argmax==gold: {agree}/{len(rows)} = {agree/len(rows):.3f}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else f"{NL}/onnx_fp32/model.onnx")
