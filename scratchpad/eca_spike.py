"""eca_spike.py — the Orio/Mediano/Rosas ECA noise sweep, measured in I_C^(3).

Pre-registered in scratchpad/ECA_SPIKE_PREREG.md, committed at 421ba25 BEFORE this ran.

Their claim (Chaos 33, 123103 (2023), arXiv:2305.13454): a BIPHASIC peak in O-information
and S-information as a function of bit-flip noise P_n, on elementary cellular automata over
a circular grid of 17 cells. Omega and Sigma are NOT pairwise-blind. This script re-runs the
sweep measuring the connected information of order 3 -- the maxent-over-all-pairs entropy
gap, `shareK` at k=3, identical to bench_detector.C3 -- and computes Omega and Sigma on the
SAME trajectories as an internal positive control, so that a null in our quantity can be
told apart from a broken reimplementation.

Scratchpad only. Model system, not nature.

Usage:
    python3 eca_spike.py --gate                # machinery gates G1-G4 only
    python3 eca_spike.py --screen              # all 256 rules, coarse
    python3 eca_spike.py --focus               # focus rules, full nulls + Omega
    python3 eca_spike.py --omega               # Omega/Sigma control at R=2^21
"""
import sys, os, json, time, argparse
import numpy as np
import cupy as cp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LN2 = float(np.log(2))
N_CELLS = 17

# =====================================================================================
# ECA ENGINE — bitwise, one uint32 per run, ring of N_CELLS
# =====================================================================================

_MOD = cp.RawModule(code=r'''
extern "C" __global__
void eca_step(const unsigned int* __restrict__ in, unsigned int* __restrict__ out,
              unsigned int lut, unsigned int mask, int n, int R)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= R) return;
    unsigned int x = in[i] & mask;
    /* bit j holds cell j; left neighbour of cell j is cell j-1 -> shift up with wrap */
    unsigned int l = ((x << 1) | (x >> (n - 1))) & mask;
    unsigned int r = ((x >> 1) | (x << (n - 1))) & mask;
    unsigned int y = 0u;
    #pragma unroll
    for (int k = 0; k < 8; ++k) {
        if ((lut >> k) & 1u) {
            unsigned int a = (k & 4) ? l : ~l;
            unsigned int b = (k & 2) ? x : ~x;
            unsigned int c = (k & 1) ? r : ~r;
            y |= (a & b & c);
        }
    }
    out[i] = y & mask;
}

extern "C" __global__
void scatter_flip(const long long* __restrict__ pos, unsigned int* __restrict__ state,
                  long long K, int n)
{
    long long i = (long long)blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= K) return;
    long long p = pos[i];
    unsigned int run = (unsigned int)(p / n);
    unsigned int bit = (unsigned int)(p % n);
    atomicXor(&state[run], 1u << bit);
}
''', options=('--std=c++11',))
_K_STEP = _MOD.get_function('eca_step')
_K_FLIP = _MOD.get_function('scatter_flip')

_MASK = np.uint32((1 << N_CELLS) - 1)
_BLOCK = 256


