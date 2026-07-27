#!/usr/bin/env python3
"""
eboss_stage0.py -- STAGE 0 inventory for the eBOSS DR16 confirmation campaign.

Reads METADATA AND THE SELECTION FUNCTION ONLY.  No order-3 quantity, no correlation
function, no power spectrum is evaluated on any catalogue here.  This is the eBOSS analogue
of SKY_REALDATA_AMENDMENT_1 (BOSS Stage 0), and it deliberately runs the SAME estimators over
the BOSS DR12 catalogue that is already on disk, so that every eBOSS number is comparable to
the priors of record rather than to a recalled number.

Cosmology is the pre-registered fiducial of the BOSS campaign: flat, Om = 0.31, h = 0.68,
imported from sky_realdata rather than re-declared (house rule: reuse the validated source).

Outputs eboss_stage0.json.
"""
import json
import os
import sys

import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import chi, growth, log            # noqa: E402

DATA = os.environ.get('SKYDATA', '/home/emoore/skydata')
EB = f"{DATA}/eboss"
RS = [15.0, 10.0]
BS = [4, 6, 8, 16]
P0_FKP = 1e4
DEG2 = (180.0 / np.pi) ** 2          # square degrees per steradian

# The published clustering redshift ranges of the DR16 LSS catalogues (Ross et al. 2020).
# They are RECORDED here and then CHECKED against the catalogue's own min/max below; the
# check is reported, never assumed.
ZRANGE = {'LRG': (0.6, 1.0), 'ELG': (0.6, 1.1), 'QSO': (0.8, 2.2),
          'LRGpCMASS': (0.6, 1.0)}


def vol_smooth(R):
    """The Gaussian smoothing volume the occupancy gate counts in, (Mpc/h)^3."""
    return (2 * np.pi) ** 1.5 * R ** 3


def equal_area_footprint(ra, dec, nra=720, ndec=360):
    """Footprint solid angle by counting occupied EQUAL-AREA cells in (RA, sin DEC).

    Cells are equal area by construction, so no cos(dec) weighting is needed and no healpix
    dependency is introduced.  Reported at two resolutions: an occupied-cell count is biased
    HIGH by the boundary (partly-filled cells count in full), and the bias shrinks with cell
    area, so the pair of numbers brackets the answer and its convergence is visible.
    """
    s = np.sin(np.deg2rad(dec))
    i = np.clip(((ra % 360.0) / 360.0 * nra).astype(np.int64), 0, nra - 1)
    j = np.clip(((s + 1.0) / 2.0 * ndec).astype(np.int64), 0, ndec - 1)
    occ = np.unique(i * ndec + j).size
    cell_sr = (2 * np.pi / nra) * (2.0 / ndec)
    return occ * cell_sr * DEG2, occ


def shell_volume(area_deg2, zlo, zhi):
    """Comoving volume of the survey shell, (Gpc/h)^3 and (Mpc/h)^3."""
    sr = area_deg2 / DEG2
    v = sr / 3.0 * (chi(zhi) ** 3 - chi(zlo) ** 3)
    return v


def nbar_summary(nz, w=None):
    """Summaries of the SHIPPED selection function n-bar(z), (h/Mpc)^3.

    Two conventions are reported because they answer different questions and the campaign
    record does not fix which one 'typical' meant:
      gal   -- the mean n-bar experienced by a galaxy (the one that governs shot noise)
      vol   -- the volume-weighted mean, sum(1)/sum(1/n) over galaxies == N / V_occupied
    """
    nz = np.asarray(nz, float)
    nz = nz[nz > 0]
    out = dict(n_gal_weighted=float(nz.mean()),
               n_vol_weighted=float(nz.size / np.sum(1.0 / nz)),
               n_median=float(np.median(nz)),
               n_peak=float(np.quantile(nz, 0.99)),
               n_max=float(nz.max()))
    return out


def veff_fkp(nz, p0=P0_FKP):
    """FKP effective volume, (Gpc/h)^3.

    V_eff = int [ n P0 / (1 + n P0) ]^2 dV, evaluated as a sum over galaxies with dV = 1/n
    (each galaxy carries the volume element in which it is the expected count), which is the
    standard Monte-Carlo form and needs no separate radial grid.
    """
    nz = np.asarray(nz, float)
    nz = nz[nz > 0]
    x = nz * p0 / (1.0 + nz * p0)
    return float(np.sum(x ** 2 / nz) / 1e9)


def kappa(w):
    """<w^2>/<w> -- the factor by which weighted counts are super-Poisson.

    This is refuter caveat A1's measured quantity, read straight off the catalogue.
    """
    w = np.asarray(w, float)
    return float((w ** 2).mean() / w.mean())


def read_eboss(tracer, cap):
    f = f"{EB}/eBOSS_{tracer}_clustering_data-{cap}-vDR16.fits"
    with fits.open(f) as h:
        d = h[1].data
        cols = list(h[1].columns.names)
        r = {k: np.asarray(d[k], float) for k in
             ('RA', 'DEC', 'Z', 'NZ', 'WEIGHT_SYSTOT', 'WEIGHT_CP', 'WEIGHT_NOZ',
              'WEIGHT_FKP') if k in cols}
    return r, cols


