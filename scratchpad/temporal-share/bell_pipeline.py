#!/usr/bin/env python3
"""The Logos Bell test — pipeline per BELL_PREREG.md (commit a318d66).

Threshold is the machine-checked classical cap (Core/ShareK.lean, 5c18af7):
no classical 5-slot state has any pair view with more entropy than its whole.
Statistic V = min over 10 pairs of S_vN(pair) - S_vN(whole); claim needs the
conservative rule of the prereg.

Usage:
  qenv/bin/python bell_pipeline.py gate            # Aer gate, no hardware
  qenv/bin/python bell_pipeline.py hardware        # the ONE pre-registered job
  qenv/bin/python bell_pipeline.py analyze F.json  # re-analyze saved counts
"""
import json
import sys
import math
import itertools
import numpy as np

LN2 = math.log(2.0)
N = 5
DIM = 2 ** N
SHOTS = 1024
BOOT_B = 200
RNG = np.random.default_rng(20260725)
SETTINGS = list(itertools.product("XYZ", repeat=N))
C5_EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]

PAULI = {
    "I": np.eye(2, dtype=complex),
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "Z": np.array([[1, 0], [0, -1]], dtype=complex),
}

# ---------------------------------------------------------------- states

def ideal_c5_state():
    """C5 graph state vector: psi[x] = 2^{-5/2} (-1)^{#edges with both bits 1}."""
    psi = np.ones(DIM) / math.sqrt(DIM)
    for idx in range(DIM):
        bits = [(idx >> q) & 1 for q in range(N)]
        sign = sum(bits[i] * bits[j] for i, j in C5_EDGES) % 2
        if sign:
            psi[idx] = -psi[idx]
    return psi

# ---------------------------------------------------------------- circuits

def build_circuit(state, setting):
    """Prep + basis rotations + tomography measurement into creg 'c'.

    The 'code' control prepares the CLASSICAL MIXTURE over the [5,3]
    codewords: the three source qubits are collapsed by mid-circuit
    measurement (into scratch creg 'm', ignored downstream) BEFORE encoding.
    The gate caught the pure-superposition version violating monotonicity —
    correctly, since a pure code state is a quantum object, not a classical
    control (see BELL_PREREG.md addendum 1)."""
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
    q = QuantumRegister(N, "q")
    c = ClassicalRegister(N, "c")
    if state == "c5":
        qc = QuantumCircuit(q, c)
        qc.h(q)
        for i, j in C5_EDGES:
            qc.cz(q[i], q[j])
    else:
        m = ClassicalRegister(3, "m")
        qc = QuantumCircuit(q, c, m)
        qc.h([q[0], q[2], q[4]])
        qc.measure(q[0], m[0])
        qc.measure(q[2], m[1])
        qc.measure(q[4], m[2])
        qc.cx(q[0], q[1])
        qc.cx(q[2], q[1])
        qc.cx(q[2], q[3])
        qc.cx(q[4], q[3])
    for k, b in enumerate(setting):
        if b == "X":
            qc.h(q[k])
        elif b == "Y":
            qc.sdg(q[k])
            qc.h(q[k])
    for k in range(N):
        qc.measure(q[k], c[k])
    return qc

def calibration_circuits():
    from qiskit import QuantumCircuit
    c0 = QuantumCircuit(N, N)
    c0.measure(range(N), range(N))
    c1 = QuantumCircuit(N, N)
    c1.x(range(N))
    c1.measure(range(N), range(N))
    return [c0, c1]

def all_circuits():
    circs, meta = [], []
    for name in ("c5", "code"):
        for s in SETTINGS:
            circs.append(build_circuit(name, s))
            meta.append({"state": name, "setting": "".join(s)})
    for i, qc in enumerate(calibration_circuits()):
        circs.append(qc)
        meta.append({"state": "cal", "setting": str(i)})
    return circs, meta

# ---------------------------------------------------------------- tomography

def counts_to_vec(counts):
    """32-vector of outcome frequencies; bit q of the index is qubit q's
    outcome (Qiskit keys little-endian: rightmost char = qubit 0 = bit 0)."""
    v = np.zeros(DIM)
    tot = 0
    for key, n in counts.items():
        bits = key.replace(" ", "")
        idx = 0
        for q in range(N):
            if bits[-1 - q] == "1":
                idx |= 1 << q
        v[idx] += n
        tot += n
    return v / tot

def assignment_matrices(cal0, cal1):
    """Per-qubit 2x2 readout assignment matrices A[q][meas, true]."""
    mats = []
    for q in range(N):
        p1_given0 = sum(v for i, v in enumerate(cal0) if (i >> q) & 1)
        p1_given1 = sum(v for i, v in enumerate(cal1) if (i >> q) & 1)
        A = np.array([[1 - p1_given0, 1 - p1_given1], [p1_given0, p1_given1]])
        mats.append(A)
    return mats

