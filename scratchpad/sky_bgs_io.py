"""DESI DR1 BGS I/O for the sky campaign — Stage 1.

NEW CODE IS CONFINED TO I/O, per `SKY_BGS_PREREG.md` §11: the estimator, grid, interlaced
CIC, masked smoothing, quantile binning, `connected_info` and LP pinning are imported from
`sky_realdata.py` UNCHANGED. Rewriting them would forfeit their validation.

What this module does and nothing more: read the DESI clustering catalogues, apply the
pre-registered selection, convert to the same Cartesian frame `sky_realdata.sky_to_cart`
defines, and hand back arrays in exactly the shape the BOSS path handed them back.

SELECTION, fixed by SKY_BGS_AMENDMENT_6 before any statistic was computed:
  sample  BGS_BRIGHT (S0-A: min n_bar V_R 19.94 vs 3.18 for -21.5)
  cap     NGC only   (S0-B: both caps 39.6 GB > 35 GB threshold)
  z       0.080 - 0.320  (S0-A's factor-of-3 occupancy trim)

WEIGHTS. The catalogues ship WEIGHT (the LSS product of completeness, systematic and
redshift-failure weights) and WEIGHT_FKP separately. The BOSS path used the total
systematic weight without FKP, and GATE W/W' varies the weight choice to show the reading
does not depend on it, so the default here is WEIGHT alone with WEIGHT*WEIGHT_FKP as the
declared variation. Nothing selects between them on a result.
"""

from __future__ import annotations

import numpy as np
from astropy.io import fits

from sky_realdata import sky_to_cart

# --- the pre-registered selection, as amended. Not arguments: constants. ---
Z_LO, Z_HI = 0.080, 0.320
SAMPLE, CAP = "BGS_BRIGHT", "NGC"

_DAT = "desi_bgs/{s}_{c}_clustering.dat.fits"
_RAN = "desi_bgs/{s}_{c}_{i}_clustering.ran.fits"


def _read(path: str, weight: str) -> tuple[np.ndarray, np.ndarray]:
    """Return (positions, weights) after the pre-registered z cut.

    `weight` is 'WEIGHT' (default) or 'WEIGHT_FKP' (the GATE W/W' variation, which
    multiplies the two). No other choice is offered, so no later reader can invent one.
    """
    with fits.open(path, memmap=True) as h:
        d = h[1].data
        z = np.asarray(d["Z"], dtype=np.float64)
        keep = (z >= Z_LO) & (z <= Z_HI)
        ra = np.asarray(d["RA"], dtype=np.float64)[keep]
        dec = np.asarray(d["DEC"], dtype=np.float64)[keep]
        zz = z[keep]
        w = np.asarray(d["WEIGHT"], dtype=np.float64)[keep]
        if weight == "WEIGHT_FKP":
            w = w * np.asarray(d["WEIGHT_FKP"], dtype=np.float64)[keep]
        elif weight != "WEIGHT":
            raise ValueError(f"unregistered weight choice: {weight!r}")
    return sky_to_cart(ra, dec, zz), w


def load_data(weight: str = "WEIGHT") -> tuple[np.ndarray, np.ndarray]:
    """The BGS_BRIGHT NGC clustering catalogue, selected and in Cartesian Mpc/h."""
    return _read(_DAT.format(s=SAMPLE, c=CAP), weight)


def load_randoms(indices, weight: str = "WEIGHT") -> tuple[np.ndarray, np.ndarray]:
    """Concatenate the requested random realizations.

    `indices` is explicit — there is no 'all available' default, so a run's random
    budget is always a recorded choice rather than a property of the directory.
    """
    idx = list(indices)
    if not idx:
        raise ValueError("no random realizations requested")
    pos, wts = [], []
    for i in idx:
        p, w = _read(_RAN.format(s=SAMPLE, c=CAP, i=i), weight)
        pos.append(p)
        wts.append(w)
    return np.concatenate(pos), np.concatenate(wts)


def split_randoms(indices, weight: str = "WEIGHT"):
    """The Stage-1 gate's construction: two disjoint half-sets of randoms.

    The split-randoms null treats one half as 'data' against the other as 'randoms'.
    It contains no galaxies, so the true reading is zero by construction, and anything
    the pipeline reports on it is manufactured by the pipeline — geometry, masking,
    smoothing, binning. This is the DESI-geometry re-run of the null the BOSS campaign
    passed, and it is the reason the halves must be disjoint and equal in count.
    """
    idx = list(indices)
    if len(idx) < 2 or len(idx) % 2:
        raise ValueError(f"need an even number >= 2 of realizations, got {len(idx)}")
    half = len(idx) // 2
    a = load_randoms(idx[:half], weight)
    b = load_randoms(idx[half:], weight)
    return a, b


def inventory(indices, weight: str = "WEIGHT") -> dict:
    """Counts only. No field, no statistic — safe to print at any stage."""
    pos_d, w_d = load_data(weight)
    pos_r, w_r = load_randoms(indices, weight)
    return {
        "sample": SAMPLE, "cap": CAP, "weight": weight,
        "z_range": [Z_LO, Z_HI],
        "n_data": int(len(pos_d)), "n_random": int(len(pos_r)),
        "randoms_used": [int(i) for i in indices],
        "alpha": float(w_d.sum() / w_r.sum()),
        "w_data_sum": float(w_d.sum()), "w_random_sum": float(w_r.sum()),
        "extent_mpc_h": [float(x) for x in (pos_d.max(axis=0) - pos_d.min(axis=0))],
    }
