"""Stage 1 gate — the split-randoms null on DESI DR1 BGS geometry.

The gate, per SKY_BGS_PREREG.md §11: *the split-randoms null re-run on DESI geometry;
G9 and G7 re-passed.*

WHAT THE NULL IS. Two disjoint halves of the random catalogue: one painted as if it were
the data, the other as the randoms. There is not one galaxy in the construction, so the
true whole-only reading is ZERO by construction. Anything the pipeline reports here it
manufactured itself — out of the footprint, the mask, the smoothing kernel, the quantile
binning, or the triple geometry. This is the DESI-geometry re-run of the null the BOSS
campaign passed, and it is the only test at this stage that can fail.

This reads NO galaxy positions and computes NO data statistic. It is inside the blind.

G7 — tied and railed fraction disclosed for every reading (house rule 4).
G9 — IPF certificate |share_H - share_KL| < 1e-9 at every b.
"""

from __future__ import annotations

import json
import sys

import numpy as np

import sky_bgs_io as io
from sky_realdata import SurveyGrid, density_and_mask, measure_field

R_PRIMARY = 15.0
BS = (4, 6, 8)
CELL = 6.0


def main(indices=(0, 1, 2, 3)) -> dict:
    idx = list(indices)
    print(f"[stage1] split-randoms null on DESI geometry, randoms {idx}", flush=True)

    (pos_a, w_a), (pos_b, w_b) = io.split_randoms(idx)
    print(f"[stage1] half A {len(pos_a):,}  half B {len(pos_b):,}", flush=True)

    # The grid is built on the union so both halves live on the identical geometry —
    # a grid fitted to one half would itself be a difference between them.
    g = SurveyGrid(np.concatenate([pos_a, pos_b]), cell=CELL)
    print(f"[stage1] grid {g.N} cell {g.cell}  ncell {g.ncell:,}", flush=True)

    n_a = g.deposit(pos_a, w_a)
    n_b = g.deposit(pos_b, w_b)
    del pos_a, pos_b, w_a, w_b

    delta, mask, alpha, thr = density_and_mask(g, n_a, n_b)
    print(f"[stage1] alpha {alpha:.6f}  mask frac {mask.mean():.4f}", flush=True)
    del n_a, n_b

    out = measure_field(g, delta, mask, R_PRIMARY, bs=BS, run_lp=True)

    # --- G7 / G9, read off every reading ---
    g7, g9 = [], []
    for b, rec in out["b"].items():
        for name, e in rec.items():
            if "share" not in e and "I3" not in e:
                continue
            key = "share" if "share" in e else "I3"
            g7.append({"b": b, "config": name, "tied": e.get("tied"),
                       "occupancy": e.get("occupancy"),
                       "occupancy_pass": e.get("occupancy_pass")})
            cert = e.get("kl_gap", e.get("cert"))
            g9.append({"b": b, "config": name, "value": e.get(key), "kl_gap": cert})

    res = {
        "stage": 1, "gate": "split-randoms null (DESI geometry)",
        "randoms": idx, "half_a": idx[: len(idx) // 2], "half_b": idx[len(idx) // 2:],
        "grid": {"N": list(g.N), "cell": g.cell, "ncell": g.ncell},
        "alpha": float(alpha), "mask_frac": float(mask.mean()),
        "n_valid": out["n_valid"], "n_indep": out["n_indep"], "sigma": out["sigma"],
        "readings": out["b"], "G7_tied": g7, "G9_cert": g9,
    }
    return res


if __name__ == "__main__":
    r = main()
    with open("desi_bgs/stage1_split_randoms.json", "w") as f:
        json.dump(r, f, indent=1, default=float)
    print(json.dumps({k: v for k, v in r.items() if k != "readings"}, indent=1, default=float))
    sys.exit(0)
