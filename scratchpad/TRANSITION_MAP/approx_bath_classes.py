"""Finite-time approximate bath-equivalence benchmark.

Preregistered in APPROX_BATH_CLASSES_PREREG.md before this file existed.
The evolution is the frozen 200-step midpoint piecewise-constant discretization.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply

HERE = Path(__file__).resolve().parent
NS = [128, 256, 512, 1024]
GS = [4, 8, 16, 32, 64, 128]
T = 20.0
NSTEPS = 200
DT = T / NSTEPS


def xi(t: float) -> np.ndarray:
    return np.array([
        0.5 * math.cos(0.7 * t) + 0.2 * math.cos(1.9 * t),
        0.5 * math.sin(0.7 * t) + 0.2 * math.sin(1.3 * t),
    ])


def smooth_profiles(n: int) -> np.ndarray:
    theta = 2.0 * math.pi * np.arange(n) / n
    return np.column_stack([np.cos(theta), np.sin(theta)])


def scrambled_profiles(n: int) -> np.ndarray:
    # Deterministic permutation coprime to every frozen power-of-two N.
    p = 37
    idx = (p * np.arange(n) + 11) % n
    return smooth_profiles(n)[idx]


def class_ids_from_profiles(A: np.ndarray, G: int) -> np.ndarray:
    ang = np.mod(np.arctan2(A[:, 1], A[:, 0]), 2.0 * math.pi)
    ids = np.floor(G * ang / (2.0 * math.pi) + 1e-12).astype(int)
    return np.minimum(ids, G - 1)


def centroids(A: np.ndarray, ids: np.ndarray, G: int):
    means = np.zeros((G, A.shape[1]))
    sizes = np.zeros(G, dtype=int)
    for g in range(G):
        mask = ids == g
        sizes[g] = int(mask.sum())
        if sizes[g]:
            means[g] = A[mask].mean(axis=0)
    keep = sizes > 0
    remap = -np.ones(G, dtype=int)
    remap[keep] = np.arange(int(keep.sum()))
    return means[keep], sizes[keep], remap[ids]


def max_row_residual(A: np.ndarray, means: np.ndarray, ids: np.ndarray) -> float:
    return float(np.max(np.linalg.norm(A - means[ids], axis=1)))


def arrowhead_sparse(energies: np.ndarray, couplings: np.ndarray) -> csr_matrix:
    m = len(energies)
    rows = []
    cols = []
    vals = []
    for j, e in enumerate(energies, start=1):
        rows.append(j); cols.append(j); vals.append(float(e))
        g = float(couplings[j - 1])
        rows.extend([0, j]); cols.extend([j, 0]); vals.extend([g, g])
    return csr_matrix((vals, (rows, cols)), shape=(m + 1, m + 1), dtype=complex)


def propagate(A: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, float]:
    q = np.zeros(len(A) + 1, dtype=complex)
    q[0] = 1.0
    pops = [1.0]
    t0 = time.perf_counter()
    for s in range(NSTEPS):
        tm = (s + 0.5) * DT
        energies = A @ xi(tm)
        H = arrowhead_sparse(energies, weights)
        q = expm_multiply((-1j * DT) * H, q, traceA=(-1j * DT) * H.diagonal().sum())
        pops.append(float(abs(q[0]) ** 2))
    elapsed = time.perf_counter() - t0
    return np.asarray(pops), elapsed


def certificate(max_resid: float) -> tuple[float, float]:
    # Exact Duhamel certificate for the frozen piecewise-constant schedule:
    # sum dt ||xi(tm)||_2 * max_i ||row residual_i||_2.
    integ = sum(DT * float(np.linalg.norm(xi((s + 0.5) * DT))) for s in range(NSTEPS))
    BT = integ * max_resid
    pop = min(1.0, 2.0 * BT + BT * BT)
    return float(BT), float(pop)


def run_family(A: np.ndarray) -> dict:
    n = len(A)
    full_weights = np.full(n, 1.0 / math.sqrt(n))
    truth, truth_time = propagate(A, full_weights)
    out = {"full_time_s": truth_time, "G": {}}
    for G in GS:
        if G > n:
            continue
        ids0 = class_ids_from_profiles(A, G)
        means, sizes, ids = centroids(A, ids0, G)
        w = np.sqrt(sizes / n)
        pred, elapsed = propagate(means, w)
        err = np.abs(pred - truth)
        resid = max_row_residual(A, means, ids)
        BT, cert = certificate(resid)
        out["G"][str(G)] = {
            "classes": int(len(means)),
            "max_row_residual": resid,
            "B_T": BT,
            "population_error_certificate": cert,
            "max_population_error": float(err.max()),
            "rmse_population": float(np.sqrt(np.mean(err * err))),
            "reduced_time_s": elapsed,
        }
    return out


def singleton_gate(A: np.ndarray) -> float:
    n = len(A)
    truth, _ = propagate(A, np.full(n, 1.0 / math.sqrt(n)))
    # Each emitter is its own exact class; ordering can be arbitrary.
    pred, _ = propagate(A.copy(), np.full(n, 1.0 / math.sqrt(n)))
    return float(np.max(np.abs(pred - truth)))


def main() -> None:
    result = {
        "prereg": "APPROX_BATH_CLASSES_PREREG.md",
        "time_discretization": {"T": T, "steps": NSTEPS, "scheme": "midpoint piecewise constant"},
        "cells": {},
        "gates": {},
        "stakes": {},
    }

    a1 = singleton_gate(smooth_profiles(128))
    max_perm_mismatch = 0.0
    max_cert_excess = -1e300

    for n in NS:
        print("N", n, flush=True)
        smooth = run_family(smooth_profiles(n))
        scrambled = run_family(scrambled_profiles(n))
        result["cells"][str(n)] = {"SMOOTH-RING": smooth, "SCRAMBLED-RING": scrambled}
        for G in GS:
            if G > n:
                continue
            a = smooth["G"][str(G)]
            b = scrambled["G"][str(G)]
            mismatch = abs(a["max_population_error"] - b["max_population_error"])
            max_perm_mismatch = max(max_perm_mismatch, mismatch)
            max_cert_excess = max(max_cert_excess, a["max_population_error"] - a["population_error_certificate"])
            max_cert_excess = max(max_cert_excess, b["max_population_error"] - b["population_error_certificate"])
            print(" G", G, "err", f"{a['max_population_error']:.3e}", "cert", f"{a['population_error_certificate']:.3e}", flush=True)

    result["gates"] = {
        "A1_singleton_max_error": a1,
        "A2_max_relabel_error_mismatch": max_perm_mismatch,
        "A3_max_observed_minus_certificate": max_cert_excess,
    }

    def min_g(n: int, family: str, tol: float = 1e-3):
        rows = result["cells"][str(n)][family]["G"]
        passing = [int(G) for G, x in rows.items() if x["max_population_error"] <= tol]
        return min(passing) if passing else None

    g256 = min_g(256, "SMOOTH-RING")
    g1024 = min_g(1024, "SMOOTH-RING")
    result["stakes"] = {
        "P1_N1024_Gle64": bool(g1024 is not None and g1024 <= 64),
        "P2_Nstable": bool(g256 is not None and g1024 is not None and g1024 <= 2 * g256 and g256 <= 2 * g1024),
        "P4_no_Gle128_meets": bool(g1024 is None),
        "min_G_1e-3": {str(n): min_g(n, "SMOOTH-RING") for n in NS},
    }

    (HERE / "approx_bath_classes_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("GATES", json.dumps(result["gates"], indent=2))
    print("STAKES", json.dumps(result["stakes"], indent=2))


if __name__ == "__main__":
    main()
