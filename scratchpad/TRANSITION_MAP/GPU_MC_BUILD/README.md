# GPU_MC_BUILD — independent annihilating coherent MC (GPU)

Independent reimplementation of the frozen annihilating coherent Monte Carlo estimator,
written from `REG_HYDRO_COHERENT_ANNIHILATING_MC_PREREG.md` alone.

**Read `LICENSE_GPU.md` first.** Verdict: `BLOCKED-MISSING-BENCHMARK-DATA`.

## Files

| file | what it is |
|---|---|
| `regmodel.py` | frozen microscopic constants re-derived: sectors, unitaries, carries |
| `mc_tables.py` | the (64,3) collision lookup tables, stream map, initial state, branch weights |
| `annihil_mc.py` | the estimator; one code path runs on numpy (CPU) or cupy (GPU) |
| `seeds_frozen.py` | the frozen deterministic seed formula (+5e10 annihilating offset) |
| `exact_ref_sup.py` | exact dense state-vector oracle (supervisor build) |
| `exact_ref_worker.py` | exact oracle, independent API-worker draft, bugs repaired here |
| `test_micro.py` | 12 hand-computable micro-case tests |
| `verify_exact.py` | MC → exact convergence and SE calibration |
| `cascade_own_configs.py` | W-cascade in prereg reporting form, on OWN configurations |
| `SHA256SUMS.txt` | per-file digests for the code-hash guard |
| `model_spec.txt`, `task_*.txt`, `sys_coder.txt` | the specs handed to the API workers |
| `draft_*.py`, `w_*.log` | raw API-worker drafts and their usage logs |

## Running

```
python3 test_micro.py                 # 12/12 expected
python3 exact_ref_sup.py              # reproduces the published L=11 bridge table
python3 verify_exact.py cpu           # MC vs exact, small lattices
python3 cascade_own_configs.py        # GPU W-cascade on own configurations
```

`annihil_mc.set_backend('gpu')` switches to CuPy. RNG streams differ between backends, so
CPU and GPU agree statistically, not bit-for-bit.

## Key numbers

- L=11 N=2 bridge reproduced at all 12 phases to 6 decimals — every published digit.
- Two independent exact implementations agree to 2.2e-16 on 25 many-body configurations.
- 12/12 micro-case tests pass; the cross estimator is unbiased for the raw probabilities.
- W=1e6 at L=7: 0.443 GiB of 15.57 GiB, 0.85 s/replica, ~55 s per configuration.
- W=1e6 on 16 own L=7 N=20 configurations: median |M_MC − M_exact| = 0.00053,
  max 0.00219, median SE 0.00077, no out-of-range estimates, 906 s for the cell.
  That clears every frozen benchmark gate by 13–29×, on own configurations only.

## The block, in one line

The frozen L=7 LOW/MID configuration lists and their 32 exact per-configuration M values are
not in the repository and never have been, so the official cascade cannot run. The three
things needed to clear it are listed at the end of `LICENSE_GPU.md`.

## Not done

No held-out target cell has been executed, and no target outcome inspected. That requires the
orchestrator's explicit go after a license, and the license is blocked.
