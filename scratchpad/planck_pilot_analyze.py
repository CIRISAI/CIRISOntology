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


# ---------------------------------------------------------------------------
# CEILING FRACTION — the cross-campaign common denominator.
#
# AMENDMENT 5 SUPERSEDES AMENDMENT 4 HERE.  Amendment 4 audited this
# denominator's provenance and reported that the UPPER-BOUND direction was not
# mechanized anywhere in this repository.  That was true when it was written and
# it is now FALSE: `Core/ThirdCap.lean` (commit 8925843) proves it.
#
#   * `share_le_log_two` — share <= log 2 for EVERY probability state on three
#     binary slots, NO hypothesis on the pair marginals.  Machine-checked,
#     sorry-free and axiom-audited (Audit/AxiomAudit.lean).
#   * `share_max_eq_log_two` — attainment and the bound together: log 2 is the
#     EXACT maximum on three bits.  So the denominator is proved, not argued.
#   * `share_le_log_card_third` — share <= log(card of the third slot's
#     alphabet), GENERAL ALPHABETS.  So b = 3 and b = 4 have a machine-checked
#     cap of log b too; Amendment 4's "no cap mechanized for b > 2" is also
#     superseded.  (Stated against the THIRD slot, which is our case exactly:
#     all three slots carry the same alphabet.)
#   * `share_le_grouping_gaps` — the SHARP, data-computable ceiling
#     share <= H(pair) + H(remaining slot) - H(p), in all three orientations;
#     the honest per-table ceiling is their MINIMUM, and each is at most log 2.
#     This replaces the `3*log2 - max H(pair)` bound used before ThirdCap
#     existed, which was LOOSER than log 2 rather than tighter.
#
# Headline denominator: log b (log 2 at b = 2).  Machine-checked at every b in
# this pilot.  The sharp per-table ceiling is reported alongside, and it is the
# tighter of the two.
# ---------------------------------------------------------------------------

LN2 = float(np.log(2.0))


def cap_nats(b):
    """Returns (cap, machine_checked, source).  Machine-checked at every b used
    here, by Core/ThirdCap.lean."""
    if b == 2:
        return LN2, True, (
            "ln 2 = 0.6931472 nats (1 bit). MACHINE-CHECKED: share_le_log_two "
            "(Core/ThirdCap.lean) bounds EVERY three-binary-slot state with no "
            "hypothesis on the pair marginals, and share_max_eq_log_two cashes "
            "it with share_parity's attainment, so ln 2 is the EXACT maximum. "
            "Sorry-free and axiom-audited.")
    return float(np.log(b)), True, (
        f"ln {b} — MACHINE-CHECKED: share_le_log_card_third "
        f"(Core/ThirdCap.lean) gives share <= log(card of the third slot's "
        f"alphabet) for GENERAL alphabets; all three slots here carry {b} "
        f"levels. Note that at b>=3 the REFERENCE is the surrogate's own "
        f"reading and not zero (PREREG section 2), so this is a differential.")


def ceil_frac(share, b):
    cap, mc, _ = cap_nats(b)
    return (share / cap if cap > 0 else None), mc


