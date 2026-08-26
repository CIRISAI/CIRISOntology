#!/usr/bin/env python3
"""INTERVENTIONAL SIGNATURE — planted-truth validation of the probe-response detector.

Theory: INTERVENTIONAL_SIGNATURE.md.  Stakes: INTERVENTIONAL_STAKES.md (frozen first).
numpy only; every seed fixed; no engine runs, no QPU.

Four planted cases (a) one-way deterministic, (b) independent deterministic,
(c) common driver, (d) stochastic one-way with coupled-noise twins + (d') the planted
noise-consumption trap.  Plus the observational detector for comparison, the sham-probe
floor (K-I1), and the engine demonstration reading of scratchpad/composition/s2/arm_K.csv.

Usage:  python3 interventional.py run    > interventional_run.log
"""
import json
import sys

import numpy as np

# ---- frozen parameters (INTERVENTIONAL_STAKES.md) --------------------------------
L = 16                 # sites per ring
EPS = 0.3              # diffusive coupling inside a ring
XC = 0.4               # cross-sector one-way link strength
T0 = 500               # burn-in steps before the probe
WIN = 1500             # response window, in steps after the probe
P_SITE = 8             # probe site for the light-cone predictions
LINK_FROM = L - 1      # cross-link leaves the driver at site 15 ...
LINK_TO = 0            # ... and enters the driven sector at site 0
SMALL = 1e-6           # small probe amplitude
LARGE = 0.4            # large probe amplitude (distributional arms)
SIGMA = 1e-3           # additive noise, stochastic cases
OBS_N = 24000          # observational comparison series length (engine frame count)
DIST_N = 400           # ensemble size, distributional arms
DIST_LAG = 20          # lag at which the distributional statistic is read
SEED = 20260826

# staked light-cone integers
RING_D = min(abs(P_SITE - LINK_FROM), L - abs(P_SITE - LINK_FROM))   # = 7
LAT_CROSS = RING_D + 1                                               # = 8
LAT_SELF = 0


def f(u):
    return 4.0 * u * (1.0 - u)


def reflect(u):
    u = np.where(u < 0.0, -u, u)
    return np.where(u > 1.0, 2.0 - u, u)


def ring_step(u):
    fu = f(u)
    return (1.0 - EPS) * fu + 0.5 * EPS * (np.roll(fu, 1) + np.roll(fu, -1))


# ---- the planted worlds ----------------------------------------------------------
def build_case(name, seed, horizon):
    """-> (state0 dict, step(state,t)->state, observable sector names).

    Every step function is a pure map; noise, where present, is drawn ONCE into an
    array indexed [t, sector, site] and consumed in that order, so it is blind to the
    state (theory sec 4.1).  Twin runs share the array by sharing the step closure.
    """
    rng = np.random.default_rng(seed)

    if name == "a":                       # one-way A -> B, deterministic
        st = {"A": rng.random(L), "B": rng.random(L)}

        def step(s, t):
            a = ring_step(s["A"])
            b = ring_step(s["B"])
            b = b.copy()
            b[LINK_TO] = (1.0 - XC) * b[LINK_TO] + XC * f(s["A"][LINK_FROM])
            return {"A": reflect(a), "B": reflect(b)}

        return st, step, ["A", "B"]

    if name == "b":                       # independent, deterministic, same law
        st = {"A": rng.random(L), "B": rng.random(L)}

        def step(s, t):
            return {"A": reflect(ring_step(s["A"])), "B": reflect(ring_step(s["B"]))}

        return st, step, ["A", "B"]

    if name == "c":                       # common driver C -> A, C -> B
        st = {"A": rng.random(L), "B": rng.random(L), "C": rng.random(L)}

        def step(s, t):
            drive = f(s["C"][LINK_FROM])
            a = ring_step(s["A"]).copy()
            b = ring_step(s["B"]).copy()
            a[LINK_TO] = (1.0 - XC) * a[LINK_TO] + XC * drive
            b[LINK_TO] = (1.0 - XC) * b[LINK_TO] + XC * drive
            return {"A": reflect(a), "B": reflect(b), "C": reflect(ring_step(s["C"]))}

        return st, step, ["A", "B", "C"]

    if name == "d":                       # one-way A -> B, additive A-blind noise
        st = {"A": rng.random(L), "B": rng.random(L)}
        xi = rng.normal(0.0, 1.0, size=(horizon + 2, 2, L))

        def step(s, t):
            a = ring_step(s["A"]) + SIGMA * xi[t, 0]
            b = ring_step(s["B"]).copy()
            b[LINK_TO] = (1.0 - XC) * b[LINK_TO] + XC * f(s["A"][LINK_FROM])
            b = b + SIGMA * xi[t, 1]
            return {"A": reflect(a), "B": reflect(b)}

        return st, step, ["A", "B"]

    if name == "dprime":                  # THE TRAP: no causal link; A picks B's slot
        st = {"A": rng.random(L), "B": rng.random(L)}
        xa = rng.normal(0.0, 1.0, size=(horizon + 2, L))
        xb = rng.normal(0.0, 1.0, size=(horizon + 2, 2, L))   # two i.i.d. slots

        def step(s, t):
            k = 1 if s["A"][0] > 0.5 else 0
            a = ring_step(s["A"]) + SIGMA * xa[t]
            b = ring_step(s["B"]) + SIGMA * xb[t, k]
            return {"A": reflect(a), "B": reflect(b)}

        return st, step, ["A", "B"]

    raise ValueError(name)


