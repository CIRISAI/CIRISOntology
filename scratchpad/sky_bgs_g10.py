"""G10 — the mock closure. THE GO/NO-GO (prereg §5.6).

*Build the entire floor model from one half of the mock suite, then predict the other
half's reading and compare. Threshold: the predicted floor must match the held-out mocks'
reading to 10% of the SIGNAL, not 10% of the floor.*

CONSTRUCTION, stated so the choice cannot be mistaken for the prereg's:
  The floor per realization is N_A — phase-randomise the gridded masked delta keeping
  |F(k)|, then Poisson-resample at the field's own n-bar through the identical selection
  (SKY_BGS_PREREG §4.3). Both pieces are imported unchanged from the validated modules.

  N_A is NOT the null of record. The prereg registers **N_B** for outcome (a), because
  N_B is the construction that cut BOSS by 30-52%. N_B requires new code (shot-noise power
  removed in Fourier before phase randomisation, weighted kappa) and is NOT run here.
  What this file therefore tests is whether the floor model TRANSPORTS between disjoint
  halves of the suite at all — a necessary condition for G10, not the whole of it.
  **A pass here is not a G10 pass; a fail here is a G10 fail.** Recorded as such.

SIGNAL is the gravitational excess: mean(mock reading) - mean(mock floor), per config,
over the whole suite. It is what the 10% is 10% OF.

Blind: mocks only. No DESI galaxy statistic.
"""

from __future__ import annotations

import gc
import glob
import json
import sys

import numpy as np
from astropy.io import fits

import sky_bgs_io as io
from sky_realdata import (SurveyGrid, density_and_mask, masked_smooth, quantile_labels,
                          triple_hist, connected_info, configs, sky_to_cart)
from sky_surrogate import phase_randomise

R, B, CELL = 10.0, 4, 6.0
RANDOMS = (0, 1, 2, 3)
SEED0 = 90210


def _mock(path):
    with fits.open(path, memmap=True) as h:
        d = h[1].data
        z = np.asarray(d["Z"], float)
        k = (z >= io.Z_LO) & (z <= io.Z_HI)
        p = sky_to_cart(np.asarray(d["RA"], float)[k], np.asarray(d["DEC"], float)[k], z[k])
        w = np.asarray(d["WEIGHT"], float)[k]
    return p, w


def _read_field(g, sm, ok):
    """The three configs' readings off an already-smoothed field."""
    lab, _ = quantile_labels(sm, ok, B)
    stride = max(1, int(round(R / g.cell / 3)))
    out = {}
    for name, orients in configs(R, g.cell, 1.5).items():
        hs = np.zeros((B, B, B))
        for (d1, d2) in orients:
            h, _ = triple_hist(lab, ok, d1, d2, B, stride)
            hs += h
        ci = connected_info(hs)
        out[name] = {"I": float(ci["I"]), "cert": float(ci["cert"])}
    del lab
    return out


def one(g, n_ran, exp_ran, path, seed):
    """Return (reading, floor) for one realization: the mock, and its N_A null."""
    pos, w = _mock(path)
    n_g = g.deposit(pos, w)
    del pos, w
    delta, mask, alpha, _ = density_and_mask(g, n_g, n_ran)
    del n_g
    sm, ok = masked_smooth(g, delta, mask, R)
    reading = _read_field(g, sm, ok)
    del sm

    # --- N_A: phase-randomise the masked delta, then Poisson-resample at its own n-bar ---
    dpr = phase_randomise(g, delta * mask, seed)
    del delta
    # POSITIVITY GUARD, and the reason it is here. The interlaced CIC deposit returns
    # small NEGATIVE cell values outside the footprint (measured min -6.95 on this grid) --
    # a known property of the interlaced scheme, which the validated path handles via
    # CapGeometry's positivity-guarded denominator. Using the raw deposit as a Poisson rate
    # therefore fails on lam < 0. Inside `mask`, density_and_mask already guarantees
    # exp > thr > 0, so the rate is evaluated ON THE MASK ONLY and is zero elsewhere.
    lam = np.zeros_like(dpr, dtype=np.float64)
    np.multiply(alpha * exp_ran, np.maximum(1.0 + dpr, 0.0), out=lam, where=mask)
    np.clip(lam, 0.0, None, out=lam)
    n_neg_guarded = int((alpha * exp_ran * mask < 0).sum())
    clipped = float(((1.0 + dpr) < 0.0)[mask].mean())
    del dpr
    n = np.random.default_rng(seed + 1).poisson(lam).astype(np.float32)
    del lam
    exp = alpha * exp_ran
    dn = np.zeros_like(n)
    np.divide(n - exp, exp, out=dn, where=mask)
    del n, exp
    smn, okn = masked_smooth(g, dn, mask, R)
    floor = _read_field(g, smn, okn)
    del dn, smn, okn, mask, ok
    gc.collect()
    return reading, floor, clipped, n_neg_guarded


def main():
    paths = sorted(glob.glob("desi_bgs/mocks/ab_*.fits"),
                   key=lambda p: int(p.split("_")[-1].split(".")[0]))
    n = len(paths)
    if n < 8:
        print(f"only {n} mocks on disk", file=sys.stderr); return 1
    print(f"[g10] {n} realizations, R={R}, b={B}", flush=True)

    pos_r, w_r = io.load_randoms(RANDOMS)
    g = SurveyGrid(pos_r, cell=CELL)
    n_ran = g.deposit(pos_r, w_r)
    del pos_r, w_r
    gc.collect()
    exp_ran = n_ran  # the selection template; alpha applied at use

    rows = []
    for i, p in enumerate(paths):
        rd, fl, cl, ng = one(g, n_ran, exp_ran, p, SEED0 + 7 * i)
        rows.append({"mock": p, "reading": rd, "floor": fl, "clipped": cl, "neg_guarded": ng})
        print(f"[g10] {p}: read(eq)={rd['equilateral']['I']:.6e} "
              f"floor(eq)={fl['equilateral']['I']:.6e} clip={cl:.4f}", flush=True)

    # --- the closure: build half vs held-out half ---
    half = n // 2
    A, Bh = rows[:half], rows[half:]
    res = {"stage": "G10", "construction": "N_A (NOT the null of record; N_B not run)",
           "n": n, "build_half": half, "heldout_half": n - half,
           "R": R, "b": B, "configs": {}}
    for name in rows[0]["reading"]:
        fa = np.array([r["floor"][name]["I"] for r in A])
        fb = np.array([r["floor"][name]["I"] for r in Bh])
        rd = np.array([r["reading"][name]["I"] for r in rows])
        fl = np.array([r["floor"][name]["I"] for r in rows])
        signal = float(rd.mean() - fl.mean())
        pred, obs = float(fa.mean()), float(fb.mean())
        miss = abs(pred - obs)
        res["configs"][name] = {
            "floor_build_mean": pred, "floor_heldout_mean": obs,
            "closure_miss": miss,
            "reading_mean": float(rd.mean()), "floor_mean": float(fl.mean()),
            "signal": signal,
            "floor_as_pct_of_reading": float(100 * fl.mean() / rd.mean()),
            "miss_as_pct_of_signal": float(100 * miss / signal) if signal else None,
            "pass_10pct_of_signal": bool(signal and 100 * miss / signal <= 10.0),
        }
    res["clipped_mean"] = float(np.mean([r["clipped"] for r in rows]))
    res["rows"] = rows
    with open("desi_bgs/g10_closure.json", "w") as f:
        json.dump(res, f, indent=1, default=float)
    print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1, default=float))
    return 0


if __name__ == "__main__":
    sys.exit(main())
