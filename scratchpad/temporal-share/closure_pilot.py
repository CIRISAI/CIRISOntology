#!/usr/bin/env python3
"""CLOSURE PILOT — instrument for CLOSURE_PILOT_PREREG.md (frozen 2026-08-26).

Gauge check on a ruler: can a directional closure residual be distinguished from its
reverse, for a deliberately ASYMMETRIC coupling? Nothing here tests the stance.

Stage 1 (screen): MEASURED readout fidelity on candidate connected pairs. Never
                  backend.properties() -- house memory qpu-published-calibration-unusable.
Stage 2 (pilot):  2 arms x 4 basis preparations, one job, interleaved.

The statistic and the floor are fixed by the prereg and are not chosen here.
"""
import json, sys, itertools
import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

TOKEN = json.load(open('/home/emoore/Downloads/apikey (1).json'))['apikey']
SCREEN_SHOTS, PILOT_SHOTS = 1024, 4096
THETA = np.pi / 2          # frozen: CRX angle
N_PERM = 500               # frozen: permutation replicates for the floor
CANDIDATE_PAIRS = 8        # connected pairs to screen

def service():
    return QiskitRuntimeService(channel="ibm_quantum_platform", token=TOKEN,
                                instance="open-instance")

def prep(qc, a, b):
    """Computational-basis input, known by PREPARATION and never inferred."""
    if a: qc.x(0)
    if b: qc.x(1)

def make_circuits(tau_dt, coupled):
    """4 basis preparations. `coupled` adds the one-way CRX (0 controls 1)."""
    out = []
    for a, b in itertools.product((0, 1), repeat=2):
        qc = QuantumCircuit(2, 2)
        prep(qc, a, b)
        if coupled:
            qc.crx(THETA, 0, 1)
        qc.barrier()
        qc.delay(tau_dt, unit='dt')
        qc.barrier()
        qc.measure([0, 1], [0, 1])
        qc.metadata = {"a_in": a, "b_in": b, "arm": "P1" if coupled else "P0"}
        out.append(qc)
    return out

def d_js(p, q):
    """Jensen-Shannon divergence in NATS. The frozen statistic."""
    p, q = np.asarray(p, float), np.asarray(q, float)
    m = 0.5 * (p + q)
    def kl(x, y):
        mask = x > 0
        return float(np.sum(x[mask] * np.log(x[mask] / y[mask])))
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)

def residual(counts_by_input, target):
    """Delta_{B->A} (target='A') or Delta_{A->B} (target='B').

    Delta = sum_a (1/2) * D_JS( P(out_target | in_target=a, in_other=0)
                              || P(out_target | in_target=a, in_other=1) )
    Weights are 1/2 by construction, never an observed frequency (prereg S2).
    """
    tot = 0.0
    for held in (0, 1):
        dists = []
        for other in (0, 1):
            key = (held, other) if target == 'A' else (other, held)
            c = counts_by_input[key]
            n = sum(c.values())
            # marginal of the TARGET's output bit
            m = [0.0, 0.0]
            for bits, k in c.items():
                # count string is "c1c0" == "B A": bits[1] is A, bits[0] is B.
                out_bit = int(bits[1]) if target == 'A' else int(bits[0])
                m[out_bit] += k / n
            dists.append(m)
        tot += 0.5 * d_js(dists[0], dists[1])
    return tot

def perm_floor(counts_by_input, target, rng):
    """Permutation floor: shuffle the OTHER input's label within each stratum of the
    target's input, preserving counts. 500 replicates, 95th percentile (prereg S4)."""
    vals = []
    # expand to per-shot arrays once
    strata = {}
    for held in (0, 1):
        rows = []
        for other in (0, 1):
            key = (held, other) if target == 'A' else (other, held)
            for bits, k in counts_by_input[key].items():
                out_bit = int(bits[1]) if target == 'A' else int(bits[0])
                rows += [(other, out_bit)] * k
        strata[held] = np.array(rows, dtype=int)
    for _ in range(N_PERM):
        tot = 0.0
        for held in (0, 1):
            arr = strata[held]
            lab = rng.permutation(arr[:, 0])
            dists = []
            for other in (0, 1):
                sel = arr[lab == other, 1]
                n = len(sel)
                dists.append([np.mean(sel == 0) if n else 0.0,
                              np.mean(sel == 1) if n else 0.0])
            tot += 0.5 * d_js(dists[0], dists[1])
        vals.append(tot)
    return float(np.percentile(vals, 95))

