#!/usr/bin/env python3
"""Stage 4 — UNBLIND.  PREREG order of operations steps 6-8."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import dalitz_share as ds
from scipy.optimize import linprog

rng = np.random.default_rng(20260727)
out = {}
d = dict(np.load("scratchpad/dalitz/kkk.npz"))
sig, side = ds.apply_windows(d, "KKK")


def slots(mask, Xq=0.5, Yq=0.5):
    sl, sh, q, pol = d["slow"][mask], d["shigh"][mask], d["q"][mask], d["pol"][mask]
    Xt, Yt = np.quantile(sl, Xq), np.quantile(sh, Yq)
    return ((sl > Xt).astype(np.int64), (sh > Yt).astype(np.int64),
            (q > 0).astype(np.int64), pol)


# ============================ PRIMARY =====================================
x, y, c, pol = slots(sig)
T = ds.table(x, y, c)
out["primary"] = {}
out["primary"]["cell_counts"] = T.astype(int).tolist()
occ = T.min()
out["primary"]["min_cell_count"] = int(occ)
out["primary"]["occupancy_gate_pass"] = bool(occ >= 1000)
out["primary"]["N"] = int(T.sum())
out["primary"]["N_plus"] = int(T[:, :, 1].sum())
out["primary"]["N_minus"] = int(T[:, :, 0].sum())

obs = ds.share_2x2x2(T)
null = ds.perm_null(x, y, c.copy(), 100000, rng)
out["primary"].update(ds.significance(obs, null))
lo, hi = ds.share_range_given_pairs(T)
out["primary"]["gate6a_share_range"] = [lo, hi]
out["primary"]["gate6a_range_width"] = hi - lo
out["primary"]["gate6a_ratio_to_measured"] = (hi - lo) / obs if obs > 0 else None
out["primary"]["gate6a_pass"] = bool((hi - lo) > 0.20 * obs)

# ============================ K3: magnet polarity =========================
out["polarity"] = {}
for name, pm in (("Down", pol == 0), ("Up", pol == 1)):
    Tp = ds.table(x[pm], y[pm], c[pm])
    o = ds.share_2x2x2(Tp)
    n = ds.perm_null(x[pm], y[pm], c[pm].copy(), 20000, rng)
    r = ds.significance(o, n); r["N"] = int(Tp.sum()); r["min_cell"] = int(Tp.min())
    out["polarity"][name] = r
zu, zd = out["polarity"]["Up"]["z"], out["polarity"]["Down"]["z"]
out["polarity"]["z_difference"] = abs(zu - zd) if (zu is not None and zd is not None) else None

# ============================ K4: sidebands ===============================
xs, ys, cs, _ = slots(side)
Ts = ds.table(xs, ys, cs)
os_ = ds.share_2x2x2(Ts)
ns = ds.perm_null(xs, ys, cs.copy(), 20000, rng)
out["sideband"] = ds.significance(os_, ns)
out["sideband"]["N"] = int(Ts.sum())
out["sideband"]["min_cell"] = int(Ts.min())

# ============================ 6b: two-resolution LP =======================
def lp_range(mask, b):
    sl, sh, q = d["slow"][mask], d["shigh"][mask], d["q"][mask]
    xb = np.clip(np.digitize(sl, np.quantile(sl, np.linspace(0, 1, b + 1)[1:-1])), 0, b - 1)
    yb = np.clip(np.digitize(sh, np.quantile(sh, np.linspace(0, 1, b + 1)[1:-1])), 0, b - 1)
    cb = (q > 0).astype(np.int64)
    n = len(sl)
    P = np.zeros((b, b, 2))
    np.add.at(P, (xb, yb, cb), 1.0)
    P /= n
    Xc = (np.arange(b) >= b // 2).astype(int)      # coarse-graining to b=2
    sigma = np.array([[[(-1.) ** (Xc[i] + Xc[j] + k) for k in (0, 1)]
                       for j in range(b)] for i in range(b)])
    nv = b * b * 2
    A, bb = [], []
    for i in range(b):                              # P(x_f, y_f)
        for j in range(b):
            r = np.zeros((b, b, 2)); r[i, j, :] = 1
            A.append(r.ravel()); bb.append(P[i, j, :].sum())
    for i in range(b):                              # P(x_f, c)
        for k in (0, 1):
            r = np.zeros((b, b, 2)); r[i, :, k] = 1
            A.append(r.ravel()); bb.append(P[i, :, k].sum())
    for j in range(b):                              # P(y_f, c)
        for k in (0, 1):
            r = np.zeros((b, b, 2)); r[:, j, k] = 1
            A.append(r.ravel()); bb.append(P[:, j, k].sum())
    A = np.array(A); bb = np.array(bb)
    cvec = sigma.ravel()
    res = {}
    for sense, sgn in (("min", 1.0), ("max", -1.0)):
        r = linprog(sgn * cvec, A_eq=A, b_eq=bb, bounds=(0, None), method="highs")
        res[sense] = float(sgn * r.fun) if r.success else None
    Tobs = float((P * sigma).sum())
    # coarse table and the share reachable over the LP's delta interval
    Pc = np.zeros((2, 2, 2))
    for i in range(b):
        for j in range(b):
            Pc[Xc[i], Xc[j], :] += P[i, j, :]
    shares = []
    for Tv in (res["min"], res["max"]):
        if Tv is None:
            continue
        delta = (Tv - Tobs) / 8.0
        q_ = Pc + delta * ds.SIGMA
        if (q_ >= -1e-12).all():
            shares.append(ds.share_2x2x2(np.clip(q_, 0, None)))
    return {"b": b, "T_obs": Tobs, "T_min": res["min"], "T_max": res["max"],
            "T_width": (res["max"] - res["min"]) if None not in res.values() else None,
            "share_endpoints": shares}


out["gate6b"] = [lp_range(sig, b) for b in (4, 8)]

# ============================ threshold stability scan ====================
scan = []
for Xq in (0.35, 0.425, 0.5, 0.575, 0.65):
    for Yq in (0.35, 0.425, 0.5, 0.575, 0.65):
        xx, yy, cc, _ = slots(sig, Xq, Yq)
        Tt = ds.table(xx, yy, cc)
        o = ds.share_2x2x2(Tt)
        n = ds.perm_null(xx, yy, cc.copy(), 4000, rng)
        scan.append({"Xq": Xq, "Yq": Yq, "share": o,
                     "z": float((o - np.median(n)) / np.std(n)),
                     "p": float((np.sum(n >= o) + 1) / (len(n) + 1)),
                     "min_cell": int(Tt.min())})
out["threshold_scan"] = scan
out["threshold_scan_summary"] = {
    "n_configs": len(scan), "max_z": max(s["z"] for s in scan),
    "min_z": min(s["z"] for s in scan),
    "n_above_3sigma": sum(1 for s in scan if s["z"] > 3),
    "n_occupancy_fail": sum(1 for s in scan if s["min_cell"] < 1000)}

json.dump(out, open("scratchpad/dalitz/stage4.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "threshold_scan"}, indent=1))
print("\nSCAN:", json.dumps(out["threshold_scan_summary"], indent=1))
