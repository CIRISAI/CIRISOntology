"""S9.1 steps 2-4: the V2 determinism gauge, the V7 truncation pass, and the C1/C1P
embeddings for all three arms.  Then the post-embedding VOID checks V1/V1b/V3/V4.

Order is the prereg's: determinism BEFORE the corpus embedding, token counts BEFORE any
spend, one item set fixed for every arm.
"""
import json, os, sys, time

import numpy as np

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen2run')
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import e2lib as L
import e2embed as E

t0 = time.time()
meta = {'ts': time.strftime('%Y-%m-%dT%H:%M:%S'), 'corpus_sha256': L.CORPUS_SHA}
rows = L.load_e2()
c1_all, c1p_all = L.c1_texts(rows)
ids = [r['id'] for r in rows]

# ---------------------------------------------------------------- V7 (token pass)
tok = json.load(open(os.path.join(L.OUT, 'tokens.json')))
over = {}
for arm in L.ARMS:
    lim = L.CTX_LIMIT[arm]
    o = [i for i in range(len(rows))
         if max(tok[arm]['c1'][i], tok[arm]['c1p'][i]) > lim]
    over[arm] = o
allover = sorted(set(i for o in over.values() for i in o))
frac = len(allover) / len(rows)
meta['V7'] = {'max_tokens': {a: [tok[a]['max_c1'], tok[a]['max_c1p']] for a in L.ARMS},
              'limits': {a: L.CTX_LIMIT[a] for a in L.ARMS},
              'n_over_per_arm': {a: len(over[a]) for a in L.ARMS},
              'frac_over_max': max(len(over[a]) for a in L.ARMS) / len(rows),
              'dropped_ids': [ids[i] for i in allover],
              'switch_to_bge_m3': bool(any(len(over[a]) / len(rows) > 0.02 for a in L.ARMS)),
              'fired': bool(allover)}
if meta['V7']['switch_to_bge_m3']:
    raise SystemExit('V7: >2% over context on some arm — the prereg requires a bge-m3 '
                     'switch; STOP and report rather than improvise.')
keep = [i for i in range(len(rows)) if i not in set(allover)]
rows = [rows[i] for i in keep]
c1 = [c1_all[i] for i in keep]
c1p = [c1p_all[i] for i in keep]
ids = [r['id'] for r in rows]
meta['n_items_analysed'] = len(rows)
print(f'V7: {len(allover)} items dropped; n = {len(rows)}', flush=True)

# ---------------------------------------------------------------- V2 (determinism)
gpath = os.path.join(L.OUT, 'determinism.json')
if os.path.exists(gpath):
    meta['V2'] = json.load(open(gpath))
    print('V2: reusing on-disk determinism gauge', flush=True)
else:
    gtexts = c1[:20]
    v2 = {}
    for arm in L.ARMS:
        model = L.ARM_MODEL[arm]
        tt = [L.arm_prefix(arm, t) for t in gtexts]
        A = E.embed_nocache(tt, model).astype(np.float64)
        B = E.embed_nocache(tt, model).astype(np.float64)
        A /= np.linalg.norm(A, axis=1, keepdims=True)
        B /= np.linalg.norm(B, axis=1, keepdims=True)
        cs = (A * B).sum(1)
        v2[arm] = {'median_cos': float(np.median(cs)), 'min_cos': float(cs.min()),
                   'n': len(gtexts), 'dim': int(A.shape[1])}
        print(f'V2 {arm}: median cos = {v2[arm]["median_cos"]:.6f} '
              f'min = {v2[arm]["min_cos"]:.6f}', flush=True)
    L.atomic_json(v2, gpath)
    meta['V2'] = v2
v2v = meta['V2']
meta['V2_verdict'] = {a: ('VOID' if v2v[a]['median_cos'] < 0.999
                          else ('noise_floor_recorded' if v2v[a]['median_cos'] < 0.9999
                                else 'clean')) for a in L.ARMS}
if any(v == 'VOID' for v in meta['V2_verdict'].values()):
    L.atomic_json(meta, os.path.join(L.OUT, 'embed_meta.json'))
    raise SystemExit('V2 FIRED: instrument nondeterminism — VOID.')

# ---------------------------------------------------------------- embed
X = {}
for arm in L.ARMS:
    model = L.ARM_MODEL[arm]
    for name, texts in (('C1', c1), ('C1P', c1p)):
        tt = [L.arm_prefix(arm, t) for t in texts]
        V = E.embed(tt, model, tag=f'{arm}/{name}')
        np.save(os.path.join(L.CACHE, f'X_{arm}_{name}.npy'), V.astype(np.float32))
        X[(arm, name)] = V.astype(np.float64)
        print(f'  embedded {arm}/{name} {V.shape}  total=${E.total_spend():.4f}', flush=True)
