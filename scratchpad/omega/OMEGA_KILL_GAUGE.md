# Ω-KILL gauge verdict — A5/M1 STOP; the experiment runs on 8 arms

G1 passes (α̂ = 0.6008 vs true 0.6000; bound holds). **G2 fails to fire**: the
planted hidden-regime non-Markov chain does NOT violate `defect(m) ≤ α̂^m` —
slow-regime memory is ABSORBED by the pooled Dobrushin coefficient (rows that
differ across regimes inflate α̂ exactly as much as they inflate the defect). A
bounded construction attempt for the one violable class (echo-type memory:
identical lag-1 rows, divergent lag-m futures in the view) also failed — every
construction either equalized the v-pushes or drove α̂ to 1.

**Verdict, per the frozen tree: S1-A5 and S3-M1 are UNPOSABLE AS STAKED** — the
instrument cannot detect a planted violation, so a pass would have been
decoration. They STOP. Recorded finding, not a failure: with in-sample α̂ on
stationary data, the Dobrushin bound has near-zero killing power outside a
narrow echo class. A future arm needs either an out-of-sample α̂ (kernel from
one regime, defect from another) or a substrate with engineered echo memory.

**Ω-KILL proceeds on 8 arms: S1 A1–A4, S2 B1–B4. Binary exit unchanged:
CONFIDENCE ⇔ 8/8, else FALSIFICATION.**
