"""PGX-1 runner. Frozen in POLARITON_GPU_EXT_PREREG.md before this file existed.
All arms run on the same hardware in float64/complex128. Primary metric is the
hardware-independent minimal reduced dimension; wall time is descriptive only."""
import json, math, time, sys
import numpy as np
import cupy as cp
from scipy.special import jv
from scipy.linalg import eigh as dense_eigh

TIMES = np.linspace(0.0, 20.0, 201)
TOL = 1e-4
MS = [2,4,6,8,12,16,24,32,48,64,96,128]
BS = [1,2,4,8,16,32,64,128,256,512,1024]
TAUS = [0.0,0.001,0.003,0.01,0.03,0.1,0.3,1.0,3.0]

def make_system(N, sigma, seed):
    rng = np.random.default_rng(seed)
    w = rng.normal(0.0, sigma, N) if sigma > 0 else np.zeros(N)
    g = np.full(N, 1.0/math.sqrt(N))
    return w, g

# ---------- GPU truth: Chebyshev, self-convergent order ----------
def cheb_truth(w, g, times=TIMES):
    wd = cp.asarray(w, dtype=cp.float64); gd = cp.asarray(g, dtype=cp.float64)
    b = float(np.max(np.abs(w)) + 1.0)          # ||H|| <= max|w| + G, G=1
    dt = float(times[1]-times[0])
    bt = b*dt
    K = 4
    while abs(jv(K, bt)) > 1e-17 and K < 400: K += 1
    K = max(K, 8)
    c = np.array([jv(k, bt)*(1 if k == 0 else 2*(-1j)**k) for k in range(K+1)])
    cd = cp.asarray(c, dtype=cp.complex128)
    def hs(pc, pe):                              # H/b applied
        return (gd @ pe)/b, (gd*pc + wd*pe)/b
    pc = cp.array(1.0+0j); pe = cp.zeros(len(w), dtype=cp.complex128)
    out = [complex(pc.get())]
    for _ in range(len(times)-1):
        t0c, t0e = pc, pe
        t1c, t1e = hs(pc, pe)
        rc = cd[0]*t0c + cd[1]*t1c; re = cd[0]*t0e + cd[1]*t1e
        for k in range(2, K+1):
            h_c, h_e = hs(t1c, t1e)
            t2c = 2*h_c - t0c; t2e = 2*h_e - t0e
            rc = rc + cd[k]*t2c; re = re + cd[k]*t2e
            t0c, t0e, t1c, t1e = t1c, t1e, t2c, t2e
        pc, pe = rc, re
        out.append(complex(pc.get()))
    return np.abs(np.array(out))**2

def exact_dense_pop(w, g, times=TIMES):
    n = len(w); H = np.zeros((n+1, n+1))
    H[1:,1:] = np.diag(w); H[0,1:] = g; H[1:,0] = g
    ev, V = dense_eigh(H); wt = np.abs(V[0,:])**2
    return np.abs(np.exp(-1j*np.outer(times, ev)) @ wt)**2

def rmse(x, y): return float(np.sqrt(np.mean((np.asarray(x)-np.asarray(y))**2)))

# ---------- Baseline A: Lanczos ----------
def lanczos_pops(w, g, ms=MS):
    wd = cp.asarray(w); gd = cp.asarray(g)
    def H(pc, pe): return (gd @ pe), (gd*pc + wd*pe)
    qc = cp.array(1.0); qe = cp.zeros(len(w))
    prevc = cp.array(0.0); preve = cp.zeros(len(w))
    alphas = []; betas = []
    mmax = max(ms)
    for j in range(mmax):
        vc, ve = H(qc, qe)
        a = float(qc*vc + (qe @ ve).get()) if False else float((qc*vc).get() + (qe @ ve).get())
        alphas.append(a)
        vc = vc - a*qc - (betas[-1]*prevc if betas else 0)
        ve = ve - a*qe - (betas[-1]*preve if betas else 0)
        bta = float(cp.sqrt(vc*vc + (ve @ ve)).get())
        if bta < 1e-14: break
        betas.append(bta)
        prevc, preve = qc, qe
        qc, qe = vc/bta, ve/bta
    res = {}
    for m in ms:
        mm = min(m, len(alphas))
        T = np.diag(alphas[:mm]) + np.diag(betas[:mm-1], 1) + np.diag(betas[:mm-1], -1)
        ev, V = dense_eigh(T); wt = np.abs(V[0,:])**2
        res[m] = np.abs(np.exp(-1j*np.outer(TIMES, ev)) @ wt)**2
    return res

# ---------- Reductions ----------
def reduced_pop(wr, gr): return exact_dense_pop(wr, gr)

