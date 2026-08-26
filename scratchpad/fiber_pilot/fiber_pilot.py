#!/usr/bin/env python3
"""Retrospective fiber-closure pilot on the OT_arHMM optical-tweezer trace.

PROVENANCE: authored and run in Eric's external session 2026-08-26; landed here
verbatim as the record the prereg cites. The dataset (docs/data/20220411-172711
Marker tether1-1.h5, public OT_arHMM) is NOT in this repository; reproduction is
step R0 of FIBER_ROBUSTNESS_PREREG.md and the numbers in
fiber_pilot_results.json are AS-REPORTED until R0 passes.
"""

from __future__ import annotations

import json
from pathlib import Path

import h5py
import matplotlib.pyplot as plt
import numpy as np
from sklearn.mixture import GaussianMixture


DATA = Path("docs/data/20220411-172711 Marker tether1-1.h5")
OUT_JSON = Path("fiber_pilot_results.json")
OUT_PNG = Path("fiber_pilot_results.png")
RAW_FS = 78_125.0
DOWNSAMPLE = 2
FS = RAW_FS / DOWNSAMPLE
TRAIN_FRAC = 0.60
FORCE_BINS = 8
VELOCITY_BINS = 5
HORIZONS_S = np.array([0.0001, 0.0005, 0.001, 0.005, 0.02, 0.1, 0.5])
ALPHA = 0.5
RNG = np.random.default_rng(20260826)


