"""
The w0-wa covariance from the DESI DR2 chains -- and, better, the POSTERIOR on
the phantom-crossing redshift itself.

Chains: `unimpeded` public nested-sampling / MCMC database (Ong & Handley,
arXiv:2511.05470 / 2511.04661), hosted on Zenodo. Model 'walcdm' = w0waCDM.

Why this beats error propagation: z_c is a strongly nonlinear function of
(w0, wa), so a linearised sigma is unreliable no matter what correlation you
assume. With samples in hand we push each one through

    a_c = 1 + (1+w0)/wa ,   z_c = 1/a_c - 1

and read the posterior off directly.

Test: `dark-balance-extensive` stakes a FROZEN kill window z_c = 0.59 +/- 0.03.
"""
import numpy as np
import pandas as pd
from unimpeded.database import DatabaseExplorer

WIN_C, WIN_HW = 0.59, 0.03

DATASETS = [
    ("DESI DR2 + Planck (no SNe) ", "bao.desi_dr2+planck_2018_plik"),
    ("DESI DR2 + Planck + Pantheon+", "bao.desi_dr2+planck_2018_plik+sn.pantheonplus"),
    ("DESI DR2 + Planck + Union3  ", "bao.desi_dr2+planck_2018_plik+sn.union3"),
    ("DESI DR2 + Planck + DES-Y5  ", "bao.desi_dr2+planck_2018_plik+sn.desy5"),
]

d = DatabaseExplorer()


def get_w(dataset):
    """Return (w0, wa, weights) from the nested-sampling chain, falling back to MCMC."""
    last = None
    for method in ("ns", "mcmc"):
        try:
            s = d.download_samples(method, "walcdm", dataset)
        except Exception as e:                       # noqa: BLE001
            last = e
            continue
        if s is None:
            continue
        # columns are MultiIndex tuples (name, latex); match on the name, and
        # strip any BOM the CSV carried in.
        def key(c):
            k = c[0] if isinstance(c, tuple) else c
            return str(k).lstrip("﻿").strip().lower()

        cols = {key(c): c for c in s.columns}
        w0c = next((cols[k] for k in ("w", "w0") if k in cols), None)
        wac = next((cols[k] for k in ("wa",) if k in cols), None)
        if w0c is None or wac is None:
            last = KeyError(f"no w0/wa in {list(s.columns)[:40]}")
            continue
        w0 = np.asarray(s[w0c], dtype=float)
        wa = np.asarray(s[wac], dtype=float)
        try:
            wt = np.asarray(s.get_weights(), dtype=float)
        except Exception:                            # noqa: BLE001
            wt = np.ones_like(w0)
        return w0, wa, wt, method
    raise RuntimeError(f"could not load {dataset}: {last}")


def wstats(x, wt):
    wt = wt / wt.sum()
    m = np.sum(wt * x)
    v = np.sum(wt * (x - m) ** 2)
    return m, np.sqrt(v)


def wquant(x, wt, qs):
    i = np.argsort(x)
    x, wt = x[i], wt[i]
    c = np.cumsum(wt) / wt.sum()
    return np.interp(qs, c, x)


print("=" * 82)
print("W0-WA COVARIANCE AND THE z_c POSTERIOR, FROM THE DESI DR2 CHAINS")
print(f"frozen kill window: z_c = {WIN_C} +/- {WIN_HW}")
print("=" * 82)

rows = []
for label, ds in DATASETS:
    try:
        w0, wa, wt, method = get_w(ds)
    except Exception as e:                           # noqa: BLE001
        print(f"\n{label}  --  UNAVAILABLE ({type(e).__name__}: {e})")
        continue

    m0, s0 = wstats(w0, wt)
    ma, sa = wstats(wa, wt)
    wn = wt / wt.sum()
    cov = np.sum(wn * (w0 - m0) * (wa - ma))
    rho = cov / (s0 * sa)

    # posterior on the crossing redshift
    with np.errstate(divide="ignore", invalid="ignore"):
        a_c = 1.0 + (1.0 + w0) / wa
        z_c = 1.0 / a_c - 1.0
    ok = np.isfinite(z_c) & (a_c > 0) & (a_c <= 1.0)     # a real crossing at z >= 0
    frac_cross = wn[ok].sum()

    zc_ok, wt_ok = z_c[ok], wn[ok]
    med, lo, hi = wquant(zc_ok, wt_ok, [0.5, 0.16, 0.84])
    mz, sz = wstats(zc_ok, wt_ok)
    inwin = wt_ok[(zc_ok >= WIN_C - WIN_HW) & (zc_ok <= WIN_C + WIN_HW)].sum() / wt_ok.sum()
    # one-sided posterior mass above the window centre
    p_above = wt_ok[zc_ok >= WIN_C].sum() / wt_ok.sum()

    print(f"\n{label}   [{method} chain, {len(w0)} samples]")
    print(f"   w0 = {m0:+.4f} +/- {s0:.4f}")
    print(f"   wa = {ma:+.4f} +/- {sa:.4f}")
    print(f"   cov(w0,wa) = {cov:+.5f}      **rho = {rho:+.4f}**")
    print(f"   posterior with a real crossing at z>=0: {100*frac_cross:.1f}%")
    print(f"   z_c  median {med:.3f}   68% [{lo:.3f}, {hi:.3f}]   mean {mz:.3f} +/- {sz:.3f}")
    print(f"   posterior mass inside the frozen window: {100*inwin:.2f}%")
    print(f"   posterior mass at z_c >= {WIN_C}: {100*p_above:.2f}%")
    rows.append((label, rho, med, lo, hi, inwin, p_above, frac_cross))

print("\n" + "=" * 82)
print("SUMMARY")
print("=" * 82)
print(f"{'dataset':<30}{'rho':>9}{'z_c (68%)':>24}{'in window':>12}{'P(z_c>=0.59)':>14}")
for label, rho, med, lo, hi, inwin, p_above, fc in rows:
    print(f"{label:<30}{rho:>9.3f}"
          f"{f'{med:.3f} [{lo:.3f},{hi:.3f}]':>24}"
          f"{100*inwin:>11.2f}%{100*p_above:>13.2f}%")
