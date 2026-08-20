"""S3.4 client-side token counting for the truncation pass (V7).

Runs under the SYSTEM python3 (transformers/tokenizers are absent from the pinned venv;
AMENDMENTS.md A5).  Counts tokens of the text ACTUALLY SENT for each arm — i.e. with the
instructed-Qwen prefix applied where it applies — and writes out/tokens.json.

Reads only `before`/`after` (via the pinned mechanical span construction).  No authored
field is read; no item body is printed.
"""
import json, os, sys

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen2run')
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import e2lib as L
from transformers import AutoTokenizer

MODELS = {'bge': 'BAAI/bge-large-en-v1.5', 'qwen': 'Qwen/Qwen3-Embedding-0.6B'}

rows = L.load_e2()
c1, c1p = L.c1_texts(rows)
ids = [r['id'] for r in rows]

sets = {'bge': (c1, c1p), 'qwen': ([L.arm_prefix('qwen', t) for t in c1],
                                   [L.arm_prefix('qwen', t) for t in c1p]),
        'qwen_noinstr': (c1, c1p)}

tok = {}
for arm, (a, b) in sets.items():
    name = MODELS['bge'] if arm == 'bge' else MODELS['qwen']
    tk = AutoTokenizer.from_pretrained(name)
    na = [len(x) for x in tk(a, add_special_tokens=True)['input_ids']]
    nb = [len(x) for x in tk(b, add_special_tokens=True)['input_ids']]
    tok[arm] = {'model': name, 'limit': L.CTX_LIMIT[arm], 'c1': na, 'c1p': nb,
                'max_c1': max(na), 'max_c1p': max(nb),
                'n_over': int(sum(1 for x, y in zip(na, nb)
                                  if max(x, y) > L.CTX_LIMIT[arm]))}
    print(f'{arm}: max_c1={max(na)} max_c1p={max(nb)} limit={L.CTX_LIMIT[arm]} '
          f'over={tok[arm]["n_over"]}', flush=True)

tok['_ids'] = ids
tok['_chars'] = {'c1_max': max(len(t) for t in c1), 'c1p_max': max(len(t) for t in c1p),
                 'c1_median': sorted(len(t) for t in c1)[len(c1) // 2]}
L.atomic_json(tok, os.path.join(L.OUT, 'tokens.json'))
print('wrote out/tokens.json', flush=True)