def read_eboss_ran(tracer, cap, cols=('RA', 'DEC', 'Z', 'NZ')):
    f = f"{EB}/eBOSS_{tracer}_clustering_random-{cap}-vDR16.fits"
    if not os.path.exists(f):
        return None, None
    with fits.open(f, memmap=True) as h:
        names = list(h[1].columns.names)
        d = h[1].data
        r = {k: np.asarray(d[k], float) for k in cols if k in names}
    return r, names


def analyse(tag, ra, dec, z, nz, wsys, wcp, wnoz, wfkp, zlo, zhi, nran, rancols):
    m = (z > zlo) & (z < zhi)
    n_all = int(z.size)
    ra, dec, z, nz = ra[m], dec[m], z[m], nz[m]
    rec = dict(tag=tag, n_rows_all_z=n_all, n_in_zrange=int(m.sum()),
               z_min_cat=float(z.min()), z_max_cat=float(z.max()),
               z_lo_used=zlo, z_hi_used=zhi)

    a512, occ512 = equal_area_footprint(ra, dec, 1440, 720)
    a256, occ256 = equal_area_footprint(ra, dec, 720, 360)
    rec['area_deg2_fine'] = a512
    rec['area_deg2_coarse'] = a256
    rec['area_cells_fine'] = occ512

    # WHICH AREA IS USED, and why it is not the galaxy-derived one.  An occupied-cell count is
    # biased HIGH by partly-filled boundary cells and biased LOW by empty interior cells, and
    # for the sparse eBOSS tracers the second bias dominates: LRG NGC puts 107 500 galaxies
    # into ~56 000 fine cells, ~1.9 per cell, so a large fraction of genuinely-covered cells
    # are empty by chance.  The RANDOM catalogue has 40-57x the density and does not have that
    # problem, so where randoms exist the footprint is taken from them.  This choice affects
    # V_shell and hence the occupancy gate; it does NOT affect n-bar V_R, which is read off the
    # shipped NZ column and is area-free.
    area = a512
    rec['area_source'] = 'galaxies (fine occupied-cell count)'
    if nran is not None:
        rz0 = nran['Z']
        rm0 = (rz0 > zlo) & (rz0 < zhi)
        ar_f, _ = equal_area_footprint(nran['RA'][rm0], nran['DEC'][rm0], 1440, 720)
        ar_c, _ = equal_area_footprint(nran['RA'][rm0], nran['DEC'][rm0], 720, 360)
        rec['area_deg2_randoms_fine'] = ar_f
        rec['area_deg2_randoms_coarse'] = ar_c
        rec['area_randoms_convergence'] = ar_f / ar_c
        area = ar_f
        rec['area_source'] = 'randoms (fine occupied-cell count)'
    rec['area_deg2'] = area

    v = shell_volume(area, zlo, zhi)
    rec['shell_volume_Gpc3'] = v / 1e9
    rec.update({('nbar_' + k): val for k, val in nbar_summary(nz).items()})
    rec['Veff_FKP_Gpc3'] = veff_fkp(nz)

    ng = rec['nbar_n_gal_weighted']
    for R in RS:
        rec[f'nbarV_R{int(R)}_galweighted'] = ng * vol_smooth(R)
        rec[f'nbarV_R{int(R)}_volweighted'] = rec['nbar_n_vol_weighted'] * vol_smooth(R)

    # Occupancy of the b^3 triple histogram, counted in INDEPENDENT SMOOTHING VOLUMES over the
    # survey shell.  This is the Stage-0 estimate; Stage 2 replaces the shell volume with the
    # measured valid-cell count, which is strictly smaller, so THIS IS AN UPPER BOUND on the
    # occupancy and a gate failing here fails a fortiori.
    for R in RS:
        n_ind = v / vol_smooth(R)
        rec[f'n_indep_shell_R{int(R)}'] = n_ind
        for b in BS:
            rec[f'occ_R{int(R)}_b{b}'] = n_ind / b ** 3

    if wsys is not None:
        wsys, wcp, wnoz = wsys[m], wcp[m], wnoz[m]
        w = wsys * (wcp + wnoz - 1.0)
        rec['weight_scheme'] = 'WEIGHT_SYSTOT * (WEIGHT_CP + WEIGHT_NOZ - 1)'
        rec['kappa_standard'] = kappa(w)
        rec['kappa_cp_noz_only'] = kappa(wcp + wnoz - 1.0)
        rec['kappa_systot_only'] = kappa(wsys)
        rec['sum_w'] = float(w.sum())
        for nm, arr in (('SYSTOT', wsys), ('CP', wcp), ('NOZ', wnoz),
                        ('FKP', wfkp[m] if wfkp is not None else None)):
            if arr is None:
                continue
            rec[f'w{nm}_mean'] = float(arr.mean())
            rec[f'w{nm}_min'] = float(arr.min())
            rec[f'w{nm}_max'] = float(arr.max())
            rec[f'w{nm}_frac_ne1'] = float(np.mean(np.abs(arr - 1.0) > 1e-9))

    if nran is not None:
        rz = nran['Z']
        rm = (rz > zlo) & (rz < zhi)
        rec['n_random_all_z'] = int(rz.size)
        rec['n_random_in_zrange'] = int(rm.sum())
        rec['random_ratio'] = float(rm.sum()) / float(m.sum())
        ar, _ = equal_area_footprint(nran['RA'][rm], nran['DEC'][rm], 1440, 720)
        rec['area_deg2_from_randoms'] = ar
        rec['random_surface_density_deg2'] = float(rm.sum()) / ar
        rec['random_columns'] = rancols
    return rec


