"""Bath-correlation projector diagnostic.

Preregistered in BATH_CORRELATION_PROJECTOR_PREREG.md before this file existed.
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
NS = [8, 16, 32, 64, 128]
ELLS = [0.1, 0.3, 1.0, 3.0, 10.0, 30.0]
SEED = 20260822


def bright_dark(N):
    B = np.ones(N, dtype=float) / np.sqrt(N)
    Q = np.eye(N) - np.outer(B, B)
    ew, ev = np.linalg.eigh(Q)
    D = ev[:, ew > 0.5]
    return B, Q, D


def weights(S, B, Q, D):
    DB = np.diag(B)
    K = DB @ S @ DB
    trace = float(np.trace(Q @ K).real)
    explicit = 0.0
    for mu in range(D.shape[1]):
        d = D[:, mu]
        explicit += float(np.vdot(d, K @ d).real)
    return trace, explicit


def block_corr(N, G):
    S = np.zeros((N, N), dtype=float)
    for i in range(N):
        gi = (i * G) // N
        for j in range(N):
            gj = (j * G) // N
            S[i, j] = 1.0 if gi == gj else 0.0
    return S


def ring_exp(N, ell):
    idx = np.arange(N)
    delta = np.abs(idx[:, None] - idx[None, :])
    d = np.minimum(delta, N - delta).astype(float)
    return np.exp(-d / ell)


def random_corr(rng, N):
    X = rng.normal(size=(N, min(N, 12)))
    S = X @ X.T
    scale = np.sqrt(np.diag(S))
    return S / np.outer(scale, scale)


def one(S, B, Q, D):
    tr, ex = weights(S, B, Q, D)
    return {
        'W_trace': tr,
        'W_explicit': ex,
        'abs_identity_error': abs(tr - ex),
        'min_eigenvalue_S': float(np.linalg.eigvalsh(S).min()),
    }


def main():
    rng = np.random.default_rng(SEED)
    out = {'prereg': 'BATH_CORRELATION_PROJECTOR_PREREG.md', 'seed': SEED, 'Ns': {}}
    all_errors = []
    limit_errors = []
    block_errors = []
    monotone_ok = True
    bounded_ok = True
    ring_psd_ok = True

    for N in NS:
        B, Q, D = bright_dark(N)
        nout = {}

        indep = one(np.eye(N), B, Q, D)
        common = one(np.ones((N, N)), B, Q, D)
        indep_pred = (N - 1) / N
        limit_errors.extend([abs(indep['W_trace'] - indep_pred), abs(common['W_trace'])])
        all_errors.extend([indep['abs_identity_error'], common['abs_identity_error']])
        nout['independent'] = {**indep, 'predicted': indep_pred}
        nout['common'] = {**common, 'predicted': 0.0}

        blocks = {}
        for G in [2, 4, 8]:
            if N % G:
                continue
            z = one(block_corr(N, G), B, Q, D)
            pred = 1.0 - 1.0 / G
            z['predicted'] = pred
            block_errors.append(abs(z['W_trace'] - pred))
            all_errors.append(z['abs_identity_error'])
            blocks[str(G)] = z
        nout['blocks'] = blocks

        ring = []
        prev = None
        for ell in ELLS:
            z = one(ring_exp(N, ell), B, Q, D)
            z['ell'] = ell
            all_errors.append(z['abs_identity_error'])
            ring_psd_ok &= z['min_eigenvalue_S'] >= -1e-10
            if prev is not None:
                monotone_ok &= z['W_trace'] <= prev + 1e-12
            prev = z['W_trace']
            bounded_ok &= (-1e-12 <= z['W_trace'] <= indep_pred + 1e-12)
            ring.append(z)
        nout['ring_exp'] = ring

        random_rows = []
        for k in range(100):
            z = one(random_corr(rng, N), B, Q, D)
            z['draw'] = k
            all_errors.append(z['abs_identity_error'])
            random_rows.append(z)
        nout['random_psd'] = random_rows
        out['Ns'][str(N)] = nout

        print('N', N, 'indep', indep['W_trace'], 'common', common['W_trace'])
        print(' blocks', {g: round(v['W_trace'], 12) for g, v in blocks.items()})
        print(' ring', [(x['ell'], round(x['W_trace'], 8)) for x in ring])

    out['gates'] = {
        'B1_worst_identity_error': float(max(all_errors)),
        'B2_worst_limit_error': float(max(limit_errors)),
        'B3_worst_block_error': float(max(block_errors)),
        'B4_monotone': bool(monotone_ok),
        'B4_bounded': bool(bounded_ok),
        'ring_psd': bool(ring_psd_ok),
    }
    with open(HERE / 'bath_correlation_projector_results.json', 'w') as f:
        json.dump(out, f, indent=2)
    print('GATES', json.dumps(out['gates'], indent=2))


if __name__ == '__main__':
    main()
