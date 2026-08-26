"""ADDENDUM A3's gate, run on the FINE-TUNED weights -- the model that actually ships.

Design, per the team lead's constraint: ONE fixed set of merged weights (ft_merged),
quantised two ways. Seed variance changes 41.3% of test answers between fine-tune
runs, so two separately-trained checkpoints would swamp the embedding effect;
quantisation is deterministic, so a within-weights comparison cancels it exactly.

  A = ft_merged, untouched
  B = ft_merged with `model.embed_tokens.weight` replaced by its 4-bit
      quantise/dequantise round-trip -- symmetric, blocks of 32, f16 scales.

That round-trip was verified to reproduce the 346 MB ONNX artifact's stored weights
and scales BIT-FOR-BIT, so this is the shipped transform's exact numerical content.
`tie_word_embeddings` is true, so it perturbs the lm_head too, as it does in ONNX.

Two scorings are reported because the programme has used both:
  * first-token argmax over the four labels -- what greedy grammar-constrained
    decoding emits (the four labels have distinct first tokens);
  * mean logprob of the full label string -- A2's "constrained argmax over the four
    label strings", scored from a shared KV cache of the prompt.
"""
import json, sys, time
import numpy as np, torch
from transformers import AutoTokenizer, AutoModelForCausalLM

EVAL = "/home/emoore/CIRISOntology/scratchpad/nl_bridge_eval"
FT = f"{EVAL}/ft_merged"
BLOCK, ZP = 32, 8
LABELS = ["Facts", "Rules", "Identity", "Manner"]

M = json.load(open(f"{EVAL}/surface_map.json")); K2B, SURF = M["kind2block"], M["surface_plain"]
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


tok = AutoTokenizer.from_pretrained(FT)
LAB_IDS = {l: tok(l, add_special_tokens=False)["input_ids"] for l in LABELS}
print("label token ids:", LAB_IDS, flush=True)

print("loading fine-tuned weights (arm A)...", flush=True)
model = AutoModelForCausalLM.from_pretrained(FT, dtype=torch.float32).eval()
emb = model.get_input_embeddings().weight
orig = emb.detach().clone()


def round_trip(t):
    """The shipped transform's exact numerical content, verified bit-identical to the
    346 MB artifact's stored weights and scales."""
    w = t.detach().to(torch.float32).numpy()
    V, D = w.shape
    NB = D // BLOCK
    out = np.empty_like(w)
    for s0 in range(0, V, 16384):
        s1 = min(s0 + 16384, V)
        blk = w[s0:s1].reshape(-1, NB, BLOCK)
        scale = np.maximum(np.abs(blk.min(2)) / ZP, blk.max(2) / (ZP - 1))
        scale[scale == 0] = np.float32(6.0e-8)
        s16 = scale.astype(np.float16); s16[s16 == 0] = np.float16(6.0e-8)
        s = s16.astype(np.float32)
        q = np.clip(np.rint(blk / s[:, :, None]) + ZP, 0, 15)
        out[s0:s1] = ((q - ZP) * s[:, :, None]).reshape(s1 - s0, D)
    return torch.from_numpy(out)


def score(o):
    """Returns (first-token logits over the 4 labels, mean logprob of each label)."""
    msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": pf(o)}]
    text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                  enable_thinking=False) + '{"family": "'
    ids = torch.tensor([tok(text, add_special_tokens=False)["input_ids"]])
    with torch.no_grad():
        out = model(ids, use_cache=True)
    first = torch.log_softmax(out.logits[0, -1].double(), -1)
    ft_logit = np.array([float(first[LAB_IDS[l][0]]) for l in LABELS])
    means = []
    for l in LABELS:
        toks = LAB_IDS[l]
        lp = float(first[toks[0]])
        if len(toks) > 1:
            with torch.no_grad():
                o2 = model(torch.tensor([[toks[0]]]), past_key_values=out.past_key_values,
                           use_cache=False)
            lp += float(torch.log_softmax(o2.logits[0, -1].double(), -1)[toks[1]])
        means.append(lp / len(toks))
    return ft_logit, np.array(means)


items = [json.loads(l) for l in open(f"{EVAL}/test_split.jsonl")]
kept = [o for o in items if o["kind_target"] in K2B]
print(f"{len(kept)} items\n", flush=True)

res = {}
for arm in ("A", "B"):
    if arm == "B":
        print("quantising the tied embedding table (arm B)...", flush=True)
        with torch.no_grad():
            emb.copy_(round_trip(orig))
        rel = float(((emb - orig) ** 2).sum().sqrt() / (orig ** 2).sum().sqrt())
        print(f"  table relative RMS perturbation: {rel:.4%}", flush=True)
    ft_l, mean_l, t0 = [], [], time.time()
    for i, o in enumerate(kept, 1):
        a, b = score(o)
        ft_l.append(a); mean_l.append(b)
        if i % 25 == 0:
            print(f"  {arm} {i}/{len(kept)}  {time.time()-t0:.0f}s", flush=True)
    res[arm] = (np.array(ft_l), np.array(mean_l))

gold = [SURF[K2B[o["kind_target"]]] for o in kept]
n = len(kept)
json.dump({k: [v[0].tolist(), v[1].tolist()] for k, v in res.items()},
          open("ft_gate.json", "w"))


def report(name, ia, ib):
    pa = [LABELS[int(x.argmax())] for x in ia]
    pb = [LABELS[int(x.argmax())] for x in ib]
    acc_a = sum(p == g for p, g in zip(pa, gold)) / n
    acc_b = sum(p == g for p, g in zip(pb, gold)) / n
    agree = sum(x == y for x, y in zip(pa, pb)) / n
    d = np.abs(ia - ib)
    flips = np.array([x != y for x, y in zip(pa, pb)])
    marg = np.sort(ia, axis=1)[:, -1] - np.sort(ia, axis=1)[:, -2]
    from collections import Counter
    print(f"\n--- scoring: {name} ---")
    print(f"  accuracy   A {acc_a:.4f}   B {acc_b:.4f}   gap {abs(acc_a-acc_b):.4f}"
          f"    criterion: gap <= 0.03")
    print(f"  labels     A {dict(Counter(pa))}")
    print(f"             B {dict(Counter(pb))}")
    print(f"  1. prediction agreement      {agree:.4f} ({sum(x==y for x,y in zip(pa,pb))}/{n})"
          f"   criterion: >= 0.95 equiv, < 0.90 NOT")
    print(f"  3. mean per-item |dlogprob|  {d.mean():.4f}   max {d.max():.4f}"
          f"   criterion: mean <= 0.05")
    print(f"     argmax flips              {int(flips.sum())} of {n}"
          + (f", of which {int(((marg>0.5)&flips).sum())} had A margin > 0.5" if flips.any() else ""))
    verdict = ("EQUIVALENT" if (agree >= 0.95 and abs(acc_a-acc_b) <= 0.03 and d.mean() <= 0.05)
               else "NOT EQUIVALENT" if (agree < 0.90 or abs(acc_a-acc_b) > 0.06)
               else "INCONCLUSIVE AT THIS N")
    print(f"  pre-registered verdict: {verdict}")


report("first-token argmax (greedy constrained decoding)", res["A"][0], res["B"][0])
report("mean logprob of full label string (A2's scoring)", res["A"][1], res["B"][1])