def advance(state, step, t_from, n):
    s = {k: v.copy() for k, v in state.items()}
    for t in range(t_from, t_from + n):
        s = step(s, t)
    return s


# ---- the probe-response instrument ------------------------------------------------
def apply_probe(state, sector, site, amp):
    s = {k: v.copy() for k, v in state.items()}
    s[sector][site] = float(reflect(np.array(s[sector][site] + amp)))
    return s


def twin_response(base, step, t0, win, probe_sector, probe_site, amp, read_sector):
    """Probed vs unprobed twins from the SAME microstate, same law, same noise stream.

    Returns raw = max_i |delta u_i| in the read sector, and view = Hamming distance of
    the 16-bit coarse view, both indexed by lag 0..win (lag 0 = immediately post-probe).
    """
    ctl = {k: v.copy() for k, v in base.items()}
    prb = apply_probe(base, probe_sector, probe_site, amp)
    raw = np.empty(win + 1)
    view = np.empty(win + 1, dtype=int)
    for lag in range(win + 1):
        d = prb[read_sector] - ctl[read_sector]
        raw[lag] = np.max(np.abs(d))
        view[lag] = int(np.sum((prb[read_sector] > 0.5) != (ctl[read_sector] > 0.5)))
        ctl = step(ctl, t0 + lag)
        prb = step(prb, t0 + lag)
    return raw, view


def onset(raw):
    nz = np.flatnonzero(raw > 0.0)
    return int(nz[0]) if len(nz) else None


def arm(case, seed, probe_sector, read_sector, amp=SMALL, site=P_SITE, win=WIN):
    st0, step, _ = build_case(case, seed, T0 + win + 4)
    base = advance(st0, step, 0, T0)
    raw, view = twin_response(base, step, T0, win, probe_sector, site, amp, read_sector)
    return {
        "onset_raw": onset(raw),
        "onset_view": onset(view.astype(float)),
        "max_raw": float(raw.max()),
        "max_view": int(view.max()),
        "exact_zero_everywhere": bool(np.all(raw == 0.0)),
        "n_nonzero_lags": int(np.sum(raw > 0.0)),
    }


# ---- distributional arm (theory sec 4, Theorem 4) ---------------------------------
def dist_arm(case, probe_sector, probe_site, read_sector, amp, lag, n_ens, seed0):
    """Fixed initial microstate, ensemble over INDEPENDENT noise streams.

    Estimates Law(v_B(X_lag) | do(delta)) vs Law(v_B(X_lag)) — the causal-effect
    definition, which the pathwise twin comparison does NOT imply (theory sec 4.1).
    """
    horizon = T0 + lag + 4
    st0, step0, _ = build_case(case, seed0, horizon)
    base = advance(st0, step0, 0, T0)          # one fixed initial microstate

    def ens(do_probe, tag):
        out = np.empty(n_ens)
        for j in range(n_ens):
            _, step, _ = build_case(case, seed0 + 1000 * tag + j + 1, horizon)
            s = apply_probe(base, probe_sector, probe_site, amp) if do_probe else \
                {k: v.copy() for k, v in base.items()}
            s = advance(s, step, T0, lag)
            out[j] = float(np.mean(s[read_sector]))
        return out

    x = ens(False, 1)
    y = ens(True, 2)
    obs = abs(y.mean() - x.mean())
    pool = np.concatenate([x, y])
    rng = np.random.default_rng(seed0 + 777)
    n_perm = 20000
    cnt = 0
    for _ in range(n_perm):
        p = rng.permutation(pool)
        if abs(p[n_ens:].mean() - p[:n_ens].mean()) >= obs:
            cnt += 1
    sd = np.sqrt(0.5 * (x.var(ddof=1) + y.var(ddof=1)))
    return {"mean_unprobed": float(x.mean()), "mean_probed": float(y.mean()),
            "abs_diff": float(obs), "pooled_sd": float(sd),
            "effect_sd_units": float(obs / sd) if sd > 0 else float("inf"),
            "p_perm": float((cnt + 1) / (n_perm + 1))}


