#!/usr/bin/env python3
"""N1 -- OUT-OF-SAMPLE Dobrushin mixing-bound instrument, chained-erasure traces.

RE-STAKED FORM (current stake).  Base lag L is chosen on TRAIN by the rule

    L = the smallest diagnostic lag at which alpha_hat_train(L-step kernel) < 0.9

and the law staked out of sample is

    defect_test(k*L) <= alpha_hat_train(L)**k + 3*sigma_train(k*L),   k in {1, 2, 4}

with alpha_hat_train(L) the Dobrushin coefficient of the empirical L-step kernel on
TRAIN, and sigma_train(k*L) the chain-block bootstrap sigma of the TRAIN defect at
that lag.  Submultiplicativity of the Dobrushin coefficient is what licenses the
k-th power: the (k*L)-step kernel is the L-step kernel composed k times.

REFUSED FORM (kept in the output as a record, never staked, no held-out reading).
The original stake used L = 1 and k in {2,4,8}.  It was refused because on this data
alpha_hat_train(1) = 1.000000 exactly -- the lag-1 chart has a row pair with disjoint
support -- so the bound sits at or above 1.0, the ceiling of a total-variation
defect, and no data whatsoever could violate it.  That is a SECOND unposability,
distinct from registry defect D-BOUND-DOB (which is about alpha absorbing planted
memory in sample, and which the out-of-sample split does fix).

STATE   : 8 = bit x fiber.  bit = (position > 0); fiber = velocity quartile, the
          three thresholds frozen from the TRAIN split ONLY and printed below.
SPLIT   : chains (axis 0).  even index = TRAIN, odd index = TEST.  Never pooled.
sigma   : BLOCK bootstrap over CHAINS -- whole chains resampled with replacement,
          500 reps.  Transitions inside one chain are autocorrelated, so the
          transition-level bootstrap in mixing_bound.boot_sigma would understate
          the error; this is the one deliberate substitution (NOTE 1).

The TEST side is blinded: it runs only under UNBLIND=1.

NOTE 1 (deviations from mixing_bound.py, declared):
  * tv / kernel_from_pairs / dobrushin / defect_m are IMPORTED and unmodified.
  * boot_sigma and adjudicate are NOT used: boot_sigma resamples transitions iid
    (wrong dependence structure here) and adjudicate assumes one contiguous series
    with an in-sample lag-1 alpha.  Replaced by chain_boot / adjudicate_train /
    test_side, which are split-aware, base-lag-aware, and freeze the whole
    right-hand side on TRAIN.
NOTE 2 (posability reporting):
  A same-bit-pair count is not the only way this arm can be unfalsifiable.  If
  bound(k) >= 1.0 then no possible defect can exceed it, so the reading is VACUOUS.
  Every adjudicated k therefore carries an explicit NON-VACUITY line.
NOTE 3 (validity window, measured -- see falsefire_probe.log):
  defect_m is a MAX over 12 same-bit pairs, so it is positively biased.  When the
  right-hand side falls under that bias floor a chain that is Markov BY
  CONSTRUCTION violates the bound: measured false-fires at alpha_hat ~ 0.40 and
  0.30 for the lag-1 form at m=8.  A gauge whose PASS side does not sit in the same
  mixing regime as the data therefore tests nothing; gauge_n1.py's PASS side is a
  Markov surrogate of this data's own measured kernel for exactly that reason.
"""
from __future__ import annotations

import os
import sys
import time

import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ERASURE = os.path.abspath(os.path.join(HERE, "..", "erasure"))
sys.path.insert(0, HERE)

from mixing_bound import tv, kernel_from_pairs, dobrushin, defect_m  # noqa: E402

S = 8                      # 8 states = bit x fiber
NFIB = 4                   # velocity quartiles
VMAP = np.array([0, 0, 0, 0, 1, 1, 1, 1])   # state -> bit; defect pushes through this
NBOOT = 500
SEED = 20260826
MIN_COMPARABLE_PAIRS = 3   # fewer than this at any staked lag voids the arm

DIAG_LADDER = (1, 2, 4, 8, 16, 32, 64, 128)
ALPHA_RULE = 0.9           # base lag L = smallest diagnostic lag with alpha_hat < this
STAKED_KS = (1, 2, 4)      # the staked form: lags L, 2L, 4L
REFUSED_L, REFUSED_KS = 1, (2, 4, 8)        # the refused lag-1 form, kept as record
THIN_MARGIN = 0.05         # 1 - bound below this is flagged THIN


# ---------------------------------------------------------------- state chart

def freeze_thresholds(v_train: np.ndarray) -> np.ndarray:
    """The three velocity-quartile cuts.  TRAIN velocities only."""
    return np.quantile(v_train.ravel(), [0.25, 0.50, 0.75])


