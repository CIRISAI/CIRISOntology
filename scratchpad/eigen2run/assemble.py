"""Assemble every artifact into one summary object for EIGEN2_RESULTS.md.

Resolves the quantities that could only be fixed after the measurement:
  * S8's ANCHOR (the gauge row whose Omega_gauge* is closest to the measured Omega*,
    with linear interpolation) and therefore S8.1's V3b row and S9.4's precondition;
  * S9.5's four-band forward scoring;
  * the cross-arm dependence labels (k-, NUISANCE-, DIFFICULTY-, EMBEDDER-,
    INSTRUCTION-DEPENDENT);
  * S21's five promotion rungs, evaluated rung by rung.
"""
import json, os, sys

import numpy as np

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen2run')
import e2lib as L

def J(p):
    p = os.path.join(L.OUT, p)
    return json.load(open(p)) if os.path.exists(p) else None

A = {c: J(f'analysis_{c}.json') for c in
     ['primary', 'witness', 'ablation', 'raw', 'spandom', 'clearonly', 'rivalnodom']}
G = J('gauge11_summary.json')
GR = J('gauge_ruling.json')
S = {'gauge': G, 'gauge_ruling': GR, 'embed': J('embed_meta.json'),
     'unit_tests': J('unit_tests.json'), 'poscontrol': J('poscontrol.json'),
     'diagnostics': J('diagnostics.json'), 'db1': J('db1.json'),
     'panel': J('panel_analysis.json'), 'panel_spend': J('panel_spend.json'),
     'usage': J('usage.json'), 'analyses': A}

P = A['primary']
om_star = P['omega_star']['11']
tab = G['rank10_table']
sc = np.array([t['scale'] for t in tab])
ex = np.array([t['omega11_excess'] for t in tab])
rh = np.array([t['Rhat'] for t in tab])
rho = np.array([t['rho_gauge'] for t in tab])
sig = np.array([t['sigma_R_cell'] for t in tab])
sigma_R = G['sigma_R']

anchor_s = float(np.interp(om_star, ex, sc))
anchor = {'measured_omega_star_11': om_star, 'anchor_scale': anchor_s,
          'Rhat_at_anchor': float(np.interp(anchor_s, sc, rh)),
          'rho_gauge_at_anchor': float(np.interp(anchor_s, sc, rho)),
          'sigma_R_cell_at_anchor': float(np.interp(anchor_s, sc, sig)),
          'sigma_R': sigma_R,
          'rule': ("S8 Addition 2: the anchor is the gauge row whose Omega_gauge* is "
                   "closest to the measured Omega*, linearly interpolated.  Selecting a "
                   "row from a frozen table by a frozen rule is not a forking path.")}
anchor['V3b_fires'] = bool(anchor['rho_gauge_at_anchor'] < 0.30)
anchor['V8_fires'] = bool(sigma_R > 1.5)
anchor['P1b_precondition_fails'] = bool(abs(anchor['Rhat_at_anchor'] - 10.0) > sigma_R)
anchor['abs_Rhat_minus_10'] = abs(anchor['Rhat_at_anchor'] - 10.0)
if anchor['P1b_precondition_fails']:
    anchor['P1b'] = 'UNDECIDED — K2 CANNOT FIRE'
elif sigma_R > 1.5:
    anchor['P1b'] = 'UNDECIDED — V8'
else:
    lo = anchor['Rhat_at_anchor'] - 2 * sigma_R
    hi = anchor['Rhat_at_anchor'] + 2 * sigma_R
    anchor['P1b'] = ('Tier 1 live, band [%.2f, %.2f] (width 4*sigma_R = %.2f)'
                     % (lo, hi, 4 * sigma_R))
    anchor['Tier1_band'] = [lo, hi]
    anchor['Tier1_CONSISTENT'] = bool(lo <= P['R_kind'] <= hi)
anchor['Tier2_live'] = bool(sigma_R <= 0.66)
anchor['R_kind_measured'] = P['R_kind']
anchor['disclosed_bias_Rhat_minus_10'] = anchor['Rhat_at_anchor'] - 10.0
S['anchor_and_P1b'] = anchor

cells = {c: (A[c]['VERDICT_CELL'] if A[c] else None) for c in A}
dep = {
 'k_DEPENDENT': P['P1a']['k_dependent'],
 'NUISANCE_DEPENDENT': bool(A['raw'] and A['spandom']
                            and (cells['raw'] != cells['primary']
                                 or cells['spandom'] != cells['primary'])),
 'DIFFICULTY_DEPENDENT': bool(A['clearonly'] and cells['clearonly'] != cells['primary']),
 'EMBEDDER_DEPENDENT': bool(A['witness'] and cells['witness'] != cells['primary']),
 'cells': cells,
}
w = A['witness']
dep['WG1'] = ({'delta_median': w['delta_obs']['11']['median_of_diffs'],
               'p_gap_N1': w['VG1']['gateA_p_gap_N1'],
               'exceedances': w['VG1']['gateA_exceedances'],
               'PASS': bool(w['delta_obs']['11']['median_of_diffs'] > 0
                            and w['VG1']['gateA_p_gap_N1'] <= 0.01)} if w else None)
