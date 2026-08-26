#!/usr/bin/env python3
"""POST-HOC DIAGNOSTIC (labelled): does per-chain KE identity survive drives?
For each protocol: KE(c,k) at drive-start; corr across CHAINS at fixed k between
KE(:,k) and KE(:,k+m), averaged over k -- the shared heating trend drops out."""
import numpy as np, glob, json, importlib.util
_s = importlib.util.spec_from_file_location("cr", "chained_run.py")
cr = importlib.util.module_from_spec(_s); _s.loader.exec_module(cr)
out = {}
for pname, pdir in cr.PROTOS.items():
    x, v = cr.load_pos(pdir)
    n_er = x.shape[1] // cr.SEG
    KE = np.stack([v[:, 37*k+1]**2 for k in range(n_er)], axis=1)  # (N, n_er)
    row = {}
    for m in (1, 2, 4, 8, 16, 32):
        cs = [np.corrcoef(KE[:, k], KE[:, k+m])[0, 1] for k in range(0, n_er-m)]
        row[m] = (float(np.mean(cs)), float(np.std(cs)/np.sqrt(len(cs))))
    out[pname] = row
    print(pname + ": " + "  ".join(f"m={m}:{r[0]:+.3f}±{r[1]:.3f}" for m, r in row.items()))
    del x, v
json.dump(out, open("ke_persistence.json","w"), indent=2)
