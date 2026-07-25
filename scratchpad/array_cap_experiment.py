"""array_cap_experiment.py — CIRISArray cap-compliance + ceiling fraction.

Pre-registered in scratchpad/ARRAY_CAP_PREREG.md (committed BEFORE this ran).

JOB 1  cap compliance: drive the REAL CIRISArray GPU kernel, read k channels, push them
       through the SAME share pipeline used for the Bell claim, and confirm it never
       reports above the cap proved in CIRISOntology/Core/ShareK.lean.
JOB 2  ceiling fraction: share / proved cap at k=3 and k=5 across the coupling dial.

NOT a claim of order-3 / whole-only structure in the array. See the prereg.

Substrate: /home/emoore/CIRISArray/src/runtime.py, Ossicle.KERNEL_CODE, on the RTX 4090.
Boundary discriminator: the native clip fminf(fmaxf(x,0.001f),0.999f) vs a reflecting
fold, compiled from the SAME kernel string with only the clamp expressions replaced. Both
variants carry a clamp-event counter that does not enter the state update.

Usage:
    python3 array_cap_experiment.py --gate          # machinery self-test only
    python3 array_cap_experiment.py --run           # full sweep (gate runs first)
"""
import sys, os, json, time, argparse
import numpy as np

sys.path.insert(0, '/home/emoore/CIRISArray')
sys.path.insert(0, '/home/emoore/CIRISArray/src')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LN2 = float(np.log(2))

# =====================================================================================
# k-SLOT SHARE MACHINERY  (shareK of Core/ShareK.lean; at k=3 this IS bench_detector.C3)
# =====================================================================================

def H(p):
    p = np.asarray(p, dtype=float).ravel()
    p = p[p > 1e-15]
    return float(-np.sum(p * np.log(p)))

def pair_marg(p, i, j):
    """(i,j) pair marginal of a k-slot state; call with i < j. = ShareK.pairMarg."""
    axes = tuple(a for a in range(p.ndim) if a not in (i, j))
    return p.sum(axis=axes)

def all_pairs(k):
    return [(i, j) for i in range(k) for j in range(i + 1, k)]

def pairwise_maxent_k(p, iters=20000, tol=1e-13):
    """IPF from uniform to the maxent state carrying p's pair marginals at every pair.
    The I-projection of uniform, hence sSup of the pair envelope. Generalizes
    bench_detector.pairwise_maxent (k=3) verbatim in structure."""
    k = p.ndim
    prs = all_pairs(k)
    marg = {ij: pair_marg(p, *ij) for ij in prs}
    q = np.full(p.shape, 1.0 / p.size)
    err = np.inf
    for it in range(iters):
        for (i, j) in prs:
            qij = pair_marg(q, i, j)
            ratio = np.where(qij > 0, marg[(i, j)] / np.where(qij > 0, qij, 1.0), 0.0)
            shape = [1] * k
            shape[i] = 2
            shape[j] = 2
            q = q * ratio.reshape(shape)
        err = max(float(np.abs(pair_marg(q, i, j) - marg[(i, j)]).max()) for (i, j) in prs)
        if err < tol:
            break
    return q, err, it + 1

def shareK(p, iters=20000, tol=1e-13):
    """shareK p = sSup(pairEnvelopeK p) - entropy p."""
    q, err, nit = pairwise_maxent_k(p, iters=iters, tol=tol)
    return H(q) - H(p), H(q), err, nit

