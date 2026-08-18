"""CROSSPAIR — screen, then one batched job. Per CROSSPAIR_PREREG.md + AMENDMENT_1.

Two jobs total. Fail-closed: if anything is off after the screen, stop before
the main job rather than spend the quota on a doubtful submission.
"""
import json, sys, time
from collections import deque
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

SHOTS_MAIN, SHOTS_SCREEN = 3072, 2048
SEP_TARGETS = [2, 4, 8, 16]

svc = QiskitRuntimeService()
bk = svc.least_busy(operational=True, simulator=False, min_num_qubits=100)
print("backend:", bk.name, bk.num_qubits, flush=True)

edges = [tuple(e) for e in bk.coupling_map]
adj = {}
for a, b in edges:
    adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)

def dist_from(srcs):
    d = {s: 0 for s in srcs}; q = deque(srcs)
    while q:
        u = q.popleft()
        for v in adj.get(u, ()):
            if v not in d: d[v] = d[u] + 1; q.append(v)
    return d

# ---- screen job: |0..0> and X-on-all, measure everything ----
n = bk.num_qubits
c0 = QuantumCircuit(n); c0.measure_all()
c1 = QuantumCircuit(n); c1.x(range(n)); c1.measure_all()
pm = generate_preset_pass_manager(backend=bk, optimization_level=0)
sampler = SamplerV2(mode=bk)
t0 = time.time()
job_s = sampler.run(pm.run([c0, c1]), shots=SHOTS_SCREEN)
print("screen job:", job_s.job_id(), flush=True)
rs = job_s.result()
print("screen done in %.0f s wall" % (time.time() - t0), flush=True)

def perbit_p1(res):
    bits = res.data.meas.get_bitstrings()
    N = len(bits); L = len(bits[0])
    cnt = [0]*L
    for s in bits:
        for i, ch in enumerate(reversed(s)):
            if ch == '1': cnt[i] += 1
    return [c/N for c in cnt]

p1_given0 = perbit_p1(rs[0]); p1_given1 = perbit_p1(rs[1])
err = [p1_given0[i] + (1.0 - p1_given1[i]) for i in range(n)]

# ---- choose pair A = best edge, then pair-B edges near separation targets ----
def edge_score(e): return err[e[0]] + err[e[1]]
edges_sorted = sorted(edges, key=edge_score)
A = edges_sorted[0]
dA = dist_from(list(A))
chosen, used = [], set(A)
for tgt in SEP_TARGETS:
    best = None
    for e in edges_sorted:
        if e[0] in used or e[1] in used: continue
        d = min(dA.get(e[0], 999), dA.get(e[1], 999))
        if d < 2: continue
        pen = abs(d - tgt) * 0.05 + edge_score(e)
        if best is None or pen < best[0]: best = (pen, e, d)
    if best:
        chosen.append((best[1], best[2])); used |= set(best[1])
print("pair A:", A, "err %.4f/%.4f" % (err[A[0]], err[A[1]]), flush=True)
for (e, d) in chosen:
    print("  pair B:", e, "sep", d, "err %.4f/%.4f" % (err[e[0]], err[e[1]]), flush=True)
if len(chosen) < 4:
    print("REFUSED: fewer than 4 separations found"); sys.exit(2)
if edge_score(A) > 0.10:
    print("REFUSED: best edge readout error too high"); sys.exit(2)

# ---- build the 24 main circuits on physical qubits ----
def cell(prep, basis, B):
    qc = QuantumCircuit(n, 4)
    a1, a2 = A; b1, b2 = B
    if prep == "bell":
        qc.h(a1); qc.cx(a1, a2); qc.h(b1); qc.cx(b1, b2)
    elif prep == "ctrlp":
        for q in (a1, a2, b1, b2): qc.h(q)
    if basis == "XX":
        for q in (a1, a2, b1, b2): qc.h(q)
    for i, q in enumerate((a1, a2, b1, b2)): qc.measure(q, i)
    return qc

cells, meta = [], []
for (B, d) in chosen:
    for basis in ("ZZ", "XX"):
        for prep in ("bell", "ctrl0", "ctrlp"):
            cells.append(cell(prep, basis, B))
            meta.append({"B": list(B), "sep": d, "basis": basis, "prep": prep})
pm0 = generate_preset_pass_manager(backend=bk, optimization_level=0)
isa = pm0.run(cells)
tot = len(cells) * SHOTS_MAIN
print(f"main job: {len(cells)} circuits x {SHOTS_MAIN} = {tot} shots", flush=True)

job_m = sampler.run(isa, shots=SHOTS_MAIN)
print("main job:", job_m.job_id(), flush=True)
rm = job_m.result()
print("main done", flush=True)

# ---- correlators ----
rows = []
for res, m in zip(rm, meta):
    bits = res.data.c.get_bitstrings()
    N = len(bits); s_pa = s_pb = s_ab = 0
    for s in bits:
        b = s[::-1]  # c0..c3 = a1,a2,b1,b2
        pa = 1 - 2 * ((int(b[0]) + int(b[1])) % 2)
        pb = 1 - 2 * ((int(b[2]) + int(b[3])) % 2)
        s_pa += pa; s_pb += pb; s_ab += pa * pb
    E = s_ab / N
    m2 = dict(m); m2.update({"N": N, "pA": s_pa / N, "pB": s_pb / N, "E_cross": E,
                             "sd": (max(1e-12, 1 - E * E) / N) ** 0.5})
    rows.append(m2)
    print("%(basis)s %(prep)6s sep=%(sep)2d  pA=%(pA)+.3f pB=%(pB)+.3f  E=%(E_cross)+.4f" % m2, flush=True)

met = {}
try:
    met = {"usage_s": job_m.metrics().get("usage", {}), "screen_usage_s": job_s.metrics().get("usage", {})}
except Exception as e:
    met = {"metrics_error": str(e)[:120]}
out = {"backend": bk.name, "pairA": list(A), "chosen": [[list(e), d] for e, d in chosen],
       "shots": SHOTS_MAIN, "rows": rows, "metrics": met,
       "screen_err_A": [err[A[0]], err[A[1]]]}
json.dump(out, open("desi_bgs/../crosspair_results.json", "w"), indent=1)
print("WRITTEN crosspair_results.json", flush=True)
