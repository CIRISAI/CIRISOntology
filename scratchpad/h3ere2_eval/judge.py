#!/usr/bin/env python3
"""h3ere2 judging harness. Implements JUDGE_PROTOCOL.md.

INPUT (from inference-scout): responses.jsonl, one object per (item, arm):
  {"id":..., "arm":"A"|"B"|"C", "response":str,
   "scramble_id":int|null, "path":[...]|null, "gen_tokens":int, "wall_s":float}

Modes:
  calib_bias   identical pairs      -> position bias      (must be < 0.075 from 0.5)
  calib_sens   known-gap pairs      -> judge sensitivity  (must be >= 0.90)
  pairs        real C-vs-B, C-vs-A  -> both orders, order-balanced scoring
"""
import json, sys, os, time, random, urllib.request, collections

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = {"type": "object",
          "properties": {"better": {"type": "string", "enum": ["1", "2"]}},
          "required": ["better"]}
SYS = ("You compare two analyses of the same document change. "
       "Judge which is more useful, accurate and actionable for someone who must act on "
       "the change. Ignore length and formatting; judge substance. "
       "You must choose one. Reply with 1 or 2.")

def ask(model, item_text, r1, r2, retries=3):
    user = (f"THE CHANGE:\n{item_text}\n\n"
            f"--- ANALYSIS 1 ---\n{r1}\n\n--- ANALYSIS 2 ---\n{r2}\n\n"
            "Which analysis is better?")
    body = json.dumps({"model": model,
        "messages": [{"role": "system", "content": SYS},
                     {"role": "user", "content": user}],
        "stream": False, "format": SCHEMA,
        "options": {"temperature": 0, "num_predict": 32, "num_ctx": 8192},
        "think": False}).encode()
    for a in range(retries):
        try:
            req = urllib.request.Request("http://localhost:11434/api/chat", body,
                                         {"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(json.loads(r.read())["message"]["content"])["better"]
        except Exception:
            if a == retries - 1: return None
            time.sleep(2)

def load_items(path=None):
    # K2 instrument adaptation (the ONLY judge.py change): the A1.2/A2 runs live on the
    # 92-item frozen split, so the corpus is a parameter; default unchanged (wild run).
    p = path or os.path.expanduser("~/CIRISOntology/scratchpad/plane_corpus/eco_corpus.jsonl")
    out = {}
    for l in open(p):
        o = json.loads(l)
        out[o["id"]] = f"BEFORE: {(o['before'] or '')[:900]}\nAFTER: {(o['after'] or '')[:900]}"
    return out

def load_resp(path):
    """Arm B has 10 scramble draws per item. Per JUDGE_PROTOCOL section 4 we do BALANCED
    RANDOM ASSIGNMENT -- one draw per item, balanced across the 10, seed recorded -- so each
    item contributes one C-vs-B pair whose B is a draw from the scramble DISTRIBUTION.
    (Naively keeping the last draw would silently fix the scramble and lose the distribution.)"""
    d = collections.defaultdict(dict); bees = collections.defaultdict(list)
    for l in open(path):
        o = json.loads(l)
        if o["arm"] == "B": bees[o["id"]].append(o)
        else: d[o["id"]][o["arm"]] = o
    rng = random.Random(20260822)
    ids = sorted(bees)
    order = list(range(len(ids)))
    rng.shuffle(order)
    for pos, iid in zip(order, ids):
        cands = sorted(bees[iid], key=lambda x: (x.get("scramble_seed") if x.get("scramble_seed") is not None else -1))
        d[iid]["B"] = cands[pos % len(cands)]          # balanced: each draw used ~equally
    return d

def main():
    mode, model, respfile, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    corpus = sys.argv[5] if len(sys.argv) > 5 else None
    items, R = load_items(corpus), load_resp(respfile)
    ids = sorted(R)
    rng = random.Random(20260822)
    rows, t0 = [], time.time()

    for i, iid in enumerate(ids, 1):
        if mode == "calib_bias":
            # identical content in both slots: ANY deviation from 50/50 is position bias
            a = R[iid].get("A")
            if not a: continue
            pick = ask(model, items[iid], a["response"], a["response"])
            rows.append({"id": iid, "mode": mode, "pick": pick})

        elif mode == "calib_sens":
            # intact vs first-sentence truncation: judge MUST prefer intact
            a = R[iid].get("A")
            if not a: continue
            full = a["response"]
            deg = full.split(".")[0].strip() + "."
            flip = rng.random() < 0.5          # randomise which slot is intact
            r1, r2 = (deg, full) if flip else (full, deg)
            pick = ask(model, items[iid], r1, r2)
            correct = (pick == "2") if flip else (pick == "1")
            rows.append({"id": iid, "mode": mode, "pick": pick, "intact_slot": 2 if flip else 1,
                         "correct": correct})

        else:  # real pairs, BOTH orders
            for lo, hi in (("C", "B"), ("C", "A")):
                x, y = R[iid].get(lo), R[iid].get(hi)
                if not x or not y: continue
                for order in (0, 1):
                    r1, r2 = (x["response"], y["response"]) if order == 0 else (y["response"], x["response"])
                    pick = ask(model, items[iid], r1, r2)
                    winner = None
                    if pick in ("1", "2"):
                        winner = (lo if pick == "1" else hi) if order == 0 else (hi if pick == "1" else lo)
                    rows.append({"id": iid, "mode": "pair", "cmp": f"{lo}v{hi}", "order": order,
                                 "pick": pick, "winner": winner,
                                 "stream": iid.split("-")[0], "surface": x.get("surface"),
                                 "scramble_id": (y.get("scramble_id") if hi == "B" else None),
                                 "len1": len(r1), "len2": len(r2)})
        if i % 20 == 0: print(f"  {i}/{len(ids)}  {time.time()-t0:.0f}s", flush=True)

    with open(out, "w") as f:
        for r in rows: f.write(json.dumps(r) + "\n")
    print(f"wrote {len(rows)} judgments -> {out}")

    if mode == "calib_bias":
        p = [r["pick"] for r in rows if r["pick"]]
        s1 = sum(x == "1" for x in p) / len(p)
        print(f"POSITION BIAS: slot-1 rate = {s1:.3f} (n={len(p)}); |dev| = {abs(s1-0.5):.3f} "
              f"-> {'PASS' if abs(s1-0.5) < 0.075 else 'BIASED (order-balanced scoring required)'}")
    elif mode == "calib_sens":
        c = [r["correct"] for r in rows if r["pick"]]
        acc = sum(c)/len(c)
        print(f"JUDGE SENSITIVITY: {acc:.3f} (n={len(c)}) "
              f"-> {'PASS' if acc >= 0.90 else 'FAILED - judge cannot detect a known gap; no verdict'}")

if __name__ == "__main__":
    main()
