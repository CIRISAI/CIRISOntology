"""S12 — the mechanical positive control (VG2).

Three mutation families applied mechanically to E2 `before` texts (no authored field, no
label, no annotation), restricted to the items where ALL THREE triggers exist so that each
item contributes exactly one text to each class and topic is exactly balanced across
classes by construction.

Staked: Omega_PC(k=3) beats its own N1 null at p <= 0.01 AND leave-one-out
nearest-contrast top-1 accuracy >= 0.60 (chance 1/3).  Class = mutation family, rank(B) = 2.
Failure of either -> VG2 fires -> VOID-AS-INSTRUMENT.  VOID if N < 60.

AMENDMENTS.md A4: the gate is the literal N1 (free permutation); a within-item permutation
is reported beside it, and splits are drawn over ITEMS so an item's three renderings never
straddle a split.
"""
import json, os, re, sys, time

import numpy as np

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen2run')
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import e2lib as L
import e2embed as E
import pipeline as pl
import phase0_span as ps

MODALS = {'may': 'must', 'should': 'must', 'must': 'may', 'will': 'may', 'can': 'must'}
RE_MODAL = re.compile(r'\b(may|should|must|will|can)\b', re.I)
RE_NUM = re.compile(r'(?<![\w.])(\d+(?:\.\d+)?)(?![\w.])')
RE_NEG = re.compile(r' (is|are|does) ')


def m1(t):
    m = RE_MODAL.search(t)
    if not m:
        return None
    w = m.group(1)
    sub = MODALS[w.lower()]
    if w[0].isupper():
        sub = sub.capitalize()
    return t[:m.start(1)] + sub + t[m.end(1):]


def m2(t):
    m = RE_NUM.search(t)
    if not m:
        return None
    s = m.group(1)
    if '.' in s:
        dec = len(s.split('.')[1])
        new = f'{float(s) + 7:.{dec}f}'
    else:
        new = str(int(s) + 7)
    return t[:m.start(1)] + new + t[m.end(1):]


def m3(t):
    m = RE_NEG.search(t)
    if not m:
        return None
    w = m.group(1)
    if w == 'does':
        return t[:m.end(1)] + ' not' + t[m.end(1):]
    return t[:m.end(0)] + 'not ' + t[m.end(0):]


FAM = [('M1_modal', m1), ('M2_numeral', m2), ('M3_negation', m3)]


