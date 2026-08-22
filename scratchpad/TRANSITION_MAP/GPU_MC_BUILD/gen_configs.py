#!/usr/bin/env python3
"""Generate the six spectator configuration lists under the interpretation DECLARED in
EXECUTION_AMENDMENT_E2.md section D1. Run once; the outputs are frozen artifacts."""
from __future__ import annotations
import hashlib, json
import numpy as np

CELLS = [
    # name,        L, N,  seed,        role
    ("L7_LOW_N20",  7, 20, 2026082271, "benchmark"),
    ("L7_MID_N25",  7, 25, 2026082272, "benchmark"),
    ("L7_HIGH_N31", 7, 31, 2026082373, "held-out"),
    ("L9_LOW_N32",  9, 32, 2026082391, "held-out"),
    ("L9_MID_N42",  9, 42, 2026082392, "held-out"),
    ("L9_HIGH_N52", 9, 52, 2026082393, "held-out"),
]
NCFG = 16


def candidates(L):
    """D1.2: every mode whose site index is not 0, ascending mode index."""
    return np.array([m for m in range(6 * L * L) if m // 6 != 0], dtype=np.int64)


def generate(L, N, seed):
    """D1.3: one Generator per cell, drawn from sequentially. D1.4: choice(replace=False)."""
    rng = np.random.default_rng(seed)           # PCG64 is numpy's default bit generator
    cand = candidates(L)
    out, seen, dupes = [], set(), 0
    while len(out) < NCFG:
        draw = rng.choice(cand, size=N - 2, replace=False)
        key = tuple(sorted(int(v) for v in draw))
        if key in seen:                          # D1.5
            dupes += 1
            continue
        seen.add(key); out.append(list(key))
    return out, dupes


manifest = {}
for name, L, N, seed, role in CELLS:
    cfgs, dupes = generate(L, N, seed)
    assert all(len(c) == N - 2 for c in cfgs)
    assert all(len(set(c)) == N - 2 for c in cfgs)
    assert all(all(m // 6 != 0 for m in c) for c in cfgs)
    blob = dict(cell=name, L=L, N=N, seed=seed, role=role, n_configs=NCFG,
                bit_generator="PCG64", duplicates_discarded=dupes,
                n_candidate_modes=int(len(candidates(L))), configs=cfgs)
    txt = json.dumps(blob, indent=1, sort_keys=True)
    path = f"configs/{name}.json"
    open(path, "w").write(txt)
    h = hashlib.sha256(txt.encode()).hexdigest()
    manifest[name] = dict(sha256=h, L=L, N=N, seed=seed, role=role,
                          duplicates_discarded=dupes)
    print(f"{name:12s} L={L} N={N} seed={seed} role={role:9s} dupes={dupes} sha256={h[:16]}…")
    print(f"             config[0] first 8 modes: {cfgs[0][:8]}")

open("configs/MANIFEST.json", "w").write(json.dumps(manifest, indent=1, sort_keys=True))
print("\nfrozen to configs/ ; manifest sha256 =",
      hashlib.sha256(open('configs/MANIFEST.json','rb').read()).hexdigest())
