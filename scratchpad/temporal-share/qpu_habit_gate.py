#!/usr/bin/env python3
"""Simulator gate for the QPU habit-lifecycle run.  MUST PASS BEFORE HARDWARE.

Two stages, exactly as BELL_PREREG.md's gate (which caught a control defect
before hardware and saved the run):

  (a) IDEAL Aer — do the circuits MEAN what the prereg says?  Every arm's
      ideal share is a machine-checked or exactly-computed number.
  (b) NOISY Aer — a noise model hand-built from the FROZEN calibration of the
      three pinned qubits (1q/2q depolarizing, per-qubit readout asymmetry,
      thermal relaxation on every delay).  Its output is what the hardware
      criteria are staked against.  Run-1 lesson: the band comes from here,
      never from (a).

Usage: qenv/bin/python qpu_habit_gate.py [shots_scale]
"""
import itertools
import json
import math
import sys

import numpy as np

import qpu_habit_pipeline as P

LN2 = math.log(2.0)
fz = P.load_freeze()
P_EXC = fz.get("p_exc_nominal", 0.01)
SL = fz["slots_abc"]                      # [a, b, c] physical
T1 = [fz["cal"]["T1_us"][str(q)] for q in SL]
T2 = [fz["cal"]["T2_us"][str(q)] for q in SL]
E0 = [fz["cal"]["prob_meas1_prep0"][str(q)] for q in SL]
E1 = [fz["cal"]["prob_meas0_prep1"][str(q)] for q in SL]
CZ = list(fz["cal"]["cz_error"].values())

# circuit qubit index -> slot: q0=a(slot0), q1=c(slot2), q2=b(slot1)
Q2SLOT = {0: 0, 1: 2, 2: 1}


def noise_model(delay_us):
    """Calibration-matched 3-qubit noise model; `delay_us` sets the thermal
    relaxation attached to the delay instruction (one duration per circuit)."""
    from qiskit_aer.noise import (NoiseModel, ReadoutError, depolarizing_error,
                                  thermal_relaxation_error)
    nm = NoiseModel(basis_gates=["id", "sx", "x", "rz", "cz", "delay", "reset"])
    for k in range(3):
        s = Q2SLOT[k]
        nm.add_readout_error(ReadoutError([[1 - E0[s], E0[s]], [E1[s], 1 - E1[s]]]), [k])
        nm.add_quantum_error(depolarizing_error(1e-4, 1), ["sx", "x"], [k])
        if delay_us and delay_us > 0:
            nm.add_quantum_error(
                thermal_relaxation_error(T1[s] * 1e-6, min(T2[s], 2 * T1[s]) * 1e-6,
                                         delay_us * 1e-6, excited_state_population=P_EXC),
                ["delay"], [k])
        # measurement and reset take ~2.2 us of real time each
        nm.add_quantum_error(
            thermal_relaxation_error(T1[s] * 1e-6, min(T2[s], 2 * T1[s]) * 1e-6,
                                     2.2e-6, excited_state_population=P_EXC),
            ["reset"], [k])
    for k, (i, j) in enumerate(((0, 1), (1, 2))):
        e = CZ[k]
        nm.add_quantum_error(depolarizing_error(e, 2), ["cz"], [i, j])
        nm.add_quantum_error(depolarizing_error(e, 2), ["cz"], [j, i])
    return nm


def circuit_delay_us(qc):
    ds = set()
    for inst in qc.data:
        if inst.operation.name == "delay":
            v = inst.operation.params[0]
            u = inst.operation.unit
            ds.add(v if u == "us" else (v * 1e6 if u == "s" else v * 4e-3))
    ds.discard(0.0)
    if len(ds) > 1:
        raise ValueError(f"circuit has multiple delay durations {ds}")
    return (ds.pop() if ds else 0.0)


def run(plan, noisy, shots_scale=1.0):
    from qiskit import transpile
    from qiskit_aer import AerSimulator
    out = {}
    groups = {}
    for tag, qc, shots in plan:
        groups.setdefault(circuit_delay_us(qc), []).append((tag, qc, shots))
    for dur, items in groups.items():
        nm = noise_model(dur) if noisy else None
        sim = AerSimulator(noise_model=nm) if noisy else AerSimulator()
        circs = [transpile(qc, sim, basis_gates=["id", "sx", "x", "rz", "cz",
                                                 "delay", "reset", "measure"],
                           optimization_level=0) for _, qc, _ in items]
        for (tag, _, shots), qc in zip(items, circs):
            r = sim.run(qc, shots=max(64, int(shots * shots_scale))).result()
            cnt = r.get_counts()
            # keep only the 'c' register (leftmost group when several cregs)
            fixed = {}
            for k, v in cnt.items():
                parts = k.split(" ")
                key = parts[-1] if len(parts) > 1 else k
                fixed[key] = fixed.get(key, 0) + v
            out[tag] = fixed
    return out


