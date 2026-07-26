"""rent_islands_design_check.py -- CONSTRUCTION FACTS ONLY, computed BEFORE the prereg.

No dynamics. No maintenance quantity. Nothing here is a measurement of rent.
It establishes that the substrates named in RENT_ISLANDS_PREREG.md exist, are exactly
pair-uniform, and have the tabled |S| / share_max / dual-distance -- so the prereg can
quote them rather than promise them.

Output: rent_islands_design_check.json
"""
import json
import numpy as np
from itertools import combinations

LN2 = float(np.log(2))


# ---------------------------------------------------------------- Hadamard matrices
def sylvester(n):
    """H_{2^n} by Sylvester recursion."""
    H = np.array([[1]], dtype=int)
    for _ in range(n):
        H = np.block([[H, H], [H, -H]])
    return H


def paley1(q):
    """Paley type I: Hadamard of order q+1, q prime power == 3 (mod 4). Prime q only here."""
    assert q % 4 == 3
    qr = set((i * i) % q for i in range(1, q))
    chi = np.array([0] + [1 if a in qr else -1 for a in range(1, q)], dtype=int)
    Q = np.array([[chi[(j - i) % q] for j in range(q)] for i in range(q)], dtype=int)
    S = np.zeros((q + 1, q + 1), dtype=int)
    S[0, 1:] = 1
    S[1:, 0] = -1
    S[1:, 1:] = Q
    return S + np.eye(q + 1, dtype=int)


def paley2(q):
    """Paley type II: Hadamard of order 2(q+1), q prime == 1 (mod 4). Prime q only here."""
    assert q % 4 == 1
    qr = set((i * i) % q for i in range(1, q))
    chi = np.array([0] + [1 if a in qr else -1 for a in range(1, q)], dtype=int)
    Q = np.array([[chi[(j - i) % q] for j in range(q)] for i in range(q)], dtype=int)
    S = np.zeros((q + 1, q + 1), dtype=int)
    S[0, 1:] = 1
    S[1:, 0] = 1
    S[1:, 1:] = Q
    n = q + 1
    # blocks: S_ij = 0 -> [[1,-1],[-1,-1]] ; S_ij = 1 -> [[1,1],[1,-1]] ; -1 -> -that
    B0 = np.array([[1, -1], [-1, -1]])
    Bp = np.array([[1, 1], [1, -1]])
    H = np.zeros((2 * n, 2 * n), dtype=int)
    for i in range(n):
        for j in range(n):
            H[2 * i:2 * i + 2, 2 * j:2 * j + 2] = B0 if S[i, j] == 0 else S[i, j] * Bp
    return H


HAD = {}


