"""Embed the RATCHET action_rationale corpus (placebo P2).

DEVIATION (forced, declared): the DeepInfra endpoint REJECTS inputs longer than the
model's 512-token context with HTTP 400 rather than truncating them, so truncation has
to happen client-side.  Every rationale is truncated to 1,500 characters before
submission; the truncated fraction is measured and checked against V7's 2% threshold.
"""
import json, os, sys, time
import numpy as np
import requests
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import corpora, embed

CAP_CHARS = 1500
PRIMARY = 'BAAI/bge-large-en-v1.5'


def main():
    rat = corpora.ratchet_rationales()
    n_trunc = sum(1 for t in rat if len(t) > CAP_CHARS)
    cut = [t[:CAP_CHARS] for t in rat]
    cache = embed.Cache(PRIMARY)
    uniq = sorted(set(cut))
    todo = [t for t in uniq if cache.get(t) is None]
    key = open('/home/emoore/.deepinfra_key').read().strip()
    hdr = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
    B = 32
    tok = 0
    for i in range(0, len(todo), B):
        chunk = todo[i:i + B]
        shrink = 1.0
        for attempt in range(8):
            payload = [t[:int(CAP_CHARS * shrink)] for t in chunk]
            r = requests.post(embed.ENDPOINT, headers=hdr,
                              json={'model': PRIMARY, 'input': payload,
                                    'encoding_format': 'float'}, timeout=180)
            if r.status_code == 200:
                break
            if r.status_code == 400:
                shrink *= 0.85
                continue
            time.sleep(2 ** attempt)
        else:
            raise RuntimeError('failed batch')
        o = r.json()
        for t, d in zip(chunk, sorted(o['data'], key=lambda x: x['index'])):
            cache.put(t, d['embedding'])
        tok += o.get('usage', {}).get('prompt_tokens', 0)
        if (i // B) % 5 == 0:
            cache.flush()
            print(f'  {i+len(chunk)}/{len(todo)}', flush=True)
    cache.flush()
    embed._usage_add(PRIMARY, tok, len(todo) // B + 1)
    rep = {'n_rationales': len(rat), 'n_unique_after_truncation': len(uniq),
           'char_cap': CAP_CHARS, 'n_truncated': n_trunc,
           'frac_truncated': n_trunc / len(rat),
           'V7_threshold': 0.02, 'V7_fired': bool(n_trunc / len(rat) > 0.02),
           'spend_usd': embed.total_spend()}
    json.dump(rep, open('/home/emoore/CIRISOntology/scratchpad/eigen/out/ratchet_embed.json', 'w'),
              indent=1)
    print(json.dumps(rep, indent=1))


if __name__ == '__main__':
    main()