# ---- the observational detector, for comparison -----------------------------------
def run_series(case, seed, nsteps):
    st0, step, sectors = build_case(case, seed, nsteps + 4)
    s = {k: v.copy() for k, v in st0.items()}
    out = {k: np.empty((nsteps, L)) for k in sectors}
    for t in range(nsteps):
        s = step(s, t)
        for k in sectors:
            out[k][t] = s[k]
    return out


def summarise(series):
    return series.mean(axis=1) - 0.5


def bits_fibers(sc, train, nfib=4):
    b = (sc > 0).astype(np.intp)
    fib = np.zeros(len(sc), dtype=np.intp)
    for stbit in (0, 1):
        m = b == stbit
        tv = np.abs(sc[train & m])
        if len(tv) < nfib:
            continue
        edges = np.quantile(tv, np.linspace(0.0, 1.0, nfib + 1))
        fib[m] = np.clip(np.digitize(np.abs(sc[m]), edges[1:-1]), 0, nfib - 1)
    return b, fib


def fit_prob(ctx, y, n):
    num = np.ones(n)
    den = 2.0 * np.ones(n)
    np.add.at(num, ctx, y.astype(float))
    np.add.at(den, ctx, 1.0)
    return num / den


def logloss(p, ctx, y):
    pr = np.clip(p[ctx], 1e-9, 1.0 - 1e-9)
    return -(y * np.log(pr) + (1 - y) * np.log(1.0 - pr))


def cross_defect(sa, sb, lag, seed, n_perm=200):
    """Held-out predictive gain of adding B's (bit,fiber) context to A's, for A's next
    bit.  Mirrors scratchpad/composition/s2_analyze.py's estimator.  Floor = 99th pct
    of the within-split permutation null."""
    rng = np.random.default_rng(seed)
    n = len(sa)
    train = np.zeros(n, bool)
    train[: int(0.6 * n)] = True
    ba, fa = bits_fibers(sa, train)
    bb, fb = bits_fibers(sb, train)
    ctx_a = ba * 4 + fa
    ctx_b = bb * 4 + fb
    ctx_ab = ctx_a * 8 + ctx_b
    y = np.roll(ba, -lag).astype(np.int8)
    v = slice(0, n - lag)
    tr, te = train[v], ~train[v]
    p_a = fit_prob(ctx_a[v][tr], y[v][tr], 8)
    p_ab = fit_prob(ctx_ab[v][tr], y[v][tr], 64)
    gain = (logloss(p_a, ctx_a[v][te], y[v][te]) -
            logloss(p_ab, ctx_ab[v][te], y[v][te])).mean()
    idx_tr, idx_te = np.flatnonzero(train), np.flatnonzero(~train)
    null = np.empty(n_perm)
    for k in range(n_perm):
        cb = ctx_b.copy()
        cb[idx_tr] = rng.permutation(cb[idx_tr])
        cb[idx_te] = rng.permutation(cb[idx_te])
        c2 = ctx_a * 8 + cb
        p2 = fit_prob(c2[v][tr], y[v][tr], 64)
        null[k] = (logloss(p_a, ctx_a[v][te], y[v][te]) -
                   logloss(p2, c2[v][te], y[v][te])).mean()
    return {"gain": float(gain), "floor99": float(np.percentile(null, 99)),
            "fires": bool(gain > np.percentile(null, 99))}


