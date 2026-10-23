"""K2 dark-state defect -> coupling -> spectral impurity analysis.

Preregistered in DARK_STATE_K2_PREREG.md before first execution.
Uses the exact PHYS-K11-1 corpus artifacts and coupling construction.
"""
import collections
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

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


def anchor_c(judgment_path: Path) -> np.ndarray:
    """Byte-for-byte-in-logic copy of PHYS-K11-1's coupling construction."""
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


def swap_matrix(n: int, a: int, b: int) -> np.ndarray:
    P = np.eye(n)
    P[[a,b]] = P[[b,a]]
    return P


def dark_vector(n: int, a: int, b: int) -> np.ndarray:
    d = np.zeros(n)
    d[a] = 1.0 / math.sqrt(2.0)
    d[b] = -1.0 / math.sqrt(2.0)
    return d


def metrics(H: np.ndarray, a: int, b: int) -> dict:
    n = H.shape[0]
    P = swap_matrix(n, a, b)
    d = dark_vector(n, a, b)
    Q = np.eye(n) - np.outer(d, d)

    defect = H - P @ H @ P
    delta = np.linalg.norm(defect, ord='fro')
    hnorm = np.linalg.norm(H, ord='fro')
    gdb = np.linalg.norm(Q @ H @ d)
    identity_resid = abs(gdb - delta / (2.0 * math.sqrt(2.0)))

    w, V = eigh(H)
    overlaps = np.abs(V.T @ d) ** 2
    imax = int(np.argmax(overlaps))
    lspec = float(1.0 - overlaps[imax])

    Ed = float(d @ H @ d)

    # Build an orthonormal basis of the P-even subspace using eigenvectors of P.
    pw, pV = eigh(P)
    B = pV[:, pw > 0.0]
    Hbright = B.T @ H @ B
    bright_w = eigh(Hbright, eigvals_only=True)
    min_bright_gap = float(np.min(np.abs(bright_w - Ed)))

    return {
        'Delta_sigma': float(delta),
        'Delta_sigma_over_Hfro': float(delta / hnorm if hnorm else 0.0),
        'g_DB': float(gdb),
        'identity_residual': float(identity_resid),
        'L_spec': lspec,
        'dark_expectation': Ed,
        'min_bright_gap_at_current_H': min_bright_gap,
        'dominant_eigenvalue': float(w[imax]),
        'dominant_dark_overlap': float(overlaps[imax]),
        'Lspec_over_gdb2': float(lspec / (gdb*gdb)) if gdb > 1e-15 else None,
    }


def continuation(H: np.ndarray, a: int, b: int) -> dict:
    P = swap_matrix(H.shape[0], a, b)
    H0 = (H + P @ H @ P) / 2.0
    Vodd = (H - P @ H @ P) / 2.0
    sgrid = np.concatenate(([0.0], np.geomspace(1e-4, 1.0, 81)))
    rows = []
    for s in sgrid:
        m = metrics(H0 + s * Vodd, a, b)
        m['s'] = float(s)
        rows.append(m)

    # Slopes use points safely above floating floor, restricted to s<=1e-2.
    def slope(key, floor):
        pts = [(r['s'], r[key]) for r in rows if r['s'] > 0 and r['s'] <= 1e-2 and r[key] is not None and r[key] > floor]
        if len(pts) < 4:
            return None
        x = np.log([p[0] for p in pts])
        y = np.log([p[1] for p in pts])
        return float(np.polyfit(x, y, 1)[0])

    # Exact-symmetry bright denominator, the perturbative licensing quantity.
    m0 = metrics(H0, a, b)
    return {
        'H0_exact': m0,
        'slope_Delta_sigma': slope('Delta_sigma', 1e-14),
        'slope_g_DB': slope('g_DB', 1e-14),
        'slope_L_spec': slope('L_spec', 1e-14),
        'rows': rows,
    }


def main():
    arms = {
        'CUR-P2': HERE / 'panel2_validation.jsonl',
        'CUR-SP': ROOT / 'scratchpad/plane_corpus/full_judgments.jsonl',
    }
    out = {'prereg': 'DARK_STATE_K2_PREREG.md', 'arms': {}}
    for arm, path in arms.items():
        H = anchor_c(path)
        aout = {'matrix_fro': float(np.linalg.norm(H, ord='fro')), 'pairs': {}}
        for label, (a,b) in TWINS.items():
            aout['pairs'][label] = {
                'measured': metrics(H, a, b),
                'continuation': continuation(H, a, b),
            }
        out['arms'][arm] = aout

    # Cross-pair ratios are explicit outputs, never inferred from prose.
    for arm, aout in out['arms'].items():
        p = aout['pairs']['Pri/Prc']['measured']
        s = aout['pairs']['Str/Cir']['measured']
        aout['ratios_StrCir_over_PriPrc'] = {
            'Delta_sigma': s['Delta_sigma'] / p['Delta_sigma'] if p['Delta_sigma'] else None,
            'g_DB': s['g_DB'] / p['g_DB'] if p['g_DB'] else None,
            'L_spec': s['L_spec'] / p['L_spec'] if p['L_spec'] else None,
            'susceptibility_Lspec_over_gdb2': (
                s['Lspec_over_gdb2'] / p['Lspec_over_gdb2']
                if s['Lspec_over_gdb2'] is not None and p['Lspec_over_gdb2'] not in (None, 0)
                else None
            ),
        }

    outfile = HERE / 'dark_state_k2_results.json'
    with open(outfile, 'w') as f:
        json.dump(out, f, indent=2)

    for arm, aout in out['arms'].items():
        print('\n', arm)
        print(' ratios:', aout['ratios_StrCir_over_PriPrc'])
        for label, pobj in aout['pairs'].items():
            m = pobj['measured']; c = pobj['continuation']
            print(label,
                  'Delta=', f"{m['Delta_sigma']:.6g}",
                  'gDB=', f"{m['g_DB']:.6g}",
                  'Lspec=', f"{m['L_spec']:.6g}",
                  'gap0=', f"{c['H0_exact']['min_bright_gap_at_current_H']:.6g}",
                  'slopes=', c['slope_Delta_sigma'], c['slope_g_DB'], c['slope_L_spec'],
                  'identity=', f"{m['identity_residual']:.3e}")


if __name__ == '__main__':
    main()