def caps_and_checks(p):
    """Everything Core/ShareK.lean bounds, evaluated on the empirical state p."""
    k = p.ndim
    Hp = H(p)
    prs = all_pairs(k)
    Hpair = {ij: H(pair_marg(p, *ij)) for ij in prs}
    sh, Hmax, err, nit = shareK(p)
    # shareK_le_log_sub_pair holds for EVERY pair -> tightest is the min over pairs,
    # i.e. k*log2 - max_pair H(pair).
    cap_robust = k * LN2 - max(Hpair.values())
    cap_headline = (k - 2) * LN2
    # pair-uniformity: hypothesis of shareK_le_of_pair_uniform, audited not assumed
    dev_linf = max(float(np.abs(pair_marg(p, *ij) - 0.25).max()) for ij in prs)
    ent_deficit = 2 * LN2 - min(Hpair.values())
    return dict(
        k=k, share=sh, H_whole=Hp, H_maxent=Hmax, ipf_err=err, ipf_iters=nit,
        cap_robust=cap_robust, cap_headline=cap_headline,
        H_pair_max=max(Hpair.values()), H_pair_min=min(Hpair.values()),
        pair_dev_linf=dev_linf, pair_ent_deficit=ent_deficit,
        # engine checks, one per Lean step
        chk_entropy_map_le=bool(all(Hpair[ij] <= Hp + 1e-9 for ij in prs)),
        chk_maxent_le_logcard=bool(Hmax <= k * LN2 + 1e-9),
        chk_cap_robust=bool(sh <= cap_robust + 1e-9),
        chk_cap_headline=bool(sh <= cap_headline + 1e-9),
        margin_robust=cap_robust - sh, margin_headline=cap_headline - sh,
    )

def emp_dist(bits):
    """bits (T,k) of 0/1 -> normalized p of shape (2,)*k, plus T."""
    bits = np.ascontiguousarray(bits.astype(np.int64))
    T, k = bits.shape
    idx = np.zeros(T, dtype=np.int64)
    for j in range(k):
        idx = idx * 2 + bits[:, j]
    cnt = np.bincount(idx, minlength=2 ** k).astype(float)
    return cnt.reshape((2,) * k) / cnt.sum(), int(T)

def surrogate_null(p, T, n_surr=60, rng=None):
    """Matched pairwise-maxent multinomial surrogate = the estimator bias floor."""
    if rng is None:
        rng = np.random.default_rng()
    q, _, _ = pairwise_maxent_k(p)
    flat = np.clip(q.ravel(), 0, None)
    flat = flat / flat.sum()
    out = np.empty(n_surr)
    for i in range(n_surr):
        c = rng.multinomial(int(T), flat).reshape(p.shape).astype(float)
        out[i] = shareK(c / c.sum())[0]
    return float(out.mean()), float(out.std(ddof=1))

def shuffle_floor(bits, n_shuf=10, rng=None):
    """Independently permute each channel -> all cross-channel structure destroyed."""
    if rng is None:
        rng = np.random.default_rng()
    vals = []
    for _ in range(n_shuf):
        b = np.column_stack([rng.permutation(bits[:, j]) for j in range(bits.shape[1])])
        vals.append(shareK(emp_dist(b)[0])[0])
    return float(np.mean(vals)), float(np.std(vals, ddof=1))

def binarize_median(x):
    med = float(np.median(x))
    return (x > med).astype(np.int8), float(np.mean(x == med)), med

def analyze(chans, tag, n_surr=60, n_shuf=10, rng=None, do_null=True):
    """chans: list of k float arrays of equal length. Full pre-registered readout."""
    if rng is None:
        rng = np.random.default_rng(0)
    bits, ties, meds = [], [], []
    for x in chans:
        b, tie, med = binarize_median(np.asarray(x, dtype=np.float64))
        bits.append(b); ties.append(tie); meds.append(med)
    bits = np.column_stack(bits)
    p, T = emp_dist(bits)
    r = caps_and_checks(p)
    r.update(tag=tag, T=T, tie_max=max(ties), tie_all=ties)
    if do_null:
        mu, sd = surrogate_null(p, T, n_surr=n_surr, rng=rng)
        r['null_mean'], r['null_sd'] = mu, sd
        r['excess'] = r['share'] - mu
        r['z'] = (r['share'] - mu) / sd if sd > 1e-15 else float('nan')
        smu, ssd = shuffle_floor(bits, n_shuf=n_shuf, rng=rng)
        r['shuffle_mean'], r['shuffle_sd'] = smu, ssd
    else:
        r['null_mean'] = r['null_sd'] = r['excess'] = r['z'] = float('nan')
        r['shuffle_mean'] = r['shuffle_sd'] = float('nan')
    # ceiling fractions (bias-corrected primary, raw alongside)
    r['CF_headline'] = r['excess'] / r['cap_headline'] if r['cap_headline'] > 0 else float('nan')
    r['CF_headline_raw'] = r['share'] / r['cap_headline'] if r['cap_headline'] > 0 else float('nan')
    exact_max = LN2 if r['k'] == 3 else (2 * LN2 if r['k'] == 5 else float('nan'))
    r['cap_exact'] = exact_max
    r['CF_exact'] = r['excess'] / exact_max
    r['CF_exact_raw'] = r['share'] / exact_max
    return r

