"""K2.3 quasi-dark linewidth battery.

Preregistered in DARK_STATE_K23_PREREG.md before this file existed.
Uses exactly the PHYS-K11/K2 coupling construction and measured odd directions.
"""
import collections
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import eig, eigh, expm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

KINDS = [
    'Priorities','Rules','Manner','Identity','Confidence','Facts',
    'Circumstances','Process','Model','Structure','Premises'
]
PLAIN = {
    'axiotic':'Priorities','deontic':'Rules','pragmatic':'Manner',
    'ontological':'Identity','epistemic':'Confidence','empirical':'Facts',
    'contingent':'Circumstances','procedural':'Process','nomological':'Model',
    'structural':'Structure','axiomatic':'Premises','testimonial':'Record'
}
KI = {k:i for i,k in enumerate(KINDS)}
TWINS = {
    'Pri/Prc': (KI['Priorities'], KI['Process']),
    'Str/Cir': (KI['Structure'], KI['Circumstances']),
}
KAPPAS = [0.1, 0.3, 1.0, 3.0, 10.0]
SGRID = np.concatenate((
    [0.0], np.geomspace(1e-5, 1e-1, 41), [0.15, 0.2, 0.3, 0.5, 0.7, 1.0]
))


def anchor_c(judgment_path: Path) -> np.ndarray:
    targets = {}
    with open(ROOT / 'scratchpad/plane_corpus/corpus_full.jsonl') as f:
        for line in f:
            row = json.loads(line)
            targets[row['id']] = PLAIN[row['kind_target']]

    by = collections.defaultdict(dict)
    with open(judgment_path) as f:
        for line in f:
            row = json.loads(line)
            by[row['id']][row['model']] = row['kind']

    M = np.zeros((11, 11), dtype=float)
    for item_id, target in targets.items():
        if target not in KI:
            continue
        for value in by.get(item_id, {}).values():
            if value in KI:
                M[KI[target], KI[value]] += 1.0

    M = M / np.maximum(M.sum(axis=1, keepdims=True), 1e-12)
    c = (M + M.T) / 2.0
    np.fill_diagonal(c, 0.0)
    if (c > 0).any():
        c = c / c[c > 0].mean()
    c = c / (c.sum() / 110.0)
    np.fill_diagonal(c, 0.0)
    return c


def swap_matrix(n, a, b):
    P = np.eye(n)
    P[[a,b]] = P[[b,a]]
    return P


def dark_vector(n, a, b):
    d = np.zeros(n)
    d[a] = 1.0 / math.sqrt(2.0)
    d[b] = -1.0 / math.sqrt(2.0)
    return d


def prepared(H, a, b):
    P = swap_matrix(len(H), a, b)
    d = dark_vector(len(H), a, b)
    H0 = (H + P @ H @ P) / 2.0
    Vodd = (H - P @ H @ P) / 2.0
    QB = np.eye(len(H)) - np.outer(d, d)

    pw, pV = eigh(P)
    B = pV[:, pw > 0]
    Hb = B.T @ H0 @ B
    Ew, W = eigh(Hb)
    bright = B @ W
    Ed = float(d @ H0 @ d)
    v = bright.T @ Vodd @ d
    return d, H0, Vodd, QB, Ed, Ew, bright, v


def coefficient(kappa, Ed, Ew, v):
    return float(np.sum((np.abs(v)**2) * kappa / ((Ed-Ew)**2 + (kappa/2.0)**2)))


def resonance(Hs, d, QB, kappa):
    Heff = Hs.astype(complex) - 0.5j * kappa * QB
    vals, vecs = eig(Heff)
    norms = np.linalg.norm(vecs, axis=0)
    ovs = np.abs(np.conjugate(d) @ vecs) ** 2 / np.maximum(norms**2, 1e-300)
    order = np.argsort(ovs)[::-1]
    i0, i1 = int(order[0]), int(order[1])
    lam = vals[i0]
    return {
        'Gamma': float(max(0.0, -2.0 * lam.imag)),
        'real_lambda': float(lam.real),
        'imag_lambda': float(lam.imag),
        'dark_overlap': float(ovs[i0]),
        'second_dark_overlap': float(ovs[i1]),
        'branch_ambiguous': bool((ovs[i0] - ovs[i1]) < 0.05),
    }


def log_slope(rows):
    pts = [(x['s'], x['Gamma']) for x in rows
           if 0 < x['s'] <= 1e-2 and x['Gamma'] > 1e-13 and not x['branch_ambiguous']]
    if len(pts) < 5:
        return None
    x = np.log([p[0] for p in pts])
    y = np.log([p[1] for p in pts])
    return float(np.polyfit(x, y, 1)[0])


def coefficient_score(rows, C):
    vals = []
    ratios = []
    for x in rows:
        if not (0 < x['s'] <= 1e-2) or x['Gamma'] <= 1e-13 or x['branch_ambiguous']:
            continue
        pred = x['s']**2 * C
        if pred <= 0:
            continue
        rat = x['Gamma'] / pred
        ratios.append(rat)
        vals.append(abs(rat - 1.0))
    if not vals:
        return {'n':0, 'median_abs_frac_error':None, 'median_ratio':None, 'max_abs_frac_error':None}
    return {
        'n': len(vals),
        'median_abs_frac_error': float(np.median(vals)),
        'median_ratio': float(np.median(ratios)),
        'max_abs_frac_error': float(np.max(vals)),
    }


