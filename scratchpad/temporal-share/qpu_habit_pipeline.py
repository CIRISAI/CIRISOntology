#!/usr/bin/env python3
"""The habit lifecycle on a QPU — pipeline per QPU_HABIT_PREREG.md.

MINT it from noise (Creation.lean `repair_creates_parity`), HOLD it under paid
maintenance, DEFAULT it when payment stops (Maintenance.lean `unpaid_decays`),
all read in share units by the exact k = 3 whole-only-share instrument.

Subcommands:
  freeze     pull + save the calibration snapshot and the pinned qubit triple
  bands      derive every pre-registered band from the noisy model (no hardware)
  gate       Aer gate on the gate-bearing (Job B) circuits (no hardware)
  jobA       the ONE pre-registered decay job
  jobB       the ONE pre-registered mint/rent job
  analyze A|B FILE.json    re-analyze saved counts
"""
import itertools
import json
import math
import sys
import time

import numpy as np

LN2 = math.log(2.0)
BACKEND_NAME = "ibm_marrakesh"
SEED = 20260725
RNG = np.random.default_rng(SEED)

# ---------------------------------------------------------------------------
# THE INSTRUMENT: exact whole-only share for three binary slots
# ---------------------------------------------------------------------------

def entropy(p):
    q = np.asarray(p, dtype=float).ravel()
    q = np.clip(q, 0.0, None)
    s = q.sum()
    if s <= 0:
        return 0.0
    q = q / s
    nz = q > 1e-15
    return float(-(q[nz] * np.log(q[nz])).sum())


def pairwise_maxent_exact(p, nbis=200):
    """EXACT pairwise maxent for three binary variables, by bisection.

    Numpy port of scratchpad/eca_spike.py:pairwise_maxent_exact (validated
    there against IPF; IPF one-sidedly overstates the share near the boundary,
    which is exactly where the late-delay points of this experiment live).
    """
    p = np.asarray(p, dtype=float).reshape(2, 2, 2)
    m12 = p.sum(axis=2); m13 = p.sum(axis=1); m23 = p.sum(axis=0)
    A = m12[0, 0]; B = m13[0, 0]; C = m23[0, 0]
    D = m12[0, 1] - m13[0, 0]
    E = m12[1, 0] - m23[0, 0]
    F = m13[1, 0] - m23[0, 0]
    G = m12[1, 1] - m13[1, 0] + m23[0, 0]
    lo = max(0.0, -D, -E, -F)
    hi = max(min(A, B, C, G), lo)

    def phi(t):
        return (t * (D + t) * (E + t) * (F + t)
                - (A - t) * (B - t) * (C - t) * (G - t))

    a, b = lo, hi
    fa = phi(a)
    for _ in range(nbis):
        m = 0.5 * (a + b)
        fm = phi(m)
        if fm * fa > 0:
            a, fa = m, fm
        else:
            b = m
    t = 0.5 * (a + b)
    q = np.empty((2, 2, 2))
    q[0, 0, 0] = t;     q[0, 0, 1] = A - t
    q[0, 1, 0] = B - t; q[0, 1, 1] = D + t
    q[1, 0, 0] = C - t; q[1, 0, 1] = E + t
    q[1, 1, 0] = F + t; q[1, 1, 1] = G - t
    return np.clip(q, 0.0, None)


def share(p):
    """I_C^(3): whole-only share in nats. share(parity) = ln 2, share(indep) =
    share(ferro) = 0 (Core/Third.lean, Core/SignSymmetry.lean)."""
    p = np.asarray(p, dtype=float).reshape(2, 2, 2)
    return entropy(pairwise_maxent_exact(p)) - entropy(p)


def s_total(p):
    """Total correlation: sum of single-slot entropies minus the whole's."""
    p = np.asarray(p, dtype=float).reshape(2, 2, 2)
    return (entropy(p.sum(axis=(1, 2))) + entropy(p.sum(axis=(0, 2)))
            + entropy(p.sum(axis=(0, 1))) - entropy(p))