def correct_readout(vec, amats):
    """Apply per-qubit inverse assignment matrices to the 32-distribution."""
    t = vec.reshape([2] * N)  # axes: qubit 0 ... qubit 4 (axis q = bit q)
    for q in range(N):
        Ainv = np.linalg.inv(amats[q])
        t = np.tensordot(Ainv, t, axes=([1], [q]))
        t = np.moveaxis(t, 0, q)
    return t.reshape(DIM)

_IDX = np.arange(DIM)
_SIGN_CACHE = {}
_COMPAT_CACHE = {}

def _sign_vec(pauli):
    if pauli not in _SIGN_CACHE:
        par = np.zeros(DIM)
        for q, p in enumerate(pauli):
            if p != "I":
                par += (_IDX >> q) & 1
        _SIGN_CACHE[pauli] = (-1.0) ** par
    return _SIGN_CACHE[pauli]

def _compatible(pauli):
    if pauli not in _COMPAT_CACHE:
        _COMPAT_CACHE[pauli] = ["".join(s) for s in SETTINGS
            if all(p == "I" or p == s[q] for q, p in enumerate(pauli))]
    return _COMPAT_CACHE[pauli]

def pauli_expectations(dists):
    """dists: dict setting-string -> corrected 32-vector. Returns dict
    pauli-string -> expectation, averaged over all compatible settings."""
    exps = {}
    for pauli in itertools.product("IXYZ", repeat=N):
        ps = "".join(pauli)
        sv = _sign_vec(ps)
        vals = [float(dists[s] @ sv) for s in _compatible(ps)]
        exps[ps] = float(np.mean(vals))
    return exps

def rho_from_expectations(exps):
    rho = np.zeros((DIM, DIM), dtype=complex)
    for ps, val in exps.items():
        op = PAULI[ps[0]]
        for ch in ps[1:]:
            op = np.kron(PAULI[ch], op)  # qubit 0 = least significant factor
        rho += val * op
    rho /= DIM
    return rho

def project_psd(rho):
    """Smolin-Gambetta-Smith: clip negative eigenvalues, redistribute."""
    w, v = np.linalg.eigh((rho + rho.conj().T) / 2)
    w = w[::-1].copy()
    v = v[:, ::-1]
    acc = 0.0
    for i in range(len(w) - 1, -1, -1):
        if w[i] + acc / (i + 1) < 0:
            acc += w[i]
            w[i] = 0.0
        else:
            w[:i + 1] += acc / (i + 1)
            break
    w = np.clip(w, 0, None)
    w = w / w.sum()
    return (v * w) @ v.conj().T, w

def svn(w):
    w = np.clip(np.real(w), 0, None)
    w = w / w.sum()
    nz = w > 1e-15
    return float(-(w[nz] * np.log(w[nz])).sum())

