"""S20 panel annotation — POST-FREEZE, secondary arms only, budget <= $1.00.

`plane_annotate.py`'s BASE condition (full retention; everything-else-fixed design
paragraph; no attribution sentence), all 474 items, the three pinned model families.
The 12-name plain vocabulary is offered unchanged, INCLUDING Record, because the
false-positive rate on a corpus with no Record items is itself a measurement.

Forbidden uses (S20, pre-committed): the panel may not filter, re-label, re-weight or drop
any item from the primary arm, and may not be used to select a friendlier label source
after the primary is read.  Primary labels stay authored, always.
"""
import json, os, sys, time

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen2run')
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad')
import e2lib as L
import plane_annotate as PA

PA.HARD_CAP_USD = 1.00
OUT = os.path.join(L.OUT, 'panel_base.jsonl')

t0 = time.time()
rc = PA.main(L.CORPUS, OUT, conditions=['BASE'], models=PA.MODELS, limit=None, workers=16)

n = sum(1 for _ in open(OUT)) if os.path.exists(OUT) else 0
# recompute spend from the recorded usage fields (authoritative, not the estimate)
usd = 0.0
for line in open(OUT):
    try:
        r = json.loads(line)
    except Exception:
        continue
    pi, po = PA.PRICE.get(r['model'], (0.2, 0.6))
    usd += r.get('in_tok', 0) * pi / 1e6 + r.get('out_tok', 0) * po / 1e6
L.atomic_json({'usd': usd, 'n_judgments': n, 'rc': rc,
               'cap': 1.00, 'seconds': time.time() - t0},
              os.path.join(L.OUT, 'panel_spend.json'))
L.done_marker('PANEL', {'artifact': OUT, 'n_judgments': n, 'usd': usd, 'rc': rc})
print(f'PANEL DONE {n} judgments  ${usd:.4f}  rc={rc}  [{time.time()-t0:.0f}s]', flush=True)