def make_states(x: np.ndarray, v: np.ndarray, thr: np.ndarray) -> np.ndarray:
    """state = bit*4 + fiber, with bit = (x > 0) and fiber = quartile(v) under thr."""
    bit = (x > 0).astype(np.int8)
    fib = np.digitize(v, thr).astype(np.int8)     # 0..3
    return (bit * NFIB + fib).astype(np.int8)


def flat_lag(states: np.ndarray, m: int):
    """(now, fut) at lag m, never crossing a chain boundary (rows are chains)."""
    return np.ascontiguousarray(states[:, :-m]).ravel(), \
           np.ascontiguousarray(states[:, m:]).ravel()


def alpha_hat(states: np.ndarray, L: int) -> float:
    """Dobrushin coefficient of the empirical L-step kernel."""
    return dobrushin(kernel_from_pairs(*flat_lag(states, L), S))


# ------------------------------------------------------------- error estimate

def chain_boot(states: np.ndarray, m: int, rng, n: int = NBOOT) -> np.ndarray:
    """Block bootstrap over CHAINS: resample whole rows with replacement."""
    nch = states.shape[0]
    out = np.empty(n)
    for k in range(n):
        r = rng.integers(0, nch, nch)
        nn, ff = flat_lag(states[r], m)
        out[k] = defect_m(nn, ff, S, VMAP)
    return out


# --------------------------------------------------------------- posability

def comparable_pairs(now: np.ndarray):
    """(n_ok, n_total, counts) for same-bit state pairs clearing defect_m's
    >=20-sample guard."""
    cnt = np.bincount(now, minlength=S)
    ok = cnt >= 20
    n_tot = n_ok = 0
    for i in range(S):
        for j in range(i + 1, S):
            if VMAP[i] != VMAP[j]:
                continue
            n_tot += 1
            if ok[i] and ok[j]:
                n_ok += 1
    return n_ok, n_tot, cnt


# ------------------------------------------------------------- base-lag rule

def diagnostic_ladder(states_tr: np.ndarray, label="TRAIN", ladder=DIAG_LADDER):
    """alpha_hat of the empirical m-step kernel across the ladder.  This is what the
    base-lag rule reads; it is a TRAIN-side quantity."""
    lad = {}
    print(f"[{label}] diagnostic ladder: Dobrushin coeff of the m-step empirical kernel")
    for m in ladder:
        if m >= states_tr.shape[1]:
            break
        lad[m] = alpha_hat(states_tr, m)
        print(f"[{label}]   alpha_hat({m}-step) = {lad[m]:.6f}")
    return lad


def select_base_lag(lad: dict, label="TRAIN"):
    """L = the smallest diagnostic lag at which alpha_hat_train < ALPHA_RULE."""
    for m in sorted(lad):
        if lad[m] < ALPHA_RULE:
            print(f"[{label}] BASE LAG RULE: smallest diagnostic lag with alpha_hat < "
                  f"{ALPHA_RULE} -> L = {m} (alpha_hat = {lad[m]:.6f})")
            return m
    print(f"[{label}] BASE LAG RULE: NO diagnostic lag reaches alpha_hat < {ALPHA_RULE}; "
          f"the arm has no posable base lag on this ladder")
    return None


# ---------------------------------------------------------------- adjudicate

