"""maintenance_sweep.py — is there ANY dynamics that MAINTAINS whole-only share,
and what does maintenance cost?

Pre-registered in scratchpad/MAINTENANCE_SWEEP_PREREG.md, committed at 5d597fe BEFORE
this file existed. Construction facts used by the prereg are in scratchpad/design_check.py.

SCOPE (prereg §0): the substrate is DESIGNED to obey the rent clause. This is a CONTROL,
not a discovery about nature. It measures the PRICE of holding whole-only structure, not
its prevalence. Nothing here bears on the `wild-share` open claim.

Substrate: a population of replicas on a maximum-share support S (a linear code, or the
order-12 Paley/Hadamard orthogonal array), driven each step by
    drift D  ->  bit-flip noise N(eps)  ->  upkeep U(q) (decode to nearest point of S).

Two independent arms:
  EXACT  — propagate the full 2^k distribution (population limit, no sampling error).
  MC     — simulate M replicas on the GPU and read them with the SAME estimator and the
           SAME floors as array_cap_experiment.py / habit_dynamics.py.

Usage:
    python3 maintenance_sweep.py --gate      # gates only
    python3 maintenance_sweep.py --run       # gates, then everything
"""
import sys, os, json, time, argparse
from itertools import combinations
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import array_cap_experiment as ACE          # share machinery, gate, floors

LN2 = float(np.log(2))
SEEDS = [20260725, 99, 7, 1337, 4242]

try:
    import cupy as cp
    _HAS_GPU = True
except Exception:                                            # pragma: no cover
    cp = None
    _HAS_GPU = False


# =====================================================================================
# STRUCTURES  (rebuilt here; identical to design_check.py, which the prereg quotes)
# =====================================================================================

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


def paley_h12():
    """Paley type-I Hadamard matrix of order 12 from the quadratic residues mod 11."""
    q = 11
    qr = set((i * i) % q for i in range(1, q))
    chi = np.array([0] + [1 if a in qr else -1 for a in range(1, q)], dtype=int)
    Q = np.array([[chi[(j - i) % q] for j in range(q)] for i in range(q)], dtype=int)
    S = np.zeros((q + 1, q + 1), dtype=int)
    S[0, 1:] = 1
    S[1:, 0] = -1
    S[1:, 1:] = Q
    return S + np.eye(q + 1, dtype=int)


def hadamard12_oa(k):
    H = paley_h12()
    assert np.array_equal(H @ H.T, 12 * np.eye(12, dtype=int)), "H12 not Hadamard"
    H = H * np.where(H[:, [0]] == -1, -1, 1)
    B = (1 - H[:, 1:]) // 2
    return np.ascontiguousarray(B[:, :k].astype(np.int8))


def dual_distance_of_columns(m, cols):
    k = len(cols)
    if 0 in cols or len(set(cols)) != k:
        return 1 if 0 in cols else 2
    for w in range(3, min(k, 8) + 1):
        for sub in combinations(range(k), w):
            s = 0
            for j in sub:
                s ^= cols[j]
            if s == 0:
                return w
    return min(k, 8) + 1


def code_min_distance(words):
    return min(int(np.sum(words[i] ^ words[j]))
               for i in range(len(words)) for j in range(i + 1, len(words)))


def best_linear_columns(m, k):
    """PRE-REGISTERED comparator rule: maximise dual distance, then minimum distance."""
    best = None
    for cols in combinations(range(1, 1 << m), k):
        dd = dual_distance_of_columns(m, list(cols))
        if best is not None and dd < best[0]:
            continue
        W = linear_code(k, cols_to_G(m, cols))
        key = (dd, code_min_distance(W))
        if best is None or key > best[:2]:
            best = (dd, key[1], list(cols), W)
    return best


def build_structures():
    st = {}
    G5 = np.array([[1, 0, 1, 0, 1], [0, 1, 1, 0, 1], [0, 0, 0, 1, 1]], dtype=np.int8)
    st['L5'] = dict(k=5, S=linear_code(5, G5), kind='linear', m=3,
                    cols=None, name='linear [5,3]')
    st['L7'] = dict(k=7, S=linear_code(7, cols_to_G(3, list(range(1, 8)))), kind='linear',
                    m=3, cols=list(range(1, 8)), name='simplex [7,3]')
    for k in (8, 9, 10, 11, 12):
        dd, dmin, cols, W = best_linear_columns(4, k)
        tag = ('E8' if k == 8 else f'L{k}')
        nm = 'ext-Hamming [8,4,4]' if k == 8 else f'best m=4 linear [{k},4]'
        st[tag] = dict(k=k, S=W, kind='linear', m=4, cols=cols, name=nm)
    cols5 = [c | 16 for c in range(12)]
    st['R12'] = dict(k=12, S=linear_code(12, cols_to_G(5, cols5)), kind='linear', m=5,
                     cols=cols5, name='m=5 affine hyperplane [12,5]')
    for k in (8, 9, 10, 11):
        st[f'H{k}'] = dict(k=k, S=hadamard12_oa(k), kind='hadamard', m=None,
                           cols=None, name='Hadamard-12 OA')
    return st


