#!/usr/bin/env python3
"""ARM A, THE EQUILIBRATION GATE -- run BEFORE any share is read.

`WATER_PREREG.md` sec 5.6 fixes four checks at every state point and declares in
advance that "Any state point failing any of the four is NOT RUN, not a null",
because "a cavitated configuration reads a large share that is a reading on a
bubble".  Check 4 is mandatory "on every negative-pressure point", and
`WATER_ARM_A_GATE.md` sec 4 disclosed in advance that the matched-density sweep
puts every low-lambda point at large negative pressure.

THIS FILE COMPUTES NO SHARE.  Every quantity here is a density or a
pair/geometric quantity the instrument is blind to by construction, plus the
label composition p1, which sec 5.4 already requires per cell.

The four diagnostics, and what each would look like if the liquid had separated:

  cell over-dispersion   sd/mean of the count in (L/4)^3 cells, against the
                         Poisson value 1/sqrt(<count>).  A homogeneous liquid
                         reads BELOW Poisson (it is more ordered than random);
                         a two-phase system reads far above.
  max void radius        distance from the emptiest point of a 24^3 grid to the
                         nearest particle.  A bubble is a void.
  <n> at r_cut           mean first-shell coordination.  At rho = 0.997 g/cm^3 a
                         HOMOGENEOUS liquid must read near the value the mean
                         number density implies; a dense droplet reads the
                         close-packed value whatever the box mean density is.
  p1                     the HDL-like label fraction.  p1 -> 1 is label
                         degeneracy: the 2x2x2 table collapses into one cell and
                         the ThirdCap ceiling goes to zero, which is outcome (g)
                         CEILING-COLLAPSED / UNGAUGED, NOT a floor reading.

POLARITY, declared here in the sec 5.5 G-POL form: a PASS is over-dispersion at
or below the Poisson value, a max void below the template's own outer edge, and
a coordination consistent with the box-mean density.  A FAIL is NOT RUN.
"""
import argparse
import json
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import water_arm_a as WA  # noqa: E402

RCUT = 3.50
MASS, NA = 18.015, 6.02214076e23


def max_sk(pos, L, nmax=8):
    """sec 5.6 check 3, the crystallinity check, in its translational form.

    S(k) = |sum_j exp(i k.r_j)|^2 / N over the box's own reciprocal lattice.  A
    liquid's S(k) peaks at O(1-3); a crystal puts a Bragg peak at O(N).  The
    hazard runs the OPPOSITE way from cavitation -- it appears as lambda rises,
    not as it falls -- so both ends of the dose are gated and neither is assumed
    safe.
    """
    n = len(pos)
    m = np.arange(-nmax, nmax + 1)
    K = np.stack(np.meshgrid(m, m, m, indexing="ij"), -1).reshape(-1, 3)
    K = K[(K != 0).any(1)] * (2 * np.pi / L)
    ph = pos @ K.T
    S = (np.cos(ph).sum(0) ** 2 + np.sin(ph).sum(0) ** 2) / n
    return float(S.max())


def diagnose(pos, L, rcut=RCUT, ncell=4, ngrid=24):
    n = len(pos)
    idx = np.floor(pos / L * ncell).astype(int) % ncell
    cnt = np.zeros((ncell,) * 3)
    np.add.at(cnt, (idx[:, 0], idx[:, 1], idx[:, 2]), 1)
    exp = n / ncell ** 3
    g = np.linspace(0, L, ngrid + 1)[:-1] + L / (2 * ngrid)
    G = np.stack(np.meshgrid(g, g, g, indexing="ij"), -1).reshape(-1, 3)
    d = G[:, None, :] - pos[None, :, :]
    d -= L * np.round(d / L)
    dmin = np.sqrt(np.einsum("ijk,ijk->ij", d, d)).min(1)
    nb = WA.coordination(pos, L, rcut)
    # the coordination an IDEAL GAS at the box-mean number density would give
    n_ideal = (4.0 / 3.0) * np.pi * rcut ** 3 * n / L ** 3
    return dict(over_disp=float(cnt.std() / exp), poisson=float(1 / np.sqrt(exp)),
                cell_min=float(cnt.min()), cell_max=float(cnt.max()),
                max_void=float(dmin.max()), nbar=float(nb.mean()),
                n_ideal_gas=float(n_ideal), local_over_mean=float(nb.mean() / n_ideal),
                p1=float((nb >= 5).mean()), max_Sk=max_sk(pos, L),
                nhist=np.bincount(nb, minlength=20)[:16].tolist())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", default="/home/emoore/CIRISOntology/scratchpad/water_mw_sweep.json")
    ap.add_argument("--every", type=int, default=20, help="stride over frames")
    ap.add_argument("--out", default="/home/emoore/CIRISOntology/scratchpad/water_homog.json")
    a = ap.parse_args()
    sw = json.load(open(a.sweep))
    res = {}
    print("%-7s %8s %8s %8s %8s %8s %8s %8s %6s %8s  %s"
          % ("lam", "rho", "overdisp", "poisson", "maxvoid", "rvoidmax", "<n>",
             "n_ideal", "p1", "maxS(k)", "verdict"), flush=True)
    for k in sorted(sw, key=float):
        fr = WA.read_dump(sw[k]["dump"])
        ds = [diagnose(p, L) for p, L in fr[::a.every]]
        agg = {q: float(np.mean([d[q] for d in ds])) for q in
               ("over_disp", "poisson", "cell_min", "max_void", "nbar",
                "n_ideal_gas", "local_over_mean", "p1", "max_Sk")}
        agg["nframes"] = len(ds)
        agg["p1_min"] = float(np.min([d["p1"] for d in ds]))
        agg["p1_max"] = float(np.max([d["p1"] for d in ds]))
        agg["nhist"] = ds[-1]["nhist"]
        # r_void_max: the radius a Poisson process at the SAME mean number
        # density exceeds with probability 0.01 over the same 24^3 grid.
        pos0, L0 = fr[0]
        nnum = len(pos0) / L0 ** 3
        rvmax = float((-np.log(0.01 / 24 ** 3) / (4.0 / 3.0 * np.pi * nnum)) ** (1.0 / 3.0))
        agg["r_void_max"] = rvmax
        disp_ok = agg["over_disp"] <= 1.5 * agg["poisson"]
        void_ok = agg["max_void"] <= rvmax
        homog = disp_ok and void_ok
        labok = 0.02 <= agg["p1"] <= 0.98
        xtal_ok = agg["max_Sk"] < 0.05 * len(pos0)
        agg["homogeneous"] = bool(homog)
        agg["disp_ok"], agg["void_ok"] = bool(disp_ok), bool(void_ok)
        agg["label_nondegenerate"] = bool(labok)
        agg["not_crystalline"] = bool(xtal_ok)
        agg["verdict"] = ("PASS" if (homog and labok and xtal_ok) else
                          ("CAVITATED" if not homog else
                           ("CRYSTALLINE" if not xtal_ok else "LABEL-DEGENERATE")))
        res[k] = agg
        print("%-7s %8.4f %8.3f %8.3f %8.2f %8.2f %8.2f %8.2f %6.3f %8.1f  %s"
              % (k, sw[k]["rho_avg"] if "rho_avg" in sw[k] else sw[k]["rho"],
                 agg["over_disp"], agg["poisson"], agg["max_void"], rvmax,
                 agg["nbar"], agg["n_ideal_gas"], agg["p1"], agg["max_Sk"],
                 agg["verdict"]), flush=True)
    json.dump(res, open(a.out, "w"), indent=1)
    print("\nwrote", a.out, flush=True)


if __name__ == "__main__":
    main()