meta['spend_embed_usd'] = E.embed_spend()
meta['dim'] = {a: int(X[(a, 'C1')].shape[1]) for a in L.ARMS}

# ---------------------------------------------------------------- V1 / V1b / V4
labels = L.labels_of(rows)


def unit(V):
    n = np.linalg.norm(V, axis=1, keepdims=True)
    return V / np.where(n > 0, n, 1.0)


v1 = {}
for arm in L.ARMS:
    A, B = unit(X[(arm, 'C1')]), unit(X[(arm, 'C1P')])
    cs = (A * B).sum(1)
    per = {}
    for k, kn in enumerate(L.KINDS):
        m = labels == k
        per[kn] = float(np.median(cs[m]))
    unmeasured = [kn for kn, v in per.items() if v > 0.999]
    v1[arm] = {'global_median_cos': float(np.median(cs)),
               'frac_items_above_0.999': float((cs > 0.999).mean()),
               'per_class_median_cos': per,
               'unmeasured_classes': unmeasured,
               'classes_kept': L.NK - len(unmeasured),
               'rank_B': min(L.NK - len(unmeasured), 10),
               'global_VOID': bool(np.median(cs) > 0.999)}
    # V4 near-duplicate ties on the primary cloud
    P = unit(X[(arm, 'C1')])
    G = P @ P.T
    np.fill_diagonal(G, -1.0)
    ties = (G > 0.99)
    v1[arm]['V4'] = {'median_pairwise_cos': float(np.median(G[np.triu_indices(len(P), 1)])),
                     'max_pairwise_cos': float(G.max()),
                     'n_pairs_above_0.99': int(ties.sum() // 2),
                     'frac_items_in_tie_cluster': float((ties.any(1)).mean())}
    print(f'V1 {arm}: median cos(C1,C1P) = {v1[arm]["global_median_cos"]:.5f}; '
          f'unmeasured = {unmeasured}; V4 max cos = {v1[arm]["V4"]["max_pairwise_cos"]:.4f}',
          flush=True)
meta['V1'] = v1
meta['V1b_VOID'] = {a: bool(v1[a]['classes_kept'] < 8) for a in L.ARMS}

# ---------------------------------------------------------------- V3 (class support)
splits = L.make_splits(labels, L.batches_of(rows))
mins = []
for s in range(splits.shape[0]):
    for m in (splits[s], ~splits[s]):
        mins.append(min(int((labels[m] == k).sum()) for k in range(L.NK)))
meta['V3'] = {'min_class_in_any_fitting_half': int(min(mins)), 'floor': 12,
              'fired': bool(min(mins) < 12)}

# ---------------------------------------------------------------- M2 diagnostic (evr)
import pipeline as pl
evr = {}
for arm in L.ARMS:
    e = {}
    for name in ('C1', 'C1P'):
        Xc = unit(X[(arm, name)])
        Xc = Xc - Xc.mean(0)
        s = np.linalg.svd(Xc, compute_uv=False)
        e[name] = float((s[:11] ** 2).sum() / (s ** 2).sum())
    e['ratio_C1_over_C1P'] = e['C1'] / e['C1P']
    evr[arm] = e
meta['evr_top11_fullcloud'] = evr

# ---------------------------------------------------------------- manifest
man = {}
for model in sorted(set(L.ARM_MODEL.values())):
    h, n = E.cache_sha256(model)
    man[model] = {'sha256': h, 'bytes': n}
for arm in L.ARMS:
    for name in ('C1', 'C1P'):
        p = os.path.join(L.CACHE, f'X_{arm}_{name}.npy')
        man[f'X_{arm}_{name}.npy'] = {'sha256': L.sha256_file(p), 'bytes': os.path.getsize(p)}
L.atomic_json(man, os.path.join(L.CACHE, 'MANIFEST.sha256'))
meta['manifest'] = man
meta['seconds'] = time.time() - t0
L.atomic_json(meta, os.path.join(L.OUT, 'embed_meta.json'))
L.done_marker('EMBED', {'artifact': os.path.join(L.OUT, 'embed_meta.json'),
                        'n': len(rows), 'spend_usd': E.total_spend(),
                        'ts': meta['ts']})
print(f'EMBED DONE  n={len(rows)}  spend=${E.total_spend():.4f}  {time.time()-t0:.0f}s',
      flush=True)