# ---- the engine demonstration reading ---------------------------------------------
def engine_reading(path="../../composition/s2/arm_K.csv"):
    rows = np.loadtxt(path, delimiter=",", skiprows=1)
    frame, dpx, dpos = rows[:, 0].astype(int), rows[:, 1], rows[:, 2]
    ped_px, ped_pos = float(dpx[0]), float(dpos[0])
    w = dpos[5:960]                       # B4's window, frames 245..1199
    med_w = float(np.median(w))
    r = w[1:][w[:-1] > 0] / w[:-1][w[:-1] > 0]
    k_orig = float(np.median(r))
    ws = w - ped_pos                      # pedestal-subtracted
    rs = ws[1:][ws[:-1] > 0] / ws[:-1][ws[:-1] > 0]
    k_sub = float(np.median(rs))
    wpx = dpx[5:960]
    rpx = wpx[1:][wpx[:-1] > 0] / wpx[:-1][wpx[:-1] > 0]
    early = slice(0, 600)
    lg = np.log(np.maximum(dpos[early] - ped_pos, 1e-30))
    good = np.isfinite(lg) & (dpos[early] - ped_pos > 0)
    slope = float(np.polyfit(frame[early][good] - frame[0], lg[good], 1)[0]) \
        if good.sum() > 10 else None
    return {
        "n_frames": int(len(frame)), "first_frame": int(frame[0]),
        "last_frame": int(frame[-1]),
        "pedestal_div_px": ped_px, "pedestal_div_pos": ped_pos,
        "median_window_div_pos": med_w,
        "pedestal_over_window_median": float(ped_pos / med_w),
        "K_median_as_published": k_orig,
        "K_median_pedestal_subtracted": k_sub,
        "K_median_div_px": float(np.median(rpx)),
        "growth_factor_pos_full": float(dpos[-1] / dpos[0]),
        "growth_factor_px_full": float(dpx[-1] / dpx[0]),
        "final_div_pos": float(dpos[-1]), "final_div_px": float(dpx[-1]),
        "log_slope_per_frame_first600_pedsub": slope,
        "frac_window_below_2x_pedestal":
            float(np.mean(w < 2.0 * ped_pos)),
    }


