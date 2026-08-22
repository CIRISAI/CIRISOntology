#!/usr/bin/env python3
"""
REG+ hydrodynamics reference reconstruction.

IMPORTANT EVIDENCE STATUS
-------------------------
This is a cleaned, reproducible reconstruction of the microscopic rules discussed
in the 2026-08-21 ChatGPT session. No original source file from those chat runs
existed. Therefore this package is NOT a bit-for-bit recovery of prior testimony.
Fresh outputs produced by this code are new artifacts; the earlier chat numbers
remain testimony unless independently reproduced.

Scope:
  * six carries directions on a triangular/hexagonal lattice
  * 2^6 = 64 local occupancy states
  * exact local (N, Px, Py) conservation sectors
  * FHP-I positive-control collision
  * reversible sector-permutation collision
  * REG coherent sector unitary U_{N,P}(W), followed by Born/dephasing read
  * fixed-W and annealed dephasing controls
  * kinetic (molecular-chaos) ensemble closure for low-noise transport estimates

There is no pressure projection, Navier-Stokes advection term, viscosity term,
or verdict/accountability readout in the microscopic update.

The non-zero-holonomy transport experiment is prereg-gated by default.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np

VERSION = "0.1.0-r1-reconstruction"

# Six equally spaced physical velocities.
ANGLES = np.arange(6, dtype=float) * np.pi / 3.0
CART_VELOCITIES = np.stack([np.cos(ANGLES), np.sin(ANGLES)], axis=1)

# Integer axial-lattice carries used for exact periodic streaming.
# Direction a+3 is the reverse of direction a.
AXIAL_CARRIES = np.array(
    [[1, 0], [0, 1], [-1, 1], [-1, 0], [0, -1], [1, -1]],
    dtype=int,
)

STATES = np.arange(64, dtype=int)
BITS = ((STATES[:, None] >> np.arange(6)) & 1).astype(np.int8)
N_PART = BITS.sum(axis=1)
P_AXIAL = BITS @ AXIAL_CARRIES

SECTORS: Dict[Tuple[int, int, int], List[int]] = {}
for s in STATES:
    key = (int(N_PART[s]), int(P_AXIAL[s, 0]), int(P_AXIAL[s, 1]))
    SECTORS.setdefault(key, []).append(int(s))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -40.0, 40.0)))


def max_entropy_channel_probs(
    rho: float,
    ux: float,
    uy: float,
    tol: float = 1e-12,
    max_iter: int = 80,
) -> np.ndarray:
    """Independent Bernoulli maximum-entropy channel probabilities.

    Solves for p_a = sigmoid(alpha + beta_x c_ax + beta_y c_ay) such that
      sum_a p_a = rho
      sum_a p_a c_a = rho * u.

    This is an initialization / kinetic-closure instrument, not a fluid equation.
    """
    if not (0.0 < rho < 6.0):
        raise ValueError("rho must lie strictly between 0 and 6")

    features = np.column_stack([np.ones(6), CART_VELOCITIES])
    target = np.array([rho, rho * ux, rho * uy], dtype=float)
    lam = np.array([math.log(rho / (6.0 - rho)), 0.0, 0.0], dtype=float)

    for _ in range(max_iter):
        p = _sigmoid(features @ lam)
        residual = features.T @ p - target
        if np.linalg.norm(residual) < tol:
            return p
        w = p * (1.0 - p)
        jac = features.T @ (features * w[:, None])
        try:
            lam -= np.linalg.solve(jac, residual)
        except np.linalg.LinAlgError as exc:
            raise ValueError("maximum-entropy initialization became singular") from exc

    p = _sigmoid(features @ lam)
    err = np.linalg.norm(features.T @ p - target)
    if err > 1e-8:
        raise ValueError(
            f"requested (rho,u) outside/near feasibility boundary; residual={err:.3e}"
        )
    return p


def fhp_theory_g(rho: float) -> float:
    """FHP-I non-Galilean convection prefactor used as the flat positive-control target."""
    return (3.0 - rho) / (6.0 - rho)


def transition_fhp1() -> np.ndarray:
    """Classical FHP-I positive-control transition matrix over the 64 local states.

    The three zero-momentum head-on pair states scatter to either of the other two
    orientations with probability 1/2; the two alternating zero-momentum triplets swap.
    All other states are unchanged.
    """
    T = np.eye(64, dtype=float)

    # Three opposite-pair states: (0,3), (1,4), (2,5).
    pair_states = [9, 18, 36]
    for s in pair_states:
        T[s, :] = 0.0
        for t in pair_states:
            if t != s:
                T[s, t] = 0.5

    # Alternating three-particle zero-momentum states.
    T[21, :] = 0.0
    T[21, 42] = 1.0
    T[42, :] = 0.0
    T[42, 21] = 1.0
    return T


def transition_reversible_sector_permutation(orientation: int = 1) -> np.ndarray:
    """Bijective collision inside every degenerate (N,P) sector.

    This is a reversible cellular-automaton corner of REG+: each degenerate sector
    is permuted, never mixed coherently. It preserves N and P exactly but carries no
    nontrivial amplitude interference.
    """
    if orientation not in (-1, 1):
        raise ValueError("orientation must be +1 or -1")
    T = np.eye(64, dtype=float)
    for states in SECTORS.values():
        d = len(states)
        if d == 1:
            continue
        T[states, :] = 0.0
        if d == 2:
            T[states[0], states[1]] = 1.0
            T[states[1], states[0]] = 1.0
        elif d == 3:
            for i, s in enumerate(states):
                T[s, states[(i + orientation) % 3]] = 1.0
        else:
            raise AssertionError(f"unexpected sector dimension {d}")
    return T


def _unitary_from_hermitian(H: np.ndarray, theta: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(H)
    return (vecs * np.exp(-1j * theta * vals)) @ vecs.conj().T


def transition_reg_coherent(theta: float, phi: float) -> np.ndarray:
    r"""REG coherent sector-unitary collision, followed by local Born/dephasing read.

    In each local conservation sector H_{N,P}, define a unitary U_{N,P}.

    * 1-state sector: identity.
    * 2-state sector: exp(-i theta sigma_x). There is no closed internal route,
      so no gauge-invariant loop phase can live there.
    * 3-state sector: the three basis states form a triangle. The Hermitian
      collision generator is

            0       1       exp(-i phi)
        H = 1       0       1
            exp(i phi) 1    0

      so the directed product around the internal triangle carries W = exp(i phi).
      Equivalently phi is the Wilson-loop angle supplied by the carries/link
      substrate. The microscopic edge magnitudes are all one.

      U(phi) = exp(-i theta H(phi)).

    The returned stochastic transition matrix is |U|^2 after a local Born/dephasing
    read. This is the tractable intermediate construction: coherence acts inside
    the local collision, but phases are not retained across spatial carries.

    The only 3-state conservation sectors on the six-carry lattice are:
      N=2, P=0: the three head-on pair orientations
      N=4, P=0: their hole complements.

    Hence W affects exactly the local route-degenerate sectors where a genuine
    gauge-invariant cycle exists.
    """
    T = np.eye(64, dtype=float)
    for states in SECTORS.values():
        d = len(states)
        if d == 1:
            continue

        if d == 2:
            H = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
        elif d == 3:
            H = np.zeros((3, 3), dtype=complex)
            H[0, 1] = H[1, 0] = 1.0
            H[1, 2] = H[2, 1] = 1.0
            H[2, 0] = np.exp(1j * phi)
            H[0, 2] = np.exp(-1j * phi)
        else:
            raise AssertionError(f"unexpected sector dimension {d}")

        U = _unitary_from_hermitian(H, theta)
        p_out_given_in = np.abs(U) ** 2  # rows=out, cols=in
        T[np.ix_(states, states)] = p_out_given_in.T  # rows=input, cols=out
    return T


def transition_reg_dephased(theta: float, phase_bins: int = 48) -> np.ndarray:
    """Annealed phase-randomization control.

    Same collision graph, same theta, same |H_ij|. Only phi is randomized uniformly
    per collision step. Under the kinetic ensemble closure this equals averaging
    transition matrices over the randomized phase.

    This is the R2 deflation control: it tests whether a W!=1 transport shift is a
    coherent loop-phase effect rather than generic phase disorder.
    """
    if phase_bins < 4:
        raise ValueError("phase_bins must be >= 4")
    Ts = [
        transition_reg_coherent(theta, 2.0 * np.pi * j / phase_bins)
        for j in range(phase_bins)
    ]
    return np.mean(Ts, axis=0)


def validate_transition(T: np.ndarray, atol: float = 1e-10) -> Dict[str, object]:
    """Mechanical collision-invariant audit."""
    if T.shape != (64, 64):
        raise ValueError("transition must be 64x64")

    row_sum_err = float(np.max(np.abs(T.sum(axis=1) - 1.0)))
    min_entry = float(T.min())
    cross_sector_mass = 0.0

    sector_key_by_state = {}
    for key, ss in SECTORS.items():
        for s in ss:
            sector_key_by_state[s] = key

    for s in range(64):
        for t in np.flatnonzero(T[s] > atol):
            if sector_key_by_state[s] != sector_key_by_state[int(t)]:
                cross_sector_mass += float(T[s, t])

    result = {
        "row_sum_max_abs_error": row_sum_err,
        "minimum_entry": min_entry,
        "cross_sector_probability_mass": cross_sector_mass,
        "sector_count": len(SECTORS),
        "sector_dimension_histogram": {
            str(d): sum(1 for ss in SECTORS.values() if len(ss) == d)
            for d in sorted(set(map(len, SECTORS.values())))
        },
        "passes": bool(
            row_sum_err <= atol
            and min_entry >= -atol
            and cross_sector_mass <= atol
        ),
    }
    return result


def kinetic_collision(f: np.ndarray, T: np.ndarray) -> np.ndarray:
    """Local ensemble collision under a molecular-chaos closure.

    f[y,x,a] is the channel occupation probability. The 64 local microstate
    probabilities are reconstructed as a product Bernoulli measure; T acts on
    those microstates; the result is projected back to six channel marginals.

    This closure is intentionally explicit. It is a transport-coefficient
    instrument, not a claim that higher-order local correlations are absent.
    """
    ny, nx, q = f.shape
    if q != 6:
        raise ValueError("last dimension must be six carries")

    state_prob = np.ones((ny, nx, 64), dtype=float)
    for a in range(6):
        fa = f[..., a, None]
        state_prob *= np.where(BITS[None, None, :, a] == 1, fa, 1.0 - fa)

    expected_out_bits = T @ BITS  # input state -> expected outgoing channel occupancy
    return state_prob @ expected_out_bits


def stream(f: np.ndarray) -> np.ndarray:
    """Directional carries: each channel moves one axial-lattice edge."""
    out = np.empty_like(f)
    for a, (dx, dy) in enumerate(AXIAL_CARRIES):
        out[..., a] = np.roll(f[..., a], shift=(dy, dx), axis=(0, 1))
    return out


def macro_fields(f: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    rho = f.sum(axis=-1)
    jx = f @ CART_VELOCITIES[:, 0]
    jy = f @ CART_VELOCITIES[:, 1]
    safe = np.maximum(rho, 1e-14)
    return rho, jx / safe, jy / safe


def init_advection(
    n: int, rho: float, background_u: float, perturbation: float, mode: int
) -> np.ndarray:
    """u_x = U0, u_y = eps sin(k x)."""
    f = np.zeros((n, n, 6), dtype=float)
    for x in range(n):
        uy = perturbation * math.sin(2.0 * math.pi * mode * x / n)
        p = max_entropy_channel_probs(rho, background_u, uy)
        f[:, x, :] = p
    return f


def init_shear(n: int, rho: float, perturbation: float, mode: int) -> np.ndarray:
    """u_x = eps sin(k y), u_y = 0."""
    f = np.zeros((n, n, 6), dtype=float)
    for y in range(n):
        ux = perturbation * math.sin(2.0 * math.pi * mode * y / n)
        p = max_entropy_channel_probs(rho, ux, 0.0)
        f[y, :, :] = p
    return f


def _complex_mode_x(field: np.ndarray, mode: int) -> complex:
    profile = field.mean(axis=0)
    n = profile.size
    x = np.arange(n)
    return complex(2.0 * np.mean(profile * np.exp(-1j * 2.0 * np.pi * mode * x / n)))


def _complex_mode_y(field: np.ndarray, mode: int) -> complex:
    profile = field.mean(axis=1)
    n = profile.size
    y = np.arange(n)
    return complex(2.0 * np.mean(profile * np.exp(-1j * 2.0 * np.pi * mode * y / n)))


def _linear_fit(x: np.ndarray, y: np.ndarray) -> Tuple[float, float, float]:
    slope, intercept = np.polyfit(x, y, 1)
    pred = slope * x + intercept
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 if ss_tot == 0 else 1.0 - ss_res / ss_tot
    return float(slope), float(intercept), float(r2)


def estimate_g(
    T: np.ndarray,
    *,
    n: int,
    rho: float,
    background_u: float,
    perturbation: float,
    mode: int,
    cycles: int,
    fit_start: int,
    fit_end: int,
) -> Dict[str, object]:
    f = init_advection(n, rho, background_u, perturbation, mode)
    series = []

    for t in range(cycles + 1):
        _, _, uy = macro_fields(f)
        z = _complex_mode_x(uy, mode)
        series.append(
            {"cycle": t, "mode_re": z.real, "mode_im": z.imag, "amplitude": abs(z)}
        )
        if t < cycles:
            f = stream(kinetic_collision(f, T))

    z = np.array([complex(r["mode_re"], r["mode_im"]) for r in series])
    phase = np.unwrap(np.angle(z))
    amp = np.abs(z)
    tt = np.arange(cycles + 1, dtype=float)

    mask = (tt >= fit_start) & (tt <= fit_end) & (amp > 1e-12)
    if mask.sum() < 5:
        return {
            "status": "fixed_point_destroyed",
            "reason": "insufficient surviving mode amplitude in fit window",
            "series": series,
        }

    slope, _, r2 = _linear_fit(tt[mask], phase[mask])
    k = 2.0 * np.pi * mode / n
    c_mode = -slope / k
    g = c_mode / background_u

    for i, ph in enumerate(phase):
        series[i]["phase_unwrapped"] = float(ph)

    return {
        "status": "measured",
        "g": float(g),
        "mode_transport_speed": float(c_mode),
        "phase_fit_r2": r2,
        "k": float(k),
        "series": series,
    }


def estimate_nu(
    T: np.ndarray,
    *,
    n: int,
    rho: float,
    perturbation: float,
    mode: int,
    cycles: int,
    fit_start: int,
    fit_end: int,
) -> Dict[str, object]:
    f = init_shear(n, rho, perturbation, mode)
    series = []

    for t in range(cycles + 1):
        _, ux, _ = macro_fields(f)
        z = _complex_mode_y(ux, mode)
        series.append(
            {"cycle": t, "mode_re": z.real, "mode_im": z.imag, "amplitude": abs(z)}
        )
        if t < cycles:
            f = stream(kinetic_collision(f, T))

    amp = np.array([r["amplitude"] for r in series], dtype=float)
    tt = np.arange(cycles + 1, dtype=float)
    mask = (tt >= fit_start) & (tt <= fit_end) & (amp > 1e-12)

    if mask.sum() < 5:
        return {
            "status": "fixed_point_destroyed",
            "reason": "insufficient surviving shear mode in fit window",
            "series": series,
        }

    slope, _, r2 = _linear_fit(tt[mask], np.log(amp[mask]))
    k = 2.0 * np.pi * mode / n
    nu = -slope / (k * k)

    return {
        "status": "measured",
        "nu": float(nu),
        "log_amplitude_fit_r2": r2,
        "k": float(k),
        "series": series,
    }


def collision_from_config(cfg: Dict[str, object]) -> Tuple[np.ndarray, Dict[str, object]]:
    c = cfg["collision"]
    family = c["family"]

    if family == "fhp1":
        T = transition_fhp1()
        meta = {"family": family, "holonomy": "not_applicable_classical_positive_control"}
    elif family == "reversible_sector_permutation":
        orientation = int(c.get("orientation", 1))
        T = transition_reversible_sector_permutation(orientation)
        meta = {"family": family, "orientation": orientation, "holonomy": "flat"}
    elif family == "reg_coherent":
        theta = float(c["theta"])
        h = c.get("holonomy", {"mode": "fixed", "phi": 0.0})
        mode = h.get("mode", "fixed")

        if mode == "fixed":
            phi = float(h.get("phi", 0.0))
            T = transition_reg_coherent(theta, phi)
            meta = {"family": family, "theta": theta, "holonomy_mode": mode, "phi": phi}
        elif mode == "annealed_dephasing":
            bins = int(h.get("phase_bins", 48))
            T = transition_reg_dephased(theta, bins)
            meta = {
                "family": family,
                "theta": theta,
                "holonomy_mode": mode,
                "phase_bins": bins,
            }
        else:
            raise ValueError(f"unknown holonomy mode: {mode}")
    else:
        raise ValueError(f"unknown collision family: {family}")

    audit = validate_transition(T)
    if not audit["passes"]:
        raise RuntimeError(f"collision invariant audit failed: {audit}")
    meta["invariant_audit"] = audit
    return T, meta


def _requires_prereg(cfg: Dict[str, object]) -> bool:
    c = cfg["collision"]
    if c["family"] != "reg_coherent":
        return False
    h = c.get("holonomy", {"mode": "fixed", "phi": 0.0})
    if h.get("mode") == "annealed_dephasing":
        return True
    return abs(float(h.get("phi", 0.0))) > 1e-14


def enforce_prereg_gate(cfg: Dict[str, object]) -> None:
    """R2 guardrail: no inferential W!=1/dephasing transport run without a frozen ID."""
    if not _requires_prereg(cfg):
        return
    if cfg.get("instrumentation_smoke", False):
        return
    prereg = str(cfg.get("prereg_id", "")).strip()
    if not prereg:
        raise RuntimeError(
            "R2 PREREG GATE: W!=1/dephasing transport run refused. "
            "Set a frozen prereg_id after the prereg is committed, or set "
            "instrumentation_smoke=true only for non-inferential instrument checks."
        )


def run_config(cfg: Dict[str, object]) -> Dict[str, object]:
    enforce_prereg_gate(cfg)
    T, collision_meta = collision_from_config(cfg)

    experiment = cfg["experiment"]
    common = {
        "n": int(cfg["grid"]),
        "rho": float(cfg["rho"]),
        "cycles": int(cfg["cycles"]),
        "fit_start": int(cfg["fit_start"]),
        "fit_end": int(cfg["fit_end"]),
    }

    if experiment == "g":
        result = estimate_g(
            T,
            **common,
            background_u=float(cfg["background_u"]),
            perturbation=float(cfg["perturbation"]),
            mode=int(cfg["mode"]),
        )
        if cfg["collision"]["family"] == "fhp1":
            result["fhp_theory_g"] = fhp_theory_g(float(cfg["rho"]))
            if result["status"] == "measured":
                result["theory_error"] = result["g"] - result["fhp_theory_g"]

    elif experiment == "nu":
        result = estimate_nu(
            T,
            **common,
            perturbation=float(cfg["perturbation"]),
            mode=int(cfg["mode"]),
        )

    elif experiment == "nu_modes":
        results = {}
        for mode in cfg["modes"]:
            results[str(mode)] = estimate_nu(
                T,
                **common,
                perturbation=float(cfg["perturbation"]),
                mode=int(mode),
            )
        result = {"status": "measured", "modes": results}

    else:
        raise ValueError(f"unknown experiment: {experiment}")

    return {
        "schema": "regplus-hydro-result-v1",
        "code_version": VERSION,
        "evidence_status": (
            "fresh artifact from reference reconstruction; not retroactive evidence "
            "for prior chat testimony"
        ),
        "experiment": experiment,
        "collision": collision_meta,
        "config": cfg,
        "result": result,
    }


def transition_smoke(theta: float = 1.0) -> Dict[str, object]:
    """Non-inferential matrix-level smoke check for the holonomy instrument.

    Does NOT estimate Delta-nu or Delta-g.
    """
    s = 9  # one N=2, P=0 opposite-pair state
    pair_states = [9, 18, 36]
    rows = []
    for phi in (0.0, np.pi / 2.0, np.pi):
        T = transition_reg_coherent(theta, phi)
        rows.append(
            {
                "phi": float(phi),
                "W_re": float(np.cos(phi)),
                "W_im": float(np.sin(phi)),
                "transition_from_state_9": {
                    str(t): float(T[s, t]) for t in pair_states
                },
                "audit": validate_transition(T),
            }
        )
    return {
        "schema": "regplus-holonomy-instrument-smoke-v1",
        "theta": theta,
        "statement": (
            "matrix-level instrument check only; no transport coefficient is read "
            "before the W!=1 prereg"
        ),
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", nargs="?", help="JSON experiment config")
    parser.add_argument("--out", help="write result JSON here")
    parser.add_argument(
        "--transition-smoke",
        action="store_true",
        help="run only the non-inferential W matrix smoke check",
    )
    parser.add_argument("--theta", type=float, default=1.0)
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()

    if args.validate:
        report = {
            "fhp1": validate_transition(transition_fhp1()),
            "reversible": validate_transition(transition_reversible_sector_permutation()),
            "reg_flat": validate_transition(transition_reg_coherent(1.0, 0.0)),
            "reg_phi90": validate_transition(transition_reg_coherent(1.0, np.pi / 2.0)),
            "sector_count": len(SECTORS),
        }
        text = json.dumps(report, indent=2, sort_keys=True)
    elif args.transition_smoke:
        text = json.dumps(transition_smoke(args.theta), indent=2, sort_keys=True)
    else:
        if not args.config:
            parser.error("provide CONFIG, or use --validate / --transition-smoke")
        cfg_path = Path(args.config)
        cfg = json.loads(cfg_path.read_text())
        payload = run_config(cfg)
        payload["config_sha256"] = hashlib.sha256(
            json.dumps(cfg, sort_keys=True).encode()
        ).hexdigest()
        payload["code_sha256"] = sha256_file(Path(__file__))
        text = json.dumps(payload, indent=2, sort_keys=True)

    if args.out:
        Path(args.out).write_text(text + "\n")
    else:
        print(text)


if __name__ == "__main__":
    main()
