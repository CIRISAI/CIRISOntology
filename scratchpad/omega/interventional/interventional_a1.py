#!/usr/bin/env python3
"""AMENDMENT 1 arms — INTERVENTIONAL_AMENDMENT_1.md, staked before this file existed.

Adds: (c') a STRONG site-wise common driver, (f) the B1 replica (shared deterministic
clock, no state coupling), and (d") the distributional arm read inside its window.
The frozen instrument `interventional.py` is NOT modified; this file imports it.

Usage:  python3 interventional_a1.py > interventional_a1.log
"""
import json

import numpy as np

import interventional as I

_ORIG_BUILD = I.build_case        # captured before the rebind below

CLOCK_P = 400.0
CLOCK_XC = 0.3
A1_DIST_LAG = 6
A1_DIST_SITE = I.LINK_FROM        # probe at the interface: light-cone 1


def build_a1(name, seed, horizon):
    rng = np.random.default_rng(seed)

    if name == "cprime":              # STRONG common driver, site-wise
        st = {"A": rng.random(I.L), "B": rng.random(I.L), "C": rng.random(I.L)}

        def step(s, t):
            drive = I.f(s["C"])
            a = (1.0 - I.XC) * I.ring_step(s["A"]) + I.XC * drive
            b = (1.0 - I.XC) * I.ring_step(s["B"]) + I.XC * drive
            return {"A": I.reflect(a), "B": I.reflect(b),
                    "C": I.reflect(I.ring_step(s["C"]))}

        return st, step, ["A", "B", "C"]

    if name == "f":                   # the B1 replica: shared exogenous clock
        st = {"A": rng.random(I.L), "B": rng.random(I.L)}

        def step(s, t):
            m = 0.5 + 0.4 * np.cos(2.0 * np.pi * t / CLOCK_P)
            a = (1.0 - CLOCK_XC) * I.ring_step(s["A"]) + CLOCK_XC * m
            b = (1.0 - CLOCK_XC) * I.ring_step(s["B"]) + CLOCK_XC * m
            return {"A": I.reflect(a), "B": I.reflect(b)}

        return st, step, ["A", "B"]

    return _ORIG_BUILD(name, seed, horizon)


I.build_case_frozen = _ORIG_BUILD
I.build_case = build_a1               # so I.arm / I.dist_arm / I.run_series see the new cases