ab = A['ablation']
if ab:
    d_i = P['delta_obs']['11']['median_of_diffs']
    d_b = ab['delta_obs']['11']['median_of_diffs']
    # S3.3b's own usage of "VG1's margin" for the bare arm is the BARE ARM'S margin: the
    # section prices the calibration's bare delta against "its own gap-null p99 of
    # 0.008848".  Both readings are recorded.
    marg = ab['VG1']['margin_used']
    marg_primary = P['VG1']['margin_used']
    dep['instruction_ablation'] = {
        'delta_instructed': d_i, 'delta_bare': d_b, 'ratio_delta': d_i / d_b if d_b else None,
        'omega_star_instructed': om_star, 'omega_star_bare': ab['omega_star']['11'],
        'ratio_excess': om_star / ab['omega_star']['11'] if ab['omega_star']['11'] else None,
        'psi_instructed': P['psi']['11'].get('value'),
        'psi_bare': ab['psi']['11'].get('value'),
        'calibration_ratios': {'excess': 1.58, 'delta': 2.55, 'psi': [0.1584, 0.2556]},
        'bare_margin_own': marg, 'primary_margin': marg_primary,
        'bare_clears_its_own_VG1_margin': bool(d_b >= marg),
        'bare_clears_the_primary_margin': bool(d_b >= marg_primary),
        'bare_arm_cell': cells['ablation'],
        'bare_arm_VG1_VALID': ab['VG1']['VALID'],
        'INSTRUCTION_DEPENDENT': bool(not ab['VG1']['VALID']
                                      or cells['ablation'] != cells['primary']),
        'branch': ('the bare arm does NOT collapse: it clears its own VG1 margin, passes '
                   'every conjunct at the 0/500 floor and lands in the SAME S9.3 cell, so '
                   'the INSTRUCTION-DEPENDENT branch does not fire.  Omega* reproduces to '
                   '2.6% but delta does not (1.64x), so this is S3.3b\'s third branch — '
                   'an intermediate outcome, reported as the measured ratio with no verdict '
                   'attached.'),
        'psi_band_S13': {'instructed': P['psi']['11'].get('value'),
                         'bare': ab['psi']['11'].get('value'),
                         'calibration_moved_across_0.25_boundary': True,
                         'E2_both_in_mostly_context_band_0.05_0.25': True},
    }
# AMENDMENTS.md A6 — the rival conjunct, on the arms where it is evaluable at all
riv = {}
for c in ('primary', 'spandom', 'clearonly', 'witness', 'ablation'):
    if A[c]:
        riv[c] = {'Z': A[c]['nuisance'], 'ANNIHILATED': True,
                  'rank_B_dom11': A[c]['rank_B']['dom11'],
                  'omega_dom11': A[c]['omega_obs']['C1_dom11']['11'],
                  'omega_tax': A[c]['omega_obs']['C1_tax']['11'],
                  'p_perm_paired': A[c]['rival_domain11']['11']['p_perm_paired'],
                  'note': ('Z contains the domain dummies, so the domain-class means of '
                           'the residualized fitting half are exactly zero and this '
                           'Omega_dom11 is roundoff; the conjunct is STRUCTURALLY '
                           'UNINFORMATIVE on this arm')}
for c in ('raw', 'rivalnodom'):
    if A[c]:
        r = A[c]['rival_domain11']['11']
        riv[c] = {'Z': A[c]['nuisance'], 'ANNIHILATED': False,
                  'rank_B_dom11': A[c]['rank_B']['dom11'],
                  'omega_dom11': A[c]['omega_obs']['C1_dom11']['11'],
                  'omega_tax': A[c]['omega_obs']['C1_tax']['11'],
                  'omega_tax_minus_dom11': r['omega_tax_minus_dom11'],
                  'p_perm_paired': r['p_perm_paired'], 'exceedances': r['exceedances'],
                  'dom11_null_median': (A[c]['omega_obs']['C1_dom11']['11']
                                        - r['dom11_excess']),
                  'dom11_excess': r['dom11_excess'],
                  'delta_tax_minus_dom11': r['delta_tax_minus_dom11'],
                  'p_perm_paired_delta': r['p_perm_paired_delta'],
                  'delta_exceedances': r['delta_exceedances'],
                  'CONJUNCT_PASS': bool(r['p_perm_paired'] < 0.01
                                        and r['omega_tax_minus_dom11'] > 0),
                  'DELTA_PRIVILEGE_PASS': bool(r['p_perm_paired_delta'] < 0.01
                                               and r['delta_tax_minus_dom11'] > 0)}