def pair_ptrace(rho, i, j):
    t = rho.reshape([2] * (2 * N))  # row axes 0..4 (qubit q = axis q), col axes 5..9
    keep_r = [i, j]
    keep_c = [i + N, j + N]
    out = np.zeros((4, 4), dtype=complex)
    tr_axes = [q for q in range(N) if q not in keep_r]
    cur = t
    for q in sorted(tr_axes, reverse=True):
        cur = np.trace(cur, axis1=q, axis2=q + (cur.ndim // 2))
    # cur now has axes (i, j | i, j)
    return cur.reshape(4, 4)

def violation(rho):
    w = np.linalg.eigvalsh(rho)
    s_whole = svn(w)
    s_pairs = []
    for i in range(N):
        for j in range(i + 1, N):
            pw = np.linalg.eigvalsh(pair_ptrace(rho, i, j))
            s_pairs.append(svn(pw))
    return min(s_pairs) - s_whole, s_whole, s_pairs

def analyze_state(dists, amats):
    corrected = {s: correct_readout(v, amats) for s, v in dists.items()}
    exps = pauli_expectations(corrected)
    rho_lin = rho_from_expectations(exps)
    rho, w = project_psd(rho_lin)
    V, s_whole, s_pairs = violation(rho)
    return {"V": V, "S_whole": s_whole, "S_pairs": s_pairs, "rho": rho}

def full_analysis(records):
    """records: list of {state, setting, counts}. Returns verdict per prereg."""
    raw = {"c5": {}, "code": {}}
    cal = {}
    for rec in records:
        vec = counts_to_vec(rec["counts"])
        if rec["state"] == "cal":
            cal[rec["setting"]] = vec
        else:
            raw[rec["state"]][rec["setting"]] = vec
    amats = assignment_matrices(cal["0"], cal["1"])
    ro_fid = min(min(amats[q][0, 0], amats[q][1, 1]) for q in range(N))

    res = {st: analyze_state(raw[st], amats) for st in ("c5", "code")}
    psi = ideal_c5_state()
    fid = float(np.real(psi.conj() @ res["c5"]["rho"] @ psi))

    boots = {"c5": [], "code": []}
    for b in range(BOOT_B):
        for st in ("c5", "code"):
            rd = {}
            for s, vec in raw[st].items():
                cnt = RNG.multinomial(SHOTS, np.clip(vec, 0, None) / np.clip(vec, 0, None).sum())
                rd[s] = cnt / SHOTS
            boots[st].append(analyze_state(rd, amats)["V"])
    vb_c5 = np.array(boots["c5"])
    vb_code = np.array(boots["code"])

    V = res["c5"]["V"]
    V_bc = 2 * V - float(vb_c5.mean())
    verdict = {
        "readout_fid_min": float(ro_fid),
        "readout_ok": bool(ro_fid >= 0.95),
        "V_c5": V, "V_c5_boot_p01": float(np.quantile(vb_c5, 0.01)),
        "V_c5_bias_corrected": V_bc,
        "S_whole_c5": res["c5"]["S_whole"],
        "S_pairs_c5_min": float(min(res["c5"]["S_pairs"])),
        "fidelity_c5": fid,
        "V_code": res["code"]["V"],
        "V_code_boot_p99": float(np.quantile(vb_code, 0.99)),
        "control_ok": bool(np.quantile(vb_code, 0.99) <= 0.0),
        "ideal_V": 2 * LN2,
        "classical_cap_statement": "V > 0 impossible classically (ShareK.lean, 5c18af7)",
    }
    verdict["claim"] = bool(
        verdict["readout_ok"] and verdict["control_ok"]
        and verdict["V_c5_boot_p01"] > 0 and V_bc >= 0.05)
    return verdict

# ---------------------------------------------------------------- runners

def execute_local(circs, meta, backend):
    from qiskit import transpile
    tqc = transpile(circs, backend)
    result = backend.run(tqc, shots=SHOTS).result()
    return [{"state": m["state"], "setting": m["setting"],
             "counts": result.get_counts(i)} for i, m in enumerate(meta)]

def run_gate():
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel, ReadoutError, depolarizing_error
    circs, meta = all_circuits()

    print("== ideal ==")
    v = full_analysis(execute_local(circs, meta, AerSimulator()))
    print(json.dumps(v, indent=2))
    # Reconstruction inflates S_whole of a near-pure state by ~0.1-0.15 nat at
    # 1024 shots (bias AGAINST the claim, the conservative direction); the
    # ideal window acknowledges it. Control must be negative per the prereg.
    ok = (1.15 < v["V_c5"] < 1.45 and v["V_code"] < 0
          and v["control_ok"] and v["readout_ok"] and v["claim"])
    print("ideal ok:", ok)

    noise = NoiseModel()
    ro = ReadoutError([[0.98, 0.02], [0.02, 0.98]])
    for q in range(N):
        noise.add_readout_error(ro, [q])
    noise.add_all_qubit_quantum_error(depolarizing_error(1e-3, 1),
                                      ["h", "s", "sdg", "x"])
    noise.add_all_qubit_quantum_error(depolarizing_error(1e-2, 2), ["cz", "cx"])
    print("== noisy ==")
    vn = full_analysis(execute_local(circs, meta, AerSimulator(noise_model=noise)))
    print(json.dumps(vn, indent=2))
    ok2 = vn["claim"]
    print("noisy claim-rule pass:", ok2)
    print("GATE", "PASS" if (ok and ok2) else "FAIL")
    return 0 if (ok and ok2) else 1

def run_hardware():
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
    from qiskit import transpile
    service = QiskitRuntimeService()
    backend = service.least_busy(operational=True, simulator=False)
    print("backend:", backend.name)
    circs, meta = all_circuits()
    tqc = transpile(circs, backend, optimization_level=3, seed_transpiler=20260725)
    sampler = SamplerV2(mode=backend)
    job = sampler.run(tqc, shots=SHOTS)
    print("job id:", job.job_id())
    result = job.result()
    recs = []
    for i, m in enumerate(meta):
        counts = result[i].data.c.get_counts()
        recs.append({"state": m["state"], "setting": m["setting"],
                     "counts": counts})
    fname = f"bell_counts_{backend.name}_{job.job_id()}.json"
    with open(fname, "w") as f:
        json.dump({"backend": backend.name, "job_id": job.job_id(),
                   "records": recs}, f)
    print("saved", fname)
    print(json.dumps(full_analysis(recs), indent=2))
    return 0

def run_analyze(path):
    with open(path) as f:
        data = json.load(f)
    v = full_analysis(data["records"])
    print(json.dumps(v, indent=2))
    out = path.replace("bell_counts", "bell_verdict")
    with open(out, "w") as f:
        json.dump(v, f, indent=2)
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