# =====================================================================================
# GATE — machinery self-test. FAIL => stop, no hardware.
# =====================================================================================

def gate():
    print("=" * 78)
    print("GATE — k-slot share machinery (must PASS before any hardware)")
    print("=" * 78)
    ok = True

    # (1) k=3 exact parity -> log2, saturating its cap exactly
    par = np.zeros((2, 2, 2))
    for a in range(2):
        for b in range(2):
            par[a, b, a ^ b] = 0.25
    s_par = shareK(par)[0]
    c_par = caps_and_checks(par)
    print(f"(1) k=3 exact parity      share = {s_par:.12f}  target ln2 = {LN2:.12f}  "
          f"cap_headline = {c_par['cap_headline']:.12f}  saturates = {abs(s_par - c_par['cap_headline']) < 1e-9}")
    ok &= abs(s_par - LN2) < 1e-9 and c_par['chk_cap_robust'] and c_par['chk_cap_headline']

    # (2) k=3 exact independent
    ind3 = np.full((2, 2, 2), 1 / 8)
    s_i3 = shareK(ind3)[0]
    print(f"(2) k=3 exact independent share = {s_i3:.3e}  target 0")
    ok &= abs(s_i3) < 1e-12

    # (3) k=5 exact pair-uniform code state (x1,x2,x3,x1^x2,x1^x2^x3): the known exact
    #     classical maximum 2*ln2 (CLASSICAL_MAX_K5.md), below the proved cap 3*ln2
    code = np.zeros((2,) * 5)
    for x1 in range(2):
        for x2 in range(2):
            for x3 in range(2):
                code[x1, x2, x3, x1 ^ x2, x1 ^ x2 ^ x3] = 1 / 8
    c_code = caps_and_checks(code)
    print(f"(3) k=5 exact code state  share = {c_code['share']:.12f}  "
          f"target 2ln2 = {2*LN2:.12f}  exact-max match = {abs(c_code['share'] - 2*LN2) < 1e-9}")
    print(f"    proved cap 3ln2 = {c_code['cap_headline']:.6f}  compliant = {c_code['chk_cap_headline']}  "
          f"pair_dev_Linf = {c_code['pair_dev_linf']:.2e}  ipf_err = {c_code['ipf_err']:.2e}")
    ok &= abs(c_code['share'] - 2 * LN2) < 1e-9 and c_code['chk_cap_headline'] and c_code['chk_cap_robust']

    # (4) k=5 exact independent
    ind5 = np.full((2,) * 5, 1 / 32)
    s_i5 = shareK(ind5)[0]
    print(f"(4) k=5 exact independent share = {s_i5:.3e}  target 0")
    ok &= abs(s_i5) < 1e-12

    # (5) IPF residual
    errs = [caps_and_checks(x)['ipf_err'] for x in (par, ind3, code, ind5)]
    print(f"(5) IPF residuals max = {max(errs):.3e}  (< 1e-12 required)")
    ok &= max(errs) < 1e-12

    # (6) SAME PIPELINE: k=3 shareK must equal bench_detector.C3 to 1e-12
    try:
        import bench_detector as BD
        rng = np.random.default_rng(11)
        d = 0.0
        for _ in range(20):
            q = rng.random((2, 2, 2)); q /= q.sum()
            d = max(d, abs(shareK(q)[0] - BD.C3(q)))
        print(f"(6) shareK(k=3) vs bench_detector.C3 on 20 random states: max diff = {d:.3e}")
        ok &= d < 1e-12
    except Exception as e:  # pragma: no cover
        print(f"(6) bench_detector cross-check UNAVAILABLE: {e}")
        ok = False

    # (7) sampled, full pipeline at hardware scale
    rng = np.random.default_rng(20260725)
    T = 200000
    a = rng.integers(0, 2, T); b = rng.integers(0, 2, T)
    rp = analyze([a.astype(float) - 0.5 + 1e-9 * rng.random(T),
                  b.astype(float) - 0.5 + 1e-9 * rng.random(T),
                  (a ^ b).astype(float) - 0.5 + 1e-9 * rng.random(T)],
                 'gate-parity-sampled', n_surr=30, n_shuf=5, rng=rng)
    print(f"(7) sampled k=3 parity T={T}: share={rp['share']:.4f} z={rp['z']:.1f} "
          f"CF_headline={rp['CF_headline']:.4f} cap_ok={rp['chk_cap_robust']} tie={rp['tie_max']:.3f}")
    ok &= rp['z'] > 5 and rp['chk_cap_robust'] and rp['chk_cap_headline']

    x = [rng.random(T) for _ in range(5)]
    ri = analyze(x, 'gate-indep5-sampled', n_surr=30, n_shuf=5, rng=rng)
    print(f"(8) sampled k=5 independent T={T}: share={ri['share']:.3e} z={ri['z']:.2f} "
          f"cap_ok={ri['chk_cap_robust']}")
    ok &= abs(ri['z']) < 5 and ri['chk_cap_robust']

    print(f"\nGATE VERDICT: {'PASS' if ok else 'FAIL'}")
    return ok