ROSTER = ['L5', 'L7', 'E8', 'H8', 'H9', 'H10', 'H11', 'L11', 'L12', 'R12']


# =====================================================================================
# EXACT MACHINERY — full 2^k distribution, no sampling
# =====================================================================================

def popcount_table(k):
    return np.array([bin(i).count('1') for i in range(1 << k)], dtype=np.int64)


def wht(a):
    """In-place-safe Walsh-Hadamard. wht(p)[T] = sum_v p_v (-1)^{T.v}."""
    a = a.astype(np.float64, copy=True)
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
    """(n,k) 0/1 -> (n,) integer index, slot 0 = most significant (matches ACE.emp_dist)."""
    bits = np.asarray(bits, dtype=np.int64)
    idx = np.zeros(bits.shape[0], dtype=np.int64)
    for j in range(bits.shape[1]):
        idx = idx * 2 + bits[:, j]
    return idx


def idx_to_bits(idx, k):
    idx = np.asarray(idx, dtype=np.int64)
    return np.stack([(idx >> (k - 1 - j)) & 1 for j in range(k)], axis=1).astype(np.int8)


class Substrate:
    """A maximum-share support S plus everything the dynamics needs, precomputed."""

    def __init__(self, tag, spec):
        self.tag, self.name, self.kind = tag, spec['name'], spec['kind']
        self.k = k = spec['k']
        self.spec = spec
        self.S = np.asarray(spec['S'], dtype=np.int8)
        self.ns = len(self.S)
        self.sidx = bits_to_idx(self.S)
        assert len(set(self.sidx.tolist())) == self.ns, "support points not distinct"
        self.N = 1 << k
        self.pc = popcount_table(k)

        self.p0 = np.zeros(self.N)
        self.p0[self.sidx] = 1.0 / self.ns
        self.share_max = k * LN2 - np.log(self.ns)

        ph = wht(self.p0)
        self.A = np.array([float(np.sum(ph[self.pc == w] ** 2)) for w in range(k + 1)])
        self.d = int(next(w for w in range(1, k + 1) if self.A[w] > 1e-12))
        self._lowmask = (self.pc == 1) | (self.pc == 2)
        self.pair_dev0 = self.max_pair_dev(self.p0)

        # nearest-point decoder, ties enumerated (broken uniformly at random)
        allx = np.arange(self.N, dtype=np.int64)
        D = self.pc[allx[:, None] ^ self.sidx[None, :]]        # (N, ns) Hamming distances
        self.mindist = D.min(axis=1)
        tie = (D == self.mindist[:, None])
        self.nties = tie.sum(axis=1).astype(np.int64)
        self.maxties = int(self.nties.max())
        self.dec_flat = np.zeros((self.N, self.maxties), dtype=np.int64)
        for x in range(self.N):
            w = np.flatnonzero(tie[x])
            self.dec_flat[x, :len(w)] = self.sidx[w]
            self.dec_flat[x, len(w):] = self.sidx[w[0]]
        # exact pushforward weights: row x scatters 1/nties[x] onto each tied support pt
        self.dec_w = (tie / self.nties[:, None])               # (N, ns), rows sum to 1
        self.deterministic_dec = self.dec_flat[:, 0].copy()    # lexicographic sensitivity

    # ---- readouts -------------------------------------------------------------
    def max_pair_dev(self, p):
        pk = p.reshape((2,) * self.k)
        return max(float(np.abs(ACE.pair_marg(pk, i, j) - 0.25).max())
                   for (i, j) in ACE.all_pairs(self.k))

    def pair_dev_bound(self, p):
        """Upper bound on max |pair marginal - 1/4|, from the Fourier coefficients at
        weights 1 and 2 alone.  P(x_i=a,x_j=b) = (1 +- phat(e_i) +- phat(e_j)
        +- phat(e_i+e_j))/4, so the bound is (3/4)*max|phat| over those weights.
        ~15x cheaper than forming every pair marginal, and it is a BOUND, so a pass
        is conclusive."""
        ph = wht(p)
        return 0.75 * float(np.abs(ph[self._lowmask]).max())

    def share_exact(self, p, force_ipf=False):
        """share = sSup(pair envelope) - H.  When the state is exactly pair-uniform the
        envelope top is the uniform state and this is k*ln2 - H; otherwise the IPF
        estimator is used.  Which branch fired is always reported."""
        dev = self.pair_dev_bound(p)
        if dev < 1e-12 and not force_ipf:
            return self.k * LN2 - ACE.H(p), dev, 'closed'
        return ACE.shareK(p.reshape((2,) * self.k))[0], dev, 'ipf'

    # ---- one exact step -------------------------------------------------------
    def noise(self, p, eps):
        lam = 1.0 - 2.0 * eps
        ph = wht(p)
        ph *= lam ** self.pc
        return wht(ph) / self.N

    def decode_push(self, p):
        """Pushforward of p through the (uniform-tie-break) decoder.
        Returns (full 2^k distribution supported on S, distribution over the ns points)."""
        onS = p @ self.dec_w                                    # (ns,)
        full = np.zeros(self.N)
        full[self.sidx] = onS
        return full, onS

    def step(self, p, eps, q, perm=None):
        """One full step. Returns (p_post, diagnostics)."""
        if perm is not None:
            p = p[perm]
        p_pre = self.noise(p, eps)
        if q <= 0.0:
            return p_pre, dict(p_pre=p_pre, cost_erase=0.0, cost_flips=0.0,
                               H_dec=np.nan, dec_unif_dev=np.nan)
        full, onS = self.decode_push(p_pre)
        p_post = (1.0 - q) * p_pre + q * full
        H_dec = ACE.H(onS)
        return p_post, dict(
            p_pre=p_pre,
            cost_erase=q * (ACE.H(p_pre) - H_dec),
            cost_flips=q * float(np.dot(p_pre, self.mindist)),
            H_dec=H_dec,
            dec_unif_dev=float(np.abs(onS - 1.0 / self.ns).max()),
        )

    # ---- closed form for the stationary state (prereg §3.3) --------------------
    def stationary_closed_form(self, eps, q):
        lam = 1.0 - 2.0 * eps
        g = q / (1.0 - (1.0 - q) * lam ** np.arange(self.k + 1)) if q > 0 else \
            np.zeros(self.k + 1)
        if q > 0:
            g[0] = 1.0
        ph = wht(self.p0) * g[self.pc]
        p = wht(ph) / self.N
        return p


