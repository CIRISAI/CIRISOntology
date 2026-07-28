#!/usr/bin/env python3
"""
Is the holonomy MAINTAINABLE?  --  the maintained-holonomy campaign.

Pre-registration: scratchpad/HOLONOMY_RENT_PREREG.md, committed at 3ae9c9b BEFORE
this file was written.  Read it first; this script implements it and nothing else.

WHAT THIS IS NOT.  The predecessor experiment
(coherence-ratchet/experiments/open_system_pomega/assumption_audit/holonomic_pomega/,
2026-05-22) measured the UNMAINTAINED Wilson-loop holonomy of the framework's genuine
emergence-map connection around the TSVF forward-backward loop, and found it decoheres:
hol_specrad(R) = 0.9655^(R-1), flowing to the zero operator.  HORN-empty; F-11 fired.
That verdict is correct as written and nothing here un-fires it.  Nothing measured here
is the unmaintained loop.

WHAT THIS IS.  A separate question the predecessor never asked: is that structure
MAINTAINABLE?  The connection is imported from the predecessor's own build code so that
W and B are bit-identical and ONLY the maintenance is new.  gamma*M is NOT varied --
the predecessor already closed that route (its Limits (3)).  The dephasing acts at full
framework strength at every rung; a separate repair operation pays back part of what it
took.

THE OBSERVABLES, and why there are two.  A repair can hold an operator's SIZE while its
DIRECTION wanders off the design.  A scalar ledger has one coordinate and cannot express
that; a 64x64 transport operator can.  So:
    gain      G(R,q) = ||Hol||_F / sqrt(d)          -- the ledger entry
    fidelity  F(R,q) = |<Hol_des,Hol>_F| / (||Hol_des||_F ||Hol||_F)   -- direction only
Gain is NOT the discovery axis (prereg 4.4: R-DES's plateau is near-structural, and both
arms coincide in the scalar limit).  Fidelity is.  Control C-RAND exists to prove it.
"""

import os
import sys

# Box is shared and loaded; stay polite.  Must precede the numpy import.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")
sys.dont_write_bytecode = True            # the predecessor tree is READ-ONLY

import importlib.util
import json
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "holonomy_rent_results.json")

PRED_DIR = ("/home/emoore/coherence-ratchet/experiments/open_system_pomega/"
            "assumption_audit/holonomic_pomega")
PRED_SRC = os.path.join(PRED_DIR, "build_holonomic_pomega.py")
PRED_JSON = os.path.join(PRED_DIR, "results_holonomic.json")

# ---------------------------------------------------------------------------
# The grid -- prereg section 8, fixed before any number.  No cell outside it
# enters a headline.
# ---------------------------------------------------------------------------
R_PRED = [3, 4, 5, 6, 7, 8, 9, 11, 13, 20, 30, 50]      # the predecessor's, verbatim
R_EXT = [75, 100, 150, 200, 300, 400]                    # the plateau extension
R_SCAN = R_PRED + R_EXT
R_MAX = max(R_SCAN)

EPS_RECEIVED = 0.0345                                    # RECEIVED, re-derived below
Q_GRID = [0.0, 0.001, 0.003, 0.01, 0.01725, 0.0345, 0.069,
          0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.99, 1.0]

N_STOCH = 64                                             # realizations, prereg section 7
STOCH_SEED0 = 20260727

SEED_CONN = 20260522                                     # the predecessor's connection seed
SEED_RAND = 20260727                                     # C-RAND's fixed random unitary
D = 64


def log(m):
    print(m, flush=True)


# ---------------------------------------------------------------------------
# Linear-algebra primitives.  Polar factors via SVD (backward stable), NEVER via
# an explicitly formed (A^dag A)^(-1/2)  --  prereg section 8.
# ---------------------------------------------------------------------------
def polar(A):
    """The nearest isometry to A in Frobenius norm: the unitary polar factor."""
    U, _, Vh = np.linalg.svd(A)
    return U @ Vh