def f_of_D(D):
    """Closed form for the share of `uniform + (D/8)*parity-sign`, the exact
    shape of every idle arm of this experiment: ln2 - h((1+D)/2)."""
    D = abs(float(D))
    if D >= 1.0:
        return LN2
    if D <= 0.0:
        return 0.0
    return 0.5 * ((1 + D) * math.log(1 + D) + (1 - D) * math.log(1 - D))


# ---------------------------------------------------------------------------
# MOMENTS: a 3-bit distribution <-> its eight Z-moments
# ---------------------------------------------------------------------------
# bit value x in {0,1}, z = (-1)^x.  Subsets encoded as 3-bit masks.

_Z = np.array([[1.0, -1.0]])

def moments(p):
    """p (2,2,2) -> M[mask] = <prod_{q in mask} z_q>, mask bit q = slot q."""
    p = np.asarray(p, dtype=float).reshape(2, 2, 2)
    M = np.zeros(8)
    for mask in range(8):
        sgn = np.ones((2, 2, 2))
        for q in range(3):
            if (mask >> q) & 1:
                shape = [1, 1, 1]; shape[q] = 2
                sgn = sgn * np.array([1.0, -1.0]).reshape(shape)
        M[mask] = float((p * sgn).sum())
    return M


def dist_from_moments(M):
    """Inverse: p(x) = (1/8) sum_mask M[mask] prod z_q."""
    p = np.zeros((2, 2, 2))
    for x in itertools.product((0, 1), repeat=3):
        acc = 0.0
        for mask in range(8):
            s = 1.0
            for q in range(3):
                if (mask >> q) & 1 and x[q] == 1:
                    s = -s
            acc += M[mask] * s
        p[x] = acc / 8.0
    return p


def apply_product_channel(M, kappa, b):
    """Each slot: z_q -> kappa_q z_q + b_q.  Exact for independent asymmetric
    bit-flip channels (amplitude damping, thermal, readout) — the whole physics
    of every idle arm here."""
    M2 = np.zeros(8)
    for mask in range(8):
        # M2[mask] = sum over subsets U of mask: prod kappa (U) prod b (mask\U) M[U]
        sub = mask
        acc = 0.0
        while True:
            coef = 1.0
            for q in range(3):
                if (mask >> q) & 1:
                    coef *= kappa[q] if (sub >> q) & 1 else b[q]
            acc += coef * M[sub]
            if sub == 0:
                break
            sub = (sub - 1) & mask
        M2[mask] = acc
    return M2


def damping_channel(t_us, T1_us, p_exc):
    """Amplitude damping for time t: kappa = exp(-t/T1), asymptote <Z> = 1-2p."""
    kappa = np.array([math.exp(-t_us / T1) for T1 in T1_us])
    m = np.array([1.0 - 2.0 * p for p in p_exc])
    b = (1.0 - kappa) * m
    return kappa, b


def readout_channel(e0, e1):
    """e0 = P(read 1 | prep 0), e1 = P(read 0 | prep 1)."""
    kappa = np.array([1.0 - a - b for a, b in zip(e0, e1)])
    b = np.array([b_ - a_ for a_, b_ in zip(e0, e1)])
    return kappa, b


# ---------------------------------------------------------------------------
# READOUT CORRECTION (per-qubit inverse assignment, as in bell_pipeline.py)
# ---------------------------------------------------------------------------

def assignment_matrices(v0, v1):
    """v0, v1: measured 8-vectors for prepared |000> and |111>.
    Returns per-slot A[meas, true]."""
    mats = []
    for q in range(3):
        p1_0 = sum(v for i, v in enumerate(v0) if (i >> q) & 1)
        p1_1 = sum(v for i, v in enumerate(v1) if (i >> q) & 1)
        mats.append(np.array([[1 - p1_0, 1 - p1_1], [p1_0, p1_1]]))
    return mats


def correct_readout(p, amats):
    t = np.asarray(p, dtype=float).reshape(2, 2, 2)
    for q in range(3):
        Ainv = np.linalg.inv(amats[q])
        t = np.tensordot(Ainv, t, axes=([1], [q]))
        t = np.moveaxis(t, 0, q)
    return t.reshape(2, 2, 2)


# ---------------------------------------------------------------------------
# ESTIMATOR FLOOR (discipline item 5: a matched surrogate floor, always)
# ---------------------------------------------------------------------------