def adjudicate_train(states_tr, L, ks, rng, label="TRAIN", stake_name="STAKED"):
    """alpha_hat(L), and the frozen bound at every staked k.  Prints the posability
    report.  Returns (alpha_L, rows, warnings)."""
    a = alpha_hat(states_tr, L)
    K1 = kernel_from_pairs(*flat_lag(states_tr, L), S)
    print(f"\n[{label}] {stake_name} FORM: base lag L={L}, k in {ks}")
    print(f"[{label}] empirical {L}-step kernel (rows = state, 8x8):")
    with np.printoptions(precision=4, suppress=True, linewidth=200):
        print(K1)
    print(f"[{label}] alpha_hat_train({L}-step) = {a:.6f}")
    worst = max(((tv(K1[i], K1[j]), i, j) for i in range(S) for j in range(S) if i < j))
    n_at_one = sum(1 for i in range(S) for j in range(S)
                   if i < j and tv(K1[i], K1[j]) >= 1.0 - 1e-12)
    print(f"[{label}] attained by state pair ({worst[1]},{worst[2]}) at TV={worst[0]:.6f}; "
          f"{n_at_one} of 28 row pairs sit at TV = 1 (disjoint {L}-step support)")

    warnings, rows = [], []
    for k in ks:
        lag = k * L
        t0 = time.time()
        now, fut = flat_lag(states_tr, lag)
        d = defect_m(now, fut, S, VMAP)
        boot = chain_boot(states_tr, lag, rng)
        sig = float(boot.std())
        bound = a ** k + 3 * sig
        n_ok, n_tot, cnt = comparable_pairs(now)
        rows.append({"k": k, "lag": lag, "defect": float(d), "alpha_pow": float(a ** k),
                     "sigma": sig, "bound": float(bound),
                     "boot_min": float(boot.min()), "boot_max": float(boot.max()),
                     "boot_p2.5": float(np.quantile(boot, 0.025)),
                     "boot_p50": float(np.quantile(boot, 0.5)),
                     "boot_p97.5": float(np.quantile(boot, 0.975)),
                     "pairs_ok": n_ok, "pairs_total": n_tot, "state_counts": cnt.tolist()})

        print(f"[{label}] k={k} lag={lag}: defect={d:.6f}  alpha_hat({L})^{k}={a**k:.6f}  "
              f"sigma_chainboot={sig:.6f}  bound={bound:.6f}  ({time.time()-t0:.1f}s)")
        print(f"[{label}] k={k} lag={lag}: POSABILITY(a) chain-bootstrap defect range "
              f"min={boot.min():.6f} p2.5={np.quantile(boot,0.025):.6f} "
              f"p50={np.quantile(boot,0.5):.6f} p97.5={np.quantile(boot,0.975):.6f} "
              f"max={boot.max():.6f}  spread={boot.max()-boot.min():.6f}")
        if boot.max() - boot.min() <= 0.0:
            warnings.append(f"{stake_name} k={k}: staked quantity constant under the chain bootstrap")
            print(f"[{label}] k={k} lag={lag}: POSABILITY WARNING -- defect is CONSTANT "
                  f"under the chain bootstrap; sigma is not an error estimate")
        print(f"[{label}] k={k} lag={lag}: POSABILITY(b) same-bit state pairs clearing the "
              f">=20-sample guard: {n_ok}/{n_tot} = {n_ok/n_tot:.3f}   "
              f"state counts={cnt.tolist()}")
        if n_ok < MIN_COMPARABLE_PAIRS:
            warnings.append(f"{stake_name} k={k}: only {n_ok} comparable same-bit pairs")
            print(f"[{label}] k={k} lag={lag}: *** POSABILITY WARNING *** only {n_ok} "
                  f"comparable same-bit pairs -- THIS VOIDS THE ARM AT FREEZE TIME")

        if k == 1:
            print(f"[{label}] k=1 lag={lag}: STRUCTURAL NOTE -- defect(L) <= alpha_hat(L) "
                  f"holds IDENTICALLY in sample (defect is a vmap-pushed TV over a subset "
                  f"of the state pairs the Dobrushin coefficient maximises over, and data "
                  f"processing cannot increase TV). Out of sample this rung can fire only "
                  f"through TRAIN/TEST kernel drift, so the extrapolation content of the "
                  f"law lives at k>=2. Observed here: defect={d:.6f} <= alpha_hat({L})="
                  f"{a:.6f} as required.")
        head = 1.0 - bound
        if bound >= 1.0:
            warnings.append(f"{stake_name} k={k}: bound={bound:.6f} >= 1.0, unfalsifiable")
            print(f"[{label}] k={k} lag={lag}: *** VACUITY WARNING *** bound={bound:.6f} "
                  f">= 1.0 = the maximum a total-variation defect can take. The stake "
                  f"CANNOT be violated at this k by any data whatsoever.")
        elif head < THIN_MARGIN:
            warnings.append(f"{stake_name} k={k}: non-vacuity margin only {head:.6f}")
            print(f"[{label}] k={k} lag={lag}: NON-VACUITY THIN -- bound={bound:.6f} < 1.0 "
                  f"but only by {head:.6f}; the arm is technically posable and practically "
                  f"nearly not")
        else:
            print(f"[{label}] k={k} lag={lag}: NON-VACUITY OK -- bound={bound:.6f} < 1.0 "
                  f"(ceiling) by margin {head:.6f}; a held-out defect of {bound:.6f} or "
                  f"more fires the kill")
    return a, rows, warnings


def test_side(states_te, rows_train, rng, label="TEST"):
    """The staked reading.  TRAIN-frozen thresholds, TRAIN-frozen bound."""
    out = []
    for r in rows_train:
        lag = r["lag"]
        now, fut = flat_lag(states_te, lag)
        d = defect_m(now, fut, S, VMAP)
        bound = r["bound"]                     # frozen on TRAIN; right-hand side untouched
        sig_te = float(chain_boot(states_te, lag, rng).std())   # diagnostic only
        n_ok, n_tot, _ = comparable_pairs(now)
        fired = d > bound
        out.append({"k": r["k"], "lag": lag, "defect_test": float(d),
                    "bound_frozen": float(bound), "margin": float(d - bound),
                    "sigma_test_diagnostic": sig_te, "pairs_ok": n_ok,
                    "pairs_total": n_tot, "violation": bool(fired)})
        print(f"[{label}] k={r['k']} lag={lag}: defect_test={d:.6f}  "
              f"bound(frozen train)={bound:.6f}  margin={d-bound:+.6f}  "
              f"pairs_ok={n_ok}/{n_tot}  sigma_test(diagnostic)={sig_te:.6f}  "
              f"{'VIOLATION' if fired else 'PASS'}")
    return out


