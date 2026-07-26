#!/usr/bin/env python3
"""Qubit screening for the re-run, after job A run 1 VOIDed on readout.

Run 1's lesson: the PUBLISHED calibration is not good enough to select on.
On the pinned triple it listed readout errors of 0.4-0.6 % where the device
delivered 0.5 %, 7 % and 10 %, and T1 values 26-53 % longer than the device
delivered in the same job.  So measure, then select.

Three circuits over the union of the candidate triples' qubits:
  |0..0> read           -> P(1|0) per qubit
  |1..1> read           -> P(0|1) per qubit
  |1..1>, idle, read    -> a one-point T1 screen per qubit

Caveat recorded rather than hidden: reading ~20 qubits at once carries more
readout crosstalk than reading 3, so this screen is CONSERVATIVE (it can only
make a qubit look worse than it will be in the real job).

Usage: qenv/bin/python qpu_habit_screen.py [--dry]
"""
import json
import sys
import time

import numpy as np

BACKEND = "ibm_marrakesh"
SHOTS = 4096
T_IDLE_US = 150.016          # dt-aligned
SEED = 20260726


def candidates(props, coupling, n, top=8):
    T1 = {q: props.t1(q) * 1e6 for q in range(n)}
    T2 = {q: props.t2(q) * 1e6 for q in range(n)}
    ro = {q: props.readout_error(q) for q in range(n)}
    cz = {}
    for g in props.gates:
        if g.gate == "cz" and len(g.qubits) == 2:
            try:
                cz[tuple(sorted(g.qubits))] = props.gate_error("cz", g.qubits)
            except Exception:
                pass
    adj = {q: set() for q in range(n)}
    for (i, j) in cz:
        adj[i].add(j); adj[j].add(i)
    out = []
    for c in range(n):
        for a in adj[c]:
            for b in adj[c]:
                if b <= a:
                    continue
                trip = [a, c, b]
                if max(ro[q] for q in trip) > 0.02:
                    continue
                e1 = cz[tuple(sorted((a, c)))]; e2 = cz[tuple(sorted((c, b)))]
                if max(e1, e2) > 0.005:
                    continue
                if not all(80.0 <= T1[q] <= 500.0 for q in trip):
                    continue
                if min(T2[q] for q in trip) < 25.0:
                    continue
                out.append(dict(trip=trip, cost=sum(ro[q] for q in trip) + 10 * (e1 + e2),
                                cz=[e1, e2],
                                T1=[T1[q] for q in trip], T2=[T2[q] for q in trip],
                                ro=[ro[q] for q in trip]))
    out.sort(key=lambda d: d["cost"])
    # keep the best `top` triples that are mutually distinct enough to be worth
    # measuring, plus job A run 1's triple as the control
    picked, seen = [], set()
    for d in out:
        if len(picked) >= top:
            break
        if any(q in seen for q in d["trip"]):
            continue
        picked.append(d); seen.update(d["trip"])
    return picked


def main():
    from qiskit import QuantumCircuit, transpile
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
    svc = QiskitRuntimeService()
    be = svc.backend(BACKEND)
    props = be.properties()
    n = be.num_qubits
    cands = candidates(props, be.coupling_map, n)
    qubits = sorted({q for d in cands for q in d["trip"]} | {13, 14, 15})
    print(f"{len(cands)} candidate triples, {len(qubits)} qubits to screen:")
    for d in cands:
        print("  ", d["trip"], "published ro", [round(x, 4) for x in d["ro"]],
              "T1", [round(x) for x in d["T1"]], "T2", [round(x) for x in d["T2"]])
    idx = {q: i for i, q in enumerate(qubits)}
    nq = len(qubits)

    def build(prep1, delay):
        qc = QuantumCircuit(nq, nq)
        if prep1:
            qc.x(range(nq))
        if delay:
            qc.barrier()
            for k in range(nq):
                qc.delay(T_IDLE_US, k, unit="us")
            qc.barrier()
        qc.measure(range(nq), range(nq))
        return qc

    circs = [build(False, False), build(True, False), build(True, True)]
    tq = [transpile(c, be, optimization_level=1, initial_layout=qubits,
                    seed_transpiler=SEED) for c in circs]
    est = 3 * SHOTS * (252 + T_IDLE_US / 3) * 1e-6
    print(f"estimated {est:.1f} QPU seconds")
    if "--dry" in sys.argv:
        return
    sampler = SamplerV2(mode=be)
    job = sampler.run([(c,) for c in tq], shots=SHOTS)
    print("job id:", job.job_id(), flush=True)
    res = job.result()
    p1 = []
    for i in range(3):
        bs = res[i].data.c.get_bitstrings() if hasattr(res[i].data, "c") else \
            res[i].data.meas.get_bitstrings()
        arr = np.array([[int(s[-1 - k]) for k in range(nq)] for s in bs])
        p1.append(arr.mean(axis=0))
    out = {"backend": BACKEND, "job_id": job.job_id(), "qubits": qubits,
           "shots": SHOTS, "t_idle_us": T_IDLE_US,
           "p1_prep0": p1[0].tolist(), "p1_prep1": p1[1].tolist(),
           "p1_prep1_idle": p1[2].tolist(), "candidates": cands,
           "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    T1est = {}
    print("\n qubit   P(1|0)   P(1|1)   P(1|1,idle)   T1_screen(us)   pub T1")
    for q in qubits:
        i = idx[q]
        a, b, c = p1[0][i], p1[1][i], p1[2][i]
        t1 = float("nan")
        if b > c > 0:
            t1 = T_IDLE_US / np.log(b / max(c, 1e-6))
        T1est[q] = t1
        print(f"  {q:4d}  {a:7.4f}  {b:7.4f}   {c:9.4f}   {t1:11.1f}   "
              f"{props.t1(q)*1e6:7.1f}")
    out["T1_screen_us"] = {str(q): T1est[q] for q in qubits}
    with open("qpu_habit_screen.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved qpu_habit_screen.json")

    # rank the candidate triples on MEASURED readout
    print("\n=== ranking on MEASURED readout ===")
    rows = []
    for d in cands:
        e0 = [float(p1[0][idx[q]]) for q in d["trip"]]
        e1 = [float(1 - p1[1][idx[q]]) for q in d["trip"]]
        worst = max(max(e0), max(e1))
        t1s = [T1est[q] for q in d["trip"]]
        rows.append((worst, d["trip"], e0, e1, t1s, d["cz"]))
    rows.sort()
    for worst, trip, e0, e1, t1s, cz in rows:
        print(f"  {trip}  worst readout {worst:.4f}   P(1|0) "
              f"{[round(x,4) for x in e0]}   P(0|1) {[round(x,4) for x in e1]}"
              f"   T1_screen {[round(x) for x in t1s]}   cz {[round(x,4) for x in cz]}")
    out["ranking"] = [dict(worst_readout=w, trip=t, e0=a, e1=b, T1=c, cz=z)
                      for w, t, a, b, c, z in rows]
    with open("qpu_habit_screen.json", "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
