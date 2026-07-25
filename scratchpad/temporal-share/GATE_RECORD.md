# Simulator gate record — 2026-07-24

Pipeline: hw_pipeline.py at this commit. Seed 20260724, B=1000, 4096 shots.

```
ideal d=0ns: positive 0.6930 (ln2=0.6931) ok=True; negative 0.0008 ok=True; idle max 0.0002 (null99 0.0013) quiet=True
ideal d=2000ns: positive 0.6931 (ln2=0.6931) ok=True; negative 0.0000 ok=True; idle max 0.0003 (null99 0.0013) quiet=True
noisy d=0: positive 0.4357, negative 0.0001, pos floor99 0.0008 -> sensitivity ok=True
GATE PASS
```

All three prereg gate criteria pass. Hardware submission now awaits (1) Eric sign-off
on HW_PREREG.md, (2) IBM credentials. One job, 58 circuits x 4096 shots.
