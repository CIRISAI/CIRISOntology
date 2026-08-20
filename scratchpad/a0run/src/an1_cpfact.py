"""AN1 — CP-FACT, the authoritative co-primary. sec 1.3, sec 7, sec 10.2.

**THIS STAGE OPENS THE OUTCOME COLUMN.** It runs first among the outcome-crossing
computations (sec 12 step 2 / freeze item 22). It reads no panel output at any point, so a
judge failure cannot be blamed for its result.

Table: ACTION3 x LANG_EN x OVR, 3 x 2 x 2, df = 2, on FRAME-CP (N = 2,662).
"""
from __future__ import annotations
import collections, json, math, sys
import numpy as np
from scipy.stats import chi2, ncx2
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad/a0run/src")
import a0lib as A
import a0stat as S

ACT = {"PONDER": 0, "SPEAK": 1, "TASK_COMPLETE": 2}


def mde(df, n_eff, alpha=0.01, power=0.80):
    """sec 15: 2*N_eff*I ~ noncentral chi2_df(lambda). Solve for the lambda giving
    `power` at `alpha`, then MDE = lambda/(2 N_eff)."""
    c = chi2.ppf(1 - alpha, df)
    lo, hi = 0.0, 200.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if ncx2.sf(c, df, mid) < power:
            lo = mid
        else:
            hi = mid
    lam = 0.5 * (lo + hi)
    return lam / (2.0 * n_eff), lam


def expected_no3way(T):
    m = S.maxent_table(T)
    return m * np.asarray(T).sum()


def v5_cells(T, bar=10.0):
    E = expected_no3way(T)
    return float(E.min()), bool(E.min() >= bar)


def quantile_bins(vals, k):
    v = np.asarray([x if x is not None else np.nan for x in vals], dtype=float)
    good = ~np.isnan(v)
    qs = np.nanquantile(v[good], np.linspace(0, 1, k + 1)[1:-1])
    out = np.digitize(v, qs)
    out[~good] = -1
    return out


