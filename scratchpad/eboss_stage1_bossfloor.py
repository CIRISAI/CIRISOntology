#!/usr/bin/env python3
"""The split-randoms floor on BOSS DR12, through the IDENTICAL code path used on eBOSS.

The split-randoms null carries the window, the selection function and the shot noise, and by
construction NO clustering.  Measured on both surveys at each survey's own galaxy count, it is a
direct, model-free comparison of how much structure each instrument's pipeline manufactures --
which is the question that decides whether eBOSS can confirm anything.
"""
import json, os, sys
import numpy as np
from astropy.io import fits
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sky_realdata import DATA, sky_to_cart, log
import sky_stage2 as S2
from sky_stage6 import DataGeometry, ZMIN, ZMAX
from eboss_stage1 import BS

out = {}
for cap in (sys.argv[1:] or ['SGC']):
    geo = DataGeometry(cap, rs=[15.0, 10.0])
    f = {'NGC': 'North', 'SGC': 'South'}[cap]
    with fits.open(f"{DATA}/random0_DR12v5_CMASSLOWZTOT_{f}.fits.gz") as h:
        d = h[1].data
        z = np.asarray(d['Z'], float)
        m = (z > ZMIN) & (z < ZMAX)
        pos = sky_to_cart(np.asarray(d['RA'], float)[m],
                          np.asarray(d['DEC'], float)[m], z[m]).astype(np.float32)
    with fits.open(f"{DATA}/galaxy_DR12v5_CMASSLOWZTOT_{f}.fits.gz") as h:
        zz = np.asarray(h[1].data['Z'], float)
        n_gal = int(((zz > ZMIN) & (zz < ZMAX)).sum())
    rng = np.random.default_rng(7)
    idx = np.nonzero(rng.random(len(pos)) < 0.5)[0]
    keep = rng.choice(idx, size=min(n_gal, idx.size), replace=False)
    out[cap] = dict(n_gal=n_gal, n_ran=len(pos),
                    res=geo.measure(pos[keep], np.ones(len(keep)), bs=BS, rs=[15.0, 10.0]))
    del geo, pos
    json.dump(out, open('eboss_stage1_bossfloor.json', 'w'), default=float, indent=1)
    for R in (15.0, 10.0):
        for b in BS:
            e = out[cap]['res'][R]['b'][b].get('folded', {})
            if e.get('occupancy_pass'):
                log(f"  BOSS {cap} R={R:.0f} b={b} folded split-randoms floor I = {e['I']:.6e}")
