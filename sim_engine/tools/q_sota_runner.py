#!/usr/bin/env python3
"""Run one external DMRG forcing case and emit a CIRIS comparison ledger.

DIAGNOSTIC ONLY: this is an independent comparator, not a q8-mps gate and not a
runtime dependency of any Rust crate.  It deliberately keeps the physical model,
initial state, optimizer schedule, carrier representation, and available
diagnostics in the same record.  In particular, a TeNPy ``chi`` is not silently
treated as identical to q8-mps's spin-orbital ``chi``: TeNPy uses one four-state
site per Hubbard site while q8-mps uses two two-state Jordan-Wigner orbitals.

The forcing case is the open, half-filled, Sz=0 Hubbard chain used by q-seam and
q8-mps.  Two product starts are supported because Q10 names initial-state trapping
as a live discriminator.  ``subspace-expansion`` selects TeNPy's implementation
of the Hubig et al. expansion named by Q10; ``none`` is its removal arm.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import platform
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCHEMA = "ciris.q-sota.run.v1"


def _finite_or_none(value: Any) -> float | None:
    """Convert a numeric scalar to finite JSON, preserving non-finite as null."""

    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _series(values: Iterable[Any] | None) -> list[float | None]:
    if values is None:
        return []
    return [_finite_or_none(value) for value in values]


def _finite_max(values: Iterable[Any] | None) -> float | None:
    finite = [value for value in _series(values) if value is not None]
    return max(finite) if finite else None


def _product_state(kind: str, sites: int) -> list[str]:
    if kind == "neel":
        return ["up" if site % 2 == 0 else "down" for site in range(sites)]
    if kind == "doublon-hole":
        return ["full" if site % 2 == 0 else "empty" for site in range(sites)]
    raise ValueError(f"unsupported initial state: {kind}")


def run_tenpy(args: argparse.Namespace) -> dict[str, Any]:
    import numpy as np
    import tenpy
    from tenpy.algorithms import dmrg
    from tenpy.algorithms.mps_common import SubspaceExpansion
    from tenpy.models.hubbard import FermiHubbardChain
    from tenpy.networks.mps import MPS

    logging.getLogger("tenpy").setLevel(logging.ERROR)

    model_params = {
        "L": args.sites,
        "t": args.t,
        "U": args.u,
        "mu": 0.0,
        "bc_MPS": "finite",
        "bc_x": "open",
        "cons_N": "N",
        "cons_Sz": "Sz",
    }
    model = FermiHubbardChain(model_params)
    labels = _product_state(args.initial_state, args.sites)
    psi = MPS.from_product_state(
        model.lat.mps_sites(),
        labels,
        bc=model.lat.bc_MPS,
        unit_cell_width=1,
    )

    mixer: bool | type[SubspaceExpansion]
    if args.mixer == "subspace-expansion":
        mixer = SubspaceExpansion
    else:
        mixer = False

    dmrg_params: dict[str, Any] = {
        "active_sites": 2,
        "mixer": mixer,
        "max_sweeps": args.max_sweeps,
        "max_E_err": args.sweep_tol,
        "N_sweeps_check": 1,
        "combine": True,
        "trunc_params": {
            "chi_max": args.chi_max,
            "svd_min": args.svd_min,
        },
        "lanczos_params": {"N_max": args.lanczos_max},
    }
    if mixer:
        dmrg_params["mixer_params"] = {
            "amplitude": args.mixer_amplitude,
            "decay": args.mixer_decay,
            "disable_after": args.mixer_disable_after,
        }

    started = time.perf_counter()
    info = dmrg.run(psi, model, dmrg_params)
    wall_seconds = time.perf_counter() - started

    energy = float(info["E"])
    sweep_statistics = info.get("sweep_statistics", {})
    energy_history = _series(sweep_statistics.get("E"))
    delta_energy_history = _series(sweep_statistics.get("Delta_E"))
    sweeps_used = len(energy_history)
    last_delta_energy = next(
        (value for value in reversed(delta_energy_history) if value is not None),
        None,
    )
    converged = sweeps_used < args.max_sweeps or (
        last_delta_energy is not None and abs(last_delta_energy) <= args.sweep_tol
    )

    occupation_up = np.asarray(psi.expectation_value("Nu"), dtype=float)
    occupation_down = np.asarray(psi.expectation_value("Nd"), dtype=float)
    density = occupation_up + occupation_down
    magnetization = occupation_up - occupation_down
    double_occupancy = np.asarray(psi.expectation_value("NuNd"), dtype=float)
    canonical_residual = float(np.max(np.abs(np.asarray(psi.norm_test()))))
    norm_squared = float(abs(psi.overlap(psi)))
    energy_variance = float(model.H_MPO.variance(psi))

    reference: dict[str, Any] | None = None
    if args.reference_energy is not None:
        absolute_error = abs(energy - args.reference_energy)
        reference = {
            "backend": args.reference_backend,
            "energy": args.reference_energy,
            "absolute_energy_error": absolute_error,
            "relative_energy_error": absolute_error / max(1.0, abs(args.reference_energy)),
        }

    return {
        "schema": SCHEMA,
        "status": "ok",
        "claim_scope": {
            "diagnostic_only": True,
            "gate": False,
            "purpose": "independent optimizer comparison and failure localization",
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
        "backend": {
            "name": "tenpy",
            "version": tenpy.__version__,
            "method": "finite two-site DMRG",
            "python": platform.python_version(),
        },
        "model": {
            "family": "one-dimensional open Hubbard chain",
            "sites": args.sites,
            "t": args.t,
            "u": args.u,
            "boundary": "open",
            "n_electrons": args.sites,
            "two_sz": 0,
            "chemical_potential": 0.0,
        },
        "representation": {
            "tensor_sites": args.sites,
            "local_dimension": 4,
            "orbital_order": "site-local up/down",
            "symmetries": ["particle number U(1)", "Sz U(1)"],
            "chi_comparable_to_q8_only_at_physical_site_cuts": True,
        },
        "initial_state": {
            "kind": args.initial_state,
            "site_labels": labels,
            "n_electrons": args.sites,
            "two_sz": 0,
        },
        "schedule": {
            "active_sites": 2,
            "chi_max": args.chi_max,
            "max_sweeps": args.max_sweeps,
            "sweep_energy_tolerance": args.sweep_tol,
            "svd_min": args.svd_min,
            "lanczos_max_iterations": args.lanczos_max,
            "mixer": args.mixer,
            "mixer_amplitude": args.mixer_amplitude if mixer else None,
            "mixer_decay": args.mixer_decay if mixer else None,
            "mixer_disable_after": args.mixer_disable_after if mixer else None,
        },
        "result": {
            "energy": energy,
            "energy_history": energy_history,
            "delta_energy_history": delta_energy_history,
            "sweeps_used": sweeps_used,
            "converged": converged,
            "wall_seconds": wall_seconds,
        },
        "observables": {
            "particle_number": float(np.sum(density)),
            "two_sz": float(np.sum(magnetization)),
            "occupation_up": occupation_up.tolist(),
            "occupation_down": occupation_down.tolist(),
            "density": density.tolist(),
            "magnetization": magnetization.tolist(),
            "double_occupancy": double_occupancy.tolist(),
            "double_occupancy_mean": float(np.mean(double_occupancy)),
        },
        "diagnostics": {
            "actual_bond_dimensions": [int(value) for value in psi.chi],
            "max_actual_chi": max(int(value) for value in psi.chi),
            "canonical_residual": canonical_residual,
            "norm_squared": norm_squared,
            "energy_variance": energy_variance,
            "last_delta_energy": last_delta_energy,
            "max_truncation_error": _finite_max(sweep_statistics.get("max_trunc_err")),
            "max_norm_error": _finite_max(sweep_statistics.get("norm_err")),
        },
        "reference": reference,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["tenpy"], default="tenpy")
    parser.add_argument("--sites", type=int, default=8)
    parser.add_argument("--t", type=float, default=1.0)
    parser.add_argument("--u", type=float, default=16.0)
    parser.add_argument("--chi-max", type=int, default=32)
    parser.add_argument("--max-sweeps", type=int, default=20)
    parser.add_argument("--sweep-tol", type=float, default=1e-10)
    parser.add_argument("--svd-min", type=float, default=1e-14)
    parser.add_argument("--lanczos-max", type=int, default=40)
    parser.add_argument(
        "--initial-state",
        choices=["neel", "doublon-hole"],
        default="neel",
    )
    parser.add_argument(
        "--mixer",
        choices=["none", "subspace-expansion"],
        default="none",
    )
    parser.add_argument("--mixer-amplitude", type=float, default=1e-5)
    parser.add_argument("--mixer-decay", type=float, default=2.0)
    parser.add_argument("--mixer-disable-after", type=int, default=15)
    parser.add_argument("--reference-energy", type=float)
    parser.add_argument("--reference-backend", default="q-seam 0.1.0")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if args.sites <= 0 or args.sites % 2 != 0:
        parser.error("--sites must be a positive even number for half-filled Sz=0")
    if args.chi_max <= 0 or args.max_sweeps <= 0 or args.lanczos_max <= 0:
        parser.error("bond dimension, sweeps, and Lanczos cap must be positive")
    return args


def main() -> int:
    args = parse_args()
    record = run_tenpy(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(record, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    result = record["result"]
    reference = record.get("reference")
    error = reference["absolute_energy_error"] if reference else None
    print(
        f"{record['backend']['name']} {args.initial_state} {args.mixer}: "
        f"E={result['energy']:.15f} dE={error!r} "
        f"sweeps={result['sweeps_used']} converged={result['converged']} "
        f"wall={result['wall_seconds']:.3f}s -> {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
