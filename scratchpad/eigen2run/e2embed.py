"""DeepInfra embedding for EIGEN2 — v1's embed.py logic, re-pointed at eigen2run/cache.

AMENDMENTS.md A1: the cache KEY is byte-identical to the prereg's
sha256(model || "\\x00" || text); only the file location moves, so that appending E2
vectors cannot alter the sha256 of the shared v1/phase-0 cache the calibration is pinned to.

The API key is read into memory and never printed or logged.
"""
import base64, hashlib, json, os, sys, time

import numpy as np
import requests

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen2run')
import e2lib as L

ENDPOINT = 'https://api.deepinfra.com/v1/openai/embeddings'
CACHE_DIR = L.CACHE
USAGE_PATH = os.path.join(L.OUT, 'usage.json')
BATCH = 64
PRICE = {'BAAI/bge-large-en-v1.5': 0.010,
         'Qwen/Qwen3-Embedding-0.6B': 0.005,
         'BAAI/bge-m3': 0.010}
CAP_TOTAL = 3.00


def _key():
    with open('/home/emoore/.deepinfra_key') as f:
        return f.read().strip()


def slug(model):
    return model.replace('/', '_')


def _h(model, text):
    return hashlib.sha256((model + '\x00' + text).encode('utf-8')).hexdigest()


class Cache:
    def __init__(self, model):
        self.model = model
        self.path = os.path.join(CACHE_DIR, f'eigen_cache_{slug(model)}.jsonl')
        self.map = {}
        if os.path.exists(self.path):
            with open(self.path) as f:
                for line in f:
                    try:
                        o = json.loads(line)
                    except Exception:
                        continue
                    self.map[o['h']] = np.frombuffer(base64.b64decode(o['b']), dtype=np.float32)
        self.fh = open(self.path, 'a')

    def get(self, text):
        return self.map.get(_h(self.model, text))

    def put(self, text, vec):
        h = _h(self.model, text)
        v = np.asarray(vec, dtype=np.float32)
        self.map[h] = v
        self.fh.write(json.dumps({'h': h, 'b': base64.b64encode(v.tobytes()).decode()}) + '\n')

    def flush(self):
        self.fh.flush()


def _usage_add(model, tokens, ncalls):
    u = {}
    if os.path.exists(USAGE_PATH):
        u = json.load(open(USAGE_PATH))
    e = u.setdefault(model, {'tokens': 0, 'calls': 0})
    e['tokens'] += int(tokens)
    e['calls'] += int(ncalls)
    u['_embed_usd'] = sum(PRICE.get(m, 0.01) * v['tokens'] / 1e6
                          for m, v in u.items() if isinstance(v, dict))
    L.atomic_json(u, USAGE_PATH)
    return u['_embed_usd']


def embed_spend():
    if not os.path.exists(USAGE_PATH):
        return 0.0
    return json.load(open(USAGE_PATH)).get('_embed_usd', 0.0)


def panel_spend():
    p = os.path.join(L.OUT, 'panel_spend.json')
    return json.load(open(p))['usd'] if os.path.exists(p) else 0.0


def total_spend():
    return embed_spend() + panel_spend()


def _post(chunk, model, hdr):
    for attempt in range(6):
        try:
            r = requests.post(ENDPOINT, headers=hdr,
                              json={'model': model, 'input': chunk,
                                    'encoding_format': 'float'}, timeout=180)
            if r.status_code == 200:
                return r
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f'HTTP {r.status_code}: {r.text[:300]}')
        except requests.RequestException:
            if attempt == 5:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError('exhausted retries')


def embed(texts, model, verbose=True, tag=''):
    """(n, d) float32 in the order of `texts`. Cached, batched, spend-capped ($3 total)."""
    cache = Cache(model)
    uniq, order, seen = [], [], {}
    for t in texts:
        if t not in seen:
            seen[t] = len(uniq)
            uniq.append(t)
        order.append(seen[t])
    todo = [t for t in uniq if cache.get(t) is None]
    if todo:
        hdr = {'Authorization': f'Bearer {_key()}', 'Content-Type': 'application/json'}
        tok = ncalls = 0
        for i in range(0, len(todo), BATCH):
            chunk = todo[i:i + BATCH]
            r = _post(chunk, model, hdr)
            o = r.json()
            for t, d in zip(chunk, sorted(o['data'], key=lambda x: x['index'])):
                cache.put(t, d['embedding'])
            tok += o.get('usage', {}).get('prompt_tokens', 0)
            ncalls += 1
            if ncalls % 5 == 0:
                cache.flush()
                sp = _usage_add(model, tok, ncalls)
                tok = ncalls = 0
                if verbose:
                    print(f'  [{tag or model}] {i+len(chunk)}/{len(todo)} '
                          f'embed=${sp:.4f} total=${total_spend():.4f}', flush=True)
                if total_spend() > CAP_TOTAL:
                    raise RuntimeError(f'V10 SPEND CAP ${CAP_TOTAL} exceeded '
                                       f'at ${total_spend():.4f}')
        cache.flush()
        _usage_add(model, tok, ncalls)
    V = np.stack([cache.get(t) for t in uniq])
    return V[np.asarray(order)]


def embed_nocache(texts, model):
    """One fresh request per BATCH, bypassing the cache — for the V2 determinism gauge."""
    hdr = {'Authorization': f'Bearer {_key()}', 'Content-Type': 'application/json'}
    out, tok, ncalls = [], 0, 0
    for i in range(0, len(texts), BATCH):
        chunk = texts[i:i + BATCH]
        o = _post(chunk, model, hdr).json()
        out += [d['embedding'] for d in sorted(o['data'], key=lambda x: x['index'])]
        tok += o.get('usage', {}).get('prompt_tokens', 0)
        ncalls += 1
    _usage_add(model, tok, ncalls)
    return np.asarray(out, dtype=np.float32)


def cache_sha256(model):
    p = os.path.join(CACHE_DIR, f'eigen_cache_{slug(model)}.jsonl')
    if not os.path.exists(p):
        return None, 0
    return L.sha256_file(p), os.path.getsize(p)