def run_exact(sub, eps, q, T, checkpoints=None, perm_mode=None, rng=None):
    """Exact population-limit trajectory. Returns per-step curves."""
    p = sub.p0.copy()
    perm = None
    if perm_mode is not None:
        rng = rng or np.random.default_rng(0)
    share, dev, cost_e, cost_f, branch, decdev = [], [], [], [], [], []
    s, d0, br = sub.share_exact(p)
    share.append(s); dev.append(d0); branch.append(br)
    cost_e.append(0.0); cost_f.append(0.0); decdev.append(np.nan)
    for t in range(T):
        if perm_mode == 'perm':
            sigma = rng.permutation(sub.k)
            perm = bits_to_idx(idx_to_bits(np.arange(sub.N), sub.k)[:, sigma])
            perm = np.argsort(perm)          # p_new[x] = p[perm[x]]
        p, diag = sub.step(p, eps, q, perm=perm)
        s, dv, br = sub.share_exact(p)
        share.append(s); dev.append(dv); branch.append(br)
        cost_e.append(diag['cost_erase']); cost_f.append(diag['cost_flips'])
        decdev.append(diag['dec_unif_dev'])
    return dict(share=np.array(share), pair_dev=np.array(dev),
                cost_erase=np.array(cost_e), cost_flips=np.array(cost_f),
                dec_unif_dev=np.array(decdev), branch=branch, p_final=p)


# =====================================================================================
# MONTE-CARLO ARM — replicas on the GPU, read with the sibling-matched estimator+floors
# =====================================================================================

def mc_trajectory(sub, eps, q, T, M, seed, checkpoints, n_surr=40, n_shuf=10):
    xp = cp if _HAS_GPU else np
    rs = xp.random.default_rng(seed)
    k, N = sub.k, sub.N
    idx = xp.asarray(sub.sidx)[rs.integers(0, sub.ns, size=M)]
    dec_flat = xp.asarray(sub.dec_flat)
    nties = xp.asarray(sub.nties)
    bitval = xp.asarray(1 << np.arange(k - 1, -1, -1, dtype=np.int64))
    out = {}
    ana_rng = np.random.default_rng(seed ^ 0x5EED)
    for t in range(T + 1):
        if t in checkpoints:
            cnt = xp.bincount(idx, minlength=N)
            cnt = cp.asnumpy(cnt) if _HAS_GPU else cnt
            p = cnt.astype(float) / cnt.sum()
            bits = idx_to_bits(np.repeat(np.arange(N), cnt.astype(np.int64)), k)
            out[t] = _analyze_bits(bits, n_surr, n_shuf, ana_rng)
        if t == T:
            break
        flip = (rs.random((M, k)) < eps)
        idx = idx ^ (flip.astype(xp.int64) @ bitval)
        if q > 0:
            coin = rs.random(M) < q
            j = (rs.random(M) * nties[idx]).astype(xp.int64)
            idx = xp.where(coin, dec_flat[idx, j], idx)
    return out


def _analyze_bits(bits, n_surr, n_shuf, rng):
    """The pre-registered readout, on already-binary channels (no binarisation, so the
    tied fraction is exactly 0 by construction — prereg §5)."""
    p, T = ACE.emp_dist(bits)
    r = ACE.caps_and_checks(p)
    mu, sd = ACE.surrogate_null(p, T, n_surr=n_surr, rng=rng)
    smu, ssd = ACE.shuffle_floor(bits, n_shuf=n_shuf, rng=rng)
    r.update(T=T, null_mean=mu, null_sd=sd, excess=r['share'] - mu,
             z=(r['share'] - mu) / sd if sd > 1e-15 else float('nan'),
             shuffle_mean=smu, shuffle_sd=ssd, tie_max=0.0)
    return r


