"""N_B — the null of record, and the G10 closure re-run under it.

SKY_BGS_PREREG §4.3: *the modulation carries the CLUSTERING ONLY — the shot-noise power is
removed in Fourier BEFORE the phases are randomised, so Poisson supplies it once rather than
twice — renormalised to the data's own number density, and the counts are drawn with the
data's own WEIGHTED shot noise kappa = <w^2>/<w>.*

THE ARITHMETIC, stated so it can be argued with rather than trusted.

With `delta_i = (n_i - e_i)/e_i` on the mask and `e_i = alpha * n_ran,i`, a weighted-Poisson
draw has `Var(n_i) = kappa * e_i`, hence `Var(delta_i) = kappa / e_i`. The unnormalised
forward transform gives a WHITE shot-noise floor

    P_shot = sum_{i in mask} kappa / e_i

which is k-independent. The clustering-only amplitudes are therefore
`|F_c|^2 = max(|F|^2 - P_shot, 0)`, and the fraction of modes where that subtraction hits
the floor is REPORTED (`fourier_clipped`), because a subtraction that zeroes most of the
spectrum is not a shot-noise removal, it is a low-pass filter.

The weighted draw: `n ~ Poisson(lam / kappa) * kappa` has mean `lam` and variance
`kappa * lam`, which is the "data's own weighted shot noise" the prereg asks for. At
kappa = 1 it reduces to N_A's draw exactly, which is the check that the two constructions
differ only where the prereg says they differ.

Blind: mocks only.
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


def n_b_floor(g, delta, mask, exp, kappa, seed):
    """The N_B null: shot-noise power removed in Fourier, then a weighted-Poisson draw."""
    F = g.fwd((delta * mask).astype(np.float32))
    p2 = (F.real.astype(np.float64) ** 2 + F.imag.astype(np.float64) ** 2)

    # white shot-noise floor, from the mask's own inverse-expectation sum
    inv_e = np.zeros_like(exp, dtype=np.float64)
    np.divide(1.0, exp, out=inv_e, where=mask)
    p_shot = float(kappa * inv_e[mask].sum())
    del inv_e

    amp2 = p2 - p_shot
    hit = float((amp2 <= 0).mean())          # the honesty number for this construction
    np.maximum(amp2, 0.0, out=amp2)
    amp = np.sqrt(amp2)
    del p2, amp2

    rng = np.random.default_rng(seed)
    ph = np.exp(1j * rng.uniform(0.0, 2.0 * np.pi, F.shape))
    Fc = (amp * ph).astype(np.complex64)
    Fc[0, 0, 0] = abs(Fc[0, 0, 0])
    del F, amp, ph
    dpr = g.inv(Fc).astype(np.float32)
    del Fc

    # renormalise the clustering modulation to the field's own variance on the mask
    lam = np.zeros_like(dpr, dtype=np.float64)
    np.multiply(exp, np.maximum(1.0 + dpr, 0.0), out=lam, where=mask)
    np.clip(lam, 0.0, None, out=lam)
    clipped = float(((1.0 + dpr) < 0.0)[mask].mean())
    del dpr

    # weighted-Poisson: mean lam, variance kappa*lam
    n = (rng.poisson(lam / kappa).astype(np.float64) * kappa)
    del lam
    dn = np.zeros_like(exp, dtype=np.float32)
    np.divide(n - exp, exp, out=dn, where=mask)
    del n
    smn, okn = masked_smooth(g, dn, mask, R)
    out = _read_field(g, smn, okn)
    del dn, smn, okn
    gc.collect()
    return out, clipped, hit, p_shot


def main():
    paths = sorted(glob.glob("desi_bgs/mocks/ab_*.fits"),
                   key=lambda p: int(p.split("_")[-1].split(".")[0]))
    n = len(paths)
    print(f"[nb] {n} realizations, R={R}, b={B}, null of record N_B", flush=True)

    pos_r, w_r = io.load_randoms(RANDOMS)
    g = SurveyGrid(pos_r, cell=CELL)
    n_ran = g.deposit(pos_r, w_r)
    del pos_r, w_r
    gc.collect()

    rows = []
    for i, p in enumerate(paths):
        pos, w = _mock(p)
        kappa = float((w ** 2).mean() / w.mean())
        n_g = g.deposit(pos, w)
        del pos, w
        delta, mask, alpha, _ = density_and_mask(g, n_g, n_ran)
        del n_g
        exp = (alpha * n_ran).astype(np.float64)
        sm, ok = masked_smooth(g, delta, mask, R)
        reading = _read_field(g, sm, ok)
        del sm, ok
        floor, cl, hit, pshot = n_b_floor(g, delta, mask, exp, kappa, SEED0 + 7 * i)
        del delta, mask, exp
        gc.collect()
        rows.append({"mock": p, "kappa": kappa, "reading": reading, "floor": floor,
                     "clipped": cl, "fourier_clipped": hit, "p_shot": pshot})
        print(f"[nb] {p}: kappa={kappa:.4f} read(eq)={reading['equilateral']['I']:.6e} "
              f"floor(eq)={floor['equilateral']['I']:.6e} clip={cl:.4f} fclip={hit:.4f}",
              flush=True)

    half = n // 2
    A, Bh = rows[:half], rows[half:]
    res = {"stage": "G10 / N_B", "construction": "N_B — the null of record",
           "n": n, "build_half": half, "heldout_half": n - half, "R": R, "b": B,
           "kappa_mean": float(np.mean([r["kappa"] for r in rows])),
           "clipped_mean": float(np.mean([r["clipped"] for r in rows])),
           "fourier_clipped_mean": float(np.mean([r["fourier_clipped"] for r in rows])),
           "configs": {}}
    for name in rows[0]["reading"]:
        fa = np.array([r["floor"][name]["I"] for r in A])
        fb = np.array([r["floor"][name]["I"] for r in Bh])
        rd = np.array([r["reading"][name]["I"] for r in rows])
        fl = np.array([r["floor"][name]["I"] for r in rows])
        signal = float(rd.mean() - fl.mean())
        miss = abs(float(fa.mean()) - float(fb.mean()))
        res["configs"][name] = {
            "floor_build_mean": float(fa.mean()), "floor_heldout_mean": float(fb.mean()),
            "closure_miss": miss, "reading_mean": float(rd.mean()),
            "floor_mean": float(fl.mean()), "signal": signal,
            "floor_as_pct_of_reading": float(100 * fl.mean() / rd.mean()),
            "miss_as_pct_of_signal": float(100 * miss / signal) if signal else None,
            # A pass requires a POSITIVE signal first. The first version of this line
            # omitted that clause, so a negative signal — the floor exceeding the
            # reading, i.e. no headroom at all — evaluated as a pass. Exactly backwards.
            "pass_10pct_of_signal": bool(signal > 0 and 100 * miss / signal <= 10.0),
            "void_no_signal": bool(signal <= 0),
        }
    res["rows"] = rows
    with open("desi_bgs/g10_closure_nb.json", "w") as f:
        json.dump(res, f, indent=1, default=float)
    print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1, default=float))
    return 0


if __name__ == "__main__":
    sys.exit(main())
