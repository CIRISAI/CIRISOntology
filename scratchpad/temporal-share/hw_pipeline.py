#!/usr/bin/env python3
"""Phase-3 pipeline: the whole-only share of a natural process on quantum hardware.

Implements exactly what HW_PREREG.md registers — estimator (IPF max-ent share,
natural log), circuits (idle basis-grid + one-remembered-bit positive control +
memoryless negative control), nulls (parametric bootstrap floor from sigma*,
max-statistic over the basis grid, matched negative control), and the simulator
gate that must pass before any hardware job.

Usage:
  qenv/bin/python hw_pipeline.py gate          # simulator gate (Aer), no hardware
  qenv/bin/python hw_pipeline.py hardware      # submit the ONE pre-registered job
  qenv/bin/python hw_pipeline.py analyze F.json# analyze saved hardware counts
"""
import json
import sys
import math
import numpy as np

LN2 = math.log(2.0)
SHOTS = 4096
BOOT_B = 1000
IPF_TOL = 1e-12
IPF_MAX = 5000
RNG = np.random.default_rng(20260724)

# ---------------------------------------------------------------- estimator

def entropy(p):
    p = np.asarray(p, dtype=float)
    nz = p > 0
    return float(-(p[nz] * np.log(p[nz])).sum())

def pair_marginals(p):
    """p is shape (2,2,2) indexed [z1,z2,z3]."""
    return p.sum(axis=2), p.sum(axis=1), p.sum(axis=0)  # m12, m13, m23

def ipf_maxent(m12, m13, m23):
    """Max-entropy joint with the three given pair marginals (IPF)."""
    q = np.full((2, 2, 2), 1.0 / 8.0)
    for _ in range(IPF_MAX):
        q12 = q.sum(axis=2)
        q = q * np.where(q12 > 0, m12 / np.where(q12 > 0, q12, 1), 0)[:, :, None]
        q13 = q.sum(axis=1)
        q = q * np.where(q13 > 0, m13 / np.where(q13 > 0, q13, 1), 0)[:, None, :]
        q23 = q.sum(axis=0)
        q = q * np.where(q23 > 0, m23 / np.where(q23 > 0, q23, 1), 0)[None, :, :]
        d12, d13, d23 = pair_marginals(q)
        err = max(abs(d12 - m12).max(), abs(d13 - m13).max(), abs(d23 - m23).max())
        if err < IPF_TOL:
            break
    return q

def share(p):
    """The mechanized definition, numerically: H(sigma*) - H(p)."""
    m12, m13, m23 = pair_marginals(p)
    return entropy(ipf_maxent(m12, m13, m23)) - entropy(p)

def sample_dist(p, shots, rng):
    flat = p.reshape(-1)
    flat = np.clip(flat, 0, None)
    flat = flat / flat.sum()
    counts = rng.multinomial(shots, flat)
    return (counts / shots).reshape(2, 2, 2)

def bootstrap_floor(p_hat, shots, rng, B=BOOT_B):
    """Estimator-bias floor: the share estimator on samples from sigma*(p_hat),
    whose true share is zero by construction."""
    m12, m13, m23 = pair_marginals(p_hat)
    sigma = ipf_maxent(m12, m13, m23)
    return np.array([share(sample_dist(sigma, shots, rng)) for _ in range(B)])

def bootstrap_self(p_hat, shots, rng, B=BOOT_B):
    """Nonparametric spread of the estimator around p_hat itself."""
    return np.array([share(sample_dist(p_hat, shots, rng)) for _ in range(B)])

# ---------------------------------------------------------------- circuits

def counts_to_dist(counts):
    """Qiskit count keys are little-endian over classical bits c2 c1 c0 with
    c0 = z1, c1 = z2, c2 = z3. Returns p[z1,z2,z3]."""
    p = np.zeros((2, 2, 2))
    total = 0
    for key, n in counts.items():
        bits = key.replace(" ", "")
        z1, z2, z3 = int(bits[-1]), int(bits[-2]), int(bits[-3])
        p[z1, z2, z3] += n
        total += n
    return p / total

def _rot(qc, q, basis):
    if basis == "X":
        qc.h(q)
    elif basis == "Y":
        qc.sdg(q)
        qc.h(q)

def _rot_inv(qc, q, basis):
    if basis == "X":
        qc.h(q)
    elif basis == "Y":
        qc.h(q)
        qc.s(q)

def idle_circuit(bases, delay_ns):
    """One qubit, prepared |+>, measured at three times in the given bases,
    free (natural) evolution of duration delay_ns between events."""
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(1, 3)
    qc.h(0)
    for k, b in enumerate(bases):
        if k > 0 and delay_ns > 0:
            qc.delay(delay_ns, 0, unit="ns")
        _rot(qc, 0, b)
        qc.measure(0, k)
        _rot_inv(qc, 0, b)
    qc.metadata = {"kind": "idle", "bases": "".join(bases), "delay_ns": delay_ns}
    return qc

