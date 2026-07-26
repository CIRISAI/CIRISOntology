# ADDENDUM 2 — my power control failed its own bar, and why the doping was the wrong probe

Committed **before `--power2` exists and before it runs**. Addendum to `KAPPA_EDGE_PREREG.md`
(`f5fa4b4`) and `KAPPA_EDGE_PREREG_ADDENDUM.md` (`a586449`). Scratchpad only.

---

## 1. WHAT FIRED

`ADDENDUM.md` ADD-2 froze three bars on the power control and stated the consequence of
failure in advance: *"If W2 or W3 fails, E1's `F ≈ 1` is UNINTERPRETABLE ... and the mission's
verdict reverts to unresolved, with the H-MANUFACTURED reading explicitly withdrawn."*

Measured, `b = 8`, κ = 0.16, σ = 1e-3, fold, exact tables:

| λ | 0 | 0.01 | 0.02 | 0.05 | 0.1 | 0.2 | 0.4 |
|---|---|---|---|---|---|---|---|
| **arm B** (dope the data) `F` | 1.0041 | 1.0039 | 1.0037 | 1.0032 | 1.0025 | 1.0015 | 1.0005 |
| **arm A** (dope the surrogate) `F` | 1.0000 | 0.9998 | 0.9997 | 0.9993 | 0.9988 | 0.9981 | 0.9974 |
| b = 2 share `s₂` | 8.51e-2 | 8.77e-2 | 9.03e-2 | 9.84e-2 | 1.12e-1 | 1.42e-1 | 2.07e-1 |

- **W1 PASSES, exactly.** Arm B at λ = 0 returns `F = 1.0041`, reproducing the independently
  measured E1 value at `b = 8` (1.0041) to four figures. Arm A at λ = 0 returns
  `F = 1.0000` with a genuine excess of `1.3e-9` — the projection of a projection is itself,
  as it must be.
- **W2 PASSES.** `F` is monotone decreasing in λ on both arms.
- **W3 FAILS, and not narrowly.** `F` never goes below **0.997**. A doping that nearly
  **triples** the b = 2 share (8.5e-2 → 2.07e-1) moves `F` by 0.3 %.

**So ADD-2's stated consequence is now owed, and it is paid in §3 — but first the failure is
diagnosed, because it is diagnosable and the diagnosis changes what is owed.**

## 2. WHY THE DOPING WAS THE WRONG PROBE — my construction error, not a property of `F`

The doped distribution was `P_λ ∝ P · exp(λ s(x)s(y)s(z))`. I described that as *"a pure,
known, sign-triple three-way coupling and **nothing else**"*. **That description is false**, and
the arithmetic says so plainly:

    M01_λ(x,y)  =  Σ_z P(x,y,z) exp(λ s(x)s(y)s(z)) / Z

which **depends on λ**. The tilt therefore **changes the level-`b` pair marginals**. The
surrogate `Q_λ` is built from those changed pair marginals, so the doping is not hidden from the
surrogate at all — the surrogate is handed a copy of it. `F` stays at 1 because the injected
structure **is** visible to pairs, which is the one thing a whole-only probe is entitled to
ignore. **The control tested the wrong thing; it does not show `F` is blind.**

The right probe injects a component that leaves **every level-`b` pair marginal exactly
unchanged**.

## 3. WHAT IS OWED, AND WHAT IS NOT

ADD-2's consequence is honoured in the following precise sense, and no wider:

- **The E1 result is NOT yet interpretable, and until §4 returns a verdict, `F ≈ 1` is not
  quoted as confirming H-MANUFACTURED.** The verdict is held, not published.
- What is **not** owed is a permanent withdrawal, because ADD-2's premise was *"W3 fails ⇒ `F`
  is near 1 for everything and measures nothing"*. That inference required the doping to be a
  fair probe. It was not. Replacing a demonstrably invalid control is not the same move as
  moving a threshold, and the distinction is stated here rather than assumed: **if POWER-2 also
  fails W3, the withdrawal is unconditional and permanent, and that is the headline.**

## 4. POWER-2 — the marginal-preserving doping

Build

    P'_λ  =  the unique distribution in  { exp(pairwise terms + λ·s(x)s(y)s(z)) }
             whose three level-`b` pair marginals equal Q's,

obtained by IPF from the starting point `Q · exp(λ s s s)` onto **Q's own** pair marginals
(IPF only ever multiplies by pair-indexed factors, so it cannot leave that family).

Two exact consequences make this the right probe and make the readout free:

1. `pair-maxent(P'_λ) = Q` **exactly**, by uniqueness of the I-projection given the pair
   marginals — so `s₂_surr` is **frozen** at `share₂(coarse2 Q)` for every λ, and any movement
   in `F` is movement in the data term alone. *(Verified numerically, not assumed: the
   projection of `P'_λ` is required to reproduce `Q` to 1e-12.)*
2. The **fine-grained** whole-only share of `P'_λ` at level `b` is `H(Q) − H(P'_λ)`, available in
   closed form with no second projection.

So POWER-2 delivers, for free, the thing the mission actually needs and neither prereg thought
to ask for: **a transfer function** from nats of genuine level-`b` whole-only structure to nats
of b = 2 excess. λ ∈ {0, 0.02, 0.05, 0.1, 0.2, 0.4, 0.8}, `b ∈ {8, 16}`, exact tables.

**Bars, frozen here:**

- **W1'** `F(0) = 1` to 1e-9 and `pair-maxent(P'_0) = Q` to 1e-12.
- **W2'** `F(λ)` monotone decreasing.
- **W3'** `F` falls **below 0.5** somewhere in range. *If it does not, §3's withdrawal becomes
  unconditional and the mission reports UNRESOLVED.*
- **W4'** the **sensitivity** is quoted as the genuine level-`b` whole-only share (in nats) at
  which `F` first drops below **0.99**, i.e. the smallest real structure this instrument could
  have distinguished from manufacture at 1 % resolution. The E1 null is then quoted **as a null
  with that sensitivity attached**, never as a bare "we found nothing".

## 5. ERROR BAR ON `F` — registered here because §4 makes `F` the headline number

`F` has so far been computed from one estimated table with no uncertainty attached. Added:

**BLOCK.** Split the triples into **16 contiguous blocks by start frame** (blocks are separated
in time, so this respects the autocorrelation the iid multinomial floor does not), recompute
`F` and the genuine b = 2 excess `s₂(1 − F)` independently on each, and quote mean ± standard
error over blocks. Reported for `b ∈ {4, 8, 16}` at κ = 0.16, and at the κ = 0.05 and κ = 0.30
controls.

A genuine excess consistent with **zero** at this error bar, against a manufactured 8.5e-2,
is the form the H-MANUFACTURED verdict must take if it is to be quoted at all — a null with a
number on it.
