"""A0 — the judge client. Copied from `scratchpad/plane_annotate.py` (sec 12 code
confinement: the judge client is copied, not rewritten), with the sec 12 cache and
spend-ledger discipline added.

The key is read from ~/.deepinfra_key and is never printed, logged, or written to any
output file.
"""
from __future__ import annotations
import hashlib, json, os, pathlib, sys, threading, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = "https://api.deepinfra.com/v1/openai/chat/completions"
_KEY = pathlib.Path(os.path.expanduser("~/.deepinfra_key")).read_text().strip()

HARD_CAP_USD = 8.00          # sec 12
SOFT_ALARM_USD = 4.00

MODELS = ["meta-llama/Llama-4-Scout-17B-16E-Instruct",
          "openai/gpt-oss-120b",
          "google/gemma-3-27b-it"]
PRICE = {"meta-llama/Llama-4-Scout-17B-16E-Instruct": (0.08, 0.30),
         "openai/gpt-oss-120b": (0.09, 0.45),
         "google/gemma-3-27b-it": (0.10, 0.20)}

CACHE_ROOT = pathlib.Path("/home/emoore/CIRISOntology/scratchpad/a0_cache")
OUT = pathlib.Path("/home/emoore/CIRISOntology/scratchpad/a0run/out")


def run_id():
    """One run id per campaign, persisted so a restart replays the same cache
    (sec 12) while a genuinely new campaign gets its own directory."""
    p = OUT / "RUN_ID"
    if p.exists():
        return p.read_text().strip()
    OUT.mkdir(parents=True, exist_ok=True)
    rid = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    p.write_text(rid + "\n")
    return rid


def cache_dir():
    d = CACHE_ROOT / run_id()
    d.mkdir(parents=True, exist_ok=True)
    return d


def key_of(model, text):
    return hashlib.sha256((model + "||" + text).encode()).hexdigest()


def load_cache():
    p = cache_dir() / "judgments.jsonl"
    got = {}
    if p.exists():
        for line in open(p):
            try:
                r = json.loads(line)
                got[r["key"]] = r
            except Exception:
                pass
    return got


def spend_so_far():
    """The cap is enforced against the sum of ledger entries at process start,
    not a counter that resets on restart (sec 12)."""
    p = cache_dir() / "spend_ledger.jsonl"
    tot = 0.0
    if p.exists():
        for line in open(p):
            try:
                tot += json.loads(line)["usd"]
            except Exception:
                pass
    return tot


def _ask(model, text, retries=3):
    body = json.dumps({"model": model, "temperature": 0.0,
                       "max_tokens": (900 if "gpt-oss" in model else 500),
                       "messages": [{"role": "user", "content": text}]}).encode()
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(URL, data=body, headers={
                "Authorization": f"Bearer {_KEY}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.loads(r.read())
            u = d.get("usage", {})
            return (d["choices"][0]["message"]["content"],
                    u.get("prompt_tokens", 0), u.get("completion_tokens", 0))
        except Exception as e:                       # noqa: BLE001
            last = type(e).__name__
            if i == retries - 1:
                return None, 0, 0
            time.sleep(4 * (i + 1))
    return None, 0, 0


def parse_json(txt):
    if not isinstance(txt, str):
        return None
    try:
        return json.loads(txt[txt.index("{"): txt.rindex("}") + 1])
    except Exception:
        return None


def run_jobs(jobs, tag, workers=16, progress_every=100):
    """jobs: list of dicts with 'model', 'text', and any metadata to carry.

    Returns (records, stats). Every call appends one JSON line to the run's
    judgments.jsonl keyed by sha256(model||prompt); a restart re-issues only
    missing keys.
    """
    cache = load_cache()
    d = cache_dir()
    jpath, spath = d / "judgments.jsonl", d / "spend_ledger.jsonl"
    base = spend_so_far()
    if base >= HARD_CAP_USD:
        print(f"[{tag}] HARD CAP already reached (${base:.4f}) — refusing to spend", flush=True)
        return [], {"aborted": True, "spend_at_start": base}

    todo, have = [], []
    for j in jobs:
        k = key_of(j["model"], j["text"])
        if k in cache:
            have.append(dict(j, **{"key": k, "raw": cache[k].get("raw"),
                                   "in_tok": cache[k].get("in_tok", 0),
                                   "out_tok": cache[k].get("out_tok", 0)}))
        else:
            todo.append(dict(j, key=k))
    print(f"[{tag}] {len(jobs)} jobs: {len(have)} cached, {len(todo)} to issue; "
          f"ledger ${base:.4f}", flush=True)

    lock = threading.Lock()
    state = {"spend": base, "n": 0, "fail": 0, "capped": False}
    jf, sf = open(jpath, "a"), open(spath, "a")

    def one(j):
        if state["capped"]:
            return None
        txt, ti, to = _ask(j["model"], j["text"])
        pi, po = PRICE.get(j["model"], (0.2, 0.6))
        usd = ti * pi / 1e6 + to * po / 1e6
        rec = {"key": j["key"], "model": j["model"], "tag": tag, "raw": txt,
               "in_tok": ti, "out_tok": to,
               **{k: v for k, v in j.items() if k not in ("text", "model", "key")}}
        with lock:
            state["spend"] += usd
            if state["spend"] > HARD_CAP_USD:
                state["capped"] = True
                print(f"[{tag}] HARD CAP ${state['spend']:.4f} — stopping", flush=True)
                return None
            sf.write(json.dumps({"tag": tag, "model": j["model"], "usd": usd,
                                 "in_tok": ti, "out_tok": to}) + "\n")
            jf.write(json.dumps(rec) + "\n")
            jf.flush(); sf.flush()
            state["n"] += 1
            if txt is None:
                state["fail"] += 1
            if state["n"] % progress_every == 0:
                print(f"[{tag}]   {state['n']}/{len(todo)} issued, "
                      f"ledger ${state['spend']:.4f}, {state['fail']} failed", flush=True)
                if state["spend"] > SOFT_ALARM_USD:
                    print(f"[{tag}]   SOFT ALARM: ${state['spend']:.4f}", flush=True)
        return rec

    new = []
    if todo:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            for r in ex.map(one, todo):
                if r is not None:
                    new.append(r)
    jf.close(); sf.close()
    out = have + [dict(j, **{}) for j in new]
    # re-attach metadata for the newly issued ones (already carried in rec)
    stats = {"n_jobs": len(jobs), "cached": len(have), "issued": len(new),
             "failed": state["fail"], "spend_total": state["spend"],
             "spend_this_stage": state["spend"] - base, "capped": state["capped"]}
    print(f"[{tag}] done: {stats}", flush=True)
    return out, stats
