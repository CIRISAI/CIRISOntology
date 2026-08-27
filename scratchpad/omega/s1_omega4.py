#!/usr/bin/env python3
"""OMEGA-KILL-4 QPU harness: pinned backbone + g-face DOSE EXTENSION, one job.
Thin wrapper over s1_omega3 with the dose axis moved to never-measured points
p in {3, 6, 12, 24} (Omega-3 measured {2, 4, 8, 16}). Same estimators, same
bracket verdict (min/max of the two point predictions +/- 3 sigma), same
in-job premises. Usage: submit | fetch <jid> | analyse <results.json>"""
import sys, json, importlib.util
_s = importlib.util.spec_from_file_location("o3", "s1_omega3.py")
o3 = importlib.util.module_from_spec(_s); _s.loader.exec_module(o3)
o3.PS = [3, 6, 12, 24]                      # the dose extension, frozen

def submit():
    s1 = o3.load_s1()
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit import qpy
    scr = json.load(open("../temporal-share/closure_pilot_screen.json"))
    svc = QiskitRuntimeService(channel="ibm_quantum_platform", token=s1.TOKEN,
                               instance="open-instance")
    bk = svc.backend(scr["backend"])
    with open("omega_arms_pinned.qpy", "rb") as f: backbone = qpy.load(f)
    try:
        with open("omega4_g_pinned.qpy", "rb") as f: gset = qpy.load(f)
        print(f"g-ext: loaded {len(gset)} pinned")
    except FileNotFoundError:
        pm = generate_preset_pass_manager(optimization_level=1, backend=bk,
                                          initial_layout=scr["selected"],
                                          scheduling_method="alap")
        gset = [pm.run(c) for c in o3.n2_circuits()]
        with open("omega4_g_pinned.qpy", "wb") as f: qpy.dump(gset, f)
        print(f"g-ext: transpiled and pinned {len(gset)}")
    circs = list(backbone) + list(gset)
    job = SamplerV2(mode=bk).run(circs, shots=o3.SHOTS)
    meta = [dict(c.metadata or {}) for c in circs]
    json.dump({"job": job.job_id(), "backend": bk.name, "pair": scr["selected"],
               "n_backbone": len(backbone), "meta": meta},
              open("omega4_job.json", "w"), indent=2)
    print("job:", job.job_id())

def fetch(jid):
    s1 = o3.load_s1()
    from qiskit_ibm_runtime import QiskitRuntimeService
    svc = QiskitRuntimeService(channel="ibm_quantum_platform", token=s1.TOKEN,
                               instance="open-instance")
    job = svc.job(jid); print("status:", job.status())
    res = job.result()
    jd = json.load(open("omega4_job.json"))
    jd["counts"] = [r.data.c.get_counts() for r in res]
    out = f"omega4_results_{jid}.json"
    json.dump(jd, open(out, "w"), indent=2)
    print("saved", out); o3.analyse(out)

if __name__ == "__main__":
    if sys.argv[1] == "submit": submit()
    elif sys.argv[1] == "fetch": fetch(sys.argv[2])
    else: o3.analyse(sys.argv[2])
