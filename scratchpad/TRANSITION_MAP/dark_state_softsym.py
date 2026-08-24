#!/usr/bin/env python3
"""Soft-symmetry dark-state benchmark.

This is a deliberately small, substrate-independent instrument for the next K11
step.  It distinguishes three objects that should not be conflated:

  defect  = ||H - P H P||_F
  coupling = ||(I-|d><d|) H |d>||
  impurity = 1 - max_j |<v_j|d>|^2

For a Hermitian H and one transposition P with normalized odd state d,
coupling = defect/(2*sqrt(2)) exactly.  Impurity is a different, spectrum-
dependent quantity and is what PHYS-K11-1 S1b measured.

The benchmark plants an exact twin, adds a controlled symmetry-breaking
perturbation, checks the identity, and measures the short-time dark-state loss.
"""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass

import numpy as np
from scipy.linalg import eigh, expm


@dataclass
class Row:
    eps: float
    defect: float
    coupling: float
    identity_abs_error: float
    impurity: float
    survival_loss: float


def swap_matrix(n: int, a: int, b: int) -> np.ndarray:
    p = np.arange(n)
    p[a], p[b] = p[b], p[a]
    return np.eye(n)[p]


def dark_state(n: int, a: int, b: int) -> np.ndarray:
    d = np.zeros(n, dtype=complex)
    d[a] = 1 / np.sqrt(2)
    d[b] = -1 / np.sqrt(2)
    return d


def hermitian_random(n: int, rng: np.random.Generator) -> np.ndarray:
    x = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    h = (x + x.conj().T) / 2
    np.fill_diagonal(h, 0.0)
    return h


def project_twin_symmetric(h: np.ndarray, p: np.ndarray) -> np.ndarray:
    return (h + p @ h @ p) / 2


def observables(h: np.ndarray, p: np.ndarray, d: np.ndarray, t: float) -> tuple[float, ...]:
    proj_d = np.outer(d, d.conj())
    defect = np.linalg.norm(h - p @ h @ p, ord="fro")
    coupling = np.linalg.norm((np.eye(len(d)) - proj_d) @ h @ d)
    _, v = eigh(h)
    impurity = 1.0 - np.max(np.abs(v.conj().T @ d) ** 2)
    u = expm(-1j * h * t)
    survival_loss = 1.0 - abs(np.vdot(d, u @ d)) ** 2
    err = abs(coupling - defect / (2 * np.sqrt(2)))
    return defect, coupling, err, impurity, survival_loss


def block_basis(n: int, a: int, b: int) -> np.ndarray:
    """Unitary basis with dark state first and twin-even state second."""
    d = dark_state(n, a, b)
    s = np.zeros(n, dtype=complex)
    s[a] = s[b] = 1 / np.sqrt(2)
    cols = [d, s]
    cols.extend(np.eye(n, dtype=complex)[:, k] for k in range(n) if k not in (a, b))
    return np.column_stack(cols)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=101)
    ap.add_argument("--a", type=int, default=0)
    ap.add_argument("--b", type=int, default=1)
    ap.add_argument("--seed", type=int, default=20260822)
    ap.add_argument("--time", type=float, default=0.05, dest="t")
    ap.add_argument("--eps-min", type=float, default=1e-4)
    ap.add_argument("--eps-max", type=float, default=1e-1)
    ap.add_argument("--points", type=int, default=15)
    ap.add_argument("--output", default="dark_state_softsym_results.json")
    args = ap.parse_args()

    if args.a == args.b or not (0 <= args.a < args.n and 0 <= args.b < args.n):
        raise SystemExit("a and b must be distinct valid indices")

    rng = np.random.default_rng(args.seed)
    p = swap_matrix(args.n, args.a, args.b)
    d = dark_state(args.n, args.a, args.b)

    h_seed = hermitian_random(args.n, rng)
    h0 = project_twin_symmetric(h_seed, p)
    # Keep a zero diagonal so the exact eigenvalue is -H_ab, matching DarkState.lean.
    np.fill_diagonal(h0, 0.0)

    # Generic Hermitian perturbation, normalized so eps is a relative Frobenius dose.
    e = hermitian_random(args.n, rng)
    e /= np.linalg.norm(e, "fro")
    e *= np.linalg.norm(h0, "fro")

    exact_residual = np.linalg.norm(h0 @ d + h0[args.a, args.b] * d)

    q = block_basis(args.n, args.a, args.b)
    h0_block = q.conj().T @ h0 @ q
    exact_dark_to_bright = np.linalg.norm(h0_block[1:, 0])

    rows: list[Row] = []
    for eps in np.geomspace(args.eps_min, args.eps_max, args.points):
        h = h0 + eps * e
        vals = observables(h, p, d, args.t)
        rows.append(Row(eps, *vals))

    # Scaling checks use points safely above roundoff and below strong mixing.
    fit = rows[max(0, args.points // 4): max(2, 3 * args.points // 4)]
    x = np.log([r.eps for r in fit])
    coupling_slope = float(np.polyfit(x, np.log([r.coupling for r in fit]), 1)[0])
    loss_slope = float(np.polyfit(x, np.log([r.survival_loss for r in fit]), 1)[0])

    # A minimal timing comparison: full dense diagonalization versus diagonalizing
    # the exact twin-symmetric bright block only.  This is not a SOTA claim; it is
    # a sanity benchmark for the reduction that exact symmetry licenses.
    t0 = time.perf_counter()
    eigh(h0, eigvals_only=True)
    dense_seconds = time.perf_counter() - t0
    t0 = time.perf_counter()
    eigh(h0_block[1:, 1:], eigvals_only=True)
    bright_seconds = time.perf_counter() - t0

    out = {
        "config": vars(args),
        "exact_tier": {
            "dark_eigen_residual": float(exact_residual),
            "dark_to_bright_block_norm": float(exact_dark_to_bright),
        },
        "identity": "coupling = ||H-PHP||_F/(2*sqrt(2))",
        "max_identity_abs_error": float(max(r.identity_abs_error for r in rows)),
        "small_breaking_scaling": {
            "coupling_vs_eps_log_slope": coupling_slope,
            "survival_loss_vs_eps_log_slope": loss_slope,
            "expected": {"coupling": 1.0, "short_time_survival_loss": 2.0},
        },
        "timing_sanity": {
            "full_eigh_seconds": dense_seconds,
            "bright_block_eigh_seconds": bright_seconds,
            "speedup_ratio": dense_seconds / bright_seconds if bright_seconds else None,
            "warning": "single-run dense timing; benchmark methodology must be strengthened before any performance claim",
        },
        "rows": [asdict(r) for r in rows],
    }
    with open(args.output, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
