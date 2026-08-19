"""S18 steps 2-3 (+6, +9's placebo): determinism gauge, then embed every corpus.

Runs only after the S8 gauge has been written to out/gauge_raw.json.
"""
import json, os, sys, time
import numpy as np
import requests
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import corpora, embed

OUT = '/home/emoore/CIRISOntology/scratchpad/eigen/out'
PRIMARY = 'BAAI/bge-large-en-v1.5'
SECONDARY = 'Qwen/Qwen3-Embedding-0.6B'
CAP = 2.00


def embed_raw(texts, model):
    """Uncached single request (used only by the determinism gauge)."""
    with open('/home/emoore/.deepinfra_key') as f:
        k = f.read().strip()
    r = requests.post(embed.ENDPOINT,
                      headers={'Authorization': f'Bearer {k}', 'Content-Type': 'application/json'},
                      json={'model': model, 'input': texts, 'encoding_format': 'float'}, timeout=180)
    r.raise_for_status()
    o = r.json()
    d = sorted(o['data'], key=lambda x: x['index'])
    return np.array([x['embedding'] for x in d], dtype=np.float64), o.get('usage', {}).get('prompt_tokens', 0)


def determinism(model):
    A = corpora.corpus_A()
    texts = [r['before'] for r in A[:20]]
    e1, t1 = embed_raw(texts, model)
    time.sleep(1.0)
    e2, t2 = embed_raw(texts, model)
    embed._usage_add(model, t1 + t2, 2)
    u1 = e1 / np.linalg.norm(e1, axis=1, keepdims=True)
    u2 = e2 / np.linalg.norm(e2, axis=1, keepdims=True)
    cos = (u1 * u2).sum(1)
    return {'model': model, 'n': 20, 'median_cos': float(np.median(cos)),
            'min_cos': float(cos.min()), 'dim': int(e1.shape[1])}


def texts_artifacts():
    A = corpora.corpus_A()
    H = corpora.corpus_held()
    BB = corpora.corpus_babel()
    B = corpora.corpus_B()
    out = []
    for rows in (A, H, BB, B):
        for r in rows:
            out += [r['before'], r['after']]
            out += ['The text reads: ' + r['span_before'], 'The text reads: ' + r['span_after']]
    return out


def texts_reasons():
    A = corpora.corpus_A()
    aids = {r['id'] for r in A}
    J = [j for j in corpora.judgments() if j['id'] in aids and j.get('reason')]
    out = []
    for j in J:
        out.append(j['reason'])
        out.append(corpora.strip_stoplist(j['reason']))
    return out


def main():
    if not os.path.exists(os.path.join(OUT, 'gauge_raw.json')):
        raise SystemExit('gauge not finished - S18 forbids embedding before the gauge')
    rep = {}
    for m in (PRIMARY, SECONDARY):
        rep[f'determinism_{m}'] = determinism(m)
        print(rep[f'determinism_{m}'], flush=True)
    ta = texts_artifacts()
    print(f'artifact texts: {len(ta)} ({len(set(ta))} unique)', flush=True)
    embed.embed(ta, PRIMARY, cap_usd=CAP)
    print('primary artifacts done, spend=%.4f' % embed.total_spend(), flush=True)
    embed.embed(ta, SECONDARY, cap_usd=CAP)
    print('secondary artifacts done, spend=%.4f' % embed.total_spend(), flush=True)
    tr = texts_reasons()
    print(f'reason texts: {len(tr)} ({len(set(tr))} unique)', flush=True)
    embed.embed(tr, PRIMARY, cap_usd=CAP)
    print('reasons done, spend=%.4f' % embed.total_spend(), flush=True)
    rat = corpora.ratchet_rationales()
    print(f'ratchet rationales: {len(rat)}', flush=True)
    embed.embed(rat, PRIMARY, cap_usd=CAP)
    print('ratchet done, spend=%.4f' % embed.total_spend(), flush=True)
    for m in (PRIMARY, SECONDARY):
        h, n = embed.cache_sha256(m)
        rep[f'cache_{m}'] = {'sha256': h, 'bytes': n}
    rep['spend_usd'] = embed.total_spend()
    json.dump(rep, open(os.path.join(OUT, 'embed_report.json'), 'w'), indent=1)
    print(json.dumps(rep, indent=1))


if __name__ == '__main__':
    main()
