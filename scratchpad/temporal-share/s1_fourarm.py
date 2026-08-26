#!/usr/bin/env python3
"""S1 arm of COMPOSITION_PREREG.md — four-arm closure matrix with common-driver.

Arms: idle | one-way CRX(0->1) | reciprocal CRX both ways | common-driver
(X on both qubits vs none, two sub-circuits pooled 50/50 = a shared classical bit).
Frozen predictions in the prereg. Reuses the screened pair and validated machinery.
"""
import json, sys, itertools, importlib.util
import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

_s = importlib.util.spec_from_file_location("cp", "closure_pilot.py")
cp = importlib.util.module_from_spec(_s); _s.loader.exec_module(cp)

TOKEN = json.load(open('/home/emoore/Downloads/apikey (1).json'))['apikey']
SHOTS, THETA, TAU = 4096, np.pi/2, 16
ARMS = ("idle", "oneway", "recip", "cd_on", "cd_off")

def circuits():
    out = []
    for arm in ARMS:
        for a, b in itertools.product((0,1), repeat=2):
            qc = QuantumCircuit(2, 2)
            if a: qc.x(0)
            if b: qc.x(1)
            if arm == "oneway": qc.crx(THETA, 0, 1)
            elif arm == "recip": qc.crx(THETA, 0, 1); qc.crx(THETA, 1, 0)
            elif arm == "cd_on": qc.x(0); qc.x(1)      # the shared driver fired
            qc.barrier(); qc.delay(TAU, unit='dt'); qc.barrier()
            qc.measure([0,1],[0,1])
            qc.metadata = {"arm": arm, "a": a, "b": b}
            out.append(qc)
    return out

def created_corr(cbi):
    """I(A';B'|A,B) in nats from pooled counts, plus a pairing-shuffle floor."""
    tot, n_all = 0.0, 0
    rng = np.random.default_rng(20260826)
    nulls = np.zeros(2000)
    for key, c in cbi.items():
        n = sum(c.values()); n_all += n
        pa = np.zeros(2); pb = np.zeros(2); pj = np.zeros((2,2))
        for bits, k in c.items():
            A, B = int(bits[1]), int(bits[0])
            pj[A,B] += k/n; pa[A] += k/n; pb[B] += k/n
        mi = sum(pj[i,j]*np.log(pj[i,j]/(pa[i]*pb[j])) for i in (0,1) for j in (0,1) if pj[i,j]>0)
        tot += (n/1.0)*mi
        # floor: break the A'/B' pairing within this prep cell
        As = np.concatenate([np.full(k, int(bits[1])) for bits,k in c.items()])
        Bs = np.concatenate([np.full(k, int(bits[0])) for bits,k in c.items()])
        for p in range(2000):
            Bp = rng.permutation(Bs)
            pj2 = np.zeros((2,2))
            for A,B in zip(As,Bp): pj2[A,B]+=1
            pj2/=n; pa2=pj2.sum(1); pb2=pj2.sum(0)
            nulls[p] += n*sum(pj2[i,j]*np.log(pj2[i,j]/(pa2[i]*pb2[j])) for i in (0,1) for j in (0,1) if pj2[i,j]>0)
    return tot/n_all, float(np.percentile(nulls/n_all, 99.375))

def analyse_counts(counts):
    rng = np.random.default_rng(20260826)
    res = {}
    # pool cd_on + cd_off = the common-driver channel
    cd = {}
    for k in set(list(counts.get("cd_on",{}).keys()) + list(counts.get("cd_off",{}).keys())):
        m = {}
        for src in ("cd_on","cd_off"):
            for bits,v in counts.get(src,{}).get(k,{}).items(): m[bits]=m.get(bits,0)+v
        cd[k]=m
    counts = dict(counts); counts["cd"] = cd
    for arm in ("idle","oneway","recip","cd"):
        cbi = {(int(k[0]),int(k[1])):v for k,v in counts[arm].items()}
        dab, dba = cp.residual(cbi,'B'), cp.residual(cbi,'A')
        fab, fba = cp.perm_floor(cbi,'B',rng), cp.perm_floor(cbi,'A',rng)
        row = {"d_ab":dab,"f_ab":fab,"d_ba":dba,"f_ba":fba}
        if arm=="cd": row["created"], row["created_floor"] = created_corr(cbi)
        res[arm]=row
        extra = f"  created={row.get('created',0):.5f} (floor {row.get('created_floor',0):.5f})" if arm=="cd" else ""
        print(f"{arm:7} D_A->B={dab:.5f} ({dab/max(fab,1e-12):8.1f}x)  D_B->A={dba:.5f} ({dba/max(fba,1e-12):8.1f}x){extra}")
    return res

