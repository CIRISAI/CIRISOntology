"""bench_experiment.py — adversary-channel hardware bench demo on the REAL CIRISArray runtime.

Drives the actual GPU OssicleRuntime kernel (src/runtime.py, the r=3.70 diffusively-coupled
logistic lattice at line ~176) on the RTX 4090. Three disjoint ossicle groups = channels
A,B,C. Bits a,b independent uniform; c = a XOR b with prob f (else fresh independent bit).
Each bit is injected as a small COUPLING modulation on its group (no clip/threshold readout
nonlinearity). Held at the validated stochastic-resonance operating point: additive noise
sigma=1e-3 on the oscillator states between the kernel's 100-iteration bursts, r=3.70.
Readout per channel = group-mean of the 'phase' metric (mean pairwise correlation among the
three oscillators). Binarize each channel at its own median (b=2). Two meters on same data.

Usage: python3 bench_experiment.py --T 4000 --G 64 --delta 0.10 --fs 0,0.25,0.5,0.75,1.0
"""
import sys, time, argparse
import numpy as np
sys.path.insert(0, '/home/emoore/CIRISArray'); sys.path.insert(0, '/home/emoore/CIRISArray/src')
import cupy as cp
from runtime import OssicleRuntime
import bench_detector as D

PHASE = 2  # metric index: (rho_ab+rho_bc+rho_ac)/3

def build_runtime(G, base_coupling=0.05):
    rt = OssicleRuntime()
    rt.configure_array(n_rows=3, n_cols=G, sample_rate_hz=2000)  # 3 groups x G ossicles
    rt.configure_ossicles(r_base=3.70, r_spacing=0.03, twist_deg=1.1,
                          coupling=base_coupling, n_cells=64, iterations=100)
    return rt

def run_f(rt, G, delta, f, T, sigma, rng, base_coupling=0.05, settle=20):
    oss = rt.array.ossicles
    N = 3 * G
    idxA, idxB, idxC = slice(0, G), slice(G, 2*G), slice(2*G, 3*G)
    coup = np.full(N, base_coupling, dtype=np.float32)
    # settle at neutral coupling
    for _ in range(settle):
        oss.states += cp.random.normal(0, sigma, oss.states.shape).astype(cp.float32)
        rt.array.measure()
    A = np.empty(T); B = np.empty(T); Cc = np.empty(T)
    abits = np.empty(T, int); bbits = np.empty(T, int); cbits = np.empty(T, int)
    for t in range(T):
        a = int(rng.integers(0, 2)); b = int(rng.integers(0, 2))
        if rng.random() < f:
            c = a ^ b
        else:
            c = int(rng.integers(0, 2))
        abits[t], bbits[t], cbits[t] = a, b, c
        coup[idxA] = base_coupling + delta * a
        coup[idxB] = base_coupling + delta * b
        coup[idxC] = base_coupling + delta * c
        oss.gpu_params[:, 3] = cp.asarray(coup)
        oss.states += cp.random.normal(0, sigma, oss.states.shape).astype(cp.float32)
        m = rt.array.measure()  # [N,4] on host
        A[t] = m[idxA, PHASE].mean()
        B[t] = m[idxB, PHASE].mean()
        Cc[t] = m[idxC, PHASE].mean()
    return dict(A=A, B=B, Cc=Cc, abits=abits, bbits=bbits, cbits=cbits)

def binarize_median(x):
    med = np.median(x)
    bits = (x > med).astype(int)
    tie = float(np.mean(np.isclose(x, med, atol=1e-12)))
    return bits, tie, med

def analyze(raw, rng, n_surr=60):
    bA, tA, _ = binarize_median(raw['A'])
    bB, tB, _ = binarize_median(raw['B'])
    bC, tC, _ = binarize_median(raw['Cc'])
    bits = np.stack([bA, bB, bC], axis=1)
    # recovery accuracy vs injected bits (how well median-binarized readout recovers the bit)
    accA = max(np.mean(bA == raw['abits']), np.mean(bA != raw['abits']))
    accB = max(np.mean(bB == raw['bbits']), np.mean(bB != raw['bbits']))
    accC = max(np.mean(bC == raw['cbits']), np.mean(bC != raw['cbits']))
    pm = D.pair_meter(bits)
    jd = D.joint_detector(bits, n_surr=n_surr, rng=rng)
    tie = max(tA, tB, tC)
    return dict(max_corr=pm[0], max_mi=pm[1], corrs=pm[2], mis=pm[3],
                c3=jd['c3_obs'], null_mean=jd['null_mean'], null_sd=jd['null_sd'],
                excess=jd['excess'], z=jd['z'], tie=tie,
                acc=(accA, accB, accC), T=jd['T'])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--T', type=int, default=4000)
    ap.add_argument('--G', type=int, default=64)
    ap.add_argument('--delta', type=float, default=0.10)
    ap.add_argument('--sigma', type=float, default=1e-3)
    ap.add_argument('--fs', type=str, default='0,0.25,0.5,0.75,1.0')
    ap.add_argument('--seed', type=int, default=20260724)
    ap.add_argument('--nsurr', type=int, default=60)
    args = ap.parse_args()
    fs = [float(x) for x in args.fs.split(',')]
    rng = np.random.default_rng(args.seed)
    cp.random.seed(args.seed)

    print(f"REAL runtime | array=3x{args.G}={3*args.G} ossicles | delta={args.delta} "
          f"coupling | sigma={args.sigma} | T={args.T} | metric=phase(group-mean) | "
          f"nsurr={args.nsurr}")
    rt = build_runtime(args.G)
    print(f"{'f':>5} | {'maxCorr':>8} {'maxMI':>9} | {'C3_obs':>7} {'null_mu':>8} "
          f"{'null_sd':>8} {'excess':>8} {'z':>9} | {'tie':>5} | recov(A,B,C)")
    rows = []
    t0 = time.time()
    for f in fs:
        raw = run_f(rt, args.G, args.delta, f, args.T, args.sigma, rng)
        r = analyze(raw, rng, n_surr=args.nsurr)
        rows.append((f, r))
        print(f"{f:>5.2f} | {r['max_corr']:>8.4f} {r['max_mi']:>9.2e} | "
              f"{r['c3']:>7.4f} {r['null_mean']:>8.4f} {r['null_sd']:>8.4f} "
              f"{r['excess']:>8.4f} {r['z']:>9.1f} | {r['tie']:>5.3f} | "
              f"{r['acc'][0]:.2f},{r['acc'][1]:.2f},{r['acc'][2]:.2f}")
    print(f"\nelapsed {time.time()-t0:.1f}s")
    return rows

if __name__ == "__main__":
    main()