# =====================================================================================
# GATES
# =====================================================================================

def gates(subs):
    print("=" * 78)
    print("GATES — all must PASS before any measurement is read (prereg §8)")
    print("=" * 78)
    res, ok = {}, True

    print("\n--- G1: share machinery (array_cap_experiment.gate) ---")
    g1 = ACE.gate()
    res['G1'] = bool(g1); ok &= bool(g1)

    print("\n--- G2: structures exactly pair-uniform, share_max via the IPF ESTIMATOR ---")
    g2 = True
    for tag in ROSTER:
        s = subs[tag]
        sh_ipf = ACE.shareK(s.p0.reshape((2,) * s.k))[0]
        good = (s.pair_dev0 < 1e-12) and abs(sh_ipf - s.share_max) < 1e-9
        g2 &= good
        print(f"  {tag:4s} k={s.k:2d} |S|={s.ns:2d} d={s.d} pair_dev={s.pair_dev0:.2e} "
              f"share_max={s.share_max:.9f} ipf={sh_ipf:.9f} {'OK' if good else 'FAIL'}")
    res['G2'] = bool(g2); ok &= g2

    print("\n--- G3: Paley H12 -- Hadamard, and strength 2 by direct counting ---")
    H = paley_h12()
    had = np.array_equal(H @ H.T, 12 * np.eye(12, dtype=int))
    B = hadamard12_oa(11)
    counts_ok = True
    for i, j in combinations(range(11), 2):
        c = np.bincount(B[:, i] * 2 + B[:, j], minlength=4)
        counts_ok &= bool(np.all(c == 3))
    rows_distinct = len(set(map(tuple, B.tolist()))) == 12
    g3 = had and counts_ok and rows_distinct
    print(f"  H12 H^T = 12I: {had}   every column pair shows each symbol pair exactly 3x: "
          f"{counts_ok}   12 rows distinct: {rows_distinct}  -> {'PASS' if g3 else 'FAIL'}")
    res['G3'] = bool(g3); ok &= g3

    print("\n--- G4: Fourier propagator == brute-force convolution ---")
    g4 = True
    for tag in ['L5', 'H8']:
        s = subs[tag]
        for eps in (0.03, 0.17):
            p = s.p0.copy()
            # brute force: explicit binomial kernel over all 2^k flip patterns
            ker = np.array([eps ** s.pc[m] * (1 - eps) ** (s.k - s.pc[m])
                            for m in range(s.N)])
            bf = np.zeros(s.N)
            for m in range(s.N):
                bf += ker[m] * p[np.arange(s.N) ^ m]
            fast = s.noise(p, eps)
            err = float(np.abs(bf - fast).max())
            g4 &= err < 1e-12
            print(f"  {tag} eps={eps}: max|brute - fourier| = {err:.3e}")
    res['G4'] = bool(g4); ok &= g4

    print("\n--- G5: MC replica simulator == exact distribution (within multinomial error) ---")
    g5 = True
    for tag in ['L7', 'H8']:
        s = subs[tag]
        for (eps, q, T) in [(0.05, 0.0, 6), (0.05, 0.3, 12)]:
            p = s.p0.copy()
            for _ in range(T):
                p, _d = s.step(p, eps, q)
            M = 400_000
            xp = cp if _HAS_GPU else np
            rs = xp.random.default_rng(12345)
            idx = xp.asarray(s.sidx)[rs.integers(0, s.ns, size=M)]
            dec_flat, nt = xp.asarray(s.dec_flat), xp.asarray(s.nties)
            bv = xp.asarray(1 << np.arange(s.k - 1, -1, -1, dtype=np.int64))
            for _ in range(T):
                idx = idx ^ ((rs.random((M, s.k)) < eps).astype(xp.int64) @ bv)
                if q > 0:
                    coin = rs.random(M) < q
                    j = (rs.random(M) * nt[idx]).astype(xp.int64)
                    idx = xp.where(coin, dec_flat[idx, j], idx)
            cnt = xp.bincount(idx, minlength=s.N)
            cnt = cp.asnumpy(cnt) if _HAS_GPU else cnt
            pmc = cnt / cnt.sum()
            sd = np.sqrt(np.maximum(p, 1e-15) * (1 - p) / M)
            zmax = float(np.abs(pmc - p).max() / sd.max())
            good = zmax < 6.0
            g5 &= good
            print(f"  {tag} eps={eps} q={q} T={T}: max |p_mc - p_exact| / sd_max = "
                  f"{zmax:.2f} {'OK' if good else 'FAIL'}")
    res['G5'] = bool(g5); ok &= g5

    print("\n--- G6: floors floor on independence and recover share_max on the code ---")
    rng = np.random.default_rng(1)
    s = subs['L7']
    Mi = 200_000
    bits_ind = rng.integers(0, 2, size=(Mi, s.k)).astype(np.int8)
    r_ind = _analyze_bits(bits_ind, 40, 10, rng)
    bits_code = s.S[rng.integers(0, s.ns, size=Mi)]
    r_code = _analyze_bits(bits_code, 40, 10, rng)
    g6 = abs(r_ind['excess']) < 5 * r_ind['null_sd'] and \
        abs(r_code['excess'] - s.share_max) < 1e-3
    print(f"  independent bits: excess = {r_ind['excess']:.3e} (null sd {r_ind['null_sd']:.3e}"
          f", z = {r_ind['z']:.2f})   shuffle floor {r_ind['shuffle_mean']:.3e}")
    print(f"  exact code state: excess = {r_code['excess']:.9f} vs share_max "
          f"{s.share_max:.9f}   z = {r_code['z']:.3e}  -> {'PASS' if g6 else 'FAIL'}")
    res['G6'] = bool(g6); ok &= g6

    print("\n--- G7: decoder fixes S pointwise; C-equivariance on linear substrates ---")
    g7 = True
    for tag in ROSTER:
        s = subs[tag]
        fixes = all(int(s.dec_flat[x, 0]) == x and s.nties[x] == 1 for x in s.sidx)
        equi = None
        if s.kind == 'linear':
            # dec(x + c) = dec(x) + c, per x, as the SET of tied nearest codewords
            equi = True
            tie_sets = [set(s.dec_flat[x, :int(s.nties[x])].tolist()) for x in range(s.N)]
            for c in s.sidx.tolist():
                for x in range(s.N):
                    if {y ^ c for y in tie_sets[x]} != tie_sets[x ^ c]:
                        equi = False
                        break
                if not equi:
                    break
            g7 &= bool(equi)
        g7 &= fixes
        print(f"  {tag:4s} decoder fixes S: {fixes}   C-equivariant: {equi}")
    res['G7'] = bool(g7); ok &= g7

    print("\n" + "=" * 78)
    print(f"GATES: {'ALL PASS' if ok else 'FAILURE — run stops'}   {res}")
    print("=" * 78)
    return ok, res


