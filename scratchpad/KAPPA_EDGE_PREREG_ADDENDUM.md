# PRE-REGISTRATION ADDENDUM — the power control, and a kill that fired on my own machinery

Committed **before `--power` and `--fdual` exist and before either runs**. Addendum to
`KAPPA_EDGE_PREREG.md` (`f5fa4b4`). Scratchpad only; no Lean file, no `Stance.lean`, no audit.

Two things forced this addendum, both disclosed here rather than absorbed silently.

---

## ADD-1 — K-VOID FIRED, at `b ∈ {4, 6, 8}`, and it fired on my own solver

`KAPPA_EDGE_PREREG.md` §5 froze **K-VOID**: *"IPF/dual disagreement > 1e-8 in `H(Q)`"* voids E1.
On the first E1 run the measured `|ΔH|` between the IPF projection and the independent dual
solve is:

| `b` | 2 | 3 | **4** | **6** | **8** |
|---|---|---|---|---|---|
| `\|ΔH\|` | 7.2e-10 | 2.2e-9 | **1.2e-6** | **4.7e-8** | **1.1e-8** |
| IPF marginal residual | 7.3e-15 | 1.0e-14 | **1.1e-7** | 1.0e-14 | 1.0e-14 |

**`b = 4` is the offender**: IPF did not reach its 1e-14 tolerance inside 200 000 iterations
(469 s wall), residual 1.1e-7, and the dual disagrees at 1.2e-6. `b = 6` and `b = 8` exceed the
bar marginally with IPF fully converged, so there the dual is the weaker solve, not IPF.

**The bar is not waived and the rung is not dropped.** The remedy is to re-derive the
conclusion *without* the IPF solution:

**FDUAL.** Recompute `F = share₂(coarse-grain Q) / share₂(coarse-grain P)` from the **dual**
`Q` at every `b`, and report `F_ipf` and `F_dual` side by side.

- If `|F_dual − F_ipf| ≤ 0.01` the E1 verdict is **independent of which solver produced `Q`**
  and stands; the fired K-VOID is reported as a **precision** failure of the projection's
  entropy that does not touch the quantity the verdict rests on.
- If they differ by more than that, **E1 is void at that `b`**, as registered, and the verdict
  rests only on the rungs that pass.

The reason this is not a rescue, stated so it can be checked: `F` depends on `Q` only through
`coarse2(Q)`, whose **three pair marginals are identically equal to `coarse2(P)`'s** — because
coarse-graining commutes with marginalisation — so `F` is driven by a single number, the
sign-triple `E[s₁s₂s₃]`, and is far less sensitive than `H(Q)` is. That prediction is testable
and FDUAL tests it.

---

## ADD-2 — THE POWER CONTROL, and why the E1 result is worthless without it

E1's first reading is **`F ≈ 1.00`** — the zero-whole-only-share surrogate reproduces the
measured b = 2 share essentially exactly. **A test that returns "everything is manufactured"
is only informative if it is capable of returning something else on data that is not.**
Gate `Ge` shows `F` is forced to 0 on a sign-symmetric field and `Gf` shows manufacture is
possible at all, but neither shows the test has **power against genuine three-way structure**
sitting on top of the array's own pair structure. Registering that now:

**POWER.** At the primary point (κ = 0.16, σ = 1e-3, fold), take the measured level-`b` table
`P`, form its pair-maxent projection `Q`, and build a **doped** distribution

    P_λ  ∝  Q(x,y,z) · exp( λ · s(x) s(y) s(z) ),      s(x) = +1 if x ≥ b/2 else −1

which is `Q` — a distribution with **exactly zero** whole-only share at level `b` — plus a pure,
known, sign-triple three-way coupling of strength λ and **nothing else**. Then run the full E1
pipeline on `P_λ` exactly as on the real data: project, coarse-grain, compute
`F(λ) = share₂(coarse2(pair-maxent(P_λ))) / share₂(coarse2(P_λ))`.

`λ ∈ {0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.4}`, at `b ∈ {8, 16}`, exact tables (no sampling), so the
curve carries no estimator noise.

**Pre-registered pass conditions, frozen here:**

- **W1** `F(0)` reproduces the measured `F` at that `b` to within 0.01. *(If it does not, the
  doping construction is not a faithful stand-in for the data and POWER is void.)*
- **W2** `F(λ)` is **monotone decreasing** in λ.
- **W3** `F` falls **below 0.5** at some λ in the tested range — i.e. the test *can* report
  "not manufactured" on data that carries real three-way structure at the level at which the
  surrogate is built.
- **W4** the λ at which `F` crosses 0.5 is reported as the instrument's **detection threshold**,
  in nats of genuine b = 2 excess, so the E1 null is quoted with a sensitivity and not as a bare
  "we found nothing".

**If W2 or W3 fails, E1's `F ≈ 1` is UNINTERPRETABLE** — it would mean `F` is near 1 for
everything and measures nothing — and the mission's verdict reverts to *unresolved*, with the
H-MANUFACTURED reading explicitly withdrawn. That outcome would be reported as the headline.
This is the control that can take down the answer I already have, which is why it is registered
before it runs rather than after.

**Honest note on what POWER does not do.** It injects structure of exactly the form the b = 2
statistic is built to see (a sign triple). Real structure of some other form could be less
visible. So W3/W4 establish power against the **best case** for the instrument, and the
sensitivity quoted is a **lower bound on the detection threshold**, not a universal one. Stated
in advance so it is not read as more than it is.

---

## ADD-3 — one scored prediction that E0 already split, recorded before the results memo

For the record and against later smoothing: `KAPPA_EDGE_PREREG.md` §3 **Z3** predicted the route
ratio would be **≤ 30** outside the crossing. The completed E0 run gives 30.3 and 31.2 at
κ = 0.200 but **72–139** at κ = 0.140–0.145. **Z3 is SPLIT** — the *spike* at κ₀ is confirmed far
beyond what was predicted (ratio → ∞ at the crossing, 1 381 at κ = 0.160), the *baseline* bar is
**not met**, and the residual route gap outside the zero is therefore **30–140×, not the ~2–10×
I guessed**. That residual is what E1 must account for, and this addendum is committed before
the number that accounts for it is written up.
