#!/usr/bin/env python3
"""Annihilating coherent Monte Carlo for the REG+ lattice.

Independent reimplementation from the frozen prereg text
(REG_HYDRO_COHERENT_ANNIHILATING_MC_PREREG.md). Backend-agnostic: the same code runs on
numpy (CPU, correctness path) or cupy (GPU, production path).

Walkers are GPU-resident:
    st : (W, nsites) uint8  -- one 6-bit local state per site
    wt : (W,)       complex128
Configuration keys are bit-packed 10 sites (60 bits) per uint64 word, so no state straddles
a word boundary.

All accumulators are fp64 / complex128.
"""
from __future__ import annotations
import numpy as np
import mc_tables as T
import regmodel as R

_XP = np
_NAME = "cpu"


def set_backend(name):
    """Select 'cpu' (numpy) or 'gpu' (cupy)."""
    global _XP, _NAME
    if name == "gpu":
        import cupy
        _XP, _NAME = cupy, "gpu"
    elif name == "cpu":
        _XP, _NAME = np, "cpu"
    else:
        raise ValueError(name)
    return _XP


def xp():
    return _XP


def backend_name():
    return _NAME


def make_rng(seed):
    if _NAME == "gpu":
        import cupy
        return cupy.random.default_rng(seed)
    return np.random.default_rng(seed)


SITES_PER_WORD = 10          # 10 sites x 6 bits = 60 bits, no straddling


# ---------------------------------------------------------------- device tables
class Tables:
    """Collision/stream tables resident on the active backend."""

    def __init__(self, L, theta=R.THETA, phi=R.PHI_DEFAULT):
        x = _XP
        UCOL, OUT, QCOL = T.collision_tables(theta, phi)
        self.L = L
        self.nsites = L * L
        self.nwords = (self.nsites + SITES_PER_WORD - 1) // SITES_PER_WORD
        self.UCOL = x.asarray(UCOL)
        self.OUT = x.asarray(OUT)
        self.QCOL = x.asarray(QCOL)
        self.QCUM = x.asarray(np.cumsum(QCOL, axis=1))
        self.KMAX = x.asarray(T.kmax_table())
        self.dst = x.asarray(T.stream_dst(L))
        self.pair_states = R.PAIR_STATES


# ---------------------------------------------------------------- propagation
def collide(st, wt, tab, rng, forced_origin=None):
    """One global collision: sample each site's output independently for every walker.

    q_k = |u_k|^2 with u_k = U[k, j] the sector-unitary column of the site's input state;
    the weight is multiplied by u_k / q_k. Sites in size-1 sectors take k=0 with
    probability 1 and factor exactly 1, with no special-casing.
    """
    x = _XP
    W = st.shape[0]
    ar = x.arange(W)
    for site in range(tab.nsites):
        s = st[:, site].astype(x.int32)
        if site == 0 and forced_origin is not None:
            # dephasing-branch preparation: force the origin output, weight factor 1.0
            st[:, site] = x.uint8(tab.pair_states[forced_origin])
            continue
        cum = tab.QCUM[s]                       # (W,3) float64
        r = rng.random(W, dtype=x.float64)
        k = (r[:, None] >= cum).sum(axis=1)
        # Clamp to the site's own sector size. cumsum(QCOL[s]) can fall short of 1.0 by up
        # to ~1e-15, so without this a draw just below 1 selects an out-of-sector slot whose
        # sampling probability is exactly 0, and the u/q update returns an infinite weight.
        k = x.minimum(k, tab.KMAX[s])
        st[:, site] = tab.OUT[s, k]
        wt *= tab.UCOL[s, k] / tab.QCOL[s, k]
    return st, wt


def stream(st, tab):
    """Deterministic carries: channel a of every site moves one axial edge. Weights untouched."""
    x = _XP
    new = x.zeros_like(st)
    for a in range(6):
        bit = (st >> np.uint8(a)) & np.uint8(1)
        new[:, tab.dst[a]] |= (bit << np.uint8(a))
    return new


def pack_keys(st, tab):
    """(W, nsites) uint8 states -> (W, nwords) uint64 bijective key."""
    x = _XP
    W = st.shape[0]
    keys = x.zeros((W, tab.nwords), dtype=x.uint64)
    for site in range(tab.nsites):
        w, off = divmod(site, SITES_PER_WORD)
        keys[:, w] |= st[:, site].astype(x.uint64) << x.uint64(6 * off)
    return keys