def quantile_edges(x: np.ndarray, n_bins: int) -> np.ndarray:
    edges = np.quantile(x, np.linspace(0, 1, n_bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    # Quantile ties are unlikely here, but monotonize defensively.
    for i in range(1, len(edges)):
        if edges[i] <= edges[i - 1]:
            edges[i] = np.nextafter(edges[i - 1], np.inf)
    return edges


def assign_bins(x: np.ndarray, coarse: np.ndarray, train_end: int, n_bins: int) -> np.ndarray:
    out = np.empty(len(x), dtype=np.int16)
    for state in (0, 1):
        train_values = x[:train_end][coarse[:train_end] == state]
        edges = quantile_edges(train_values, n_bins)
        mask = coarse == state
        out[mask] = np.digitize(x[mask], edges[1:-1], right=False)
    return out


def fit_prob(context: np.ndarray, target: np.ndarray, n_context: int) -> np.ndarray:
    counts = np.full((n_context, 2), ALPHA, dtype=float)
    np.add.at(counts, (context, target), 1.0)
    return counts / counts.sum(axis=1, keepdims=True)


def score(prob: np.ndarray, context: np.ndarray, target: np.ndarray) -> np.ndarray:
    return -np.log2(np.clip(prob[context, target], 1e-12, 1.0))


def block_ci(delta: np.ndarray, times: np.ndarray, block_s: float = 0.5, n_boot: int = 4000) -> tuple[float, float]:
    block = np.floor(times / block_s).astype(int)
    block_means = np.array([delta[block == b].mean() for b in np.unique(block)])
    choices = RNG.integers(0, len(block_means), size=(n_boot, len(block_means)))
    boot = block_means[choices].mean(axis=1)
    return tuple(np.quantile(boot, [0.025, 0.975]))


def shuffled_null(
    train_coarse: np.ndarray,
    train_fine: np.ndarray,
    test_coarse: np.ndarray,
    test_fine: np.ndarray,
    train_target: np.ndarray,
    test_target: np.ndarray,
    base_test_loss: np.ndarray,
    n_fine: int,
    n_perm: int = 100,
) -> np.ndarray:
    null = np.empty(n_perm)
    for p in range(n_perm):
        tr = train_fine.copy()
        te = test_fine.copy()
        for state in (0, 1):
            idx = np.flatnonzero(train_coarse == state)
            tr[idx] = RNG.permutation(tr[idx])
            idx = np.flatnonzero(test_coarse == state)
            te[idx] = RNG.permutation(te[idx])
        tr_context = train_coarse * n_fine + tr
        te_context = test_coarse * n_fine + te
        prob = fit_prob(tr_context, train_target, 2 * n_fine)
        null[p] = np.mean(base_test_loss - score(prob, te_context, test_target))
    return null


def main() -> None:
    with h5py.File(DATA, "r") as h5:
        f1 = h5["Force HF/Force 1x"][::DOWNSAMPLE]
        f2 = h5["Force HF/Force 2x"][::DOWNSAMPLE]
    force = (f2 - f1) / 2.0
    velocity = np.empty_like(force)
    velocity[0] = 0.0
    velocity[1:] = np.diff(force) * FS
    train_end = int(TRAIN_FRAC * len(force))

    sample = force[:train_end:5, None]
    # Match the dataset tutorial's preregistered physical initialization.  An
    # unconstrained mixture can instead split the dominant high-force peak and
    # miss the rare low-force state entirely.
    gmm = GaussianMixture(
        2,
        random_state=20260826,
        n_init=1,
        weights_init=np.array([0.1, 0.9]),
        means_init=np.array([[8.0], [10.0]]),
        precisions_init=np.array([[[4.0]], [[4.0]]]),
    ).fit(sample)
    order = np.argsort(gmm.means_.ravel())
    raw_label = gmm.predict(force[:, None])
    coarse = np.where(raw_label == order[0], 0, 1).astype(np.int8)

    force_bin = assign_bins(force, coarse, train_end, FORCE_BINS)
    vel_bin = assign_bins(velocity, coarse, train_end, VELOCITY_BINS)
    dynamic_bin = force_bin * VELOCITY_BINS + vel_bin

    results: list[dict[str, float | int | list[float]]] = []
    for horizon_s in HORIZONS_S:
        lag = max(1, int(round(horizon_s * FS)))
        train_idx = np.arange(1, train_end - lag)
        # Keep test origins approximately independent at the prediction horizon,
        # with a minimum spacing of 1 ms.
        stride = max(lag, int(round(0.001 * FS)))
        test_idx = np.arange(train_end, len(force) - lag, stride)
        y_train = coarse[train_idx + lag]
        y_test = coarse[test_idx + lag]

        base_prob = fit_prob(coarse[train_idx], y_train, 2)
        base_loss = score(base_prob, coarse[test_idx], y_test)

        force_context_train = coarse[train_idx] * FORCE_BINS + force_bin[train_idx]
        force_context_test = coarse[test_idx] * FORCE_BINS + force_bin[test_idx]
        force_prob = fit_prob(force_context_train, y_train, 2 * FORCE_BINS)
        force_loss = score(force_prob, force_context_test, y_test)

        n_dynamic = FORCE_BINS * VELOCITY_BINS
        dyn_context_train = coarse[train_idx] * n_dynamic + dynamic_bin[train_idx]
        dyn_context_test = coarse[test_idx] * n_dynamic + dynamic_bin[test_idx]
        dyn_prob = fit_prob(dyn_context_train, y_train, 2 * n_dynamic)
        dyn_loss = score(dyn_prob, dyn_context_test, y_test)

        force_gain = base_loss - force_loss
        dyn_gain = base_loss - dyn_loss
        times = (test_idx - train_end) / FS
        force_ci = block_ci(force_gain, times)
        dyn_ci = block_ci(dyn_gain, times)

        null = shuffled_null(
            coarse[train_idx],
            force_bin[train_idx],
            coarse[test_idx],
            force_bin[test_idx],
            y_train,
            y_test,
            base_loss,
            FORCE_BINS,
        )
        p_perm = (1 + np.sum(null >= force_gain.mean())) / (len(null) + 1)

        results.append(
            {
                "horizon_s": float(lag / FS),
                "lag_samples": int(lag),
                "n_test": int(len(test_idx)),
                "baseline_logloss_bits": float(base_loss.mean()),
                "force_gain_bits": float(force_gain.mean()),
                "force_gain_block95": [float(force_ci[0]), float(force_ci[1])],
                "dynamic_gain_bits": float(dyn_gain.mean()),
                "dynamic_gain_block95": [float(dyn_ci[0]), float(dyn_ci[1])],
                "force_permutation_p": float(p_perm),
                "coarse_switch_fraction": float(np.mean(coarse[test_idx] != y_test)),
            }
        )

    payload = {
        "dataset": str(DATA),
        "samples": int(len(force)),
        "duration_s": float(len(force) / FS),
        "sample_rate_hz": FS,
        "train_fraction": TRAIN_FRAC,
        "gmm_means_pN": [float(x) for x in gmm.means_.ravel()[order]],
        "gmm_weights": [float(x) for x in gmm.weights_[order]],
        "coarse_low_state_fraction": float(np.mean(coarse == 0)),
        "results": results,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n")

    h_ms = np.array([r["horizon_s"] for r in results]) * 1000
    fg = np.array([r["force_gain_bits"] for r in results])
    dg = np.array([r["dynamic_gain_bits"] for r in results])
    fig, ax = plt.subplots(figsize=(7, 4.3), layout="constrained")
    ax.semilogx(h_ms, fg, "o-", label="within-fiber force rank")
    ax.semilogx(h_ms, dg, "s-", label="force rank + backward velocity")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set(xlabel="Prediction horizon (ms)", ylabel="Held-out log-loss gain (bits/sample)")
    ax.set_title("OT_arHMM optical-tweezer fiber-closure pilot")
    ax.legend()
    fig.savefig(OUT_PNG, dpi=180)

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
