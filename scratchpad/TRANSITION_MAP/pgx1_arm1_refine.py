"""SUPPLEMENTARY to PGX-1 Arm 1 — labelled exploratory, NOT part of frozen scoring.

TWO reasons this exists, both discovered during the run:
 (1) the frozen Krylov grid stops at 128, and at sigma=3 the A arm hits that ceiling
     (A=128 at N=262144, A=None at N=1048576) — so A's true cost is unmeasured there;
 (2) plain Lanczos loses orthogonality after ~50 steps in floating point, so an A arm
     read at m~128 needs a full-reorthogonalization cross-check before it is trusted.
Both can only make A look BETTER or equal. Neither can manufacture a win for C."""
import json
import numpy as np, cupy as cp
from scipy.linalg import eigh as dense_eigh
from polariton_gpu_ext import make_system, cheb_truth, rmse, TOL, TIMES, lanczos_pops

def lanczos_full_reorth(w, g, mmax):
    N = len(w); wd = cp.asarray(w); gd = cp.asarray(g)
    def H(pc, pe): return (gd @ pe), (gd*pc + wd*pe)
    Qc = cp.zeros(mmax+1); Qe = cp.zeros((mmax+1, N))
    Qc[0] = 1.0
    alphas = []; betas = []
    for j in range(mmax):
        vc, ve = H(Qc[j], Qe[j])
        a = float((Qc[j]*vc).get() + (Qe[j] @ ve).get()); alphas.append(a)
        vc = vc - a*Qc[j] - (betas[-1]*Qc[j-1] if j > 0 else 0)
        ve = ve - a*Qe[j] - (betas[-1]*Qe[j-1] if j > 0 else 0)
        for _ in range(2):                      # full reorthogonalization, twice
            ov = Qc[:j+1]*vc + Qe[:j+1] @ ve
            vc = vc - ov @ Qc[:j+1]; ve = ve - ov @ Qe[:j+1]
        b = float(cp.sqrt(vc*vc + (ve @ ve)).get())
        if b < 1e-13: break
        betas.append(b); Qc[j+1] = vc/b; Qe[j+1] = ve/b
    return alphas, betas

def pops_from_T(alphas, betas, m):
    mm = min(m, len(alphas))
    T = np.diag(alphas[:mm]) + np.diag(betas[:mm-1], 1) + np.diag(betas[:mm-1], -1)
    ev, V = dense_eigh(T); wt = np.abs(V[0, :])**2
    return np.abs(np.exp(-1j*np.outer(TIMES, ev)) @ wt)**2

SEEDS = {16384: 20260846, 65536: 20260856, 262144: 20260866, 1048576: 20260876}
GRID = list(range(90, 401, 10))
rows = []
for N, seed in SEEDS.items():
    w, g = make_system(N, 3.0, seed)
    truth = cheb_truth(w, g)
    mmax = 400 if N <= 262144 else 260
    al, be = lanczos_full_reorth(w, g, mmax)
    grid = [m for m in GRID if m <= len(al)]
    amin = next((m for m in grid if rmse(pops_from_T(al, be, m), truth) <= TOL), None)
    plain = lanczos_pops(w, g, ms=[m for m in grid if m <= 128])
    pmin = next((m for m in sorted(plain) if rmse(plain[m], truth) <= TOL), None)
    rows.append({'N': N, 'sigma': 3.0, 'A_min_reorth': amin, 'A_min_plain_le128': pmin,
                 'mmax_used': mmax})
    print(f"N={N:>8} sigma=3: reorth A_min={amin}  (plain-Lanczos<=128: {pmin})", flush=True)
    json.dump(rows, open('pgx1_arm1_refine.json', 'w'), indent=1, default=str)
