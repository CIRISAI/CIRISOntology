"""AN3 — CP-KIND, the mechanism probe. sec 7.2, sec 10.2. FRAME-TL, 2 x 2 x 2, df = 1.

CP-KIND cannot fire the stance kill and cannot block it (sec 1.3). Both surface maps are run
and their disagreement is a quoted systematic (sec 7.2).
"""
from __future__ import annotations
import collections, json, math, sys
import numpy as np
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad/a0run/src")
import a0lib as A
import a0stat as S
from an1_cpfact import mde, v5_cells


def cramers_v(x, y):
    xs = sorted(set(x)); ys = sorted(set(y))
    T = np.zeros((len(xs), len(ys)))
    for a, b in zip(x, y):
        T[xs.index(a), ys.index(b)] += 1
    n = T.sum()
    E = np.outer(T.sum(1), T.sum(0)) / n
    chi2v = float(((T - E) ** 2 / np.where(E > 0, E, 1)).sum())
    r = min(len(xs), len(ys)) - 1
    return chi2v, float(math.sqrt(chi2v / (n * r))) if r > 0 and n > 0 else float("nan")


def analyse(a, c, o, cl, ver, d, label, gates_void):
    shape = (2, 2, 2)
    N = len(o)
    T = S.table_of(a, c, o, shape)
    obs = S.share_general(T)
    sharp, sharp_all = S.sharp_ceiling(T)
    rho, mbar, deff = S.deff_icc(np.array(o, dtype=float), cl)
    n_dist = len({x["bid"] for x in d})
    n_eff = min(N / deff, n_dist)
    floor = 1.0 / (2.0 * n_eff)
    m_eff, lam = mde(1, n_eff)
    _, mx = S.share_interval(T)
    p_ovr = float(np.mean(o))
    r = {"label": label, "N": N, "df": 1, "table": T.tolist(),
         "p_deep": float(np.mean(a)), "p_en": float(np.mean(c)),
         "override_marginal": p_ovr,
         "share_nats": obs, "pct_of_ln2": 100 * obs / S.LN2,
         "sharp_ceiling": sharp, "sharp_all_splits": sharp_all,
         "ceiling_fraction": obs / sharp if sharp > 0 else None,
         "V10": {"rho": rho, "DEFF": deff, "N_eff_DEFF": N / deff,
                 "distinct_inputs": n_dist, "N_eff_used": n_eff},
         "floor_analytic_at_N_eff": floor,
         "floor_median_0.2275_over_N_eff": 0.2275 / n_eff,
         "V16": {"MDE_at_N_eff": m_eff, "max_achievable_share": mx,
                 "V16_UNDERPOWERED": bool(mx < m_eff)},
         "V15": {"distinct_inputs": n_dist, "V15_PASS": n_dist >= 300},
         "V5": {"n_override": int(sum(o)), "n_non": int(N - sum(o)),
                "min_expected_cell": v5_cells(T)[0],
                "V5_PASS": bool(v5_cells(T)[1] and sum(o) >= 100 and N - sum(o) >= 100)},
         "C2c_V8": {"width": mx, "floor": floor,
                    "V8_FOULED": bool(mx <= 2 * floor)}}

    n1c = S.n1c(a, c, o, cl, ver, seed=A.SEED, shape=shape)
    r["N1c"] = {k: v for k, v in n1c.items() if k != "draws"}
    n1 = S.n1_exact(a, c, o, shape=shape)
    r["N1_exact"] = {k: v for k, v in n1.items() if k not in ("shares", "weights")}
    d2, drift = S.n2(a, c, o, cl, seed=A.SEED, ndraw=10000, shape=shape)
    d2 = np.array(d2)
    r["N2"] = {"mean": float(d2.mean()), "p99": float(np.percentile(d2, 99)),
               "median": float(np.median(d2)), "p": S.pct_p(obs, d2),
               "skew": float(((d2 - d2.mean()) ** 3).mean() / max(d2.std() ** 3, 1e-300))}
    d3 = np.array(S.n3(a, c, o, seed=A.SEED, ndraw=10000, shape=shape))
    r["N3"] = {"mean": float(d3.mean()), "p99": float(np.percentile(d3, 99)),
               "p": S.pct_p(obs, d3)}
    ao = T.sum(axis=1)[:, 1]; co = T.sum(axis=0)[:, 1]
    r["N2_margin_drift"] = {
        "A_O_observed": ao.tolist(),
        "A_O_null_mean": np.mean([x[0] for x in drift], axis=0).tolist(),
        "C_O_observed": co.tolist(),
        "C_O_null_mean": np.mean([x[1] for x in drift], axis=0).tolist()}
    vd = d2 if n1c["NON_MIXING"] else np.array(n1c["draws"])
    r["verdict_null"] = "N2 (N1c NON-MIXING fallback)" if n1c["NON_MIXING"] else "N1c"
    p = S.pct_p(obs, vd); fl = float(vd.mean())
    r["verdict"] = {"p": p, "null_mean_floor": fl,
                    "obs_over_floor": obs / fl if fl > 0 else None}
    r["C2a"] = {"C2a_PASS": bool(p < 0.01 and obs >= 3 * fl), "p": p,
                "obs_over_floor": obs / fl if fl > 0 else None}

    # C2b
    rng = np.random.default_rng(A.SEED)
    idx = {}
    for i, k in enumerate(cl):
        idx.setdefault(k, []).append(i)
    ck = list(idx)
    syn = []
    for _ in range(10000):
        lat = rng.random(len(ck)) < p_ovr
        os_ = np.empty(N, dtype=int)
        for kk2, key in enumerate(ck):
            os_[idx[key]] = int(lat[kk2])
        syn.append(S.share_general(S.table_of(a, c, os_, shape)))
    syn = np.array(syn)
    frac = obs / sharp if sharp > 0 else float("nan")

    def placebo(nm, vals):
        v = np.array([1 if x is True else 0 for x in vals])
        Tp = S.table_of(a, c, v, shape)
        mn, ok = v5_cells(Tp)
        sh = S.share_general(Tp); shp, _ = S.sharp_ceiling(Tp)
        f = sh / shp if shp > 0 else float("nan")
        return {"name": nm, "spread": [int((v == 1).sum()), int((v == 0).sum())],
                "share": sh, "ceiling_fraction": f, "min_expected_cell": mn,
                "V5_PASS": ok, "UNGAUGED": not ok,
                "ratio_obs_over_placebo": (frac / f) if f and f > 0 else None,
                "PASS_2x": bool(ok and f > 0 and frac >= 2 * f)}

    p2 = placebo("pdma.has_conflicts", [x["has_conflicts"] for x in d])
    p3 = placebo("idma.fragility_flag", [x["fragility"] for x in d])
    g = [x for x in (p2, p3) if not x["UNGAUGED"]]
    i_pass = bool(obs > np.percentile(syn, 99))
    r["C2b"] = {"i_synthetic": {"mean": float(syn.mean()),
                                "p99": float(np.percentile(syn, 99)), "PASS": i_pass},
                "ii": p2, "iii": p3, "n_gauged": len(g),
                "rests_on_i_alone": len(g) == 0,
                "C2b_PASS": bool(i_pass and all(x["PASS_2x"] for x in g))}

    # C2d
    P = T / T.sum(); M = S.maxent_table(T)
    with np.errstate(divide="ignore", invalid="ignore"):
        cw = np.where(P > 0, P * np.log(P / M), 0.0)
    I3 = cw.sum()
    C = float(cw[:, :, 1].sum() / I3) if I3 > 0 else float("nan")
    r["C2d"] = {"C": C, "ratio_to_marginal": C / p_ovr if p_ovr else None,
                "CONCENTRATES_ON_CELLS": bool(C >= 1.5 * p_ovr)}

    # epoch
    ep = np.array([0 if v == "2.7.0-stable" else 1 for v in ver])
    pe = {}
    for e, nm in ((0, "2.7.0-stable"), (1, "2.7.1-stable")):
        m = ep == e
        Te = S.table_of(np.asarray(a)[m], np.asarray(c)[m], np.asarray(o)[m], shape)
        se = S.share_general(Te); sc, _ = S.sharp_ceiling(Te)
        pe[nm] = {"N": int(m.sum()), "share": se,
                  "ceiling_fraction": se / sc if sc > 0 else None}
    sh_ep = S.share_general(S.table_of(a, ep, o, shape))
    r["epoch"] = {"per_epoch": pe, "V14_share_A_EPOCH_O": sh_ep,
                  "V14_FIRES": bool(sh_ep > obs)}

    # band
    if r["C2c_V8"]["V8_FOULED"]:
        band = "FOULED"
    elif gates_void:
        band = "VOID (" + ",".join(gates_void) + ")"
    elif not r["V5"]["V5_PASS"]:
        band = "VOID (V5)"
    elif r["V16"]["V16_UNDERPOWERED"] or not r["V15"]["V15_PASS"]:
        band = "UNDERPOWERED"
    elif r["C2b"]["rests_on_i_alone"]:
        band = "UNDERPOWERED (C2b rests on the synthetic alone, sec 7.5)"
    elif r["C2a"]["C2a_PASS"] and r["C2b"]["C2b_PASS"]:
        band = "CONCENTRATES"
    else:
        band = "DOES NOT CONCENTRATE"
    if r["epoch"]["V14_FIRES"] and band == "CONCENTRATES":
        band = "UNDERPOWERED (V14 epoch-confounded)"
    r["BAND"] = band
    return r