def lindblad_sink_crosscheck(H0, Vodd, d, bright, s=0.01, kappa=1.0):
    """Compare 12-state absorbing-sink Lindblad system population to Heff norm."""
    n = len(d)
    ns = n + 1
    sink = n
    Hs = H0 + s * Vodd
    Hext = np.zeros((ns, ns), dtype=complex)
    Hext[:n,:n] = Hs

    jumps = []
    for j in range(bright.shape[1]):
        L = np.zeros((ns,ns), dtype=complex)
        L[sink,:n] = math.sqrt(kappa) * np.conjugate(bright[:,j])
        jumps.append(L)

    I = np.eye(ns, dtype=complex)
    Liouv = -1j * (np.kron(I, Hext) - np.kron(np.conjugate(Hext), I))
    for L in jumps:
        A = np.conjugate(L).T @ L
        Liouv += np.kron(np.conjugate(L), L)
        Liouv -= 0.5 * np.kron(I, A)
        Liouv -= 0.5 * np.kron(A.T, I)

    QB = np.eye(n) - np.outer(d,d)
    Heff = Hs.astype(complex) - 0.5j*kappa*QB
    psi0 = d.astype(complex)
    rho0 = np.zeros((ns,ns), dtype=complex)
    rho0[:n,:n] = np.outer(psi0, np.conjugate(psi0))
    v0 = rho0.reshape(-1, order='F')

    times = [0.1, 0.3, 1.0, 3.0]
    errs=[]
    records=[]
    for t in times:
        vt = expm(Liouv*t) @ v0
        rt = vt.reshape((ns,ns), order='F')
        pop_l = float(np.trace(rt[:n,:n]).real)
        psi = expm(-1j*Heff*t) @ psi0
        pop_h = float(np.vdot(psi,psi).real)
        err = abs(pop_l-pop_h)
        errs.append(err)
        records.append({'t':t,'lindblad_system_population':pop_l,'heff_norm2':pop_h,'abs_error':err})
    return {'s':s,'kappa':kappa,'max_abs_error':float(max(errs)),'rows':records}


def run_pair(H, a, b):
    d,H0,Vodd,QB,Ed,Ew,bright,v = prepared(H,a,b)
    pair = {
        'Ed': Ed,
        'bright_eigenvalues': [float(x) for x in Ew],
        'bright_detunings': [float(Ed-x) for x in Ew],
        'vodd_couplings': [float(x) for x in v],
        'min_abs_bright_detuning': float(np.min(np.abs(Ed-Ew))),
        'kappas': {},
    }
    for kappa in KAPPAS:
        C = coefficient(kappa,Ed,Ew,v)
        rows=[]
        for s in SGRID:
            r=resonance(H0+s*Vodd,d,QB,kappa)
            r['s']=float(s)
            rows.append(r)
        pair['kappas'][str(kappa)]={
            'C_pred':C,
            'weak_log_slope':log_slope(rows),
            'coefficient_score':coefficient_score(rows,C),
            'endpoint':rows[-1],
            'first_branch_ambiguous_s': next((x['s'] for x in rows if x['branch_ambiguous']),None),
            'rows':rows,
        }
    pair['lindblad_crosscheck']=lindblad_sink_crosscheck(H0,Vodd,d,bright)
    return pair


def main():
    arms={
        'CUR-P2': HERE/'panel2_validation.jsonl',
        'CUR-SP': ROOT/'scratchpad/plane_corpus/full_judgments.jsonl',
    }
    out={'prereg':'DARK_STATE_K23_PREREG.md','arms':{}}
    for arm,path in arms.items():
        H=anchor_c(path)
        aout={'pairs':{}}
        for label,(a,b) in TWINS.items():
            aout['pairs'][label]=run_pair(H,a,b)
        out['arms'][arm]=aout

    with open(HERE/'dark_state_k23_results.json','w') as f:
        json.dump(out,f,indent=2)

    for arm,aout in out['arms'].items():
        print('\n'+arm)
        for label,p in aout['pairs'].items():
            print(label,'min_gap=',f"{p['min_abs_bright_detuning']:.6g}",
                  'Lindblad_err=',f"{p['lindblad_crosscheck']['max_abs_error']:.3e}")
            for ks,k in p['kappas'].items():
                sc=k['coefficient_score']
                ep=k['endpoint']
                print(' kappa',ks,'C=',f"{k['C_pred']:.6g}",
                      'slope=',k['weak_log_slope'],
                      'median_err=',sc['median_abs_frac_error'],
                      'endpoint_Gamma=',f"{ep['Gamma']:.6g}",
                      'endpoint_overlap=',f"{ep['dark_overlap']:.4f}",
                      'first_ambg=',k['first_branch_ambiguous_s'])


if __name__=='__main__':
    main()
