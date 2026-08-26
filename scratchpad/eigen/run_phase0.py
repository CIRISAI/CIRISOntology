"""EIGEN v2 PHASE 0 — construction bake-off (INSTRUMENT CALIBRATION ONLY).

Corpus A is SPENT: v1 already read it.  Nothing here is a taxonomy verdict.  The single
question is which change-reading construction gives the best null-separated Omega(11)
that also beats its own placebo, so that v2's prereg can stake ONE instrument.

Constructions (each -> one n x d matrix over the same 247 items, same 200 splits):
  C1  span-in-context, ONE embedding of "A passage changed. Before: <s_b> After: <s_a>"
  C2  concatenated pair [unit e(s_b) ; unit e(s_a)] / sqrt2      (NO subtraction)
  C3  e(after doc) residualized on e(before doc) by per-split reduced-rank regression
  C4  v1 baseline unit( unit e(after doc) - unit e(before doc) )
Placebos (context-only / before-only; the K1c generalisation):
  C1p same rendering with the AFTER slot filled by the BEFORE sentence
  C2p [unit e(s_b) ; unit e(s_b)] / sqrt2
  C3p, C4p the before-document cloud (exactly v1's K1c placebo)

Embedder arms: bge (v1 primary) and Qwen3-0.6B with a change-kind instruction prefix.

SELECTION RULE (calibration heuristic, not a claim about the world):
  a construction PASSES iff
    (a) p_N1(Omega(11)) <= 0.01                         -- beats the label-permutation floor
    (b) sign-flip paired test on the per-split obs-placebo difference: p <= 0.05, median > 0
    (c) p_gap_N1 <= 0.01 -- the construction-MINUS-placebo gap beats its OWN label-permutation
        floor (the same permutations drive both arms, so this is properly paired)
  Ties broken on Omega(11).
DISCLOSURE: (c) was added after a 3-permutation smoke run had shown the Omega and placebo-
Omega values (which are deterministic and carry no p-value).  No p-value at the run's
permutation count had been seen when the rule was fixed.
"""
import json, os, sys, time
import numpy as np

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import corpora, embed, pipeline as pl, phase0_span as ps
from common import maxt_stepdown  # noqa: F401  (kept for parity with run_main)

OUT = '/home/emoore/CIRISOntology/scratchpad/eigen/out'
BGE = 'BAAI/bge-large-en-v1.5'
QWEN = 'Qwen/Qwen3-Embedding-0.6B'
NSPLIT = 200
NPERM = int(os.environ.get('PHASE0_NPERM', '500'))
SEED = 20260819              # v1's split seed, reused verbatim
NBEFORE_PC = 20              # C3's reduced-rank before-basis (pinned in advance)
CAP_USD = 1.00
KS = pl.KS
JMAX = pl.JMAX

ARMS = os.environ.get('PHASE0_ARMS', 'bge,qwen').split(',')
CONS = os.environ.get('PHASE0_CONS', 'C1,C2,C3,C4').split(',')
MERGE = os.environ.get('PHASE0_MERGE') == '1'

R = {'_meta': {'nsplit': NSPLIT, 'nperm': NPERM, 'seed': SEED,
               'nbefore_pc': NBEFORE_PC, 'cap_usd': CAP_USD,
               'label': 'CALIBRATION ONLY - corpus A is spent, no taxonomy verdict',
               'selection_rule': 'PASS iff p_N1(Omega11)<=0.01 AND sign-flip paired '
                                 'p<=0.05 with median diff>0 AND p_gap_N1<=0.01'}}


def save():
    json.dump(R, open(os.path.join(OUT, 'phase0_bakeoff.json'), 'w'), indent=1, default=str)


def E(texts, model):
    return embed.embed(texts, model, cap_usd=CAP_USD, verbose=False).astype(np.float64)


def unit(V):
    n = np.linalg.norm(V, axis=-1, keepdims=True)
    n = np.where(n > 0, n, 1.0)
    return V / n


