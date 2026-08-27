#!/usr/bin/env python3
"""Planted end-to-end validation of s1_omega3.analyse: synthesize a results file
with known truth (ideal backbone unitaries + single-mode N2 decay), run the real
analyse, and check the verdicts. PASS side = planted truth; FIRE side = planted
out-of-bracket dose + planted cycle-memory. This gauges the ANALYSIS PATH."""
import json, itertools, importlib.util
import numpy as np
_o = importlib.util.spec_from_file_location("o3", "s1_omega3.py")
o3 = importlib.util.module_from_spec(_o); _o.loader.exec_module(o3)
s1 = o3.load_s1()
from qiskit import QuantumCircuit
from qiskit.circuit.library import XXPlusYYGate
from qiskit.quantum_info import Operator
rng = np.random.default_rng(7); SHOTS = 4096; labels = ['00','01','10','11']

def sample(p):
    c = {}
    for k in rng.choice(4, SHOTS, p=np.asarray(p)/sum(p)): c[labels[k]] = c.get(labels[k],0)+1
    return c

meta, counts = [], []
for arm in s1.ARMS:                       # backbone in s1.circuits() order
    for a,b in itertools.product((0,1), repeat=2):
        qc = QuantumCircuit(2)
        if a: qc.x(0)
        if b: qc.x(1)
        if arm=="oneway": qc.crx(s1.THETA,0,1)
        elif arm=="hop": qc.append(XXPlusYYGate(s1.THETA),[0,1])
        elif arm=="cd_on": qc.x(0); qc.x(1)
        U = Operator(qc).data; p = np.abs(U[:,0])**2
        meta.append({"arm":arm,"a":a,"b":b}); counts.append(sample(p))

LAM, S0, PINF = 0.92, 0.97, 0.015
def p1(k_slots, s=S0): return PINF + (s-PINF)*LAM**k_slots
def two_bit(pa, pb): return sample([ (1-pa)*(1-pb), (1-pa)*pb, pa*(1-pb), pa*pb ][::1])
# NOTE label order: labels are 'b a'? qiskit keys are c1 c0 -> bits[::-1][q]=cbit q.
# probabilities indexed 00,01,10,11 as (c1 c0): p(c1,c0) = p_q1(c1)*p_q0(c0)
def two_bit(pq0, pq1):
    return sample([ (1-pq1)*(1-pq0), (1-pq1)*pq0, pq1*(1-pq0), pq1*pq0 ])

def add(m, pq0, pq1): meta.append(m); counts.append(two_bit(pq0, pq1))

FIRE = False
def n2_block(fire):
    for k in o3.KS: add({"n2":"ladder","k":k}, p1(k), p1(k))
    add({"n2":"pinf"}, PINF, PINF)
    add({"n2":"s0eff"}, S0, S0)
    for p in o3.PS:
        for C in o3.CS:
            if not fire: r = p1(p)
            else:        r = PINF + (S0-PINF)*0.70**p if C==2 else PINF + (S0-PINF)*0.55**p
            add({"n2":"dose","p":p,"C":C}, r, r)
n2_block(FIRE)
json.dump({"counts":counts,"meta":meta,"n_backbone":20,"backend":"planted","pair":[95,99]},
          open("omega3_planted_pass.json","w"))
print("=== PLANTED PASS SIDE (single-mode truth) ===")
o3.analyse("omega3_planted_pass.json")
vp = json.load(open("omega3_verdicts.json"))
assert all(vp["backbone"].values()), f"backbone planted pass failed: {vp['backbone']}"
assert vp["n2"]["0"]["bracket"] and vp["n2"]["0"]["memory"] and vp["n2"]["0"]["monotone_premise"]
meta, counts = meta[:20], counts[:20]
n2_block(True)
json.dump({"counts":counts,"meta":meta,"n_backbone":20,"backend":"planted","pair":[95,99]},
          open("omega3_planted_fire.json","w"))
print("\n=== PLANTED FIRE SIDE (out-of-bracket dose + cycle memory) ===")
o3.analyse("omega3_planted_fire.json")
vf = json.load(open("omega3_verdicts.json"))
assert not vf["n2"]["0"]["bracket"], "bracket failed to fire"
assert not vf["n2"]["0"]["memory"], "memory failed to fire"
print("\nvalidate verdict: analyse path PASSES planted truth and FIRES planted violations. Two-sided.")