def verdict(res):
    v = {}
    v["idle"] = res["idle"]["d_ab"]<=res["idle"]["f_ab"] and res["idle"]["d_ba"]<=res["idle"]["f_ba"]
    ow = res["oneway"]; v["oneway"] = ow["d_ab"]>=max(50*ow["f_ab"],1e-3) and ow["d_ab"]>=20*max(ow["d_ba"],1e-12)
    rc = res["recip"]; v["recip"] = rc["d_ab"]>=max(20*rc["f_ab"],1e-3) and rc["d_ba"]>=max(20*rc["f_ba"],1e-3)
    cdr = res["cd"]; v["cd"] = (cdr["d_ab"]<=cdr["f_ab"] and cdr["d_ba"]<=cdr["f_ba"]
                               and cdr["created"]>cdr["created_floor"])
    return v

def validate():
    from qiskit.quantum_info import Operator
    rng = np.random.default_rng(3); labels=['00','01','10','11']; N=4096
    counts={}
    for arm in ARMS:
        counts[arm]={}
        for a,b in itertools.product((0,1),repeat=2):
            qc=QuantumCircuit(2)
            if a: qc.x(0)
            if b: qc.x(1)
            if arm=="oneway": qc.crx(THETA,0,1)
            elif arm=="recip": qc.crx(THETA,0,1); qc.crx(THETA,1,0)
            elif arm=="cd_on": qc.x(0); qc.x(1)
            U=Operator(qc).data; p=np.abs(U[:, 0])**2; p/=p.sum()  # prep is IN the circuit: column 0
            dr=rng.choice(4,size=N,p=p); c={}
            for k in dr: c[labels[k]]=c.get(labels[k],0)+1
            counts[arm][f"{a}{b}"]=c
    res=analyse_counts(counts); print("PLANTED VERDICTS:",verdict(res))

def run():
    scr=json.load(open("closure_pilot_screen.json")); pair=scr["selected"]
    svc=QiskitRuntimeService(channel="ibm_quantum_platform",token=TOKEN,instance="open-instance")
    bk=svc.backend(scr["backend"])
    pm=generate_preset_pass_manager(optimization_level=1,backend=bk,initial_layout=pair)
    circs=circuits()
    job=SamplerV2(mode=bk).run([pm.run(c) for c in circs],shots=SHOTS)
    print("S1 job:",job.job_id())
    res=job.result(); raw={}
    for r,c in zip(res,circs):
        m=c.metadata
        raw.setdefault(m["arm"],{})[f'{m["a"]}{m["b"]}']=r.data.c.get_counts()
    json.dump({"backend":bk.name,"job":job.job_id(),"pair":pair,"shots":SHOTS,"counts":raw},
              open(f"s1_fourarm_{job.job_id()}.json","w"),indent=2)
    a=analyse_counts(raw); v=verdict(a)
    json.dump({"scores":a,"verdict":v},open(f"s1_fourarm_{job.job_id()}_verdict.json","w"),indent=2,default=float)
    print("S1 VERDICTS:",v)

def fetch(jid):
    svc=QiskitRuntimeService(channel="ibm_quantum_platform",token=TOKEN,instance="open-instance")
    job=svc.job(jid); print("status:",job.status()); res=job.result()
    circs=circuits(); raw={}
    for r,c in zip(res,circs):
        m=c.metadata
        raw.setdefault(m["arm"],{})[f'{m["a"]}{m["b"]}']=r.data.c.get_counts()
    a=analyse_counts(raw); v=verdict(a)
    json.dump({"job":jid,"counts":raw,"scores":a,"verdict":v},
              open(f"s1_fourarm_{jid}.json","w"),indent=2,default=float)
    print("S1 VERDICTS:",v)

if __name__=="__main__":
    {"validate":validate,"run":run,"fetch":lambda:fetch(sys.argv[2])}[sys.argv[1]]()