def main():
    fr = A.rjson("A0_frames.json")
    rows_blind = {d["id"]: d for d in A.rjson("A0_rows.json")}
    # ---- THE OUTCOME COLUMN OPENS HERE --------------------------------------
    live = A.load_rows(allow_outcome=True)
    ovr = {r["t"]["id"]: int(bool(r["t"].get(A.OUTCOME))) for r in live}

    ids = fr["frames"]["FRAME-CP"]
    d = [rows_blind[i] for i in ids]
    a = np.array([ACT[x["action"]] for x in d])
    c = np.array([1 if x["lang"] == "en" else 0 for x in d])
    o = np.array([ovr[i] for i in ids])
    cl = [x["cluster"] for x in d]
    ver = [x["agent_version"] for x in d]
    N = len(ids)
    shape = (3, 2, 2)
    T = S.table_of(a, c, o, shape)
    p_ovr = float(o.mean())

    res = {"frame": "FRAME-CP", "N": N, "df": 2,
           "override_marginal_frame": p_ovr,
           "n_override": int(o.sum()), "n_non_override": int(N - o.sum()),
           "table_AxCxO": T.tolist(),
           "planning_value_note": "the corpus-wide 0.303 is a planning value only (sec 7.5); "
                                  "the frame-realised marginal above is what every gate uses"}

    # ---- V10: DEFF on the override, N_eff -----------------------------------
    rho, mbar, deff = S.deff_icc(o, cl)
    n_clusters = len({*cl})
    n_eff = N / deff
    res["V10"] = {"rho_override": rho, "mbar": mbar, "DEFF": deff,
                  "N_eff_from_DEFF": n_eff, "n_clusters": n_clusters,
                  "distinct_normalised_inputs": None,
                  "note": "CP-FACT uses no judge, so the distinct-input estimator does not "
                          "apply (sec 4); N_eff is N/DEFF, with the cluster count reported "
                          "as sec 15.1's worst case",
                  "N_eff_used": n_eff, "N_eff_worst_case": n_clusters}

    # ---- floors and ceilings (sec 7.3) --------------------------------------
    obs = S.share_general(T)
    sharp, sharp_all = S.sharp_ceiling(T)
    floor_analytic = 2.0 / (2.0 * n_eff)
    res["share"] = {"observed_nats": obs,
                    "pct_of_ln2": 100 * obs / S.LN2,
                    "sharp_ceiling_nats": sharp, "sharp_all_splits": sharp_all,
                    "pct_of_sharp": 100 * obs / sharp if sharp > 0 else None,
                    "ln2": S.LN2,
                    "floor_analytic_at_N_eff": floor_analytic,
                    "floor_analytic_at_N": 2.0 / (2.0 * N)}

    # ---- V16: power ---------------------------------------------------------
    m_eff, lam = mde(2, n_eff)
    _, max_share = S.share_interval(T)
    res["V16"] = {"MDE_at_N_eff": m_eff, "lambda": lam,
                  "max_achievable_share_given_margins": max_share,
                  "MDE_at_N": mde(2, N)[0],
                  "V16_UNDERPOWERED": bool(max_share < m_eff)}

    # ---- V8 / C2c: the LP certificate ---------------------------------------
    width = max_share
    res["C2c_V8"] = {"feasible_interval_nats": [0.0, width],
                     "width": width, "floor": floor_analytic,
                     "width_over_2xfloor": width / (2 * floor_analytic),
                     "V8_FOULED": bool(width <= 2 * floor_analytic)}

    # ---- the nulls (sec 7.4) -------------------------------------------------
    n1c = S.n1c(a, c, o, cl, ver, seed=A.SEED, shape=shape)
    res["N1c"] = {k: v for k, v in n1c.items() if k != "draws"}
    if n1c["draws"]:
        dr = np.array(n1c["draws"])
        res["N1c"].update({"mean": float(dr.mean()), "p99": float(np.percentile(dr, 99)),
                           "p": S.pct_p(obs, dr)})
    n1 = S.n1_exact(a, c, o, shape=shape)
    res["N1_exact"] = {k: v for k, v in n1.items() if k not in ("shares", "weights")}
    d2, drift = S.n2(a, c, o, cl, seed=A.SEED, ndraw=10000, shape=shape)
    d2 = np.array(d2)
    res["N2"] = {"mean": float(d2.mean()), "p99": float(np.percentile(d2, 99)),
                 "p": S.pct_p(obs, d2), "skew": float(((d2 - d2.mean()) ** 3).mean() /
                                                      max(d2.std() ** 3, 1e-300)),
                 "median": float(np.median(d2)),
                 "quantiles": {q: float(np.percentile(d2, q))
                               for q in (50, 90, 95, 99, 99.9)}}
    # margin drift the fallback must print (sec 7.4)
    ao_obs = T.sum(axis=1)[:, 1]; co_obs = T.sum(axis=0)[:, 1]
    ao_null = np.mean([x[0] for x in drift], axis=0)
    co_null = np.mean([x[1] for x in drift], axis=0)
    ao_sd = np.std([x[0] for x in drift], axis=0)
    co_sd = np.std([x[1] for x in drift], axis=0)
    res["N2_margin_drift"] = {
        "A_O_observed": ao_obs.tolist(), "A_O_null_mean": ao_null.tolist(),
        "A_O_null_sd": ao_sd.tolist(),
        "C_O_observed": co_obs.tolist(), "C_O_null_mean": co_null.tolist(),
        "C_O_null_sd": co_sd.tolist(),
        "note": "N2 does not condition on these margins; this is exactly what the "
                "NON-MIXING fallback stopped conditioning on (sec 7.4)"}
    d3 = np.array(S.n3(a, c, o, seed=A.SEED, ndraw=10000, shape=shape))
    res["N3"] = {"mean": float(d3.mean()), "p99": float(np.percentile(d3, 99)),
                 "p": S.pct_p(obs, d3)}

    verdict_null = "N1c" if not n1c["NON_MIXING"] else "N2 (N1c NON-MIXING fallback, sec 7.4)"
    vd = np.array(n1c["draws"]) if (not n1c["NON_MIXING"] and n1c["draws"]) else d2
    res["verdict_null"] = verdict_null
    p_verdict = S.pct_p(obs, vd)
    floor_emp = float(vd.mean())
    res["verdict"] = {"p": p_verdict, "null_mean_floor": floor_emp,
                      "obs_over_floor": obs / floor_emp if floor_emp > 0 else None}

    # ---- C2a ----------------------------------------------------------------
    c2a = (p_verdict < 0.01) and (obs >= 3 * floor_emp)
    res["C2a"] = {"p_lt_0.01": bool(p_verdict < 0.01), "p": p_verdict,
                  "obs_over_null_mean": obs / floor_emp if floor_emp > 0 else None,
                  "needs_>=3x": True, "C2a_PASS": bool(c2a)}

    # ---- C2b ----------------------------------------------------------------
    rng = np.random.default_rng(A.SEED)
    clusters = {}
    for i, k in enumerate(cl):
        clusters.setdefault(k, []).append(i)
    ckeys = list(clusters)
    syn = []
    frac_obs = obs / sharp if sharp > 0 else float("nan")
    for _ in range(10000):
        lat = rng.random(len(ckeys)) < p_ovr
        os_ = np.empty(N, dtype=int)
        for kk, key in enumerate(ckeys):
            os_[clusters[key]] = int(lat[kk])
        syn.append(S.share_general(S.table_of(a, c, os_, shape)))
    syn = np.array(syn)
    res["C2b_i_synthetic"] = {
        "construction": "cluster-level Bernoulli at the FRAME-realised override marginal, "
                        "constant within cluster, 10,000 draws (sec 7.5, referee M9)",
        "p_used": p_ovr, "mean": float(syn.mean()),
        "p99": float(np.percentile(syn, 99)),
        "obs": obs, "PASS": bool(obs > np.percentile(syn, 99))}

    def placebo(name, vals):
        v = np.array([1 if x is True else 0 for x in vals])
        if len(set(v.tolist())) < 2:
            return {"name": name, "UNGAUGED": True, "reason": "no spread"}
        Tp = S.table_of(a, c, v, shape)
        mn, ok = v5_cells(Tp)
        sh = S.share_general(Tp)
        shp, _ = S.sharp_ceiling(Tp)
        fr_ = sh / shp if shp > 0 else float("nan")
        return {"name": name, "spread": [int((v == 1).sum()), int((v == 0).sum())],
                "share_nats": sh, "sharp_ceiling": shp, "ceiling_fraction": fr_,
                "min_expected_cell": mn, "V5_PASS": ok, "UNGAUGED": not ok,
                "obs_fraction": frac_obs,
                "ratio_obs_over_placebo": (frac_obs / fr_) if fr_ and fr_ > 0 else None,
                "PASS_2x": bool(ok and fr_ > 0 and frac_obs >= 2 * fr_)}

    pl2 = placebo("pdma.has_conflicts", [x["has_conflicts"] for x in d])
    pl3 = placebo("idma.fragility_flag", [x["fragility"] for x in d])
    gauged = [p for p in (pl2, pl3) if not p.get("UNGAUGED")]
    c2b = res["C2b_i_synthetic"]["PASS"] and all(p["PASS_2x"] for p in gauged)
    res["C2b"] = {"i": res["C2b_i_synthetic"]["PASS"], "ii": pl2, "iii": pl3,
                  "n_gauged_placebos": len(gauged),
                  "rests_on_i_alone": len(gauged) == 0,
                  "C2b_PASS": bool(c2b)}

    # ---- C2d: the cellwise reading (sec 7.5) --------------------------------
    P = T / T.sum()
    M = S.maxent_table(T)
    with np.errstate(divide="ignore", invalid="ignore"):
        cellwise = np.where(P > 0, P * np.log(P / M), 0.0)
    I3 = cellwise.sum()
    Cshare = float(cellwise[:, :, 1].sum() / I3) if I3 > 0 else float("nan")
    c2d_null = []
    for os_ in (vd,):
        pass
    res["C2d"] = {"C": Cshare, "override_marginal": p_ovr,
                  "ratio": Cshare / p_ovr if p_ovr else None,
                  "CONCENTRATES_ON_CELLS": bool(Cshare >= 1.5 * p_ovr),
                  "I3_from_cellwise": float(I3),
                  "cellwise": cellwise.tolist()}

    # ---- epoch (sec 3.4, sec 7.5, V14) --------------------------------------
    ep = np.array([0 if v == "2.7.0-stable" else 1 for v in ver])
    per_epoch = {}
    for e, nm in ((0, "2.7.0-stable"), (1, "2.7.1-stable")):
        m = ep == e
        Te = S.table_of(a[m], c[m], o[m], shape)
        se = S.share_general(Te)
        sc, _ = S.sharp_ceiling(Te)
        per_epoch[nm] = {"N": int(m.sum()), "share": se, "sharp_ceiling": sc,
                         "ceiling_fraction": se / sc if sc > 0 else None,
                         "min_expected_cell": v5_cells(Te)[0]}
    Tep = S.table_of(a, ep, o, shape)
    sh_ep = S.share_general(Tep)
    res["epoch"] = {"pooled_share": obs, "per_epoch": per_epoch,
                    "V14_share_A_EPOCH_O": sh_ep, "V14_share_A_LANG_O": obs,
                    "V14_FIRES": bool(sh_ep > obs),
                    "note": "every three-way term involving EPOCH is a deployment-epoch "
                            "proxy and is uninterpretable as a context effect (sec 7.6)"}

    # ---- V13 volume proxy ---------------------------------------------------
    I_A = S.mi_plugin(a.tolist(), o.tolist())
    base = {}
    for nm, key in (("tokens_total", "tokens_total"), ("llm_calls", "llm_calls")):
        b = quantile_bins([x[key] for x in d], 3)
        base[nm] = {"MI": S.mi_plugin(b.tolist(), o.tolist()),
                    "levels": int(len(set(b.tolist())))}
    res["V13"] = {"I_A": I_A, "baselines": base,
                  "V13_PASS": bool(all(I_A >= 1.2 * v["MI"] for v in base.values())),
                  "consequence_if_fail": "CP-FACT's CONCENTRATES band is unavailable"}

    # ---- V5, V11 ------------------------------------------------------------
    mn, ok = v5_cells(T)
    res["V5"] = {"n_override": int(o.sum()), "n_non_override": int(N - o.sum()),
                 "min_expected_cell_primary": mn, "V5_PASS": bool(
                     ok and o.sum() >= 100 and (N - o.sum()) >= 100)}
    res["V11"] = {"scrub_corrupted_in_analysed_cells": 0.0,
                  "V11_PASS": True,
                  "note": "ACTION3 excludes the 30 scrub-corrupted actions by construction "
                          "and the language leg carries no scrub token"}

    # ---- band (sec 10.2) ----------------------------------------------------
    void = not res["V5"]["V5_PASS"]
    if res["C2c_V8"]["V8_FOULED"]:
        band = "FOULED"
    elif void:
        band = "VOID"
    elif res["V16"]["V16_UNDERPOWERED"]:
        band = "UNDERPOWERED"
    elif c2a and c2b:
        band = "CONCENTRATES" if res["V13"]["V13_PASS"] else \
            "CONCENTRATES-BAND-UNAVAILABLE (V13)"
    else:
        band = "DOES NOT CONCENTRATE"
    if res["epoch"]["V14_FIRES"] and band.startswith("CONCENTRATES"):
        band = "UNDERPOWERED (V14 epoch-confounded)"
    res["BAND"] = band

    # ---- sensitivity legs ---------------------------------------------------
    sens = {}
    tl = set(fr["frames"]["FRAME-TL"])
    m = np.array([i in tl for i in ids])
    Tm = S.table_of(a[m], c[m], o[m], shape)
    sh_m = S.share_general(Tm)
    scm, _ = S.sharp_ceiling(Tm)
    d2m, _ = S.n2([int(x) for x in a[m]], [int(x) for x in c[m]], [int(x) for x in o[m]],
                  [x for x, k in zip(cl, m) if k], seed=A.SEED, ndraw=2000, shape=shape)
    sens["FRAME-TL_matched_rows"] = {
        "N": int(m.sum()), "share": sh_m, "ceiling_fraction": sh_m / scm if scm else None,
        "p_N2": S.pct_p(sh_m, np.array(d2m)),
        "note": "sec 9.1 — the key comparison for the sec 10.3 mechanism reading"}

    lang4 = {l: i for i, l in enumerate(sorted({x["lang"] for x in d}))}
    c4 = np.array([lang4[x["lang"]] for x in d])
    T4 = S.table_of(a, c4, o, (3, len(lang4), 2))
    sh4 = S.share_general(T4)
    sc4, _ = S.sharp_ceiling(T4)
    d24, _ = S.n2(a, c4, o, cl, seed=A.SEED, ndraw=2000, shape=(3, len(lang4), 2))
    sens["ACTION3xLANG4xOVR"] = {
        "df": 2 * (len(lang4) - 1), "share": sh4,
        "ceiling_fraction": sh4 / sc4 if sc4 else None,
        "p_N2": S.pct_p(sh4, np.array(d24)),
        "min_expected_cell": v5_cells(T4)[0],
        "MDE_at_N_eff": mde(2 * (len(lang4) - 1), n_eff)[0],
        "levels": lang4}

    clean = np.array([not A.is_partial(x["task_id_raw"] or "") for x in d])
    if clean.sum() > 200:
        Tc = S.table_of(a[clean], c[clean], o[clean], shape)
        shc = S.share_general(Tc)
        d2c, _ = S.n2([int(x) for x in a[clean]], [int(x) for x in c[clean]],
                      [int(x) for x in o[clean]],
                      [x for x, k in zip(cl, clean) if k], seed=A.SEED, ndraw=2000,
                      shape=shape)
        sens["clean_task_id"] = {"N": int(clean.sum()), "share": shc,
                                 "p_N2": S.pct_p(shc, np.array(d2c))}
    res["sensitivity"] = sens
    res["crosscheck_2x2x2"] = S.crosscheck_report()

    A.wjson("A0_cpfact.json", res)
    print(json.dumps({k: v for k, v in res.items()
                      if k not in ("table_AxCxO", "C2d", "sensitivity")}, indent=1,
                     default=str))
    print("BAND:", band)
    A.marker("AN1_cpfact.done", {"BAND": band, "share": obs, "p": p_verdict})
    return 0


if __name__ == "__main__":
    sys.exit(main())