def floor_share(p, shots, reps=300, rng=None):
    """Mean + sd of the share estimator under the matched INDEPENDENT surrogate
    (product of p's own single-slot marginals) at the same shot count."""
    rng = rng or RNG
    p = np.asarray(p, dtype=float).reshape(2, 2, 2)
    m = [p.sum(axis=(1, 2)), p.sum(axis=(0, 2)), p.sum(axis=(0, 1))]
    prod = np.einsum('i,j,k->ijk', *[np.clip(x, 0, None) / max(x.sum(), 1e-12) for x in m])
    prod = np.clip(prod.ravel(), 0, None); prod = prod / prod.sum()
    vals = [share(rng.multinomial(shots, prod) / shots) for _ in range(reps)]
    return float(np.mean(vals)), float(np.std(vals))


def D_stat(p):
    """The connected 3-body moment: M_123 - M_1 M_2 M_3.  For every idle arm of
    this experiment the pair-connected moments vanish identically, so this is
    the whole of the whole-only content, and share = f_of_D(D)."""
    M = moments(p)
    return float(M[7] - M[1] * M[2] * M[4])


# ---------------------------------------------------------------------------
# CIRCUITS
# ---------------------------------------------------------------------------
# slot order everywhere is (a, b, c) = (data, data, check).
# physical mapping: a = TRIPLE[0], c = TRIPLE[1] (the middle, adjacent to both),
# b = TRIPLE[2].

def _qc(nc=3, extra=0):
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
    q = QuantumRegister(3, "q")          # q[0]=a, q[1]=c(middle), q[2]=b
    c = ClassicalRegister(3, "c")
    regs = [q, c]
    if extra:
        regs.append(ClassicalRegister(extra, "m"))
    qc = QuantumCircuit(*regs)
    return qc, q, c, (qc.cregs[2] if extra else None)


def _basis_rot(qc, q, basis):
    """basis: 3 chars over {X,Y,Z}, one per SLOT (a,b,c) -> qubits 0,2,1."""
    slot2q = {0: 0, 1: 2, 2: 1}
    for slot, ch in enumerate(basis):
        k = slot2q[slot]
        if ch == "X":
            qc.h(q[k])
        elif ch == "Y":
            qc.sdg(q[k]); qc.h(q[k])


def _measure_all(qc, q, creg):
    for slot, k in ((0, 0), (1, 2), (2, 1)):
        qc.measure(q[k], creg[slot])


def circ_idle(prep, basis, delay_us):
    """prep in {ghz, classical, product, exc}; idle `delay_us`; read in `basis`."""
    qc, q, c, _ = _qc()
    if prep == "ghz":
        qc.h(q[1]); qc.cx(q[1], q[0]); qc.cx(q[1], q[2])
    elif prep == "classical":
        m = _add_creg(qc, 2, "m")
        qc.h(q[0]); qc.h(q[2])
        qc.measure(q[0], m[0]); qc.measure(q[2], m[1])   # collapse -> classical
        qc.cx(q[0], q[1]); qc.cx(q[2], q[1])             # c := a XOR b
    elif prep == "product":
        m = _add_creg(qc, 3, "m")
        qc.h(q[0]); qc.h(q[1]); qc.h(q[2])
        qc.measure(q[0], m[0]); qc.measure(q[1], m[1]); qc.measure(q[2], m[2])
    elif prep == "exc":
        qc.x(q[0]); qc.x(q[1]); qc.x(q[2])
    elif prep == "gnd":
        pass
    else:
        raise ValueError(prep)
    qc.barrier()
    if delay_us > 0:
        for k in range(3):
            qc.delay(delay_us, q[k], unit="us")
        qc.barrier()
    _basis_rot(qc, q, basis)
    _measure_all(qc, q, c)
    return qc


def _add_creg(qc, n, name):
    from qiskit import ClassicalRegister
    r = ClassicalRegister(n, name)
    qc.add_register(r)
    return r


