#!/usr/bin/env python3
"""E2 cascade / target driver. Computes BOTH declared witness conventions (E2 D2) from the
same runs and stores the raw per-batch q vectors so either license re-issues without re-running.

usage: cascade_e2.py <CELL> <W> [<W> ...]
"""
from __future__ import annotations
import json, sys, time
import numpy as np
import annihil_mc as A, mc_tables as T, seeds_frozen as S

A.set_backend("gpu")
NBATCH = 8


def batch_q(L, init_st, W, seed_pair, tab, bw):
    """One replica-pair batch -> the RAW q vectors of both arms."""
    sA, sB = seed_pair
    mA, _ = A.run_replica(L, init_st, None, W, sA, tab)
    mB, _ = A.run_replica(L, init_st, None, W, sB, tab)
    q_coh = A.cross_probs(mA, mB, tab)
    q_deph = np.zeros(3)
    for j in range(3):
        bA, _ = A.run_replica(L, init_st, j, W, sA + S.BRANCH_OFFSET * (j + 1), tab)
        bB, _ = A.run_replica(L, init_st, j, W, sB + S.BRANCH_OFFSET * (j + 1), tab)
        q_deph += bw[j] * A.cross_probs(bA, bB, tab)
    return q_coh, q_deph


def config_estimate(L, N, cfg_index, spectators, W, tab):
    """8 batches; both conventions; everything stored."""
    init_st = T.initial_site_states(L, spectators)
    bw = T.exact_branch_weights(L, spectators)
    QC, QD, Mn, Mr = [], [], [], []
    oor_raw = oor_norm = tot = 0
    nonfinite = 0
    for b in range(NBATCH):
        qc, qd = batch_q(L, init_st, W, S.seed_pair(L, N, cfg_index, b), tab, bw)
        QC.append(qc.tolist()); QD.append(qd.tolist())
        for v in list(qc) + list(qd):
            tot += 1
            if v < -0.05 or v > 1.05:
                oor_raw += 1
        Mr.append(0.5 * float(np.abs(qc - qd).sum()))
        if qc.sum() == 0.0 or qd.sum() == 0.0:
            nonfinite += 1
            Mn.append(float("nan"))
            continue
        pc, pd = qc / qc.sum(), qd / qd.sum()
        for v in list(pc) + list(pd):
            if v < -0.05 or v > 1.05:
                oor_norm += 1
        Mn.append(0.5 * float(np.abs(pc - pd).sum()))
    out = dict(cfg=cfg_index, q_coh=QC, q_deph=QD, M_norm_batches=Mn,
               M_raw_batches=Mr, nonfinite_batches=nonfinite,
               oor_raw=oor_raw / tot, oor_norm=oor_norm / max(tot - 6 * nonfinite, 1))
    for tag, arr in (("norm", np.array(Mn)), ("raw", np.array(Mr))):
        good = arr[np.isfinite(arr)]
        out[f"M_{tag}"] = float(good.mean()) if len(good) else float("nan")
        out[f"SE_{tag}"] = (float(good.std(ddof=1) / np.sqrt(len(good)))
                            if len(good) > 1 else float("nan"))
    return out


if __name__ == "__main__":
    cell = sys.argv[1]
    Ws = [int(w) for w in sys.argv[2:]]
    blob = json.load(open(f"configs/{cell}.json"))
    L, N = blob["L"], blob["N"]
    tab = A.Tables(L)
    for W in Ws:
        t0 = time.time()
        res = []
        for c, sp in enumerate(blob["configs"]):
            r = config_estimate(L, N, c, sp, W, tab)
            res.append(r)
            print(f"{cell} W={W:>9,d} cfg {c:2d}: M_norm={r['M_norm']:.6f}"
                  f"({r['SE_norm']:.6f}) M_raw={r['M_raw']:.6f}({r['SE_raw']:.6f})"
                  f" nf={r['nonfinite_batches']}", flush=True)
        json.dump(dict(cell=cell, L=L, N=N, W=W, n_batches=NBATCH, results=res),
                  open(f"mc_{cell}_W{W}.json", "w"), indent=1)
        print(f"--- {cell} W={W:,d} done in {time.time()-t0:.0f}s ---", flush=True)
