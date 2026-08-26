"""Gate the COMPOSED artifact: 4-bit MatMuls AND a 4-bit embedding, on fine-tuned weights.

The 346.1 MB file on disk was built from the BASE q4f16 export, so it cannot be gated
against a fine-tuned reference -- it would measure fine-tuning, not quantisation. The
fine-tune moves the weights by only 0.182% relative RMS but is worth +46 accuracy
points, so base weights are not a stand-in. This reconstructs the same composition on
`ft_merged` instead.

  REF  ft_merged untouched                  (0.7717; validated 92/92 vs model-scout's ONNX run)
  M    all 196 linear weights 4-bit         CONTROL -- must reproduce their q4f16 (0.5761 / 0.7174)
  C    M plus the embedding 4-bit           the composed artifact

Quantisation matches what the ONNX export actually stores, read off its own tensors:
symmetric uint4, implicit zero point 8, blocks of 32 along the INPUT dimension, f16
scales. The embedding round-trip was separately verified BIT-FOR-BIT against the
346 MB artifact's stored weights and scales.

Arm M is a control, not decoration: if it does not land near model-scout's independently
measured q4f16 then my round-to-nearest scheme is not the one their exporter used, and
arm C is not interpretable. Reported either way.
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


def round_trip(t, block=BLOCK):
    """Symmetric uint4, implicit zero point 8, blocks along the LAST dim of a [out, in]
    weight -- which is the input dimension, matching MatMulNBits' [N, k_blocks, blob]."""
    w = t.detach().to(torch.float32).numpy()
    R, D = w.shape
    if D % block:
        return None
    NB = D // block
    out = np.empty_like(w)
    for s0 in range(0, R, 16384):
        s1 = min(s0 + 16384, R)
        blk = w[s0:s1].reshape(-1, NB, block)
        scale = np.maximum(np.abs(blk.min(2)) / ZP, blk.max(2) / (ZP - 1))
        scale[scale == 0] = np.float32(6.0e-8)
        s16 = scale.astype(np.float16); s16[s16 == 0] = np.float16(6.0e-8)
        s = s16.astype(np.float32)
        q = np.clip(np.rint(blk / s[:, :, None]) + ZP, 0, 15)
        out[s0:s1] = ((q - ZP) * s[:, :, None]).reshape(s1 - s0, D)
    return torch.from_numpy(out)


tok = AutoTokenizer.from_pretrained(FT)
LAB_IDS = {l: tok(l, add_special_tokens=False)["input_ids"] for l in LABELS}
print("loading ft_merged...", flush=True)
model = AutoModelForCausalLM.from_pretrained(FT, dtype=torch.float32).eval()

# The 196 MatMulNBits nodes are the 7 projections x 28 layers.
PROJ = ("q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj")
linears = [(n, m) for n, m in model.named_modules()
           if isinstance(m, torch.nn.Linear) and any(p in n for p in PROJ)]
print(f"linear weights to quantise: {len(linears)}", flush=True)
orig_lin = {n: m.weight.detach().clone() for n, m in linears}
emb = model.get_input_embeddings().weight
orig_emb = emb.detach().clone()


def score(o):
    msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": pf(o)}]
    text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                   enable_thinking=False) + '{"family": "'
    ids = torch.tensor([tok(text, add_special_tokens=False)["input_ids"]])
    with torch.no_grad():
        lg = model(ids).logits[0, -1]
    lp = torch.log_softmax(lg.double(), -1)
    return np.array([float(lp[LAB_IDS[l][0]]) for l in LABELS])


items = [json.loads(l) for l in open(f"{EVAL}/test_split.jsonl")]
kept = [o for o in items if o["kind_target"] in K2B]
gold = [SURF[K2B[o["kind_target"]]] for o in kept]
n = len(kept)
res = {}

for arm in ("REF", "M", "C"):
    with torch.no_grad():
        if arm == "REF":
            pass
        elif arm == "M":
            emb.copy_(orig_emb)
            done = 0
            for name, mod in linears:
                rt = round_trip(orig_lin[name])
                if rt is not None:
                    mod.weight.copy_(rt); done += 1
            print(f"  quantised {done}/{len(linears)} linear weights", flush=True)
        else:
            emb.copy_(round_trip(orig_emb))
            print("  plus the embedding", flush=True)
    vals, t0 = [], time.time()
    for i, o in enumerate(kept, 1):
        vals.append(score(o))
        if i % 30 == 0:
            print(f"  {arm} {i}/{n}  {time.time()-t0:.0f}s", flush=True)
    res[arm] = np.array(vals)
    print(f"  {arm} done", flush=True)

json.dump({k: v.tolist() for k, v in res.items()}, open("composed_gate.json", "w"))
pick = {k: [LABELS[int(x.argmax())] for x in v] for k, v in res.items()}
acc = {k: sum(p == g for p, g in zip(v, gold)) / n for k, v in pick.items()}
from collections import Counter

print("\n" + "=" * 74)
print(f"COMPOSED GATE -- {n} frozen items, one fixed ft_merged weight set")
print(f"{'arm':<40} {'accuracy':>9} {'agree vs REF':>13}")
for k, lab in (("REF", "REF  untouched"), ("M", "M    all matmuls 4-bit"),
               ("C", "C    matmuls + embedding 4-bit")):
    ag = sum(a == b for a, b in zip(pick[k], pick["REF"])) / n
    print(f"{lab:<40} {acc[k]:>9.4f} {ag:>13.4f}")
print(f"\n  model-scout's independently measured q4f16:  0.5761      0.7174   <- control target for M")
print(f"\n  marginal cost of the embedding (C vs M): agreement "
      f"{sum(a==b for a,b in zip(pick['C'],pick['M']))/n:.4f}, "
      f"accuracy change {acc['C']-acc['M']:+.4f}")
for k in ("REF", "M", "C"):
    print(f"  {k} labels: {dict(Counter(pick[k]))}")
d = np.abs(res["C"] - res["REF"])
flips = sum(a != b for a, b in zip(pick["C"], pick["REF"]))
print(f"\n  A3 instruments for C vs REF: agreement "
      f"{1-flips/n:.4f} ({n-flips}/{n}), accuracy gap {abs(acc['C']-acc['REF']):.4f}, "
      f"mean |dlogprob| {d.mean():.4f}, flips {flips}")
verdict = ("EQUIVALENT" if (1-flips/n >= 0.95 and abs(acc['C']-acc['REF']) <= 0.03 and d.mean() <= 0.05)
           else "NOT EQUIVALENT" if (1-flips/n < 0.90 or abs(acc['C']-acc['REF']) > 0.06)
           else "INCONCLUSIVE AT THIS N")
print(f"  pre-registered verdict for the composed artifact: {verdict}")
