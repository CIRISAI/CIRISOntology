"""S11 D-B2 recomputed on a nuisance matrix that does not annihilate its own label.

AMENDMENTS.md A6: on the frozen `res` arm, Z contains the 39 batch dummies, so the
batch-class means of the residualized fitting half are exactly zero and the pinned
Omega_batch is roundoff.  Here Z = [1, log10(1+span), domain(11)] = 13 columns — the frozen
Z with only the batch dummies removed.  Disclosure statistic only (S17): it is never used
to adjust a verdict.  The `raw` arm (Z = [1]) is reported beside it.
"""
import json, os, sys, time

import numpy as np

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen2run')
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import e2lib as L
import pipeline as pl

t0 = time.time()
rows_all = L.load_e2()
meta = json.load(open(os.path.join(L.OUT, 'embed_meta.json')))
drop = set(meta['V7']['dropped_ids'])
ki = [i for i, r in enumerate(rows_all) if r['id'] not in drop]
rows = [rows_all[i] for i in ki]
labels = L.labels_of(rows)
batches = L.batches_of(rows)
dom11, _ = L.domain11_of(rows)
splits = L.make_splits(labels, batches, L.NSPLIT, L.SEED)
X = np.load(os.path.join(L.CACHE, 'X_qwen_C1.npy')).astype(np.float64)[ki]
X /= np.linalg.norm(X, axis=1, keepdims=True)
Xr = X @ np.linalg.svd(X, full_matrices=False)[2].T

NP = 200
out = {}
for zk, lab, K, tag in (('nobatch', batches, 40, 'batch_label_Z_without_batch'),
                        ('none', batches, 40, 'batch_label_Z_constant_only'),
                        ('nodom', dom11, 11, 'domain11_label_Z_without_domain'),
                        ('none', dom11, 11, 'domain11_label_Z_constant_only')):
    Z = L.nuisance_Z(rows, zk)
    prep = pl.Prepared(Xr, Z, splits, residualize=(zk != 'none'))
    obs = pl.full_stats(prep, pl.onehot(lab, K), ks=[11], want_eta=False)
    C, _ = pl.contrasts_batch(prep, pl.onehot(lab, K), 'F')
    rng = np.random.default_rng(4242)
    null = np.array([pl.full_stats(prep, pl.onehot(rng.permutation(lab), K), ks=[11],
                                   want_eta=False)['omega'][11] for _ in range(NP)])
    tax = pl.full_stats(prep, pl.onehot(labels, 11), ks=[11], want_eta=False)
    out[tag] = {'z_cols': int(Z.shape[1]), 'n_classes': K,
                'contrast_frobenius_norm': float(np.linalg.norm(C[0])),
                'omega11': obs['omega'][11], 'rank_B': obs['rank'],
                'null_median': float(np.median(null)),
                'excess': obs['omega'][11] - float(np.median(null)),
                'p': float((1 + int((null >= obs['omega'][11]).sum())) / (1 + NP)),
                'nperm': NP,
                'omega11_taxonomy_same_Z': tax['omega'][11],
                'rank_B_taxonomy': tax['rank']}
    print(f'{tag}: ||C||={out[tag]["contrast_frobenius_norm"]:.4g} '
          f'Om11={obs["omega"][11]:.5f} rank={obs["rank"]:.0f} '
          f'null={out[tag]["null_median"]:.5f} p={out[tag]["p"]:.4f} '
          f'| taxonomy same Z: {tax["omega"][11]:.5f} rank {tax["rank"]:.0f} '
          f'[{time.time()-t0:.0f}s]', flush=True)
    L.atomic_json(out, os.path.join(L.OUT, 'db2_nobatch.json'))

out['_note'] = ('AMENDMENTS.md A6.  Disclosure statistics only; no verdict is adjusted by '
                'them (S17).  The pinned res-arm values in diagnostics.json are annihilated '
                'and are reported beside these as such.')
L.atomic_json(out, os.path.join(L.OUT, 'db2_nobatch.json'))
print('DONE', time.time() - t0, flush=True)
