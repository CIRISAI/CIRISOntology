#!/usr/bin/env python3
"""OMEGA_KILL3 QPU harness: pinned backbone (S1 A1-A4) + N2 rent bracket, ONE job.

Backbone: the 20 pinned circuits (omega_arms_pinned.qpy, D-CHAN-DRIFT repair).
N2: single-qubit rent instrument on BOTH screened qubits (staked qubit named in
the prereg from the screen record; the other is an unscored replicate):
  - decay ladder  k in {0,1,2,4,8,16,32} slots of tau_slot
  - thermal floor Pinf: prep |0>, 32 slots
  - deposit s0_eff: X, 1 slot, reset, X, measure
  - dose arms (p,C): X, then (C-1)x[p slots, reset, X], then p slots, measure
    p in {2,4,8,16}, C in {2,4}
tau_slot = 8 us. Frozen estimators (no curve fits): see gauge_n2.py.
Verdicts: N2a bracket uses [min-3s, max+3s] of the two point predictions
(gauge caught single-mode ordering inversion under shot noise). All floors
and premises in-job. Usage: submit | analyse <results.json>
"""
import json, sys, importlib.util
import numpy as np
from qiskit import QuantumCircuit, qpy
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

import os

def load_s1():
    here = os.getcwd()
    ts = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "temporal-share")
    os.chdir(ts)
    try:
        _s = importlib.util.spec_from_file_location("s1", "s1_omega.py")
        s1 = importlib.util.module_from_spec(_s); _s.loader.exec_module(s1)
    finally:
        os.chdir(here)
    return s1

TAU_US, KS, PS, CS, SHOTS = 8.0, [0,1,2,4,8,16,32], [2,4,8,16], [2,4], 4096

def n2_circuits():
    out = []
    def base(): 
        qc = QuantumCircuit(2, 2); return qc
    def slot(qc):
        qc.barrier(); qc.delay(TAU_US, (0,1), unit='us'); qc.barrier()
    for k in KS:
        qc = base(); qc.x((0,1))
        for _ in range(k): slot(qc)
        qc.measure((0,1),(0,1)); qc.metadata = {"n2":"ladder","k":k}; out.append(qc)
    qc = base()
    for _ in range(32): slot(qc)
    qc.measure((0,1),(0,1)); qc.metadata = {"n2":"pinf"}; out.append(qc)
    qc = base(); qc.x((0,1)); slot(qc); qc.reset((0,1)); qc.x((0,1))
    qc.measure((0,1),(0,1)); qc.metadata = {"n2":"s0eff"}; out.append(qc)
    for p in PS:
        for C in CS:
            qc = base(); qc.x((0,1))
            for c in range(C):
                for _ in range(p): slot(qc)
                if c < C-1: qc.reset((0,1)); qc.x((0,1))
            qc.measure((0,1),(0,1)); qc.metadata = {"n2":"dose","p":p,"C":C}; out.append(qc)
    return out

def submit():
    s1 = load_s1()
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
    scr = json.load(open("../temporal-share/closure_pilot_screen.json"))
    svc = QiskitRuntimeService(channel="ibm_quantum_platform", token=s1.TOKEN,
                               instance="open-instance")
    bk = svc.backend(scr["backend"])
    with open("omega_arms_pinned.qpy","rb") as f: backbone = qpy.load(f)
    try:
        with open("omega3_n2_pinned.qpy","rb") as f: n2t = qpy.load(f)
        print(f"n2: loaded {len(n2t)} pinned")
    except FileNotFoundError:
        pm = generate_preset_pass_manager(optimization_level=1, backend=bk,
                                          initial_layout=scr["selected"],
                                          scheduling_method="alap")
        n2t = [pm.run(c) for c in n2_circuits()]
        with open("omega3_n2_pinned.qpy","wb") as f: qpy.dump(n2t, f)
        print(f"n2: transpiled and pinned {len(n2t)}")
    circs = list(backbone) + list(n2t)
    job = SamplerV2(mode=bk).run(circs, shots=SHOTS)
    meta = [dict(c.metadata or {}) for c in circs]
    json.dump({"job": job.job_id(), "backend": bk.name, "pair": scr["selected"],
               "n_backbone": len(backbone), "meta": meta},
              open("omega3_job.json","w"), indent=2)
    print("job:", job.job_id())

