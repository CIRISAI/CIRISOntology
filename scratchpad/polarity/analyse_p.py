"""POLARITY stage 5 — P2's p-value and P3's twin test.

REFUSES to run unless stage 4 (`power.json`) exists: the prereg requires the UNDERPOWERED
determination to be made before any p-value is read.
"""
from __future__ import annotations
import collections, json, pathlib, sys
import numpy as np
from scipy.stats import fisher_exact, chi2

D = pathlib.Path("/home/emoore/CIRISOntology/scratchpad/polarity")
NPERM = 2000
SEED = 20260820
sys.path.insert(0, str(D))
from analyse_power import build, load  # same modal convention, same inputs

def tvd(A, B):
    keys = set(A) | set(B)
    na, nb = max(sum(A.values()), 1), max(sum(B.values()), 1)
    return 0.5 * sum(abs(A[x] / na - B[x] / nb) for x in keys)

def pooled(cells, kinds, weighted=False):
    vals, ws = [], []
    for k in kinds:
        A = collections.Counter(cells[k]["+"]); B = collections.Counter(cells[k]["-"])
        vals.append(tvd(A, B)); ws.append(len(cells[k]["+"]) + len(cells[k]["-"]))
    if not vals:
        return float("nan")
    return float(np.average(vals, weights=ws) if weighted else np.mean(vals))

def perm_null(cells, kinds, weighted, seed, nperm=NPERM):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(nperm):
        c = {}
        for k in kinds:
            lab = cells[k]["+"] + cells[k]["-"]; npl = len(cells[k]["+"])
            idx = rng.permutation(len(lab))
            c[k] = {"+": [lab[j] for j in idx[:npl]], "-": [lab[j] for j in idx[npl:]]}
        out.append(pooled(c, kinds, weighted))
    return np.array(out)

def pval(obs, null):
    return (1 + int((null >= obs - 1e-12).sum())) / (1 + len(null))

def cmh(tables):
    """Cochran-Mantel-Haenszel, tables = list of [[a,b],[c,d]]."""
    A = E = V = 0.0
    for (a, b), (c_, d) in tables:
        n = a + b + c_ + d
        if n < 2: continue
        A += a; E += (a + b) * (a + c_) / n
        V += (a + b) * (c_ + d) * (a + c_) / (n * n) * (b + d) / (n - 1)
    if V <= 0:
        return float("nan"), float("nan"), A, E
    stat = (abs(A - E) - 0.5) ** 2 / V
    return stat, float(chi2.sf(stat, 1)), A, E

def strat_perm(rows, seed=7, nperm=20000):
    """Exact-ish stratified test: permute the KIND label within each polarity stratum.
    rows = list of (kind, polarity, is_target_read). Statistic = |sum_strata (a - E)|."""
    rng = np.random.default_rng(seed)
    strata = collections.defaultdict(list)
    for k, p, y in rows:
        strata[p].append((k, y))
    def stat(assign):
        tot = 0.0
        for p, lst in strata.items():
            ks = assign[p]; ys = [y for _, y in lst]
            a = sum(y for k, y in zip(ks, ys) if k == "Structure")
            n = len(ys); n1 = sum(1 for k in ks if k == "Structure"); m1 = sum(ys)
            tot += a - (n1 * m1 / n if n else 0)
        return abs(tot)
    obs = stat({p: [k for k, _ in lst] for p, lst in strata.items()})
    cnt = 0
    for _ in range(nperm):
        assign = {p: list(rng.permutation([k for k, _ in lst])) for p, lst in strata.items()}
        if stat(assign) >= obs - 1e-12:
            cnt += 1
    return obs, (1 + cnt) / (1 + nperm)

