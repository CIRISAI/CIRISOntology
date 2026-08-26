#!/usr/bin/env python3
"""Qwen3-0.6B 4-way surface LoRA fine-tune + constrained-argmax scorer.
Scoring = argmax over the 4 label continuations == masked decoding."""
import json, sys, os, random, collections
SEED = int(os.environ.get('FT_SEED', '20260822'))
SAVE = os.environ.get('FT_SAVE', '1') == '1'
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

BASE = "Qwen/Qwen3-0.6B"
HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(f"{HERE}/surface_map.json"))
K2B, SURF = M["kind2block"], M["surface_plain"]
LABELS = ["Facts", "Rules", "Identity", "Manner"]

FAM = [
    ("Facts",    "the assertive family: what is claimed, how strongly, under what rule, on what premise"),
    ("Rules",    "the directive family: what is required, in what preference order, in what step order"),
    ("Identity", "the declarative family: what counts as what"),
    ("Manner",   "the force-neutral carrier family: how it is encoded, how it is presented or registered, which instance it is"),
]
SYS = ("You classify what FAMILY of change was made to a document. "
       "Answer with exactly one label from this list:\n"
       + "\n".join(f"- {n}: {g}" for n, g in FAM)
       + "\nPick the single family the change belongs to.")

def trunc(s, n=1400):
    s = s or ""
    return s if len(s) <= n else s[:n] + "\n[...truncated]"

def user_msg(o):
    return (f"BEFORE:\n{trunc(o['before'])}\n\nAFTER:\n{trunc(o['after'])}\n\n"
            f"WHAT CHANGED: {o.get('variation_site','')}\n\nWhich family of change is this?")

def load(split):
    return [o for o in (json.loads(l) for l in open(split)) if o["kind_target"] in K2B]

# No trailing space: the model emits ' "' as a SINGLE token here, so the space
# must live in the scored continuation or we force a token it never emits.
JSON_OPEN = '{"family":'

def prefix_ids(tok, o):
    """Assistant prefix up to the point where the label string begins, so the
    scored continuation is the SAME object ollama's structured output produced."""
    msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": user_msg(o)}]
    text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                   enable_thinking=False) + JSON_OPEN
    return tok(text, return_tensors="pt").input_ids[0]

@torch.no_grad()
def score(model, tok, items, dev):
    """Constrained GREEDY decoding over the 4 label continuations - a token-level
    prefix-trie walk, which is exactly what llguidance/ollama's enum mask does.
    NOT argmax over whole-sequence logprob: those differ, and the production
    condition is the masked greedy one."""
    model.eval(); rows = []
    opts = {l: tok(f' "{l}"', add_special_tokens=False).input_ids for l in LABELS}
    for o in items:
        pre = prefix_ids(tok, o).to(dev)
        alive, cur, step = list(LABELS), pre.clone(), 0
        while len(alive) > 1:
            nxt = {}
            for l in alive:
                if step < len(opts[l]):
                    nxt.setdefault(opts[l][step], []).append(l)
            if len(nxt) <= 1:
                alive = next(iter(nxt.values())) if nxt else alive
                step += 1
                if step > 12: break
                continue
            lg = model(cur.unsqueeze(0)).logits[0, -1].float().log_softmax(-1)
            tk = max(nxt, key=lambda t: lg[t].item())
            alive = nxt[tk]
            cur = torch.cat([cur, torch.tensor([tk], device=dev)])
            step += 1
        rows.append({"id": o["id"], "gold_ctor": o["kind_target"],
                     "gold": SURF[K2B[o["kind_target"]]], "pred": alive[0]})
    acc = sum(r["pred"] == r["gold"] for r in rows) / len(rows)
    return acc, rows

def main():
    mode = sys.argv[1]
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(SEED)
    tok = AutoTokenizer.from_pretrained(BASE)
    test = load(f"{HERE}/test_split.jsonl")

    if mode == "zeroshot":
        model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.bfloat16).to(dev)
        acc, rows = score(model, tok, test, dev)
        with open(f"{HERE}/pred4_qwen3_zs_hf.jsonl", "w") as f:
            for r in rows: f.write(json.dumps(r) + "\n")
        print(f"ZEROSHOT(transformers) 4way={acc:.3f} ({round(acc*len(rows))}/{len(rows)})")
        print("labels:", dict(collections.Counter(r['pred'] for r in rows)))
        return

    # ---- fine-tune ----
    from peft import LoraConfig, get_peft_model
    tr_all = load(f"{HERE}/train_split.jsonl")
    by = collections.defaultdict(list)
    for o in tr_all: by[SURF[K2B[o["kind_target"]]]].append(o)
    rng = random.Random(SEED); train, devset = [], []
    for k in sorted(by):
        g = sorted(by[k], key=lambda x: x["id"]); rng.shuffle(g)
        n_dev = max(1, round(len(g) * 20 / len(tr_all)))
        devset += g[:n_dev]; train += g[n_dev:]
    print(f"train={len(train)} dev={len(devset)} test={len(test)}")

    model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.bfloat16).to(dev)
    model = get_peft_model(model, LoraConfig(
        r=16, lora_alpha=32, lora_dropout=0.05, task_type="CAUSAL_LM",
        target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"]))
    model.print_trainable_parameters()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=1e-4)

    def batch(o):
        pre = prefix_ids(tok, o)
        lab = tok(f' "{SURF[K2B[o["kind_target"]]]}"', add_special_tokens=False).input_ids
        ids = torch.cat([pre, torch.tensor(lab)]).unsqueeze(0).to(dev)
        labels = ids.clone(); labels[0, :len(pre)] = -100
        return ids, labels

    best, best_state, curve = -1, None, []
    for ep in range(1, 13):
        model.train(); rng.shuffle(train); tot = 0.0
        for i, o in enumerate(train):
            ids, labels = batch(o)
            loss = model(ids, labels=labels).loss / 4
            loss.backward(); tot += loss.item() * 4
            if (i + 1) % 4 == 0: opt.step(); opt.zero_grad()
        opt.step(); opt.zero_grad()
        dacc, _ = score(model, tok, devset, dev)
        curve.append({"epoch": ep, "train_loss": tot/len(train), "dev_acc": dacc})
        print(f"  ep{ep:2d} loss={tot/len(train):.4f} dev={dacc:.3f}", flush=True)
        if dacc > best:
            best = dacc
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items() if "lora" in k}
    model.load_state_dict(best_state, strict=False)
    print(f"restored best dev={best:.3f}")
    # persist the merged fine-tuned weights: this is the DEPLOYED artifact and
    # every equivalence arm must be built from it, not from the base model.
    if SAVE:
        merged = model.merge_and_unload()
        merged.save_pretrained(f"{HERE}/ft_merged"); tok.save_pretrained(f"{HERE}/ft_merged")
        print("merged model saved -> ft_merged/")
    acc, rows = score(model, tok, test, dev)
    tag = os.environ.get("FT_TAG", "")
    with open(f"{HERE}/pred4_qwen3_ft{tag}.jsonl", "w") as f:
        for r in rows: f.write(json.dumps(r) + "\n")
    json.dump(curve, open(f"{HERE}/ft_curve{tag}.json", "w"), indent=2)
    print(f"FINETUNED 4way={acc:.3f} ({round(acc*len(rows))}/{len(rows)})")
    print("labels:", dict(collections.Counter(r['pred'] for r in rows)))

if __name__ == "__main__":
    main()