# =====================================================================================
# THE REAL KERNEL — native clip vs reflecting fold, same string, clamp lines only
# =====================================================================================

FOLD_DEV = r'''
extern "C" __device__ __forceinline__ float fold01(float x){
    const float lo = 0.001f, hi = 0.999f;
    const float w = hi - lo, per = 2.0f * w;
    float y = fmodf(x - lo, per);
    if (y < 0.0f) y += per;
    if (y > w) y = per - y;
    return lo + y;
}
'''

def build_kernel(boundary):
    """Compile the SHIPPED Ossicle.KERNEL_CODE with (a) a clamp-event counter appended
    and (b) for 'fold', the three clamp expressions replaced by a reflecting fold.
    Nothing else in the kernel is touched."""
    import cupy as cp
    from runtime import Ossicle
    src = Ossicle.KERNEL_CODE

    # append the counter argument
    old_sig = "        int iterations\n    ) {"
    assert old_sig in src, "kernel signature not found — refusing to guess"
    src = src.replace(old_sig, "        int iterations,\n        float* clipcount\n    ) {")
    src = src.replace("        if (oid >= n_ossicles) return;",
                      "        if (oid >= n_ossicles) return;\n        float nclip = 0.0f;")

    n_rep = 0
    for v in ('a', 'b', 'c'):
        old = f"{v} = fminf(fmaxf(new_{v}, 0.001f), 0.999f);"
        assert old in src, f"clamp line for {v} not found — refusing to guess"
        if boundary == 'clip':
            new = (f"float cl_{v} = fminf(fmaxf(new_{v}, 0.001f), 0.999f); "
                   f"if (cl_{v} != new_{v}) nclip += 1.0f; {v} = cl_{v};")
        elif boundary == 'fold':
            new = (f"float cl_{v} = fold01(new_{v}); "
                   f"if (cl_{v} != new_{v}) nclip += 1.0f; {v} = cl_{v};")
        else:
            raise ValueError(boundary)
        src = src.replace(old, new)
        n_rep += 1
    assert n_rep == 3

    src = src.replace("        outputs[oid * 4 + 3] = sharpness;",
                      "        outputs[oid * 4 + 3] = sharpness;\n        clipcount[oid] = nclip;")
    if boundary == 'fold':
        src = FOLD_DEV + src
    mod = cp.RawModule(code=src, options=('--std=c++11',))
    return mod.get_function('ossicle_measure')

