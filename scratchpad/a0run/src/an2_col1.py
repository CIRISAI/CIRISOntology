"""AN2 — column 1, the matched-alphabet information contest. sec 10.1, on FRAME-H.

sec 12 step 9 order: the leak-only arm and V7 first, then V6 and V12, then Delta and its CI.
V7b (the adversarial probe's AUC) is discharged here too, before any band is read.

Floors for every MI are N2 cluster permutations, per AMENDMENTS A0-NOTE-4.
"""
from __future__ import annotations
import collections, json, math, sys
import numpy as np
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad/a0run/src")
import a0lib as A
import a0stat as S

NDRAW = 10000


def cluster_perm_mi(pred, o, cl, seed=A.SEED, ndraw=NDRAW):
    """N2: permute the override vectors among whole canonical task_id clusters of
    equal size (AMENDMENTS A0-NOTE-4)."""
    rng = np.random.default_rng(seed)
    idx = {}
    for i, k in enumerate(cl):
        idx.setdefault(k, []).append(i)
    keys = list(idx)
    vecs = [np.array([o[i] for i in idx[k]]) for k in keys]
    by_size = {}
    for i, v in enumerate(vecs):
        by_size.setdefault(len(v), []).append(i)
    o2 = np.empty(len(o), dtype=int)
    out = []
    for _ in range(ndraw):
        for s, grp in by_size.items():
            perm = rng.permutation(len(grp))
            for gi, pi in zip(grp, perm):
                o2[idx[keys[gi]]] = vecs[grp[pi]]
        out.append(S.mi_plugin(pred, o2.tolist()))
    return np.array(out)


def legacy_m5(e, c):
    if e is None or c is None:
        return None
    m = round(min(0.4 - e, c - 0.6), 9)          # sec 10.1 float hygiene
    if m < 0:
        return "L0-failed"
    if m <= 0.12:
        return "L1-hairline"
    if m == 0.15:
        return "L2-mode"
    if m <= 0.25:
        return "L3-middling"
    return "L4-wide"


def qbins(vals, k):
    v = np.array([np.nan if x is None else float(x) for x in vals])
    good = ~np.isnan(v)
    qs = np.nanquantile(v[good], np.linspace(0, 1, k + 1)[1:-1])
    b = np.digitize(v, qs).astype(int)
    b[~good] = -1
    return b.tolist()