def main():
    res = {}
    S = I.SEED

    # ---- sham floor for the new cases (K-I1 again) ----
    sham = {}
    for case, pairs in (("cprime", [("A", "B"), ("B", "A"), ("C", "A")]),
                        ("f", [("A", "B"), ("B", "A")])):
        for ps, rs in pairs:
            sham[f"{case}:{ps}->{rs}"] = I.arm(case, S, ps, rs, amp=0.0,
                                               win=200)["exact_zero_everywhere"]
    res["sham"] = {"per_arm": sham, "pass": bool(all(sham.values()))}
    print("sham floor (new cases):", res["sham"]["pass"])

    # ---- (c') strong common driver ----
    ab = I.arm("cprime", S, "A", "B")
    ba = I.arm("cprime", S, "B", "A")
    ca = I.arm("cprime", S, "C", "A")
    cb = I.arm("cprime", S, "C", "B")
    ser = I.run_series("cprime", S, I.OBS_N)
    sa, sb = I.summarise(ser["A"]), I.summarise(ser["B"])
    o1 = I.cross_defect(sa, sb, 1, S + 51)
    o2 = I.cross_defect(sb, sa, 1, S + 52)
    r = float(np.corrcoef(sa, sb)[0, 1])
    res["cprime"] = {"probe_A_read_B": ab, "probe_B_read_A": ba,
                     "probe_C_read_A": ca, "probe_C_read_B": cb,
                     "obs_AB": o1, "obs_BA": o2, "pearson_r": r,
                     "e1_confounded": bool(abs(r) >= 0.5),
                     "e2_obs_fires": bool(o1["fires"] or o2["fires"]),
                     "e3_interv_exact_zero": bool(ab["exact_zero_everywhere"] and
                                                  ba["exact_zero_everywhere"]),
                     "e4_driver_control": bool(ca["onset_raw"] == 1 and cb["onset_raw"] == 1)}
    print(f"(c') r={r:+.3f} | obs A<-B {o1['gain']:+.5f} (fl {o1['floor99']:.5f}) fires={o1['fires']}"
          f" | obs B<-A {o2['gain']:+.5f} (fl {o2['floor99']:.5f}) fires={o2['fires']}"
          f" | interv exact zero both ways: {res['cprime']['e3_interv_exact_zero']}"
          f" | C->A onset={ca['onset_raw']} C->B onset={cb['onset_raw']} (staked 1)")

    # ---- (f) the B1 replica ----
    fab = I.arm("f", S, "A", "B")
    fba = I.arm("f", S, "B", "A")
    serf = I.run_series("f", S, I.OBS_N)
    fa, fb = I.summarise(serf["A"]), I.summarise(serf["B"])
    f1 = I.cross_defect(fa, fb, 1, S + 61)
    f2 = I.cross_defect(fb, fa, 1, S + 62)
    rf = float(np.corrcoef(fa, fb)[0, 1])
    res["f"] = {"probe_A_read_B": fab, "probe_B_read_A": fba,
                "obs_AB": f1, "obs_BA": f2, "pearson_r": rf,
                "f1_obs_fires": bool(f1["fires"] or f2["fires"]),
                "f2_interv_exact_zero": bool(fab["exact_zero_everywhere"] and
                                             fba["exact_zero_everywhere"])}
    print(f"(f) B1 replica: r={rf:+.3f} | obs A<-B {f1['gain']:+.5f} (fl {f1['floor99']:.5f}) "
          f"fires={f1['fires']} | obs B<-A {f2['gain']:+.5f} (fl {f2['floor99']:.5f}) "
          f"fires={f2['fires']} | interv exact zero both ways: {res['f']['f2_interv_exact_zero']}")

    # ---- (d") distributional arms inside the window ----
    d_path = I.arm("d", S, "A", "B", amp=I.SMALL, site=A1_DIST_SITE)
    g_d = I.dist_arm("d", "A", A1_DIST_SITE, "B", I.LARGE, A1_DIST_LAG, I.DIST_N, S + 71)
    g_dp = I.dist_arm("dprime", "A", 0, "B", I.LARGE, A1_DIST_LAG, I.DIST_N, S + 81)
    dp_path = I.arm("dprime", S, "A", "B", amp=I.LARGE, site=0)
    res["dpp"] = {"d_dist": g_d, "dprime_dist": g_dp,
                  "d_pathwise_interface": d_path, "dprime_pathwise": dp_path,
                  "g1_d_dist_fires": bool(g_d["p_perm"] < 0.01),
                  "g2_dprime_dist_null": bool(g_dp["p_perm"] > 0.05),
                  "g4_interface_latency_1": bool(d_path["onset_raw"] == 1)}
    res["dpp"]["g3_rule_separates"] = bool(
        res["dpp"]["g1_d_dist_fires"] and res["dpp"]["g2_dprime_dist_null"] and
        d_path["max_raw"] > 0.0 and dp_path["max_raw"] > 0.0)
    print(f"(d\") d dist p={g_d['p_perm']:.2e} effect={g_d['effect_sd_units']:.1f} sd "
          f"| d' dist p={g_dp['p_perm']:.3f} effect={g_dp['effect_sd_units']:.2f} sd "
          f"| d interface onset={d_path['onset_raw']} (staked 1)")

    v = {"sham": res["sham"]["pass"],
         "e1": res["cprime"]["e1_confounded"], "e2": res["cprime"]["e2_obs_fires"],
         "e3": res["cprime"]["e3_interv_exact_zero"], "e4": res["cprime"]["e4_driver_control"],
         "f1": res["f"]["f1_obs_fires"], "f2": res["f"]["f2_interv_exact_zero"],
         "g1": res["dpp"]["g1_d_dist_fires"], "g2": res["dpp"]["g2_dprime_dist_null"],
         "g3": res["dpp"]["g3_rule_separates"]}
    v["ALL"] = bool(all(v.values()))
    res["verdict"] = v
    print("\nAMENDMENT-1 VERDICT:", json.dumps(v))
    json.dump(res, open("interventional_a1_results.json", "w"), indent=2, default=float)
    print("wrote interventional_a1_results.json")


if __name__ == "__main__":
    main()
