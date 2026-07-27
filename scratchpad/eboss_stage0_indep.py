#!/usr/bin/env python3
"""
eboss_stage0_indep.py -- STAGE 0, part 3: HOW INDEPENDENT IS THE CONFIRMATION SAMPLE, and what
significance does it project to.

The mission is an INDEPENDENT-SAMPLE confirmation.  "Independent" is a claim about the volume,
not about the catalogue filename, and eBOSS overlaps BOSS on the sky and in redshift.  This
measures the overlap rather than asserting it.  Metadata and positions only.

Writes eboss_stage0_indep.json.
"""
import json
import os
import sys

import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import chi, growth, log                       # noqa: E402

DATA = os.environ.get('SKYDATA', '/home/emoore/skydata')
EB = f"{DATA}/eboss"
DEG2 = (180.0 / np.pi) ** 2
BOSS_Z = (0.2, 0.75)
ZR = {'LRG': (0.6, 1.0), 'ELG': (0.6, 1.1), 'QSO': (0.8, 2.2), 'LRGpCMASS': (0.6, 1.0)}

# Priors of record: the refuter's CORRECTED significances, not the campaign's published ones.
BOSS_PRIOR = {('NGC', 15, 4): 6.0, ('NGC', 15, 6): 9.7,
              ('NGC', 10, 4): 20.9, ('NGC', 10, 6): 26.3, ('NGC', 10, 8): 29.8}


def cells(ra, dec, nra=720, ndec=360):
    s = np.sin(np.deg2rad(dec))
    i = np.clip(((ra % 360.0) / 360.0 * nra).astype(np.int64), 0, nra - 1)
    j = np.clip(((s + 1.0) / 2.0 * ndec).astype(np.int64), 0, ndec - 1)
    return set(np.unique(i * ndec + j).tolist()), (2 * np.pi / nra) * (2.0 / ndec) * DEG2


def radial_overlap(zlo, zhi):
    """Fraction of the comoving radial volume of [zlo,zhi] that lies inside BOSS's [0.2,0.75]."""
    a, b = max(zlo, BOSS_Z[0]), min(zhi, BOSS_Z[1])
    if b <= a:
        return 0.0
    return (chi(b) ** 3 - chi(a) ** 3) / (chi(zhi) ** 3 - chi(zlo) ** 3)


def main():
    s0 = json.load(open(f"{HERE}/eboss_stage0.json"))
    out = {'boss_z': BOSS_Z, 'samples': {}}

    boss = {}
    for cap, f in (('NGC', 'North'), ('SGC', 'South')):
        with fits.open(f"{DATA}/galaxy_DR12v5_CMASSLOWZTOT_{f}.fits.gz") as h:
            d = h[1].data
            z = np.asarray(d['Z'], float)
            m = (z > BOSS_Z[0]) & (z < BOSS_Z[1])
            boss[cap] = cells(np.asarray(d['RA'], float)[m],
                              np.asarray(d['DEC'], float)[m])[0]
    boss_all = boss['NGC'] | boss['SGC']
    log("=" * 100)
    log("STAGE 0 part 3 -- independence of the confirmation volume, MEASURED")
    log("=" * 100)
    log(f"  BOSS DR12 occupies {len(boss_all)} coarse sky cells "
        f"({len(boss_all) * cells(np.array([0.]), np.array([0.]))[1]:.0f} deg^2)")
    log("")
    log(f"  {'sample':16s} {'sky overlap':>12s} {'radial overlap':>15s} "
        f"{'VOLUME SHARED':>14s}   z_eff  D(z_eff)")
    for tracer in ('LRG', 'ELG', 'QSO', 'LRGpCMASS'):
        zlo, zhi = ZR[tracer]
        fr = radial_overlap(zlo, zhi)
        for cap in ('NGC', 'SGC'):
            f = f"{EB}/eBOSS_{tracer}_clustering_random-{cap}-vDR16.fits"
            if not os.path.exists(f):
                f = f"{EB}/eBOSS_{tracer}_clustering_data-{cap}-vDR16.fits"
            with fits.open(f, memmap=True) as h:
                d = h[1].data
                z = np.asarray(d['Z'], float)
                m = (z > zlo) & (z < zhi)
                c, ca = cells(np.asarray(d['RA'], float)[m],
                              np.asarray(d['DEC'], float)[m])
            sky = len(c & boss_all) / len(c)
            key = f"{tracer}|{cap}"
            r = s0['tracers'][key]
            out['samples'][key] = dict(sky_overlap_frac=sky, radial_overlap_frac=fr,
                                       volume_shared_frac=sky * fr,
                                       z_eff=r['z_eff'], D=r['growth_D_at_zeff'])
            log(f"  {key:16s} {100*sky:11.1f}% {100*fr:14.1f}% {100*sky*fr:13.1f}%   "
                f"{r['z_eff']:.3f}  {r['growth_D_at_zeff']:.4f}")

    # ---------------- projected significance
    # z ~ signal / sigma.  Per realisation sigma of the target scales as 1/sqrt(n_indep); the
    # signal amplitude scales as D^0.82 (SKY_FORECAST_RESULTS F3, measured).  So
    #     z_new / z_BOSS = (D_new/D_BOSS)^0.82 * sqrt(n_indep_new / n_indep_BOSS).
    # WHAT THIS SCALING DOES NOT CARRY, stated rather than buried:
    #   - tracer BIAS.  eBOSS ELG (b~1.4) and LRG (b~2.3) differ from CMASS (b~2.0), and the
    #     order-3 sector's dependence on bias is NOT measured by this campaign.  No bias factor
    #     is applied and the projection is therefore a scaling, not a forecast.
    #   - the floor being a larger FRACTION of signal, which raises the systematic but does not
    #     by itself move this ratio.
    #   - any eBOSS-specific systematic, which is the whole reason the gates exist.
    log("")
    log("  PROJECTED SIGNIFICANCE by the D^0.82 * sqrt(n_indep) scaling (bias NOT carried):")
    bref = s0['boss_reference']
    D_boss = float(growth(0.45))
    proj = {}
    log(f"  {'sample':16s} {'R':>3s} {'b':>2s} {'BOSS z':>7s} {'n_ind ratio':>12s} "
        f"{'D ratio^.82':>12s} {'PROJECTED z':>12s}")
    for (cap, R, b), zb in sorted(BOSS_PRIOR.items()):
        nb = bref[cap][f'n_indep_shell_R{R}']
        for tracer in ('LRG', 'ELG', 'LRGpCMASS'):
            key = f"{tracer}|{cap}"
            r = s0['tracers'][key]
            occ = r[f'occ_R{R}_b{b}']
            if occ <= 100:
                continue
            nr = r[f'n_indep_shell_R{R}'] / nb
            dr = (r['growth_D_at_zeff'] / D_boss) ** 0.82
            zp = zb * np.sqrt(nr) * dr
            proj[f"{key}|{R}|{b}"] = dict(boss_z=zb, n_indep_ratio=nr, D_ratio=dr,
                                          projected_z=zp, occupancy=occ)
            log(f"  {key:16s} {R:3d} {b:2d} {zb:7.1f} {nr:12.3f} {dr:12.3f} {zp:12.1f}")
    out['projection'] = proj
    out['D_boss_zeff0.45'] = D_boss
    json.dump(out, open(f"{HERE}/eboss_stage0_indep.json", 'w'), default=float, indent=1)
    log("\nwrote eboss_stage0_indep.json")


if __name__ == '__main__':
    main()