def metrics(Hol, Hol_des, d, want_specrad=True):
    """The reported columns.  Denominators are named in the prereg section 3 table."""
    fro = float(np.linalg.norm(Hol))
    tr = complex(np.trace(Hol))
    sv = np.linalg.svd(Hol, compute_uv=False)
    sv_max, sv_min = float(sv[0]), float(sv[-1])

    # identity distance, plus the pre-registered catastrophic-cancellation cross-check
    fro_HmI = float(np.linalg.norm(Hol - np.eye(d)))
    inner = fro * fro - 2.0 * float(tr.real) + d
    alt = float(np.sqrt(max(inner, 0.0)))
    canc = abs(fro_HmI - alt) / max(fro_HmI, 1e-300)

    fro_des = float(np.linalg.norm(Hol_des))
    ov = complex(np.vdot(Hol_des, Hol))                  # <A,B>_F = Tr(A^dag B)
    fid = abs(ov) / max(fro_des * fro, 1e-300)

    out = dict(
        gain=fro / np.sqrt(d),                           # rms singular value
        hol_trace=abs(tr) / d,
        hol_id_dist=fro_HmI / np.sqrt(d),
        sv_max=sv_max, sv_min=sv_min,
        cond_ratio=sv_min / max(sv_max, 1e-300),
        fidelity=fid,
        cancel_rel=canc,
    )
    if want_specrad:
        out["specrad"] = float(np.max(np.abs(np.linalg.eigvals(Hol))))
    return out


# ---------------------------------------------------------------------------
# The repair maps -- prereg section 2.3.  Declared in advance; exactly two forms
# and three controls; no further form is introduced.
# ---------------------------------------------------------------------------
def rep_pol(A, q, _design):
    """R-POL, the PRIMARY arm.  Knows the CONSTRAINT (be an isometry) but NOT the
    design -- it does not know where the loop was supposed to point."""
    if q == 0.0:
        return A
    return (1.0 - q) * A + q * polar(A)


def rep_des(A, q, design):
    """R-DES, the CALIBRATION arm.  Deposits the design itself: the literal analogue
    of the maintenance sweep's decoder and of Core/Creation.lean's parityRepair."""
    if q == 0.0:
        return A
    return (1.0 - q) * A + q * design


def rep_rand(A, q, _design, U_rand=None):
    """C-RAND, the MIXTURE NULL.  Deposits a FIXED random unitary in place of the
    design.  If its gain plateau matches the genuine arms', gain alone is not
    evidence of maintenance and only fidelity discriminates."""
    if q == 0.0:
        return A
    return (1.0 - q) * A + q * U_rand


def rep_norm(A, _q, _design, d=D):
    """C-NORM, the FORBIDDEN move, run deliberately.  A pure scalar rescale restores
    the norm and cannot move direction -- a manufactured plateau, kept visible so a
    real one is distinguishable from it."""
    f = float(np.linalg.norm(A))
    if f <= 0.0:
        return A
    return A * (np.sqrt(d) / f)


ARMS = {"R-POL": rep_pol, "R-DES": rep_des}


# ---------------------------------------------------------------------------
# One pass down the loop.
# ---------------------------------------------------------------------------
def run_loop(W, B, Udes, repair, q, dosing, rng=None, U_rand=None,
             want_specrad=True, checkpoints=R_SCAN):
    """Walk the maintained TSVF loop out to R_MAX, reading off at each checkpoint.

        H_0 = I ;  H_k = Rep_q(B H_{k-1} ; design (CG^dag)^k) ;
        Hol_q(R) = H_{R-1} W^(R-1)

    The forward leg carries no repair because the repair is provably the identity
    there (both maps fix the isometries) -- asserted in the prereg, VERIFIED as
    gate C-NOOP, not assumed.

    dosing:
      'cont'   -- strength q at every rung
      'stoch'  -- full-strength repair with probability q, else none
      'per'    -- full-strength repair every round(1/q) rungs
    """
    d = W.shape[0]
    H = np.eye(d, dtype=np.complex128)
    Wp = np.eye(d, dtype=np.complex128)
    Dp = np.eye(d, dtype=np.complex128)       # the design backward accumulation
    period = int(round(1.0 / q)) if q > 0 else 0
    cps = set(checkpoints)
    rows, n_rep = {}, 0

    for k in range(1, R_MAX):
        H = B @ H
        Dp = Udes @ Dp
        Wp = W @ Wp

        if q > 0.0:
            if dosing == "cont":
                s = q
            elif dosing == "stoch":
                s = 1.0 if rng.random() < q else 0.0
            elif dosing == "per":
                s = 1.0 if (period > 0 and k % period == 0) else 0.0
            else:
                raise ValueError(dosing)
            if s > 0.0:
                n_rep += 1
                H = (repair(H, s, Dp) if U_rand is None
                     else repair(H, s, Dp, U_rand))

        R = k + 1
        if R in cps:
            rows[R] = metrics(H @ Wp, Dp @ Wp, d, want_specrad=want_specrad)
            rows[R]["n_repairs"] = n_rep

    return rows, Wp, Dp


# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    log("=" * 78)
    log("Is the holonomy MAINTAINABLE?  --  maintained-holonomy campaign")
    log("  prereg 3ae9c9b.  F-11 STAYS FIRED: the UNMAINTAINED loop does decohere,")
    log("  that verdict is correct as written, and nothing here is that loop.")
    log("=" * 78)

    # -- the connection, imported from the predecessor so it is bit-identical ----
    log(f"  importing the connection from {PRED_SRC}")
    spec = importlib.util.spec_from_file_location("bhp_pred", PRED_SRC)
    bhp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bhp)
    import cupy as cp
    Wc, Bc, Hc, Vc = bhp.build_connection(D, SEED_CONN)
    W = np.asarray(cp.asnumpy(Wc), dtype=np.complex128)
    B = np.asarray(cp.asnumpy(Bc), dtype=np.complex128)
    H_corr = np.asarray(cp.asnumpy(Hc), dtype=np.complex128)
    del Wc, Bc, Hc, Vc
    cp.get_default_memory_pool().free_all_blocks()

    gates = {}
    gates["c1_recomputed"] = float((0.31 * 0.72 * 1.15) ** (1.0 / 3.0))
    gates["c1_module"] = float(bhp.C1_RG)
    gates["W_isometry_resid"] = float(np.linalg.norm(W.conj().T @ W - np.eye(D)))
    gates["B_minus_Wdag"] = float(np.linalg.norm(B - W.conj().T))

    # -- the design transport, read OFF B, not chosen --------------------------
    # B = Deph . CG^dag with Deph Hermitian PSD, so B's LEFT polar decomposition
    # is B = P U with P = Deph and U = CG^dag.  The design backward step is that
    # polar unitary factor: the framework's own isometry property of the connection.
    Udes = polar(B)
    Deph = B @ Udes.conj().T
    gates["Udes_unitary_resid"] = float(np.linalg.norm(Udes.conj().T @ Udes - np.eye(D)))
    gates["Deph_hermitian_resid"] = float(np.linalg.norm(Deph - Deph.conj().T))
    dev = np.linalg.eigvalsh((Deph + Deph.conj().T) / 2)
    gates["Deph_eig_min"] = float(dev.min())
    gates["Deph_eig_max"] = float(dev.max())
    # cross-check the damping spectrum against the framework constants that built it
    w_hs = np.linalg.eigvalsh((H_corr + H_corr.conj().T) / 2)
    w_n = (w_hs - w_hs.min()) / max(w_hs.max() - w_hs.min(), 1e-12)
    damp_expect = np.sort(np.exp(-bhp.GAMMA * bhp.M_BASE * bhp.MIN_DWELL * w_n))
    gates["damp_spectrum_maxdev"] = float(np.max(np.abs(np.sort(dev) - damp_expect)))
    gates["gamma_deph"] = float(bhp.GAMMA * bhp.M_BASE)
    log(f"    ||W^dag W - I||      = {gates['W_isometry_resid']:.2e}")
    log(f"    ||B - W^dag||        = {gates['B_minus_Wdag']:.4f}")
    log(f"    design = polar(B):  unitary resid {gates['Udes_unitary_resid']:.2e}, "
        f"Deph spectrum [{gates['Deph_eig_min']:.4f}, {gates['Deph_eig_max']:.4f}], "
        f"vs framework constants max dev {gates['damp_spectrum_maxdev']:.2e}")

    # -- C-NOOP: the repair must not touch what is already at design -----------
    # Both maps must be exactly the identity on an isometry.  This is what makes
    # the word "repair" carry its meaning (Core/Creation.lean parityRepair_fixed_iff)
    # and it is why the forward leg needs no repair.
    noop = 0.0
    Utest = polar(np.random.default_rng(11).standard_normal((D, D))
                  + 1j * np.random.default_rng(12).standard_normal((D, D)))
    for q in Q_GRID:
        noop = max(noop, float(np.linalg.norm(rep_pol(Utest, q, None) - Utest)))
        noop = max(noop, float(np.linalg.norm(rep_des(Utest, q, Utest) - Utest)))
    gates["C_NOOP_max"] = noop
    gates["C_NOOP_pass"] = bool(noop < 1e-12)
    log(f"    C-NOOP  max ||Rep_q(U) - U|| = {noop:.2e}  "
        f"{'PASS' if gates['C_NOOP_pass'] else 'FAIL -- CAMPAIGN VOID'}")

    results = {"meta": dict(
        campaign="maintained holonomy -- is the decohering Wilson-loop holonomy MAINTAINABLE?",
        prereg="scratchpad/HOLONOMY_RENT_PREREG.md @ 3ae9c9b",
        f11="STAYS FIRED on its own terms; the unmaintained loop decoheres and nothing "
            "here is the unmaintained loop",
        connection_source=PRED_SRC, seed_conn=SEED_CONN, d=D,
        R_scan=R_SCAN, q_grid=Q_GRID, n_stoch=N_STOCH,
        design="polar(B) -- the polar unitary factor of the framework's own genuine "
               "backward generator, read off B, not chosen",
        note_q1="q=1 reproduces the design loop BY CONSTRUCTION and is a calibration "
                "endpoint, not evidence",
    ), "gates": gates, "arms": {}}

    def store(key, rows):
        results["arms"][key] = {str(R): rows[R] for R in sorted(rows)}

    # -- C-Q0 + the deterministic arms ----------------------------------------
    log("-" * 78)
    log("  deterministic arms (continuous and periodic dosing)")
    for arm, fn in ARMS.items():
        for dosing in ("cont", "per"):
            for q in Q_GRID:
                if q == 0.0 and (arm, dosing) != ("R-POL", "cont"):
                    continue                              # q=0 is one physical run
                rows, Wp, Dp = run_loop(W, B, Udes, fn, q, dosing)
                store(f"{arm}|{dosing}|q={q}", rows)
            log(f"    {arm} {dosing}: done  ({time.time()-t0:.1f}s)")

    # unitarity drift of the accumulated forward and design legs at max depth
    gates["Wpow_unitary_drift"] = float(np.linalg.norm(Wp.conj().T @ Wp - np.eye(D)))
    gates["Dpow_unitary_drift"] = float(np.linalg.norm(Dp.conj().T @ Dp - np.eye(D)))
    log(f"    accumulated-leg unitarity drift at R={R_MAX}: "
        f"W {gates['Wpow_unitary_drift']:.2e}, design {gates['Dpow_unitary_drift']:.2e}")

    # -- the controls ----------------------------------------------------------
    log("  controls: C-NORM (the forbidden scalar rescale) and C-RAND (the mixture null)")
    rows, _, _ = run_loop(W, B, Udes, rep_norm, 1.0, "cont")
    store("C-NORM|cont|q=1.0", rows)
    rng_u = np.random.default_rng(SEED_RAND)
    U_rand = polar(rng_u.standard_normal((D, D)) + 1j * rng_u.standard_normal((D, D)))
    for q in Q_GRID:
        if q == 0.0:
            continue
        rows, _, _ = run_loop(W, B, Udes, rep_rand, q, "cont", U_rand=U_rand)
        store(f"C-RAND|cont|q={q}", rows)

    # -- the stochastic dosing arm --------------------------------------------
    # specrad is computed on the deterministic arms only; the stochastic arm reports
    # gain and fidelity -- the primary and the discovery observables.  Recorded here
    # rather than left implicit.
    log(f"  stochastic dosing, {N_STOCH} realizations per cell "
        f"(seeds {STOCH_SEED0}..{STOCH_SEED0 + N_STOCH - 1})")
    results["meta"]["stoch_no_specrad"] = ("specrad computed on deterministic arms only; "
                                           "the stochastic arm reports gain and fidelity")
    for arm, fn in ARMS.items():
        for q in Q_GRID:
            if q == 0.0:
                continue
            acc = {R: {"gain": [], "fidelity": [], "n_repairs": []} for R in R_SCAN}
            for i in range(N_STOCH):
                rng = np.random.default_rng(STOCH_SEED0 + i)
                rows, _, _ = run_loop(W, B, Udes, fn, q, "stoch", rng=rng,
                                      want_specrad=False)
                for R in R_SCAN:
                    for kk in ("gain", "fidelity", "n_repairs"):
                        acc[R][kk].append(rows[R][kk])
            out = {}
            for R in R_SCAN:
                out[R] = {
                    "gain": float(np.mean(acc[R]["gain"])),
                    "gain_sd": float(np.std(acc[R]["gain"], ddof=1)),
                    "fidelity": float(np.mean(acc[R]["fidelity"])),
                    "fidelity_sd": float(np.std(acc[R]["fidelity"], ddof=1)),
                    "n_repairs": float(np.mean(acc[R]["n_repairs"])),
                }
            store(f"{arm}|stoch|q={q}", out)
        log(f"    {arm} stoch: done  ({time.time()-t0:.1f}s)")

    results["meta"]["elapsed_s"] = time.time() - t0
    with open(OUT, "w") as f:
        json.dump(results, f, indent=1)
    log(f"\ndone, {time.time()-t0:.1f}s.  raw -> {OUT}")


if __name__ == "__main__":
    main()