def positive_control(delay_ns):
    """memory_realizes_parity as a circuit: one remembered bit makes z3 = z1 xor z2."""
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(2, 3)
    qc.h(0)
    qc.cx(0, 1)          # remember z1-to-be
    qc.measure(0, 0)     # z1
    if delay_ns > 0:
        qc.delay(delay_ns, 0, unit="ns")
    qc.h(0)              # fresh fair coin
    qc.measure(0, 1)     # z2
    if delay_ns > 0:
        qc.delay(delay_ns, 0, unit="ns")
    qc.cx(0, 1)          # memory now z1 xor z2
    qc.measure(1, 2)     # z3
    qc.metadata = {"kind": "positive", "delay_ns": delay_ns}
    return qc

def negative_control(delay_ns):
    """Memoryless chain with the same event structure: iid fair bits."""
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(1, 3)
    qc.h(0)
    qc.measure(0, 0)
    if delay_ns > 0:
        qc.delay(delay_ns, 0, unit="ns")
    qc.h(0)
    qc.measure(0, 1)
    if delay_ns > 0:
        qc.delay(delay_ns, 0, unit="ns")
    qc.h(0)
    qc.measure(0, 2)
    qc.metadata = {"kind": "negative", "delay_ns": delay_ns}
    return qc

DELAYS = [0, 2000]  # ns, per prereg
BASES3 = [(a, b, c) for a in "XYZ" for b in "XYZ" for c in "XYZ"]

def all_circuits():
    circs = []
    for d in DELAYS:
        for bases in BASES3:
            circs.append(idle_circuit(list(bases), d))
        circs.append(positive_control(d))
        circs.append(negative_control(d))
    return circs

# ---------------------------------------------------------------- analysis

def analyze(records):
    """records: list of dicts {kind, bases, delay_ns, counts}. Applies the
    pre-registered decision rules; returns a verdict dict."""
    out = {"per_circuit": [], "verdict": {}}
    idle = {d: [] for d in DELAYS}
    controls = {}
    for rec in records:
        p_hat = counts_to_dist(rec["counts"])
        s = share(p_hat)
        floor = bootstrap_floor(p_hat, SHOTS, RNG)
        row = {
            "kind": rec["kind"], "bases": rec.get("bases", "ZZZ"),
            "delay_ns": rec["delay_ns"], "share": s,
            "floor99": float(np.quantile(floor, 0.99)),
            "floor_mean": float(floor.mean()), "floor_std": float(floor.std()),
        }
        if rec["kind"] == "positive":
            spread = bootstrap_self(p_hat, SHOTS, RNG)
            row["self_std"] = float(spread.std())
            controls[("positive", rec["delay_ns"])] = row
        elif rec["kind"] == "negative":
            controls[("negative", rec["delay_ns"])] = row
        else:
            row["floor_samples"] = floor
            idle[rec["delay_ns"]].append(row)
        out["per_circuit"].append(row)

    verdict = {}
    for d in DELAYS:
        pos = controls[("positive", d)]
        neg = controls[("negative", d)]
        pos_ok = abs(pos["share"] - LN2) <= 3 * max(pos["self_std"], 1e-9) + 0.05
        neg_ok = neg["share"] <= neg["floor99"] + 0.01
        rows = idle[d]
        max_share = max(r["share"] for r in rows)
        # max-statistic null: max over the 27 per-basis floors within replicates
        M = np.stack([r["floor_samples"] for r in rows])  # 27 x B
        max_null = M.max(axis=0)
        p_emp = float((max_null >= max_share).mean())
        clears_neg = max_share > neg["share"] + 3 * neg["floor_std"]
        verdict[f"delay_{d}ns"] = {
            "positive_control_ok": bool(pos_ok), "positive_share": pos["share"],
            "negative_control_ok": bool(neg_ok), "negative_share": neg["share"],
            "idle_max_share": float(max_share),
            "idle_max_basis": max(rows, key=lambda r: r["share"])["bases"],
            "max_null_99": float(np.quantile(max_null, 0.99)),
            "empirical_p": p_emp,
            "clears_bootstrap_floor": bool(p_emp < 0.01),
            "clears_negative_control": bool(clears_neg),
            "effect_above_sensitivity": bool(max_share >= 0.01),
            "claim": bool(pos_ok and neg_ok and p_emp < 0.01 and clears_neg
                          and max_share >= 0.01),
        }
    for row in out["per_circuit"]:
        row.pop("floor_samples", None)
    out["verdict"] = verdict
    return out

# ---------------------------------------------------------------- runners

