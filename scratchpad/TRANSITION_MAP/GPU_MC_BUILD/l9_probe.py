#!/usr/bin/env python3
"""Forward feasibility probe: cost of one replica at the larger held-out sizes.

Informational only -- no held-out target cell is executed and no witness is read. This times
and measures a single replica propagation at L=9 and L=11 to size the orchestrator's options.
"""
import time, numpy as np, cupy
import annihil_mc as A, mc_tables as T, seeds_frozen as S
A.set_backend('gpu'); mp = cupy.get_default_memory_pool()
for L, N in ((7, 20), (9, 32), (9, 52), (11, 48)):
    cand = [m for m in range(6*L*L) if m//6 != 0]
    sp = sorted(np.random.default_rng(555+L*100+N).choice(cand, size=N-2, replace=False).tolist())
    tab = A.Tables(L); init = T.initial_site_states(L, sp)
    for W in (1_000_000,):
        mp.free_all_blocks()
        t = time.time()
        try:
            (_, amps, _), nu = A.run_replica(L, init, None, W, S.seed(L, N, 0, 0, 0), tab)
            cupy.cuda.Stream.null.synchronize()
            dt = time.time()-t
            print(f"L={L:>2d} N={N:>2d} W={W:,d}: {dt:6.2f} s/replica  "
                  f"peak={mp.total_bytes()/2**30:5.2f} GiB  unique_cfgs={nu:,d}  "
                  f"-> 16-config cell approx {dt*64*16/60:.0f} min", flush=True)
        except cupy.cuda.memory.OutOfMemoryError:
            print(f"L={L} N={N} W={W:,d}: OUT OF MEMORY", flush=True)
