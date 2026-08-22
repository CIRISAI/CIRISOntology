"""Dynamic-disorder gray-algebra structural screen.

Preregistered in DYNAMIC_GRAY_ALGEBRA_PREREG.md before this file existed.
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
NS = [16, 32, 64, 128]
TOL = 1e-10


def common(N):
    return np.ones((N, 1), dtype=float)


def groups(N, G):
    A = np.zeros((N, G), dtype=float)
    for i in range(N):
        A[i, (i * G) // N] = 1.0
    return A


def rank1_generic(N):
    # Exact row labels are 0..N-1; normalized later only for numerical closure.
    return np.arange(N, dtype=float)[:, None]


def next_prime(n):
    def prime(x):
        if x < 2:
            return False
        d = 2
        while d * d <= x:
            if x % d == 0:
                return False
            d += 1
        return True
    x = n + 1
    while not prime(x):
        x += 1
    return x


def rank2_generic(N):
    p = next_prime(N)
    i = np.arange(N, dtype=int)
    return np.column_stack((i, (i * i) % p)).astype(float)


def local(N):
    return np.eye(N, dtype=float)


def class_count(A):
    # Constructions use exact integer/0-1-valued floats, so tuple equality is exact.
    return len({tuple(row.tolist()) for row in A})


def direct_gray_rank(A):
    N = A.shape[0]
    B = np.ones(N) / np.sqrt(N)
    Q = np.eye(N) - np.outer(B, B)
    # diag(a_alpha) B = a_alpha / sqrt(N)
    M = Q @ (A / np.sqrt(N))
    s = np.linalg.svd(M, compute_uv=False)
    if len(s) == 0 or s[0] == 0:
        return 0, [float(x) for x in s]
    return int(np.sum(s > TOL * s[0])), [float(x) for x in s]


def normalize_profiles(A):
    X = A.astype(float).copy()
    for j in range(X.shape[1]):
        col = X[:, j]
        lo, hi = float(col.min()), float(col.max())
        if hi > lo:
            X[:, j] = 2.0 * (col - lo) / (hi - lo) - 1.0
        else:
            X[:, j] = 1.0
    return X


def add_orthonormal(basis, v, tol=TOL):
    v = np.asarray(v, dtype=float).copy()
    n0 = np.linalg.norm(v)
    if n0 == 0:
        return False
    # Two-pass modified Gram-Schmidt.
    for _ in range(2):
        for q in basis:
            v -= np.dot(q, v) * q
    nv = np.linalg.norm(v)
    if nv <= tol * n0:
        return False
    basis.append(v / nv)
    return True


def numerical_closure(A):
    """Closure of B under repeated diagonal-generator action."""
    N = A.shape[0]
    X = normalize_profiles(A)
    basis = [np.ones(N) / np.sqrt(N)]
    frontier = [0]
    products = 0
    while frontier and len(basis) < N:
        idx = frontier.pop(0)
        q = basis[idx]
        for alpha in range(X.shape[1]):
            v = X[:, alpha] * q
            products += 1
            before = len(basis)
            if add_orthonormal(basis, v):
                frontier.append(before)
                if len(basis) == N:
                    break
    Q = np.column_stack(basis)
    ortho_err = float(np.linalg.norm(Q.T @ Q - np.eye(len(basis)), ord='fro'))
    return len(basis), products, ortho_err


def class_basis_residual(A):
    """Independent exact-class invariant-subspace check."""
    N = A.shape[0]
    rows = [tuple(x.tolist()) for x in A]
    labels = {}
    for i, row in enumerate(rows):
        labels.setdefault(row, []).append(i)
    vecs = []
    for ids in labels.values():
        v = np.zeros(N)
        v[ids] = 1.0 / np.sqrt(len(ids))
        vecs.append(v)
    C = np.column_stack(vecs)
    P = C @ C.T
    worst = 0.0
    for j in range(A.shape[1]):
        D = np.diag(A[:, j])
        worst = max(worst, float(np.linalg.norm((np.eye(N)-P) @ D @ C, ord='fro')))
    B = np.ones(N) / np.sqrt(N)
    bright_resid = float(np.linalg.norm((np.eye(N)-P) @ B))
    return {'dimension': C.shape[1], 'generator_invariance_residual': worst,
            'bright_containment_residual': bright_resid}


def predicted(name, N):
    if name == 'COMMON': return {'direct': 0, 'G': 1}
    if name == 'GROUP4': return {'direct': 3, 'G': 4}
    if name == 'GROUP8': return {'direct': 7, 'G': 8}
    if name == 'RANK1-GENERIC': return {'direct': 1, 'G': N}
    if name == 'RANK2-GENERIC': return {'direct_max': 2, 'G': N}
    if name == 'LOCAL': return {'direct': N-1, 'G': N}
    raise KeyError(name)


def main():
    makers = [
        ('COMMON', common),
        ('GROUP4', lambda N: groups(N, 4)),
        ('GROUP8', lambda N: groups(N, 8)),
        ('RANK1-GENERIC', rank1_generic),
        ('RANK2-GENERIC', rank2_generic),
        ('LOCAL', local),
    ]
    out = {'prereg': 'DYNAMIC_GRAY_ALGEBRA_PREREG.md', 'tolerance': TOL, 'rows': []}
    for N in NS:
        for name, maker in makers:
            A = maker(N)
            dr, sv = direct_gray_rank(A)
            G = class_count(A)
            closure, nprod, oerr = numerical_closure(A)
            cb = class_basis_residual(A)
            pred = predicted(name, N)
            row = {
                'N': N, 'case': name, 'profile_rank': int(np.linalg.matrix_rank(A)),
                'r_direct': dr, 'direct_singular_values': sv,
                'G_class_count': G, 'predicted_invariant_with_cavity': G+1,
                'numerical_closure_dimension': closure,
                'numerical_products': nprod, 'numerical_orthogonality_error': oerr,
                'class_basis_check': cb, 'prediction': pred,
            }
            out['rows'].append(row)
            print(N, name, 'rankA=', row['profile_rank'], 'r_direct=', dr,
                  'G=', G, 'closure=', closure, 'class_resid=', cb['generator_invariance_residual'])

    # Frozen stakes.
    D1 = True; D2 = True; D3 = True
    closure_mismatches = []
    for x in out['rows']:
        N, name = x['N'], x['case']
        if name == 'COMMON': D1 &= (x['r_direct']==0 and x['G_class_count']==1)
        elif name == 'GROUP4': D1 &= (x['r_direct']==3 and x['G_class_count']==4)
        elif name == 'GROUP8': D1 &= (x['r_direct']==7 and x['G_class_count']==8)
        elif name == 'RANK1-GENERIC': D2 &= (x['profile_rank']==1 and x['r_direct']==1 and x['G_class_count']==N)
        elif name == 'LOCAL': D3 &= (x['r_direct']==N-1 and x['G_class_count']==N)
        if x['numerical_closure_dimension'] != x['G_class_count']:
            closure_mismatches.append({'N':N,'case':name,'closure':x['numerical_closure_dimension'],'G':x['G_class_count']})
    out['gates'] = {'D1': bool(D1), 'D2': bool(D2), 'D3': bool(D3),
                    'D4_closure_mismatches': closure_mismatches}
    with open(HERE/'dynamic_gray_algebra_results.json','w') as f:
        json.dump(out, f, indent=2)
    print('GATES', json.dumps(out['gates'], indent=2))


if __name__ == '__main__':
    main()