# ---------------------------------------------------------------- annihilation
def _lexsort_keys(keys):
    """Sort order grouping identical multi-word keys together."""
    x = _XP
    return x.lexsort(keys.T[::-1])


def _segment_ids(keys_sorted):
    """(seg_id per row, n_unique, index of first row of each segment)."""
    x = _XP
    n = keys_sorted.shape[0]
    if n == 0:
        return x.zeros(0, dtype=x.int64), 0, x.zeros(0, dtype=x.int64)
    diff = x.zeros(n, dtype=bool)
    diff[1:] = (keys_sorted[1:] != keys_sorted[:-1]).any(axis=1)
    seg = x.cumsum(diff.astype(x.int64))
    n_unique = int(seg[-1]) + 1
    first = x.flatnonzero(x.concatenate([x.ones(1, dtype=bool), diff[1:]]))
    return seg, n_unique, first


def _segment_complex_sum(seg, n_unique, wt):
    """Segmented complex sum in fp64."""
    x = _XP
    re = x.bincount(seg, weights=wt.real, minlength=n_unique)
    im = x.bincount(seg, weights=wt.imag, minlength=n_unique)
    return re + 1j * im


def annihilate(st, wt, tab):
    """Steps 1-3 of the frozen recipe: aggregate identical configurations by COMPLEX sum.

    Returns (rep_st, s_c, S) where rep_st is one representative site-state row per surviving
    configuration and s_c the annihilated complex amplitude at it.
    """
    x = _XP
    keys = pack_keys(st, tab)
    order = _lexsort_keys(keys)
    ks = keys[order]
    seg, n_unique, first = _segment_ids(ks)
    s_c = _segment_complex_sum(seg, n_unique, wt[order])
    rep_st = st[order][first]
    S = float(x.abs(s_c).sum())
    return rep_st, s_c, S


def resample(rep_st, s_c, S, W, rng):
    """Steps 4-5: exactly W i.i.d. draws with q_c = |s_c|/S; w'_c = (S/W) * s_c/|s_c|."""
    x = _XP
    absS = x.abs(s_c)
    cum = x.cumsum(absS)
    u = rng.random(W, dtype=x.float64) * S
    idx = x.searchsorted(cum, u, side="right")
    idx = x.minimum(idx, absS.shape[0] - 1)
    st_new = rep_st[idx]
    wt_new = (S / W) * (s_c[idx] / absS[idx])
    return st_new, wt_new


def annihilate_and_resample(st, wt, tab, W, rng):
    rep_st, s_c, S = annihilate(st, wt, tab)
    if S == 0.0:
        raise ZeroAmplitude("replica collapsed to zero amplitude")
    st_new, wt_new = resample(rep_st, s_c, S, W, rng)
    return st_new, wt_new, S, s_c.shape[0]


class ZeroAmplitude(RuntimeError):
    pass


# ---------------------------------------------------------------- estimators
def amplitude_map(st, wt, tab, W):
    """A_hat(c) = (1/W) sum of walker weights at c, on the post-final-resampling population."""
    rep_st, s_c, _ = annihilate(st, wt, tab)
    return pack_keys(rep_st, tab), s_c / W, rep_st[:, 0]


def cross_probs(mapA, mapB, tab):
    """P_hat(E_j) = Re sum_{c in E_j} conj(A_hat(c)) B_hat(c), over configurations in BOTH."""
    x = _XP
    kA, aA, oA = mapA
    kB, aB, oB = mapB
    nA = kA.shape[0]
    if nA == 0 or kB.shape[0] == 0:
        return np.zeros(3)
    allk = x.concatenate([kA, kB], axis=0)
    tag = x.concatenate([x.zeros(nA, dtype=x.int64), x.ones(kB.shape[0], dtype=x.int64)])
    amp = x.concatenate([aA, aB])
    org = x.concatenate([oA, oB])
    order = _lexsort_keys(allk)
    ks, tg, am, og = allk[order], tag[order], amp[order], org[order]
    same = (ks[1:] == ks[:-1]).all(axis=1) & (tg[1:] != tg[:-1])
    hit = x.flatnonzero(same)
    if hit.shape[0] == 0:
        return np.zeros(3)
    # orient each matched pair as (A, B) then take Re(conj(A) B); Re is symmetric in the
    # pair so the ordering does not matter.
    prod = (am[hit].conj() * am[hit + 1]).real
    ostate = og[hit]
    out = np.zeros(3)
    for j, ps in enumerate(tab.pair_states):
        out[j] = float(prod[ostate == ps].sum())
    return out