def circ_mint(kind):
    """kind: 'parity' (the Lean repair), 'copy' (wrong code: c := a),
    'none' (no repair; the false-positive floor)."""
    qc, q, c, _ = _qc()
    m = _add_creg(qc, 3, "m")
    qc.h(q[0]); qc.h(q[1]); qc.h(q[2])
    qc.measure(q[0], m[0]); qc.measure(q[2], m[1]); qc.measure(q[1], m[2])
    qc.barrier()
    if kind == "parity":
        qc.reset(q[1])
        qc.cx(q[0], q[1]); qc.cx(q[2], q[1])
    elif kind == "copy":
        qc.reset(q[1])
        qc.cx(q[0], q[1])
    elif kind == "none":
        qc.delay(3, q[0], unit="us"); qc.delay(3, q[1], unit="us")
        qc.delay(3, q[2], unit="us")
    else:
        raise ValueError(kind)
    qc.barrier()
    _measure_all(qc, q, c)
    return qc


def circ_rent(n_cycles, total_us):
    """Birth the parity habit, then n cycles of [idle, repair] over `total_us`.
    n_cycles = 0 is the DEFAULT (unpaid) arm."""
    qc, q, c, _ = _qc()
    m = _add_creg(qc, 2, "m")
    qc.h(q[0]); qc.h(q[2])
    qc.measure(q[0], m[0]); qc.measure(q[2], m[1])
    qc.cx(q[0], q[1]); qc.cx(q[2], q[1])
    qc.barrier()
    if n_cycles == 0:
        for k in range(3):
            qc.delay(total_us, q[k], unit="us")
    else:
        dt = total_us / n_cycles
        for _ in range(n_cycles):
            for k in range(3):
                qc.delay(dt, q[k], unit="us")
            qc.barrier()
            qc.reset(q[1])
            qc.cx(q[0], q[1]); qc.cx(q[2], q[1])
            qc.barrier()
    _measure_all(qc, q, c)
    return qc


def circ_cal(state):
    qc, q, c, _ = _qc()
    if state == "111":
        qc.x(q[0]); qc.x(q[1]); qc.x(q[2])
    _measure_all(qc, q, c)
    return qc


# ---------------------------------------------------------------------------
# COUNTS -> distribution
# ---------------------------------------------------------------------------

def counts_to_p(counts):
    """Qiskit creg string is little-endian: rightmost char = bit 0 = slot 0."""
    p = np.zeros(8)
    tot = 0
    for key, n in counts.items():
        bits = key.replace(" ", "")
        idx = 0
        for s in range(3):
            if bits[-1 - s] == "1":
                idx |= 1 << s
        p[idx] += n
        tot += n
    return (p / max(tot, 1)).reshape(2, 2, 2)


# ---------------------------------------------------------------------------
# JOB PLANS
# ---------------------------------------------------------------------------

def load_freeze(path="qpu_habit_freeze.json"):
    with open(path) as f:
        return json.load(f)


def plan_A(fz):
    """(tag, circuit, shots) list for the decay job."""
    dQ = fz["delays_quantum_us"]; dC = fz["delays_classical_us"]
    dT = fz["delays_t1_us"]
    sh = fz["shots"]
    plan = []
    for t in dC:
        plan.append((f"A1|classical|ZZZ|{t}", circ_idle("classical", "ZZZ", t), sh["A1"]))
    for t in dQ:
        plan.append((f"A2|ghz|XXX|{t}", circ_idle("ghz", "XXX", t), sh["A2"]))
        plan.append((f"A3|ghz|YXX|{t}", circ_idle("ghz", "YXX", t), sh["A2"]))
    for t in fz["delays_control_us"]:
        plan.append((f"A4|ghz|ZZZ|{t}", circ_idle("ghz", "ZZZ", t), sh["A4"]))
        plan.append((f"A5|classical|XXX|{t}", circ_idle("classical", "XXX", t), sh["A4"]))
    for t in fz["delays_product_us"]:
        plan.append((f"A6|product|ZZZ|{t}", circ_idle("product", "ZZZ", t), sh["A4"]))
    for t in dT:
        plan.append((f"A7|exc|ZZZ|{t}", circ_idle("exc", "ZZZ", t), sh["A7"]))
    plan.append(("A8|cal|000|0", circ_cal("000"), sh["A8"]))
    plan.append(("A8|cal|111|0", circ_cal("111"), sh["A8"]))
    return plan


