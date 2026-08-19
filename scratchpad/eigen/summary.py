import json, sys, numpy as np
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import corpora
P = '/home/emoore/CIRISOntology/scratchpad/eigen/out/'
M = json.load(open(P + 'main_primary.json'))
K = corpora.KINDS
PL = corpora.PLAIN
print('n_A =', M['n_A'], ' dropped:', M.get('degenerate_items_dropped'))
print('split min class n =', M['split_class_min'], ' V3 fired', M['V3']['fired'])
print('V1 unmeasured:', M['V1']['unmeasured'], 'global median cos %.5f' % M['V1']['global_median_cos'])
print('per-class cos(before,after):')
for k in K:
    print('   %-12s %-13s cos=%.5f  ||d||=%.4f' % (k, PL[k], M['V1']['per_class'][k]['median_cos_ba'],
                                                   M['V1']['per_class'][k]['median_norm_delta_un']))
p = M['P1a']
print('\nP1a: rank(B)=%s  Omega(11)=%.4f  CI=[%.4f, %.4f]' % (p['rank_B'], p['omega']['11'] if '11' in p['omega'] else p['omega'][11], *p['omega11_ci']))
print('   p_N1=%.4g  p_N1b=%.4g  null medians %.4f / %.4f  null p99=%.4f' % (
    p['p_N1'], p['p_N1b'], p['null_N1_median'], p['null_N1b_median'], p['null_N1_p99']))
print('   Omega by k:', {k: round(float(v), 4) for k, v in p['omega'].items()})
print('   p_N1 by k:', {k: round(float(v), 4) for k, v in p['p_N1_by_k'].items()})
print('   evr_top11 = %.4f' % p['evr_top11'])
print('   span decile descriptive:', {k: (v['median_span_chars'], round(v['mean_kind_subspace_loading'], 4))
                                      for k, v in p['span_decile_descriptive'].items()})
b = M['P1b']
print('\nP1b: R_kind(N1)=%d  R_kind(N1b)=%d' % (b['R_kind_N1'], b['R_kind_N1b']))
print('   a_obs[0:15] =', [round(x, 4) for x in b['a_obs'][:15]])
print('   a_null[0:15]=', [round(x, 4) for x in b['a_null_median'][:15]])
print('   padj[0:15]  =', [round(x, 4) for x in b['padj'][:15]])
n4 = M['N4']
print('\nN4: Om_tax=%.4f Om_kmeans=%.4f Om_nontax=%.4f (levels %d, rank %s/%s)' % (
    n4['omega_taxonomy'], n4['omega_kmeans'], n4['omega_nontaxonomy'], n4['nontax_levels'],
    n4['rank_kmeans'], n4['rank_nontax']))
print('   p(tax>nontax)=%.4g  meandiff=%.4f  frac splits=%.3f  gap kmeans-tax=%.4f' % (
    n4['p_tax_gt_nontax'], n4['mean_diff_tax_minus_nontax'], n4['frac_splits_tax_gt_nontax'],
    n4['gap_kmeans_minus_tax']))
q = M['P2neg']
print('\nP2-neg LOKO table (eta = A * rho):')
print('   %-13s %-13s %8s %8s %8s %10s %8s' % ('kind', 'plain', 'eta', 'A', 'rho', 'eta_p95', 'A_loko'))
for i, k in enumerate(K):
    print('   %-13s %-13s %8.4f %8.4f %8.4f %10.4f %8.4f' % (
        k, PL[k], q['eta'][i], q['A'][i], q['rho'][i], q['eta_null_p95'][i], q['A_loko_excluded'][i]))
print('   base kinds > p95: %d/11   Record>p95 %s  Record>p99 %s  rank(asc) %d/12' % (
    q['base_kinds_exceeding_p95'], q['record_exceeds_p95'], q['record_exceeds_p99'],
    q['record_rank_ascending']))
print('   rho_Record=%.4f  A_Record=%.4f  median A base=%.4f' % (q['rho_record'], q['A_record'], q['A_median_base']))
print('   V5 fired', M['V5']['fired'], ' V5b fired', M['V5b']['fired'], 'auc_upper=%.3f' % M['V5b']['auc_record_ci_upper'])
print('\nAUC (LOO, residualized / raw):')
for k in K:
    a1 = M['AUC_residualized'][k]
    a2 = M['AUC_raw'][k]
    print('   %-13s %-13s res %.3f [%.3f,%.3f]   raw %.3f [%.3f,%.3f]' % (
        k, PL[k], a1['auc'], *a1['ci95'], a2['auc'], *a2['ci95']))
c = M['K1c']
print('\nK1c placebo: Om_delta=%.4f Om_before=%.4f diff=%.4f p=%.4g frac=%.3f' % (
    c['omega_delta'], c['omega_before'], c['median_diff'], c['p_paired'], c['frac_splits_delta_gt_before']))
print('\nP1a-batch:', json.dumps(M['P1a_batch'], indent=1))
print('V11 both fail:', M['V11']['both_within_batch_fail'])
print('\narms:', json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'eta'}
                             for k, v in M['arms'].items()}, indent=1))
try:
    X = json.load(open(P + 'extras.json'))
    for tag in ['primary', 'secondary']:
        e = X[tag]
        print(f'\n--- {tag} ---')
        print(' P1c:', {k: v for k, v in e['P1c'].items() if k not in ('V4',)})
        print(' V4:', json.dumps(e['P1c']['V4']))
        print(' babel:', e['babel']['top1_correct'], '/10 p_perm=%.4f p_binom=%.4f' % (
            e['babel']['p_permutation'], e['babel']['p_binomial_ge']))
        print(' partd:', e['partd']['top1_correct'], '/12', e['partd']['kinds_covered'])
        if 'P1a' in e:
            print(' P1a:', e['P1a'])
            print(' P2neg:', {k: v for k, v in e['P2neg'].items() if k in
                              ('base_exceed', 'record_exceeds_p95', 'record_rank_ascending')})
            print('  eta:', [round(x, 4) for x in e['P2neg']['eta']])
            print('  p95:', [round(x, 4) for x in e['P2neg']['eta_null_p95']])
except FileNotFoundError:
    print('\n(extras.json not written yet)')