# ---------------------------------------------------------------- drivers
def run_replica(L, init_st, forced_origin, W, seed, tab):
    """collide, A/R, then L times (stream, collide, A/R); return the amplitude map."""
    x = _XP
    rng = make_rng(seed)
    st = x.asarray(np.tile(init_st, (W, 1)))
    wt = x.ones(W, dtype=x.complex128)
    st, wt = collide(st, wt, tab, rng, forced_origin=forced_origin)
    st, wt, S, nu = annihilate_and_resample(st, wt, tab, W, rng)
    for _ in range(L):
        st = stream(st, tab)
        st, wt = collide(st, wt, tab, rng, forced_origin=None)
        st, wt, S, nu = annihilate_and_resample(st, wt, tab, W, rng)
    return amplitude_map(st, wt, tab, W), nu


def batch_M(L, init_st, W, seed_pair, tab, branch_weights):
    """One replica-pair batch: coherent arm plus the three dephasing branches -> M."""
    (sA, sB) = seed_pair
    mA, nuA = run_replica(L, init_st, None, W, sA, tab)
    mB, nuB = run_replica(L, init_st, None, W, sB, tab)
    q_coh = cross_probs(mA, mB, tab)
    q_deph = np.zeros(3)
    for j in range(3):
        bA, _ = run_replica(L, init_st, j, W, sA + 1_000_000_000 * (j + 1), tab)
        bB, _ = run_replica(L, init_st, j, W, sB + 1_000_000_000 * (j + 1), tab)
        q_deph += branch_weights[j] * cross_probs(bA, bB, tab)
    # The cross estimator can return zero support when the two replicas share no
    # configuration in the head-on-pair event set. That is a genuine small-W failure mode of
    # the frozen estimator, not a numerical accident: flag it, never silently average it away.
    if q_coh.sum() == 0.0 or q_deph.sum() == 0.0:
        return (float("nan"), np.full(3, np.nan), np.full(3, np.nan),
                float(q_coh.sum()), float(q_deph.sum()), (nuA + nuB) / 2.0)
    p_coh = q_coh / q_coh.sum()
    p_deph = q_deph / q_deph.sum()
    M = 0.5 * float(np.abs(p_coh - p_deph).sum())
    return M, p_coh, p_deph, q_coh.sum(), q_deph.sum(), (nuA + nuB) / 2.0


def estimate_M(L, spectator_modes, W, n_batches, seeds, theta=R.THETA, phi=R.PHI_DEFAULT):
    """Mean M over independent replica-pair batches, with its Monte Carlo standard error."""
    tab = Tables(L, theta, phi)
    init_st = T.initial_site_states(L, spectator_modes)
    bw = T.exact_branch_weights(L, spectator_modes, theta, phi)
    Ms, oor, tot, nus, nonfinite = [], 0, 0, [], 0
    for b in range(n_batches):
        M, pc, pd, sc, sd, nu = batch_M(L, init_st, W, seeds[b], tab, bw)
        nus.append(nu)
        if not np.isfinite(M):
            nonfinite += 1
            continue
        Ms.append(M)
        for v in list(pc) + list(pd):
            tot += 1
            if v < -0.05 or v > 1.05:
                oor += 1
    Ms = np.array(Ms)
    if len(Ms) == 0:
        return dict(M=float("nan"), M_se=float("nan"), M_batches=Ms,
                    raw_out_of_range_fraction=float("nan"),
                    mean_unique_configs=float(np.mean(nus)),
                    nonfinite_batches=nonfinite, n_batches=n_batches)
    se = float(Ms.std(ddof=1) / np.sqrt(len(Ms))) if len(Ms) > 1 else float("nan")
    return dict(M=float(Ms.mean()), M_se=se, M_batches=Ms,
                raw_out_of_range_fraction=oor / max(tot, 1),
                mean_unique_configs=float(np.mean(nus)),
                nonfinite_batches=nonfinite, n_batches=n_batches)