def main():
    fr = A.rjson("A0_frames.json")
    rows = {d["id"]: d for d in A.rjson("A0_rows.json")}
    kinds = {json.loads(l)["bid"]: json.loads(l)["majority"]
             for l in open(A.OUT / "A0_kinds.jsonl")}
    panel = A.rjson("A0_panel.json")
    col1 = A.rjson("A0_col1.json")
    live = A.load_rows(allow_outcome=True)
    ovr = {r["t"]["id"]: int(bool(r["t"].get(A.OUTCOME))) for r in live}

    ids = fr["frames"]["FRAME-TL"]
    d0 = [rows[i] for i in ids]
    kraw = [kinds.get(x["bid"]) for x in d0]

    gates_void = []
    mc2 = A.rjson("A0_mc2.json"); mc1 = A.rjson("A0_mc1.json")
    if not mc2["V1_PASS"]:
        gates_void.append("V1")
    if not mc1["V2_PASS"]:
        gates_void.append("V2")
    g = panel["gates"]["FRAME-TL"]
    if not g["V3_PASS"]:
        gates_void.append("V3")
    if not g["V4_PASS"]:
        gates_void.append("V4")
    if col1["V7"]["V7_VOID"]:
        gates_void.append("V7")
    if col1["V7b"]["V7b_VOID"]:
        gates_void.append("V7b")

    out = {"gates_voiding_CP_KIND": gates_void,
           "panel_gates_FRAME_TL": g,
           "kind_distribution_rows": dict(collections.Counter(kraw))}

    variants = {}
    for alt in (False, True):
        for rec_deep in (True, False):
            keep = [j for j in range(len(ids))
                    if kraw[j] not in (None, "NO FIT", "NO MAJORITY")
                    and (rec_deep or kraw[j] != "Record")]
            a = [A.is_deep(kraw[j], alt=alt) for j in keep]
            if any(x is None for x in a):
                continue
            c = [1 if d0[j]["lang"] == "en" else 0 for j in keep]
            o = [ovr[ids[j]] for j in keep]
            cl = [d0[j]["cluster"] for j in keep]
            ver = [d0[j]["agent_version"] for j in keep]
            dd = [d0[j] for j in keep]
            nm = ("Block.surfaceAlt" if alt else "Block.surface") + \
                 ("" if rec_deep else " (Record excluded)")
            variants[nm] = analyse(a, c, o, cl, ver, dd, nm, gates_void)
    out["variants"] = variants
    prim = variants["Block.surface"]
    out["AUTHORITATIVE_VARIANT_NOTE"] = (
        "CP-KIND is the mechanism probe (sec 1.3). It cannot fire the stance kill and "
        "cannot block it. The primary map is Block.surface; Block.surfaceAlt and the "
        "Record-excluded leg are pinned robustness legs and their disagreement is a quoted "
        "systematic (sec 7.2).")
    out["BAND_primary"] = prim["BAND"]
    out["surface_map_disagreement"] = {
        k: {"share": v["share_nats"], "p": v["verdict"]["p"], "BAND": v["BAND"],
            "p_deep": v["p_deep"]} for k, v in variants.items()}

    # ---- M8: the instrument-borne A-C association, against the recorded-fact bench
    keep = [j for j in range(len(ids)) if kraw[j] not in (None, "NO FIT", "NO MAJORITY")]
    kd = [str(A.is_deep(kraw[j])) for j in keep]
    ln = [str(1 if d0[j]["lang"] == "en" else 0) for j in keep]
    l4 = [d0[j]["lang"] for j in keep]
    act = [d0[j]["action"] for j in keep]
    chi_k, v_k = cramers_v(kd, ln)
    chi_a, v_a = cramers_v(act, ln)
    mi_k = S.mi_plugin(kd, ln); mi_a = S.mi_plugin(act, ln)
    chi_a4, v_a4 = cramers_v(act, l4)
    out["M8_instrument_borne_association"] = {
        "KIND_DEEP_x_LANG_EN": {"chi2": chi_k, "V": v_k, "MI_nats": mi_k},
        "recorded_fact_benchmark_selected_action_x_LANG_EN":
            {"chi2": chi_a, "V": v_a, "MI_nats": mi_a,
             "prereg_pinned": {"V": 0.118, "MI": 0.0071}},
        "selected_action_x_LANG4": {"chi2": chi_a4, "V": v_a4,
                                    "MI_nats": S.mi_plugin(act, l4),
                                    "prereg_pinned": {"V": 0.130, "MI": 0.0176}},
        "excess_ratio_MI": mi_k / mi_a if mi_a > 0 else None,
        "HEADLINE_SYSTEMATIC": bool(mi_a > 0 and mi_k > 3 * mi_a),
        "rule": "sec 4.1: a judge-borne association exceeding the recorded-fact association "
                "by more than 3x on MI is reported as an instrument-borne systematic in the "
                "headline, not a footnote"}

    # ---- sec 7.6(1): KIND5 x LANG4 x OVR, with the declared occupancy pooling
    k5 = [A.kind_m5(kraw[j]) for j in keep]
    lang4 = sorted({d0[j]["lang"] for j in keep})
    o5 = [ovr[ids[j]] for j in keep]
    pooled, levels = [], sorted(set(k5))
    cur = list(k5)
    poolinfo = []
    while True:
        lv = sorted(set(cur))
        T = S.table_of([lv.index(x) for x in cur],
                       [lang4.index(d0[j]["lang"]) for j in keep], o5,
                       (len(lv), len(lang4), 2))
        E = S.maxent_table(T) * T.sum()
        if E.min() >= 5 or len(lv) <= 3:
            break
        cnt = collections.Counter(cur)
        smallest = min((l for l in lv if l != "other"), key=lambda l: cnt[l], default=None)
        if smallest is None:
            break
        poolinfo.append({"pooled": smallest, "n": cnt[smallest]})
        cur = ["other" if x == smallest else x for x in cur]
    lv = sorted(set(cur))
    if len(lv) < 3:
        out["secondary_KIND5xLANG4"] = {"VOID": True,
                                        "reason": "pooling reduced the kind alphabet below "
                                                  "3 levels (sec 7.6(1))",
                                        "pooling": poolinfo}
    else:
        T = S.table_of([lv.index(x) for x in cur],
                       [lang4.index(d0[j]["lang"]) for j in keep], o5,
                       (len(lv), len(lang4), 2))
        sh = S.share_general(T)
        cl5 = [d0[j]["cluster"] for j in keep]
        dd, _ = S.n2([lv.index(x) for x in cur],
                     [lang4.index(d0[j]["lang"]) for j in keep], o5, cl5,
                     seed=A.SEED, ndraw=2000, shape=(len(lv), len(lang4), 2))
        rho, _, deff = S.deff_icc(np.array(o5, dtype=float), cl5)
        neff = min(len(o5) / deff, len({d0[j]["bid"] for j in keep}))
        dfx = (len(lv) - 1) * (len(lang4) - 1)
        out["secondary_KIND5xLANG4"] = {
            "levels": lv, "pooling": poolinfo, "df": dfx, "share": sh,
            "p_N2": S.pct_p(sh, np.array(dd)),
            "floor_analytic": dfx / (2 * neff), "N_eff": neff,
            "MDE": mde(dfx, neff)[0], "min_expected_cell": float(
                (S.maxent_table(T) * T.sum()).min()),
            "note": "not kill-bearing; Holm-corrected within its family"}

    # ---- sec 7.6(4): qa_question_num context leg (invisible to the judge)
    qn = [d0[j]["qa_question_num"] for j in keep]
    ok = [j2 for j2, q in enumerate(qn) if q is not None]
    if len(ok) > 300:
        aq = [A.is_deep(kraw[keep[j2]]) for j2 in ok]
        cq = [1 if qn[j2] <= 2 else 0 for j2 in ok]
        oq = [o5[j2] for j2 in ok]
        clq = [d0[keep[j2]]["cluster"] for j2 in ok]
        Tq = S.table_of(aq, cq, oq, (2, 2, 2))
        shq = S.share_general(Tq)
        dq, _ = S.n2(aq, cq, oq, clq, seed=A.SEED, ndraw=2000, shape=(2, 2, 2))
        out["secondary_qa_question_num"] = {
            "N": len(ok), "spread": [int(sum(cq)), int(len(cq) - sum(cq))],
            "share": shq, "p_N2": S.pct_p(shq, np.array(dq)),
            "label": "context variable INVISIBLE to the judge — cannot pass the sec 8.1 "
                     "manipulation check; a null here means nothing on its own (sec 7.6)"}

    A.wjson("A0_cpkind.json", out)
    print(json.dumps({"BAND_primary": out["BAND_primary"],
                      "gates_voiding": gates_void,
                      "surface_map_disagreement": out["surface_map_disagreement"],
                      "M8": out["M8_instrument_borne_association"]}, indent=1, default=str))
    A.marker("AN3_cpkind.done", {"BAND": out["BAND_primary"]})
    return 0


if __name__ == "__main__":
    sys.exit(main())