def plan_B(fz):
    sh = fz["shots"]
    plan = []
    for kind in ("parity", "copy", "none"):
        plan.append((f"B1|mint|{kind}|0", circ_mint(kind), sh["B1"]))
    for T in fz["rent_totals_us"]:
        for n in fz["rent_cycles"]:
            plan.append((f"B2|rent|{n}|{T}", circ_rent(n, T), sh["B2"]))
    plan.append(("B3|cal|000|0", circ_cal("000"), sh["A8"]))
    plan.append(("B3|cal|111|0", circ_cal("111"), sh["A8"]))
    return plan


def estimate_seconds(plan, rep_delay_us=252.0):
    """Budget model calibrated on the Bell run (488x1024 shots = 134 s)."""
    tot = 0.0
    for tag, qc, shots in plan:
        d = 0.0
        for inst in qc.data:
            nm = inst.operation.name
            if nm == "delay" and qc.find_bit(inst.qubits[0]).index == 0:
                # delays are applied to all three qubits in parallel: count once
                u = inst.operation.unit
                v = inst.operation.params[0]
                d += v if u == "us" else (v * 1e6 if u == "s" else v * 4e-3)
            elif nm in ("measure", "reset") and qc.find_bit(inst.qubits[0]).index == 0:
                d += 2.2
        tot += shots * (rep_delay_us + d) * 1e-6
    return tot


# ---------------------------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------------------------

def analyze_records(records, fz, job):
    """records: list of {tag, counts}.  Returns the full verdict dict."""
    by = {}
    for r in records:
        by[r["tag"]] = counts_to_p(r["counts"])
    calkey0 = [k for k in by if k.startswith(("A8|cal|000", "B3|cal|000"))][0]
    calkey1 = [k for k in by if k.startswith(("A8|cal|111", "B3|cal|111"))][0]
    amats = assignment_matrices(by[calkey0].ravel(), by[calkey1].ravel())
    ro_fid = float(min(min(A[0, 0], A[1, 1]) for A in amats))
    out = {"readout_fid_min": ro_fid, "arms": {}}
    for tag, p in by.items():
        pc = correct_readout(p, amats)
        pc = np.clip(pc, 0, None); pc = pc / pc.sum()
        out["arms"][tag] = {
            "share_raw": share(p), "share_corr": share(pc),
            "S_total_raw": s_total(p), "S_total_corr": s_total(pc),
            "D_raw": D_stat(p), "D_corr": D_stat(pc),
            "marg_raw": [float(x) for x in
                         (p.sum(axis=(1, 2))[1], p.sum(axis=(0, 2))[1], p.sum(axis=(0, 1))[1])],
        }
    return out


def fit_T1(ts, p1s, floor=0.0):
    """P(1|t) = (A - m) exp(-t/T1) + m, least squares over (A, m, T1)."""
    from scipy.optimize import curve_fit
    ts = np.asarray(ts, float); p1s = np.asarray(p1s, float)

    def model(t, A, m, T1):
        return (A - m) * np.exp(-t / T1) + m
    best = None
    for T0 in (100.0, 200.0, 350.0, 600.0):
        p0 = [min(max(p1s[0], 0.5), 1.0), min(max(p1s[-1], 1e-3), 0.4), T0]
        try:
            popt, pcov = curve_fit(model, ts, p1s, p0=p0, maxfev=40000,
                                   bounds=([0, 0, 5], [1, 0.5, 5000]))
            r = model(ts, *popt) - p1s
            ss = float(np.sum(r ** 2))
            if best is None or ss < best[0]:
                best = (ss, popt, pcov)
        except Exception:
            continue
    if best is None:
        return dict(error="all starts failed")
    _, popt, pcov = best
    return dict(A=float(popt[0]), p_exc=float(popt[1]), T1=float(popt[2]),
                T1_err=float(np.sqrt(abs(pcov[2, 2]))))


def wls_logfit(ts, ys, sigmas):
    """Weighted least squares of log y on t; returns (rate, rate_sd)."""
    ts = np.asarray(ts, float); ys = np.asarray(ys, float)
    w = 1.0 / np.asarray(sigmas, float) ** 2
    X = np.vstack([np.ones_like(ts), ts]).T
    W = np.diag(w)
    cov = np.linalg.inv(X.T @ W @ X)
    beta = cov @ (X.T @ W @ np.log(ys))
    return float(-beta[1]), float(math.sqrt(cov[1, 1]))