def make_runtime(n_rows, n_cols, coupling, seed):
    import cupy as cp
    from runtime import OssicleRuntime
    cp.random.seed(seed)
    rt = OssicleRuntime()
    rt.configure_array(n_rows=n_rows, n_cols=n_cols, sample_rate_hz=2000)
    rt.configure_ossicles(r_base=3.70, r_spacing=0.03, twist_deg=1.1,
                          coupling=coupling, n_cells=64, iterations=100)
    return rt

def run_trajectory(rt, kern, N, N_state, settle, sigma):
    """Drive the real kernel. Returns recorded states [N_state,n,3,cells], phase [N,n],
    and the clamp-binding rate (fraction of clamp applications that actually bound)."""
    import cupy as cp
    oss = rt.array.ossicles
    n = oss.n_ossicles
    ncells = oss.params.n_cells
    iters = oss.params.iterations
    clipbuf = cp.zeros(n, dtype=cp.float32)
    block = 256
    grid = (n + block - 1) // block
    args = (oss.states, oss.outputs, oss.baselines, oss.gpu_params,
            cp.int32(n), cp.int32(ncells), cp.int32(iters), clipbuf)

    def burst():
        oss.states += cp.random.normal(0, sigma, oss.states.shape).astype(cp.float32)
        clipbuf.fill(0)
        kern((grid,), (block,), args)
        cp.cuda.Stream.null.synchronize()

    for _ in range(settle):
        burst()
    states = np.empty((N_state, n, 3, ncells), dtype=np.float32)
    phase = np.empty((N, n), dtype=np.float32)
    clip_tot = 0.0
    denom = float(n * 3 * iters * ncells)
    for t in range(N):
        burst()
        phase[t] = cp.asnumpy(oss.outputs)[:, 2]
        clip_tot += float(clipbuf.sum()) / denom
        if t < N_state:
            states[t] = cp.asnumpy(oss.states)
    return states, phase, clip_tot / N

# =====================================================================================
# READINGS
# =====================================================================================

def reading_S3_state(states, stride=8):
    """SPATIAL k=3: the three oscillators (a,b,c) at one cell, one time. The array's
    only native coupled spatial structure (the a-b-c chain, cell-wise)."""
    sl = states[::stride]                       # (S, n, 3, cells)
    return [sl[:, :, j, :].ravel().astype(np.float64) for j in range(3)]

def reading_T_state(states, k, osc=1):
    """TEMPORAL k: oscillator `osc` (default b, the chain's centre) at k successive
    bursts. Non-overlapping stride-k windows; units (ossicle,cell) are independent
    replicas and are pooled."""
    x = states[:, :, osc, :]                    # (N, n, cells)
    N = x.shape[0]
    x = x.reshape(N, -1)                        # (N, U)
    starts = range(0, N - k + 1, k)
    return [np.concatenate([x[s + j] for s in starts]).astype(np.float64) for j in range(k)]

def reading_T_state_overlap(states, k, osc=1):
    x = states[:, :, osc, :]
    N = x.shape[0]
    x = x.reshape(N, -1)
    starts = range(0, N - k + 1)
    return [np.concatenate([x[s + j] for s in starts]).astype(np.float64) for j in range(k)]

def reading_X5_state(states, stride=3):
    """SPATIOTEMPORAL k=5: (a_t,b_t,c_t,b_{t+1},b_{t+2}). The only k=5 reading on this
    device in which all five slots are causally connected."""
    N = states.shape[0]
    starts = list(range(0, N - 2, stride))
    def g(j, dt):
        return np.concatenate([states[s + dt, :, j, :].ravel() for s in starts]).astype(np.float64)
    return [g(0, 0), g(1, 0), g(2, 0), g(1, 1), g(1, 2)]

