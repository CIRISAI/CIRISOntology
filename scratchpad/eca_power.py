"""eca_power.py — how big a spike would this pipeline have caught?

A null result is worth only as much as its detection floor. This injects a KNOWN biphasic
order-3 component into the REAL ECA triples, at the real sample sizes, on the real P_n grid,
and runs the identical measurement, null and pre-registered spike statistic over it. The
output is the smallest peak amplitude recovered at z_spike > 5 -- i.e. the size of spike the
main sweep could not have missed.

Injection: with probability w(P_n), slot 3 of the triple is replaced by slot1 XOR slot2.
That turns a fraction w of the ensemble into exact three-coin parity and leaves the rest as
the automaton produced it. The profile w(P_n) is biphasic by construction, peaked at
P_n = 2^-9, so the injected curve has the exact shape H1 asks about.
"""
import sys, os, json
import numpy as np
import cupy as cp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eca_spike as E

R = 1 << 20
STEPS = 800
SEEDS = [0, 1, 2]
RULE = 110
READING = 'SPATIAL'          # a primary reading; shape index 0
PEAK_K = 9                   # inject the maximum at P_n = 2^-9


def profile(amp, k):
    """Biphasic weight: a Gaussian in log2(P_n) centred on PEAK_K, zero at P_n = 0."""
    if k is None:
        return 0.0
    return amp * float(np.exp(-0.5 * ((k - PEAK_K) / 1.5) ** 2))


def run(amp, rng_np):
    rows = []
    for gi, (p_n, k) in enumerate(zip(E.P_GRID, E.K_GRID)):
        w = profile(amp, k)
        sh, nu, nsd = [], [], []
        for s in SEEDS:
            c, _ = E.run_eca(RULE, R, STEPS, k, seed=1000 * s + 7 * RULE + gi)
            tags, idx = E.reading_index(c)
            t = tags.index('SPATIAL:1-3-13')
            b = idx[t]
            b0 = (b >> 2) & 1; b1 = (b >> 1) & 1; b2 = b & 1
            if w > 0:
                m = cp.asarray(rng_np.random(R) < w)
                b2 = cp.where(m, b0 ^ b1, b2)
            p = E.hist_triples((4 * b0 + 2 * b1 + b2)[None, :].astype(cp.uint8), R)
            share, q, _, _ = E.shareK3_batch(p)
            fl = E.surrogate_and_shuffle(q, R, 60, 0, rng_np)
            sh.append(float(cp.asnumpy(share)[0]))
            nu.append(float(fl['null'][0][0])); nsd.append(float(fl['null'][1][0]))
        exc = np.array(sh) - np.array(nu)
        rows.append(dict(P_n=p_n, w=w, excess=float(exc.mean()),
                         sem=float(exc.std(ddof=1) / np.sqrt(len(SEEDS))),
                         null_sd=float(np.mean(nsd))))
    ex = np.array([r['excess'] for r in rows])
    sem = np.array([r['sem'] for r in rows])
    j = int(np.argmax(ex[1:])) + 1
    delta = ex[j] - ex[0]
    z = delta / np.sqrt(sem[j] ** 2 + sem[0] ** 2) if (sem[j] + sem[0]) > 0 else np.nan
    return dict(amp=amp, delta=float(delta), z_spike=float(z), P_peak=rows[j]['P_n'],
                peak_excess=float(ex[j]), det_excess=float(ex[0]),
                found_at_peak_k=bool(rows[j]['P_n'] == 2.0 ** -PEAK_K), rows=rows)


def main():
    rng_np = np.random.default_rng(31415)
    out = []
    print(f"injection power control: rule {RULE}, {READING}:1-3-13, R={R}, "
          f"{len(SEEDS)} seeds, peak injected at P_n = 2^-{PEAK_K} = {2.0**-PEAK_K:.3e}")
    print(f"{'inject w':>10} {'Delta(nats)':>13} {'z_spike':>10} {'P_peak':>10} "
          f"{'peak at right P_n':>18} {'detected':>9}")
    for amp in (0.0, 1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2):
        r = run(amp, rng_np)
        out.append(r)
        print(f"{amp:10.1e} {r['delta']:+13.3e} {r['z_spike']:10.1f} {r['P_peak']:10.2e} "
              f"{str(r['found_at_peak_k']):>18} "
              f"{'YES' if (r['z_spike'] > 5 and r['found_at_peak_k']) else 'no':>9}",
              flush=True)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'eca_power.json'), 'w') as f:
        json.dump(out, f, default=float)
    det = [r for r in out if r['amp'] > 0 and r['z_spike'] > 5 and r['found_at_peak_k']]
    if det:
        m = min(det, key=lambda r: r['amp'])
        print(f"\nSMALLEST SPIKE RECOVERED: injection weight {m['amp']:.1e} -> "
              f"Delta = {m['delta']:.3e} nats at z_spike = {m['z_spike']:.1f}. "
              f"A biphasic peak of this size or larger could not have been missed.")
    print(f"amp=0 control (no injection): z_spike = {out[0]['z_spike']:.2f}, "
          f"Delta = {out[0]['delta']:+.3e} nats")


if __name__ == '__main__':
    main()
