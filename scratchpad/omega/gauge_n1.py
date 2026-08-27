#!/usr/bin/env python3
"""Gauge for N1 (out-of-sample Dobrushin mixing bound) -- freeze evidence.

A ruler that cannot fire is decoration.  This gauge drives the EXACT pipeline of
oos_mixing.py (same threshold freezing, same even/odd chain split, same imported
defect_m, same chain-block bootstrap, same TRAIN-frozen bound) on synthetic data of
the SAME GEOMETRY as the real Basic-protocol traces: 174 chains x 3700 timesteps ->
87 TRAIN and 87 TEST chains.

Two modes.

`lag1`  -- the ORIGINAL lag-1 form (now REFUSED on the real data for vacuity).
    PASS-A  genuine 8-state Markov chain, doubly stochastic kernel, alpha ~ 0.65.
    PASS-B  the same at alpha ~ 0.50; a secondary probe, not a verdict input.  It is
            what exposed the estimator-bias boundary chased in falsefire_probe.py.
    FIRE    hidden two-valued regime, mean dwell 200, iid emissions given the regime:
            the pooled lag-1 kernel looks mixing (alpha_hat ~ 0.5) while the fiber
            keeps reporting the regime for hundreds of steps.

`restake` -- the CURRENT form: base lag L chosen by the alpha<0.9 rule, k in {1,2,4}.
    PASS-16 a MARKOV SURROGATE of the real data's own measured TRAIN lag-1 kernel
            (read from train_kernel.npy).  This is the control the re-staked form
            actually needs: falsefire_probe.log showed that a PASS side outside the
            data's mixing regime tests nothing, because once the right-hand side
            drops under the max-estimator's bias floor even a chain that is Markov by
            construction violates the bound.  The surrogate is Markov by construction
            AND sits in this data's regime.  The bound must HOLD on the held-out split.
    FIRE-16 the same surrogate with a hidden slow regime (mean dwell 500) in which
            every bit-flipping transition is redirected to itself, so the trajectory
            is trapped in its current well.  The regime is not in the observed state,
            the pooled one-step kernel is almost unchanged, but the current state is
            informative about the regime and the regime decides whether the bit can
            flip over the next 64 steps.  Must VIOLATE at some staked k.

    Both restake sides FORCE L=16, the base lag the rule selects on the real data.
    The rule selects L=8 on the surrogate (it mixes faster than the data at lag 8),
    so forcing is a declared deviation, printed by oos_mixing.run_split, and it is the
    right one: the point is to gauge the machinery at the base lag the real reading
    will use.

VERDICT (restake): TRANSFERS iff PASS-16 holds at every staked k on the held-out
split AND FIRE-16 violates at some staked k.  The adjudication is never touched to
make either side land.

The gauge synthesises all of its own series.  It reads ONE real quantity, the TRAIN
lag-1 kernel, from a file written by the blinded oos_mixing run -- so no real TEST
data is ever present in this process, which does set UNBLIND=1.
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

os.environ["UNBLIND"] = "1"          # synthetic series only -- see module docstring

import oos_mixing as om              # noqa: E402

NCHAIN, NSTEP = 174, 3700            # matched to Basic: zBasic.npy (174, 370000) at ::100
FIB_CENTRE = np.array([-3.0, -1.0, 1.0, 3.0])
FIB_SD = 0.15                        # quartile recovery is ~0.998 at this SD
BASE_L = 16                          # the base lag the rule selects on the real data


# ------------------------------------------------------------- emission layer

def emit(states: np.ndarray, rng):
    """Turn an 8-state integer array into (position, velocity) so that the real
    pipeline's bit = (x>0) and fiber = velocity quartile recover the state."""
    b = (states // 4).astype(np.int8)
    f = (states % 4).astype(np.int8)
    v = FIB_CENTRE[f] + FIB_SD * rng.standard_normal(states.shape)
    x = (2 * b - 1) * (0.5 + 0.5 * np.abs(rng.standard_normal(states.shape)))
    return x, v


# ------------------------------------------------------------------ samplers

def sim_markov(K, rng, n=NCHAIN, t=NSTEP):
    cum = K.cumsum(1)
    st = np.empty((n, t), np.int8)
    s = rng.integers(0, 8, n)
    for i in range(t):
        st[:, i] = s
        s = (cum[s] < rng.random(n)[:, None]).sum(1)
    return st


def sim_regime(Ks, p_sw, rng, n=NCHAIN, t=NSTEP):
    """Two kernels, hidden regime switching between them with per-step prob p_sw.
    The regime is NOT part of the observed state -- that is the planted memory."""
    cums = np.stack([k.cumsum(1) for k in Ks])
    st = np.empty((n, t), np.int8)
    s = rng.integers(0, 8, n)
    r = rng.integers(0, 2, n)
    for i in range(t):
        st[:, i] = s
        r = np.where(rng.random(n) < p_sw, 1 - r, r)
        s = (cums[r, s] < rng.random(n)[:, None]).sum(1)
    return st


# --------------------------------------------------------------- lag-1 mode

def doubly_stochastic(rng, n=8, it=300):
    """Sinkhorn a random positive matrix -> uniform stationary distribution, so the
    velocity-quartile marginal is uniform and the frozen thresholds land in the gaps."""
    R = rng.random((n, n)) ** 2 + 0.02
    for _ in range(it):
        R /= R.sum(1, keepdims=True)
        R /= R.sum(0, keepdims=True)
    R /= R.sum(1, keepdims=True)
    return R


def markov_kernel(rng, target_alpha):
    """K = (1-w)*uniform + w*R keeps double stochasticity and scales the Dobrushin
    coefficient linearly, so w picks alpha exactly."""
    R = doubly_stochastic(rng)
    w = target_alpha / om.dobrushin(R)
    assert 0 < w <= 1, f"target alpha {target_alpha} unreachable (dobrushin(R)={om.dobrushin(R)})"
    return (1 - w) / 8.0 + w * R


# -------------------------------------------------------------- restake mode

def trap_kernel(K):
    """The surrogate kernel with every bit-flipping transition redirected to itself:
    inside this regime the trajectory cannot leave its current well."""
    Kf = K.copy()
    bit = np.arange(8) // 4
    for i in range(8):
        for j in range(8):
            if bit[i] != bit[j] and Kf[i, j] > 0:
                Kf[i, i] += Kf[i, j]
                Kf[i, j] = 0.0
    rows = Kf.sum(1, keepdims=True)
    rows[rows == 0] = 1
    return Kf / rows


def load_train_kernel():
    p = os.path.join(HERE, "train_kernel.npy")
    if not os.path.exists(p):
        raise SystemExit(f"{p} missing -- run the blinded `python3 oos_mixing.py` first")
    return np.load(p)


# ------------------------------------------------------------------- harness

def run_side(states_true, tag, rng, seed, force_L=None, show_refused=True, ks=None):
    """Emit -> freeze TRAIN thresholds -> real pipeline -> held-out adjudication."""
    x, v = emit(states_true, rng)
    thr = om.freeze_thresholds(v[0::2])
    st = om.make_states(x, v, thr)
    recov = float((st == states_true).mean())
    print(f"\n{'='*78}\n{tag}: chains={x.shape[0]} timesteps={x.shape[1]}")
    print(f"{tag}: FROZEN velocity-quartile thresholds (TRAIN chains only): "
          f"{thr[0]:.6f}  {thr[1]:.6f}  {thr[2]:.6f}")
    print(f"{tag}: state recovery through the emission layer = {recov:.9f}")
    return om.run_split(st, seed=seed, tag=f"{tag} ", force_L=force_L,
                        show_refused=show_refused, ks=ks)


def summarise(sides, verdict_pass, verdict_fire, header):
    print("\n" + "=" * 78)
    print(header)
    print("=" * 78)
    for tag, alpha, tst in sides:
        print(f"{tag}: alpha_hat_train(base) = {alpha:.6f}")
        for r in tst:
            print(f"{tag}: k={r['k']} lag={r['lag']}  defect_test={r['defect_test']:.6f}  "
                  f"bound={r['bound_frozen']:.6f}  margin={r['margin']:+.6f}  "
                  f"{'VIOLATION' if r['violation'] else 'PASS'}")
    holds = all(not r["violation"] for r in verdict_pass)
    fires = any(r["violation"] for r in verdict_fire)
    best = max((r["margin"] for r in verdict_fire), default=float("-inf"))
    print()
    print(f"PASS side holds at every staked k on the held-out split: {holds}")
    print(f"FIRE side fires on the held-out split: {fires} (best margin {best:+.6f})")
    verdict = "TRANSFERS" if (holds and fires) else "STOP"
    gloss = ("holds on a chain that is Markov by construction in this data's own mixing "
             "regime, and DETECTS planted hidden-regime memory out of sample"
             if verdict == "TRANSFERS" else
             "FAILED its own gauge; the arm is unposable as built")
    print(f"\nGAUGE N1 ({header.split()[-1]}): {verdict} -- the instrument {gloss}")
    print("=" * 78)
    return verdict


def main_lag1():
    print("=" * 78)
    print("GAUGE N1 [lag-1 form, now REFUSED for vacuity] -- can the ruler FIRE?")
    print(f"geometry matched to Basic: {NCHAIN} chains x {NSTEP} timesteps")
    print("=" * 78)
    rng = np.random.default_rng(20260826)
    K_a = markov_kernel(np.random.default_rng(101), 0.65)
    print(f"\nPASS-A source: doubly stochastic 8-state kernel, "
          f"true Dobrushin alpha = {om.dobrushin(K_a):.6f}")
    a_a, _, tst_a, _ = run_side(sim_markov(K_a, rng), "PASS-A", rng, 4001,
                                force_L=1, show_refused=False, ks=(2, 4, 8))
    K_b = markov_kernel(np.random.default_rng(202), 0.50)
    print(f"\nPASS-B source (secondary probe): true Dobrushin alpha = "
          f"{om.dobrushin(K_b):.6f}")
    a_b, _, tst_b, _ = run_side(sim_markov(K_b, rng), "PASS-B", rng, 4002,
                                force_L=1, show_refused=False, ks=(2, 4, 8))
    print("\nFIRE source: hidden two-valued regime, p_switch=0.005 (mean dwell 200), "
          "phi=0.30 (fiber bias), delta=0.25 (bit bias)")
    a_f, _, tst_f, _ = run_side(sim_hidden_emission(rng), "FIRE", rng, 4003,
                                force_L=1, show_refused=False, ks=(2, 4, 8))
    summarise([("PASS-A", a_a, tst_a), ("PASS-B", a_b, tst_b), ("FIRE", a_f, tst_f)],
              tst_a, tst_f, "GAUGE N1 SUMMARY -- lag-1")


def sim_hidden_emission(rng, p_sw=0.005, phi=0.30, delta=0.25, n=NCHAIN, t=NSTEP):
    """lag-1 FIRE source: hidden regime with iid emissions given the regime."""
    hi = np.array([(0.5 - phi) / 2, (0.5 - phi) / 2, (0.5 + phi) / 2, (0.5 + phi) / 2])
    lo = hi[::-1].copy()
    cf = np.stack([lo.cumsum(), hi.cumsum()])
    st = np.empty((n, t), np.int8)
    r = rng.integers(0, 2, n)
    for i in range(t):
        if i:
            r = np.where(rng.random(n) < p_sw, 1 - r, r)
        f = (cf[r] < rng.random(n)[:, None]).sum(1)
        b = (rng.random(n) < np.where(r == 1, 0.5 + delta, 0.5 - delta)).astype(int)
        st[:, i] = b * 4 + f
    return st


def main_restake():
    print("\n\n" + "#" * 78)
    print("GAUGE N1 [RE-STAKED form] -- base lag L, k in {1,2,4}")
    print(f"geometry matched to Basic: {NCHAIN} chains x {NSTEP} timesteps; "
          f"base lag FORCED to L={BASE_L} (the rule's choice on the real data)")
    print("#" * 78)
    K = load_train_kernel()
    print(f"\nsurrogate source: the real data's measured TRAIN lag-1 kernel "
          f"(train_kernel.npy), Dobrushin alpha(1) = {om.dobrushin(K):.6f}")
    rng = np.random.default_rng(20260826)

    a_p, _, tst_p, warn_p = run_side(sim_markov(K, np.random.default_rng(31)),
                                     "PASS-16", rng, 5001, force_L=BASE_L,
                                     show_refused=False)

    Kf = trap_kernel(K)
    print(f"\nFIRE-16 source: the same surrogate kernel plus a hidden regime "
          f"(p_switch=0.002, mean dwell 500) whose kernel redirects every "
          f"bit-flipping transition to itself; alpha(1) of the trapped kernel = "
          f"{om.dobrushin(Kf):.6f}")
    a_f, _, tst_f, warn_f = run_side(sim_regime([K, Kf], 0.002, np.random.default_rng(32)),
                                     "FIRE-16", rng, 5002, force_L=BASE_L,
                                     show_refused=False)

    v = summarise([("PASS-16", a_p, tst_p), ("FIRE-16", a_f, tst_f)],
                  tst_p, tst_f, "GAUGE N1 SUMMARY -- restake")
    for w in warn_p + warn_f:
        print(f"GAUGE WARNING CARRIED: {w}")
    return v



def main_control():
    """MATCHED CONTROL for FIRE-16.

    FIRE-16's emission layer recovers only ~0.886 of the generated states, because the
    trapped regime skews the fiber marginal away from uniform and the frozen quartile
    thresholds then no longer sit in the gaps.  A skeptic can therefore ask whether the
    violation comes from the planted hidden regime or from the chart relabeling itself.

    This control settles it.  It rebuilds FIRE-16's OBSERVED state series (post-emission,
    post-relabel), fits the pooled TRAIN lag-1 kernel of THAT series, and simulates a pure
    Markov chain from it.  The surrogate therefore inherits everything the relabeling did
    to the one-step statistics and differs from FIRE-16 only in having no memory beyond
    one step.  If the surrogate HOLDS where FIRE-16 fires, the fire is the planted regime.
    """
    print("\n\n" + "#" * 78)
    print("GAUGE N1 [restake] MATCHED CONTROL -- Markov surrogate of FIRE-16's OWN")
    print("observed lag-1 kernel: same chart, same relabeling loss, no memory past 1 step")
    print("#" * 78)
    K = load_train_kernel()
    Kf = trap_kernel(K)
    true_states = sim_regime([K, Kf], 0.002, np.random.default_rng(32))
    x, v = emit(true_states, np.random.default_rng(20260826))
    thr = om.freeze_thresholds(v[0::2])
    obs = om.make_states(x, v, thr)
    print(f"CONTROL: reproduced FIRE-16 observed series, state recovery "
          f"{float((obs == true_states).mean()):.9f} (matches the FIRE-16 side)")
    K_obs = om.kernel_from_pairs(*om.flat_lag(obs[0::2], 1), om.S)
    print(f"CONTROL: pooled TRAIN lag-1 kernel of the OBSERVED FIRE-16 series, "
          f"alpha(1) = {om.dobrushin(K_obs):.6f}")
    st = sim_markov(K_obs, np.random.default_rng(33))
    print(f"\n{'='*78}\nCONTROL-16: chains={st.shape[0]} timesteps={st.shape[1]} "
          f"(integer states adjudicated directly -- the relabeling is already baked into "
          f"the fitted kernel, so a second emission round trip would double-count it)")
    a, _, tst, warns = om.run_split(st, seed=5003, tag="CONTROL-16 ", force_L=BASE_L,
                                    show_refused=False)
    print("\n" + "=" * 78)
    print("GAUGE N1 MATCHED-CONTROL SUMMARY")
    print("=" * 78)
    print(f"CONTROL-16: alpha_hat_train(16) = {a:.6f}")
    for r in tst:
        print(f"CONTROL-16: k={r['k']} lag={r['lag']}  defect_test={r['defect_test']:.6f}  "
              f"bound={r['bound_frozen']:.6f}  margin={r['margin']:+.6f}  "
              f"{'VIOLATION' if r['violation'] else 'PASS'}")
    holds = all(not r["violation"] for r in tst)
    print(f"\nCONTROL holds at every staked k: {holds}")
    print("CONTROL VERDICT: " + ("the FIRE-16 violation is attributable to the planted "
          "hidden regime, NOT to the chart relabeling" if holds else
          "*** the chart relabeling alone can violate the bound -- FIRE-16 is CONFOUNDED "
          "and the gauge does not transfer ***"))
    for w in warns:
        print(f"CONTROL WARNING CARRIED: {w}")
    print("=" * 78)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "restake"
    {"lag1": main_lag1, "restake": main_restake, "control": main_control}[mode]()