def main():
    t0 = time.time()
    rows_all = L.load_e2()
    meta = json.load(open(os.path.join(L.OUT, 'embed_meta.json')))
    dropped = set(meta['V7']['dropped_ids'])
    rows = [r for r in rows_all if r['id'] not in dropped]

    trig = {n: [] for n, _ in FAM}
    for i, r in enumerate(rows):
        for n, f in FAM:
            if f(r['before']) is not None:
                trig[n].append(i)
    inter = sorted(set(trig['M1_modal']) & set(trig['M2_numeral']) & set(trig['M3_negation']))
    R = {'trigger_marginals': {n: len(v) for n, v in trig.items()},
         'intersection_n': len(inter), 'prereg_measured': {'M1': 272, 'M2': 208, 'M3': 451,
                                                           'intersection': 95},
         'n_corpus': len(rows), 'ts': time.strftime('%Y-%m-%dT%H:%M:%S')}
    print(f'triggers {R["trigger_marginals"]}  intersection {len(inter)}', flush=True)

    texts, fam_lab, item_lab = [], [], []
    for j, i in enumerate(inter):
        r = rows[i]
        for fi, (n, f) in enumerate(FAM):
            mut = f(r['before'])
            cb, ca, _ = ps.context_pair(r['before'], mut)
            texts.append(ps.c1_text(cb, ca))
            fam_lab.append(fi)
            item_lab.append(j)
    fam_lab = np.array(fam_lab)
    item_lab = np.array(item_lab)

    # the control's own truncation pass (S12): drop an item if ANY of its four texts
    # exceeds any arm's context.  Token counts via the same tokenizers as S3.4.
    tp = os.path.join(L.OUT, 'poscontrol_tokens.json')
    if not os.path.exists(tp):
        import subprocess
        pre = [ps.qwen(t) for t in texts]
        before_win = [ps.context_pair(rows[i]['before'], rows[i]['before'])[0] for i in inter]
        payload = {'texts': texts, 'texts_qwen': pre, 'before_windows': before_win}
        L.atomic_json(payload, os.path.join(L.OUT, 'poscontrol_texts.json'))
        subprocess.run(['python3', os.path.join(L.RUN, 'poscontrol_tokens.py')], check=True)
    tk = json.load(open(tp))
    R['token_max'] = tk['max']
    bad_items = set(tk['over_items'])
    R['control_dropped_items'] = sorted(bad_items)
    keep = np.array([k for k in range(len(texts)) if item_lab[k] not in bad_items])
    texts = [texts[k] for k in keep]
    fam_lab, item_lab = fam_lab[keep], item_lab[keep]
    N = len(set(item_lab.tolist()))
    R['N'] = N
    R['VOID_N_below_60'] = bool(N < 60)
    if R['VOID_N_below_60']:
        L.atomic_json(R, os.path.join(L.OUT, 'poscontrol.json'))
        raise SystemExit('VG2: N < 60 — VOID')

    # relabel items 0..N-1
    remap = {v: i for i, v in enumerate(sorted(set(item_lab.tolist())))}
    item_lab = np.array([remap[v] for v in item_lab])

    NSPLIT, NPERM = 200, 500
    rng = np.random.default_rng(L.SEED)
    isplits = np.zeros((NSPLIT, N), dtype=bool)
    for s in range(NSPLIT):
        idx = rng.permutation(N)
        isplits[s, idx[:N // 2]] = True
    splits = isplits[:, item_lab]

    R['arms'] = {}
    for arm in ['qwen', 'bge']:
        model = L.ARM_MODEL[arm]
        V = E.embed([L.arm_prefix(arm, t) for t in texts], model, tag=f'PC/{arm}')
        X = V.astype(np.float64)
        X /= np.linalg.norm(X, axis=1, keepdims=True)
        Xr = X @ np.linalg.svd(X, full_matrices=False)[2].T
        Z = np.ones((len(X), 1))
        prep = pl.Prepared(Xr, Z, splits, residualize=False)
        obs = pl.full_stats(prep, pl.onehot(fam_lab, 3), ks=[3], want_eta=False)
        nulls, nulls_wi = [], []
        rg = np.random.default_rng(99)
        for b in range(NPERM):
            nulls.append(pl.full_stats(prep, pl.onehot(rg.permutation(fam_lab), 3),
                                       ks=[3], want_eta=False)['omega'][3])
            wi = fam_lab.copy()
            for it in range(N):
                m = item_lab == it
                wi[m] = rg.permutation(fam_lab[m])
            nulls_wi.append(pl.full_stats(prep, pl.onehot(wi, 3), ks=[3],
                                          want_eta=False)['omega'][3])
        nulls = np.array(nulls)
        nulls_wi = np.array(nulls_wi)
        p = float((1 + int((nulls >= obs['omega'][3]).sum())) / (1 + NPERM))
        pwi = float((1 + int((nulls_wi >= obs['omega'][3]).sum())) / (1 + NPERM))

        sc = pl.loo_auc_scores(X, fam_lab, 3)
        top1 = float((sc.argmax(1) == fam_lab).mean())
        # stricter: leave-one-ITEM-out
        correct = 0
        for it in range(N):
            m = item_lab != it
            P = pl.onehot(fam_lab[m], 3)
            S = P.T @ X[m]
            cnt = P.sum(0)
            tot = X[m].sum(0)
            C = S / cnt[:, None] - (tot[None, :] - S) / (len(X[m]) - cnt)[:, None]
            C /= np.linalg.norm(C, axis=1, keepdims=True)
            q = item_lab == it
            correct += int(((X[q] @ C.T).argmax(1) == fam_lab[q]).sum())
        top1_item = correct / int((item_lab < N).sum())

        R['arms'][arm] = {
            'omega_PC_3': obs['omega'][3], 'rank_B': obs['rank'],
            'null_median': float(np.median(nulls)), 'p_N1': p,
            'exceedances': int((nulls >= obs['omega'][3]).sum()),
            'null_median_within_item': float(np.median(nulls_wi)),
            'p_within_item': pwi,
            'loo_top1': top1, 'loo_top1_leave_one_item_out': top1_item,
            'chance': 1 / 3,
            'PASS': bool(p <= 0.01 and top1 >= 0.60)}
        print(f'PC {arm}: Om3={obs["omega"][3]:.4f} p={p:.4f} (within-item {pwi:.4f}) '
              f'top1={top1:.3f} (item-LOO {top1_item:.3f}) '
              f'-> {"PASS" if R["arms"][arm]["PASS"] else "FAIL"}', flush=True)
        L.atomic_json(R, os.path.join(L.OUT, 'poscontrol.json'))

    R['VG2_FIRED'] = bool(not R['arms']['qwen']['PASS'])
    R['VG2_note'] = ('the gate is read on the PRIMARY embedder; the witness arm is '
                     'reported beside it')
    R['seconds'] = time.time() - t0
    R['spend_usd'] = E.total_spend()
    L.atomic_json(R, os.path.join(L.OUT, 'poscontrol.json'))
    L.done_marker('POSCTRL', {'artifact': os.path.join(L.OUT, 'poscontrol.json'),
                              'VG2_FIRED': R['VG2_FIRED'], 'N': N})
    print(f'POSCTRL DONE VG2_FIRED={R["VG2_FIRED"]} [{time.time()-t0:.0f}s]', flush=True)


if __name__ == '__main__':
    main()