def reading_phase_groups(phase, k):
    """SPATIAL k across disjoint ossicle groups, group-mean of the kernel's `phase`
    metric — the bench readout. Ossicles do not interact, so this is independent by
    construction: an architectural control."""
    n = phase.shape[1]
    g = n // k
    return [phase[:, i * g:(i + 1) * g].mean(axis=1).astype(np.float64) for i in range(k)]

# =====================================================================================
# SWEEP
# =====================================================================================

def condition(kappa, boundary, seed, N, N_state, settle, sigma, n_surr, n_shuf, quick=False):
    rt = make_runtime(3, 64, kappa, seed)
    kern = build_kernel(boundary)
    t0 = time.time()
    states, phase, clip_rate = run_trajectory(rt, kern, N, N_state, settle, sigma)
    t_hw = time.time() - t0
    rng = np.random.default_rng(seed)
    out = []
    specs = [
        ('S3-state', reading_S3_state(states)),
        ('T3-state', reading_T_state(states, 3)),
        ('T5-state', reading_T_state(states, 5)),
        ('X5-state', reading_X5_state(states)),
        ('S3-phase', reading_phase_groups(phase, 3)),
        ('S5-phase', reading_phase_groups(phase, 5)),
    ]
    if not quick:
        specs.append(('T3-state-overlap', reading_T_state_overlap(states, 3)))
    for tag, ch in specs:
        r = analyze(ch, tag, n_surr=n_surr, n_shuf=n_shuf, rng=rng)
        r.update(kappa=kappa, boundary=boundary, seed=seed, clip_rate=clip_rate)
        out.append(r)
        print(f"  {tag:<17} k={r['k']} T={r['T']:>8} share={r['share']:.6f} "
              f"cap_rob={r['cap_robust']:.4f} cap_hl={r['cap_headline']:.4f} "
              f"CF_hl={r['CF_headline']:+.4f} z={r['z']:>9.1f} tie={r['tie_max']:.4f} "
              f"ROB_OK={r['chk_cap_robust']} HL_OK={r['chk_cap_headline']}")
    print(f"  [hw {t_hw:.1f}s, clamp-binding rate {clip_rate:.3e}]")
    return out

