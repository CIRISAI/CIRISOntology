"""Token pass for S12's positive-control renderings (system python3; AMENDMENTS.md A5).

An item is dropped from the control if ANY of its four texts — the C1 rendering of each of
the three mutations, plus the shared before-window — exceeds any arm's context.
"""
import json, os, sys

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen2run')
import e2lib as L
from transformers import AutoTokenizer

p = json.load(open(os.path.join(L.OUT, 'poscontrol_texts.json')))
texts, tq, bw = p['texts'], p['texts_qwen'], p['before_windows']

tb = AutoTokenizer.from_pretrained('BAAI/bge-large-en-v1.5')
tqk = AutoTokenizer.from_pretrained('Qwen/Qwen3-Embedding-0.6B')

nb = [len(x) for x in tb(texts + bw, add_special_tokens=True)['input_ids']]
nq = [len(x) for x in tqk(tq + bw, add_special_tokens=True)['input_ids']]

over = set()
n_items = len(bw)
for k in range(len(texts)):
    if nb[k] > 512 or nq[k] > 32768:
        over.add(k // 3)
for k in range(len(bw)):
    if nb[len(texts) + k] > 512 or nq[len(tq) + k] > 32768:
        over.add(k)

out = {'max': {'bge': max(nb), 'qwen': max(nq)},
       'limits': {'bge': 512, 'qwen': 32768},
       'over_items': sorted(over), 'n_items': n_items}
L.atomic_json(out, os.path.join(L.OUT, 'poscontrol_tokens.json'))
print(f'poscontrol tokens: max bge={max(nb)} qwen={max(nq)} over={len(over)} items',
      flush=True)