def analyse(path):
    s1 = load_s1()
    d = json.load(open(path)); res_counts = d["counts"]; meta = d["meta"]; nb = d["n_backbone"]
    # ---- backbone: rebuild s1's counts structure {arm: {"ab": {bits: n}}}
    bb = {}
    for c, m in zip(res_counts[:nb], meta[:nb]):
        bb.setdefault(m["arm"], {})[f'{m["a"]}{m["b"]}'] = c
    res = s1.analyse_counts(bb)
    v = s1.verdict(res)
    ow = res["oneway"]
    premise_ok = ow["d_ba"] <= 10*max(ow["f_ba"],1e-12)
    if not premise_ok:
        v["A2_oneway"] = None
        print(f"A2 PREMISE FAILED (reverse {ow['d_ba']/max(ow['f_ba'],1e-12):.1f}x floor > 10x): VOID-PREMISE")
    # ---- N2 per qubit: bit index 0/1 of the 2-bit strings (staked qubit per prereg)
    P = {}
    for c, m in zip(res_counts[nb:], meta[nb:]):
        tot = sum(c.values())
        for q in (0,1):
            p1 = sum(n for bits,n in c.items() if bits[::-1][q]=='1')/tot
            P[(q, tuple(sorted(m.items())))] = p1
    sig = np.sqrt(0.25/SHOTS)
    def g(q, **kw): return P[(q, tuple(sorted([("n2",kw.pop("n2"))]+list(kw.items()))))]
    out = {}
    for q in (0,1):
        lad = {k: g(q, n2="ladder", k=k) for k in KS}
        pinf = g(q, n2="pinf"); s0e = g(q, n2="s0eff")
        mono = all(lad[KS[i]] >= lad[KS[i+1]] - 3*sig*np.sqrt(2) for i in range(len(KS)-1))
        lam_f = (lad[1]-pinf)/(lad[0]-pinf)
        lam_s = ((lad[32]-pinf)/(lad[16]-pinf))**(1/16)
        brk, mem, rows = True, True, []
        for p in PS:
            r2, r4 = g(q, n2="dose", p=p, C=2), g(q, n2="dose", p=p, C=4)
            pf = pinf+(s0e-pinf)*lam_f**p; ps_ = pinf+(s0e-pinf)*lam_s**p
            lo, hi = min(pf,ps_)-3*sig, max(pf,ps_)+3*sig
            okb = lo <= r2 <= hi; okm = abs(r4-r2) <= 3*sig*np.sqrt(2)
            brk &= okb; mem &= okm
            rows.append((p, r2, r4, lo, hi, okb, okm))
        out[q] = {"lam_fast": lam_f, "lam_slow": lam_s, "pinf": pinf, "s0eff": s0e,
                  "monotone_premise": mono, "bracket": brk, "memory": mem, "rows": rows}
        print(f"\nqubit[{q}]: lam_f={lam_f:.4f} lam_s={lam_s:.4f} Pinf={pinf:.4f} s0eff={s0e:.4f} "
              f"monotone_premise={'OK' if mono else 'FAILED->VOID-PREMISE'}")
        for p, r2, r4, lo, hi, okb, okm in rows:
            print(f"  p={p:2d}: R2={r2:.4f} in [{lo:.4f},{hi:.4f}] {'ok' if okb else 'OUT'}"
                  f"  |R4-R2|={abs(r4-r2):.4f} {'ok' if okm else 'MEMORY'}")
        print(f"  N2a bracket: {'PASS' if brk else 'MISS'}   N2b memory: {'PASS' if mem else 'MISS'}"
              + ("" if mono else "   [BOTH VOID-PREMISE: ladder non-monotone]"))
    print("\nbackbone verdicts:", v)
    json.dump({"backbone": {k:(None if x is None else bool(x)) for k,x in v.items()},
               "premise_oneway_ok": bool(premise_ok),
               "n2": {str(q): {kk: (vv if kk=="rows" else (bool(vv) if isinstance(vv,(bool,np.bool_)) else float(vv)))
                              for kk,vv in out[q].items()} for q in out}},
              open("omega3_verdicts.json","w"), indent=2, default=float)

def fetch(jid):
    s1 = load_s1()
    from qiskit_ibm_runtime import QiskitRuntimeService
    svc = QiskitRuntimeService(channel="ibm_quantum_platform", token=s1.TOKEN,
                               instance="open-instance")
    job = svc.job(jid); print("status:", job.status())
    res = job.result()
    jd = json.load(open("omega3_job.json"))
    counts = [r.data.c.get_counts() for r in res]
    jd["counts"] = counts
    out = f"omega3_results_{jid}.json"
    json.dump(jd, open(out,"w"), indent=2)
    print("saved", out); analyse(out)

if __name__ == "__main__":
    if sys.argv[1] == "submit": submit()
    elif sys.argv[1] == "fetch": fetch(sys.argv[2])
    else: analyse(sys.argv[2])