def main():
    pj = D / "power.json"
    if not pj.exists():
        sys.exit("REFUSING: power.json absent — the UNDERPOWERED determination (prereg §3) "
                 "must be made before any p-value is computed.")
    power = json.loads(pj.read_text())
    corpus, scored, _, _ = build()
    modal = {i: scored[i]["modal"] for i in scored}
    sc = {i for i in modal if modal[i] in ("+", "-")}

    def cells(exclude_conj=False, errors_only=False):
        c = collections.defaultdict(lambda: collections.defaultdict(list))
        for i in sc:
            r = corpus[i]
            if exclude_conj and r["part"] == "CONJ": continue
            if r["base_modal"] is None: continue
            if errors_only and r["base_modal"] == r["axis_kind"]: continue
            c[r["axis_kind"]][modal[i]].append(r["base_modal"])
        return c

    out = {"UNDERPOWERED": power["UNDERPOWERED"],
           "qualifying_primary": power["P2_qualifying_kinds_primary"]}

    # ---- P2 primary: full confusion rows, unweighted pooling, CONJ included ----
    c = cells(); q = power["P2_qualifying_kinds_primary"]
    obs = pooled(c, q)
    null = np.load(D / "null_primary.npy")
    out["P2_primary"] = {"obs": obs, "p": pval(obs, null), "n_kinds": len(q),
                         "null_mean": float(null.mean()), "null_sd": float(null.std(ddof=1)),
                         "null_p95": float(np.quantile(null, .95)),
                         "null_p99": float(np.quantile(null, .99)),
                         "per_kind": {k: {"tvd": tvd(collections.Counter(c[k]["+"]),
                                                     collections.Counter(c[k]["-"])),
                                          "n_plus": len(c[k]["+"]), "n_minus": len(c[k]["-"]),
                                          "reads_plus": dict(collections.Counter(c[k]["+"])),
                                          "reads_minus": dict(collections.Counter(c[k]["-"]))}
                                      for k in q}}
    # per-kind permutation p (descriptive)
    for k in q:
        nk = perm_null({k: c[k]}, [k], False, seed=SEED + int(__import__("zlib").crc32(k.encode()) % 9973))
        o = tvd(collections.Counter(c[k]["+"]), collections.Counter(c[k]["-"]))
        out["P2_primary"]["per_kind"][k]["p"] = pval(o, nk)

    # ---- pre-specified sensitivities ----
    sens = {}
    ce = cells(errors_only=True)
    qe = [k for k in ce if len(ce[k]["+"]) >= 8 and len(ce[k]["-"]) >= 8]
    if qe:
        o = pooled(ce, qe); n = perm_null(ce, qe, False, SEED + 1)
        sens["errors_only"] = {"obs": o, "p": pval(o, n), "kinds": sorted(qe),
                               "cells": {k: [len(ce[k]['+']), len(ce[k]['-'])] for k in sorted(qe)}}
    else:
        sens["errors_only"] = {"note": "no kind clears 8-per-polarity once correct reads are "
                                       "removed", "cells": {k: [len(ce[k]['+']), len(ce[k]['-'])]
                                                            for k in sorted(ce)}}
    o = pooled(c, q, weighted=True); n = perm_null(c, q, True, SEED + 2)
    sens["n_weighted"] = {"obs": o, "p": pval(o, n)}
    cn = cells(exclude_conj=True); qn = power["P2_qualifying_kinds_no_conj"]
    if qn:
        o = pooled(cn, qn); n = perm_null(cn, qn, False, SEED + 3)
        sens["no_conj"] = {"obs": o, "p": pval(o, n), "kinds": qn}
    else:
        sens["no_conj"] = {"note": "no qualifying kind without CONJ"}
    out["P2_sensitivities"] = sens

    # ---- P3: the twins under sign ----
    tw = [corpus[i] for i in corpus
          if corpus[i]["axis_kind"] in ("Structure", "Circumstances")
          and corpus[i]["base_modal"] is not None]
    unc = collections.defaultdict(collections.Counter)
    for r in tw:
        unc[r["axis_kind"]][r["base_modal"]] += 1
    p3 = {"unconditional_rows": {k: dict(v) for k, v in unc.items()},
          "unconditional_2x2_Manner": {k: [unc[k]["Manner"], sum(unc[k].values()) - unc[k]["Manner"]]
                                       for k in ("Structure", "Circumstances")},
          "unconditional_2x2_Facts": {k: [unc[k]["Facts"], sum(unc[k].values()) - unc[k]["Facts"]]
                                      for k in ("Structure", "Circumstances")}}
    st = [r for r in tw if modal.get(r["id"]) in ("+", "-")]
    p3["polarity_balance"] = {k: dict(collections.Counter(modal[r["id"]] for r in st
                                                          if r["axis_kind"] == k))
                              for k in ("Structure", "Circumstances")}
    bal = [[p3["polarity_balance"]["Structure"].get(s, 0) for s in ("+", "-")],
           [p3["polarity_balance"]["Circumstances"].get(s, 0) for s in ("+", "-")]]
    p3["polarity_imbalance_fisher_p"] = float(fisher_exact(bal)[1])
    for target_read in ("Manner", "Facts"):
        tabs, strat = [], {}
        for pol in ("+", "-"):
            a = sum(1 for r in st if r["axis_kind"] == "Structure" and modal[r["id"]] == pol
                    and r["base_modal"] == target_read)
            b = sum(1 for r in st if r["axis_kind"] == "Structure" and modal[r["id"]] == pol) - a
            cc = sum(1 for r in st if r["axis_kind"] == "Circumstances" and modal[r["id"]] == pol
                     and r["base_modal"] == target_read)
            d = sum(1 for r in st if r["axis_kind"] == "Circumstances" and modal[r["id"]] == pol) - cc
            tabs.append([[a, b], [cc, d]])
            strat[pol] = {"table": [[a, b], [cc, d]],
                          "fisher_p": float(fisher_exact([[a, b], [cc, d]])[1]) if (a+b) and (cc+d) else None}
        s, pv, A, E = cmh(tabs)
        rows = [(r["axis_kind"], modal[r["id"]], int(r["base_modal"] == target_read)) for r in st]
        so, sp = strat_perm(rows)
        # unconditional comparison on the same scoreable subset
        ua = sum(1 for r in st if r["axis_kind"] == "Structure" and r["base_modal"] == target_read)
        ub = sum(1 for r in st if r["axis_kind"] == "Structure") - ua
        uc = sum(1 for r in st if r["axis_kind"] == "Circumstances" and r["base_modal"] == target_read)
        ud = sum(1 for r in st if r["axis_kind"] == "Circumstances") - uc
        p3[f"to_{target_read}"] = {"strata": strat, "cmh_stat": s, "cmh_p": pv,
                                   "cmh_A": A, "cmh_E": E,
                                   "strat_perm_stat": so, "strat_perm_p": sp,
                                   "unconditional_on_scoreable": [[ua, ub], [uc, ud]],
                                   "unconditional_fisher_p": float(fisher_exact([[ua, ub], [uc, ud]])[1])}
    out["P3"] = p3

    (D / "pvalues.json").write_text(json.dumps(out, indent=1, sort_keys=True, default=float) + "\n")
    print(json.dumps(out, indent=1, sort_keys=True, default=float))

if __name__ == "__main__":
    main()
