"""S11 design diagnostics — D-S1, D-B2, D-B3 and the VG3 interleave gate.

D-B1 (TF-IDF + logistic batch detectability) runs separately under the system python3
(db1.py; AMENDMENTS.md A5).  D-S1 is READ BEFORE N1b's p is read (S11, S18 step 9).
None of these adjusts a verdict: D-B2 is a disclosure statistic (S17), D-B3 is a
disclosure whose governing null stays N1 in every branch, D-S1 fixes how an N1b failure
is reported (K1-GEOMETRY vs SPAN-CONFOUNDED).
"""
import json, os, sys, time

import numpy as np
from scipy import stats as sps

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen2run')
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import e2lib as L
import pipeline as pl

t0 = time.time()
rows_all = L.load_e2()
meta = json.load(open(os.path.join(L.OUT, 'embed_meta.json')))
dropped = set(meta['V7']['dropped_ids'])
keep_idx = [i for i, r in enumerate(rows_all) if r['id'] not in dropped]
rows = [rows_all[i] for i in keep_idx]
labels = L.labels_of(rows)
batches = L.batches_of(rows)
span = np.array([r['ctx_chars'] for r in rows], dtype=float)
R = {'ts': time.strftime('%Y-%m-%dT%H:%M:%S'), 'n': len(rows)}

# ---------------------------------------------------------------- D-S1
groups = [span[labels == k] for k in range(L.NK)]
H, p = sps.kruskal(*groups)
med = {L.KINDS[k]: float(np.median(groups[k])) for k in range(L.NK)}
ratio = max(med.values()) / min(med.values())
R['D_S1'] = {'per_kind_median_span_chars': med,
             'max_over_min_ratio': float(ratio),
             'kruskal_H': float(H), 'kruskal_p': float(p),
             'corpusA_comparison': {'ratio': 87, 'kruskal_p': 7.6e-16},
             'reading': ('N1b is a light correction; K1-on-N1b would be a geometry verdict'
                         if ratio <= 5 else
                         ('N1b is doing very heavy lifting; an N1b failure is reported as '
                          'SPAN-CONFOUNDED' if ratio > 20 else
                          'intermediate: N1b is a real correction, reported with the ratio')),
             'span_summary': {'min': float(span.min()), 'median': float(np.median(span)),
                              'max': float(span.max())}}
print('D-S1 span ratio %.2fx  KW p=%.3g' % (ratio, p), flush=True)

# ---------------------------------------------------------------- VG3
nb = len(np.unique(batches))
lost_batch = {}
lost_kind = {}
kb = np.zeros((L.NK, 40), dtype=int)
for k, b in zip(labels, batches):
    kb[k, b] += 1
orig = {}
for r in rows_all:
    orig.setdefault(int(r['batch']), 0)
    orig[int(r['batch'])] += 1
for b in range(40):
    lost_batch[b] = orig[b] - int((batches == b).sum())
origk = {}
for r in rows_all:
    origk[r['kind_target']] = origk.get(r['kind_target'], 0) + 1
for k, kn in enumerate(L.KINDS):
    lost_kind[kn] = (origk[kn] - int((labels == k).sum())) / origk[kn]
missing = int(max(11 - (kb > 0).sum(0)))
R['VG3'] = {'max_items_lost_from_a_batch': int(max(lost_batch.values())),
            'criterion_a_max': 3,
            'max_frac_lost_from_a_kind': float(max(lost_kind.values())),
            'criterion_b_max': 0.10,
            'max_missing_kinds_in_a_batch': missing, 'criterion_c_max': 3,
            'FIRED': bool(max(lost_batch.values()) > 3 or max(lost_kind.values()) > 0.10
                          or missing > 3)}
print('VG3 fired =', R['VG3']['FIRED'], flush=True)

# ---------------------------------------------------------------- D-B2
X = np.load(os.path.join(L.CACHE, 'X_qwen_C1.npy')).astype(np.float64)[keep_idx]
X /= np.linalg.norm(X, axis=1, keepdims=True)
Xr = X @ np.linalg.svd(X, full_matrices=False)[2].T
Z = L.nuisance_Z(rows, 'full')
splits = L.make_splits(labels, batches, L.NSPLIT, L.SEED)
prep = pl.Prepared(Xr, Z, splits, residualize=True)
KSb = [11]
obs = pl.full_stats(prep, pl.onehot(batches, 40), ks=KSb, want_eta=False)
rng = np.random.default_rng(4242)
null = []
NP = 0   # superseded by db2_nobatch.py: on this arm Z contains the batch dummies, so the
         # batch contrasts are annihilated (AMENDMENTS A6) and a null on roundoff is
         # meaningless.  The disclosure that matters is ||C||, computed below.
null = np.array([np.nan])
Cb, _ = pl.contrasts_batch(prep, pl.onehot(batches, 40), 'F')
R['D_B2'] = {'omega11_batch_label': obs['omega'][11], 'rank_B': obs['rank'],
             'contrast_frobenius_norm': float(np.linalg.norm(Cb[0])),
             'ANNIHILATED': True, 'nperm': NP,
             'note': ('AMENDMENTS A6: Z contains the 39 batch dummies, so every batch-class '
                      'mean of the residualized fitting half is exactly zero and this Omega '
                      'is roundoff.  See db2_nobatch.json for the evaluable version. '
                      'Disclosure statistic only (S17); never used to adjust a verdict.')}
print('D-B2 (annihilated) Omega_batch = %.5f  ||C||=%.3g' % (obs['omega'][11], R['D_B2']['contrast_frobenius_norm']), flush=True)

# ---------------------------------------------------------------- D-B3
ap = os.path.join(L.OUT, 'analysis_primary.json')
if os.path.exists(ap):
    A = json.load(open(ap))
    if 'N1c' in A.get('nulls', {}):
        n1 = A['nulls']['N1']['11']['null_median']
        n1c = A['nulls']['N1c']['11']['null_median']
        R['D_B3'] = {'N1_null_median': n1, 'N1c_null_median': n1c,
                     'difference_N1_minus_N1c': n1 - n1c,
                     'expected_direction': 'N1 >= N1c (free permutation is the conservative one)',
                     'direction_as_expected': bool(n1 >= n1c),
                     'governing_null': 'N1 in every branch (S11-D-B3, S17 forbids the switch)'}
        print('D-B3 N1 %.5f vs N1c %.5f' % (n1, n1c), flush=True)

R['seconds'] = time.time() - t0
L.atomic_json(R, os.path.join(L.OUT, 'diagnostics.json'))
L.done_marker('DIAG', {'artifact': os.path.join(L.OUT, 'diagnostics.json')})
print('DIAG DONE', time.time() - t0, flush=True)
