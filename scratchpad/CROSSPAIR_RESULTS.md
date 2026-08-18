# CROSSPAIR RESULTS — S1 NULL at every separation; the quantum sector's first wild-style bound

Run 2026-08-18 on `ibm_kingston` (156 qubits), per `CROSSPAIR_PREREG.md` + `AMENDMENT_1`,
both committed before submission. **Cost: 25 QPU-seconds of the 106 remaining** (screen 3 s,
main 22 s — 81 s left in the window). Two jobs, no retries needed.

## The verdict

**S1 — the QM null — SURVIVES at every separation and in both bases.** Connected cross-pair
correlator excess (Bell over parity-matched control, same qubits, same batch):

| separation | pooled excess | σ | z | **3σ bound** |
|---|---|---|---|---|
| 2 | +0.0022 | 0.0127 | +0.17 | **\|E\| < 0.040** |
| 4 | −0.0016 | 0.0122 | −0.13 | **\|E\| < 0.038** |
| 8 | −0.0012 | 0.0117 | −0.10 | **\|E\| < 0.036** |
| 16 | +0.0037 | 0.0121 | +0.30 | **\|E\| < 0.040** |

Largest single-cell z anywhere: +0.33. **No excess exists to fit a shape to; S2 (the
separation-ratio-squared discriminant) is NOT ENTERED**, exactly as the prereg's ladder
requires — a shape test on a null would be reading pattern into noise.

**K1 — the instrument kill — does not fire.** All 16 control cells' connected correlators
sit within 3σ of zero (0/16 flagged). The manufactured floor at these separations, on
screened qubits, is itself consistent with zero at the ~0.018/cell resolution — the
crosstalk this design budgeted for did not materially appear on this geometry.

## Fidelity, self-reported by the run

Bell pairs carried parity in BOTH bases simultaneously — pA ≈ 0.80–0.84, pB ≈ 0.94–0.97 in
ZZ *and* XX — which no product state can do, and the controls confirm the instrument reads
exactly that: ctrl0 is parity-definite only in ZZ (≈+0.96), ctrlp only in XX (≈+0.94), each
reading ≈0 in the conjugate basis. Pair A ran ~10 points below pair B (its CX is noisier);
both are unambiguously entangled, so the null is a null ABOUT entangled pairs, not about
failed preparations.

## What this is, stated at its real size

* A **gauged bound**: independent Bell pairs on this device leave no receipts on each other
  above |E| ≈ 0.04 (3σ) at coupling-map separations 2–16, in either basis. This is the
  stance's named quantum-sector instrument actually fired once, and the expected QM answer
  is the answer.
* Per the prereg's honesty clause: this result is **consistent with `precedent-is-bits`
  and lends it no support** (a classical record cannot carry quantum correlations by the
  lake's own causal-cap clause). The bulk-mediation falsifier (arXiv:2606.12457) is
  **constrained, not killed** — the paper's photonic prediction lives at sensitivities and
  separations a 25-second superconducting run does not reach, and a chip is not a cosmology.
* The single-causal-order scope note on `Core/Temporal.lean` stands unchanged: this bound
  says nature declined to use the loophole HERE, at THIS sensitivity — nothing more.

## Honest limits

One device, one session, one geometry; 3072 shots/cell (Amendment 1); mixed bases not run;
the bound is ~2.5× above the design sensitivity of the unreduced prereg. The controls bound
the floor only at the measured separations on screened qubits — noisier neighbourhoods would
carry higher floors. Nothing here moves any stance claim; `wild-share` stays open, with its
quantum sector now carrying its first measured bound instead of a promise.