def bin_reduce(ws, gs, B):
    n = len(ws); idx = np.linspace(0, n, B+1).astype(int)
    w2 = gs**2
    wr = np.empty(B); gr = np.empty(B)
    for b in range(B):
        s, e = idx[b], idx[b+1]
        m = w2[s:e].sum()
        wr[b] = (w2[s:e]*ws[s:e]).sum()/m; gr[b] = math.sqrt(m)
    return wr, gr

def tau_clusters(ws, gs, tau):
    n = len(ws); starts = []; i = 0
    while i < n:
        starts.append(i)
        j = np.searchsorted(ws, ws[i] + 2*tau, side='right') - 1
        i = max(j, i) + 1
    starts = np.array(starts)
    w2 = gs**2
    csum_m = np.concatenate(([0.0], np.cumsum(w2)))
    csum_wm = np.concatenate(([0.0], np.cumsum(w2*ws)))
    ends = np.concatenate((starts[1:], [n]))
    m = csum_m[ends] - csum_m[starts]
    wr = (csum_wm[ends] - csum_wm[starts])/m
    return wr, np.sqrt(m), len(starts)

EVAL_CAP = 2500   # max reduced dimension we diagonalize; RECORDED, never silent.
                  # A method needing more than this has already lost to B (grid caps at 1024).

def score_cell(N, sigma, seed, do_krylov=True):
    w, g = make_system(N, sigma, seed)
    t0 = time.time(); truth = cheb_truth(w, g); t_truth = time.time()-t0
    order = np.argsort(w); ws = w[order]; gs = g[order]
    out = {'N': N, 'sigma': sigma, 'seed': seed, 't_truth': t_truth, 'eval_cap': EVAL_CAP}
    # A
    if do_krylov:
        t0 = time.time(); pops = lanczos_pops(w, g); tA = time.time()-t0
        amin = None
        for m in MS:
            if rmse(pops[m], truth) <= TOL: amin = m; break
        out['A_min_m'] = amin; out['t_A'] = tA
    # B
    bmin = None; bcurve = []
    for B in BS:
        if B > N: break
        wr, gr = bin_reduce(ws, gs, B)
        e = rmse(reduced_pop(wr, gr), truth); bcurve.append((B, e))
        if e <= TOL and bmin is None: bmin = B
    out['B_min'] = bmin; out['B_curve'] = bcurve
    # C
    cmin = None; ccurve = []
    for tau in TAUS:
        if tau == 0.0:
            wr, gr, k = ws.copy(), gs.copy(), N
            if N > EVAL_CAP: ccurve.append((N, 'over_cap'))
            else:
                e = rmse(reduced_pop(wr, gr), truth); ccurve.append((k, e))
                if e <= TOL and cmin is None: cmin = k
            continue
        wr, gr, k = tau_clusters(ws, gs, tau)
        if k > EVAL_CAP: ccurve.append((k, 'over_cap')); continue
        e = rmse(reduced_pop(wr, gr), truth); ccurve.append((k, e))
        if e <= TOL and (cmin is None or k < cmin): cmin = k
    out['C_min'] = cmin; out['C_curve'] = ccurve
    return out

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'gates'
    R = {}
    if mode == 'gates':
        for N in (1024, 4096):
            w, g = make_system(N, 1.0, 20260823)
            gpu = cheb_truth(w, g); cpu = exact_dense_pop(w, g)
            R[f'G1_N{N}'] = float(np.max(np.abs(gpu-cpu)))
        for N in (1024, 16384, 262144):
            w, g = make_system(N, 0.0, 20260823)
            gpu = cheb_truth(w, g)
            two = exact_dense_pop(np.array([0.0]), np.array([1.0]))
            R[f'G2_N{N}_rmse'] = rmse(gpu, two)
        print(json.dumps(R, indent=1))
        json.dump(R, open('pgx1_gates.json','w'), indent=1)
    elif mode == 'arm1':
        rows = []
        for i, N in enumerate([1024, 4096, 16384, 65536, 262144, 1048576]):
            for j, s in enumerate([0.1, 0.3, 1.0, 3.0]):
                r = score_cell(N, s, 20260823 + 10*i + j)
                rows.append(r)
                print(f"N={N:>8} s={s}: A={r.get('A_min_m')} B={r['B_min']} C={r['C_min']} (truth {r['t_truth']:.1f}s)", flush=True)
                json.dump(rows, open('pgx1_arm1.json','w'), indent=1)
        json.dump(rows, open('pgx1_arm1.json','w'), indent=1)
    elif mode == 'arm2':
        rows = []
        for N in (4096, 16384):
            for s in (0.3, 1.0):
                for r_i in range(64):
                    r = score_cell(N, s, 20260823000 + 1000*r_i + N + int(s*10), do_krylov=(r_i < 8))
                    rows.append(r)
                print(f"N={N} s={s}: done 64", flush=True)
                json.dump(rows, open('pgx1_arm2.json','w'), indent=1)
        json.dump(rows, open('pgx1_arm2.json','w'), indent=1)
