#!/usr/bin/env python3
"""
PLANCK / WMAP PLUMB LINE — analysis and gate register.

Reads the stage outputs of `planck_pilot.py` and produces every number that
`PLANCK_PILOT_RESULTS.md` reports, plus the VOID-condition checks and the
GATES.md discharge list.  Pre-registered in `PLANCK_PILOT_PREREG.md`
(+ AMENDMENT_1, AMENDMENT_2).

Scratchpad only.  No Lean, no Stance.lean, no audit, no `lake`.
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "planck_pilot")
sys.path.insert(0, HERE)
from planck_pilot import (TEMPLATE_ORDER, BS, OCCUPANCY_MIN, null_shape,  # noqa: E402
                          emp_p, gamma_p, collect, DYE_TAGS, DYE_F,
                          VALVE_EPS, BOUND_K)


def J(name):
    p = os.path.join(OUT, name)
    if not os.path.exists(p):
        return None
    with open(p) as f:
        return json.load(f)


CELLS = [f"{t}|b{b}" for t in TEMPLATE_ORDER for b in BS]


# ---------------------------------------------------------------------------
# The primary test (PREREG 7.2): X = # cells above their own matched p99,
# with the null of X obtained LEAVE-ONE-OUT over the surrogate ensemble.
# ---------------------------------------------------------------------------

def primary_test(data, ens, cells):
    """Returns X_data, the leave-one-out null of X, and the per-cell detail."""
    V = np.array([[r[c]["share"] for c in cells] for r in ens])      # (n, ncell)
    n = V.shape[0]
    d = np.array([data[c]["share"] for c in cells])
    p99 = np.percentile(V, 99, axis=0)
    x_data = int(np.sum(d > p99))
    x_null = np.empty(n, dtype=int)
    for j in range(n):
        others = np.delete(V, j, axis=0)
        x_null[j] = int(np.sum(V[j] > np.percentile(others, 99, axis=0)))
    detail = []
    for k, c in enumerate(cells):
        col = V[:, k]
        med = float(np.median(col))
        pv = emp_p(d[k], col)
        gp, ks = gamma_p(d[k], col)
        detail.append({
            "cell": c, "share": float(d[k]), "n": int(data[c]["n"]),
            "null_median": med, "null_p99": float(p99[k]),
            "ratio_to_median": float(d[k] / med) if med > 0 else None,
            "above_p99": bool(d[k] > p99[k]),
            "below_p01": bool(d[k] < np.percentile(col, 1)),
            "p_emp": pv, "p_gamma": gp, "ks_p_gammafit": ks,
            "tied_frac": data[c]["tied_frac"], "min_occ": data[c]["min_occ"],
            "shape": null_shape(col),
        })
    return {"X_data": x_data,
            "X_null_mean": float(x_null.mean()),
            "X_null_p95": float(np.percentile(x_null, 95)),
            "X_null_max": int(x_null.max()),
            "X_null_hist": np.bincount(x_null, minlength=len(cells) + 1).tolist(),
            "p_X": float((1.0 + np.sum(x_null >= x_data)) / (1.0 + n)),
            "pass": bool(x_data <= np.percentile(x_null, 95)),
            "n_cells": len(cells), "n_surr": n, "detail": detail}


def occupancy_void(data, ens, cells):
    """V1 — a cell with any histogram bin at or below OCCUPANCY_MIN is ungauged."""
    keep, drop = [], []
    for c in cells:
        occ = min([data[c]["min_occ"]] + [r[c]["min_occ"] for r in ens])
        (keep if occ > OCCUPANCY_MIN else drop).append((c, occ))
    return [c for c, _ in keep], drop


def floor_match_void(data, ens, cells):
    """V3 — the floor must be drawn at the same N_kept as the reading."""
    bad = []
    for c in cells:
        ns = {data[c]["n"]} | {r[c]["n"] for r in ens}
        if len(ns) != 1:
            bad.append((c, sorted(ns)))
    return bad


def null_construction_void(e1, e2, cells):
    """V6 — S1 and S2 floors must agree within their own ensemble scatters."""
    rows = []
    for c in cells:
        a, b = collect(e1, c), collect(e2, c)
        ma, mb = float(np.median(a)), float(np.median(b))
        sa = float(np.std(a, ddof=1) / np.sqrt(a.size))
        sb = float(np.std(b, ddof=1) / np.sqrt(b.size))
        sep = abs(ma - mb) / np.hypot(sa, sb) if (sa or sb) else np.inf
        rows.append({"cell": c, "s1_median": ma, "s2_median": mb,
                     "ratio": mb / ma if ma > 0 else None, "sigma_sep": float(sep)})
    return rows


def main():
    R = {}

    # ---------------- stage 1 / 1b : V8 ----------------------------------
    R["v8"] = J("stage1b_v8_amended.json")
    R["v8_legacy"] = J("stage1_surrogate_sanity.json")

    # ---------------- stage 2 : geometry ---------------------------------
    R["geometry"] = J("stage2_geometry.json")

    # ---------------- stage 5 : the data ---------------------------------
    D = J("stage5_data.json")
    if D is None:
        print("stage5 not run yet; analysing floors only", flush=True)

    for inst, ekey, dkey, ckey, cekey in (
            ("planck", "stage3_planck_s1.json", "planck",
             "planck_cons", "stage3_planck_cons_s1.json"),
            ("wmap", "stage3_wmap_s1.json", "wmap",
             "wmap_cons", "stage3_wmap_cons_s1.json")):
        e1 = J(ekey)
        if e1 is None:
            continue
        e2 = J(ekey.replace("_s1", "_s2"))
        block = {"n_s1": len(e1), "n_s2": len(e2) if e2 else 0}
        cells, dropped = (occupancy_void(D[dkey], e1, CELLS) if D
                          else (CELLS, []))
        block["v1_occupancy_dropped"] = dropped
        if D:
            block["v3_floor_mismatch"] = floor_match_void(D[dkey], e1, cells)
            block["primary"] = primary_test(D[dkey], e1, cells)
            # conservative-mask arm (V5 / G3)
            ec = J(cekey)
            if ec and dkey + "_cons" not in ("",):
                dc = D.get(ckey)
                if dc:
                    rows = []
                    for c in cells:
                        col = collect(ec, c)
                        med = float(np.median(col))
                        rows.append({"cell": c, "share": dc[c]["share"],
                                     "null_median": med,
                                     "ratio": dc[c]["share"] / med if med > 0 else None,
                                     "p_emp": emp_p(dc[c]["share"], col),
                                     "n": dc[c]["n"]})
                    block["conservative"] = rows
            # zero-threshold variant
            zt = D.get(dkey + "_zero_thresh")
            if zt:
                block["zero_threshold"] = {
                    c: {"share": zt[c]["share"],
                        "primary_share": D[dkey][c]["share"],
                        "cut_zero": zt[c]["cuts"][0],
                        "cut_median": D[dkey][c]["cuts"][0]}
                    for c in zt}
            # G1 LP pair-pinning, G8 IPF-vs-exact  (b=2 only)
            g1, g8 = [], []
            for t in TEMPLATE_ORDER:
                c = f"{t}|b2"
                r = D[dkey][c]
                if "lp_width" in r:
                    g1.append({"cell": c, "lp_width": r["lp_width"],
                               "share": r["share"],
                               "null_median": float(np.median(collect(e1, c))),
                               "width_over_nullmedian":
                                   r["lp_width"] / float(np.median(collect(e1, c)))})
                if "share_ipf" in r:
                    g8.append({"cell": c, "exact": r["share"], "ipf": r["share_ipf"],
                               "ipf_minus_exact": r["share_ipf"] - r["share"],
                               "ratio": (r["share_ipf"] / r["share"]
                                         if r["share"] > 0 else None),
                               "ipf_cert": r["ipf_cert"], "iters": r["ipf_iters"]})
            block["g1_pair_pinning"] = g1
            block["g8_ipf_vs_exact"] = g8
            # V7 IPF certificate at b>=3
            block["v7_ipf_cert_max"] = max(
                [D[dkey][f"{t}|b{b}"]["ipf_cert"]
                 for t in TEMPLATE_ORDER for b in (3, 4)])
        if e2:
            block["v6_null_construction"] = null_construction_void(e1, e2, cells)
        block["null_shape"] = {c: null_shape(collect(e1, c)) for c in CELLS}
        R[inst] = block

    # ---------------- S3 theory floor (Planck only) ----------------------
    e3 = J("stage3_planck_s3.json")
    if e3:
        e1 = J("stage3_planck_s1.json")
        R["planck_s3"] = {c: {"s3_median": float(np.median(collect(e3, c))),
                              "s1_median": float(np.median(collect(e1, c)))}
                          for c in CELLS}

    # ---------------- SMICA vs WMAP consistency (PREREG 7.3) -------------
    if D and "planck" in R and "wmap" in R:
        rows = []
        for c in CELLS:
            pd = {d["cell"]: d for d in R["planck"]["primary"]["detail"]}.get(c)
            wd = {d["cell"]: d for d in R["wmap"]["primary"]["detail"]}.get(c)
            if not (pd and wd):
                continue
            rp = pd["ratio_to_median"]
            rw = wd["ratio_to_median"]
            sp = pd["shape"]["std"] / pd["shape"]["median"] / np.sqrt(1)
            sw = wd["shape"]["std"] / wd["shape"]["median"] / np.sqrt(1)
            rows.append({"cell": c, "planck_ratio": rp, "wmap_ratio": rw,
                         "diff": rp - rw if (rp and rw) else None,
                         "sigma_quad": float(np.hypot(sp, sw)),
                         "n_sigma": float((rp - rw) / np.hypot(sp, sw))
                         if (rp and rw) else None})
        R["consistency"] = rows

    # ---------------- stage 4 arms ---------------------------------------
    fl = J("stage4_floor.json")
    dye = J("stage4_dye.json")
    if fl and dye:
        rows = []
        for arm in ("D0", "D1", "D2"):
            for f in DYE_F:
                for t in DYE_TAGS:
                    for b in (2, 3):
                        c = f"{t}|b{b}"
                        v = dye[f"{arm}_f{f}"][c]["share"]
                        base = dye["base"][c]["share"]
                        sh = fl[c]
                        rows.append({"arm": arm, "f": f, "cell": c,
                                     "share": v, "base_share": base,
                                     "floor_median": sh["median"],
                                     "floor_p99": sh["p99"],
                                     "over_floor_p99": bool(v > sh["p99"]),
                                     "ratio_to_floor_median":
                                         v / sh["median"] if sh["median"] > 0 else None,
                                     "identical_to_base": bool(v == base)})
        R["dye"] = rows
        # detection limit per arm: smallest f clearing p99 on ALL DYE_TAGS at b=2
        dl = {}
        for arm in ("D0", "D1", "D2"):
            hit = None
            for f in DYE_F:
                ok = all(dye[f"{arm}_f{f}"][f"{t}|b2"]["share"] > fl[f"{t}|b2"]["p99"]
                         for t in DYE_TAGS)
                if ok:
                    hit = f
                    break
            dl[arm] = hit
        R["dye_detection_limit_b2"] = dl

    bnd_s = J("stage4_boundary_surrogate.json")
    if bnd_s:
        R["boundary_surrogate"] = boundary_rows(bnd_s, fl)
    if D and "planck_boundary" in D:
        R["boundary_data"] = boundary_rows(D["planck_boundary"], fl)

    val = J("stage4_valve.json")
    if val and fl:
        rows = []
        for kind in ("sym", "asym"):
            for eps in VALVE_EPS:
                for t in DYE_TAGS:
                    c = f"{t}|b2"
                    s = val[f"{kind}_eps{eps}"][c]
                    rows.append({"kind": kind, "eps": eps, "cell": c,
                                 "median": s["median"], "p01": s["p01"],
                                 "p99": s["p99"],
                                 "base_floor_median": fl[c]["median"],
                                 "base_floor_p99": fl[c]["p99"],
                                 "ratio": s["median"] / fl[c]["median"]
                                 if fl[c]["median"] > 0 else None,
                                 "mints": bool(s["median"] > fl[c]["p99"])})
        R["valve"] = rows

    deg = J("stage6_degrade_floor.json")
    if deg and D and "planck_degrade" in D:
        rows = []
        for ns in ("nside512", "nside256"):
            dd = D["planck_degrade"][ns]
            for t in TEMPLATE_ORDER:
                for b in (2, 3):
                    c = f"{t}|b{b}"
                    if c not in deg[ns] or c not in dd["reading"]:
                        continue
                    sh = deg[ns][c]
                    rows.append({"nside": ns, "cell": c,
                                 "share": dd["reading"][c]["share"],
                                 "floor_median": sh["median"], "floor_p99": sh["p99"],
                                 "over_p99": bool(dd["reading"][c]["share"] > sh["p99"]),
                                 "ratio": dd["reading"][c]["share"] / sh["median"]
                                 if sh["median"] > 0 else None,
                                 "n": dd["reading"][c]["n"]})
        R["degrade"] = rows

    with open(os.path.join(OUT, "analysis.json"), "w") as f:
        json.dump(R, f, indent=1, default=float)
    print("wrote", os.path.join(OUT, "analysis.json"))
    summarise(R)
    return R


def boundary_rows(bnd, fl):
    rows = []
    for k in BOUND_K:
        for t in DYE_TAGS:
            for b in (2, 3):
                c = f"{t}|b{b}"
                base = bnd["base"][c]["share"]
                cl = bnd[f"clip_k{k}"][c]["share"]
                fo = bnd[f"fold_k{k}"][c]["share"]
                rows.append({
                    "k": k, "cell": c, "base": base, "clip": cl, "fold": fo,
                    "clip_ratio": cl / base if base > 0 else None,
                    "clip_identical": bool(cl == base),
                    "fold_ratio": fo / base if base > 0 else None,
                    "fold_delta": fo - base,
                    "flipped_frac": bnd[f"flipped_frac_k{k}"],
                    "floor_p99": fl[c]["p99"] if fl and c in fl else None,
                    "fold_over_floor_p99": (bool(fo > fl[c]["p99"])
                                            if fl and c in fl else None),
                })
    return rows


def summarise(R):
    print("\n" + "=" * 78)
    for inst in ("planck", "wmap"):
        if inst not in R or "primary" not in R.get(inst, {}):
            continue
        p = R[inst]["primary"]
        print(f"\n{inst.upper()}  n_surr={p['n_surr']}  cells={p['n_cells']}")
        print(f"  PRIMARY TEST  X_data={p['X_data']}  "
              f"null mean {p['X_null_mean']:.2f}  p95 {p['X_null_p95']:.1f}  "
              f"max {p['X_null_max']}  p(X)={p['p_X']:.4f}  "
              f"{'PASS' if p['pass'] else 'ALARM'}")
        print(f"  {'cell':<10} {'share':>12} {'null med':>12} {'ratio':>8} "
              f"{'p99':>12} {'p_emp':>8}")
        for d in p["detail"]:
            print(f"  {d['cell']:<10} {d['share']:>12.4e} {d['null_median']:>12.4e} "
                  f"{(d['ratio_to_median'] or 0):>8.3f} {d['null_p99']:>12.4e} "
                  f"{d['p_emp']:>8.4f}"
                  + ("  <<< ABOVE p99" if d["above_p99"] else ""))
    if "dye_detection_limit_b2" in R:
        print("\nDYE detection limit (smallest f clearing floor p99 on all three "
              f"templates, b=2): {R['dye_detection_limit_b2']}")


if __name__ == "__main__":
    main()