def sharp_cap_of(rec, b):
    """The per-table ceiling of `share_le_grouping_gaps`, as recorded by
    planck_pilot.reading().  Falls back to None for records written before
    Amendment 5 added it."""
    return rec.get("sharp_cap")


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
        b = int(c.split("|b")[1])
        cap, mc, src = cap_nats(b)
        tight = sharp_cap_of(data[c], b)
        detail.append({
            "cell": c, "share": float(d[k]), "n": int(data[c]["n"]),
            "null_median": med, "null_p99": float(p99[k]),
            "ratio_to_median": float(d[k] / med) if med > 0 else None,
            "above_p99": bool(d[k] > p99[k]),
            "below_p01": bool(d[k] < np.percentile(col, 1)),
            "p_emp": pv, "p_gamma": gp, "ks_p_gammafit": ks,
            "tied_frac": data[c]["tied_frac"], "min_occ": data[c]["min_occ"],
            # --- ceiling fraction, the cross-campaign common denominator ---
            "cap_nats": cap, "cap_machine_checked": mc, "cap_source": src,
            "ceiling_frac_reading": float(d[k] / cap),
            "ceiling_frac_null_median": float(med / cap),
            "ceiling_frac_null_p95": float(np.percentile(col, 95) / cap),
            "ceiling_frac_null_p99": float(p99[k] / cap),
            "sharp_cap_nats": tight,
            "ceiling_frac_vs_sharp_cap": (float(d[k] / tight)
                                          if tight and tight > 0 else None),
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
            if ec:
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
        # Effective independent-triple count implied by the measured floor.
        # For a chi^2_1 null the share's median is 0.4549/(2 N_eff), so the ratio
        # N_nominal/N_eff says how far the correlated, with-replacement triple
        # draw sits from the 1/(2N) ideal.  This is a measurement of the floor,
        # not an assumption about it.
        neff = []
        for t in TEMPLATE_ORDER:
            c = f"{t}|b2"
            med = float(np.median(collect(e1, c)))
            nnom = int(e1[0][c]["n"])
            ne = 0.45494/(2*med) if med > 0 else None
            neff.append({"cell": c, "null_median": med, "n_nominal": nnom,
                         "n_eff_chi2_1": ne,
                         "n_nominal_over_n_eff": nnom/ne if ne else None,
                         "naive_floor_1_over_2N": 0.45494/(2*nnom)})
        block["effective_N"] = neff
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
    fls = J("stage4_floor_smoothed.json")
    dye = J("stage4_dye.json")
    if fl and dye:
        # AMENDMENT 3: each arm is judged against ITS OWN f=0 map and against the
        # floor family it lives in — raw for D0, 60'-smoothed for D1 and D2.
        FLOOR = {"D0": fl, "D1": fls or fl, "D2": fls or fl}
        rows = []
        for arm in ("D0", "D1", "D2"):
            for f in DYE_F:
                for t in DYE_TAGS:
                    for b in (2, 3):
                        c = f"{t}|b{b}"
                        v = dye[f"{arm}_f{f}"][c]["share"]
                        zero = dye[f"{arm}_f0.0"][c]["share"]
                        sh = FLOOR[arm][c]
                        rows.append({
                            "arm": arm, "f": f, "cell": c, "share": v,
                            "own_zero": zero,
                            "identical_to_own_zero": bool(v == zero),
                            "delta_over_zero": v - zero,
                            "floor_family": "smoothed" if arm != "D0" else "raw",
                            "floor_median": sh["median"], "floor_p99": sh["p99"],
                            "over_floor_p99": bool(v > sh["p99"]),
                            "ratio_to_floor_median":
                                v / sh["median"] if sh["median"] > 0 else None})
        R["dye"] = rows
        dl = {}
        for arm in ("D0", "D1", "D2"):
            hit = None
            for f in DYE_F:
                if f == 0.0:
                    continue
                if all(dye[f"{arm}_f{f}"][f"{t}|b2"]["share"] > FLOOR[arm][f"{t}|b2"]["p99"]
                       for t in DYE_TAGS):
                    hit = f
                    break
            dl[arm] = hit
        R["dye_detection_limit_b2"] = dl
        # FACT 3 check: D0 and D2 must be bit-identical to their own f=0 map for
        # every f at which u -> u + f(u^2-1) is still monotone on the sample.
        R["fact3"] = {
            arm: {str(f): all(dye[f"{arm}_f{f}"][f"{t}|b{b}"]["share"]
                              == dye[f"{arm}_f0.0"][f"{t}|b{b}"]["share"]
                              for t in DYE_TAGS for b in (2, 3))
                  for f in DYE_F}
            for arm in ("D0", "D1", "D2")}

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

    # ---------------- the ceiling-fraction headline ----------------------
    # For a theorem-pinned-zero target the deliverable is an UPPER LIMIT.  The
    # estimator is positively biased at a true share of zero (the finite-sample
    # floor ADDS), so the raw reading bounds the truth from above without any
    # further assumption: true share <= measured share, up to the null's own
    # scatter.  The sensitivity is the floor: nothing below the null's p95 could
    # have been distinguished from zero at this N.
    hl = {}
    for inst in ("planck", "wmap"):
        if inst not in R or "primary" not in R.get(inst, {}):
            continue
        det = R[inst]["primary"]["detail"]
        for b in BS:
            rows = [d for d in det if d["cell"].endswith(f"|b{b}")]
            if not rows:
                continue
            worst = max(rows, key=lambda d: d["ceiling_frac_reading"])
            cap, mc, src = cap_nats(b)
            hl[f"{inst}_b{b}"] = {
                "cap_nats": cap, "cap_machine_checked": mc, "cap_source": src,
                "n_cells": len(rows),
                "upper_limit_ceiling_frac": worst["ceiling_frac_reading"],
                "upper_limit_pct": 100.0 * worst["ceiling_frac_reading"],
                "attained_at": worst["cell"],
                "median_cell_ceiling_frac": float(np.median(
                    [d["ceiling_frac_reading"] for d in rows])),
                "sensitivity_ceiling_frac_null_p95": float(np.median(
                    [d["ceiling_frac_null_p95"] for d in rows])),
                "floor_ceiling_frac_null_median": float(np.median(
                    [d["ceiling_frac_null_median"] for d in rows])),
                "worst_cell_vs_sharp_cap": worst.get("ceiling_frac_vs_sharp_cap"),
            }
    R["ceiling_headline"] = hl

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
    if R.get("ceiling_headline"):
        print("\nCEILING FRACTION (share / machine-checked cap for the same slot "
              "count and alphabet)")
        for k, v in R["ceiling_headline"].items():
            mc = "machine-checked" if v["cap_machine_checked"] else "NOT machine-checked"
            print(f"  {k:<12} cap {v['cap_nats']:.6f} nats ({mc})")
            print(f"     UPPER LIMIT  {v['upper_limit_pct']:.4g}% of ceiling "
                  f"(worst of {v['n_cells']} cells, at {v['attained_at']})")
            print(f"     median cell  {100*v['median_cell_ceiling_frac']:.4g}%   "
                  f"floor {100*v['floor_ceiling_frac_null_median']:.4g}%   "
                  f"sensitivity (null p95) {100*v['sensitivity_ceiling_frac_null_p95']:.4g}%")


if __name__ == "__main__":
    main()