# ---------------------------------------------------------------- stage 1: screen
def screen():
    svc = service()
    bk = svc.least_busy(operational=True, simulator=False)
    edges = sorted({tuple(sorted(e)) for e in bk.coupling_map})
    step = max(1, len(edges) // CANDIDATE_PAIRS)
    cands = edges[::step][:CANDIDATE_PAIRS]
    print(f"backend={bk.name} dt={bk.dt} screening {len(cands)} pairs: {cands}")
    circs, meta = [], []
    for (q0, q1) in cands:
        for a, b in ((0, 0), (1, 1)):
            qc = QuantumCircuit(2, 2); prep(qc, a, b); qc.measure([0, 1], [0, 1])
            circs.append(qc); meta.append({"pair": [q0, q1], "prep": f"{a}{b}"})
    pm_cache = {}
    isa = []
    for qc, m in zip(circs, meta):
        key = tuple(m["pair"])
        if key not in pm_cache:
            pm_cache[key] = generate_preset_pass_manager(
                optimization_level=1, backend=bk, initial_layout=list(key))
        isa.append(pm_cache[key].run(qc))
    job = SamplerV2(mode=bk).run(isa, shots=SCREEN_SHOTS)
    print("screen job:", job.job_id())
    res = job.result()
    out = {}
    for r, m in zip(res, meta):
        c = r.data.c.get_counts()
        want = m["prep"][::-1]  # qiskit bit order
        out.setdefault(tuple(m["pair"]), {})[m["prep"]] = c.get(want, 0) / SCREEN_SHOTS
    best, bestf = None, -1
    for pair, d in out.items():
        f = min(d.values())
        print(f"  pair {pair}: P(00->00)={d.get('00',0):.4f} P(11->11)={d.get('11',0):.4f} worst={f:.4f}")
        if f > bestf: best, bestf = pair, f
    print(f"SELECTED pair={best} worst_fidelity={bestf:.4f}")
    json.dump({"backend": bk.name, "screen_job": job.job_id(), "readings":
               {str(k): v for k, v in out.items()}, "selected": list(best),
               "worst_fidelity": bestf},
              open("closure_pilot_screen.json", "w"), indent=2)

# ---------------------------------------------------------------- stage 2: pilot
def pilot():
    scr = json.load(open("closure_pilot_screen.json"))
    pair = scr["selected"]
    svc = service()
    bk = svc.backend(scr["backend"])
    gran = getattr(bk, "granularity", 16) or 16
    tau = int(gran)   # frozen: shortest supported non-zero delay, in dt
    print(f"backend={bk.name} pair={pair} tau={tau} dt ({tau*bk.dt*1e9:.1f} ns) theta={THETA}")
    circs = make_circuits(tau, False) + make_circuits(tau, True)
    pm = generate_preset_pass_manager(optimization_level=1, backend=bk,
                                      initial_layout=pair)
    isa = [pm.run(c) for c in circs]
    job = SamplerV2(mode=bk).run(isa, shots=PILOT_SHOTS)
    print("pilot job:", job.job_id())
    res = job.result()
    raw = {}
    for r, c in zip(res, circs):
        m = c.metadata
        raw.setdefault(m["arm"], {})[f'{m["a_in"]}{m["b_in"]}'] = r.data.c.get_counts()
    json.dump({"backend": bk.name, "job": job.job_id(), "pair": pair,
               "tau_dt": tau, "tau_ns": tau * bk.dt * 1e9, "theta": THETA,
               "shots": PILOT_SHOTS, "counts": raw},
              open(f"closure_pilot_{job.job_id()}.json", "w"), indent=2)
    print("saved. run: closure_pilot.py analyse <file>")

# ---------------------------------------------------------------- stage 3: analyse
def analyse(path):
    d = json.load(open(path))
    rng = np.random.default_rng(20260826)
    print(f"backend={d['backend']} pair={d['pair']} tau={d['tau_ns']:.1f}ns "
          f"theta={d['theta']:.4f} shots={d['shots']}")
    print(f"{'arm':>4} {'D_A->B':>12} {'floor':>10} {'D_B->A':>12} {'floor':>10}")
    verdict = {}
    for arm in ("P0", "P1"):
        cbi = {(int(k[0]), int(k[1])): v for k, v in d["counts"][arm].items()}
        dab = residual(cbi, 'B'); fab = perm_floor(cbi, 'B', rng)
        dba = residual(cbi, 'A'); fba = perm_floor(cbi, 'A', rng)
        print(f"{arm:>4} {dab:12.6e} {fab:10.3e} {dba:12.6e} {fba:10.3e}")
        verdict[arm] = {"d_ab": dab, "floor_ab": fab, "d_ba": dba, "floor_ba": fba,
                        "ab_above": bool(dab > fab), "ba_above": bool(dba > fba)}
    p0, p1 = verdict["P0"], verdict["P1"]
    if p0["ab_above"] or p0["ba_above"]:
        v = "DIRTY BASELINE"
    elif p1["ab_above"] and not p1["ba_above"]:
        v = "SEPARABLE"
    elif p1["ba_above"] and not p1["ab_above"]:
        v = "BACKWARDS"
    else:
        v = "NOT SEPARABLE"
    print(f"\nVERDICT: {v}")
    json.dump({**d, "analysis": verdict, "verdict": v},
              open(path.replace(".json", "_verdict.json"), "w"), indent=2)

if __name__ == "__main__":
    {"screen": screen, "pilot": pilot,
     "analyse": lambda: analyse(sys.argv[2])}[sys.argv[1]]()
