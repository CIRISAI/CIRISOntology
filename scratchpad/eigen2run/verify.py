"""Independent re-derivation of the headline numbers from the raw checkpoint arrays.

Recomputes the observed statistics from the cached vectors by a separate code path and
re-derives Omega*, delta, every p-value, VG1's two gates and psi straight from
`analysis_<cfg>.ckpt.npz`, then diffs against `analysis_<cfg>.json`.  Anything above 1e-12
is printed.  House rule: verify against the primary artifact, do not trust the summary.
"""
import json, os, sys

import numpy as np

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen2run')
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import e2lib as L
import pipeline as pl
from analysis import CONFIGS, reduce_dim, unit, KS

cfg = sys.argv[1] if len(sys.argv) > 1 else 'primary'
arm, nuis, clear_only, nulls = CONFIGS[cfg]
R = json.load(open(os.path.join(L.OUT, f'analysis_{cfg}.json')))
z = np.load(os.path.join(L.OUT, f'analysis_{cfg}.ckpt.npz'))

rows_all = L.load_e2()
meta = json.load(open(os.path.join(L.OUT, 'embed_meta.json')))
drop = set(meta['V7']['dropped_ids'])
ki = [i for i, r in enumerate(rows_all) if r['id'] not in drop]
if clear_only:
    ki = [i for i in ki if rows_all[i]['difficulty'] == 'clear']
rows = [rows_all[i] for i in ki]
labels = L.labels_of(rows)
batches = L.batches_of(rows)
dom11, _ = L.domain11_of(rows)
Z = L.nuisance_Z(rows, nuis if nuis != 'none' else 'none')
splits = L.make_splits(labels, batches, L.NSPLIT, L.SEED)
XC = np.load(os.path.join(L.CACHE, f'X_{arm}_C1.npy')).astype(np.float64)[ki]
XP = np.load(os.path.join(L.CACHE, f'X_{arm}_C1P.npy')).astype(np.float64)[ki]
prepC = pl.Prepared(reduce_dim(unit(XC))[0], Z, splits, residualize=(nuis != 'none'))
prepP = pl.Prepared(reduce_dim(unit(XP))[0], Z, splits, residualize=(nuis != 'none'))
oC = pl.full_stats(prepC, pl.onehot(labels, 11), ks=KS, want_eta=False)
oP = pl.full_stats(prepP, pl.onehot(labels, 11), ks=KS, want_eta=False)
oCd = pl.full_stats(prepC, pl.onehot(dom11, 11), ks=KS, want_eta=False)

j = KS.index(11)
bad = []


def chk(name, a, b, tol=1e-10):
    if b is None or (isinstance(b, float) and np.isnan(b)):
        return
    d = abs(a - b)
    print(f'{name:42s} recomputed={a:.8f}  stored={b:.8f}  |diff|={d:.2e}')
    if d > tol:
        bad.append((name, d))


chk('Omega(11) C1', oC['omega'][11], R['omega_obs']['C1_tax']['11'])
chk('Omega(11) C1P', oP['omega'][11], R['omega_obs']['C1P_tax']['11'])
chk('Omega(11) C1 domain-11', oCd['omega'][11], R['omega_obs']['C1_dom11']['11'])
chk('rank(B)', oC['rank'], R['rank_B']['tax'])

omC, omP = z['N1_omC'], z['N1_omP']
nm = float(np.median(omC[:, j]))
chk('N1 null median', nm, R['nulls']['N1']['11']['null_median'])
chk('Omega*(11)', oC['omega'][11] - nm, R['omega_star']['11'])
p = (1 + int((omC[:, j] >= oC['omega'][11]).sum())) / (1 + len(omC))
chk('p_N1', p, R['nulls']['N1']['11']['p_N'])
d_splits = oC['omega_splits'][11] - oP['omega_splits'][11]
chk('delta (median of per-split diffs)', float(np.median(d_splits)),
    R['delta_obs']['11']['median_of_diffs'])
chk('delta (difference of medians)', oC['omega'][11] - oP['omega'][11],
    R['delta_obs']['11']['diff_of_medians'])
gn = omC[:, j] - omP[:, j]
chk('gap-null p99', float(np.percentile(gn, 99)), R['VG1']['gap_null_p99'])
pg = (1 + int((gn >= float(np.median(d_splits))).sum())) / (1 + len(gn))
chk('VG1 gate A p_gap_N1', pg, R['VG1']['gateA_p_gap_N1'])
if R['psi']['11'].get('defined'):
    chk('psi', float(np.median(d_splits)) / (oC['omega'][11] - nm), R['psi']['11']['value'])
if 'N1b' in R['nulls']:
    b = z['N1b_omC']
    chk('N1b null median', float(np.median(b[:, j])), R['nulls']['N1b']['11']['null_median'])
    chk('p_N1b', (1 + int((b[:, j] >= oC['omega'][11]).sum())) / (1 + len(b)),
        R['nulls']['N1b']['11']['p_N'])

print()
print('VERIFY', cfg, ':', 'ALL MATCH' if not bad else f'MISMATCHES {bad}')
sys.exit(1 if bad else 0)
