#!/usr/bin/env python3
"""BANKED REPAIR (D-CHAN-DRIFT, compilation component): pin transpiled circuits.

Transpile ONCE, serialize to QPY, and every subsequent job runs the identical
compiled artifact — the realized channel becomes a fixed object across epochs,
removing per-job re-transpilation as a drift source. Hardware ageing remains
(the premise check covers it); what this kills is the compiler's contribution.

Usage:
  pin_circuits.py pin <out.qpy>     # transpile the omega arm set once, save
  pin_circuits.py load <in.qpy>     # load for submission (returns circuits)
Evidence for the mechanism: the CRX pair's reverse influence jumped 6x within
hours between two jobs (19.7x -> 137x floor) -- compilation-rate, not
ageing-rate.
"""
import sys, json, importlib.util
from qiskit import qpy

def pin(out_path):
    _s = importlib.util.spec_from_file_location("s1", "../temporal-share/s1_omega.py")
    s1 = importlib.util.module_from_spec(_s); _s.loader.exec_module(s1)
    from qiskit_ibm_runtime import QiskitRuntimeService
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    scr = json.load(open("../temporal-share/closure_pilot_screen.json"))
    svc = QiskitRuntimeService(channel="ibm_quantum_platform", token=s1.TOKEN,
                               instance="open-instance")
    bk = svc.backend(scr["backend"])
    pm = generate_preset_pass_manager(optimization_level=1, backend=bk,
                                      initial_layout=scr["selected"])
    circs = [pm.run(c) for c in s1.circuits()]
    with open(out_path, "wb") as f: qpy.dump(circs, f)
    print(f"pinned {len(circs)} compiled circuits -> {out_path}")

def load(in_path):
    with open(in_path, "rb") as f: return qpy.load(f)

if __name__ == "__main__":
    if sys.argv[1] == "pin": pin(sys.argv[2])
    else: print(f"{len(load(sys.argv[2]))} circuits loadable")
