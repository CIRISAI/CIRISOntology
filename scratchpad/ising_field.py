"""ising_field.py — the pairwise-blind order-3 share I_C^(3) over the (T,h) plane
of the 2D Ising model.

Pre-registered in scratchpad/ISING_FIELD_PREREG.md, committed BEFORE this file existed.

WHY.  Core/SignSymmetry.lean proves a zero-field Ising model has whole-only share
EXACTLY ZERO at every temperature, criticality included.  It also says, in the other
direction, where to look: break the global sign symmetry.  This maps what is there when
you do.

ARM A (primary) — EXACT enumeration on periodic lattices small enough to sum over all
2^N configurations.  No sampling, no estimator, no bias.  The whole (T,h) plane comes
almost free because the Boltzmann weight depends on a configuration ONLY through its
bond energy and its magnetisation: histogram (n_broken_bonds, popcount, triple_pattern)
once, and every grid point is a contraction of that histogram.

ARM B — Metropolis MC (checkerboard, on GPU) at larger L, with the full null apparatus.
Cluster algorithms do not apply in a field.  Arm B is gated on reproducing Arm A's exact
answer on the small lattices; if it cannot, it is not reported (kill K5).

Usage:
    python3 ising_field.py --gate
    python3 ising_field.py --exact
    python3 ising_field.py --mc
    python3 ising_field.py --all
"""
import sys, os, json, time, argparse, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LN2 = float(np.log(2.0))
TC = 2.0 / math.log(1.0 + math.sqrt(2.0))
DECORRELATE = False   # set by --fss2; see mc_budget

# =====================================================================================
# THE INSTRUMENT.  I_C^(3) on three binary slots, exactly.
# =====================================================================================
#
# The k=3 pair envelope is ONE-DIMENSIONAL.  Adding t*sigma(s) to the eight cell
# probabilities, sigma(s) = s1*s2*s3 = +-1, preserves normalisation and all three pair
# marginals; nothing else does (8 cells, 7 independent constraints).  So
#
#     pairEnvelope(p) = { p + t*sigma : feasible t },
#
# and the maxent member is the unique root of  g(t) = sum_s sigma(s) log(p_s + t sigma_s),
# because dH/dt = -g(t).  g is strictly increasing (g' = sum 1/(p_s + t sigma_s) > 0) and
# runs from -inf to +inf across the feasible interval, so bisection is bulletproof.
#
# Bisection precision is a non-issue here: H is being MAXIMISED, so dH/dt = 0 at t*, and
# an error d in t costs O(d^2) in the entropy.
#
# Cell index convention: bit b_i in {0,1}, s_i = 1-2b_i, index = 4*b1 + 2*b2 + b3.
# sigma = +1 on even popcount, -1 on odd.

_POP = np.array([bin(i).count('1') for i in range(8)])
SIGMA = np.where(_POP % 2 == 0, 1.0, -1.0)          # s1*s2*s3 on the eight cells
_TINY = 1e-300


def _xlogx(x):
    x = np.asarray(x, dtype=np.float64)
    return np.where(x > 0.0, x * np.log(np.where(x > 0.0, x, 1.0)), 0.0)


def H8(p):
    """Entropy (nats) of a batch of 8-cell states, p shape (..., 8)."""
    return -_xlogx(p).sum(axis=-1)


def maxent_t(p, iters=200):
    """Root of g(t)=0 by vectorised bisection.  p shape (..., 8), rows sum to 1."""
    p = np.asarray(p, dtype=np.float64)
    even = p[..., SIGMA > 0]
    odd = p[..., SIGMA < 0]
    lo = -even.min(axis=-1)          # p_s + t > 0 for sigma=+1
    hi = odd.min(axis=-1)            # p_s - t > 0 for sigma=-1
    degenerate = (hi - lo) <= 0.0    # a zero cell on each parity: p is the only member
    lo = np.where(degenerate, 0.0, lo)
    hi = np.where(degenerate, 0.0, hi)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        q = p + mid[..., None] * SIGMA
        g = (SIGMA * np.log(np.maximum(q, _TINY))).sum(axis=-1)
        lo = np.where(g < 0.0, mid, lo)
        hi = np.where(g < 0.0, hi, mid)
    return 0.5 * (lo + hi)


def share3(p):
    """I_C^(3) = S[maxent carrying all pair marginals] - S[p].  p shape (..., 8)."""
    p = np.asarray(p, dtype=np.float64)
    t = maxent_t(p)
    q = np.maximum(p + t[..., None] * SIGMA, 0.0)
    return H8(q) - H8(p), q, t


def share_mpmath(p, dps=60, iters=400):
    """Arbitrary-precision reference for I_C^(3): the same one-dimensional root, solved
    at `dps` digits.  Independent of both the float64 solver and of IPF, so it can
    adjudicate between them.  Slow; used only in the gate."""
    import mpmath as mp
    mp.mp.dps = dps
    P = [mp.mpf(float(x)) for x in np.asarray(p).ravel()]
    S = [mp.mpf(int(s)) for s in SIGMA]
    lo = -min(P[i] for i in range(8) if S[i] > 0)
    hi = min(P[i] for i in range(8) if S[i] < 0)
    if hi - lo <= 0:
        return mp.mpf(0)
    g = lambda t: sum(S[i] * mp.log(P[i] + t * S[i]) for i in range(8))
    a, b = lo * mp.mpf('0.99999999'), hi * mp.mpf('0.99999999')
    for _ in range(iters):
        m = (a + b) / 2
        if g(m) < 0:
            a = m
        else:
            b = m
    t = (a + b) / 2
    ent = lambda q: -sum(x * mp.log(x) for x in q if x > 0)
    return ent([P[i] + t * S[i] for i in range(8)]) - ent(P)


