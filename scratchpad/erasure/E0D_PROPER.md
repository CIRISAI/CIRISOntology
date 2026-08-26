# E0d proper — GO, with two ruler calibrations carried into the unblind

Synthetic underdamped Langevin at pinned f₀=1090 Hz, Q=7, fs_a=54.5 kHz, windowed
exactly as the real analysis. Recorded BEFORE the unblind ran.

- **Transfer: YES.** E3-style witness gain +0.0072 (p=0.0025); E1 windowed gains rise
  to +0.032 at 0.44 ms and the CI touches zero at 0.88 ms — at the window edge, as
  stage-2b's posability note predicted. STOP does not fire.
- **Calibration 1 (from the dev gauge):** the τ_c ruler reads 2.45× τ_R on known truth.
- **Calibration 2 (new):** at fs_a the velocity-only fiber does NOT beat position-only
  even on synthetic truth where velocity genuinely decides the outcome (pos +0.0147 vs
  vel +0.0052). **E3's velocity-dominance sub-claim is therefore VOID-capable:** an
  inverted real-data reading is an instrument limit, not physics. E3's PRIMARY
  (witness gain beyond the bit, CI > 0, Bonferroni p) is unaffected.
- **Floor note:** the permutation floor for E3-style gains is NEGATIVE (−0.009 at the
  95th) because overfitting dominates the null; "> 5× floor" therefore reduces to
  CI > 0 ∧ p < 0.0125, declared here.