# ---- the run ----------------------------------------------------------------------
def run():
    res = {"params": {"L": L, "EPS": EPS, "XC": XC, "T0": T0, "WIN": WIN,
                      "P_SITE": P_SITE, "SMALL": SMALL, "LARGE": LARGE,
                      "SIGMA": SIGMA, "SEED": SEED, "OBS_N": OBS_N,
                      "DIST_N": DIST_N, "DIST_LAG": DIST_LAG},
           "staked_latency": {"cross": LAT_CROSS, "self": LAT_SELF}}

    # --- K-I1: the sham probe floor, every case, both directions ---
    sham = {}
    for case in ("a", "b", "c", "d", "dprime"):
        pairs = [("A", "B"), ("B", "A")] + ([("C", "A")] if case == "c" else [])
        for ps, rs in pairs:
            k = f"{case}:{ps}->{rs}"
            sham[k] = arm(case, SEED, ps, rs, amp=0.0, win=200)["exact_zero_everywhere"]
    res["K_I1_sham"] = {"per_arm": sham, "pass": bool(all(sham.values()))}
    print("K-I1 sham floor (delta = id):", res["K_I1_sham"]["pass"],
          "" if res["K_I1_sham"]["pass"] else sham)
    if not res["K_I1_sham"]["pass"]:
        print("K-I1 FIRED -> run VOID")
        json.dump(res, open("interventional_results.json", "w"), indent=2, default=float)
        return

    # --- (a) one-way deterministic ---
    a_ab = arm("a", SEED, "A", "B")
    a_ba = arm("a", SEED, "B", "A")
    a_aa = arm("a", SEED, "A", "A")
    res["a"] = {"probe_A_read_B": a_ab, "probe_B_read_A": a_ba, "probe_A_read_A": a_aa,
                "a1_arrow_found": bool(a_ab["max_raw"] > 0.0),
                "a2_latency_exact": bool(a_ab["onset_raw"] == LAT_CROSS),
                "a3_reverse_exact_zero": bool(a_ba["exact_zero_everywhere"]),
                "a4_view_registers": bool(a_ab["max_view"] >= 1),
                "P2_self_latency_exact": bool(a_aa["onset_raw"] == LAT_SELF)}
    print(f"(a) A->B onset={a_ab['onset_raw']} (staked {LAT_CROSS}) max_raw={a_ab['max_raw']:.3e} "
          f"max_view={a_ab['max_view']} | B->A exact zero: {a_ba['exact_zero_everywhere']} "
          f"| A->A onset={a_aa['onset_raw']}")

    # --- (b) independent deterministic ---
    b_ab = arm("b", SEED, "A", "B")
    b_ba = arm("b", SEED, "B", "A")
    ser_b = run_series("b", SEED, OBS_N)
    sa_b, sb_b = summarise(ser_b["A"]), summarise(ser_b["B"])
    obs_b1 = cross_defect(sa_b, sb_b, 1, SEED + 11)
    obs_b2 = cross_defect(sb_b, sa_b, 1, SEED + 12)
    res["b"] = {"probe_A_read_B": b_ab, "probe_B_read_A": b_ba,
                "b1_both_exact_zero": bool(b_ab["exact_zero_everywhere"] and
                                           b_ba["exact_zero_everywhere"]),
                "observational_AB": obs_b1, "observational_BA": obs_b2,
                "pearson_r": float(np.corrcoef(sa_b, sb_b)[0, 1])}
    print(f"(b) both exact zero: {res['b']['b1_both_exact_zero']} | "
          f"obs A<-B gain={obs_b1['gain']:+.5f} (fl {obs_b1['floor99']:.5f}) fires={obs_b1['fires']} | "
          f"obs B<-A gain={obs_b2['gain']:+.5f} (fl {obs_b2['floor99']:.5f}) fires={obs_b2['fires']} | "
          f"r={res['b']['pearson_r']:+.3f}")

    # --- (c) common driver ---
    c_ab = arm("c", SEED, "A", "B")
    c_ba = arm("c", SEED, "B", "A")
    c_ca = arm("c", SEED, "C", "A")
    c_cb = arm("c", SEED, "C", "B")
    ser_c = run_series("c", SEED, OBS_N)
    sa_c, sb_c = summarise(ser_c["A"]), summarise(ser_c["B"])
    obs_c1 = cross_defect(sa_c, sb_c, 1, SEED + 21)
    obs_c2 = cross_defect(sb_c, sa_c, 1, SEED + 22)
    res["c"] = {"probe_A_read_B": c_ab, "probe_B_read_A": c_ba,
                "probe_C_read_A": c_ca, "probe_C_read_B": c_cb,
                "c1_both_exact_zero": bool(c_ab["exact_zero_everywhere"] and
                                           c_ba["exact_zero_everywhere"]),
                "c2_driver_control": bool(c_ca["onset_raw"] == LAT_CROSS and
                                          c_cb["onset_raw"] == LAT_CROSS),
                "observational_AB": obs_c1, "observational_BA": obs_c2,
                "c3_observational_fires": bool(obs_c1["fires"] or obs_c2["fires"]),
                "pearson_r": float(np.corrcoef(sa_c, sb_c)[0, 1])}
    print(f"(c) A<->B exact zero both ways: {res['c']['c1_both_exact_zero']} | "
          f"C->A onset={c_ca['onset_raw']} C->B onset={c_cb['onset_raw']} (staked {LAT_CROSS}) | "
          f"obs A<-B gain={obs_c1['gain']:+.5f} (fl {obs_c1['floor99']:.5f}) fires={obs_c1['fires']} | "
          f"obs B<-A gain={obs_c2['gain']:+.5f} (fl {obs_c2['floor99']:.5f}) fires={obs_c2['fires']} | "
          f"r={res['c']['pearson_r']:+.3f}")

    # --- (d) stochastic one-way, coupled-noise twins ---
    d_ab = arm("d", SEED, "A", "B")
    d_ba = arm("d", SEED, "B", "A")
    d_dist = dist_arm("d", "A", P_SITE, "B", LARGE, DIST_LAG, DIST_N, SEED + 31)
    res["d"] = {"probe_A_read_B": d_ab, "probe_B_read_A": d_ba, "dist": d_dist,
                "d1_arrow_and_latency": bool(d_ab["max_raw"] > 0.0 and
                                             d_ab["onset_raw"] == LAT_CROSS),
                "d2_reverse_exact_zero": bool(d_ba["exact_zero_everywhere"]),
                "d3_dist_fires": bool(d_dist["p_perm"] < 0.01)}
    print(f"(d) A->B onset={d_ab['onset_raw']} (staked {LAT_CROSS}) max_raw={d_ab['max_raw']:.3e} | "
          f"B->A exact zero: {d_ba['exact_zero_everywhere']} | "
          f"dist p={d_dist['p_perm']:.2e} effect={d_dist['effect_sd_units']:.1f} sd")

    # --- (d') the planted trap: no causal link, state-dependent noise consumption ---
    dp_ab = arm("dprime", SEED, "A", "B", amp=LARGE, site=0)
    dp_dist = dist_arm("dprime", "A", 0, "B", LARGE, DIST_LAG, DIST_N, SEED + 41)
    # how often do the twins' noise selectors differ?
    st0, step, _ = build_case("dprime", SEED, T0 + 200 + 4)
    base = advance(st0, step, 0, T0)
    ctl = {k: v.copy() for k, v in base.items()}
    prb = apply_probe(base, "A", 0, LARGE)
    diff = 0
    for lag in range(200):
        if (ctl["A"][0] > 0.5) != (prb["A"][0] > 0.5):
            diff += 1
        ctl = step(ctl, T0 + lag)
        prb = step(prb, T0 + lag)
    res["dprime"] = {"pathwise_probe_A_read_B": dp_ab, "dist": dp_dist,
                     "dp1_pathwise_fires": bool(dp_ab["max_raw"] > 0.0),
                     "dp2_dist_null": bool(dp_dist["p_perm"] > 0.05),
                     "dp4_selector_diff_frac": diff / 200.0}
    print(f"(d') pathwise max_raw={dp_ab['max_raw']:.3e} onset={dp_ab['onset_raw']} "
          f"(FIRES={res['dprime']['dp1_pathwise_fires']}, planted) | "
          f"dist p={dp_dist['p_perm']:.3f} effect={dp_dist['effect_sd_units']:.2f} sd | "
          f"selector differs {res['dprime']['dp4_selector_diff_frac']:.1%} of steps")

    res["dprime"]["dp3_rule_separates"] = bool(
        res["d"]["d1_arrow_and_latency"] and res["d"]["d3_dist_fires"] and
        res["dprime"]["dp1_pathwise_fires"] and res["dprime"]["dp2_dist_null"])

    # --- adjudication against the frozen stakes ---
    verdict = {
        "a1": res["a"]["a1_arrow_found"], "a2": res["a"]["a2_latency_exact"],
        "a3": res["a"]["a3_reverse_exact_zero"], "a4": res["a"]["a4_view_registers"],
        "b1": res["b"]["b1_both_exact_zero"],
        "c1": res["c"]["c1_both_exact_zero"], "c2": res["c"]["c2_driver_control"],
        "c3": res["c"]["c3_observational_fires"],
        "d1": res["d"]["d1_arrow_and_latency"], "d2": res["d"]["d2_reverse_exact_zero"],
        "d3": res["d"]["d3_dist_fires"],
        "dp1": res["dprime"]["dp1_pathwise_fires"],
        "dp2": res["dprime"]["dp2_dist_null"],
        "dp3": res["dprime"]["dp3_rule_separates"],
        "P1": res["a"]["a2_latency_exact"], "P2": res["a"]["P2_self_latency_exact"],
        "P3": res["c"]["c2_driver_control"], "K_I1": res["K_I1_sham"]["pass"],
    }
    verdict["ALL"] = bool(all(verdict.values()))
    res["verdict"] = verdict
    print("\nVERDICT:", json.dumps(verdict, indent=None))
    print("ALL STAKED ARMS LAND:", verdict["ALL"])

    # --- engine demonstration reading ---
    eng = engine_reading()
    res["engine_demo"] = eng
    print("\nENGINE DEMONSTRATION (arm_K.csv, NOT a stake):")
    for k, v in eng.items():
        print(f"  {k}: {v}")

    json.dump(res, open("interventional_results.json", "w"), indent=2, default=float)
    print("\nwrote interventional_results.json")


if __name__ == "__main__":
    {"run": run}[sys.argv[1] if len(sys.argv) > 1 else "run"]()