def summarize(counts, label):
    print(f"\n--- {label} ---")
    rows = {}
    amats = None
    if "A8|cal|000|0" in counts:
        amats = P.assignment_matrices(P.counts_to_p(counts["A8|cal|000|0"]).ravel(),
                                      P.counts_to_p(counts["A8|cal|111|0"]).ravel())
    if "B3|cal|000|0" in counts:
        amats = P.assignment_matrices(P.counts_to_p(counts["B3|cal|000|0"]).ravel(),
                                      P.counts_to_p(counts["B3|cal|111|0"]).ravel())
    for tag in sorted(counts):
        p = P.counts_to_p(counts[tag])
        sh, st, D = P.share(p), P.s_total(p), P.D_stat(p)
        shc = stc = float("nan")
        if amats is not None:
            pc = P.correct_readout(p, amats)
            pc = np.clip(pc, 0, None); pc = pc / pc.sum()
            shc, stc = P.share(pc), P.s_total(pc)
        rows[tag] = dict(share_raw=sh, share_corr=shc, S_total_raw=st,
                         S_total_corr=stc, D_raw=D)
        print(f"  {tag:28s} share {sh:9.5f} (corr {shc:9.5f})  S_tot {st:8.5f}"
              f"  D {D:8.5f}")
    return rows


def main():
    scale = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    planA = P.plan_A(fz)
    planB = P.plan_B(fz)
    res = {}

    ideal_A = summarize(run(planA, noisy=False, shots_scale=scale), "JOB A — IDEAL")
    ideal_B = summarize(run(planB, noisy=False, shots_scale=scale), "JOB B — IDEAL")

    ok = True
    def chk(name, got, want, tol):
        nonlocal ok
        good = abs(got - want) <= tol
        ok = ok and good
        print(f"  [{'ok ' if good else 'FAIL'}] {name}: {got:.5f} vs {want:.5f} +-{tol}")
        return good

    print("\n=== IDEAL GATE CHECKS (the circuits must mean what the prereg says) ===")
    d0 = fz["delays_classical_us"][0]
    chk("A1 classical/Z at t=0 = ln2", ideal_A[f"A1|classical|ZZZ|{d0}"]["share_raw"], LN2, 0.01)
    chk("A1 classical/Z at t=max = ln2 (no noise)",
        ideal_A[f"A1|classical|ZZZ|{fz['delays_classical_us'][-1]}"]["share_raw"], LN2, 0.01)
    chk("A2 ghz/X at t=0 = ln2", ideal_A[f"A2|ghz|XXX|{fz['delays_quantum_us'][0]}"]["share_raw"], LN2, 0.01)
    chk("A3 ghz/YXX at t=0 = 0 (phase is real at t=0)",
        ideal_A[f"A3|ghz|YXX|{fz['delays_quantum_us'][0]}"]["share_raw"], 0.0, 0.01)
    chk("A4 ghz/Z = 0 (ferro reading, sign-symmetric)",
        ideal_A[f"A4|ghz|ZZZ|{fz['delays_control_us'][0]}"]["share_raw"], 0.0, 0.005)
    chk("A4 ghz/Z S_total = 2 ln2",
        ideal_A[f"A4|ghz|ZZZ|{fz['delays_control_us'][0]}"]["S_total_raw"], 2 * LN2, 0.02)
    chk("A5 classical/X = 0 (a diagonal state has no X-moments)",
        ideal_A[f"A5|classical|XXX|{fz['delays_control_us'][0]}"]["share_raw"], 0.0, 0.005)
    chk("A6 product/Z = 0", ideal_A[f"A6|product|ZZZ|{fz['delays_product_us'][0]}"]["share_raw"], 0.0, 0.005)
    chk("B1 MINT parity share = ln2 (repair_creates_parity)",
        ideal_B["B1|mint|parity|0"]["share_raw"], LN2, 0.01)
    chk("B1 MINT parity S_total = ln2 (S_total_parityRepair)",
        ideal_B["B1|mint|parity|0"]["S_total_raw"], LN2, 0.01)
    chk("B1 COPY share = 0 (wrong code mints no whole-only share)",
        ideal_B["B1|mint|copy|0"]["share_raw"], 0.0, 0.005)
    chk("B1 COPY S_total = ln2", ideal_B["B1|mint|copy|0"]["S_total_raw"], LN2, 0.01)
    chk("B1 NONE share = 0 (false-positive floor)",
        ideal_B["B1|mint|none|0"]["share_raw"], 0.0, 0.005)
    for T in fz["rent_totals_us"]:
        for n in (1, 2, 4):
            chk(f"B2 rent n={n} T={T} share = ln2 (no noise)",
                ideal_B[f"B2|rent|{n}|{T}"]["share_raw"], LN2, 0.01)
        chk(f"B2 default n=0 T={T} share = ln2 (no noise)",
            ideal_B[f"B2|rent|0|{T}"]["share_raw"], LN2, 0.01)

    noisy_A = summarize(run(planA, noisy=True, shots_scale=scale), "JOB A — NOISY (calibration-matched)")
    noisy_B = summarize(run(planB, noisy=True, shots_scale=scale), "JOB B — NOISY (calibration-matched)")

    res = {"ideal_A": ideal_A, "ideal_B": ideal_B,
           "noisy_A": noisy_A, "noisy_B": noisy_B, "ideal_gate_pass": ok}
    with open("qpu_habit_gate.json", "w") as f:
        json.dump(res, f, indent=2, default=float)
    print("\nGATE (ideal):", "PASS" if ok else "FAIL")
    print("saved qpu_habit_gate.json")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