def main():
    fr = A.rjson("A0_frames.json")
    rows = {d["id"]: d for d in A.rjson("A0_rows.json")}
    kinds = {json.loads(l)["bid"]: json.loads(l)["majority"]
             for l in open(A.OUT / "A0_kinds.jsonl")}
    live = A.load_rows(allow_outcome=True)
    ovr = {r["t"]["id"]: int(bool(r["t"].get(A.OUTCOME))) for r in live}
    res = {}

    # ---- V7b: the adversarial leak probe's AUC (sec 6.5) --------------------
    ps = {r["bid"]: r for r in A.rjson("A0_probe_scores.json")["scores"]}
    v7b = {}
    for fname in ("FRAME-T", "FRAME-H", "FRAME-TL"):
        ids = fr["frames"][fname]
        blk = collections.defaultdict(list)
        for i in ids:
            blk[rows[i]["bid"]].append(ovr[i])
        sc, lab, mixed = [], [], 0
        for b, ovs in blk.items():
            if ps.get(b, {}).get("score") is None:
                continue
            rate = float(np.mean(ovs))
            if 0 < rate < 1:
                mixed += 1
            sc.append(ps[b]["score"]); lab.append(1 if rate >= 0.5 else 0)
        auc, tie = S.auc_tie_corrected(sc, lab)
        rsc = [ps[rows[i]["bid"]]["score"] for i in ids
               if ps.get(rows[i]["bid"], {}).get("score") is not None]
        rlab = [ovr[i] for i in ids
                if ps.get(rows[i]["bid"], {}).get("score") is not None]
        rauc, rtie = S.auc_tie_corrected(rsc, rlab)
        se = 0.5 / math.sqrt(min(sum(lab), len(lab) - sum(lab))) if lab else float("nan")
        v7b[fname] = {"n_blocks_scored": len(sc), "mixed_blocks": mixed,
                      "AUC_distinct_input": auc, "tie_fraction": tie,
                      "AUC_row_basis": rauc, "tie_fraction_rows": rtie,
                      "n_pos_blocks": int(sum(lab)), "n_neg_blocks": int(len(lab) - sum(lab))}
    primary_auc = v7b["FRAME-T"]["AUC_distinct_input"]
    cues = collections.Counter()
    for r in A.rjson("A0_probe_scores.json")["scores"]:
        for c in r.get("cues", []):
            cues[c.strip().lower()[:80]] += 1
    v7b["V7b_VOID"] = bool(primary_auc >= 0.60)
    v7b["band"] = ("VOID-BY-LEAKAGE (AUC >= 0.60)" if primary_auc >= 0.60 else
                   "measured residual leak; column 1's SUPERIOR band unavailable"
                   if primary_auc >= 0.539 else
                   "no leak resolved above the probe's own detection limit of 0.539 "
                   "(sec 6.5: this is NOT 'no leak')")
    v7b["top_cues"] = cues.most_common(15)
    res["V7b"] = v7b

    # ---- the column-1 frame -------------------------------------------------
    ids = fr["frames"]["FRAME-H"]
    d = [rows[i] for i in ids]
    o = [ovr[i] for i in ids]
    cl = [x["cluster"] for x in d]
    N = len(ids)
    res["frame"] = {"name": "FRAME-H", "N": N, "n_clusters": len({*cl}),
                    "distinct_inputs": len({x["bid"] for x in d}),
                    "override_marginal": float(np.mean(o)),
                    "conditioning": "FRAME-H is exactly the text-tier rows where the entropy "
                                    "faculty did not fire (sec 3.10); column 1's contest "
                                    "happens downstream of one of the four consciences it "
                                    "argues about"}

    rho, mbar, deff = S.deff_icc(np.array(o, dtype=float), cl)
    n_eff = min(N / deff, len({x["bid"] for x in d}))
    res["V10"] = {"rho": rho, "DEFF": deff, "N_eff_DEFF": N / deff,
                  "distinct_inputs": len({x["bid"] for x in d}),
                  "N_eff_used": n_eff}

    # ---- the two arms (sec 10.1) -------------------------------------------
    LG = [legacy_m5(x["entropy_score"], x["coherence_score"]) for x in d]
    KD = [A.kind_m5(kinds.get(x["bid"])) for x in d]
    kraw = [kinds.get(x["bid"]) for x in d]
    excl = [i for i in range(N) if kraw[i] in (None, "NO FIT", "NO MAJORITY")
            or KD[i] is None or LG[i] is None]
    res["exclusions"] = {"n_excluded": len(excl),
                         "reasons": dict(collections.Counter(
                             (kraw[i] if kraw[i] in (None, "NO FIT", "NO MAJORITY")
                              else "other") for i in excl))}
    keep = [i for i in range(N) if i not in set(excl)]
    kc = collections.Counter(KD[i] for i in keep)
    res["KIND_M5_realised"] = dict(kc)
    res["LEGACY_M5_realised"] = dict(collections.Counter(LG[i] for i in keep))
    small = [lvl for lvl, n in kc.items() if n < 20]
    dropped = [i for i in keep if KD[i] in small]
    keep = [i for i in keep if KD[i] not in small]
    res["under20_kind_levels_dropped"] = {"levels": small, "rows_dropped": len(dropped),
                                          "rule": "sec 10.1: an empty or under-20 KIND-M5 "
                                                  "level is DROPPED from BOTH arms, never "
                                                  "merged (dropping is outcome-blind)"}
    kk = [KD[i] for i in keep]; ll = [LG[i] for i in keep]
    oo = [o[i] for i in keep]; cc = [cl[i] for i in keep]
    res["matched_contest"] = {"N": len(keep), "kind_levels": len(set(kk)),
                              "legacy_levels": len(set(ll)),
                              "df_kind": len(set(kk)) - 1, "df_legacy": len(set(ll)) - 1}

    # ---- leak-only arm and V7 (sec 6.4) — FIRST, per sec 12 step 9 ----------
    leak = [f"{min(d[i]['s1_removed'],2)}|{int(bool(d[i]['s2_hit']))}" for i in keep]
    I_leak_raw = S.mi_plugin(leak, oo)
    I_kind_raw = S.mi_plugin(kk, oo)
    I_leg_raw = S.mi_plugin(ll, oo)
    fl_leak = cluster_perm_mi(leak, oo, cc)
    fl_kind = cluster_perm_mi(kk, oo, cc)
    fl_leg = cluster_perm_mi(ll, oo, cc)
    I_leak = I_leak_raw - fl_leak.mean()
    I_kind = I_kind_raw - fl_kind.mean()
    I_leg = I_leg_raw - fl_leg.mean()
    res["V7"] = {"leak_levels": dict(collections.Counter(leak)),
                 "I_leak_raw": I_leak_raw, "I_kind_raw": I_kind_raw,
                 "I_leak_floor": float(fl_leak.mean()), "I_kind_floor": float(fl_kind.mean()),
                 "I_leak_subtracted": I_leak, "I_kind_subtracted": I_kind,
                 "ratio_subtracted": (I_leak / I_kind) if I_kind > 0 else float("inf"),
                 "ratio_raw": I_leak_raw / I_kind_raw if I_kind_raw > 0 else float("inf"),
                 "V7_VOID": bool(I_kind <= 0 or I_leak >= 0.5 * I_kind),
                 "gate": "VOID-BY-LEAKAGE if I_leak >= 0.5 * I_kind (floor-subtracted, "
                         "A0-NOTE-4)",
                 "bounds_only": "sec 6.4 bounds THE MARKER CHANNEL and nothing else; it is "
                                "structurally blind to a paraphrase that triggers no removal"}

    # ---- V6 and V12 ---------------------------------------------------------
    res["V6"] = {"I_L_raw": I_leg_raw, "I_L_subtracted": I_leg,
                 "null_p95": float(np.percentile(fl_leg, 95)),
                 "V6_PASS": bool(I_leg_raw > np.percentile(fl_leg, 95)),
                 "consequence_if_fail": "column 1 VOID-BY-NO-BASELINE"}
    vol = {}
    for nm, key in (("tokens_total", "tokens_total"), ("llm_calls", "llm_calls")):
        b = qbins([d[i][key] for i in keep], len(set(kk)))
        raw = S.mi_plugin([str(x) for x in b], oo)
        f = cluster_perm_mi([str(x) for x in b], oo, cc, ndraw=2000)
        vol[nm] = {"MI_raw": raw, "MI_subtracted": raw - float(f.mean()),
                   "levels": len(set(b))}
    res["V12"] = {"I_K_subtracted": I_kind, "baselines": vol,
                  "V12_PASS": bool(all(I_kind >= 1.2 * max(v["MI_subtracted"], 0)
                                       for v in vol.values())),
                  "consequence_if_fail": "column 1's SUPERIOR band is unavailable"}

    # ---- Delta and its cluster bootstrap CI ---------------------------------
    delta = I_kind - I_leg
    rng = np.random.default_rng(A.SEED)
    byc = {}
    for j, k in enumerate(cc):
        byc.setdefault(k, []).append(j)
    ckeys = list(byc)
    boot = []
    for _ in range(NDRAW):
        pick = rng.integers(0, len(ckeys), len(ckeys))
        sel = [j for t in pick for j in byc[ckeys[t]]]
        bk = [kk[j] for j in sel]; bl = [ll[j] for j in sel]; bo = [oo[j] for j in sel]
        boot.append(S.mi_plugin(bk, bo) - S.mi_plugin(bl, bo))
    boot = np.array(boot)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    # the bootstrap is of the RAW difference; re-centre on the floor-subtracted Delta
    shift = delta - (I_kind_raw - I_leg_raw)
    lo, hi = float(lo + shift), float(hi + shift)
    half = max(abs(hi - delta), abs(delta - lo))
    res["contest"] = {"I_K": I_kind, "I_L": I_leg, "Delta": delta,
                      "CI95": [lo, hi], "half_width": half,
                      "half_width_rule": "max(|hi-Delta|,|Delta-lo|), the larger arm (m10)",
                      "n_bootstrap": NDRAW}

    # ---- bands (sec 10.1, sec 15.3) ----------------------------------------
    from scipy.stats import chi2 as _c
    dfk = len(set(kk)) - 1
    v6_admit = _c.ppf(0.95, dfk) / (2 * n_eff)
    E_I0 = dfk / (2 * n_eff)
    proj_half = 1.96 * math.sqrt(2) * math.sqrt(2 * dfk) / (2 * n_eff)
    # sec 15.3: PARITY needs I_L >= projected half-width / 0.20 (= 5x the half-width;
    # reproduces the prereg's 0.03126 at N_eff = 627 from its 0.00625)
    parity_min_IL = proj_half / 0.20
    res["power"] = {"df": dfk, "N_eff": n_eff, "E_I_under_null": E_I0,
                    "V6_admits_I_L_above": v6_admit,
                    "projected_CI_half_width": proj_half,
                    "PARITY_needs_I_L_at_least": parity_min_IL,
                    "dead_window": [v6_admit, parity_min_IL]}
    rel = 0.20 * I_leg
    band = None
    if not res["V6"]["V6_PASS"]:
        band = "VOID-BY-NO-BASELINE"
    elif res["V7"]["V7_VOID"] or res["V7b"]["V7b_VOID"]:
        band = "VOID-BY-LEAKAGE"
    elif I_leg < parity_min_IL:
        band = "UNDERPOWERED"
    elif lo > 0 and delta > rel and delta > proj_half:
        band = "SUPERIOR"
    elif hi < 0 and delta < -rel and abs(delta) > proj_half:
        band = "INFERIOR"
    elif (lo <= 0 <= hi and half <= rel and half <= 0.02) or \
         ((lo > 0 or hi < 0) and abs(delta) <= rel):
        band = "PARITY"
    else:
        band = "INCONCLUSIVE"
    if band == "SUPERIOR" and (not res["V12"]["V12_PASS"] or
                               0.539 <= primary_auc < 0.60):
        band = "SUPERIOR-BAND-UNAVAILABLE (V12 or measured residual leak)"
    res["BAND"] = band

    # ---- coverage and secondaries ------------------------------------------
    T_ids = fr["frames"]["FRAME-T"]
    kd_T = [A.kind_m5(kinds.get(rows[i]["bid"])) for i in T_ids]
    okT = [j for j in range(len(T_ids)) if kd_T[j] is not None]
    res["coverage"] = {
        "LEGACY_M5_computable": f"{N}/{len(T_ids)} = {N/len(T_ids):.3f}",
        "KIND_M5_computable_on_FRAME_T": f"{len(okT)}/{len(T_ids)}",
        "I_K_on_whole_FRAME_T": S.mi_plugin([kd_T[j] for j in okT],
                                            [ovr[T_ids[j]] for j in okT]),
        "note": "the head-to-head is on the legacy arm's turf by construction (M3)"}
    auc_k, tie_k = S.auc_tie_corrected(
        [sorted(set(kk)).index(x) for x in kk], oo)
    auc_l, tie_l = S.auc_tie_corrected(
        [["L0-failed", "L1-hairline", "L2-mode", "L3-middling", "L4-wide"].index(x)
         for x in ll], oo)
    res["V9_ties"] = {"kind_arm_AUC": auc_k, "kind_tie_fraction": tie_k,
                      "legacy_arm_AUC": auc_l, "legacy_tie_fraction": tie_l,
                      "entropy_distinct_FRAME_H": len({x["entropy_score"] for x in d}),
                      "coherence_distinct_FRAME_H": len({x["coherence_score"] for x in d})}
    res["trivial_baselines"] = {
        "selected_action": S.mi_plugin([d[i]["action"] for i in keep], oo),
        "constant": 0.0}

    A.wjson("A0_col1.json", res)
    print(json.dumps({k: v for k, v in res.items() if k != "V7b"}, indent=1, default=str))
    print("V7b:", json.dumps(res["V7b"], indent=1, default=str))
    print("BAND:", band)
    A.marker("AN2_col1.done", {"BAND": band, "Delta": delta, "I_K": I_kind, "I_L": I_leg})
    return 0


if __name__ == "__main__":
    sys.exit(main())