# ---------------------------------------------------------------------------
# RUNNERS
# ---------------------------------------------------------------------------

def _service():
    from qiskit_ibm_runtime import QiskitRuntimeService
    return QiskitRuntimeService()


def cmd_freeze():
    """Pin the qubit triple by the pre-registered rule and snapshot calibration."""
    svc = _service()
    b = svc.backend(BACKEND_NAME)
    props = b.properties()
    n = b.num_qubits
    T1 = {q: props.t1(q) * 1e6 for q in range(n)}
    T2 = {q: props.t2(q) * 1e6 for q in range(n)}
    ro = {q: props.readout_error(q) for q in range(n)}
    e0 = {q: props.qubit_property(q, "prob_meas1_prep0")[0] for q in range(n)}
    e1 = {q: props.qubit_property(q, "prob_meas0_prep1")[0] for q in range(n)}
    cz = {}
    for g in props.gates:
        if g.gate == "cz" and len(g.qubits) == 2:
            try:
                cz[tuple(sorted(g.qubits))] = props.gate_error("cz", g.qubits)
            except Exception:
                pass
    adj = {q: set() for q in range(n)}
    for (i, j) in cz:
        adj[i].add(j); adj[j].add(i)

    # PRE-REGISTERED SELECTION RULE (stated in QPU_HABIT_PREREG.md §2):
    #   over all paths a-c-b (c adjacent to both),
    #   filter  ro <= 0.015 (all three), cz error <= 0.004 (both edges),
    #           T1 in [120, 400] us (all three), T2 >= 30 us (all three)
    #   minimise  sum(ro) + 10 * sum(cz error)      [readout dominates the read]
    #   tie-break maximise min(T2)
    cands = []
    for c in range(n):
        for a in adj[c]:
            for bq in adj[c]:
                if bq <= a:
                    continue
                trip = [a, c, bq]
                if max(ro[q] for q in trip) > 0.015:
                    continue
                eac = cz[tuple(sorted((a, c)))]; ecb = cz[tuple(sorted((c, bq)))]
                if max(eac, ecb) > 0.004:
                    continue
                if not all(120.0 <= T1[q] <= 400.0 for q in trip):
                    continue
                if min(T2[q] for q in trip) < 30.0:
                    continue
                cost = sum(ro[q] for q in trip) + 10 * (eac + ecb)
                cands.append((cost, -min(T2[q] for q in trip), trip, eac, ecb))
    cands.sort()
    if not cands:
        raise SystemExit("no triple passes the pre-registered filter")
    cost, negT2, trip, eac, ecb = cands[0]
    a, c, bq = trip
    slots = [a, bq, c]          # slot order (a, b, c=check)

    T1s = [T1[q] for q in slots]
    T2s = [T2[q] for q in slots]
    rate_share_cl = 2.0 * sum(1.0 / x for x in T1s)      # nats-decay rate, classical
    rate_share_q = 2.0 * sum(1.0 / x for x in T2s)       # nats-decay rate, quantum

    def dt_align(x):
        """IBM delays must be whole numbers of 16 dt = 64 ns."""
        return round(round(x / 0.064) * 0.064, 3)

    def grid(rate, npts, lo_frac=0.0):
        """Log-spaced-ish delays covering share from ln2 down to ~1e-3 nat."""
        tmax = math.log(LN2 / 1e-3) / rate
        xs = [0.0] + [tmax * (i / (npts - 1)) ** 1.35 for i in range(1, npts)]
        return [dt_align(x) for x in xs]

    fz = {
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "backend": BACKEND_NAME,
        "triple_path": trip, "slots_abc": slots,
        "selection_cost": cost,
        "cal": {
            "T1_us": {str(q): T1[q] for q in slots},
            "T2_us": {str(q): T2[q] for q in slots},
            "readout_error": {str(q): ro[q] for q in slots},
            "prob_meas1_prep0": {str(q): e0[q] for q in slots},
            "prob_meas0_prep1": {str(q): e1[q] for q in slots},
            "cz_error": {f"{a}_{c}": eac, f"{c}_{bq}": ecb},
        },
        "predicted_rate_classical_per_us": rate_share_cl,
        "predicted_rate_quantum_per_us": rate_share_q,
        "delays_classical_us": grid(rate_share_cl, 9),
        "delays_quantum_us": grid(rate_share_q, 6),
        "delays_control_us": None,
        "delays_product_us": None,
        "delays_t1_us": None,
        "shots": {"A1": 8192, "A2": 4096, "A4": 4096, "A7": 4096, "A8": 8192,
                  "B1": 8192, "B2": 8192},
        "rent_cycles": [0, 1, 2, 4],
    }
    dC = fz["delays_classical_us"]
    fz["delays_control_us"] = [dC[0], dC[3], dC[6]]
    fz["delays_product_us"] = [dC[0], dC[6]]
    T1med = sum(T1s) / 3
    fz["delays_t1_us"] = [dt_align(x) for x in
                          (0.0, 0.3 * T1med, 0.7 * T1med, 1.2 * T1med, 1.8 * T1med)]
    fz["rent_totals_us"] = [dC[3], dC[5]]
    with open("qpu_habit_freeze.json", "w") as f:
        json.dump(fz, f, indent=2)
    print(json.dumps(fz, indent=2))
    plan = plan_A(fz)
    print("JOB A circuits:", len(plan), "est seconds: %.1f" % estimate_seconds(plan))
    planb = plan_B(fz)
    print("JOB B circuits:", len(planb), "est seconds: %.1f" % estimate_seconds(planb))
    return 0