def parity_stress(boundary, seed, T, delta, sigma, n_surr, n_shuf):
    """P3-inject: the bench f=1 parity construction, which SATURATES the k=3 cap.
    The sharpest cap-compliance control available — tests the bound AT the bound."""
    import cupy as cp
    rt = make_runtime(3, 64, 0.05, seed)
    kern = build_kernel(boundary)
    oss = rt.array.ossicles
    n = oss.n_ossicles
    G = n // 3
    ncells, iters = oss.params.n_cells, oss.params.iterations
    clipbuf = cp.zeros(n, dtype=cp.float32)
    block = 256; grid = (n + block - 1) // block
    args = (oss.states, oss.outputs, oss.baselines, oss.gpu_params,
            cp.int32(n), cp.int32(ncells), cp.int32(iters), clipbuf)
    rng = np.random.default_rng(seed)
    base = 0.05
    coup = np.full(n, base, dtype=np.float32)
    for _ in range(20):
        oss.states += cp.random.normal(0, sigma, oss.states.shape).astype(cp.float32)
        kern((grid,), (block,), args); cp.cuda.Stream.null.synchronize()
    A = np.empty(T); B = np.empty(T); C = np.empty(T)
    clip_tot = 0.0
    for t in range(T):
        a = int(rng.integers(0, 2)); b = int(rng.integers(0, 2)); c = a ^ b
        coup[0:G] = base + delta * a
        coup[G:2 * G] = base + delta * b
        coup[2 * G:3 * G] = base + delta * c
        oss.gpu_params[:, 3] = cp.asarray(coup)
        oss.states += cp.random.normal(0, sigma, oss.states.shape).astype(cp.float32)
        clipbuf.fill(0)
        kern((grid,), (block,), args); cp.cuda.Stream.null.synchronize()
        m = cp.asnumpy(oss.outputs)[:, 2]
        A[t] = m[0:G].mean(); B[t] = m[G:2 * G].mean(); C[t] = m[2 * G:3 * G].mean()
        clip_tot += float(clipbuf.sum()) / (n * 3 * iters * ncells)
    r = analyze([A, B, C], 'P3-inject', n_surr=n_surr, n_shuf=n_shuf, rng=rng)
    r.update(kappa=0.05, boundary=boundary, seed=seed, clip_rate=clip_tot / T)
    print(f"  P3-inject(f=1)   k=3 T={r['T']:>8} share={r['share']:.6f} "
          f"cap_hl={r['cap_headline']:.6f} CF_hl={r['CF_headline']:+.4f} z={r['z']:.1f} "
          f"ROB_OK={r['chk_cap_robust']} HL_OK={r['chk_cap_headline']}")
    return r

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gate', action='store_true')
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--N', type=int, default=6000)
    ap.add_argument('--Nstate', type=int, default=400)
    ap.add_argument('--settle', type=int, default=50)
    ap.add_argument('--sigma', type=float, default=1e-3)
    ap.add_argument('--seed', type=int, default=20260725)
    ap.add_argument('--nsurr', type=int, default=60)
    ap.add_argument('--nshuf', type=int, default=10)
    ap.add_argument('--kappas', type=str, default='0.0,0.02,0.05,0.10,0.20,0.35,0.50')
    ap.add_argument('--out', type=str, default='array_cap_results.json')
    args = ap.parse_args()

    if not gate():
        print("GATE FAILED — refusing to touch hardware.")
        return 1
    if args.gate and not args.run:
        return 0

    import cupy as cp
    print(f"\nDEVICE: {cp.cuda.runtime.getDeviceProperties(0)['name'].decode()}")
    kappas = [float(x) for x in args.kappas.split(',')]
    rows = []
    for boundary in ('clip', 'fold'):
        for kap in kappas:
            print(f"\n=== kappa={kap} boundary={boundary} seed={args.seed} ===")
            rows += condition(kap, boundary, args.seed, args.N, args.Nstate,
                              args.settle, args.sigma, args.nsurr, args.nshuf)
    print("\n=== P3-inject cap-saturating stress test ===")
    for boundary in ('clip', 'fold'):
        rows.append(parity_stress(boundary, args.seed, 4000, 0.10, args.sigma,
                                  args.nsurr, args.nshuf))
    print("\n=== replication at seeds 99, 7 (kappa=0.05) ===")
    for sd in (99, 7):
        for boundary in ('clip', 'fold'):
            print(f"--- seed={sd} boundary={boundary} ---")
            rows += condition(0.05, boundary, sd, args.N, args.Nstate, args.settle,
                              args.sigma, args.nsurr, args.nshuf, quick=True)

    viol = [r for r in rows if not r['chk_cap_robust']]
    print("\n" + "=" * 78)
    print(f"CAP COMPLIANCE: {len(rows)} readings, {len(viol)} robust-cap violations")
    print(f"  engine entropy_map_le holds: {all(r['chk_entropy_map_le'] for r in rows)}")
    print(f"  maxent <= k*log2 holds:      {all(r['chk_maxent_le_logcard'] for r in rows)}")
    hl = [r for r in rows if not r['chk_cap_headline']]
    print(f"  headline-cap exceedances:    {len(hl)}")
    for r in hl:
        print(f"    {r['tag']} k={r['k']} kappa={r['kappa']} {r['boundary']} "
              f"share={r['share']:.4f} > {r['cap_headline']:.4f}; "
              f"pair_dev_Linf={r['pair_dev_linf']:.4f} pair_ent_deficit={r['pair_ent_deficit']:.4f}")
    print("=" * 78)

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.out)
    with open(path, 'w') as f:
        json.dump(rows, f, indent=1, default=float)
    print(f"wrote {path}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