def reduce_dim(X, tol=1e-10):
    """Exact orthonormal re-coordinatisation onto the row space of X.

    Omega, the held-out PCA and the centroid contrasts are all invariant under an
    orthonormal change of basis of any subspace containing every row of X, and every
    quantity the pipeline forms from X (means, residuals X - Z beta with beta fit by
    least squares on rows of X, centred SVDs) stays inside that row space.  This is a
    lossless 1024 -> <=247 compression, verified by reproducing v1's C4 Omega exactly.
    """
    u, s, vt = np.linalg.svd(X, full_matrices=False)
    keep = s > s.max() * tol
    Q = vt[keep].T
    return X @ Q, int(keep.sum())


# ---------------------------------------------------------------- per-sd machinery
class PreparedSD:
    """Like pipeline.Prepared but X already differs per split-direction (C3)."""

    def __init__(self, Xsd, splits, jmax=JMAX):
        self.Xsd = Xsd
        nsd, n, d = Xsd.shape
        self.nsd, self.n, self.d = nsd, n, d
        S = splits.shape[0]
        self.S = S
        Hf = np.zeros((nsd, n))
        for s in range(S):
            Hf[2 * s] = splits[s].astype(float)
            Hf[2 * s + 1] = (~splits[s]).astype(float)
        self.Hf = Hf
        self.U = np.zeros((nsd, d, jmax))
        self.evr = np.zeros((nsd, jmax))
        for sd in range(nsd):
            E_ = Hf[sd] == 0
            Xe = Xsd[sd][E_]
            Xe = Xe - Xe.mean(0)
            u, s_, vt = np.linalg.svd(Xe, full_matrices=False)
            k = min(jmax, vt.shape[0])
            self.U[sd, :, :k] = vt[:k].T
            ev = s_ ** 2
            self.evr[sd, :k] = ev[:k] / ev.sum()


