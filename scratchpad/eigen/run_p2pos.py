"""S11 P2-pos: does Record surface when the frame is supplied?  Second-moment statistic."""
import json, os, sys, time, collections
import numpy as np
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import corpora, embed, pipeline as pl
from run_main import E, build, zmat_A, keep_mask, PRIMARY, OUT

CONDS = ['BASE', 'F1', 'F2', 'D1', 'D2', 'W2', 'W3']
NDRAW = 2000
SEED = 20260819


def rbar(rows_by, items, cond, stripped, model):
    """(n_items, d) mean of the 3 model vectors for (item, cond); NaN row if absent."""
    texts, where = [], []
    for i, it in enumerate(items):
        for j in rows_by.get((it, cond), []):
            texts.append(j['_txt_s'] if stripped else j['reason'])
            where.append(i)
    V = pl.unit(E(texts, model))
    d = V.shape[1]
    out = np.zeros((len(items), d))
    cnt = np.zeros(len(items))
    for v, i in zip(V, where):
        out[i] += v
        cnt[i] += 1
    ok = cnt > 0
    out[ok] /= cnt[ok][:, None]
    return out, ok


def pistat(Dt, G):
    Dc = Dt - Dt.mean(0)
    den = (Dc ** 2).sum(1).mean()
    num = ((Dc @ G.T) ** 2).mean(0)
    return num / den, Dc, den


def main():
    t0 = time.time()
    A_all = corpora.corpus_A()
    A = [r for r, k in zip(A_all, keep_mask(A_all)) if k]
    items = [r['id'] for r in A]
    labels = np.array([corpora.KIDX[r['kind_target']] for r in A])
    ZA = zmat_A(A)
    cl = build(A, PRIMARY)
    X = cl['delta']
    bA = np.linalg.lstsq(ZA, X, rcond=None)[0]
    Xr = X - ZA @ bA
    P = pl.onehot(labels, 12)
    cnt = P.sum(0)
    S = P.T @ Xr
    tot = Xr.sum(0)
    N = float(len(labels))
    C = S / cnt[:, None] - (tot[None, :] - S) / (N - cnt)[:, None]
    G = C / np.linalg.norm(C, axis=1, keepdims=True)          # the 12 LOKO directions

    aids = set(items)
    J = [j for j in corpora.judgments() if j['id'] in aids and j.get('reason')]
    for j in J:
        j['_txt_s'] = corpora.strip_stoplist(j['reason'])
    by = collections.defaultdict(list)
    for j in J:
        by[(j['id'], j['condition'])].append(j)
    parse = {c: sum(1 for j in J if j['condition'] == c) for c in CONDS}
    tot_expect = len(items) * 3
    R = {'parse_rate': {c: parse[c] / tot_expect for c in CONDS}}
    R['V9'] = {'worst_missing_frac': float(max(1 - parse[c] / tot_expect for c in CONDS)),
               'fired': bool(max(1 - parse[c] / tot_expect for c in CONDS) > 0.05)}
    R['stoplist_touch_frac'] = float(np.mean([j['_txt_s'] != j['reason'] for j in J]))

    for stripped in (True, False):
        tag = 'stripped' if stripped else 'unstripped'
        rb, ok = {}, {}
        for c in CONDS:
            rb[c], ok[c] = rbar(by, items, c, stripped, PRIMARY)
        good = np.all([ok[c] for c in CONDS], axis=0)
        res = {'n_items': int(good.sum())}
        Draw = {'frame': rb['F2'][good] - rb['BASE'][good],
                'design': rb['D2'][good] - rb['BASE'][good],
                'warrant': rb['W3'][good] - rb['BASE'][good]}
        pis, dens, norms = {}, {}, {}
        for T, Dt in Draw.items():
            p, Dc, den = pistat(Dt, G)
            pis[T] = p
            dens[T] = float(den)
            norms[T] = float(np.median(np.linalg.norm(Dc, axis=1)))
            res[f'raw_energy_{T}'] = float((Dt ** 2).sum(1).mean())
        res['pi'] = {T: pis[T].tolist() for T in pis}
        res['median_centred_norm'] = norms
        res['V6'] = {'ratio_frame_over_warrant': norms['frame'] / norms['warrant'],
                     'fired': bool(norms['frame'] <= 1.1 * norms['warrant'])}
        res['V6b'] = {'item_specific_energy_frac':
                      float(dens['frame'] / ((Draw['frame'] ** 2).sum(1).mean())),
                      'fired': bool(dens['frame'] / ((Draw['frame'] ** 2).sum(1).mean()) < 0.05)}
        # N3 any-swap floor: per item an independent random ordered distinct condition pair
        rng = np.random.default_rng(SEED + 31)
        M = np.stack([rb[c][good] for c in CONDS])
        n = M.shape[1]
        null = np.zeros((NDRAW, 12))
        for b in range(NDRAW):
            c1 = rng.integers(0, 7, n)
            off = rng.integers(1, 7, n)
            c2 = (c1 + off) % 7
            Dr = M[c2, np.arange(n)] - M[c1, np.arange(n)]
            null[b] = pistat(Dr, G)[0]
        res['N3_p95'] = np.percentile(null, 95, axis=0).tolist()
        res['N3_p99'] = np.percentile(null, 99, axis=0).tolist()
        res['p_vs_N3'] = {T: [float((1 + (null[:, k] >= pis[T][k]).sum()) / (1 + NDRAW))
                              for k in range(12)] for T in pis}
        ri = corpora.KIDX[corpora.RECORD]
        res['record_idx'] = ri
        res['record_is_largest'] = bool(int(np.argmax(pis['frame'])) == ri)
        res['argmax_frame'] = corpora.KINDS[int(np.argmax(pis['frame']))]
        R[tag] = res
        print(tag, 'pi_frame Record=%.5f rank=%d/12  p=%.4f' % (
            pis['frame'][ri], int(np.where(np.argsort(-pis['frame']) == ri)[0][0]) + 1,
            res['p_vs_N3']['frame'][ri]), flush=True)
    R['kinds'] = corpora.KINDS
    json.dump(R, open(os.path.join(OUT, 'p2pos.json'), 'w'), indent=1, default=str)
    print('elapsed', time.time() - t0)


if __name__ == '__main__':
    main()
