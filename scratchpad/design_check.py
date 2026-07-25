"""design_check.py -- CONSTRUCTION validation only, run BEFORE the prereg is written.

This computes properties of the candidate SUBSTRATES (which codes / orthogonal arrays
exist, are they pair-uniform, what is their Fourier weight profile). It runs NO dynamics
and measures NOTHING about maintenance. Its outputs are design facts that the
pre-registration quotes and derives predictions from.
"""
import numpy as np
from itertools import combinations

LN2 = float(np.log(2))


# ---------------------------------------------------------------- structures

def linear_code(k, G):
    """G: (m,k) 0/1 generator. Returns the 2^m codewords as (2^m,k) array."""
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


def simplex_columns(m, k, drop=None):
    """k distinct nonzero columns in F_2^m -> (m,k) generator of a punctured simplex."""
    cols = [c for c in range(1, 1 << m)]
    if drop:
        cols = [c for c in cols if c not in drop]
    cols = cols[:k]
    assert len(cols) == k, (m, k, len(cols))
    G = np.zeros((m, k), dtype=np.int8)
    for j, c in enumerate(cols):
        for b in range(m):
            G[b, j] = (c >> b) & 1
    return G


def ext_hamming8():
    """[8,4,4] extended Hamming, self-dual."""
    G = np.array([
        [1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 1, 1, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ], dtype=np.int8)
    return linear_code(8, G)


def paley_h12():
    """Paley type-I Hadamard matrix of order 12 from quadratic residues mod 11."""
    q = 11
    qr = set((i * i) % q for i in range(1, q))
    chi = np.zeros(q, dtype=int)
    for a in range(1, q):
        chi[a] = 1 if a in qr else -1
    Q = np.zeros((q, q), dtype=int)
    for i in range(q):
        for j in range(q):
            Q[i, j] = chi[(j - i) % q]
    # Paley I:  S = [[0, 1...1], [-1...-1, Q]],  H = S + I  is Hadamard of order q+1.
    S = np.zeros((q + 1, q + 1), dtype=int)
    S[0, 1:] = 1
    S[1:, 0] = -1
    S[1:, 1:] = Q
    H = S + np.eye(q + 1, dtype=int)
    return H


def hadamard12_oa(k):
    """OA(12,11,2,2) from Paley H12; take the first k of its 11 binary columns."""
    H = paley_h12()
    assert np.array_equal(H @ H.T, 12 * np.eye(12, dtype=int)), "H12 not Hadamard"
    # normalise first column to +1
    H = H * np.where(H[:, [0]] == -1, -1, 1)
    assert np.all(H[:, 0] == 1)
    B = (1 - H[:, 1:]) // 2          # 12 x 11 binary
    return np.ascontiguousarray(B[:, :k].astype(np.int8))


# ---------------------------------------------------------------- Fourier

def uniform_dist(support, k):
    p = np.zeros(1 << k)
    for v in support:
        idx = 0
        for j in range(k):
            idx = idx * 2 + int(v[j])
        p[idx] += 1.0
    return p / p.sum()


def wht(p):
    """Walsh-Hadamard: returns phat(S) = sum_v p_v (-1)^{S.v}, indexed by S."""
    a = p.copy()
    n = a.size
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            x = a[i:i + h].copy()
            y = a[i + h:i + 2 * h].copy()
            a[i:i + h] = x + y
            a[i + h:i + 2 * h] = x - y
        h *= 2
    return a


def popcounts(k):
    return np.array([bin(i).count('1') for i in range(1 << k)])


def fourier_profile(p, k):
    """A_w = sum over |S|=w of phat(S)^2 ; and max |phat| per weight."""
    ph = wht(p)
    w = popcounts(k)
    A = np.zeros(k + 1)
    mx = np.zeros(k + 1)
    for ww in range(k + 1):
        m = (w == ww)
        A[ww] = float(np.sum(ph[m] ** 2))
        mx[ww] = float(np.max(np.abs(ph[m])))
    return A, mx, ph


def H_nats(p):
    p = p[p > 1e-300]
    return float(-np.sum(p * np.log(p)))


def report(name, support, k):
    support = np.asarray(support, dtype=np.int8)
    p = uniform_dist(support, k)
    nsupp = int(np.count_nonzero(p))
    A, mx, ph = fourier_profile(p, k)
    d = next((w for w in range(1, k + 1) if A[w] > 1e-12), None)
    Hp = H_nats(p)
    share = k * LN2 - Hp
    pu = max(abs(A[1]), abs(A[2])) < 1e-12
    print(f"\n{name}:  k={k}  |supp|={nsupp}  pair-uniform={pu}")
    print(f"   H = {Hp:.9f} = ln {np.exp(Hp):.4f}    share_max = {share:.9f} "
          f"= {share/LN2:.4f} * ln2")
    print(f"   lowest nonzero Fourier weight d = {d}   A_d = {A[d]:.6f}  "
          f"(count {int(round(A[d]/mx[d]**2)) if mx[d]>0 else 0} coeffs of |phat|={mx[d]:.4f})")
    print(f"   A_w = " + "  ".join(f"{w}:{A[w]:.4f}" for w in range(k + 1) if A[w] > 1e-12))
    # pairwise Hamming distance spectrum of the support
    ds = [int(np.sum(support[i] ^ support[j]))
          for i, j in combinations(range(len(support)), 2)]
    print(f"   support pairwise distances: min={min(ds)} max={max(ds)} "
          f"spectrum={dict(sorted({x: ds.count(x) for x in set(ds)}.items()))}")
    return dict(name=name, k=k, nsupp=nsupp, share_max=share, d=d, A=A.tolist(),
                pair_uniform=bool(pu), Hp=Hp)


def code_min_distance(words):
    n = len(words)
    best = 10 ** 9
    for i in range(n):
        for j in range(i + 1, n):
            best = min(best, int(np.sum(words[i] ^ words[j])))
    return best


def dual_distance_of_columns(m, cols):
    """cols: list of k nonzero ints in [1,2^m). Dual distance = min weight of a
    nonempty column subset summing to 0 (>=3 iff nonzero+distinct)."""
    k = len(cols)
    if len(set(cols)) != k or 0 in cols:
        return 2 if len(set(cols)) != k else 1
    # search increasing subset size
    for w in range(3, min(k, 8) + 1):
        for sub in combinations(range(k), w):
            s = 0
            for j in sub:
                s ^= cols[j]
            if s == 0:
                return w
    return min(k, 8) + 1


def best_linear_columns(m, k):
    """Pre-registered comparator rule: over all k-subsets of the nonzero vectors of
    F_2^m, maximise dual distance first, then the code's minimum distance."""
    allc = list(range(1, 1 << m))
    best = None
    for cols in combinations(allc, k):
        dd = dual_distance_of_columns(m, list(cols))
        if best is not None and dd < best[0]:
            continue
        G = np.zeros((m, k), dtype=np.int8)
        for j, c in enumerate(cols):
            for b in range(m):
                G[b, j] = (c >> b) & 1
        W = linear_code(k, G)
        dmin = code_min_distance(W)
        key = (dd, dmin)
        if best is None or key > best[:2]:
            best = (dd, dmin, cols, W)
    return best


if __name__ == "__main__":
    print("=" * 78)
    print("DESIGN CHECK -- construction properties only, no dynamics")
    print("=" * 78)

    out = []
    # k=5 [5,3]
    G5 = np.array([[1, 0, 1, 0, 1], [0, 1, 1, 0, 1], [0, 0, 0, 1, 1]], dtype=np.int8)
    out.append(report("k=5 linear [5,3]", linear_code(5, G5), 5))

    out.append(report("k=6 punctured simplex [6,3]", linear_code(6, simplex_columns(3, 6)), 6))
    out.append(report("k=7 simplex [7,3]", linear_code(7, simplex_columns(3, 7)), 7))

    out.append(report("k=8 ext-Hamming [8,4,4]", ext_hamming8(), 8))
    for k in (8, 9, 10, 11):
        out.append(report(f"k={k} Hadamard-12 OA", hadamard12_oa(k), k))
    for k in (8, 9, 10, 11, 12):
        dd, dmin, cols, W = best_linear_columns(4, k)
        print(f"\n[best m=4 linear at k={k}: cols={cols} dual_dist={dd} d_min={dmin}]")
        out.append(report(f"k={k} best linear m=4", W, k))
    # capacity/robustness frontier partner at k=12: 32 words, dual distance >= 4
    cols5 = [c | 16 for c in range(12)]           # affine hyperplane in F_2^5
    G = np.zeros((5, 12), dtype=np.int8)
    for j, c in enumerate(cols5):
        for b in range(5):
            G[b, j] = (c >> b) & 1
    print(f"\n[k=12 m=5 affine-hyperplane cols={cols5} "
          f"dual_dist={dual_distance_of_columns(5, cols5)}]")
    out.append(report("k=12 linear m=5 (affine hyperplane)", linear_code(12, G), 12))

    print("\n" + "=" * 78)
    print("SUMMARY TABLE (design facts the prereg will quote)")
    print("=" * 78)
    print(f"{'structure':34s} {'k':>3s} {'|S|':>4s} {'share_max':>11s} {'/ln2':>7s} "
          f"{'d':>3s} {'A_d':>9s}")
    for r in out:
        print(f"{r['name']:34s} {r['k']:3d} {r['nsupp']:4d} {r['share_max']:11.6f} "
              f"{r['share_max']/LN2:7.4f} {r['d']:3d} {r['A'][r['d']]:9.5f}")

    import json
    with open('/home/emoore/CIRISOntology/scratchpad/design_check.json', 'w') as f:
        json.dump(out, f, indent=1)
    print("\nwrote design_check.json")