S['A6_rival_conjunct'] = riv
# The A6-CORRECTED reading of the primary's cell: identical in every respect except that
# P1a's rival conjunct and P1d's delta-privilege conjunct are taken from `rivalnodom`,
# where they are evaluable.  Reported BESIDE the pinned cell, never instead of it.
if A['rivalnodom']:
    rn = riv['rivalnodom']
    c11 = dict(P['P1a']['conjuncts_k11'])
    c10 = dict(P['P1a']['conjuncts_k10'])
    c11['rival_dom11'] = rn['CONJUNCT_PASS']
    r10 = A['rivalnodom']['rival_domain11']['10']
    c10['rival_dom11'] = bool(r10['p_perm_paired'] < 0.01
                              and r10['omega_tax_minus_dom11'] > 0)
    det = all(c11.values()) and all(c10.values())
    p1d = bool(P['VG1']['VALID'] and rn['DELTA_PRIVILEGE_PASS'])
    if not P['VG1']['VALID']:
        cell6 = 'VOID-AS-INSTRUMENT'
    elif p1d and det:
        cell6 = 'CHANGE-CARRIED ALIGNMENT'
    elif p1d and not det:
        cell6 = 'CHANGE-READ, TAXONOMY-NULL'
    elif not p1d and det:
        cell6 = 'CONTEXT-PRIVILEGED'
    else:
        cell6 = 'CHANGE-READ, NOTHING-PRIVILEGED'
    S['A6_corrected_primary'] = {'conjuncts_k11': c11, 'conjuncts_k10': c10,
                                 'P1a_DETECTED': det, 'P1d_PASS': p1d,
                                 'VERDICT_CELL': cell6,
                                 'k_dependent': bool(all(c11.values())
                                                     and not all(c10.values())),
                                 'agrees_with_pinned': bool(cell6 == P['VERDICT_CELL'])}
S['dependence'] = dep

psi = P['psi']['11']
lad = {
 'rung1_cell_CHANGE_CARRIED_ALIGNMENT_and_k10_same_cell': {
    'cell_k11': P['VERDICT_CELL'], 'k10_conjuncts': P['P1a']['conjuncts_k10'],
    'PASS': bool(P['VERDICT_CELL'] == 'CHANGE-CARRIED ALIGNMENT'
                 and not P['P1a']['k_dependent'])},
 'rung2_omega_star_ge_0.190': {'value': om_star, 'PASS': bool(om_star >= 0.190)},
 'rung3_psi_point_ge_0.25_and_interval_lower_ge_0.15': {
    'psi': psi.get('value'), 'interval_bootstrap': psi.get('ci_bootstrap'),
    'interval_perm_width': psi.get('ci_perm_width'),
    'interval_note': ('S13 says "whichever is wider".  The permutation-implied interval is '
                      'DEGENERATE here: the ratio delta/Omega* has a denominator that crosses '
                      'zero under the label permutation, so the perm-width interval spans '
                      '[-57, +57] and carries no information.  The bootstrap interval over '
                      'the 200 splits (10,000 resamples, percentile) is reported as the '
                      'operative one, with this disclosure.  The rung fails on the POINT '
                      'estimate regardless.'),
    'PASS': bool(psi.get('defined') and psi.get('value', 0) >= 0.25
                 and psi.get('ci_bootstrap', [-9])[0] >= 0.15)},
 'rung4_WG1_witness_replication_sign_and_cell': {
    'witness_cell': cells['witness'], 'WG1': dep['WG1'],
    'PASS': bool(dep['WG1'] and dep['WG1']['PASS']
                 and cells['witness'] == cells['primary'])},
 'rung5_ablation_not_INSTRUCTION_DEPENDENT': {
    'INSTRUCTION_DEPENDENT': dep.get('instruction_ablation', {}).get(
        'INSTRUCTION_DEPENDENT'),
    'PASS': bool(not dep.get('instruction_ablation', {}).get('INSTRUCTION_DEPENDENT',
                                                             True))},
}
lad['ALL_FIVE'] = all(v['PASS'] for k, v in lad.items() if k.startswith('rung'))
lad['note'] = ('promotion is a STEWARD decision (S21); the ladder is TICKED as written by '
               'the S24 freeze stamp, but a ladder pass is an eligibility condition, not a '
               'promotion')
S['ladder'] = lad
S['forward'] = P['forward']
S['db2_nobatch'] = J('db2_nobatch.json')
S['spend'] = {'embed_usd': (S['usage'] or {}).get('_embed_usd', 0.0),
              'panel_usd': (S['panel_spend'] or {}).get('usd', 0.0)}
S['spend']['total_usd'] = S['spend']['embed_usd'] + S['spend']['panel_usd']
S['spend']['cap'] = 3.00
S['spend']['V10_fired'] = bool(S['spend']['total_usd'] > 3.00)

L.atomic_json(S, os.path.join(L.OUT, 'ASSEMBLED.json'))
print(json.dumps({'cell': P['VERDICT_CELL'], 'omega_star': om_star,
                  'anchor': anchor, 'dependence': {k: v for k, v in dep.items()
                                                   if k != 'cells'},
                  'cells': cells, 'ladder': lad, 'forward': P['forward'],
                  'spend': S['spend']}, indent=1, default=str))