def contrasts_sd(prep, P):
    W = prep.Hf[:, None, :] * P.T[None, :, :]          # (nsd,K,n)
    cnt = W.sum(axis=2)
    SX = np.matmul(W, prep.Xsd)                        # (nsd,K,d)
    tot = cnt.sum(axis=1)
    TX = SX.sum(axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        mX = SX / cnt[:, :, None]
        nX = (TX[:, None, :] - SX) / (tot[:, None] - cnt)[:, :, None]
    C = mX - nX
    C[cnt == 0] = 0.0
    return C


def stats_sd(prep, P):
    C = contrasts_sd(prep, P)
    om, a, r = pl.omega_a_batch(C, prep.U)
    return {'omega': {k: float(np.median(pl.split_reduce(v))) for k, v in om.items()},
            'omega_splits': {k: pl.split_reduce(v) for k, v in om.items()},
            'rank': float(np.median(r))}


def stats_std(prep, P):
    return pl.full_stats(prep, P, want_eta=False)


# ---------------------------------------------------------------- one arm
def run_arm(prep, labels, K, tag, statfn, nperm=NPERM, seed=SEED):
    t0 = time.time()
    obs = statfn(prep, pl.onehot(labels, K))
    pm = pl.perm_labels(labels, nperm, seed)
    nullom = {k: [] for k in obs['omega']}
    for b in range(nperm):
        s = statfn(prep, pl.onehot(pm[b], K))
        for k in nullom:
            nullom[k].append(s['omega'][k])
        if (b + 1) % 100 == 0:
            print(f'    [{tag}] {b+1}/{nperm}  {time.time()-t0:.0f}s', flush=True)
    nullom = {k: np.array(v) for k, v in nullom.items()}
    out = {'omega': obs['omega'], 'rank_B': obs['rank'],
           'omega11_ci': [float(np.percentile(obs['omega_splits'][11], 2.5)),
                          float(np.percentile(obs['omega_splits'][11], 97.5))],
           'null_median': {k: float(np.median(v)) for k, v in nullom.items()},
           'null_p99': {k: float(np.percentile(v, 99)) for k, v in nullom.items()},
           'p_N1': {k: pl.perm_p(obs['omega'][k], nullom[k]) for k in nullom},
           'evr_top11': float(np.median(prep.evr[:, :11].sum(axis=1))),
           'seconds': time.time() - t0}
    return out, obs['omega_splits'][11], nullom[11]


def paired(d, nperm=10000, seed=11):
    """Sign-flip randomisation on the per-split difference (v1's K1c test)."""
    rng = np.random.default_rng(seed)
    sgn = rng.choice([-1.0, 1.0], size=(nperm, len(d)))
    nullmed = np.median(sgn * d[None, :], axis=1)
    med = float(np.median(d))
    return {'median_diff': med,
            'p_paired': float((1 + int((nullmed >= med).sum())) / (1 + nperm)),
            'frac_splits_gt': float((d > 0).mean())}


# ---------------------------------------------------------------- main
def main():
    t00 = time.time()
    spend0 = embed.total_spend()
    if MERGE and os.path.exists(os.path.join(OUT, 'phase0_bakeoff.json')):
        prev = json.load(open(os.path.join(OUT, 'phase0_bakeoff.json')))
        R['cells'] = prev.get('cells', {})
        R['cloud_diag'] = prev.get('cloud_diag', {})
        R['_meta'] = {**prev.get('_meta', {}), **R['_meta']}
        print(f'MERGE: {len(R["cells"])} cells already on disk', flush=True)

    A_all = ps.attach(corpora.corpus_A())
    # PINNED item set: v1's, so every cell sits on identical items and identical splits.
    dropped = json.load(open(os.path.join(OUT, 'main_primary.json')))['degenerate_items_dropped']
    A = [r for r in A_all if r['id'] not in dropped]
    R['_meta']['n_items'] = len(A)
    R['_meta']['items_dropped_from_v1'] = dropped
    labels = np.array([corpora.KIDX[r['kind_target']] for r in A])
    strata = [(r['kind_target'], r['domain']) for r in A]
    splits = pl.make_splits(strata, NSPLIT, SEED)

    # v1's nuisance matrix, verbatim: [1, log10(1+span_chars_v1), domain(4), part(2)]
    def dummies(vals):
        u = sorted(set(vals))[1:]
        return np.array([[1.0 if v == c else 0.0 for c in u] for v in vals])

    sp = np.log10(1.0 + np.array([r['span_chars'] for r in A]))
    Zbase = np.column_stack([np.ones(len(A)), sp,
                             dummies([r['domain'] for r in A]),
                             dummies([r['part'] for r in A])])
    R['_meta']['z_cols'] = Zbase.shape[1]

    # ---------------- texts (mechanical only; no authored field is read) ----------
    ctx_b = [r['ctx_before'] for r in A]
    ctx_a = [r['ctx_after'] for r in A]
    doc_b = [r['before'] for r in A]
    doc_a = [r['after'] for r in A]
    c1 = [ps.c1_text(b, a) for b, a in zip(ctx_b, ctx_a)]
    c1p = [ps.c1_text(b, b) for b in ctx_b]
    R['_meta']['example_c1'] = c1[0]
    R['_meta']['example_c1_placebo'] = c1p[0]

    texts = {'ctx_b': ctx_b, 'ctx_a': ctx_a, 'doc_b': doc_b, 'doc_a': doc_a,
             'c1': c1, 'c1p': c1p}

    print('embedding...', flush=True)
    SPEC = {'bge': (BGE, lambda t: t),
            'qwen': (QWEN, ps.qwen),
            'qwen_noinstr': (QWEN, lambda t: t)}
    Vec = {}
    for emb_name in ARMS:
        model, pre = SPEC[emb_name]
        for key, tt in texts.items():
            Vec[(emb_name, key)] = E([pre(t) for t in tt], model)
            print(f'  {emb_name}/{key} done  spend=${embed.total_spend():.4f}', flush=True)
    R['_meta']['arms'] = sorted(set(R['_meta'].get('arms', [])) | set(ARMS))
    R['_meta']['spend_usd_total'] = embed.total_spend()
    save()

    # ---------------- clouds ------------------------------------------------------
    def clouds(e):
        ub, ua = unit(Vec[(e, 'doc_b')]), unit(Vec[(e, 'doc_a')])
        sb, sa = unit(Vec[(e, 'ctx_b')]), unit(Vec[(e, 'ctx_a')])
        dun = ua - ub
        deg = int((np.linalg.norm(dun, axis=1) == 0).sum())
        return {
            'C1': unit(Vec[(e, 'c1')]),
            'C1p': unit(Vec[(e, 'c1p')]),
            'C2': np.hstack([sb, sa]) / np.sqrt(2.0),
            'C2p': np.hstack([sb, sb]) / np.sqrt(2.0),
            'C3_after': ua, 'C3_before': ub,
            'C4': unit(dun),
            # C5 is an ADDITION beyond the brief's four: v1's difference vector taken at
            # the SENTENCE granularity instead of the document's.  It is the control that
            # separates "subtraction cancels the site cues" from "the document is the
            # wrong unit" -- the two halves of the design doc's defect 1.
            'C5': unit(sa - sb),
            'BEFORE': ub,
            '_degenerate_delta_rows': deg,
            '_median_cos_ba': float(np.median((ub * ua).sum(1))),
            '_median_cos_ctx': float(np.median((sb * sa).sum(1))),
        }

    R.setdefault('cells', {})
    for e in ARMS:
        CL = clouds(e)
        R.setdefault('cloud_diag', {})[e] = {
            'degenerate_delta_rows': CL['_degenerate_delta_rows'],
            'median_cos_before_after_doc': CL['_median_cos_ba'],
            'median_cos_before_after_ctx': CL['_median_cos_ctx']}
        save()

        # placebo preps, shared where the cloud is shared
        Xbef, r_bef = reduce_dim(CL['BEFORE'])
        prep_bef = {'res': pl.Prepared(Xbef, Zbase, splits),
                    'raw': pl.Prepared(Xbef, Zbase, splits, residualize=False)}
        pl_splits_cache = {}
        placebo_cache = {}

        def placebo_run(pkey, prep_p, statfn_p, tag):
            if pkey not in placebo_cache:
                placebo_cache[pkey] = run_arm(prep_p, labels, 12, tag + '.placebo', statfn_p)
            return placebo_cache[pkey]

        for cons in CONS:
            for nuis in ('res', 'raw'):
                tag = f'{cons}.{e}.{nuis}'
                if MERGE and tag in R['cells']:
                    print(f'== {tag} == (already present, skipped)', flush=True)
                    continue
                print(f'== {tag} ==', flush=True)
                if cons == 'C3':
                    # reduced-rank before-basis (label-free), then per-sd regression
                    Bc = CL['C3_before'] - CL['C3_before'].mean(0)
                    Vb = np.linalg.svd(Bc, full_matrices=False)[2][:NBEFORE_PC].T
                    Zb = Bc @ Vb
                    Zb = Zb / Zb.std(0)
                    Z = np.column_stack([Zbase, Zb]) if nuis == 'res' else \
                        np.column_stack([np.ones(len(A)), Zb])
                    Xa, r_dim = reduce_dim(CL['C3_after'])
                    nsd = 2 * NSPLIT
                    Xsd = np.zeros((nsd, len(A), Xa.shape[1]))
                    for s in range(NSPLIT):
                        for half, F in ((0, splits[s]), (1, ~splits[s])):
                            beta = np.linalg.lstsq(Z[F], Xa[F], rcond=None)[0]
                            Xsd[2 * s + half] = unit(Xa - Z @ beta)
                    prep = PreparedSD(Xsd, splits)
                    statfn = stats_sd
                    prep_p, pkey = prep_bef[nuis], ('BEFORE', nuis)
                    statfn_p = stats_std
                    extra = {'before_pc': NBEFORE_PC, 'z_cols': Z.shape[1],
                             'before_evr_top20': float(
                                 (np.linalg.svd(Bc, compute_uv=False)[:NBEFORE_PC] ** 2).sum()
                                 / (np.linalg.svd(Bc, compute_uv=False) ** 2).sum())}
                else:
                    X, r_dim = reduce_dim(CL[cons])
                    key = (cons, nuis)
                    if key not in pl_splits_cache:
                        pl_splits_cache[key] = pl.Prepared(
                            X, Zbase, splits, residualize=(nuis == 'res'))
                    prep = pl_splits_cache[key]
                    statfn = stats_std
                    if cons in ('C1', 'C2', 'C5'):
                        # C5's placebo is the before-SENTENCE cloud (C2p), matching its
                        # granularity, exactly as C4's is the before-DOCUMENT cloud.
                        pname = 'C2p' if cons == 'C5' else cons + 'p'
                        pkey = (pname, nuis)
                        if pkey not in pl_splits_cache:
                            Xp, _ = reduce_dim(CL[pname])
                            pl_splits_cache[pkey] = pl.Prepared(
                                Xp, Zbase, splits, residualize=(nuis == 'res'))
                        prep_p = pl_splits_cache[pkey]
                    else:
                        prep_p, pkey = prep_bef[nuis], ('BEFORE', nuis)
                    statfn_p = stats_std
                    extra = {}

                res, om_splits, nl_c = run_arm(prep, labels, 12, tag, statfn)
                res.update(extra)
                res['d_eff'] = int(r_dim)
                pres, om_p, nl_p = placebo_run(pkey, prep_p, statfn_p, tag)
                res['placebo'] = {'omega': pres['omega'], 'rank_B': pres['rank_B'],
                                  'p_N1': pres['p_N1'], 'null_median': pres['null_median']}
                res['placebo_paired'] = paired(om_splits - om_p)
                # sharper bar: the SAME label permutations drive both arms, so the
                # construction-minus-placebo gap gets its own rule-5 permutation floor.
                obs_gap = res['omega'][11] - pres['omega'][11]
                gap_null = nl_c - nl_p
                res['gap'] = {
                    'obs': float(obs_gap),
                    'null_median': float(np.median(gap_null)),
                    'null_p99': float(np.percentile(gap_null, 99)),
                    'p_gap_N1': float((1 + int((gap_null >= obs_gap).sum())) / (1 + NPERM)),
                    'omega_minus_null': float(res['omega'][11] - res['null_median'][11]),
                    'placebo_omega_minus_null': float(
                        pres['omega'][11] - pres['null_median'][11])}
                ok_null = res['p_N1'][11] <= 0.01
                ok_plac = (res['placebo_paired']['p_paired'] <= 0.05
                           and res['placebo_paired']['median_diff'] > 0
                           and res['gap']['p_gap_N1'] <= 0.01)
                res['verdict'] = ('PASS' if (ok_null and ok_plac)
                                  else ('FAIL:null' if not ok_null else 'FAIL:placebo'))
                R['cells'][tag] = res
                print(f'   -> Omega11={res["omega"][11]:.4f} rank={res["rank_B"]:.0f} '
                      f'null={res["null_median"][11]:.4f} p={res["p_N1"][11]:.4f} '
                      f'placebo={pres["omega"][11]:.4f} '
                      f'pp={res["placebo_paired"]["p_paired"]:.4f} '
                      f'gap={res["gap"]["obs"]:+.4f} p_gap={res["gap"]["p_gap_N1"]:.4f} '
                      f'{res["verdict"]}', flush=True)
                save()

    R['_meta']['elapsed_s'] = time.time() - t00
    R['_meta']['spend_usd_total'] = embed.total_spend()
    R['_meta']['spend_usd_this_phase'] = embed.total_spend() - spend0
    save()
    print('DONE', time.time() - t00, flush=True)


if __name__ == '__main__':
    main()
