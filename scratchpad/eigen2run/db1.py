"""S11 D-B1 — is batch style textually detectable on E2?

5-fold stratified TF-IDF 1-2gram + logistic accuracy predicting BATCH (40 classes) from
the UNCHANGED `before` text.  Majority baseline = 12/474 = 0.0253, so the reported
quantity is LIFT = accuracy / baseline, not accuracy (S11-D-B1, referee defect M9).

Staked meaning: lift <= 1.2x -> batch style is weak (at or below the 1.18x lift that
forced the corpus rebuild).  1.2-3x -> detectable.  > 3x -> strong, and the disclosure
sentence is mandatory in the headline.

Runs under the system python3 (sklearn absent from the pinned venv; AMENDMENTS.md A5).
A parallel run predicting KIND is reported beside it, purely as a scale.
"""
import json, os, sys

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen2run')
import e2lib as L

rows_all = L.load_e2()
meta = json.load(open(os.path.join(L.OUT, 'embed_meta.json')))
dropped = set(meta['V7']['dropped_ids'])
rows = [r for r in rows_all if r['id'] not in dropped]
txt = [r['before'] for r in rows]

out = {}
for target, y in (('batch', np.array([int(r['batch']) for r in rows])),
                  ('kind', np.array([L.KIDX[r['kind_target']] for r in rows]))):
    base = float(np.bincount(y).max() / len(y))
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=20260819)
    acc = []
    for tr, te in skf.split(txt, y):
        clf = make_pipeline(
            TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True),
            LogisticRegression(max_iter=2000, C=1.0))
        clf.fit([txt[i] for i in tr], y[tr])
        acc.append(float((clf.predict([txt[i] for i in te]) == y[te]).mean()))
    a = float(np.mean(acc))
    out[target] = {'accuracy': a, 'per_fold': acc, 'majority_baseline': base,
                   'lift': a / base, 'n_classes': int(len(np.unique(y)))}
    print(f'{target}: acc={a:.4f} baseline={base:.4f} lift={a/base:.3f}x', flush=True)

lift = out['batch']['lift']
out['staked_reading'] = ('batch style is WEAK (<= 1.2x, at or below the 1.18x lift that '
                         'forced the rebuild)' if lift <= 1.2 else
                         ('batch style is DETECTABLE (1.2-3x); the batch-residualized '
                          'primary is doing real work' if lift <= 3.0 else
                          'batch style is STRONG (> 3x); Omega_batch must be reported and '
                          'the disclosure sentence is mandatory in the headline'))
out['corpusA_comparison'] = {'accuracy': 0.573, 'baseline': 0.484, 'lift': 1.18,
                             'note': '3-class part a/b/c problem on Corpus A (v1 S2.1a)'}
L.atomic_json(out, os.path.join(L.OUT, 'db1.json'))
print(out['staked_reading'], flush=True)