def marginals3(p):
    """Singles H(X_i) and pairs H(X_jk) of a batch of 8-cell states."""
    p = np.asarray(p, dtype=np.float64)
    r = p.reshape(p.shape[:-1] + (2, 2, 2))
    H1 = [H8_gen(r.sum(axis=(-2, -1))), H8_gen(r.sum(axis=(-3, -1))), H8_gen(r.sum(axis=(-3, -2)))]
    H2 = [H8_gen(r.sum(axis=-1).reshape(p.shape[:-1] + (4,))),      # (1,2)
          H8_gen(r.sum(axis=-2).reshape(p.shape[:-1] + (4,))),      # (1,3)
          H8_gen(r.sum(axis=-3).reshape(p.shape[:-1] + (4,)))]      # (2,3)
    return H1, H2


def H8_gen(p):
    return -_xlogx(p).sum(axis=-1)


def all_measures(p):
    """Everything reported per state: the pairwise-blind quantity and the ordinary ones."""
    p = np.asarray(p, dtype=np.float64)
    ic3, q, t = share3(p)
    Hp = H8(p)
    H1, H2 = marginals3(p)
    sH1 = H1[0] + H1[1] + H1[2]
    sH2 = H2[0] + H2[1] + H2[2]
    TCv = sH1 - Hp                       # multi-information / total correlation
    Ov = Hp + sH1 - sH2                  # O-information, n=3
    DTC = sH2 - 2.0 * Hp                 # dual total correlation (TC - O)
    return dict(ic3=ic3, tc=TCv, ic2=TCv - ic3, omega=Ov, dtc=DTC,
                H=Hp, t_star=t, cf=ic3 / LN2)


# =====================================================================================
# GEOMETRY CLASSES.  Kept separate, never pooled.
# =====================================================================================

GEOMS = {
    # three of the four neighbours of a common site: the class in which integrating out
    # that shared neighbour DIRECTLY generates an effective three-body coupling
    'star':    ((1, 0), (0, 1), (-1, 0)),
    'Lcorner': ((0, 0), (1, 0), (0, 1)),      # tightest triple: two NN bonds + a diagonal
    'plaq':    ((0, 0), (1, 0), (1, 1)),      # three corners of one plaquette
    'colin1':  ((0, 0), (1, 0), (2, 0)),      # collinear, NN spacing
    'colin2':  ((0, 0), (2, 0), (4, 0)),      # collinear, spacing 2
    'far':     None,                          # filled per lattice: maximally separated
}