# ------------------------------------------------------------------ pipeline

def run_split(states, seed=SEED, tag="", force_L=None, show_refused=True, ks=None):
    """Even chains TRAIN, odd chains TEST.  Shared by the real run and gauge_n1."""
    tr, te = states[0::2], states[1::2]
    print(f"{tag}SPLIT: TRAIN chains={tr.shape[0]} timesteps={tr.shape[1]}  |  "
          f"TEST chains={te.shape[0]} timesteps={te.shape[1]}")

    if show_refused:
        print(f"\n{'-'*78}\n{tag}REFUSED-FORM RECORD (lag-1 base, k in {REFUSED_KS}) -- "
              f"kept for the record, NOT staked, no held-out reading is taken from it.")
        adjudicate_train(tr, REFUSED_L, REFUSED_KS, np.random.default_rng(seed),
                         label=f"{tag}TRAIN", stake_name="REFUSED")

    print(f"\n{'-'*78}")
    lad = diagnostic_ladder(tr, label=f"{tag}TRAIN")
    L_rule = select_base_lag(lad, label=f"{tag}TRAIN")
    L = L_rule if force_L is None else force_L
    if force_L is not None and force_L != L_rule:
        print(f"[{tag}TRAIN] BASE LAG FORCED to L={force_L} (rule would have chosen "
              f"{L_rule}) -- declared deviation, gauge only")
    if L is None:
        print(f"[{tag}TRAIN] no posable base lag; nothing staked")
        return None, [], None, ["no base lag reaches the alpha rule"]

    a, rows, warns = adjudicate_train(tr, L, ks or STAKED_KS,
                                      np.random.default_rng(seed + 7),
                                      label=f"{tag}TRAIN", stake_name="STAKED")
    if os.environ.get("UNBLIND") == "1":
        print(f"\nUNBLIND=1 -- running the staked TEST side (base lag L={L})")
        tst = test_side(te, rows, np.random.default_rng(seed + 1), label=f"{tag}TEST")
    else:
        print("\nTEST SIDE BLINDED (set UNBLIND=1 to run the staked held-out reading)")
        tst = None
    return a, rows, tst, warns


def load_basic():
    """Basic protocol only.  174 chains x 370000 raw -> 3700 after the loader's ::100."""
    cwd = os.getcwd()
    os.chdir(ERASURE)                # chained_run's ROOT and fiber_pilot import are relative
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("chained_run", "chained_run.py")
        cr = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cr)
        proto = os.environ.get("PROTO", "Basic")
        x, v = cr.load_pos(cr.PROTOS[proto])
    finally:
        os.chdir(cwd)
    return x, v


def main():
    print("=" * 78)
    print(f"N1 -- OUT-OF-SAMPLE Dobrushin mixing bound, chained erasure, {os.environ.get('PROTO','Basic')} protocol")
    print("RE-STAKED: defect_test(k*L) <= alpha_hat_train(L)^k + 3*sigma_train(k*L), "
          f"k in {STAKED_KS}")
    print(f"           L = smallest diagnostic lag with alpha_hat_train < {ALPHA_RULE}")
    print("=" * 78)
    x, v = load_basic()
    print(f"DATA: Basic, position {x.shape} {x.dtype} ({x.nbytes/1e6:.1f} MB), "
          f"velocity {v.shape}")
    thr = freeze_thresholds(v[0::2])        # TRAIN chains only
    print(f"FROZEN velocity-quartile thresholds (TRAIN chains only, "
          f"n={v[0::2].size} samples): {thr[0]:.6f}  {thr[1]:.6f}  {thr[2]:.6f}")
    print(f"TRAIN bit=1 fraction (position>0): {(x[0::2] > 0).mean():.6f}")
    states = make_states(x, v, thr)
    # TRAIN-side artifact for the gauge's Markov surrogate.  Only the TRAIN split is
    # touched; the gauge reads this file so that no real TEST data ever enters a
    # process that has UNBLIND set.
    K_tr = kernel_from_pairs(*flat_lag(states[0::2], 1), S)
    np.save(os.path.join(HERE, "train_kernel.npy"), K_tr)
    print(f"WROTE {os.path.join(HERE, 'train_kernel.npy')} "
          f"(TRAIN lag-1 kernel, for the gauge's Markov surrogate)")
    run_split(states)
    print("=" * 78)


if __name__ == "__main__":
    main()
