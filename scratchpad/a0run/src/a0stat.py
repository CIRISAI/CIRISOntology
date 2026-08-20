"""A0 — statistics. sec 7.3, sec 7.4, sec 7.5, sec 10.1, sec 15.

The exact 2x2x2 solver and the fibre headroom are CALLED from the existing validated
instrument `scratchpad/glass_share.py` (sec 12 code confinement), which states them to be
byte-for-byte the solver of `dalitz_share.py`.

NEW CODE, declared per sec 12: `share_general` / `share_interval`, the log-linear no-3-way
fit for a 3-level A leg. It carries NO inherited validation. It is cross-checked against
`glass_share.share_2x2x2` on every 2x2x2 table this run computes (`crosscheck` below), and
that cross-check's worst discrepancy is reported in the results.
"""
from __future__ import annotations
import hashlib, math, sys
import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
from glass_share import share_2x2x2, share_headroom, entropy  # noqa: E402

_CROSSCHECK = {"n": 0, "worst": 0.0}


# ---------------------------------------------------------------------------
# the estimator, general I x J x K, exact log-linear no-3-way fit
# ---------------------------------------------------------------------------

def _pair_design(shape):
    """Rows = the three 2-way margins as linear functionals of the flattened table."""
    M = []          # one constraint row per (pair of axes, level-combination)
    for (d0, d1) in ((0, 1), (0, 2), (1, 2)):
        n0, n1 = shape[d0], shape[d1]
        for u in range(n0):
            for v in range(n1):
                r = np.zeros(shape)
                sl = [slice(None)] * 3
                sl[d0] = u
                sl[d1] = v
                r[tuple(sl)] = 1.0
                M.append(r.ravel())
    return np.array(M)


_KERNEL_CACHE = {}


def kernel_basis(shape):
    """Basis of the kernel of the 2-way margin map — the fibre's tangent space.
    dim = (I-1)(J-1)(K-1)."""
    if shape in _KERNEL_CACHE:
        return _KERNEL_CACHE[shape]
    M = _pair_design(shape)
    # null space via SVD
    u, s, vt = np.linalg.svd(M)
    tol = max(M.shape) * (s[0] if len(s) else 1.0) * np.finfo(float).eps
    r = int((s > tol).sum())
    B = vt[r:].T                      # (n_cells, kdim)
    _KERNEL_CACHE[shape] = B
    return B


def _maxent_on_fibre(p, B):
    """Damped Newton on the strictly concave entropy over {p + B d >= 0}.
    Returns the pair-maxent distribution. No IPF anywhere (sec 7.3)."""
    n = p.size
    d = np.zeros(B.shape[1])
    q = p.copy()
    for _ in range(200):
        with np.errstate(divide="ignore"):
            g = B.T @ (np.log(np.clip(q, 1e-300, None)) + 1.0)   # grad of -H
        H = B.T @ (B / np.clip(q, 1e-300, None)[:, None])
        try:
            step = np.linalg.solve(H + 1e-14 * np.eye(H.shape[0]), -g)
        except np.linalg.LinAlgError:
            break
        t = 1.0
        f0 = float(np.sum(q[q > 0] * np.log(q[q > 0])))
        for _ in range(80):
            qn = p + B @ (d + t * step)
            if qn.min() > 0:
                fn = float(np.sum(qn * np.log(qn)))
                if fn <= f0 + 1e-16:
                    break
            t *= 0.5
        else:
            break
        d = d + t * step
        q = p + B @ d
        if np.max(np.abs(g)) < 1e-13 or t * np.max(np.abs(step)) < 1e-15:
            break
    return q


def share_general(tab, crosscheck=True):
    """Whole-only share (order-3 connected information) of an I x J x K table, nats."""
    p = np.asarray(tab, dtype=float)
    shape = p.shape
    s = p.sum()
    if s <= 0:
        return float("nan")
    p = (p / s).ravel()
    B = kernel_basis(shape)
    if B.shape[1] == 0:
        return 0.0
    if p.min() <= 0:
        # zero cells pin the fibre; the exact solver handles them by clipping
        p = np.clip(p, 1e-12, None)
        p = p / p.sum()
    q = _maxent_on_fibre(p, B)
    val = max(0.0, float(entropy(q) - entropy(p)))
    if crosscheck and shape == (2, 2, 2):
        ref = share_2x2x2(np.asarray(tab, dtype=float))
        _CROSSCHECK["n"] += 1
        _CROSSCHECK["worst"] = max(_CROSSCHECK["worst"], abs(val - ref))
        return ref                      # the validated instrument governs at 2x2x2
    return val


