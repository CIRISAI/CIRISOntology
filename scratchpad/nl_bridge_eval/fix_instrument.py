#!/usr/bin/env python3
"""Instrument fix: honest checkpoint selection.

WHY NOT the obvious thing: selecting the best of the 6 existing runs by TEST score is
selection on the evaluation set. Expected max of 6 draws from N(0.763,0.078) is 0.862,
so "pick the 0.880 run" inflates the estimate by ~0.10 -- it reports the max of noise.
Each seed also re-partitions its own dev set, so dev is not comparable across runs.

So: a FIXED selection set S, common to every run, disjoint from the frozen test AND
held out of every run's training. Select on S, report on test once.
"""
import json, os, sys, random, collections, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model
import importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ft", f"{HERE}/finetune4.py")
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)
SURF, K2B = ft.SURF, ft.K2B

def build_splits():
    pool = ft.load(f"{HERE}/train_split.jsonl")
    by = collections.defaultdict(list)
    for o in pool: by[SURF[K2B[o["kind_target"]]]].append(o)
    rng = random.Random(999)                      # FIXED, independent of training seed
    sel, tr = [], []
    for k in sorted(by):
        g = sorted(by[k], key=lambda x: x["id"]); rng.shuffle(g)
        n = max(2, round(len(g) * 40 / len(pool)))
        sel += g[:n]; tr += g[n:]
    return tr, sel

def run_seed(seed, train, sel, test, tok, dev):
    torch.manual_seed(seed); rng = random.Random(seed)
    m = AutoModelForCausalLM.from_pretrained(ft.BASE, dtype=torch.bfloat16).to(dev)
    m = get_peft_model(m, LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05,
        task_type="CAUSAL_LM",
        target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"]))
    opt = torch.optim.AdamW([p for p in m.parameters() if p.requires_grad], lr=1e-4)
    best, best_state = -1, None
    for ep in range(1, 11):
        m.train(); rng.shuffle(train)
        for i, o in enumerate(train):
            pre = ft.prefix_ids(tok, o)
            lab = tok(f' "{SURF[K2B[o["kind_target"]]]}"', add_special_tokens=False).input_ids
            ids = torch.cat([pre, torch.tensor(lab)]).unsqueeze(0).to(dev)
            labels = ids.clone(); labels[0, :len(pre)] = -100
            (m(ids, labels=labels).loss / 4).backward()
            if (i + 1) % 4 == 0: opt.step(); opt.zero_grad()
        opt.step(); opt.zero_grad()
        sacc, _ = ft.score(m, tok, sel, dev)
        if sacc > best:
            best = sacc
            best_state = {k: v.detach().clone() for k, v in m.state_dict().items() if "lora" in k}
        print(f"    seed{seed} ep{ep:2d} sel={sacc:.3f}", flush=True)
    m.load_state_dict(best_state, strict=False)
    tacc, trows = ft.score(m, tok, test, dev)
    print(f"  seed{seed}: SELECTION={best:.3f}  test={tacc:.3f}", flush=True)
    return best, tacc, trows, m

def main():
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    tok = AutoTokenizer.from_pretrained(ft.BASE)
    train, sel = build_splits()
    test = ft.load(f"{HERE}/test_split.jsonl")
    print(f"train={len(train)}  SELECTION={len(sel)} (fixed, seed 999)  test={len(test)} (frozen)")
    seeds = [int(x) for x in sys.argv[1].split(",")]
    res = []
    for s in seeds:
        b, t, rows, model = run_seed(s, train, sel, test, tok, dev)
        res.append({"seed": s, "sel": b, "test": t, "rows": rows})
        with open(f"{HERE}/pred4_fix_s{s}.jsonl", "w") as f:
            for r in rows: f.write(json.dumps(r) + "\n")
        if b >= max(x["sel"] for x in res):
            model.merge_and_unload().save_pretrained(f"{HERE}/ft_best")
            tok.save_pretrained(f"{HERE}/ft_best")
            print(f"    (leader on selection -> saved to ft_best/)", flush=True)
        del model; torch.cuda.empty_cache()
    win = max(res, key=lambda x: x["sel"])
    print(f"\nSELECTED seed {win['seed']} (selection={win['sel']:.3f}) -> HONEST test = {win['test']:.3f}")
    print(f"  mean test over runs = {sum(r['test'] for r in res)/len(res):.3f}")
    byitem = collections.defaultdict(list)
    for r in res:
        for x in r["rows"]: byitem[x["id"]].append(x["pred"] == x["gold"])
    uns = sum(1 for v in byitem.values() if 0 < sum(v) < len(v))
    print(f"  boundary-unstable items across these runs: {uns}/{len(byitem)} = {uns/len(byitem):.1%}")
    json.dump({"selection_n": len(sel), "runs": [{k: v for k, v in r.items() if k != "rows"} for r in res],
               "selected_seed": win["seed"], "honest_test": win["test"],
               "unstable_frac": uns/len(byitem)}, open(f"{HERE}/results_fix_instrument.json","w"), indent=2)

if __name__ == "__main__": main()