def hadamard(N):
    """A Hadamard matrix of order N, by whichever named construction covers it."""
    if N in HAD:
        return HAD[N]
    if N == 1:
        H = np.array([[1]], dtype=int)
    elif (N & (N - 1)) == 0:
        H = sylvester(int(np.log2(N)))
    elif is_prime(N - 1) and (N - 1) % 4 == 3:
        H = paley1(N - 1)
    elif N % 2 == 0 and is_prime(N // 2 - 1) and (N // 2 - 1) % 4 == 1:
        H = paley2(N // 2 - 1)
    else:
        raise ValueError(f"no construction wired for order {N}")
    assert H.shape == (N, N)
    assert np.array_equal(H @ H.T, N * np.eye(N, dtype=int)), f"order {N} not Hadamard"
    HAD[N] = H
    return H


def is_prime(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, int(n ** 0.5) + 1))


def had_source(N):
    if (N & (N - 1)) == 0:
        return f"Sylvester 2^{int(np.log2(N))}"
    if is_prime(N - 1) and (N - 1) % 4 == 3:
        return f"Paley-I q={N-1}"
    return f"Paley-II q={N//2-1}"


def N0(k):
    return 4 * ((k + 1 + 3) // 4)


def maxshare_oa(k):
    """The minimum-size strength-2 OA on k factors, as 0/1 rows, from H_{N0(k)}."""
    N = N0(k)
    H = hadamard(N).copy()
    H = H * np.where(H[:, [0]] == -1, -1, 1)          # normalise first column to +1
    B = (1 - H[:, 1:]) // 2                            # drop it; map +-1 -> 0/1
    return np.ascontiguousarray(B[:, :k].astype(np.int8))


# ---------------------------------------------------------------- linear codes
def linear_code(k, G):
    G = np.asarray(G, dtype=np.int8)
    m = G.shape[0]
    words = []
    for msg in range(1 << m):
        v = np.zeros(k, dtype=np.int8)
        for b in range(m):
            if (msg >> b) & 1:
                v ^= G[b]
        words.append(v)
    return np.array(words, dtype=np.int8)


def cols_to_G(m, cols):
    G = np.zeros((m, len(cols)), dtype=np.int8)
    for j, c in enumerate(cols):
        for b in range(m):
            G[b, j] = (c >> b) & 1
    return G


def dual_distance_of_columns(m, cols):
    k = len(cols)
    if 0 in cols or len(set(cols)) != k:
        return 1 if 0 in cols else 2
    for w in range(3, min(k, 6) + 1):
        for sub in combinations(range(k), w):
            s = 0
            for j in sub:
                s ^= cols[j]
            if s == 0:
                return w
    return min(k, 6) + 1


def code_min_distance(words):
    n = len(words)
    step = max(1, n // 512)
    return min(int(np.sum(words[i] ^ words[j]))
               for i in range(0, n, step) for j in range(i + 1, n))


def armB_columns(k):
    """PRE-REGISTERED rule for the power-of-two comparator: m = ceil(log2(k+1)); take the
    k columns of F_2^m that maximise dual distance, then minimum distance. Search is
    exhaustive when C(2^m-1, k) is small, otherwise the canonical affine-first list
    [2^{m-1}..2^m-1] then [1..2^{m-1}-1], which is the dual-distance-4 choice while it
    lasts and dual-distance-3 after."""
    m = int(np.ceil(np.log2(k + 1)))
    pool = list(range(1, 1 << m))
    from math import comb
    if comb(len(pool), k) <= 20000:
        best = None
        for cols in combinations(pool, k):
            dd = dual_distance_of_columns(m, list(cols))
            if best is not None and dd < best[0]:
                continue
            W = linear_code(k, cols_to_G(m, cols))
            key = (dd, code_min_distance(W))
            if best is None or key > best[:2]:
                best = (dd, key[1], list(cols))
        return m, best[2], 'exhaustive'
    half = 1 << (m - 1)
    canon = list(range(half, 1 << m)) + list(range(1, half))
    return m, canon[:k], 'canonical'


# ---------------------------------------------------------------- perfect codes
def hamming_code(r):
    """Perfect Hamming [2^r-1, 2^r-1-r]: the code whose PARITY CHECK columns are all
    nonzero vectors of F_2^r. Returned as the full codeword list."""
    n = (1 << r) - 1
    Hchk = np.array([[(c >> b) & 1 for c in range(1, 1 << r)] for b in range(r)],
                    dtype=np.int8)
    # codewords = null space of Hchk; build a generator by systematic reduction
    words = []
    for x in range(1 << n):
        pass
    raise NotImplementedError


def code_from_parity_check(Hchk):
    """All codewords of the code {v : Hchk v = 0}, by enumerating a generator basis."""
    r, n = Hchk.shape
    # gaussian elimination over F2 to find null space basis
    A = Hchk.copy() % 2
    piv, row = [], 0
    for col in range(n):
        sel = None
        for rr in range(row, r):
            if A[rr, col]:
                sel = rr
                break
        if sel is None:
            continue
        A[[row, sel]] = A[[sel, row]]
        for rr in range(r):
            if rr != row and A[rr, col]:
                A[rr] ^= A[row]
        piv.append(col)
        row += 1
        if row == r:
            break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = np.zeros(n, dtype=np.int8)
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = A[i, f]
        basis.append(v)
    basis = np.array(basis, dtype=np.int8)
    assert np.all((Hchk @ basis.T) % 2 == 0)
    return linear_code(n, basis)


def golay23():
    """The perfect binary Golay [23,12,7], from the quadratic-residue generator
    polynomial g(x) = x^11+x^10+x^6+x^5+x^4+x^2+1 over F_2, cyclic of length 23."""
    g = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1]      # coefficients, degree 11, g[i] = x^i
    n, kk = 23, 12
    G = np.zeros((kk, n), dtype=np.int8)
    for i in range(kk):
        for j, c in enumerate(g):
            G[i, i + j] = c
    return G


# ---------------------------------------------------------------- diagnostics
def popcount(a):
    return np.array([bin(int(i)).count('1') for i in a], dtype=np.int64)


def wht(a):
    a = np.asarray(a, dtype=np.float64).copy()
    n, h = a.size, 1
    while h < n:
        a = a.reshape(-1, 2, h)
        x, y = a[:, 0, :].copy(), a[:, 1, :].copy()
        a[:, 0, :] = x + y
        a[:, 1, :] = x - y
        a = a.reshape(n)
        h *= 2
    return a


def bits_to_idx(bits):
    bits = np.asarray(bits, dtype=np.int64)
    idx = np.zeros(bits.shape[0], dtype=np.int64)
    for j in range(bits.shape[1]):
        idx = idx * 2 + bits[:, j]
    return idx


def diagnose(k, S, name):
    """Exact: pair-uniformity by direct counting, |S|, share_max, dual distance d, A_w."""
    S = np.asarray(S, dtype=np.int8)
    ns = len(S)
    distinct = len(set(map(tuple, S.tolist())))
    # strength 2 by direct combination counting (independent of Fourier)
    ok2 = True
    for i, j in combinations(range(k), 2):
        c = np.bincount(S[:, i].astype(int) * 2 + S[:, j].astype(int), minlength=4)
        ok2 &= bool(np.all(c == ns // 4))
    share_max = k * LN2 - np.log(distinct)
    out = dict(k=k, name=name, ns=ns, distinct=distinct, strength2=bool(ok2),
               share_max=float(share_max), density=float(share_max / k))
    if k <= 20:                       # A_w needs the 2^k transform
        N = 1 << k
        p0 = np.zeros(N)
        p0[bits_to_idx(S)] = 1.0 / distinct
        ph = wht(p0)
        pc = popcount(np.arange(N))
        A = np.array([float(np.sum(ph[pc == w] ** 2)) for w in range(k + 1)])
        d = int(next((w for w in range(1, k + 1) if A[w] > 1e-12), -1))
        out.update(d=d, A1=float(A[1]), A2=float(A[2]),
                   A=[float(x) for x in A],
                   B_moment=float(sum(A[w] / w ** 2 for w in range(1, k + 1))))
    return out


def main():
    res = dict(arms={}, hadamard_orders={})
    for N in (8, 12, 16, 20, 24, 28):
        H = hadamard(N)
        res['hadamard_orders'][N] = dict(
            source=had_source(N),
            verified=bool(np.array_equal(H @ H.T, N * np.eye(N, dtype=int))))
        print(f"H{N:3d}  {had_source(N):16s}  H H^T = {N} I : "
              f"{res['hadamard_orders'][N]['verified']}")

    print("\n=== ARM A: minimum-size OA (the max-share structure) ===")
    print(f"{'k':>3s} {'N0':>3s} {'src':>16s} {'dist':>5s} {'str2':>5s} {'share_max':>10s} "
          f"{'density':>8s} {'d':>2s}")
    for k in range(5, 25):
        S = maxshare_oa(k)
        r = diagnose(k, S, f"OA({N0(k)},{k},2,2) [{had_source(N0(k))}]")
        res['arms'][f'A{k}'] = r
        print(f"{k:3d} {N0(k):3d} {had_source(N0(k)):>16s} {r['distinct']:5d} "
              f"{str(r['strength2']):>5s} {r['share_max']:10.6f} {r['density']:8.5f} "
              f"{r.get('d', -1):2d}")

    print("\n=== ARM B: best linear code with m = ceil(log2(k+1)), |S| = 2^m ===")
    for k in range(5, 25):
        m, cols, how = armB_columns(k)
        S = linear_code(k, cols_to_G(m, cols))
        r = diagnose(k, S, f"linear [{k},{m}] ({how})")
        r.update(m=m, cols=list(map(int, cols)), search=how)
        res['arms'][f'B{k}'] = r
        same = (r['distinct'] == N0(k))
        print(f"{k:3d} m={m} |S|={r['distinct']:3d} str2={str(r['strength2']):>5s} "
              f"share_max={r['share_max']:10.6f} density={r['density']:8.5f} "
              f"d={r.get('d',-1)}  {'== ARM A size' if same else ''}")

    print("\n=== ARM C: the three binary perfect codes ===")
    for k, tag in ((7, 'C7'), (15, 'C15')):
        rr = int(np.log2(k + 1))
        Hchk = np.array([[(c >> b) & 1 for c in range(1, 1 << rr)] for b in range(rr)],
                        dtype=np.int8)
        S = code_from_parity_check(Hchk)
        r = diagnose(k, S, f"perfect Hamming [{k},{k-rr}]")
        res['arms'][tag] = r
        print(f"{k:3d} Hamming [{k},{k-rr}] |S|={r['distinct']:5d} "
              f"str2={str(r['strength2']):>5s} share_max={r['share_max']:10.6f} "
              f"density={r['density']:8.5f} d={r.get('d',-1)}")
    G = golay23()
    S = linear_code(23, G)
    dmin = code_min_distance(S)
    r = diagnose(23, S, "perfect Golay [23,12,7]")
    r['min_distance_sampled'] = int(dmin)
    res['arms']['C23'] = r
    print(f" 23 Golay [23,12] |S|={r['distinct']:5d} str2={str(r['strength2']):>5s} "
          f"share_max={r['share_max']:10.6f} density={r['density']:8.5f} "
          f"(min distance, sampled: {dmin})")

    print("\n=== the density ceiling: maxshare(k)/k, and where it steps ===")
    prev = None
    for k in range(5, 29):
        dens = (k * LN2 - np.log(N0(k))) / k
        mark = ''
        if prev is not None and dens < prev:
            mark = '  <-- STEP (density falls)'
        if k % 4 == 3:
            mark += '   [k = 4m-1, Hadamard-attained]'
        print(f"  k={k:3d}  N0={N0(k):3d}  density={dens:.6f}{mark}")
        prev = dens

    with open('/home/emoore/CIRISOntology/scratchpad/rent_islands_design_check.json',
              'w') as f:
        json.dump(res, f, indent=1)
    print("\nwrote rent_islands_design_check.json")


if __name__ == '__main__':
    main()