# =====================================================================================
# MEASUREMENTS
# =====================================================================================

EPS_GRID = [0.005, 0.01, 0.02, 0.05, 0.10, 0.20]
Q_GRID = [0.0, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0]


def measure_exact_sweep(subs, T=400):
    """M1: the full exact eps x q x substrate sweep."""
    print("\n" + "=" * 78)
    print("MEASUREMENT 1 — exact sweep (population limit)")
    print("=" * 78)
    out = {}
    t0 = time.time()
    for tag in ROSTER:
        s = subs[tag]
        for eps in EPS_GRID:
            for q in Q_GRID:
                r = run_exact(s, eps, q, T)
                sh = r['share']
                tail = sh[-50:]
                # free-decay asymptotic ratio, taken where the share is still resolvable
                ratio = asym_ratio(sh)[0] if q == 0 else float('nan')
                out[f'{tag}|{eps}|{q}'] = dict(
                    tag=tag, k=s.k, eps=eps, q=q, d=s.d, ns=s.ns,
                    share_max=s.share_max,
                    share_t=[float(x) for x in sh[:9]],
                    share_inf=float(tail.mean()), share_inf_sd=float(tail.std()),
                    retained=float(tail.mean() / s.share_max),
                    cost_erase=float(r['cost_erase'][-50:].mean()),
                    cost_flips=float(r['cost_flips'][-50:].mean()),
                    rent=float(sh[-1] - (s.k * LN2 - ACE.H(
                        s.noise(r['p_final'], eps)))) if True else 0.0,
                    max_pair_dev=float(np.nanmax(r['pair_dev'])),
                    dec_unif_dev=float(np.nanmax(r['dec_unif_dev'])),
                    used_ipf=any(b == 'ipf' for b in r['branch']),
                    asym_ratio=ratio,
                    lam2d=float((1 - 2 * eps) ** (2 * s.d)),
                    closed_form_share=float(
                        s.share_exact(s.stationary_closed_form(eps, q))[0]) if q > 0
                    else 0.0,
                )
        print(f"  {tag:4s} done  ({time.time()-t0:.1f}s)")
    return out


def asym_ratio(sh, lo=1e-12, hi=1e-4):
    """Geometric decay ratio read in a window where the share is well above float64
    underflow and well into the asymptotic regime. Returns (median ratio, n_used)."""
    sh = np.asarray(sh, dtype=float)
    s0 = sh[0] if sh[0] > 0 else 1.0
    ok = np.flatnonzero((sh[:-1] > lo * s0) & (sh[:-1] < hi * s0) & (sh[1:] > lo * s0))
    if len(ok) < 2:
        ok = np.flatnonzero((sh[:-1] > 1e-13) & (sh[1:] > 1e-13))
    if len(ok) < 2:
        return float('nan'), 0
    r = sh[ok + 1] / sh[ok]
    return float(np.median(r)), int(len(r))