def maxent_table(tab):
    """The no-3-way fit m(x), for the cellwise decomposition of C2d."""
    p = np.asarray(tab, dtype=float)
    shape = p.shape
    p = (p / p.sum()).ravel()
    p = np.clip(p, 1e-12, None); p = p / p.sum()
    B = kernel_basis(shape)
    if B.shape[1] == 0:
        return p.reshape(shape)
    return _maxent_on_fibre(p, B).reshape(shape)


def crosscheck_report():
    return dict(_CROSSCHECK)


# ---------------------------------------------------------------------------
# sec 7.5 C2c / V8 — the feasible interval of the share over the fibre, in nats
# ---------------------------------------------------------------------------

def share_interval(tab, ngrid=4001):
    """max and min of the order-3 connected information over the polytope of tables
    carrying the observed two-way margins. All members of the fibre share one
    pair-maxent, so share(q) = H* - H(q) and the interval is [0, H* - min_q H(q)];
    H is concave so its minimum is at a vertex."""
    p = np.asarray(tab, dtype=float)
    shape = p.shape
    p = (p / p.sum()).ravel()
    B = kernel_basis(shape)
    k = B.shape[1]
    if k == 0:
        return 0.0, 0.0
    q0 = _maxent_on_fibre(np.clip(p, 1e-12, None) / np.clip(p, 1e-12, None).sum(), B)
    Hstar = entropy(q0)
    if k == 1:
        b = B[:, 0]
        lo = max((-p[i] / b[i]) for i in range(len(b)) if b[i] > 0)
        hi = min((-p[i] / b[i]) for i in range(len(b)) if b[i] < 0)
        ds = np.linspace(lo, hi, ngrid)
        Hs = [entropy(np.clip(p + d * b, 0, None)) for d in ds]
        return 0.0, float(Hstar - min(Hs))
    if k == 2:
        # 2-D polygon {d : p + B d >= 0}: enumerate vertices from constraint pairs
        A = -B                                   # A d <= p
        rhs = p
        V = []
        m = A.shape[0]
        for i in range(m):
            for j in range(i + 1, m):
                M2 = np.array([A[i], A[j]])
                if abs(np.linalg.det(M2)) < 1e-14:
                    continue
                d = np.linalg.solve(M2, np.array([rhs[i], rhs[j]]))
                if np.all(A @ d <= rhs + 1e-12):
                    V.append(d)
        if not V:
            return 0.0, 0.0
        Hs = [entropy(np.clip(p + B @ d, 0, None)) for d in V]
        return 0.0, float(Hstar - min(Hs))
    # k > 2: random extreme-point search (reported as approximate)
    rng = np.random.default_rng(20260820)
    best = Hstar
    for _ in range(4000):
        u = rng.normal(size=k)
        t = np.inf
        A = -B
        for i in range(A.shape[0]):
            a = A[i] @ u
            if a > 1e-14:
                t = min(t, p[i] / a)
        if not np.isfinite(t):
            continue
        best = min(best, entropy(np.clip(p + B @ (t * u), 0, None)))
    return 0.0, float(Hstar - best)


# ---------------------------------------------------------------------------
# sec 7.3 — ceilings
# ---------------------------------------------------------------------------

LN2 = math.log(2.0)


def sharp_ceiling(tab):
    """`share_le_grouping_gaps`: H(pair) + H(third) - H(p), minimised over the three
    ways of splitting the triple into a pair and a singleton. The pair-maxent carries
    p's pair marginals, so H(Q*) <= H(pair) + H(third) for each split."""
    p = np.asarray(tab, dtype=float)
    p = p / p.sum()
    Hp = entropy(p)
    caps = []
    for third in (0, 1, 2):
        pair_axes = tuple(a for a in (0, 1, 2) if a != third)
        Hpair = entropy(p.sum(axis=third))
        Hthird = entropy(p.sum(axis=pair_axes))
        caps.append(Hpair + Hthird - Hp)
    return float(min(caps)), [float(c) for c in caps]


