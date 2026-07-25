"""array_cap_diagnostics.py — the two refuters the main sweep demanded.

DIAG A — the P3-inject parity demo collapsed from share 0.251 (clip) to 0.001 (fold).
         Measure per-channel BIT RECOVERY under both boundaries. If recovery collapses
         under fold, the coupling-modulation -> phase-metric transduction the bench demo
         relies on runs substantially THROUGH the clamp, and the bench's claim to have
         used no clip/threshold readout nonlinearity is not supported.

DIAG B — the architecturally-uncoupled phase controls (S3-phase, S5-phase) fired at
         z = 7..31 under clip at kappa >= 0.35. Those channels are disjoint ossicle
         groups and the kernel gives ossicles NO mutual coupling, so any firing is
         null mis-specification. Adjudicate with a CROSS-RUN control: build the k
         channels from TWO INDEPENDENT RUNS (different seeds, identical parameters).
         Guaranteed independent, identical marginals and identical autocorrelation.
         If the surrogate null still fires, the null is proved mis-specified for
         autocorrelated series and the z-values are not evidence.
         (Deliberately NOT IAAFT — it certifies nothing; see the prereg.)
"""
import sys, os, json
import numpy as np
import cupy as cp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import array_cap_experiment as E

LN2 = float(np.log(2))
OUT = {}

# ---------------------------------------------------------------- DIAG A
def parity_recovery(boundary, seed=20260725, T=4000, delta=0.10, sigma=1e-3):
    rt = E.make_runtime(3, 64, 0.05, seed)
    kern = E.build_kernel(boundary)
    oss = rt.array.ossicles
    n = oss.n_ossicles; G = n // 3
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
    ch = np.empty((T, 3)); bits = np.empty((T, 3), int); crate = 0.0
    for t in range(T):
        a = int(rng.integers(0, 2)); b = int(rng.integers(0, 2)); c = a ^ b
        bits[t] = (a, b, c)
        coup[0:G] = base + delta * a
        coup[G:2*G] = base + delta * b
        coup[2*G:3*G] = base + delta * c
        oss.gpu_params[:, 3] = cp.asarray(coup)
        oss.states += cp.random.normal(0, sigma, oss.states.shape).astype(cp.float32)
        clipbuf.fill(0)
        kern((grid,), (block,), args); cp.cuda.Stream.null.synchronize()
        m = cp.asnumpy(oss.outputs)[:, 2]
        ch[t] = (m[0:G].mean(), m[G:2*G].mean(), m[2*G:3*G].mean())
        crate += float(clipbuf.sum()) / (n * 3 * iters * ncells)
    rec, dprime, seps = [], [], []
    for j in range(3):
        b_ = (ch[:, j] > np.median(ch[:, j])).astype(int)
        rec.append(max(np.mean(b_ == bits[:, j]), np.mean(b_ != bits[:, j])))
        x0 = ch[bits[:, j] == 0, j]; x1 = ch[bits[:, j] == 1, j]
        sd = np.sqrt(0.5 * (x0.var() + x1.var()))
        dprime.append(abs(x1.mean() - x0.mean()) / sd if sd > 0 else np.nan)
        seps.append((float(x0.mean()), float(x1.mean())))
    r = E.analyze([ch[:, 0], ch[:, 1], ch[:, 2]], f'P3-recov-{boundary}',
                  n_surr=60, n_shuf=10, rng=rng)
    return dict(boundary=boundary, recovery=rec, dprime=dprime, means=seps,
                share=r['share'], z=r['z'], clip_rate=crate / T,
                chan_sd=[float(ch[:, j].std()) for j in range(3)])

print("=" * 92)
print("DIAG A — P3-inject bit recovery: does the injected bit reach the readout WITHOUT the clamp?")
print("=" * 92)
OUT['diagA'] = []
for bnd in ('clip', 'fold'):
    d = parity_recovery(bnd)
    OUT['diagA'].append(d)
    print(f"  {bnd:<5} recovery A,B,C = {d['recovery'][0]:.3f},{d['recovery'][1]:.3f},"
          f"{d['recovery'][2]:.3f}   d' = {d['dprime'][0]:.3f},{d['dprime'][1]:.3f},"
          f"{d['dprime'][2]:.3f}   share = {d['share']:.6f}  z = {d['z']:.0f}  "
          f"clamp-rate = {d['clip_rate']:.3e}")
    print(f"        channel mean(bit=0) -> mean(bit=1): "
          + "  ".join(f"{m0:.5f}->{m1:.5f}" for m0, m1 in d['means'])
          + f"   chan sd = {d['chan_sd'][0]:.5f}")

# ---------------------------------------------------------------- DIAG B
def phase_run(kappa, boundary, seed, N=6000, sigma=1e-3):
    rt = E.make_runtime(3, 64, kappa, seed)
    kern = E.build_kernel(boundary)
    _, phase, crate = E.run_trajectory(rt, kern, N, 1, 50, sigma)
    return phase, crate

def acf_time(x, maxlag=200):
    x = np.asarray(x, float) - np.mean(x)
    v = np.dot(x, x) / len(x)
    if v <= 0:
        return 0.0
    tau = 0.0
    for L in range(1, maxlag):
        c = np.dot(x[:-L], x[L:]) / (len(x) - L) / v
        if c <= 0:
            break
        tau += c
    return 1 + 2 * tau

print("\n" + "=" * 92)
print("DIAG B — CROSS-RUN control: k channels drawn from TWO INDEPENDENT RUNS.")
print("         Independent by construction, identical marginals AND autocorrelation.")
print("         Any z>5 here proves the iid multinomial null is mis-specified.")
print("=" * 92)
OUT['diagB'] = []
for kappa in (0.05, 0.20, 0.35, 0.50):
    for boundary in ('clip', 'fold'):
        pA, cr = phase_run(kappa, boundary, 20260725)
        pB, _ = phase_run(kappa, boundary, 424242)
        rng = np.random.default_rng(1234)
        g3 = pA.shape[1] // 3
        g5 = pA.shape[1] // 5
        # WITHIN-RUN (as in the sweep): all channels from run A
        w3 = [pA[:, i*g3:(i+1)*g3].mean(axis=1) for i in range(3)]
        w5 = [pA[:, i*g5:(i+1)*g5].mean(axis=1) for i in range(5)]
        # CROSS-RUN: channel 0 from A, the rest from B (guaranteed independent)
        x3 = [pA[:, 0:g3].mean(axis=1)] + [pB[:, i*g3:(i+1)*g3].mean(axis=1) for i in (1, 2)]
        x5 = [pA[:, 0:g5].mean(axis=1)] + [pB[:, i*g5:(i+1)*g5].mean(axis=1) for i in (1, 2, 3, 4)]
        tau = acf_time(w3[0])
        for nm, chans in (('k3-within', w3), ('k3-cross', x3),
                          ('k5-within', w5), ('k5-cross', x5)):
            r = E.analyze(chans, nm, n_surr=60, n_shuf=10, rng=rng)
            OUT['diagB'].append(dict(kappa=kappa, boundary=boundary, which=nm,
                                     share=r['share'], z=r['z'], tau=tau,
                                     clip_rate=cr, cap_ok=r['chk_cap_robust']))
            print(f"  kappa={kappa:<5} {boundary:<5} {nm:<10} share={r['share']:.6f} "
                  f"z={r['z']:>8.1f}  tau_int={tau:6.2f}  cap_ok={r['chk_cap_robust']}")

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'array_cap_diagnostics.json')
json.dump(OUT, open(p, 'w'), indent=1, default=float)
print(f"\nwrote {p}")