def measure_free_decay(subs, T=200):
    """M2: q = 0 -- the shape of free decay, and the head-to-head curves."""
    print("\n" + "=" * 78)
    print("MEASUREMENT 2 — free decay (q = 0): shape, rate, and the k-fixed head-to-heads")
    print("=" * 78)
    out = {}
    for tag in ROSTER:
        s = subs[tag]
        for eps in EPS_GRID:
            r = run_exact(s, eps, 0.0, T)
            sh = r['share']
            with np.errstate(divide='ignore', invalid='ignore'):
                rat = sh[1:] / sh[:-1]
            live = sh > 1e-14
            n_live = int(live.sum()) - 1
            # 1/e time by log-linear interpolation on the live part
            tau = float('nan')
            tgt = sh[0] / np.e
            below = np.flatnonzero(sh < tgt)
            if len(below):
                i = below[0]
                if i > 0 and sh[i] > 0:
                    tau = float(i - 1 + (np.log(sh[i - 1]) - np.log(tgt)) /
                                (np.log(sh[i - 1]) - np.log(sh[i])))
            rr = asym_ratio(sh)
            out[f'{tag}|{eps}'] = dict(
                tag=tag, k=s.k, d=s.d, eps=eps, share_max=s.share_max,
                share=[float(x) for x in sh[:65]],
                asym_ratio=rr[0], asym_n=rr[1],
                pred_ratio=float((1 - 2 * eps) ** (2 * s.d)),
                tau_e=tau, pred_tau=float(1.0 / (2 * s.d * np.log(1 / (1 - 2 * eps)))),
                n_live=n_live, max_pair_dev=float(np.nanmax(r['pair_dev'])),
            )
    return out


def measure_equivariance(subs):
    """M3 (Task 2): does the decoder return the UNIFORM distribution on S?  Guaranteed
    for linear codes; a measured question for the Hadamard OA (prereg §1.1, §6)."""
    print("\n" + "=" * 78)
    print("MEASUREMENT 3 — decoder equivariance: is dec#(uniform(S) (x) noise) uniform on S?")
    print("=" * 78)
    out = {}
    for tag in ROSTER:
        s = subs[tag]
        row = {}
        for eps in [0.01, 0.05, 0.10, 0.20]:
            p = s.noise(s.p0, eps)
            _full, onS = s.decode_push(p)
            row[eps] = dict(max_dev=float(np.abs(onS - 1 / s.ns).max()),
                            ratio=float(onS.max() / onS.min()),
                            H_dec=float(ACE.H(onS)), lnS=float(np.log(s.ns)),
                            onS=[float(x) for x in onS],
                            orbit_sizes=sorted(
                                int(c) for c in np.unique(
                                    np.round(onS, 12), return_counts=True)[1]))
        # also: multi-step (the state a real trajectory presents to the decoder)
        p = s.p0.copy()
        for _ in range(20):
            p, _d = s.step(p, 0.05, 0.0)
        _full, onS = s.decode_push(p)
        row['deep'] = dict(max_dev=float(np.abs(onS - 1 / s.ns).max()),
                           ratio=float(onS.max() / onS.min()))
        out[tag] = dict(k=s.k, kind=s.kind, ns=s.ns, rows=row)
        m = max(row[e]['max_dev'] for e in [0.01, 0.05, 0.10, 0.20])
        print(f"  {tag:4s} k={s.k:2d} {s.kind:9s} |S|={s.ns:2d}  max dev from uniform "
              f"over eps: {m:.3e}   deep(t=20): {row['deep']['max_dev']:.3e}")
    return out


