#!/usr/bin/env python3
"""Control for the Stage-1 occupancy finding: run the IDENTICAL geometry code on BOSS DR12 and
compare to AMENDMENT_2's recorded numbers (SGC: mask 0.302, valid 0.250 at R=15, n_indep 33264).

If this reproduces, the eBOSS n_indep shortfall against the Stage-0 shell estimate is real
geometry and not a bug in the eBOSS adapter -- which is the only question worth asking before a
gate verdict is written down.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sky_realdata import log
import sky_stage2 as S2
from sky_stage6 import DataGeometry

out = {}
for cap in (sys.argv[1:] or ['SGC']):
    g = DataGeometry(cap, rs=[15.0, 10.0])
    out[cap] = dict(grid=list(g.g.N), ncell=g.g.ncell, n_ran_obj=g.n_ran_obj,
                    mask=float(g.mask.mean()),
                    frac_valid={str(R): float(g.ok[R].mean()) for R in (15.0, 10.0)},
                    n_indep={str(R): g.n_indep[R] for R in (15.0, 10.0)},
                    occ={f"{R}|{b}": g.occupancy(R, b) for R in (15.0, 10.0) for b in (4, 6, 8)})
    del g
json.dump(out, open('eboss_stage1_bosscheck.json', 'w'), default=float, indent=1)
log(json.dumps(out, indent=1, default=float))
