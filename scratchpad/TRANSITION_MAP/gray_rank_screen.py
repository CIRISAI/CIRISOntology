"""Preregistered gray-rank screen for dynamically disordered polariton models.

See GRAY_RANK_PREREG.md. Uses analytic/circulant spectra where possible so the
screen measures the object of interest rather than eigensolver scaling.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
NS = [64, 128, 256, 512, 1024]
REL_RANK_TOL = 1e-10


def metrics(vals: np.ndarray, n: int) -> dict:
    vals = np.asarray(vals, dtype=float)
    vals[np.abs(vals) < 1e-14] = 0.0
    vals = np.clip(vals, 0.0, None)
    vals = np.sort(vals)[::-1]
    vmax = float(vals[0]) if len(vals) else 0.0
    rank = int(np.sum(vals > REL_RANK_TOL * vmax)) if vmax > 0 else 0
    total = float(vals.sum())

    def rfrac(frac: float) -> int:
        if total <= 0:
            return 0
        return int(np.searchsorted(np.cumsum(vals), frac * total, side="left") + 1)

    r_eff = float(total * total / np.dot(vals, vals)) if np.dot(vals, vals) > 0 else 0.0
    r99 = rfrac(0.99)
    return {
        "rank": rank,
        "r90": rfrac(0.90),
        "r99": r99,
        "r999": rfrac(0.999),
        "r_eff": r_eff,
        "r99_fraction_dark": float(r99 / (n - 1)) if n > 1 else 0.0,
        "r_eff_fraction_dark": float(r_eff / (n - 1)) if n > 1 else 0.0,
        "trace": total,
        "lambda_max": vmax,
        "aux_proxy": {
            str(L): {
                "r99_modes": math.comb(r99 + L, L),
                "independent_modes": math.comb((n - 1) + L, L),
            }
            for L in [2, 3, 4]
        },
    }


def periodic_exponential_spectrum(n: int, ell: float) -> np.ndarray:
    j = np.arange(n)
    d = np.minimum(j, n - j)
    row = np.exp(-d / ell)
    lam = np.real(np.fft.fft(row))
    # Q projects out the uniform k=0 eigenvector; all other Fourier modes survive.
    lam[0] = 0.0
    return lam


def lowrank_feature_spectrum(n: int, r: int) -> tuple[np.ndarray, float]:
    # Deterministic orthonormal real Fourier features, first feature common mode.
    x = np.arange(n)
    cols = [np.ones(n) / math.sqrt(n)]
    k = 1
    while len(cols) < r:
        c = np.cos(2 * math.pi * k * x / n)
        c = c / np.linalg.norm(c)
        cols.append(c)
        if len(cols) < r:
            s = np.sin(2 * math.pi * k * x / n)
            if np.linalg.norm(s) > 1e-12:
                s = s / np.linalg.norm(s)
                cols.append(s)
        k += 1
    F = np.column_stack(cols[:r])
    b = np.ones(n) / math.sqrt(n)
    QF = F - np.outer(b, b @ F)
    s = np.linalg.svd(QF, compute_uv=False)
    vals = s * s
    # Frobenius cross-check against explicit Q C Q at small N only.
    err = 0.0
    if n <= 128:
        Q = np.eye(n) - np.outer(b, b)
        C = F @ F.T
        A = Q @ C @ Q
        ev = np.linalg.eigvalsh(A)
        ev = np.sort(np.clip(ev, 0.0, None))[::-1]
        vv = np.sort(np.pad(vals, (0, n - len(vals))))[::-1]
        err = float(np.max(np.abs(ev - vv)))
    return vals, err


def run() -> dict:
    out = {"prereg": "GRAY_RANK_PREREG.md", "sizes": NS, "cells": {}, "gates": {}}
    independent_rank_ok = True
    independent_equal_ok = True
    common_ok = True
    lowrank_ok = True
    lowrank_crosscheck = 0.0

    for n in NS:
        cells = {}

        # Independent C=I -> QIQ=Q: N-1 unit eigenvalues and one zero.
        ind_vals = np.r_[np.ones(n - 1), 0.0]
        cells["independent"] = metrics(ind_vals, n)
        independent_rank_ok &= cells["independent"]["rank"] == n - 1
        independent_equal_ok &= abs(cells["independent"]["lambda_max"] - 1.0) < 1e-12

        # Common C=11^T -> QCQ=0 exactly.
        cells["common"] = metrics(np.zeros(n), n)
        common_ok &= cells["common"]["rank"] == 0 and cells["common"]["trace"] == 0.0

        for r in [4, 16]:
            vals, err = lowrank_feature_spectrum(n, r)
            m = metrics(vals, n)
            cells[f"lowrank_r{r}"] = m
            lowrank_ok &= m["rank"] <= r - 1
            lowrank_crosscheck = max(lowrank_crosscheck, err)

        for label, ell in [
            ("exp_ell2", 2.0),
            ("exp_ell8", 8.0),
            ("exp_ellN16", n / 16.0),
            ("exp_ellN4", n / 4.0),
        ]:
            cells[label] = metrics(periodic_exponential_spectrum(n, ell), n)

        out["cells"][str(n)] = cells

    out["gates"] = {
        "G1_independent_rank": bool(independent_rank_ok),
        "G1_independent_unit_spectrum": bool(independent_equal_ok),
        "G2_common_rank_zero": bool(common_ok),
        "G3_lowrank_bound": bool(lowrank_ok),
        "lowrank_smallN_spectrum_crosscheck_max_abs": lowrank_crosscheck,
    }

    # Frozen stakes.
    out["stakes"] = {}
    out["stakes"]["S1_independent_kills_rank_compression"] = all(
        out["cells"][str(n)]["independent"]["r99_fraction_dark"] >= 0.95 for n in NS
    )

    def finite_len_extensive(label: str) -> dict:
        vals = [out["cells"][str(n)][label]["r99"] for n in NS]
        fracs = [out["cells"][str(n)][label]["r99_fraction_dark"] for n in NS]
        # Operationalized prereg language: last/third r99 grows at least 3x while N grows 4x,
        # and the terminal fraction remains >= half the N=256 fraction.
        return {
            "r99": vals,
            "fractions": fracs,
            "extensive_operational": bool(vals[-1] >= 3 * vals[-3] and fracs[-1] >= 0.5 * fracs[-3]),
        }

    out["stakes"]["S2_ell2"] = finite_len_extensive("exp_ell2")
    out["stakes"]["S2_ell8"] = finite_len_extensive("exp_ell8")

    for label in ["exp_ellN16", "exp_ellN4"]:
        r256 = out["cells"]["256"][label]["r99"]
        r1024 = out["cells"]["1024"][label]["r99"]
        out["stakes"][f"S3_{label}"] = {
            "r99_N256": r256,
            "r99_N1024": r1024,
            "opportunity": bool(r1024 <= 64 and r1024 <= 2 * r256),
        }

    return out


def main() -> None:
    r = run()
    (HERE / "gray_rank_results.json").write_text(json.dumps(r, indent=2) + "\n")
    print("GATES", json.dumps(r["gates"], indent=2))
    for n in NS:
        print("N", n)
        for name, m in r["cells"][str(n)].items():
            print(name, "rank", m["rank"], "r99", m["r99"], "r_eff", f"{m['r_eff']:.3f}", "r99frac", f"{m['r99_fraction_dark']:.3f}")
    print("STAKES", json.dumps(r["stakes"], indent=2))


if __name__ == "__main__":
    main()
