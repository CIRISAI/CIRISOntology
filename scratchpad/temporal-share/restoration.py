#!/usr/bin/env python3
"""RESTORATION — instrument for RESTORATION_PREREG.md (frozen 2026-08-26).

Tests the 2x2 MatterCoupling claims: neither marginal closes under coupling, but a
LOSSY joint view is Held where a conserved quantity exists and not otherwise.

closure_pilot.py and tau_sweep.py are NOT modified; both produced recorded results.
"""
import json, sys, itertools, importlib.util
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import XXPlusYYGate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

_s = importlib.util.spec_from_file_location("cp", "closure_pilot.py")
cp = importlib.util.module_from_spec(_s); _s.loader.exec_module(cp)

TOKEN = json.load(open('/home/emoore/Downloads/apikey (1).json'))['apikey']
SHOTS, THETA, TAU_DT = 4096, np.pi / 2, 16
N_PERM, N_TESTS = 2000, 6
PCTL = 100.0 * (1.0 - 0.05 / N_TESTS)          # frozen: 99.167

def n_of(bits):  # total excitation number; symmetric, so bit ORDER cannot corrupt it
    return bits.count('1')

def joint_residual(counts_by_input):
    """D_JS( P(n_out | in=01) || P(n_out | in=10) ) -- the two states inside n=1's fiber."""
    dists = []
    for key in ((0, 1), (1, 0)):
        c = counts_by_input[key]; tot = sum(c.values()); m = [0.0, 0.0, 0.0]
        for bits, k in c.items():
            m[n_of(bits)] += k / tot
        dists.append(m)
    return cp.d_js(dists[0], dists[1])

def joint_floor(counts_by_input, rng):
    """Shuffle the WITHIN-FIBER label, preserving the pooled n=1 output distribution."""
    rows = []
    for lab, key in enumerate(((0, 1), (1, 0))):
        for bits, k in counts_by_input[key].items():
            rows += [(lab, n_of(bits))] * k
    arr = np.array(rows, dtype=int)
    vals = []
    for _ in range(N_PERM):
        lab = rng.permutation(arr[:, 0]); d = []
        for l in (0, 1):
            sel = arr[lab == l, 1]; n = len(sel)
            d.append([np.mean(sel == v) if n else 0.0 for v in (0, 1, 2)])
        vals.append(cp.d_js(d[0], d[1]))
    return float(np.percentile(vals, PCTL))

def marg_floor(counts_by_input, target, rng):
    strata = {}
    for held in (0, 1):
        rows = []
        for other in (0, 1):
            key = (held, other) if target == 'A' else (other, held)
            for bits, k in counts_by_input[key].items():
                rows += [(other, int(bits[1]) if target == 'A' else int(bits[0]))] * k
        strata[held] = np.array(rows, dtype=int)
    vals = []
    for _ in range(N_PERM):
        tot = 0.0
        for held in (0, 1):
            arr = strata[held]; lab = rng.permutation(arr[:, 0]); d = []
            for other in (0, 1):
                sel = arr[lab == other, 1]; n = len(sel)
                d.append([np.mean(sel == 0) if n else 0.0, np.mean(sel == 1) if n else 0.0])
            tot += 0.5 * cp.d_js(d[0], d[1])
        vals.append(tot)
    return float(np.percentile(vals, PCTL))

def arm_circuits(arm):
    out = []
    for a, b in itertools.product((0, 1), repeat=2):
        qc = QuantumCircuit(2, 2)
        if a: qc.x(0)
        if b: qc.x(1)
        if arm == "J":
            qc.append(XXPlusYYGate(THETA), [0, 1])
        else:
            qc.crx(THETA, 0, 1); qc.crx(THETA, 1, 0)
        qc.barrier(); qc.delay(TAU_DT, unit='dt'); qc.barrier()
        qc.measure([0, 1], [0, 1])
        qc.metadata = {"arm": arm, "a_in": a, "b_in": b}
        out.append(qc)
    return out

def run():
    scr = json.load(open("closure_pilot_screen.json")); pair = scr["selected"]
    svc = QiskitRuntimeService(channel="ibm_quantum_platform", token=TOKEN,
                               instance="open-instance")
    bk = svc.backend(scr["backend"])
    print(f"backend={bk.name} pair={pair} theta={THETA:.4f} tau={TAU_DT}dt floor_pctl={PCTL:.3f}")
    circs = arm_circuits("J") + arm_circuits("R")
    pm = generate_preset_pass_manager(optimization_level=1, backend=bk, initial_layout=pair)
    job = SamplerV2(mode=bk).run([pm.run(c) for c in circs], shots=SHOTS)
    print("restoration job:", job.job_id())
    res = job.result(); raw = {}
    for r, c in zip(res, circs):
        m = c.metadata
        raw.setdefault(m["arm"], {})[f'{m["a_in"]}{m["b_in"]}'] = r.data.c.get_counts()
    json.dump({"backend": bk.name, "job": job.job_id(), "pair": pair, "shots": SHOTS,
               "theta": THETA, "tau_dt": TAU_DT, "floor_pctl": PCTL, "counts": raw},
              open(f"restoration_{job.job_id()}.json", "w"), indent=2)
    print("saved.")

def score(counts, rng):
    out = {}
    for arm in ("J", "R"):
        cbi = {(int(k[0]), int(k[1])): v for k, v in counts[arm].items()}
        out[arm] = {
            "d_ab": cp.residual(cbi, 'B'), "f_ab": marg_floor(cbi, 'B', rng),
            "d_ba": cp.residual(cbi, 'A'), "f_ba": marg_floor(cbi, 'A', rng),
            "d_joint": joint_residual(cbi), "f_joint": joint_floor(cbi, rng)}
    return out

def verdict(sc):
    marg_ok = all(sc[a][f"d_{d}"] > sc[a][f"f_{d}"] for a in ("J", "R") for d in ("ab", "ba"))
    j_closed = sc["J"]["d_joint"] <= sc["J"]["f_joint"]
    r_open = sc["R"]["d_joint"] > sc["R"]["f_joint"]
    if not marg_ok: return "MARGINALS SURVIVE (VOID)"
    if not r_open:  return "JOINT CLOSURE IS GENERIC"
    if not j_closed: return "RESTORATION FAILS"
    return "RESTORATION"

def analyse(path):
    d = json.load(open(path)); rng = np.random.default_rng(20260826)
    sc = score(d["counts"], rng)
    print(f"{'arm':>4} {'D_A->B':>11} {'floor':>10} {'D_B->A':>11} {'floor':>10} {'D_joint':>11} {'floor':>10}")
    for a in ("J", "R"):
        v = sc[a]
        print(f"{a:>4} {v['d_ab']:11.4e} {v['f_ab']:10.3e} {v['d_ba']:11.4e} {v['f_ba']:10.3e} "
              f"{v['d_joint']:11.4e} {v['f_joint']:10.3e}"
              f"{'  joint CLOSED' if v['d_joint']<=v['f_joint'] else '  joint OPEN'}")
    vd = verdict(sc); print(f"\nVERDICT: {vd}")
    json.dump({**d, "scores": sc, "verdict": vd},
              open(path.replace(".json", "_verdict.json"), "w"), indent=2)

if __name__ == "__main__":
    {"run": run, "analyse": lambda: analyse(sys.argv[2])}[sys.argv[1]]()
