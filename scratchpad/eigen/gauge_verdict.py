"""S8.4 consequence ladder + S22 Ruling 3 separation verdict, applied mechanically."""
import json, sys
import numpy as np

P = '/home/emoore/CIRISOntology/scratchpad/eigen/out/'
g = json.load(open(P + 'gauge_raw.json'))
grid = g['grid']
cells = g['cells']
out = {'grid': grid, 'ndraw': g['ndraw'], 'nperm_gauge': g['nperm_gauge']}

tab = {}
for w in ['rank7', 'rank11', 'rank13']:
    tab[w] = [{'scale': s, **{k: cells[f'{w}@{s}'][k] for k in
               ['omega11_median', 'rkind_mean', 'rkind_sd', 'rkind_median',
                'rho_gauge_median', 'rank_b_median']},
               'pcrep': cells[f'{w}@{s}']['pcrep']} for s in grid]
out['table'] = tab

# ---- sigma_R : largest across-scale sd of R_kind at planted rank 11, over scales
# where the mean recovered rank is within +-3 of planted (S8.2)
adm = [c for c in tab['rank11'] if abs(c['rkind_mean'] - 11) <= 3]
out['admissible_scales'] = [c['scale'] for c in adm]
if adm:
    sigma_R = max(c['rkind_sd'] for c in adm)
    out['sigma_R'] = sigma_R
    out['sigma_R_defined'] = True
else:
    sigma_R = None
    out['sigma_R'] = None
    out['sigma_R_defined'] = False

if sigma_R is None:
    rung, verdict = 4, 'sigma_R UNDEFINED (empty admissible set) -> treated as > 1.5 -> V8 FIRES'
elif sigma_R <= 0.66:
    rung, verdict = 1, 'sharp clause LIVES: P1b Tier 2, band R_kind in {10,11,12}'
elif sigma_R <= 1.5:
    rung, verdict = 2, '"not 7, not 13" RETRACTED in advance; P1b Tier 1 only, band |R_kind-11| <= 2*sigma_R (sigma_R floored at 1 per S9-P1b)'
else:
    rung, verdict = 3, 'V8 FIRES: the rank leg cannot kill; R_kind descriptive only'
out['ladder_rung_fired'] = rung
out['ladder_verdict'] = verdict
sr_floor = max(sigma_R, 1.0) if sigma_R is not None else None
out['P1b_tier'] = 1 if rung == 2 else (2 if rung == 1 else None)
out['P1b_band'] = ([11 - 2 * sr_floor, 11 + 2 * sr_floor] if rung == 2 else
                   ([10, 12] if rung == 1 else None))
out['V8_fired'] = rung in (3, 4)

# ---- V3b : rho_gauge at the grid scale where median Omega(11) ~ 0.25
om = np.array([c['omega11_median'] for c in tab['rank11']])
anchor_i = int(np.argmin(np.abs(om - 0.25)))
out['anchor_scale'] = grid[anchor_i]
out['anchor_omega11'] = float(om[anchor_i])
out['rho_gauge_at_anchor'] = tab['rank11'][anchor_i]['rho_gauge_median']
out['V3b_fired'] = bool(out['rho_gauge_at_anchor'] < 0.30)

# ---- Ruling 3 : two-world separation of the LOKO eta statistic
r3 = {}
for w in ['worldI', 'worldII']:
    r3[w] = [{'scale': s,
              'omega11_median': cells[f'{w}@{s}']['omega11_median'],
              'frac_12th_below_min_content': cells[f'{w}@{s}']['frac_12th_below_min_content'],
              'eta_median': cells[f'{w}@{s}']['eta_median']} for s in grid]
out['ruling3_table'] = r3
sep = []
for i, s in enumerate(grid):
    a = r3['worldI'][i]['frac_12th_below_min_content']
    b = r3['worldII'][i]['frac_12th_below_min_content']
    sep.append({'scale': s, 'worldI_frac': a, 'worldII_frac': b,
                'staked_i_met': bool(a >= 0.95), 'ii_inside_range': bool(b <= 0.25),
                'separated': bool(a >= 0.95 and b <= 0.25)})
out['ruling3_by_scale'] = sep
out['ruling3_anchor'] = sep[anchor_i]
out['ruling3_any_scale_separated'] = bool(any(s['separated'] for s in sep))
out['ruling3_separated_scales'] = [s['scale'] for s in sep if s['separated']]
# pinned decision point: the anchor scale (the same anchor V3b uses)
out['ruling3_verdict'] = ('eta leg CONFIRMED as gauge-validated at the anchor scale'
                          if sep[anchor_i]['separated'] else
                          'eta leg DOWNGRADED TO EXPLORATORY (gauge could not separate the two worlds at the anchor scale)')
json.dump(out, open(P + 'gauge_verdict.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('table', 'ruling3_table')}, indent=1))
print()
for w in ['rank7', 'rank11', 'rank13']:
    print(w, ' '.join(f"{c['scale']}:Om={c['omega11_median']:.4f},Rk={c['rkind_mean']:.2f}+-{c['rkind_sd']:.2f}"
                      for c in tab[w]))