def eca_step_gpu(state, out, rule, n=N_CELLS):
    R = state.size
    grid = ((R + _BLOCK - 1) // _BLOCK,)
    _K_STEP(grid, (_BLOCK,), (state, out, cp.uint32(rule), cp.uint32((1 << n) - 1),
                              cp.int32(n), cp.int32(R)))
    return out


def apply_noise(state, k, rng, n=N_CELLS, nrng=None):
    """Flip each cell independently with probability p = 2**-k. Two exact code paths.

    k <= 3 (dense): AND of k uniform bit-words -> each bit set with probability exactly 2^-k.
    k >= 4 (sparse): draw K ~ Poisson(lambda), scatter K uniform positions and XOR. Each of
      the M = n*R positions then receives an independent Poisson(lambda/M) count, and flips
      iff that count is odd, so its flip probability is exactly (1-exp(-2*lambda/M))/2 = p
      when lambda = -M*ln(1-2p)/2. No approximation, and cells stay independent.
    """
    R = state.size
    if k <= 3:
        # low 17 bits of a uniform draw on [0, 2^30) are exactly uniform (2^30 is a
        # multiple of 2^17); cupy's Generator.integers cannot take high = 2^32.
        m = rng.integers(0, 1 << 30, size=R, dtype=cp.uint32)
        for _ in range(k - 1):
            m &= rng.integers(0, 1 << 30, size=R, dtype=cp.uint32)
        state ^= (m & cp.uint32((1 << n) - 1))
        return state
    p = 2.0 ** (-k)
    M = n * R
    lam = -M * float(np.log1p(-2.0 * p)) / 2.0
    K = int((nrng if nrng is not None else np.random.default_rng()).poisson(lam))
    if K > 0:
        pos = rng.integers(0, M, size=K, dtype=cp.int64)
        grid = ((K + _BLOCK - 1) // _BLOCK,)
        _K_FLIP(grid, (_BLOCK,), (pos, state, cp.int64(K), cp.int32(n)))
    return state


def run_eca(rule, R, n_steps, k_noise, seed, n=N_CELLS, n_record=3, snapshots=()):
    """Evolve R independent runs from uniform random ICs. k_noise=None => deterministic.

    Returns a list of `n_record` consecutive configurations starting at n_steps, plus a
    dict of {step: config} for any requested convergence snapshots.
    """
    rng = cp.random.default_rng(seed)
    nrng = np.random.default_rng(seed)
    state = rng.integers(0, 1 << n, size=R, dtype=cp.uint32)
    buf = cp.empty_like(state)
    snaps, want = {}, set(snapshots)
    for t in range(n_steps):
        eca_step_gpu(state, buf, rule, n)
        state, buf = buf, state
        if k_noise is not None:
            apply_noise(state, k_noise, rng, n, nrng)
        if (t + 1) in want:
            snaps[t + 1] = state.copy()
    out = [state.copy()]
    for _ in range(n_record - 1):
        eca_step_gpu(state, buf, rule, n)
        state, buf = buf, state
        if k_noise is not None:
            apply_noise(state, k_noise, rng, n, nrng)
        out.append(state.copy())
    return out, snaps


def eca_step_reference(bits, rule, n=N_CELLS):
    """Naive per-cell reference implementation. Used only by gate G3."""
    bits = np.asarray(bits, dtype=np.int64)
    R = bits.shape[0]
    out = np.empty_like(bits)
    for j in range(n):
        a = bits[:, (j - 1) % n]
        b = bits[:, j]
        c = bits[:, (j + 1) % n]
        idx = 4 * a + 2 * b + c
        out[:, j] = (rule >> idx) & 1
    return out


def unpack(state, n=N_CELLS):
    s = cp.asnumpy(state).astype(np.int64)
    return np.stack([(s >> j) & 1 for j in range(n)], axis=1)


# =====================================================================================
# SHARE MACHINERY — batched IPF, structurally identical to array_cap_experiment.shareK
# =====================================================================================

def Hb(p):
    """Row-wise Shannon entropy (nats) of a (B,2,2,2) or (B,8) batch."""
    q = p.reshape(p.shape[0], -1)
    return -cp.sum(cp.where(q > 1e-300, q * cp.log(cp.maximum(q, 1e-300)), 0.0), axis=1)


def pairwise_maxent_batch(p, iters=20000, tol=1e-13, check_every=25):
    """IPF from uniform to the maxent state carrying p's pair marginals at every pair.
    Batched over the leading axis; the per-element update is verbatim the structure of
    array_cap_experiment.pairwise_maxent_k / bench_detector.pairwise_maxent."""
    m12 = p.sum(axis=3); m13 = p.sum(axis=2); m23 = p.sum(axis=1)
    q = cp.full(p.shape, 0.125, dtype=cp.float64)
    err, it = float('inf'), 0
    for it in range(1, iters + 1):
        q12 = q.sum(axis=3)
        q = q * cp.where(q12 > 0, m12 / cp.where(q12 > 0, q12, 1.0), 0.0)[:, :, :, None]
        q13 = q.sum(axis=2)
        q = q * cp.where(q13 > 0, m13 / cp.where(q13 > 0, q13, 1.0), 0.0)[:, :, None, :]
        q23 = q.sum(axis=1)
        q = q * cp.where(q23 > 0, m23 / cp.where(q23 > 0, q23, 1.0), 0.0)[:, None, :, :]
        if it % check_every == 0 or it == iters:
            e = cp.max(cp.stack([cp.abs(q.sum(axis=3) - m12).max(),
                                 cp.abs(q.sum(axis=2) - m13).max(),
                                 cp.abs(q.sum(axis=1) - m23).max()]))
            err = float(e)
            if err < tol:
                break
    return q, err, it


def pairwise_maxent_exact(p, nbis=200):
    """EXACT pairwise maxent for three binary variables, by bisection. No iteration cap,
    no residual, and correct on distributions with structural zeros -- where IPF converges
    only sublinearly and hit its 20000-iteration cap at a marginal residual of 3e-6, which
    is above this experiment's floor and therefore not usable.

    A distribution over three binary variables is the maxent one carrying given pair
    marginals exactly when its three-way log odds ratio vanishes,
        q000 q011 q101 q110 = q001 q010 q100 q111,
    since that is precisely the condition for log q to contain no three-body term. Fixing
    the pair marginals leaves one free parameter t = q000, in which every cell is affine
    (even-parity cells +t, odd-parity cells -t). On the feasible interval -- where all eight
    cells are non-negative -- the left side increases in t, the right side decreases, and the
    two ends bracket a sign change, so bisection converges to the unique root. The endpoints
    of that interval are exactly the boundary cases, so the closure of the family is covered
    and no regularisation is needed anywhere.
    """
    m12 = p.sum(axis=3); m13 = p.sum(axis=2); m23 = p.sum(axis=1)
    A = m12[:, 0, 0]; B = m13[:, 0, 0]; C = m23[:, 0, 0]
    D = m12[:, 0, 1] - m13[:, 0, 0]
    E = m12[:, 1, 0] - m23[:, 0, 0]
    F = m13[:, 1, 0] - m23[:, 0, 0]
    G = m12[:, 1, 1] - m13[:, 1, 0] + m23[:, 0, 0]
    lo = cp.maximum(cp.maximum(cp.zeros_like(A), -D), cp.maximum(-E, -F))
    hi = cp.minimum(cp.minimum(A, B), cp.minimum(C, G))
    hi = cp.maximum(hi, lo)

    def phi(t):
        return (t * (D + t) * (E + t) * (F + t)
                - (A - t) * (B - t) * (C - t) * (G - t))

    a, b = lo.copy(), hi.copy()
    fa = phi(a)
    for _ in range(nbis):
        m = 0.5 * (a + b)
        fm = phi(m)
        same = (fm * fa) > 0
        a = cp.where(same, m, a); fa = cp.where(same, fm, fa)
        b = cp.where(same, b, m)
    t = 0.5 * (a + b)
    q = cp.empty_like(p)
    q[:, 0, 0, 0] = t;      q[:, 0, 0, 1] = A - t
    q[:, 0, 1, 0] = B - t;  q[:, 0, 1, 1] = D + t
    q[:, 1, 0, 0] = C - t;  q[:, 1, 0, 1] = E + t
    q[:, 1, 1, 0] = F + t;  q[:, 1, 1, 1] = G - t
    q = cp.maximum(q, 0.0)
    res = cp.max(cp.stack([cp.abs(q.sum(axis=3) - m12).max(),
                           cp.abs(q.sum(axis=2) - m13).max(),
                           cp.abs(q.sum(axis=1) - m23).max()]))
    return q, float(res), nbis


def shareK3_batch(p, exact=True, **kw):
    """I_C^(3) = S[pairwise maxent] - S[p], batched. Returns (share, q, residual, iters)."""
    q, err, it = (pairwise_maxent_exact(p) if exact else pairwise_maxent_batch(p, **kw))
    return Hb(q) - Hb(p), q, err, it


def hist_triples(idx, R):
    """idx: (B,R) int in 0..7 -> normalized (B,2,2,2) empirical distributions."""
    B = idx.shape[0]
    off = (cp.arange(B, dtype=cp.int64) * 8)[:, None]
    flat = cp.bincount((idx.astype(cp.int64) + off).ravel(), minlength=8 * B)
    return (flat.reshape(B, 2, 2, 2).astype(cp.float64) / float(R))


def surrogate_and_shuffle(q, R, n_surr, n_shuf, rng_np):
    """Matched pairwise-maxent multinomial surrogate (the estimator floor) and the
    independent-slot shuffle floor (multinomial from the product of the 1-marginals --
    the with-replacement analogue of permuting each slot across runs; validated against
    direct permutation in gate G5b)."""
    B = q.shape[0]
    qn = cp.asnumpy(q).reshape(B, 8)
    qn = np.clip(qn, 0, None); qn /= qn.sum(axis=1, keepdims=True)
    m1 = cp.asnumpy(q.sum(axis=(2, 3))); m2 = cp.asnumpy(q.sum(axis=(1, 3)))
    m3 = cp.asnumpy(q.sum(axis=(1, 2)))
    prod = (m1[:, :, None, None] * m2[:, None, :, None] * m3[:, None, None, :]).reshape(B, 8)
    prod = np.clip(prod, 0, None); prod /= prod.sum(axis=1, keepdims=True)

    def draw(pv, m):
        c = rng_np.multinomial(int(R), np.repeat(pv, m, axis=0))
        return cp.asarray(c.astype(np.float64).reshape(B * m, 2, 2, 2) / float(R))

    out = {}
    for tag, pv, m in (('null', qn, n_surr), ('shuf', prod, n_shuf)):
        if m == 0:
            out[tag] = (np.zeros(B), np.zeros(B)); continue
        s = cp.asnumpy(shareK3_batch(draw(pv, m))[0]).reshape(B, m)
        out[tag] = (s.mean(axis=1), s.std(axis=1, ddof=1))
    return out


# =====================================================================================
# READINGS — SPATIAL (gap shapes), TEMPORAL, CAUSAL
# =====================================================================================

def spatial_shapes(n=N_CELLS):
    """Partitions of n into three positive parts: the distinct gap-shapes of a triple on
    the ring. The ensemble is exactly translation-invariant, so one representative triple
    per shape carries the whole distribution and no rotations need to be pooled."""
    out = []
    for d1 in range(1, n - 1):
        for d2 in range(d1, n - d1):
            d3 = n - d1 - d2
            if d3 >= d2:
                out.append((d1, d2, d3))
    return out


SHAPES = spatial_shapes()


def reading_index(cfgs, n=N_CELLS):
    """cfgs = [s(T), s(T+1), s(T+2)] as uint32 arrays. Returns (tags, idx (B,R))."""
    c0, c1, c2 = cfgs
    tags, rows = [], []
    for (d1, d2, d3) in SHAPES:
        i, j, kk = 0, d1, d1 + d2
        rows.append(4 * ((c0 >> i) & 1) + 2 * ((c0 >> j) & 1) + ((c0 >> kk) & 1))
        tags.append(f'SPATIAL:{d1}-{d2}-{d3}')
    rows.append(4 * (c0 & 1) + 2 * (c1 & 1) + (c2 & 1))
    tags.append('TEMPORAL')
    # the three input-pairs of the neighbourhood {left, centre, right} against the output.
    # CAUSAL-LR is the rule-90 gate; LC and CR are the gates for rules 60 and 102, whose
    # parity mechanism uses a different pair. These read the rule's own truth table through
    # the stationary input distribution -- a MECHANISM reading, not emergent structure.
    out1 = (c1 >> 1) & 1
    for tag, u, v in (('CAUSAL-LR', c0 & 1, (c0 >> 2) & 1),
                      ('CAUSAL-LC', c0 & 1, (c0 >> 1) & 1),
                      ('CAUSAL-CR', (c0 >> 1) & 1, (c0 >> 2) & 1)):
        rows.append(4 * u + 2 * v + out1)
        tags.append(tag)
    return tags, cp.stack(rows).astype(cp.uint8)


def frozen_fraction(p):
    """Fraction of triples with a slot whose marginal is within 1e-6 of 0 or 1 -- the live
    degeneracy on a natively binary substrate, standing in for the (structurally zero)
    tied fraction."""
    m = cp.stack([p.sum(axis=(2, 3))[:, 1], p.sum(axis=(1, 3))[:, 1], p.sum(axis=(1, 2))[:, 1]],
                 axis=1)
    return cp.asnumpy(cp.minimum(m, 1.0 - m).min(axis=1))


# =====================================================================================
# OMEGA / SIGMA — the paper's quantities, on the same trajectories (internal control)
# =====================================================================================

def _H_from_counts(cnt, T):
    p = cnt[cnt > 0].astype(np.float64) / T
    Hpl = float(-(p * np.log2(p)).sum())
    return Hpl, Hpl + (len(p) - 1) / (2.0 * T * LN2)   # plugin, Miller-Madow (bits)


def omega_sigma(state, n=N_CELLS):
    """TC, DTC, Omega = TC - DTC, Sigma = TC + DTC over all n cells at one time, in bits.
    Definitions exactly as the paper's Methods. Plugin (their choice) and Miller-Madow."""
    T = state.size
    cnt = cp.asnumpy(cp.bincount(state.astype(cp.int64), minlength=1 << n))
    Hpl, Hmm = _H_from_counts(cnt, T)
    H1 = []
    for j in range(n):
        o = float(cp.asnumpy(cp.sum((state >> j) & 1))) / T
        H1.append(0.0 if o <= 0 or o >= 1 else float(-(o * np.log2(o) + (1 - o) * np.log2(1 - o))))
    Hm_pl, Hm_mm = [], []
    for j in range(n):
        low = state & cp.uint32((1 << j) - 1)
        high = (state >> (j + 1)) << j
        c = cp.asnumpy(cp.bincount((low | high).astype(cp.int64), minlength=1 << (n - 1)))
        a, b = _H_from_counts(c, T)
        Hm_pl.append(a); Hm_mm.append(b)
    out = {}
    for tag, Hj, Hm in (('plugin', Hpl, Hm_pl), ('mm', Hmm, Hm_mm)):
        TC = sum(H1) - Hj
        DTC = sum(Hm) - (n - 1) * Hj
        out[f'H_{tag}'] = Hj; out[f'TC_{tag}'] = TC; out[f'DTC_{tag}'] = DTC
        out[f'Omega_{tag}'] = TC - DTC; out[f'Sigma_{tag}'] = TC + DTC
    out['n_states_occupied'] = int((cnt > 0).sum())
    return out


# =====================================================================================
# GATES
# =====================================================================================

def selfconj_rules():
    out = []
    for r in range(256):
        if all(((r >> k) & 1) + ((r >> (7 - k)) & 1) == 1 for k in range(8)):
            out.append(r)
    return out


SELFCONJ = selfconj_rules()


def gates(verbose=True):
    ok = True
    print("=" * 78); print("GATES"); print("=" * 78)

    # ---- G1: the repository's share machinery ----
    import array_cap_experiment as ACE
    g1 = ACE.gate()
    print(f"G1 share machinery (array_cap_experiment.gate): {'PASS' if g1 else 'FAIL'}")
    ok &= g1

    # ---- G2: batched IPF == reference shareK ----
    rng = np.random.default_rng(20260725)
    P = rng.random((1000, 2, 2, 2)); P /= P.sum(axis=(1, 2, 3), keepdims=True)
    ref = np.array([ACE.shareK(P[i])[0] for i in range(P.shape[0])])
    bat = cp.asnumpy(shareK3_batch(cp.asarray(P))[0])
    d = float(np.abs(ref - bat).max())
    par = np.zeros((1, 2, 2, 2))
    for a in range(2):
        for b in range(2):
            par[0, a, b, a ^ b] = 0.25
    sp = float(cp.asnumpy(shareK3_batch(cp.asarray(par))[0])[0])
    g2 = d < 1e-12 and abs(sp - LN2) < 1e-12          # the pre-registered criterion
    print(f"G2 exact batched maxent vs reference shareK on 1000 random 2x2x2 states: "
          f"max diff {d:.3e}; exact parity -> {sp:.12f} (ln2 = {LN2:.12f}) "
          f"{'PASS' if g2 else 'FAIL'}")
    ok &= g2
    # The solver was switched from IPF to the exact bisection because IPF hit its 20000-
    # iteration cap at a residual of 3.1e-6 on the near-deterministic states this substrate
    # actually produces -- above this experiment's floor, hence unusable. Both are shown.
    P2 = rng.random((200, 2, 2, 2)) ** 12; P2 /= P2.sum(axis=(1, 2, 3), keepdims=True)
    P3 = np.concatenate([P2, np.array([[[[0.25, 0.], [0., 0.25]], [[0., 0.25], [0.25, 0.]]]]),
                         np.array([[[[0.5, 0.], [0., 0.]], [[0., 0.], [0., 0.5]]]])])
    ref3 = np.array([ACE.shareK(P3[i], tol=1e-15, iters=200000)[0] for i in range(len(P3))])
    ex3 = cp.asnumpy(shareK3_batch(cp.asarray(P3))[0])
    ipf3 = cp.asnumpy(shareK3_batch(cp.asarray(P3), exact=False, tol=1e-13)[0])
    r_ex = pairwise_maxent_exact(cp.asarray(P3))[1]
    r_ipf = pairwise_maxent_batch(cp.asarray(P3), tol=1e-13)[1]
    print(f"    near-deterministic + structural-zero states (n={len(P3)}): exact solver vs "
          f"reference max diff {float(np.abs(ref3 - ex3).max()):.3e} "
          f"(marginal residual {r_ex:.1e}); IPF vs reference {float(np.abs(ref3 - ipf3).max()):.3e} "
          f"(marginal residual {r_ipf:.1e})")

    # ---- G3: ECA engine == naive reference, ALL 256 rules, bit-identical ----
    R = 512
    rng_c = cp.random.default_rng(7)
    s0 = rng_c.integers(0, 1 << N_CELLS, size=R, dtype=cp.uint32)
    bits0 = unpack(s0)
    bad = []
    for rule in range(256):
        st = s0.copy(); buf = cp.empty_like(st); bits = bits0.copy()
        for _ in range(50):
            eca_step_gpu(st, buf, rule); st, buf = buf, st
            bits = eca_step_reference(bits, rule)
        if not np.array_equal(unpack(st), bits):
            bad.append(rule)
    g3 = not bad
    print(f"G3 ECA engine vs naive reference, all 256 rules x 50 steps x {R} runs, n=17 "
          f"ring: {'bit-identical, PASS' if g3 else f'FAIL on rules {bad[:10]}'}")
    ok &= g3

    # ---- G4: noise engine flip rate ----
    R = 1 << 20
    rows = []
    for k in range(1, 18):
        st = cp.zeros(R, dtype=cp.uint32)
        apply_noise(st, k, cp.random.default_rng(100 + k), N_CELLS,
                    np.random.default_rng(100 + k))
        flips = int(sum(int(cp.sum((st >> j) & 1)) for j in range(N_CELLS)))
        M = N_CELLS * R
        phat = flips / M
        p = 2.0 ** (-k)
        se = np.sqrt(max(p * (1 - p), 1e-12) / M)
        rows.append((k, p, phat, (phat - p) / se))
    g4 = all(abs(z) < 5 for _, _, _, z in rows)
    print(f"G4 noise engine, per-bit flip rate at all 17 levels (M = {N_CELLS * R:.3g} bits each):")
    for k, p, phat, z in rows:
        print(f"    k={k:2d}  p={p:.8g}  measured={phat:.8g}  z={z:+.2f}"
              + ("   [dense]" if k <= 3 else "   [sparse Poisson-XOR]"))
    print(f"G4 {'PASS' if g4 else 'FAIL'}")
    ok &= g4

    # ---- G5b: shuffle-floor construction == direct independent permutation ----
    rr = np.random.default_rng(3)
    a = rr.integers(0, 2, 200000); b = (a ^ (rr.random(200000) < 0.2)).astype(int)
    c = rr.integers(0, 2, 200000)
    idx = cp.asarray((4 * a + 2 * b + c)[None, :].astype(np.uint8))
    p = hist_triples(idx, 200000)
    perm = []
    for _ in range(10):
        pa, pb, pc = rr.permutation(a), rr.permutation(b), rr.permutation(c)
        ii = cp.asarray((4 * pa + 2 * pb + pc)[None, :].astype(np.uint8))
        perm.append(float(cp.asnumpy(shareK3_batch(hist_triples(ii, 200000))[0])[0]))
    sh = surrogate_and_shuffle(p, 200000, 0, 10, np.random.default_rng(4))['shuf']
    g5 = abs(np.mean(perm) - sh[0][0]) < 4 * (np.std(perm, ddof=1) / np.sqrt(10) + sh[1][0] / np.sqrt(10))
    print(f"G5b shuffle floor: direct permutation {np.mean(perm):.3e} +/- {np.std(perm, ddof=1):.1e}"
          f" vs product-of-marginals multinomial {sh[0][0]:.3e} +/- {sh[1][0]:.1e} "
          f"{'PASS' if g5 else 'FAIL'}")
    ok &= g5

    print(f"\nGATE VERDICT: {'PASS' if ok else 'FAIL'}")
    print(f"complementation-symmetric rules ({len(SELFCONJ)}): {SELFCONJ}")
    print(f"spatial gap-shapes on the n=17 ring: {len(SHAPES)}")
    return ok


# =====================================================================================
# SWEEP
# =====================================================================================

NOISE_K = list(range(17, 0, -1))            # P_n = 2^-k, k = 17..1
P_GRID = [0.0] + [2.0 ** -k for k in NOISE_K]
K_GRID = [None] + NOISE_K

FOCUS_RULES = [0, 8, 18, 19, 22, 23, 28, 30, 45, 46, 54, 60, 90, 97, 102, 105, 110,
               150, 178, 204, 232]


def sweep(rules, R, n_steps, seeds, n_surr, n_shuf, do_omega, out_path, tag):
    """One rule at a time. Every histogram for the rule's whole (P_n x seed) grid is
    accumulated first, then the IPF runs on the entire batch in a single call: the IPF is
    kernel-launch bound, so batching the grid is the difference between hours and minutes.
    The measurement itself is unchanged."""
    rng_np = np.random.default_rng(20260725)
    rows = []
    t0 = time.time()
    NS = len(seeds)
    for ri, rule in enumerate(rules):
        keys, hs, omrows = [], [], []
        for gi, (p_n, k) in enumerate(zip(P_GRID, K_GRID)):
            cbs = []
            for s in seeds:
                c, _ = run_eca(rule, R, n_steps, k, seed=1000 * s + 7 * rule + gi)
                cbs.append(c)
            for si in range(NS):
                tags, idx = reading_index(cbs[si])
                keys.append((gi, si)); hs.append(hist_triples(idx, R))
            if NS >= 3:                      # cross-run refuter: slot j from seed j
                ix = [reading_index(c)[1] for c in cbs[:3]]
                keys.append((gi, 'ref'))
                hs.append(hist_triples(4 * ((ix[0] >> 2) & 1) + 2 * ((ix[1] >> 1) & 1)
                                       + (ix[2] & 1), R))
            if do_omega:
                om = omega_sigma(cbs[0][0])
                om.update(rule=rule, P_n=p_n, reading='OMEGA', R=R, n_steps=n_steps)
                omrows.append(om)
            del cbs

        NT = hs[0].shape[0]
        P = cp.concatenate(hs, axis=0)
        share, q, err, it = shareK3_batch(P)                       # ONE IPF call
        fl = surrogate_and_shuffle(q, R, n_surr, n_shuf, rng_np)   # two more
        share = cp.asnumpy(share).reshape(len(keys), NT)
        nullm = fl['null'][0].reshape(len(keys), NT)
        nullsd = fl['null'][1].reshape(len(keys), NT)
        shufm = fl['shuf'][0].reshape(len(keys), NT)
        froz = frozen_fraction(P).reshape(len(keys), NT)
        pos = {kk: i for i, kk in enumerate(keys)}

        for gi, p_n in enumerate(P_GRID):
            si_rows = [pos[(gi, si)] for si in range(NS)]
            sh = share[si_rows]; nu = nullm[si_rows]; nsd = nullsd[si_rows]
            sf = shufm[si_rows]; fz = froz[si_rows]
            exc = sh - nu
            for t in range(NT):
                r = dict(rule=rule, P_n=p_n, reading=tags[t], R=R, n_steps=n_steps,
                         n_seeds=NS, share=float(sh[:, t].mean()),
                         null_mean=float(nu[:, t].mean()), null_sd=float(nsd[:, t].mean()),
                         excess=float(exc[:, t].mean()),
                         excess_sem=(float(exc[:, t].std(ddof=1) / np.sqrt(NS))
                                     if NS > 1 else float('nan')),
                         excess_per_seed=[float(v) for v in exc[:, t]],
                         shuffle_mean=float(sf[:, t].mean()),
                         min_slot_marg=float(fz[:, t].min()), ipf_err=float(err))
                if (gi, 'ref') in pos:
                    j = pos[(gi, 'ref')]
                    r['refuter_excess'] = float(share[j, t] - nullm[j, t])
                    r['refuter_z'] = (float(r['refuter_excess'] / nullsd[j, t])
                                      if nullsd[j, t] > 1e-15 else 0.0)
                rows.append(r)
        rows += omrows
        el = time.time() - t0
        print(f"[{tag}] rule {rule:3d} ({ri+1}/{len(rules)})  {el:.0f}s elapsed, "
              f"eta {el / (ri + 1) * (len(rules) - ri - 1):.0f}s  "
              f"(IPF {it} iters, residual {err:.1e})", flush=True)
        with open(out_path, 'w') as f:
            json.dump(rows, f, default=float)
    print(f"[{tag}] wrote {out_path} ({len(rows)} rows, {time.time() - t0:.0f}s)")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gate', action='store_true')
    ap.add_argument('--screen', action='store_true')
    ap.add_argument('--focus', action='store_true')
    ap.add_argument('--omega', action='store_true')
    ap.add_argument('--converge', action='store_true')
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))

    if a.gate:
        return 0 if gates() else 1

    if a.converge:
        # convergence check: does the measurement move between 200, 400 and 800 steps?
        rows = []
        for rule in (19, 28, 97, 110, 90):
            for k in (None, 10, 7):
                c, snaps = run_eca(rule, 1 << 18, 800, k, seed=5, snapshots=(200, 400))
                for st, cfg in list(snaps.items()) + [(800, c[0])]:
                    tags, idx = reading_index([cfg, cfg, cfg])
                    p = hist_triples(idx, 1 << 18)
                    s = cp.asnumpy(shareK3_batch(p)[0])
                    om = omega_sigma(cfg)
                    rows.append(dict(rule=rule, k=k, step=st,
                                     spatial_max=float(s[:len(SHAPES)].max()),
                                     H=om['H_plugin'], Omega=om['Omega_plugin']))
                    print(rows[-1], flush=True)
        with open(os.path.join(here, 'eca_converge.json'), 'w') as f:
            json.dump(rows, f, default=float)
        return 0

    if not gates():
        print("GATES FAILED — refusing to sweep."); return 1

    if a.screen:
        sweep(list(range(256)), 1 << 16, 400, [0], 16, 4, False,
              os.path.join(here, 'eca_screen.json'), 'screen')
    if a.focus:
        sweep(FOCUS_RULES, 1 << 20, 800, [0, 1, 2], 60, 10, True,
              os.path.join(here, 'eca_focus.json'), 'focus')
    if a.omega:
        sweep([8, 19, 22, 28, 30, 45, 46, 60, 97], 1 << 21, 800, [0], 0, 0, True,
              os.path.join(here, 'eca_omega.json'), 'omega')
    return 0


if __name__ == '__main__':
    sys.exit(main())
