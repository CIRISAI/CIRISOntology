"""S2.4 / S18 step 9: RATCHET AUDIT 1-3 for the record, plus placebo P2 (R-placebo)."""
import json, os, sys
import numpy as np
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import corpora, embed
from run_main import E, PRIMARY, OUT
from common import parallel_analysis_rank

CTX = '/home/emoore/RATCHET/release/data_scrubbed_v1/trace_context.jsonl'
SHIPPED8 = ['csdma_plausibility_score', 'dsdma_domain_alignment', 'entropy_score',
            'coherence_score', 'optimization_veto_entropy_ratio', 'tokens_input',
            'tokens_output', 'processing_ms']
NUM25 = ['attestation_level', 'coherence_level', 'coherence_score', 'conscience_checks_count',
         'cost_cents', 'csdma_plausibility_score', 'dsdma_domain_alignment', 'entropy_level',
         'entropy_score', 'epistemic_humility_certainty', 'id', 'idma_correlation_risk',
         'idma_k_eff', 'llm_calls', 'optimization_veto_entropy_ratio', 'processing_ms',
         'qa_question_num', 't_action_ms', 't_aspdma_ms', 't_conscience_ms', 't_dma_ms',
         't_snap_ms', 'thought_depth', 'tokens_input', 'tokens_output']


def load():
    return [json.loads(l) for l in open(CTX)]


def corr_pca(rows, cols, task_filter=None):
    sel = [r for r in rows if task_filter is None or r.get('task_class') == task_filter]
    M, keep = [], []
    for r in sel:
        v = []
        ok = True
        for c in cols:
            x = r.get(c)
            try:
                x = float(x)
            except (TypeError, ValueError):
                ok = False
                break
            if not np.isfinite(x):
                ok = False
                break
            v.append(x)
        if ok:
            M.append(v)
    M = np.array(M)
    if M.size == 0:
        return None
    sd = M.std(0)
    good = sd > 0
    M = M[:, good]
    Zs = (M - M.mean(0)) / M.std(0)
    Cmat = np.corrcoef(Zs, rowvar=False)
    w = np.sort(np.linalg.eigvalsh(Cmat))[::-1]
    w = np.clip(w, 0, None)
    cum = np.cumsum(w) / w.sum()
    return {'n_rows': int(M.shape[0]), 'n_cols': int(M.shape[1]),
            'cols_used': [c for c, g in zip(cols, good) if g],
            'eigenvalues': [float(x) for x in w],
            'h90': int(np.searchsorted(cum, 0.90) + 1),
            'h99': int(np.searchsorted(cum, 0.99) + 1),
            'participation_ratio': float(w.sum() ** 2 / (w ** 2).sum())}


def main():
    rows = load()
    R = {'n_trace_context': len(rows), 'n_columns': len(set().union(*[set(r) for r in rows]))}
    R['AUDIT1_shipped8_qa_eval'] = corr_pca(rows, SHIPPED8, task_filter='qa_eval')
    R['AUDIT2_all25'] = corr_pca(rows, NUM25)
    R['AUDIT3_shipped8_allrows'] = corr_pca(rows, SHIPPED8)
    rat = [t[:1500] for t in corpora.ratchet_rationales()]   # client-side truncation, see run_ratchet_embed.py
    V = E(rat, PRIMARY)
    V = V / np.linalg.norm(V, axis=1, keepdims=True)
    cnt, ev, thr = parallel_analysis_rank(V, n_perm=50, seed=5)
    R['R_placebo'] = {'n': len(rat), 'parallel_analysis_rank': int(cnt),
                      'top20_eigenvalues': [float(x) for x in ev[:20]],
                      'top20_null_p95': [float(x) for x in thr[:20]],
                      'frac_var_top11': float(ev[:11].sum() / ev.sum()),
                      'n_unique_texts': len(set(rat)),
                      'n_truncated_at_1500': int(sum(1 for t in corpora.ratchet_rationales() if len(t) > 1500))}
    json.dump(R, open(os.path.join(OUT, 'ratchet.json'), 'w'), indent=1, default=str)
    print(json.dumps({k: (v if not isinstance(v, dict) else
                          {kk: vv for kk, vv in v.items() if kk != 'eigenvalues'})
                      for k, v in R.items()}, indent=1)[:3000])


if __name__ == '__main__':
    main()