def geom_for(Lx, Ly):
    """Realise the geometry classes on an Lx x Ly periodic lattice, dropping any class
    whose sites collide under the periodicity (e.g. colin2 on a lattice of width 4)."""
    out = {}
    for name, disp in GEOMS.items():
        if name == 'far':
            disp = ((0, 0), (Lx // 2, 0), (0, Ly // 2))
        sites = [((x % Lx), (y % Ly)) for (x, y) in disp]
        if len(set(sites)) < 3:
            continue                        # degenerate on this lattice; skipped, not fudged
        out[name] = tuple(sites)
    return out


# =====================================================================================
# ARM A — EXACT ENUMERATION
# =====================================================================================

def bonds_of(Lx, Ly):
    idx = lambda x, y: (y % Ly) * Lx + (x % Lx)
    b = []
    for y in range(Ly):
        for x in range(Lx):
            b.append((idx(x, y), idx(x + 1, y)))
            b.append((idx(x, y), idx(x, y + 1)))
    return b


def exact_histogram(Lx, Ly, xp, chunk=1 << 22, verbose=True):
    """One pass over all 2^N configurations.

    Returns counts[g] of shape (nbonds+1, N+1, 8):
      counts[g][B, P, v] = # configurations with B broken bonds, popcount P, and the
      triple of geometry g in pattern v.

    The Boltzmann weight of a configuration depends on it ONLY through (B, P):
        E = -J*(nbonds - 2B) - h*(N - 2P)
    so this histogram is a sufficient statistic for the entire (T,h) plane.
    """
    N = Lx * Ly
    bonds = bonds_of(Lx, Ly)
    nb = len(bonds)
    geoms = geom_for(Lx, Ly)
    gnames = list(geoms)
    sites = {g: [ (y * Lx + x) for (x, y) in geoms[g] ] for g in gnames}
    nP = N + 1
    counts = {g: xp.zeros((nb + 1) * nP * 8, dtype=xp.int64) for g in gnames}
    total = 1 << N
    t0 = time.time()
    for lo in range(0, total, chunk):
        hi = min(lo + chunk, total)
        c = xp.arange(lo, hi, dtype=xp.int64)
        B = xp.zeros(hi - lo, dtype=xp.int32)
        for (i, j) in bonds:
            B += (((c >> i) ^ (c >> j)) & 1).astype(xp.int32)
        P = xp.zeros(hi - lo, dtype=xp.int32)
        for i in range(N):
            P += ((c >> i) & 1).astype(xp.int32)
        base = (B.astype(xp.int64) * nP + P.astype(xp.int64)) * 8
        for g in gnames:
            s0, s1, s2 = sites[g]
            v = (((c >> s0) & 1) << 2) | (((c >> s1) & 1) << 1) | ((c >> s2) & 1)
            counts[g] += xp.bincount(base + v, minlength=(nb + 1) * nP * 8)
        del c, B, P, base
    if verbose:
        print(f"    [{Lx}x{Ly}: {total} configs enumerated in {time.time()-t0:.1f}s, "
              f"geoms {gnames}]")
    return {g: xp.asnumpy(counts[g]).reshape(nb + 1, nP, 8) if hasattr(xp, 'asnumpy')
            else counts[g].reshape(nb + 1, nP, 8) for g in gnames}, nb, N


def exact_grid_fast(counts, nb, N, Ts, hs):
    """Contract the histogram onto the whole (T,h) grid at once.  counts (nb+1, N+1, 8).
    Log-weights with a per-grid-point max subtraction, so low T does not overflow."""
    nbp, nP = counts.shape[0], counts.shape[1]
    Bv = np.arange(nbp, dtype=np.float64)
    Pv = np.arange(nP, dtype=np.float64)
    Ebond = -(nb - 2.0 * Bv)[:, None]
    Mag = (N - 2.0 * Pv)[None, :]
    cflat = counts.reshape(-1, 8).astype(np.float64)
    occ = cflat.sum(axis=1) > 0
    cflat = cflat[occ]
    Eb = np.broadcast_to(Ebond, (nbp, nP)).reshape(-1)[occ]
    Mg = np.broadcast_to(Mag, (nbp, nP)).reshape(-1)[occ]
    logc = np.log(cflat.sum(axis=1))
    frac = cflat / cflat.sum(axis=1, keepdims=True)
    T = np.asarray(Ts, dtype=np.float64)[:, None, None]
    h = np.asarray(hs, dtype=np.float64)[None, :, None]
    lw = (-(Eb[None, None, :] - h * Mg[None, None, :]) / T) + logc[None, None, :]
    lw -= lw.max(axis=2, keepdims=True)
    w = np.exp(lw)
    p = np.einsum('abk,kv->abv', w, frac)
    return p / p.sum(axis=2, keepdims=True)


def exact_thermo(counts_any, nb, N, Ts, hs):
    """Exact magnetisation and bond energy per site on the grid, same histogram."""
    nbp, nP = counts_any.shape[0], counts_any.shape[1]
    tot = counts_any.sum(axis=2).astype(np.float64)
    Bv = np.arange(nbp, dtype=np.float64)[:, None]
    Pv = np.arange(nP, dtype=np.float64)[None, :]
    Ebond = -(nb - 2.0 * Bv) + 0.0 * Pv
    Mag = (N - 2.0 * Pv) + 0.0 * Bv
    occ = tot > 0
    Eb, Mg = Ebond[occ], Mag[occ]
    logc = np.log(tot[occ])
    T = np.asarray(Ts, dtype=np.float64)[:, None, None]
    h = np.asarray(hs, dtype=np.float64)[None, :, None]
    lw = (-(Eb[None, None, :] - h * Mg[None, None, :]) / T) + logc[None, None, :]
    lw -= lw.max(axis=2, keepdims=True)
    w = np.exp(lw)
    w /= w.sum(axis=2, keepdims=True)
    m = (w * (Mg / N)[None, None, :]).sum(axis=2)
    e = (w * (Eb / N)[None, None, :]).sum(axis=2)
    return m, e


# =====================================================================================
# ARM B — METROPOLIS MONTE CARLO (checkerboard, GPU)
# =====================================================================================

def mc_run(Lx, Ly, T, h, R, n_burn, n_samp, gap, xp, seed=0, want_mag=True):
    """R independent replicas, checkerboard Metropolis in a field.

    Returns bits (n_samp, R, Ly, Lx) uint8 with 1 == spin down, and the per-replica
    magnetisation trace over the sampling phase (for tau_int)."""
    rs = xp.random.RandomState(seed) if hasattr(xp.random, 'RandomState') else np.random.RandomState(seed)
    s = (rs.randint(0, 2, size=(R, Ly, Lx)) * 2 - 1).astype(xp.int8)
    yy, xx = xp.meshgrid(xp.arange(Ly), xp.arange(Lx), indexing='ij')
    color = ((xx + yy) % 2).astype(xp.int8)
    masks = [(color == 0), (color == 1)]

    def sweep():
        for mk in masks:
            nb = (xp.roll(s, 1, axis=2) + xp.roll(s, -1, axis=2)
                  + xp.roll(s, 1, axis=1) + xp.roll(s, -1, axis=1)).astype(xp.float32)
            dE = 2.0 * s.astype(xp.float32) * (nb + xp.float32(h))
            acc = (dE <= 0) | (rs.rand(R, Ly, Lx).astype(xp.float32) < xp.exp(-dE / xp.float32(T)))
            flip = acc & mk[None, :, :]
            s[...] = xp.where(flip, -s, s)

    for _ in range(n_burn):
        sweep()
    out = xp.empty((n_samp, R, Ly, Lx), dtype=xp.int8)
    mags = xp.empty((n_samp, R), dtype=xp.float32)
    for t in range(n_samp):
        for _ in range(gap):
            sweep()
        out[t] = s
        if want_mag:
            mags[t] = s.astype(xp.float32).mean(axis=(1, 2))
    bits = ((1 - out) // 2).astype(xp.uint8)          # spin +1 -> bit 0, spin -1 -> bit 1
    return bits, mags


def tau_int(mag, cutoff=6):
    """Integrated autocorrelation time (in units of `gap` sweeps) with automatic
    windowing, averaged over replicas."""
    m = np.asarray(mag, dtype=np.float64)
    n, R = m.shape
    taus = []
    for r in range(R):
        x = m[:, r] - m[:, r].mean()
        v = (x * x).mean()
        if v <= 0:
            taus.append(0.5)
            continue
        tau = 0.5
        for lag in range(1, min(n // 4, 500)):
            c = (x[:-lag] * x[lag:]).mean() / v
            if c <= 0:
                break
            tau += c
            if lag >= cutoff * tau:
                break
        taus.append(tau)
    return float(np.mean(taus))


def triple_counts(bits, sites, Lx, Ly, xp):
    """Per-block 8-cell counts, pooling all lattice translates.
    bits (n_samp, R, Ly, Lx); block == replica (independent chain).
    Returns counts (R, 8) int64 summed over samples and translates."""
    (x0, y0), (x1, y1), (x2, y2) = sites
    b0 = xp.roll(xp.roll(bits, -y0, axis=2), -x0, axis=3)
    b1 = xp.roll(xp.roll(bits, -y1, axis=2), -x1, axis=3)
    b2 = xp.roll(xp.roll(bits, -y2, axis=2), -x2, axis=3)
    v = (b0 << 2) | (b1 << 1) | b2                      # uint8, values 0..7
    del b0, b1, b2
    R = v.shape[1]
    out = np.empty((R, 8), dtype=np.int64)
    step = max(1, min(R, (1 << 24) // max(v.shape[0] * v.shape[2] * v.shape[3], 1)))
    for lo in range(0, R, step):                        # chunked: keeps int32 temporaries small
        hi = min(lo + step, R)
        vc = v[:, lo:hi].transpose(1, 0, 2, 3).reshape(hi - lo, -1).astype(xp.int32)
        off = (xp.arange(hi - lo, dtype=xp.int32) * 8)[:, None]
        c = xp.bincount((vc + off).reshape(-1), minlength=(hi - lo) * 8).reshape(hi - lo, 8)
        out[lo:hi] = xp.asnumpy(c) if hasattr(xp, 'asnumpy') else c
        del vc, off, c
    return out


def analyse_block_counts(cblocks, rng, n_surr=200):
    """Full pre-registered readout from per-block 8-cell counts (R, 8).

    N_eff, not nominal N: pooling L^2 translates does NOT give L^2 independent samples.
    The plugin bias of this nested-family statistic goes as 1/(2 N_eff), so using nominal
    N would UNDERSTATE the floor.  F is measured from the across-block variance of the
    cell frequencies against multinomial."""
    cb = np.asarray(cblocks, dtype=np.float64)
    R = cb.shape[0]
    nper = cb.sum(axis=1)
    N = float(nper.sum())
    tot = cb.sum(axis=0)
    p = tot / N
    m = all_measures(p)

    # variance-inflation factor F, per cell, across independent blocks
    pb = cb / np.maximum(nper[:, None], 1)
    var_blocks = pb.var(axis=0, ddof=1) / R                      # var of the block mean
    var_multi = np.maximum(p * (1 - p), 1e-300) / N
    Fc = var_blocks / var_multi
    F_max = float(np.nanmax(Fc)); F_mean = float(np.nanmean(Fc))
    F = max(F_max, 1.0)
    N_eff = N / F

    # matched pairwise-maxent multinomial surrogate at N_eff  = the estimator-bias floor
    _, q, _ = share3(p)
    qf = np.clip(q, 0, None); qf = qf / qf.sum()
    n_draw = max(int(round(N_eff)), 8)
    draws = rng.multinomial(n_draw, qf, size=n_surr).astype(np.float64)
    draws /= draws.sum(axis=1, keepdims=True)
    s_sur = share3(draws)[0]
    floor_mu, floor_sd = float(s_sur.mean()), float(s_sur.std(ddof=1))

    # the same floor at NOMINAL N, reported alongside so the size of the correction shows
    d2 = rng.multinomial(max(int(round(N)), 8), qf, size=max(n_surr // 4, 20)).astype(np.float64)
    d2 /= d2.sum(axis=1, keepdims=True)
    floor_naive = float(share3(d2)[0].mean())

    # configuration-level bootstrap error bar
    nboot = 200
    bi = rng.integers(0, R, size=(nboot, R))
    bs = cb[bi].sum(axis=1)
    bs /= bs.sum(axis=1, keepdims=True)
    boot_sd = float(share3(bs)[0].std(ddof=1))

    # shuffle floor: destroy all cross-site structure, keep the single-site marginals
    r3 = p.reshape(2, 2, 2)
    p1 = [r3.sum(axis=(1, 2)), r3.sum(axis=(0, 2)), r3.sum(axis=(0, 1))]
    prod = np.einsum('a,b,c->abc', p1[0], p1[1], p1[2]).reshape(8)
    dsh = rng.multinomial(n_draw, prod, size=max(n_surr // 4, 20)).astype(np.float64)
    dsh /= dsh.sum(axis=1, keepdims=True)
    shuf_mu = float(share3(dsh)[0].mean())

    excess = float(m['ic3']) - floor_mu
    sd = max(floor_sd, boot_sd)
    z = excess / sd if sd > 1e-300 else float('nan')

    min_cell = float(p.min())
    trustworthy = bool(min_cell * N_eff >= 20.0 and N_eff >= 1e3)
    return dict(
        share_raw=float(m['ic3']), excess=excess, z=float(z),
        floor_neff=floor_mu, floor_sd=floor_sd, floor_naive=floor_naive,
        boot_sd=boot_sd, shuffle_floor=shuf_mu,
        N=N, N_eff=float(N_eff), F_max=F_max, F_mean=F_mean, R_blocks=int(R),
        min_cell=min_cell, trustworthy=trustworthy,
        cf_excess=excess / LN2, cf_raw=float(m['ic3']) / LN2,
        tc=float(m['tc']), omega=float(m['omega']), ic2=float(m['ic2']),
        H=float(m['H']), tie_fraction=0.0,
    )


# =====================================================================================
# GATE — eight tests, all must pass before any grid runs
# =====================================================================================

def gate(xp):
    print("=" * 80)
    print("GATE — instrument + enumeration.  All eight required (prereg section 7).")
    print("=" * 80)
    ok = True
    rng = np.random.default_rng(20260725)

    # ---- 1: fast solver vs the repository's validated IPF machinery
    try:
        import array_cap_experiment as ACE
        P = rng.random((2000, 8)); P /= P.sum(axis=1, keepdims=True)
        mine = share3(P)[0]
        theirs = np.array([ACE.shareK(P[i].reshape(2, 2, 2))[0] for i in range(2000)])
        d1 = float(np.abs(mine - theirs).max())
        print(f"(1) fast solver vs array_cap_experiment.shareK (IPF), 2000 random states:"
              f"  max|diff| = {d1:.3e}   (< 1e-12 required)")
        ok &= d1 < 1e-12
    except Exception as e:
        print(f"(1) IPF cross-check UNAVAILABLE: {e}")
        ok = False

    # ---- 2: boundary-adjacent states.  AMENDED AFTER FAILING — see the results memo.
    # As first written this test used IPF as the reference and required agreement to
    # 1e-9.  It failed at 5.6e-5.  The prereg's own row for this test already names the
    # tie-break ("the fast solver is the reference where IPF fails to converge"), so the
    # amendment is to make that operational with an INDEPENDENT 60-digit reference
    # rather than to relax a threshold.  IPF's error against the same reference is
    # reported as a diagnostic, not as a pass condition.
    Pb = rng.random((2000, 8)) ** 6
    for i in range(2000):
        Pb[i, rng.integers(0, 8)] *= 1e-7
    Pb /= Pb.sum(axis=1, keepdims=True)
    mine = share3(Pb)[0]
    idx = list(range(0, 2000, 40))
    ref = np.array([float(share_mpmath(Pb[i])) for i in idx])
    ipf = np.array([ACE.shareK(Pb[i].reshape(2, 2, 2))[0] for i in idx])
    d2 = float(np.abs(mine[idx] - ref).max())
    d2i = float(np.abs(ipf - ref).max())
    print(f"(2) boundary-adjacent states (min cell ~1e-8), vs an independent 60-digit"
          f" reference, {len(idx)} states:")
    print(f"      fast solver: max|diff| = {d2:.3e}   (< 1e-9 required)")
    print(f"      IPF        : max|diff| = {d2i:.3e}   [diagnostic: IPF OVERSTATES the"
          f" share on near-deterministic states]")
    ok &= d2 < 1e-9

    # ---- 3: exact three-coin parity saturates the machine-checked cap
    par = np.zeros(8)
    for a in range(2):
        for b in range(2):
            par[(a << 2) | (b << 1) | (a ^ b)] = 0.25
    mp = all_measures(par)
    print(f"(3) exact parity: I_C^(3) = {float(mp['ic3']):.15f}   ln2 = {LN2:.15f}   "
          f"CF = {float(mp['cf']):.6f}   TC = {float(mp['tc']):.6f}   "
          f"O-info = {float(mp['omega']):+.6f}   I_C^(2) = {float(mp['ic2']):.2e}")
    ok &= abs(float(mp['ic3']) - LN2) < 1e-12 and abs(float(mp['ic2'])) < 1e-12

    # ---- 4: exact independent
    ind = np.full(8, 1 / 8)
    s_ind = float(share3(ind)[0])
    print(f"(4) exact independent: I_C^(3) = {s_ind:.3e}   (< 1e-14 required)")
    ok &= abs(s_ind) < 1e-14

    # ---- 5: explicit three-body coupling.  AMENDED AFTER FAILING — see the memo.
    # As first written this asserted the SPIKE_SURVEY pairing (K = 0.9 -> 0.247 nats)
    # and failed at 0.284838.  Adjudicated in CLOSED FORM, which needs no solver at all:
    # for p ~ exp(K*s1*s2*s3) every pair marginal is exactly 1/4, so the pairwise maxent
    # IS the uniform state and I_C^(3) = 3ln2 - H(p) exactly.  The closed form gives
    # 0.284838 at K = 0.9; 0.247 corresponds to K = 0.8146.  The survey's LABEL is off by
    # a coupling value; the instrument is right.  Gate now tests against the closed form.
    s3 = np.array([[1 - 2 * ((i >> b) & 1) for b in (2, 1, 0)] for i in range(8)])
    sg = s3[:, 0] * s3[:, 1] * s3[:, 2]
    worst5 = 0.0
    for K in (0.5, 0.8146, 0.9, 1.2):
        pk = np.exp(K * sg); pk /= pk.sum()
        c = np.cosh(K); pp = np.exp(K) / (8 * c); pm = np.exp(-K) / (8 * c)
        closed = 3 * LN2 - (-4 * (pp * np.log(pp) + pm * np.log(pm)))
        worst5 = max(worst5, abs(float(share3(pk)[0]) - closed))
    pk = np.exp(0.9 * sg); pk /= pk.sum()
    print(f"(5) explicit 3-body coupling vs CLOSED FORM at K = 0.5/0.8146/0.9/1.2:"
          f"  max|diff| = {worst5:.3e}   (< 1e-12 required)")
    print(f"      K=0.9 gives {float(share3(pk)[0]):.6f} nats, NOT the 0.247 that"
          f" SPIKE_SURVEY.md pairs with K=0.9 (0.247 is K=0.8146)")
    ok &= worst5 < 1e-12

    # ---- 6: the lemma.  2000 random SIGN-SYMMETRIC states must read zero.
    A = rng.random((2000, 4))
    Ps = np.concatenate([A, A[:, ::-1]], axis=1)      # p(s) = p(-s): cell i <-> cell 7-i
    Ps /= Ps.sum(axis=1, keepdims=True)
    d6 = float(np.abs(share3(Ps)[0]).max())
    print(f"(6) sign-symmetry lemma, 2000 random Z2-symmetric states:"
          f"  max|I_C^(3)| = {d6:.3e}   (< 1e-12 required)")
    ok &= d6 < 1e-12

    # ---- 8 (run before 7, which needs it): enumeration vs brute-force energy
    Lx, Ly = 4, 4
    counts, nb, N = exact_histogram(Lx, Ly, np, verbose=False)
    g0 = list(counts)[0]
    tot = counts[g0].sum()
    bf_ok = (tot == (1 << N))
    bonds = bonds_of(Lx, Ly)
    chk = True
    for c in rng.integers(0, 1 << N, 200):
        c = int(c)
        s = np.array([1 - 2 * ((c >> i) & 1) for i in range(N)])
        Eb = -sum(s[i] * s[j] for (i, j) in bonds)
        B = sum(((c >> i) ^ (c >> j)) & 1 for (i, j) in bonds)
        chk &= (Eb == -(nb - 2 * B))
    print(f"(8) enumeration bookkeeping: total configs {tot} == 2^{N} -> {bf_ok};"
          f"  bond energy vs brute force on 200 random configs -> {chk}")
    ok &= bf_ok and chk

    # ---- 7: THE VALIDITY CONDITION.  h = 0, every T, every geometry -> exactly zero.
    Ts = grid_T()
    worst = 0.0
    for g in counts:
        p = exact_grid_fast(counts[g], nb, N, Ts, [0.0])
        worst = max(worst, float(np.abs(share3(p.reshape(-1, 8))[0]).max()))
    print(f"(7) *** VALIDITY *** exact 4x4 Ising, h=0, {len(Ts)} temperatures x "
          f"{len(counts)} geometries:  max|I_C^(3)| = {worst:.3e}   (< 1e-12 required)")
    ok &= worst < 1e-12

    # ---- 9: THE CHECK THAT ACTUALLY BEARS ON THIS EXPERIMENT.  Added after test 2
    # exposed a solver-precision question: how accurate is the instrument on the states
    # this experiment REALLY encounters, including the near-deterministic corners of the
    # (T,h) grid?  Adversarial synthetic states are not the operating regime; these are.
    Ts9, hs9 = grid_T(), grid_h()
    w9 = w9i = 0.0
    for g in counts:
        Pg = exact_grid_fast(counts[g], nb, N, Ts9, hs9).reshape(-1, 8)
        mine9 = share3(Pg)[0]
        order = np.argsort(Pg.min(axis=1))
        pick = sorted(set(list(order[:20]) + list(np.linspace(0, len(Pg) - 1, 15).astype(int))))
        for i in pick:
            r9 = float(share_mpmath(Pg[i]))
            w9 = max(w9, abs(r9 - float(mine9[i])))
            w9i = max(w9i, abs(r9 - ACE.shareK(Pg[i].reshape(2, 2, 2))[0]))
    print(f"(9) precision on the REAL 4x4 Ising grid (worst-conditioned states incl. the "
          f"near-deterministic corners), vs 60-digit reference:")
    print(f"      fast solver: max|diff| = {w9:.3e}   (< 1e-12 required)")
    print(f"      IPF        : max|diff| = {w9i:.3e}   [diagnostic]")
    ok &= w9 < 1e-12

    print(f"\nGATE VERDICT: {'PASS' if ok else 'FAIL'}")
    return ok


# =====================================================================================
# GRIDS
# =====================================================================================

def grid_T():
    a = np.linspace(0.40, 1.60, 9, endpoint=False)
    b = np.linspace(1.60, 3.20, 29, endpoint=False)     # dense around T_c
    c = np.linspace(3.20, 5.00, 10)
    return np.unique(np.concatenate([a, b, c, [TC]]))


def grid_h(include_zero=True):
    h = np.geomspace(1e-3, 4.0, 32)
    return np.concatenate([[0.0], h]) if include_zero else h


# =====================================================================================
# ARM A DRIVER
# =====================================================================================

def run_exact(xp, lattices, outpath):
    Ts, hs = grid_T(), grid_h()
    print(f"\nARM A — exact enumeration.  {len(Ts)} temperatures x {len(hs)} fields "
          f"(h=0 included exactly), lattices {lattices}")
    res = {'T': Ts.tolist(), 'h': hs.tolist(), 'Tc': TC, 'lattices': {}}
    for (Lx, Ly) in lattices:
        key = f"{Lx}x{Ly}"
        print(f"  {key} (N={Lx*Ly}, 2^{Lx*Ly} = {1<<(Lx*Ly)} configs)")
        use = xp if Lx * Ly >= 22 else np
        counts, nb, N = exact_histogram(Lx, Ly, use)
        counts = {g: (np.asarray(c) if not isinstance(c, np.ndarray) else c)
                  for g, c in counts.items()}
        m_grid, _ = exact_thermo(next(iter(counts.values())), nb, N, Ts, hs)
        entry = {'N': N, 'nbonds': nb, 'm_abs': np.abs(m_grid).tolist(), 'geoms': {}}
        for g in counts:
            p = exact_grid_fast(counts[g], nb, N, Ts, hs)
            mm = all_measures(p.reshape(-1, 8))
            sh = np.asarray(mm['ic3']).reshape(len(Ts), len(hs))
            entry['geoms'][g] = {
                'ic3': sh.tolist(),
                'tc': np.asarray(mm['tc']).reshape(len(Ts), len(hs)).tolist(),
                'ic2': np.asarray(mm['ic2']).reshape(len(Ts), len(hs)).tolist(),
                'omega': np.asarray(mm['omega']).reshape(len(Ts), len(hs)).tolist(),
                'sites': geom_for(Lx, Ly)[g],
            }
            h0 = float(np.abs(sh[:, 0]).max())
            i = int(np.argmax(sh)); a, b = divmod(i, len(hs))
            print(f"    {g:<8} h=0 column max|I_C3| = {h0:.2e}   "
                  f"peak = {sh[a,b]:.6e} nats (CF {sh[a,b]/LN2*100:.3f}%) at "
                  f"T = {Ts[a]:.3f} (T/Tc = {Ts[a]/TC:.3f}), h = {hs[b]:.4f}, "
                  f"|m| = {abs(m_grid[a,b]):.3f}")
            if h0 > 1e-12:
                print(f"    *** K1 FIRED on {key}/{g}: h=0 column is not zero. RUN VOID.")
        res['lattices'][key] = entry
    with open(outpath, 'w') as f:
        json.dump(res, f)
    print(f"  wrote {outpath}")
    return res


# =====================================================================================
# ARM B DRIVER
# =====================================================================================

def run_mc(xp, specs, outpath, scale=1.0, seed=20260725):
    print(f"\nARM B — Metropolis (checkerboard, in a field), {len(specs)} grid points")
    rows = []
    rng = np.random.default_rng(seed)
    for (Lx, Ly, T, h, tag) in specs:
        t0 = time.time()
        R, n_samp, gap, n_burn = mc_budget(Lx, Ly, scale)
        geoms = geom_for(Lx, Ly)
        bits, mags = mc_run(Lx, Ly, T, h, R, n_burn, n_samp, gap, xp, seed=seed)
        tau = tau_int(xp.asnumpy(mags) if hasattr(xp, 'asnumpy') else np.asarray(mags))
        mabs = float(abs((1.0 - 2.0 * (xp.asnumpy(bits) if hasattr(xp, 'asnumpy') else np.asarray(bits))).mean()))
        for g, sites in geoms.items():
            cb = triple_counts(bits, sites, Lx, Ly, xp)
            r = analyse_block_counts(cb, rng)
            r.update(Lx=Lx, Ly=Ly, T=T, h=h, geom=g, tag=tag, tau_int=tau,
                     m_abs=mabs, sweeps_total=n_burn + n_samp * gap,
                     undersampled=bool(n_samp * gap < 200 * tau * gap))
            rows.append(r)
            print(f"  L={Lx}x{Ly} T={T:.3f} h={h:.4f} {g:<8} "
                  f"raw={r['share_raw']:.3e} floor={r['floor_neff']:.3e} "
                  f"excess={r['excess']:+.3e} z={r['z']:+8.2f} "
                  f"N={r['N']:.2e} N_eff={r['N_eff']:.2e} F={r['F_max']:.1f} "
                  f"{'OK' if r['trustworthy'] else 'UNTRUSTWORTHY'}")
        del bits, mags
        if hasattr(xp, 'get_default_memory_pool'):
            xp.get_default_memory_pool().free_all_blocks()
        print(f"    [{time.time()-t0:.1f}s, R={R} n_samp={n_samp} gap={gap}, "
              f"tau_int = {tau:.2f} x gap, |m| = {mabs:.3f}]")
        with open(outpath, 'w') as f:          # incremental: long runs stay analysable
            json.dump(rows, f, default=float)
    with open(outpath, 'w') as f:
        json.dump(rows, f, default=float)
    print(f"  wrote {outpath}")
    return rows


def run_sep(xp, L, T, h, outpath, scale=1.0, seed=20260725):
    """SEPARATION SCAN — I_C^(3) of a collinear triple as a function of its spacing r,
    evaluated on ONE set of samples so the geometries are directly comparable.

    This tests the post-hoc explanation offered for `far` beating `star`: if the order-3
    structure comes from three spins reading a shared global mode, it should PERSIST or
    GROW out to r ~ L/2; if it is the local integrate-out mechanism, it should DECAY once
    r exceeds a few lattice spacings."""
    print(f"\nSEPARATION SCAN — L={L}, T={T:.4f} (T/Tc={T/TC:.3f}), h={h:.4f}")
    R, n_samp, gap, n_burn = mc_budget(L, L, scale)
    rng = np.random.default_rng(seed + 7)
    bits, mags = mc_run(L, L, T, h, R, n_burn, n_samp, gap, xp, seed=seed)
    tau = tau_int(xp.asnumpy(mags) if hasattr(xp, 'asnumpy') else np.asarray(mags))
    rows = []
    rs = [r for r in (1, 2, 3, 4, 6, 8, 12, 16, 24, 32) if 2 * r <= L]
    for r in rs:
        sites = ((0, 0), (r % L, 0), ((2 * r) % L, 0))
        if len({sites[0], sites[1], sites[2]}) < 3:
            continue
        rr = analyse_block_counts(triple_counts(bits, sites, L, L, xp), rng)
        rr.update(Lx=L, Ly=L, T=T, h=h, geom=f'colin-r{r}', r=r, tag='sep', tau_int=tau)
        rows.append(rr)
        print(f"  r={r:<3} excess={rr['excess']:+.4e} z={rr['z']:+8.2f} "
              f"N_eff={rr['N_eff']:.2e} F={rr['F_max']:.0f} "
              f"{'' if rr['trustworthy'] else 'UNTRUSTWORTHY'}")
    del bits, mags
    if hasattr(xp, 'get_default_memory_pool'):
        xp.get_default_memory_pool().free_all_blocks()
    with open(outpath, 'w') as f:
        json.dump(rows, f, default=float)
    print(f"  wrote {outpath}  [tau_int = {tau:.2f} x gap]")
    return rows


def run_refuter(xp, specs, outpath, scale=1.0, seed=20260725):
    """Cross-configuration refuter: slot j drawn from an independent run at the same
    (T,h) with a different seed.  True share is zero by construction; |z| > 5 proves the
    null mis-specified and voids the grid point."""
    print("\nARM B REFUTER — cross-run triples, true share zero by construction")
    rows = []
    rng = np.random.default_rng(seed + 1)
    for (Lx, Ly, T, h, tag) in specs:
        R, n_samp, gap, n_burn = mc_budget(Lx, Ly, scale)
        runs = [mc_run(Lx, Ly, T, h, R, n_burn, n_samp, gap, xp, seed=seed + 100 * k)[0]
                for k in range(3)]
        b = xp.stack([runs[0][:, :, 0, 0], runs[1][:, :, 0, 0], runs[2][:, :, 0, 0]], axis=0)
        v = (b[0].astype(xp.int32) << 2) | (b[1].astype(xp.int32) << 1) | b[2].astype(xp.int32)
        v = v.transpose(1, 0).reshape(R, -1)
        off = (xp.arange(R, dtype=xp.int32) * 8)[:, None]
        c = xp.bincount((v + off).reshape(-1), minlength=R * 8).reshape(R, 8)
        cb = xp.asnumpy(c) if hasattr(xp, 'asnumpy') else c
        r = analyse_block_counts(cb, rng)
        r.update(Lx=Lx, Ly=Ly, T=T, h=h, geom='CROSS-RUN', tag=tag)
        rows.append(r)
        flag = 'MIS-SPECIFIED' if abs(r['z']) > 5 else 'clean'
        print(f"  L={Lx}x{Ly} T={T:.3f} h={h:.4f} cross-run: excess={r['excess']:+.3e} "
              f"z={r['z']:+.2f}  -> null {flag}")
        del runs, b, v, c
        if hasattr(xp, 'get_default_memory_pool'):
            xp.get_default_memory_pool().free_all_blocks()
    with open(outpath, 'w') as f:
        json.dump(rows, f, default=float)
    return rows


# =====================================================================================

def mc_budget(Lx, Ly, scale=1.0):
    """Replicas / samples / gap per lattice.  Sized so N_eff can resolve a ~1e-3 nat
    effect: sd(I) ~ sqrt(2 I / N_eff), so N_eff ~ 1e5-1e6 is the target.  Small lattices
    buy independence with many replicas, large ones with many sites.

    DECORRELATE (used by --fss2 only) scales the sampling gap with L.  The first
    finite-size pass showed the peak migrating to small field, into the near-critical
    region where Metropolis critical slowing down (dynamic exponent z ~ 2.17, and no
    cluster algorithm is available in a field) drove the measured variance-inflation F
    above 1e3 and collapsed N_eff below the pre-registered trustworthiness floor — i.e.
    the honest filter was excluding precisely the points of interest.  A longer gap buys
    that independence back.  This is a choice about ESTIMATOR VALIDITY, not about the
    value of the estimate; it is disclosed in the results memo."""
    N = Lx * Ly
    if N <= 24:
        R, n_samp, gap, burn = 4096, 700, 10, 400
    elif N <= 256:
        R, n_samp, gap, burn = 1024, 500, 10, 600
    elif N <= 1024:
        R, n_samp, gap, burn = 256, 500, 10, 1000
    else:
        R, n_samp, gap, burn = 96, 500, 10, 2000
    if DECORRELATE:
        gap = max(10, 3 * max(Lx, Ly))
        n_samp = 200
        burn = max(burn, 6 * gap)
        R = max(R, 256)          # blocks are replicas; keep enough for F and the bootstrap
    return R, max(int(n_samp * scale), 40), gap, burn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gate', action='store_true')
    ap.add_argument('--exact', action='store_true')
    ap.add_argument('--mc', action='store_true')
    ap.add_argument('--mcmap', action='store_true')
    ap.add_argument('--fss2', action='store_true')
    ap.add_argument('--sep', action='store_true')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--cpu', action='store_true')
    ap.add_argument('--scale', type=float, default=1.0)
    args = ap.parse_args()

    xp = np
    if not args.cpu:
        try:
            import cupy
            xp = cupy
            print(f"DEVICE: {cupy.cuda.runtime.getDeviceProperties(0)['name'].decode()}")
        except Exception as e:
            print(f"cupy unavailable ({e}); CPU")

    if not gate(xp):
        print("GATE FAILED — refusing to run the grid.")
        return 1
    if args.gate and not (args.exact or args.mc or args.all):
        return 0

    here = os.path.dirname(os.path.abspath(__file__))
    ex = None
    if args.exact or args.all:
        ex = run_exact(xp, [(4, 4), (6, 4), (5, 5)], os.path.join(here, 'ising_exact.json'))

    if args.mc or args.mcmap or args.sep or args.fss2 or args.all:
        if ex is None:
            with open(os.path.join(here, 'ising_exact.json')) as f:
                ex = json.load(f)
        Ts, hs = np.array(ex['T']), np.array(ex['h'])
        sh = np.array(ex['lattices']['4x4']['geoms']['star']['ic3'])
        a, b = np.unravel_index(int(np.argmax(sh)), sh.shape)
        Tpk, hpk = float(Ts[a]), float(hs[b])
        print(f"\nexact 4x4 star peak at T={Tpk:.4f} (T/Tc={Tpk/TC:.4f}), h={hpk:.4f} "
              f"-> Monte Carlo slices anchored there")

    if args.mc or args.all:
        # CROSS-ARM (kill K5): the same lattices Arm A solved exactly.
        specs = []
        for (Lx, Ly) in [(4, 4), (6, 4)]:
            for (T, h) in [(Tpk, hpk), (Tpk, 0.0), (TC, 0.3), (1.60, 0.6), (3.00, 0.3)]:
                specs.append((Lx, Ly, float(T), float(h), 'crossarm'))
        run_mc(xp, specs, os.path.join(here, 'ising_mc_crossarm.json'), args.scale)
        run_refuter(xp, [(4, 4, Tpk, hpk, 'crossarm'), (6, 4, Tpk, hpk, 'crossarm')],
                    os.path.join(here, 'ising_mc_refuter.json'), args.scale)

    if args.mcmap or args.all:
        # FINITE-SIZE: does the peak height grow with L, and does its locus move?  (b1)/(b2)
        specs = []
        for L in (8, 16, 32, 64):
            for T in np.linspace(max(0.6, Tpk - 1.2), Tpk + 1.6, 8):
                specs.append((L, L, float(T), hpk, 'fss-Tscan'))
            for h in np.geomspace(max(hpk / 16, 1e-3), min(hpk * 8, 4.0), 8):
                specs.append((L, L, Tpk, float(h), 'fss-hscan'))
            specs.append((L, L, 0.0 + TC, 0.0, 'fss-h0'))       # the lemma's control at size
        run_mc(xp, specs, os.path.join(here, 'ising_mc_fss.json'), args.scale)

    if args.fss2:
        globals()['DECORRELATE'] = True
        # TARGETED finite-size run.  The first FSS pass anchored its h-scan at the 4x4
        # peak and so did NOT bracket the peak for large L: the peak field shrinks with
        # L.  Grid placement here uses the standard finite-size scaling of the ordering
        # field at the 2D Ising critical point, h*(L) ~ L^(-15/8) (magnetic scaling
        # dimension y_h = 15/8), anchored on the measured 4x4 peak.  Disclosed as a
        # physics-motivated grid placement, not a fit.
        specs = []
        for L in (8, 16, 32, 64):
            hstar = hpk * (L / 4.0) ** (-15.0 / 8.0)
            for h in np.geomspace(hstar / 6, hstar * 6, 7):
                for T in (TC, 0.92 * TC):
                    specs.append((L, L, float(T), float(h), f'fss2-L{L}'))
        run_mc(xp, specs, os.path.join(here, 'ising_mc_fss2.json'), args.scale)

    if args.sep:
        globals()['DECORRELATE'] = True
        out = []
        for L in (16, 32):
            hstar = hpk * (L / 4.0) ** (-15.0 / 8.0)
            out += run_sep(xp, L, TC, float(hstar),
                           os.path.join(here, f'ising_mc_sep_L{L}.json'), args.scale)
        with open(os.path.join(here, 'ising_mc_sep.json'), 'w') as f:
            json.dump(out, f, default=float)
    return 0


if __name__ == '__main__':
    sys.exit(main())
