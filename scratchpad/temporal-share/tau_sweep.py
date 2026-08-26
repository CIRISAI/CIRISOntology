#!/usr/bin/env python3
"""TAU SWEEP — instrument for TAU_SWEEP_PREREG.md (frozen 2026-08-26).

Is the idle pair's cross-residual dynamical or preparational? Independent decay is a
PRODUCT map and `independent_views_closed` proves both views close under every product
map, so decoherence cannot manufacture a cross-residual. Growth with tau is coupling;
flatness is fixed cost at preparation or readout.

closure_pilot.py is NOT modified: it produced a recorded result and is frozen. The
shared statistic is imported from it; the floor here is the prereg's corrected one.
"""
import json, sys, itertools, importlib.util
import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

_spec = importlib.util.spec_from_file_location("cp", "closure_pilot.py")
cp = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(cp)

TOKEN = json.load(open('/home/emoore/Downloads/apikey (1).json'))['apikey']
SHOTS = 4096
TAUS_DT = [16, 64, 256, 1024, 4096, 16384]      # frozen
N_PERM = 2000                                    # frozen: up from 500
N_TESTS = 12                                     # 2 directions x 6 delays
PCTL = 100.0 * (1.0 - 0.05 / N_TESTS)            # frozen: 99.583, Bonferroni FWER 0.05

def service():
    return QiskitRuntimeService(channel="ibm_quantum_platform", token=TOKEN,
                                instance="open-instance")

def perm_floor(counts_by_input, target, rng):
    """Same permutation scheme as the pilot, at the CORRECTED percentile."""
    strata = {}
    for held in (0, 1):
        rows = []
        for other in (0, 1):
            key = (held, other) if target == 'A' else (other, held)
            for bits, k in counts_by_input[key].items():
                out_bit = int(bits[1]) if target == 'A' else int(bits[0])
                rows += [(other, out_bit)] * k
        strata[held] = np.array(rows, dtype=int)
    vals = []
    for _ in range(N_PERM):
        tot = 0.0
        for held in (0, 1):
            arr = strata[held]
            lab = rng.permutation(arr[:, 0])
            d = []
            for other in (0, 1):
                sel = arr[lab == other, 1]; n = len(sel)
                d.append([np.mean(sel == 0) if n else 0.0, np.mean(sel == 1) if n else 0.0])
            tot += 0.5 * cp.d_js(d[0], d[1])
        vals.append(tot)
    return float(np.percentile(vals, PCTL))

