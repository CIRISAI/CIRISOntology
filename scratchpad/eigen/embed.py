"""DeepInfra embeddings client with on-disk cache (S3 of the prereg).

Cache: /home/emoore/CIRISOntology/scratchpad/eigen/cache/eigen_cache_<slug>.jsonl
one JSON object per line: {"h": sha256(model || "\\x00" || text), "b": base64(float32[])}
The key is exactly the prereg's; the location is the orchestrator's eigen/cache/.
The API key is read into memory and never printed or logged.
"""
import base64, hashlib, json, os, sys, time
import numpy as np
import requests

ENDPOINT = 'https://api.deepinfra.com/v1/openai/embeddings'
CACHE_DIR = '/home/emoore/CIRISOntology/scratchpad/eigen/cache'
USAGE_PATH = '/home/emoore/CIRISOntology/scratchpad/eigen/out/usage.json'
BATCH = 64

# DeepInfra list prices, USD per 1M input tokens (embeddings), 2026-08
PRICE = {'BAAI/bge-large-en-v1.5': 0.010,
         'Qwen/Qwen3-Embedding-0.6B': 0.005,
         'BAAI/bge-m3': 0.010}


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
    u['_total_usd'] = sum(PRICE.get(m, 0.01) * v['tokens'] / 1e6
                          for m, v in u.items() if isinstance(v, dict))
    json.dump(u, open(USAGE_PATH, 'w'), indent=1)
    return u['_total_usd']


def total_spend():
    if not os.path.exists(USAGE_PATH):
        return 0.0
    return json.load(open(USAGE_PATH)).get('_total_usd', 0.0)


def embed(texts, model, cap_usd=2.00, verbose=True):
    """Return (n, d) float32 array in the order of `texts`. Cached, batched."""
    cache = Cache(model)
    uniq, order = [], []
    seen = {}
    for t in texts:
        if t not in seen:
            seen[t] = len(uniq)
            uniq.append(t)
        order.append(seen[t])
    todo = [t for t in uniq if cache.get(t) is None]
    if todo and os.environ.get('EIGEN_STRICT') == '1':
        raise RuntimeError(f'STRICT: {len(todo)} of {len(uniq)} texts missing from the '
                           f'{model} cache; no API call made')
    if todo:
        key = _key()
        hdr = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
        tok = 0
        ncalls = 0
        for i in range(0, len(todo), BATCH):
            chunk = todo[i:i + BATCH]
            for attempt in range(6):
                try:
                    r = requests.post(ENDPOINT, headers=hdr,
                                      json={'model': model, 'input': chunk,
                                            'encoding_format': 'float'}, timeout=180)
                    if r.status_code == 200:
                        break
                    if r.status_code in (429, 500, 502, 503, 504):
                        time.sleep(2 ** attempt)
                        continue
                    raise RuntimeError(f'HTTP {r.status_code}: {r.text[:300]}')
                except requests.RequestException as e:
                    if attempt == 5:
                        raise
                    time.sleep(2 ** attempt)
            else:
                raise RuntimeError('exhausted retries')
            o = r.json()
            data = sorted(o['data'], key=lambda x: x['index'])
            for t, d in zip(chunk, data):
                cache.put(t, d['embedding'])
            tok += o.get('usage', {}).get('prompt_tokens', 0)
            ncalls += 1
            if ncalls % 10 == 0:
                cache.flush()
                spend = _usage_add(model, tok, ncalls)
                tok, ncalls = 0, 0
                if verbose:
                    print(f'  [{model}] {i+len(chunk)}/{len(todo)} spend=${spend:.4f}', flush=True)
                if spend > cap_usd:
                    raise RuntimeError(f'SPEND CAP {cap_usd} exceeded at ${spend:.4f}')
        cache.flush()
        _usage_add(model, tok, ncalls)
    V = np.stack([cache.get(t) for t in uniq])
    return V[np.asarray(order)]


def cache_sha256(model):
    p = os.path.join(CACHE_DIR, f'eigen_cache_{slug(model)}.jsonl')
    if not os.path.exists(p):
        return None, 0
    h = hashlib.sha256()
    n = 0
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
            n += len(blk)
    return h.hexdigest(), n