def run_job(which, fz, dry=False):
    from qiskit import transpile
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
    svc = _service()
    backend = svc.backend(BACKEND_NAME)
    plan = plan_A(fz) if which == "A" else plan_B(fz)
    est = estimate_seconds(plan)
    print(f"JOB {which}: {len(plan)} circuits, estimated {est:.1f} QPU seconds")
    if dry:
        return 0
    layout = fz["slots_abc"]
    layout_phys = [layout[0], layout[2], layout[1]]   # circuit q0,q1,q2 = a,c,b
    circs = [transpile(qc, backend, optimization_level=1,
                       initial_layout=layout_phys, seed_transpiler=SEED)
             for _, qc, _ in plan]
    shots = [s for _, _, s in plan]
    sampler = SamplerV2(mode=backend)
    t0 = time.time()
    pubs = [(c, None, s) for c, s in zip(circs, shots)]
    job = sampler.run(pubs)
    print("job id:", job.job_id(), flush=True)
    res = job.result()
    print("wall seconds:", round(time.time() - t0, 1))
    try:
        meta = job.metrics()
        print("usage seconds:", meta.get("usage", {}).get("quantum_seconds"))
    except Exception as e:
        meta = {"err": str(e)}
    recs = []
    for i, (tag, qc, _) in enumerate(plan):
        db = res[i].data
        rec = {"tag": tag, "counts": db.c.get_counts()}
        if hasattr(db, "m"):
            rec["counts_m"] = db.m.get_counts()
            # per-shot join: the mint circuit's 'm' IS the input state and its
            # 'c' the output, on the SAME shots (both sides of the theorem)
            try:
                cs = db.c.get_bitstrings(); ms = db.m.get_bitstrings()
                joint = {}
                for x, y in zip(cs, ms):
                    k = f"{x}|{y}"
                    joint[k] = joint.get(k, 0) + 1
                rec["counts_joint_c_m"] = joint
            except Exception as e:
                rec["joint_err"] = str(e)
        recs.append(rec)
    fname = f"qpu_habit_{which}_{job.job_id()}.json"
    with open(fname, "w") as f:
        json.dump({"backend": BACKEND_NAME, "job_id": job.job_id(),
                   "which": which, "metrics": meta,
                   "freeze": fz, "records": recs}, f)
    print("saved", fname)
    return fname


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "freeze"
    if cmd == "freeze":
        sys.exit(cmd_freeze())
    elif cmd in ("jobA", "jobB"):
        fz = load_freeze()
        dry = "--dry" in sys.argv
        run_job(cmd[-1], fz, dry=dry)
    else:
        raise SystemExit(f"unknown command {cmd}")
