#!/usr/bin/env python3
"""Build the run-2 freeze from MEASURED values (QPU_HABIT_PREREG.md addendum 1).

Run 1 VOIDed because the published calibration is not good enough to select on:
on the pinned triple it listed P(0|1) = 0.0098 where the device delivered
0.127, and T1 values up to 63 % longer than the same job measured.  Run 2
therefore selects the triple, and sets the delay grid, from the screening job
`qpu_habit_screen.json` — measured minutes earlier, on this device.

Selection rule for run 2, fixed before the screen was read:
  among the screened candidate triples, take the one minimising the WORST
  measured readout error over its three qubits; require that worst error
  <= 0.015 (so the pre-registered readout VOID floor of 0.95 has real margin),
  and all three screened T1 in [60, 500] us.

Usage: qenv/bin/python qpu_habit_freeze2.py
"""
import json
import math
import time

import numpy as np

import qpu_habit_pipeline as P

LN2 = math.log(2.0)


def dt_align(x):
    return round(round(x / 0.064) * 0.064, 3)


def main():
    scr = json.load(open("qpu_habit_screen.json"))
    fz1 = P.load_freeze()
    rank = scr["ranking"]
    pick = None
    for r in rank:
        if r["worst_readout"] <= 0.015 and all(60 <= x <= 500 for x in r["T1"]):
            pick = r
            break
    if pick is None:
        raise SystemExit("no screened triple passes the run-2 rule")
    trip = pick["trip"]
    a, c, b = trip                      # path a-c-b, check bit on the middle
    slots = [a, b, c]
    qi = {q: i for i, q in enumerate(scr["qubits"])}

    T1s = [pick["T1"][trip.index(q)] for q in slots]
    e0 = [float(scr["p1_prep0"][qi[q]]) for q in slots]
    e1 = [float(1 - scr["p1_prep1"][qi[q]]) for q in slots]

    from qiskit_ibm_runtime import QiskitRuntimeService
    svc = QiskitRuntimeService()
    be = svc.backend(P.BACKEND_NAME)
    props = be.properties()
    T2s = [props.t2(q) * 1e6 for q in slots]
    T1pub = [props.t1(q) * 1e6 for q in slots]

    gam1 = sum(1.0 / x for x in T1s)
    rate_cl = 2.0 * gam1
    rate_q = 2.0 * sum(1.0 / x for x in T2s)

    # The screen's one-point T1 assumes a zero floor and therefore OVERSTATES
    # T1 (run 1 fitted excited-state populations of 0.025-0.065).  Design the
    # grid at a rate 15 % faster than the screen implies, so the late points sit
    # at SNR ~ 8 rather than ~ 5 if the device is worse than screened.
    rate_design = rate_cl * 1.15
    tmax = math.log(LN2 / 4e-3) / rate_design
    npts = 10
    dC = [dt_align(tmax * (i / (npts - 1)) ** 1.30) for i in range(npts)]
    tmaxq = math.log(LN2 / 5e-3) / (rate_q * 1.15)
    dQ = [dt_align(tmaxq * (i / 5) ** 1.30) for i in range(6)]
    T1med = sum(T1s) / 3
    dT = [dt_align(x) for x in (0.0, 0.35 * T1med, 0.8 * T1med, 1.4 * T1med,
                                2.2 * T1med, 3.2 * T1med)]

    fz = {
        "v2": True,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "backend": P.BACKEND_NAME,
        "screen_job": scr["job_id"],
        "void_run": "qpu_habit_A_d9immeqbr2fc73e4u02g.json",
        "triple_path": trip, "slots_abc": slots,
        "selection": "min worst MEASURED readout error over screened triples",
        "worst_measured_readout": pick["worst_readout"],
        "cal": {
            "T1_us": {str(q): T1s[i] for i, q in enumerate(slots)},
            "T1_source": "screening job (measured), one-point estimate",
            "T1_published_us": {str(q): T1pub[i] for i, q in enumerate(slots)},
            "T2_us": {str(q): T2s[i] for i, q in enumerate(slots)},
            "T2_source": "published (no in-job T2 audit; quantum arm is a demonstration)",
            "prob_meas1_prep0": {str(q): e0[i] for i, q in enumerate(slots)},
            "prob_meas0_prep1": {str(q): e1[i] for i, q in enumerate(slots)},
            "readout_source": "screening job (measured)",
            "cz_error": {f"{a}_{c}": pick["cz"][0], f"{c}_{b}": pick["cz"][1]},
        },
        "predicted_rate_classical_per_us": rate_cl,
        "predicted_rate_quantum_per_us": rate_q,
        "rate_design_per_us": rate_design,
        "delays_classical_us": dC,
        "delays_quantum_us": dQ,
        "delays_t1_us": dT,
        "delays_control_us": [dC[0], dC[4], dC[8]],
        "delays_product_us": [dC[0], dC[8]],
        "shots": {"A1": 8192, "A2": 4096, "A4": 4096, "A7": 4096, "A8": 8192,
                  "B1": 8192, "B2": 8192},
        "rent_cycles": [0, 1, 2, 4],
        "rent_totals_us": [dC[4], dC[7]],
        "p_exc_nominal": 0.02,
    }
    with open("qpu_habit_freeze2.json", "w") as f:
        json.dump(fz, f, indent=2)
    print(json.dumps({k: v for k, v in fz.items() if k != "cal"}, indent=2))
    print("cal:", json.dumps(fz["cal"], indent=2))
    planA = P.plan_A(fz); planB = P.plan_B(fz)
    print(f"JOB A: {len(planA)} circuits, est {P.estimate_seconds(planA):.1f} s")
    print(f"JOB B: {len(planB)} circuits, est {P.estimate_seconds(planB):.1f} s")


if __name__ == "__main__":
    main()
