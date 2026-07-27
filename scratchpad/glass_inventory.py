#!/usr/bin/env python3
"""Stage-1 inventory: what is actually inside the converted GlassBench data.

Reports, per state point: configuration count, particle count, composition, the
box edge (determined from the data, not assumed), and the species-resolved pair
correlation functions.

`g(r)` is a PAIR quantity.  The instrument of this campaign is blind to it by
construction, and it has been published for the Kob-Andersen mixture since 1995,
so measuring it at the inventory stage is not a look at the campaign's own
observable.  It is here to (a) fix the box edge, (b) confirm the data is the
model it says it is, and (c) state where the first coordination shell sits.
NO SHARE IS COMPUTED IN THIS FILE.
"""
import glob
import json
import os
import sys

import numpy as np


def fit_box(pos, dim, rho_hint=None):
    """Box edge, determined from the data rather than assumed.

    The configurations are wrapped into [-L/2, L/2), and at these particle
    counts the box is filled to its edge, so `2*max|x|` pins L directly.  It is
    checked against the model's nominal density rather than taken on faith, and
    the RELATIVE DISAGREEMENT between the two is returned so that the check is a
    reading and not a claim.
    """
    ext = float(np.abs(pos).max()) * 2.0
    N = pos.shape[1]
    if rho_hint is None:
        return ext, 0.0, ext
    nominal = (N / rho_hint) ** (1.0 / dim)
    return nominal, abs(ext / nominal - 1.0), ext


def gofr(pos, types, L, dim, rmax, nbin=300, nconf=40):
    """Species-resolved g_ab(r), minimum image."""
    N = pos.shape[1]
    edges = np.linspace(0.0, rmax, nbin + 1)
    labs = np.unique(types)
    H = {(int(a), int(b)): np.zeros(nbin) for a in labs for b in labs}
    use = pos[:nconf]
    tt = types[:nconf]
    for c, t in zip(use, tt):
        d = c[:, None, :] - c[None, :, :]
        d -= L * np.round(d / L)
        r = np.sqrt(np.einsum('ijk,ijk->ij', d, d))
        np.fill_diagonal(r, np.inf)
        for a in labs:
            for b in labs:
                m = (t[:, None] == a) & (t[None, :] == b)
                H[(int(a), int(b))] += np.histogram(r[m], bins=edges)[0]
    rho = N / L ** dim
    rc = 0.5 * (edges[1:] + edges[:-1])
    shell = (4 * np.pi * rc ** 2 * (edges[1] - edges[0]) if dim == 3
             else 2 * np.pi * rc * (edges[1] - edges[0]))
    out = {}
    for (a, b), h in H.items():
        na = int((tt[0] == a).sum())
        out[f"{a}{b}"] = (h / (len(use) * na * rho * shell *
                               ((tt[0] == b).sum() / N))).tolist()
    return rc.tolist(), out


def main():
    base = "/home/emoore/CIRISOntology/scratchpad/glass/compact"
    rows = {}
    for f in sorted(glob.glob(os.path.join(base, "*.npz"))):
        tag = os.path.basename(f)[:-4]
        z = np.load(f, allow_pickle=False)
        pos, typ = z["positions"], z["types"]
        dim = pos.shape[2]
        rho_hint = 1.2 if dim == 3 else None
        L, res, ext = fit_box(pos, dim, rho_hint)
        if tag.startswith("KA2D"):
            L = 32.8962                      # stated in the dataset's own README
            res = 0.0
        N = pos.shape[1]
        labs, cnts = np.unique(typ, return_counts=True)
        rc, g = gofr(pos, typ, L, dim, min(6.0, 0.49 * L))
        gtot = np.zeros(len(rc))
        for a, na in zip(labs, cnts):
            for b, nb in zip(labs, cnts):
                gtot += (na / cnts.sum()) * (nb / cnts.sum()) * np.array(g[f"{a}{b}"])
        i0 = int(np.argmax(np.array(gtot)[np.array(rc) > 0.7 * (1 if dim == 3 else 1)]))
        off = int((np.array(rc) <= 0.7).sum())
        rows[tag] = dict(
            n_config=int(pos.shape[0]), n_particles=int(N), dim=dim,
            box=L, box_fit_residual=res, particle_extent=ext,
            density=float(N / L ** dim),
            species={int(a): int(c // pos.shape[0]) for a, c in zip(labs, cnts)},
            composition={int(a): float(c / cnts.sum()) for a, c in zip(labs, cnts)},
            first_peak_r=float(rc[off + i0]), first_peak_g=float(gtot[off + i0]),
            g_tail_mean=float(np.mean(gtot[-20:])),
            has_inherent=bool(np.isfinite(z["inherent"][:, 0, 0]).all()),
            rc=rc, g=g, g_total=gtot.tolist())
        r = rows[tag]
        print(f"{tag:12s} nconf={r['n_config']:5d} N={N:5d} d={dim} "
              f"L={L:.4f} (fit res {res:.4f}) rho={r['density']:.4f} "
              f"comp={r['composition']} peak r={r['first_peak_r']:.3f} "
              f"g={r['first_peak_g']:.3f} tail={r['g_tail_mean']:.4f}")
    json.dump(rows, open("/home/emoore/CIRISOntology/scratchpad/glass_inventory.json", "w"))
    print("\nwrote glass_inventory.json")


if __name__ == "__main__":
    main()