# ---------------------------------------------------------------------------
# mutual information, AUC, ICC
# ---------------------------------------------------------------------------

def mi_plugin(x, y):
    """Plug-in mutual information in nats between two categorical vectors."""
    xs = sorted(set(x)); ys = sorted(set(y))
    xi = {v: i for i, v in enumerate(xs)}; yi = {v: i for i, v in enumerate(ys)}
    n = len(x)
    T = np.zeros((len(xs), len(ys)))
    for a, b in zip(x, y):
        T[xi[a], yi[b]] += 1
    P = T / n
    px = P.sum(1, keepdims=True); py = P.sum(0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        L = np.where(P > 0, np.log(P / (px * py)), 0.0)
    return float((P * L).sum())


def auc_tie_corrected(scores, labels):
    """Mann-Whitney AUC with mid-ranks for ties; also returns the tied-pair fraction."""
    s = np.asarray(scores, dtype=float); y = np.asarray(labels, dtype=int)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan"), float("nan")
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(len(s), dtype=float)
    sr = s[order]
    i = 0
    while i < len(sr):
        j = i
        while j + 1 < len(sr) and sr[j + 1] == sr[i]:
            j += 1
        ranks[order[i:j + 1]] = 0.5 * (i + j) + 1.0
        i = j + 1
    R = ranks[y == 1].sum()
    n1, n0 = len(pos), len(neg)
    auc = (R - n1 * (n1 + 1) / 2) / (n1 * n0)
    # tied-pair fraction over all cross pairs
    vals, cnt = np.unique(s, return_counts=True)
    tie_pairs = 0
    for v, c in zip(vals, cnt):
        tie_pairs += (y[s == v] == 1).sum() * (y[s == v] == 0).sum()
    return float(auc), float(tie_pairs / (n1 * n0))


def deff_icc(values, clusters):
    """One-way ANOVA intra-cluster correlation and the design effect (sec 3.5)."""
    v = np.asarray(values, dtype=float)
    g = {}
    for i, c in enumerate(clusters):
        g.setdefault(c, []).append(i)
    k, N = len(g), len(v)
    if k < 2 or N <= k:
        return 0.0, N / max(1, k), 1.0
    gm = v.mean()
    msb = sum(len(ix) * (v[ix].mean() - gm) ** 2 for ix in g.values()) / (k - 1)
    msw = sum(((v[ix] - v[ix].mean()) ** 2).sum() for ix in g.values()) / (N - k)
    m = (N - sum(len(ix) ** 2 for ix in g.values()) / N) / (k - 1)
    rho = (msb - msw) / (msb + (m - 1) * msw) if (msb + (m - 1) * msw) > 0 else 0.0
    rho = float(min(max(rho, 0.0), 1.0))
    mbar = N / k
    return rho, mbar, float(1 + (mbar - 1) * rho)


def clopper_pearson_lower(k, n, alpha=0.05):
    from scipy.stats import beta
    if k == 0:
        return 0.0
    return float(beta.ppf(alpha, k, n - k + 1))


def holm(pvals):
    idx = sorted(range(len(pvals)), key=lambda i: pvals[i])
    out = [0.0] * len(pvals)
    run = 0.0
    for r, i in enumerate(idx):
        run = max(run, min(1.0, (len(pvals) - r) * pvals[i]))
        out[i] = run
    return out


# ---------------------------------------------------------------------------
# sec 7.4 — the nulls
# ---------------------------------------------------------------------------

def table_of(a, c, o, shape):
    a = np.asarray(a, dtype=np.int64); c = np.asarray(c, dtype=np.int64)
    o = np.asarray(o, dtype=np.int64)
    idx = (a * shape[1] + c) * shape[2] + o
    return np.bincount(idx, minlength=int(np.prod(shape))).reshape(shape).astype(float)


_SHARE_CACHE = {}


def share_cached(T):
    """Memoised share on the exact integer table. Pure speed: the fibre of a table with
    fixed margins is small, so permutation ensembles revisit tables often."""
    k = (T.shape, np.asarray(T, dtype=np.int64).tobytes())
    v = _SHARE_CACHE.get(k)
    if v is None:
        v = share_general(T)
        if len(_SHARE_CACHE) < 400000:
            _SHARE_CACHE[k] = v
    return v


def thash(T):
    return hashlib.sha1(np.asarray(T, dtype=np.int64).tobytes()).hexdigest()[:16]


def n1c(a, c, o, cluster, ver, seed=20260820, burn=20000, thin=200, ndraw=10000,
        shape=(3, 2, 2), probe_budget=200000):
    """N1c, exactly as sec 7.4 pins it: cluster-swap chain, move = transpose the OVR
    vectors of two clusters equal in size, language and agent_version; accepted iff the
    A-O two-way margin is unchanged. Mixing gate measured, not assumed."""
    rng = np.random.default_rng(seed)
    idx = {}
    for i, cl in enumerate(cluster):
        idx.setdefault(cl, []).append(i)
    keys = list(idx)
    A_ = {k: np.array([a[i] for i in idx[k]]) for k in keys}
    O_ = {k: np.array([o[i] for i in idx[k]]) for k in keys}
    L_ = {k: c[idx[k][0]] for k in keys}
    V_ = {k: ver[idx[k][0]] for k in keys}
    nA = shape[0]
    Mm = {k: np.stack([(A_[k] == t).astype(float) for t in range(nA)], axis=1)
          for k in keys}
    classes = {}
    for k in keys:
        classes.setdefault((len(idx[k]), L_[k], V_[k]), []).append(k)
    swap = [v for v in classes.values() if len(v) > 1]
    n_swappable = sum(len(v) for v in swap)
    rows_swappable = sum(len(idx[k]) for v in swap for k in v)

    T = table_of(a, c, o, shape)
    obs_hash = thash(T)
    seen_tables, seen_states, draws = {obs_hash}, set(), []
    acc = prop = 0
    if not swap:
        return {"draws": [], "acc_rate": 0.0, "distinct_tables": 1,
                "distinct_states": 0, "n_swappable_clusters": 0,
                "rows_swappable": 0, "NON_MIXING": True,
                "reason": "no swap class has two members"}
    wts = np.array([len(v) for v in swap], dtype=float); wts /= wts.sum()
    cum = np.cumsum(wts)
    ACT = {k: np.asarray(A_[k], dtype=np.int64) for k in keys}
    target_acc = burn + thin * ndraw
    BLK = 1 << 16
    buf_u = rng.random(BLK); buf_i = rng.random(BLK); buf_j = rng.random(BLK)
    bp = 0
    cap = target_acc * 200 + probe_budget
    while acc < target_acc and prop < cap:
        if bp >= BLK:
            buf_u = rng.random(BLK); buf_i = rng.random(BLK); buf_j = rng.random(BLK)
            bp = 0
        ci = int(np.searchsorted(cum, buf_u[bp]))
        cl = swap[min(ci, len(swap) - 1)]
        m = len(cl)
        i = int(buf_i[bp] * m); j = int(buf_j[bp] * m)
        bp += 1
        if i == j:
            continue
        k1, k2 = cl[i], cl[j]
        prop += 1
        d = (O_[k2] - O_[k1]).astype(float)
        if not np.array_equal(
                np.bincount(ACT[k1], weights=d, minlength=nA),
                np.bincount(ACT[k2], weights=d, minlength=nA)):
            continue
        O_[k1], O_[k2] = O_[k2], O_[k1]
        acc += 1
        if acc == probe_budget or prop == probe_budget:
            pass
        if acc > burn and (acc - burn) % thin == 0:
            o2 = np.empty(len(o), dtype=int)
            for k in keys:
                o2[idx[k]] = O_[k]
            Td = table_of(a, c, o2, shape)
            seen_tables.add(thash(Td))
            seen_states.add(hashlib.sha1(o2.tobytes()).hexdigest()[:16])
            draws.append(share_cached(Td))
    acc_rate_first = acc / max(1, prop)
    nm = (len(seen_tables) < 1000) or (acc_rate_first < 0.02)
    return {"draws": draws, "acc_rate": float(acc_rate_first),
            "accepted": acc, "proposed": prop,
            "distinct_tables": len(seen_tables), "distinct_states": len(seen_states),
            "n_swappable_clusters": n_swappable, "rows_swappable": rows_swappable,
            "n_clusters": len(keys), "n_rows": len(o),
            "NON_MIXING": bool(nm)}


def n1_exact(a, c, o, shape=(2, 2, 2)):
    """N1: the exact conditional test — enumerate the integer fibre carrying all three
    two-way margins. For 2x2x2 the Diaconis-Sturmfels basis is the single alternating
    +-1 move; for I x 2 x 2 the lattice has dimension I-1 and is enumerated directly."""
    T = table_of(a, c, o, shape)
    I, Jd, K = shape
    assert Jd == 2 and K == 2
    moves = []
    for u in range(I - 1):
        M = np.zeros(shape)
        for du, s0 in ((u, 1.0), (u + 1, -1.0)):
            for x in range(2):
                for y in range(2):
                    M[du, x, y] = s0 * (1.0 if x == y else -1.0)
        moves.append(M)
    # enumerate by bounded search over integer coefficients of the lattice basis
    lims = []
    for M in moves:
        lims.append(int(min(T[M > 0].min(), T[M < 0].min())) + 1)
    tables, shares = [], []
    if len(moves) == 1:
        L = lims[0]
        for d in range(-L, L + 1):
            Td = T + d * moves[0]
            if Td.min() < 0:
                continue
            tables.append(Td); shares.append(share_cached(Td))
    else:
        L0, L1 = lims[0], lims[1]
        for d0 in range(-L0, L0 + 1):
            for d1 in range(-L1, L1 + 1):
                Td = T + d0 * moves[0] + d1 * moves[1]
                if Td.min() < 0:
                    continue
                tables.append(Td); shares.append(share_cached(Td))
    # hypergeometric-style conditional weights: multinomial coefficient of each table
    logw = []
    for Td in tables:
        lw = -sum(math.lgamma(v + 1) for v in np.asarray(Td).ravel())
        logw.append(lw)
    logw = np.array(logw); logw -= logw.max()
    w = np.exp(logw); w /= w.sum()
    obs = share_general(T)
    p = float(w[np.array(shares) >= obs - 1e-15].sum())
    return {"fibre_size": len(tables), "obs": float(obs), "p": p,
            "mean": float((w * np.array(shares)).sum()),
            "shares": [float(s) for s in shares], "weights": [float(x) for x in w]}


def n2(a, c, o, cluster, seed=20260820, ndraw=10000, shape=(3, 2, 2)):
    """N2: permute OVR in whole canonical task_id blocks."""
    rng = np.random.default_rng(seed)
    idx = {}
    for i, cl in enumerate(cluster):
        idx.setdefault(cl, []).append(i)
    keys = list(idx)
    o = np.asarray(o)
    by_size = {}
    for k in keys:
        by_size.setdefault(len(idx[k]), []).append(k)
    groups = []
    for sz, ks in by_size.items():
        RI = np.array([idx[k] for k in ks], dtype=np.int64)
        VV = np.array([o[idx[k]] for k in ks], dtype=np.int64)
        groups.append((RI, VV))
    a = np.asarray(a); c = np.asarray(c)
    out, drift = [], []
    o2 = np.empty(len(o), dtype=np.int64)
    for _ in range(ndraw):
        for RI, VV in groups:
            o2[RI] = VV[rng.permutation(len(VV))]
        Td = table_of(a, c, o2, shape)
        out.append(share_cached(Td))
        drift.append((Td.sum(axis=1)[:, 1], Td.sum(axis=0)[:, 1]))
    return out, drift


def n3(a, c, o, seed=20260820, ndraw=10000, shape=(3, 2, 2)):
    rng = np.random.default_rng(seed)
    o = np.asarray(o); a = np.asarray(a); c = np.asarray(c)
    return [share_cached(table_of(a, c, rng.permutation(o), shape))
            for _ in range(ndraw)]


def pct_p(obs, draws):
    d = np.asarray(draws, dtype=float)
    if d.size == 0:
        return float("nan")
    return float((d >= obs - 1e-15).sum() + 1) / (d.size + 1)