def measure_rent_controller(subs, targets=(1.0, 0.5, 0.1)):
    """M4: the rent-targeting controller -- the direct empirical form of rent_holds.
    Choose q each step to hold the share exactly; report the steady q* and its cost."""
    print("\n" + "=" * 78)
    print("MEASUREMENT 4 — rent targeting: the q that buys standing still, and its bill")
    print("=" * 78)
    out = {}
    qs = np.concatenate([[0.0], np.logspace(-5, 0, 60)])
    for tag in ROSTER:
        s = subs[tag]
        for eps in [0.01, 0.05, 0.20]:
            for frac in targets:
                # settle onto the target level under free decay, then hold it
                p = s.p0.copy()
                tgt = frac * s.share_max
                for _ in range(4000):
                    cur = s.share_exact(p)[0]
                    if cur <= tgt:
                        break
                    p, _d = s.step(p, eps, 0.0)
                hold, qhist, cost_e, cost_f = True, [], [], []
                for _ in range(60):
                    cur = s.share_exact(p)[0]
                    p_pre = s.noise(p, eps)
                    full, onS = s.decode_push(p_pre)
                    vals = np.array([s.share_exact((1 - qq) * p_pre + qq * full)[0]
                                     for qq in qs])
                    okq = np.flatnonzero(vals >= cur)
                    if not len(okq):
                        hold = False
                        break
                    i = okq[0]
                    # refine by bisection between qs[i-1] and qs[i]
                    lo, hi = qs[max(i - 1, 0)], qs[i]
                    for _ in range(40):
                        mid = 0.5 * (lo + hi)
                        if s.share_exact((1 - mid) * p_pre + mid * full)[0] >= cur:
                            hi = mid
                        else:
                            lo = mid
                    qq = hi
                    qhist.append(qq)
                    cost_e.append(qq * (ACE.H(p_pre) - ACE.H(onS)))
                    cost_f.append(qq * float(np.dot(p_pre, s.mindist)))
                    p = (1 - qq) * p_pre + qq * full
                out[f'{tag}|{eps}|{frac}'] = dict(
                    tag=tag, k=s.k, d=s.d, eps=eps, frac=frac, held=hold,
                    share_held=float(s.share_exact(p)[0]),
                    share_max=s.share_max,
                    q_star=float(np.mean(qhist[-20:])) if qhist else float('nan'),
                    q_sd=float(np.std(qhist[-20:])) if qhist else float('nan'),
                    cost_erase=float(np.mean(cost_e[-20:])) if cost_e else float('nan'),
                    cost_flips=float(np.mean(cost_f[-20:])) if cost_f else float('nan'),
                    rent_nats=float(s.share_exact(p)[0] -
                                    s.share_exact(s.noise(p, eps))[0]),
                )
        print(f"  {tag:4s} done")
    return out


def measure_arms(subs):
    """M5: the drift arms -- AUT (trivial), PERM, SCRAMBLE, MISMATCH."""
    print("\n" + "=" * 78)
    print("MEASUREMENT 5 — drift arms: automorphism, coordinate permutation, scramble,")
    print("                and upkeep pointed at the WRONG structure")
    print("=" * 78)
    out = {}
    rng = np.random.default_rng(20260725)

    # --- AUT: translations (always automorphisms of a linear code) + found column perms
    for tag in ROSTER:
        s = subs[tag]
        auts = find_automorphisms(s, limit=60, rng=rng)
        devs = []
        for (sigma, c) in auts:
            perm = aut_perm(s, sigma, c)
            devs.append(abs(s.share_exact(s.p0[perm])[0] - s.share_max))
        out[f'AUT|{tag}'] = dict(n_found=len(auts),
                                 max_share_change=float(max(devs)) if devs else None)
        print(f"  AUT      {tag:4s}: {len(auts):3d} automorphisms found, "
              f"max |Dshare| = {max(devs) if devs else float('nan'):.3e}")

    # --- SCRAMBLE: random bijection of {0,1}^k. Entropy fixed, structure destroyed.
    for tag in ROSTER:
        s = subs[tag]
        vals, Hs = [], []
        for _ in range(20):
            pi = rng.permutation(s.N)
            p = np.zeros(s.N)
            p[pi[s.sidx]] = 1.0 / s.ns
            vals.append(ACE.shareK(p.reshape((2,) * s.k))[0])
            Hs.append(ACE.H(p))
        out[f'SCRAMBLE|{tag}'] = dict(
            share_mean=float(np.mean(vals)), share_sd=float(np.std(vals)),
            share_max=s.share_max, frac=float(np.mean(vals) / s.share_max),
            H_mean=float(np.mean(Hs)), H_target=float(np.log(s.ns)),
            H_exact=bool(np.allclose(Hs, np.log(s.ns))))
        print(f"  SCRAMBLE {tag:4s}: share {np.mean(vals):.4f} +- {np.std(vals):.4f} "
              f"({np.mean(vals)/s.share_max:.1%} of max)   H fixed at ln|S|: "
              f"{np.allclose(Hs, np.log(s.ns))}")

    # --- PERM (share-neutral drift) and MISMATCH (upkeep to the original S)
    for tag in ['L7', 'E8', 'H8', 'L12']:
        s = subs[tag]
        r_perm = run_exact(s, 0.0, 0.0, 12, perm_mode='perm',
                           rng=np.random.default_rng(11))
        # mismatch: drift + full upkeep to the ORIGINAL S
        rr = {}
        for q in (0.0, 1.0):
            r = run_exact(s, 0.05, q, 40, perm_mode='perm',
                          rng=np.random.default_rng(11))
            rr[q] = [float(x) for x in r['share']]
        out[f'PERM|{tag}'] = dict(
            share=[float(x) for x in r_perm['share']],
            max_change=float(np.abs(r_perm['share'] - s.share_max).max()))
        out[f'MISMATCH|{tag}'] = dict(share_max=s.share_max, q0=rr[0.0], q1=rr[1.0])
        print(f"  PERM     {tag:4s}: max |Dshare| under pure drift (eps=q=0) = "
              f"{np.abs(r_perm['share'] - s.share_max).max():.3e}")
        print(f"  MISMATCH {tag:4s}: drift + FULL upkeep to the original S -> share "
              f"{rr[1.0][-1]:.4f} vs no upkeep {rr[0.0][-1]:.4f} "
              f"(max {s.share_max:.4f})")
    return out