def boss_reference(cap):
    """The SAME estimators on the BOSS DR12 catalogue already on disk.

    This exists so the eBOSS density numbers are compared against a number produced by this
    code, not against a number recalled from AMENDMENT_1.  If this reproduces AMENDMENT_1's
    4.81 / 16.22, the eBOSS numbers below are on the same footing as the priors of record; if
    it does not, the discrepancy is a Stage-0 finding and is reported as one.
    """
    f = {'NGC': 'North', 'SGC': 'South'}[cap]
    with fits.open(f"{DATA}/galaxy_DR12v5_CMASSLOWZTOT_{f}.fits.gz") as h:
        d = h[1].data
        z = np.asarray(d['Z'], float)
        ra = np.asarray(d['RA'], float); dec = np.asarray(d['DEC'], float)
        nz = np.asarray(d['NZ'], float)
        ws = np.asarray(d['WEIGHT_SYSTOT'], float)
        wc = np.asarray(d['WEIGHT_CP'], float)
        wn = np.asarray(d['WEIGHT_NOZ'], float)
        wf = np.asarray(d['WEIGHT_FKP'], float)
    return analyse(f"BOSS-DR12-{cap}", ra, dec, z, nz, ws, wc, wn, wf,
                   0.2, 0.75, None, None)


def main():
    out = {'cosmology': dict(Om=0.31, h=0.68, flat=True),
           'P0_FKP': P0_FKP, 'V_smooth': {str(int(R)): vol_smooth(R) for R in RS},
           'tracers': {}, 'boss_reference': {}}

    log("=" * 96)
    log("eBOSS DR16 STAGE 0 -- metadata and selection function only.")
    log("=" * 96)

    for cap in ('NGC', 'SGC'):
        r = boss_reference(cap)
        out['boss_reference'][cap] = r
        log(f"  BOSS DR12 {cap}: N={r['n_in_zrange']}  area={r['area_deg2']:.0f} deg^2  "
            f"V_shell={r['shell_volume_Gpc3']:.3f} (Gpc/h)^3  Veff={r['Veff_FKP_Gpc3']:.3f}  "
            f"nbarV(15)={r['nbarV_R15_galweighted']:.2f} / {r['nbarV_R15_volweighted']:.2f}  "
            f"nbarV(10)={r['nbarV_R10_galweighted']:.2f} / {r['nbarV_R10_volweighted']:.2f}  "
            f"kappa={r['kappa_standard']:.4f}")

    for tracer in ('LRG', 'ELG', 'QSO', 'LRGpCMASS'):
        zlo, zhi = ZRANGE[tracer]
        for cap in ('NGC', 'SGC'):
            try:
                g, cols = read_eboss(tracer, cap)
            except FileNotFoundError:
                log(f"  [{tracer} {cap}] catalogue absent -- skipped")
                continue
            nran, rancols = read_eboss_ran(tracer, cap)
            r = analyse(f"{tracer}-{cap}", g['RA'], g['DEC'], g['Z'], g['NZ'],
                        g.get('WEIGHT_SYSTOT'), g.get('WEIGHT_CP'), g.get('WEIGHT_NOZ'),
                        g.get('WEIGHT_FKP'), zlo, zhi, nran, rancols)
            r['data_columns'] = cols
            r['z_eff'] = float(np.average(
                g['Z'][(g['Z'] > zlo) & (g['Z'] < zhi)]))
            r['growth_D_at_zeff'] = float(growth(r['z_eff']))
            out['tracers'][f"{tracer}|{cap}"] = r
            log(f"  {tracer:10s} {cap}: N={r['n_in_zrange']:7d}  "
                f"z[{r['z_min_cat']:.3f},{r['z_max_cat']:.3f}]  "
                f"area={r['area_deg2']:.0f}  V={r['shell_volume_Gpc3']:.3f} Gpc3  "
                f"Veff={r['Veff_FKP_Gpc3']:.3f}  "
                f"nbarV15={r['nbarV_R15_galweighted']:.2f}  "
                f"nbarV10={r['nbarV_R10_galweighted']:.2f}  "
                f"kappa={r.get('kappa_standard', float('nan')):.4f}  "
                f"ran/gal={r.get('random_ratio', float('nan')):.1f}")

    json.dump(out, open(f"{HERE}/eboss_stage0.json", 'w'), default=float, indent=1)
    log("\nwrote eboss_stage0.json")
    return out


if __name__ == '__main__':
    main()