def spearman(x, y):
    """rho and a two-sided permutation p — no scipy dependency."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    # Ties disclosed BEFORE any early return, per house rule -- printing the wrong
    # row's tie fraction is worse than printing none.
    print(f"    [spearman] tied fraction: x={1 - len(np.unique(x))/len(x):.3f} "
          f"y={1 - len(np.unique(y))/len(y):.3f}")
    def rank(v):
        # AVERAGE ranks for ties. argsort alone assigns 0..n-1 to a CONSTANT series,
        # which made a flat curve read rho=1.000, p=0.003 -- classifying
        # PREPARATIONAL as DYNAMICAL, the exact inversion of the verdict. Caught by
        # the planted flat series before any data. House rule: disclose the tied
        # fraction before believing any rank-based statistic.
        v = np.asarray(v, float)
        o = np.argsort(v, kind="mergesort")
        r = np.empty(len(v), float); r[o] = np.arange(len(v), dtype=float)
        for val in np.unique(v):
            m = v == val
            if m.sum() > 1:
                r[m] = r[m].mean()
        return r
    rx, ry = rank(x), rank(y)
    if np.std(rx) == 0 or np.std(ry) == 0:
        return 0.0, 1.0          # no variation => no trend, not a perfect one
    rho = float(np.corrcoef(rx, ry)[0, 1])
    rng = np.random.default_rng(20260826)
    null = [abs(np.corrcoef(rx, rng.permutation(ry))[0, 1]) for _ in range(20000)]
    return rho, float((np.sum(np.array(null) >= abs(rho)) + 1) / (len(null) + 1))

def run():
    scr = json.load(open("closure_pilot_screen.json"))
    pair = scr["selected"]
    svc = service(); bk = svc.backend(scr["backend"])
    print(f"backend={bk.name} pair={pair} taus_dt={TAUS_DT} floor_pctl={PCTL:.3f}")
    circs = []
    for tau in TAUS_DT:
        for a, b in itertools.product((0, 1), repeat=2):
            qc = QuantumCircuit(2, 2)
            if a: qc.x(0)
            if b: qc.x(1)
            qc.barrier(); qc.delay(tau, unit='dt'); qc.barrier()
            qc.measure([0, 1], [0, 1])
            qc.metadata = {"tau": tau, "a_in": a, "b_in": b}
            circs.append(qc)
    pm = generate_preset_pass_manager(optimization_level=1, backend=bk, initial_layout=pair)
    isa = [pm.run(c) for c in circs]
    job = SamplerV2(mode=bk).run(isa, shots=SHOTS)
    print("tau-sweep job:", job.job_id())
    res = job.result()
    raw = {}
    for r, c in zip(res, circs):
        m = c.metadata
        raw.setdefault(str(m["tau"]), {})[f'{m["a_in"]}{m["b_in"]}'] = r.data.c.get_counts()
    json.dump({"backend": bk.name, "job": job.job_id(), "pair": pair, "shots": SHOTS,
               "taus_dt": TAUS_DT, "tau_ns": [t * bk.dt * 1e9 for t in TAUS_DT],
               "floor_pctl": PCTL, "n_perm": N_PERM, "counts": raw},
              open(f"tau_sweep_{job.job_id()}.json", "w"), indent=2)
    print("saved.")

def analyse(path):
    d = json.load(open(path)); rng = np.random.default_rng(20260826)
    print(f"backend={d['backend']} pair={d['pair']} floor at {d['floor_pctl']:.3f} pctl, "
          f"{d['n_perm']} perms")
    print(f"{'tau_ns':>10} {'D_A->B':>12} {'floor':>10} {'D_B->A':>12} {'floor':>10}")
    rows = []
    for tau, tns in zip(d["taus_dt"], d["tau_ns"]):
        cbi = {(int(k[0]), int(k[1])): v for k, v in d["counts"][str(tau)].items()}
        ab, fab = cp.residual(cbi, 'B'), perm_floor(cbi, 'B', rng)
        ba, fba = cp.residual(cbi, 'A'), perm_floor(cbi, 'A', rng)
        print(f"{tns:10.1f} {ab:12.4e} {fab:10.3e} {ba:12.4e} {fba:10.3e}"
              f"{'   <-- B->A ABOVE' if ba > fba else ''}"
              f"{'   <-- A->B ABOVE' if ab > fab else ''}")
        rows.append({"tau_ns": tns, "d_ab": ab, "f_ab": fab, "d_ba": ba, "f_ba": fba,
                     "ab_above": bool(ab > fab), "ba_above": bool(ba > fba)})
    any_above = any(r["ba_above"] or r["ab_above"] for r in rows)
    rho, p = spearman([r["tau_ns"] for r in rows], [r["d_ba"] for r in rows])
    print(f"\nSpearman(tau, D_B->A): rho={rho:+.4f}  p={p:.4f}")
    if not any_above:
        v = "CLEAN"
    elif rho > 0 and p < 0.05:
        v = "DYNAMICAL"
    else:
        v = "PREPARATIONAL"
    print(f"VERDICT: {v}")
    json.dump({**d, "rows": rows, "spearman_rho": rho, "spearman_p": p, "verdict": v},
              open(path.replace(".json", "_verdict.json"), "w"), indent=2)

if __name__ == "__main__":
    {"run": run, "analyse": lambda: analyse(sys.argv[2])}[sys.argv[1]]()