def find_automorphisms(sub, limit=60, rng=None):
    """(sigma, c) with sigma(S) + c = S. Translations by codewords are automorphisms of
    any linear code; column permutations are searched for."""
    rng = rng or np.random.default_rng(0)
    k, target = sub.k, set(map(tuple, sub.S.tolist()))
    found = []
    if sub.kind == 'linear':
        for c in sub.S[:min(limit // 2, sub.ns)]:
            found.append((np.arange(k), c.copy()))
    tries = 0
    while len(found) < limit and tries < 20000:
        tries += 1
        sigma = rng.permutation(k)
        Sp = sub.S[:, sigma]
        for c in list(sub.S[:4]) + [np.zeros(k, dtype=np.int8)]:
            if set(map(tuple, (Sp ^ c).tolist())) == target:
                found.append((sigma, np.asarray(c, dtype=np.int8).copy()))
                break
    return found


def aut_perm(sub, sigma, c):
    """Index permutation implementing x -> sigma(x) + c, as p_new[y] = p[perm[y]]."""
    B = idx_to_bits(np.arange(sub.N), sub.k)
    img = bits_to_idx(B[:, sigma] ^ c)
    perm = np.empty(sub.N, dtype=np.int64)
    perm[img] = np.arange(sub.N)
    return perm


def measure_mc(subs, T=64, M=500_000, n_surr=40, n_shuf=10):
    """M6: the Monte-Carlo arm with the sibling-matched floors."""
    print("\n" + "=" * 78)
    print("MEASUREMENT 6 — Monte-Carlo arm, sibling-matched surrogate + shuffle floors")
    print("=" * 78)
    cps = {0, 1, 2, 4, 8, 16, 32, 64}
    out = {}
    t0 = time.time()
    for tag in ['L5', 'L7', 'E8', 'H8', 'H11', 'L12']:
        s = subs[tag]
        for eps in (0.02, 0.05):
            for q in (0.0, 0.01, 0.1, 1.0):
                exact = run_exact(s, eps, q, T)
                per_seed = {}
                for sd in SEEDS:
                    per_seed[sd] = mc_trajectory(s, eps, q, T, M, sd, cps,
                                                 n_surr=n_surr, n_shuf=n_shuf)
                for t in sorted(cps):
                    ex = [per_seed[sd][t]['excess'] for sd in SEEDS]
                    zz = [per_seed[sd][t]['z'] for sd in SEEDS]
                    nm = [per_seed[sd][t]['null_mean'] for sd in SEEDS]
                    sm = [per_seed[sd][t]['shuffle_mean'] for sd in SEEDS]
                    caps = all(per_seed[sd][t]['chk_cap_robust'] and
                               per_seed[sd][t]['chk_cap_headline'] for sd in SEEDS)
                    out[f'{tag}|{eps}|{q}|{t}'] = dict(
                        tag=tag, k=s.k, eps=eps, q=q, t=t, M=M,
                        excess=float(np.mean(ex)), excess_sem=float(np.std(ex) / np.sqrt(5)),
                        z=float(np.mean(zz)), null_mean=float(np.mean(nm)),
                        shuffle_mean=float(np.mean(sm)),
                        exact_share=float(exact['share'][t]),
                        share_max=s.share_max, cap_ok=bool(caps), tie_max=0.0)
                print(f"  {tag:4s} eps={eps} q={q}  done ({time.time()-t0:.0f}s)")
    return out


# =====================================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gate', action='store_true')
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--out', default='/home/emoore/CIRISOntology/scratchpad/maintenance_sweep_results.json')
    a = ap.parse_args()

    print(f"GPU: {'cupy available' if _HAS_GPU else 'CPU only'}")
    print("Building structures (the m=4 comparator search is exhaustive over C(15,k))...")
    specs = build_structures()
    subs = {t: Substrate(t, specs[t]) for t in ROSTER}

    ok, gres = gates(subs)
    if not ok:
        print("GATE FAILURE — stopping, per prereg §8.")
        sys.exit(1)
    if a.gate:
        return

    results = dict(gates=gres, prereg='5d597fe',
                   roster={t: dict(k=subs[t].k, ns=subs[t].ns, d=subs[t].d,
                                   kind=subs[t].kind, name=subs[t].name,
                                   share_max=subs[t].share_max,
                                   A=[float(x) for x in subs[t].A])
                           for t in ROSTER})
    results['equivariance'] = measure_equivariance(subs)
    results['free_decay'] = measure_free_decay(subs)
    results['exact_sweep'] = measure_exact_sweep(subs)
    results['rent'] = measure_rent_controller(subs)
    results['arms'] = measure_arms(subs)
    results['mc'] = measure_mc(subs)

    with open(a.out, 'w') as f:
        json.dump(results, f, indent=1)
    print(f"\nwrote {a.out}")


if __name__ == '__main__':
    main()