def run_gate():
    """Simulator gate per prereg: (a) ideal positive ~ ln2, (b) ideal negative
    in floor, (c) noisy positive still clears floors; plus ideal idle sweep."""
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel, ReadoutError, depolarizing_error
    from qiskit import transpile

    def execute(circs, backend):
        tqc = transpile(circs, backend)
        result = backend.run(tqc, shots=SHOTS).result()
        recs = []
        for i, qc in enumerate(circs):
            md = qc.metadata
            recs.append({"kind": md["kind"], "bases": md.get("bases", "ZZZ"),
                         "delay_ns": md["delay_ns"],
                         "counts": result.get_counts(i)})
        return recs

    print("== simulator gate ==")
    ideal = AerSimulator()
    recs = execute(all_circuits(), ideal)
    res = analyze(recs)
    ok = True
    for d in DELAYS:
        v = res["verdict"][f"delay_{d}ns"]
        a = v["positive_control_ok"]
        b = v["negative_control_ok"]
        idle_quiet = not v["clears_bootstrap_floor"]
        print(f"ideal d={d}ns: positive {v['positive_share']:.4f} (ln2={LN2:.4f}) ok={a}; "
              f"negative {v['negative_share']:.4f} ok={b}; "
              f"idle max {v['idle_max_share']:.4f} (null99 {v['max_null_99']:.4f}) quiet={idle_quiet}")
        ok = ok and a and b and idle_quiet

    noise = NoiseModel()
    ro = ReadoutError([[0.98, 0.02], [0.02, 0.98]])
    for q in range(2):
        noise.add_readout_error(ro, [q])
    noise.add_all_qubit_quantum_error(depolarizing_error(1e-3, 1), ["h", "s", "sdg", "x"])
    noise.add_all_qubit_quantum_error(depolarizing_error(1e-2, 2), ["cx"])
    noisy = AerSimulator(noise_model=noise)
    circs = [positive_control(0), negative_control(0)]
    recs_n = []
    tqc = transpile(circs, noisy)
    result = noisy.run(tqc, shots=SHOTS).result()
    for i, qc in enumerate(circs):
        recs_n.append({"kind": qc.metadata["kind"], "bases": "ZZZ",
                       "delay_ns": 0, "counts": result.get_counts(i)})
    p_pos = counts_to_dist(recs_n[0]["counts"])
    p_neg = counts_to_dist(recs_n[1]["counts"])
    s_pos, s_neg = share(p_pos), share(p_neg)
    fl = bootstrap_floor(p_pos, SHOTS, RNG)
    neg_fl = bootstrap_floor(p_neg, SHOTS, RNG)
    sens = s_pos > max(float(np.quantile(fl, 0.99)), s_neg + 3 * float(neg_fl.std()))
    print(f"noisy d=0: positive {s_pos:.4f}, negative {s_neg:.4f}, "
          f"pos floor99 {float(np.quantile(fl, 0.99)):.4f} -> sensitivity ok={sens}")
    ok = ok and sens
    print("GATE", "PASS" if ok else "FAIL")
    return 0 if ok else 1

def run_hardware():
    """Submit the ONE pre-registered job. Requires saved IBM credentials."""
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
    from qiskit import transpile
    service = QiskitRuntimeService()
    backend = service.least_busy(operational=True, simulator=False)
    print("backend:", backend.name)
    circs = all_circuits()
    tqc = transpile(circs, backend, optimization_level=1)
    sampler = SamplerV2(mode=backend)
    job = sampler.run(tqc, shots=SHOTS)
    print("job id:", job.job_id())
    result = job.result()
    recs = []
    for i, qc in enumerate(circs):
        md = qc.metadata
        counts = result[i].data.c.get_counts() if hasattr(result[i].data, "c") \
            else result[i].join_data().get_counts()
        recs.append({"kind": md["kind"], "bases": md.get("bases", "ZZZ"),
                     "delay_ns": md["delay_ns"], "counts": counts})
    fname = f"hw_counts_{backend.name}_{job.job_id()}.json"
    with open(fname, "w") as f:
        json.dump({"backend": backend.name, "job_id": job.job_id(),
                   "records": recs}, f)
    print("saved", fname)
    res = analyze(recs)
    print(json.dumps(res["verdict"], indent=2))
    return 0

def run_analyze(path):
    with open(path) as f:
        data = json.load(f)
    res = analyze(data["records"])
    print(json.dumps(res["verdict"], indent=2))
    out = path.replace("hw_counts", "hw_verdict")
    with open(out, "w") as f:
        json.dump(res, f, indent=2, default=float)
    print("saved", out)
    return 0

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "gate"
    if mode == "gate":
        sys.exit(run_gate())
    elif mode == "hardware":
        sys.exit(run_hardware())
    elif mode == "analyze":
        sys.exit(run_analyze(sys.argv[2]))
