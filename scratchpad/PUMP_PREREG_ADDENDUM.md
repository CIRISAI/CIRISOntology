# PUMP prereg — ADDENDUM: an independent check of §4.3, and one amendment that must land before the run

**Status.** `PUMP_PREREG.md` (commit `64028fb`) stands and is good work. This document does not
replace it. It records an independent re-derivation of its load-bearing analytic result and six
findings, one of which is **fatal to a kill band as written** and must be amended **before**
task #9 builds the instrument or task #10 runs anything.

**Committed before any curve was computed**, like its parent. Everything below is either (a) a
hand re-derivation of the prereg's own algebra, or (b) arithmetic evaluating the prereg's own
published closed form at chosen parameters. **No solver was run, no state was constructed, and no
reading of the pump curve exists anywhere in this document.** Checking whether a stated formula,
its declared validity region and its kill band are mutually consistent is refutation of a
pre-registration, not measurement of a result; the distinction is the whole reason this can be
done now rather than after.

Script: `/tmp/…/scratchpad/prereg_consistency2.py` (scratch, not committed — every number below is
reproducible from the formula in §4.3 in three lines).

---

## FINDING 0 — the closed form is CORRECT. Re-derived independently, end to end.

Before criticising anything, the central result was checked rather than trusted. Every step of
§4.3 was re-derived from scratch and every step agrees:

| step | §4.3 says | independent re-derivation |
|---|---|---|
| moment propagation, singles | `m = a` | ✓ `⟨z⟩_out = κ⟨z⟩ + a`, and `⟨z⟩_in = 0` |
| moment propagation, pairs | `r = r₀ + a²` | ✓ `κ²ρ + a²`, conditional independence across cells |
| moment propagation, triple | `c = 3r₀a + a³` | ✓ `κ³·0 + aκ²·3ρ + 0 + a³` |
| cell probabilities | `p₀…p₃` by Hamming weight | ✓ all four checked against `p = (1 + m Σz + r Σzz + c z₁z₂z₃)/8` |
| the competitor line is the `c` line | asserted | ✓ `∂p/∂c ∝ (+1,−1,+1,−1)` by weight — exactly the parity character `χ` |
| stationarity | `p₀p₂³ = p₁³p₃` | ✓ it is `dH/dc = 0`; the `+1`s cancel because `1−3+3−1 = 0` |
| maximiser | `c* = 3r₀a/(1+2r₀)` | ✓ solving `B(3+γ) = 3A(1−γ)` with `A = 1+3r₀`, `B = 1−r₀` |
| displacement | `\|Δc\| = 6r₀²a/(1+2r₀)` | ✓ |
| Hessian | `\|g''\| = (1+2r₀)/[(1+3r₀)(1−r₀)]` | ✓ `−(1/64)[1/p₀ + 3/p₁ + 3/p₂ + 1/p₃]` at `a = 0` |
| **the law** | **`Δ = 18r₀⁴a²/[(1+2r₀)(1+3r₀)(1−r₀)]`** | ✓ **exactly** |

**P-FORM is sound as an `a → 0` statement, and P-FORM-κ's eighth power and P-FORM-ρ's fourth
power follow.** The rest of this document is about where that statement may be *applied*.

---

## FINDING 1 — FATAL: §4.6's validity region and §4.3's kill band are mutually inconsistent. P-FORM will fire spuriously.

**The mechanism.** §4.3's own moment line says the output's **raw** pair moment is `r = r₀ + a²`.
The `a²` there is not a correlation — it is the square of the induced magnetisation `m = a`, and
the *connected* pair correlation is exactly `r₀ = κ²ρ`, cleanly. But the cell probabilities
`p₀…p₃` are written in **raw** moments, so the maximiser and the Hessian must be evaluated at
`r = r₀ + a²`, and §4.3 evaluates them at `r₀`. That is correct to leading order — it is what
makes the `a²` law right — and it makes the **relative** size of the first neglected term

> `≈ 4a²/r₀ + a²/(1−r₀)`,

because `C ∝ r⁴/(1−r)`. Neither denominator is bounded away from zero inside the declared region.

**The numbers**, evaluating §4.3's own `C(r)` at `r₀` and at `r₀ + a²`, `ρ = 1`, `a = 0.25`
(the flat cap §4.6 declares):

| `κ` | `r₀ = κ²` | `C(r₀)` | `C(r₀+a²)` | **ratio** | max `\|a\|` for a 2 % band | vs the declared 0.25 |
|---|---|---|---|---|---|---|
| 0.10 | 0.0100 | 1.731e−07 | 3.846e−04 | **2222** | 0.0071 | **35× too loose** |
| 0.20 | 0.0400 | 3.968e−05 | 1.405e−03 | **35.4** | 0.0143 | 17× |
| 0.30 | 0.0900 | 8.660e−04 | 6.039e−03 | **6.97** | 0.0219 | 11× |
| 0.50 | 0.2500 | 3.571e−02 | 7.931e−02 | **2.22** | 0.0373 | 6.7× |
| 0.70 | 0.4900 | 4.160e−01 | 6.700e−01 | 1.61 | 0.0501 | 5.0× |
| 0.80 | 0.6400 | 1.260e+00 | 1.972e+00 | 1.56 | 0.0527 | 4.7× |
| 0.90 | 0.8100 | 4.538e+00 | 8.239e+00 | 1.82 | 0.0480 | 5.2× |
| 0.95 | 0.9025 | 1.178e+01 | 3.908e+01 | **3.32** | 0.0387 | 6.5× |

**Read the bottom line: §4.3 stakes a 2 % kill band over `κ ∈ [0.1, 0.95]`, and §4.6 declares the
form valid out to `|a| = 0.25`, where the first neglected term is between 56 % and 222 200 %.**
P-FORM is therefore **guaranteed to fire**, everywhere, for a reason that has nothing to do with
the physics — and a kill that is guaranteed to fire carries no information. Under the house rule
that a kill must be able to be survived, this one cannot be, so it is not yet a kill.

Note the worst case is at **low** `κ`, not high. There the surviving connected correlation
`r₀ = κ²ρ` becomes *smaller than* the induced `a²`, and since `C ∝ r₀⁴`, a shift of `r₀` by `a²`
is a factor `(1 + a²/r₀)⁴`. At `κ = 0.1` that is `(1 + 6.25)⁴ ≈ 2200`.

### The amendment, and it is cheap

Replace §4.6's flat cap with a region that scales, staked here before the run:

> **§4.6′ (amended).** The closed form is declared valid where
> **`a² ≤ 0.005 · min(r₀, 1−r₀)`**, with `r₀ = κ²ρ`. Outside it, only the exact solver is quoted
> and the closed form is plotted as a visibly-labelled extrapolation.

Checked against the computed caps: `κ = 0.10 → |a| ≤ 0.0071` (computed 0.0071 ✓);
`κ = 0.50 → 0.035` (computed 0.0373 ✓); `κ = 0.95 → 0.022` (computed 0.0387, conservative ✓).
Two further options, either acceptable and both strictly better than the flat cap:

- **quote `C` at the output's own raw `r`** rather than at `r₀`. This resums the dominant
  neglected term for free and costs one substitution; the kill band then means what it says.
- **redo the expansion keeping the output's actual `(m, r)`.** Correct but more work, and the
  `O(a²)` correction to `c*` from `m = a` enters at the same order, so it must be kept too — this
  is *not* a one-line patch and should not be attempted under time pressure.

**Recommendation: adopt §4.6′ and the `C(r)` substitution. Do not attempt the full re-expansion
before the run.** The `a²` law and the band are then consistent and P-FORM becomes a real stake.

---

## FINDING 2 — the crossover line, and both of the repository's exhibited channels sit on it

The same algebra names a structural feature worth having in the results document. The induced
magnetisation squared equals the surviving connected pair correlation when `a² = r₀ = κ²ρ`, i.e.

> **`|a| = κ√ρ`**, and at `ρ = 1`, **`|a| = 1 − 2s`.**

Below that line the output's pair structure is inherited from the input; above it, it is dominated
by what the channel itself put there. And:

| channel | where it sits |
|---|---|
| **`Core/Valve.lean`'s `damp`** (`a = ½`, `κ = ½`) | **exactly on the line**, `a/κ = 1.000` |
| hardware ray, perfectly cold (`α = 1`) | crosses at `κ = 0.500` (`s = 0.250`) |
| hardware ray, `p_exc = 0.05` (`α = 0.90`) | crosses at `κ = 0.474` |
| hardware ray, `p_exc = 0.09` (`α = 0.82`) | crosses at `κ = 0.451` |

So the theorem's own witness sits precisely where the perturbative picture changes character, and
the hardware trajectory sweeps *through* the line as it idles. This sharpens
`PUMP_PRIOR_ART_ADDENDUM.md` §A8's "both exhibited points are corner points" into something
quantitative, and it belongs in §4.5's QPU-3 placement plot as a drawn line.

---

## FINDING 3 — the closed form vs a machine-checked theorem, computable now

Evaluating §4.3's form at `damp` (`a = ½`, `s = ¼`, `ρ = 1`) gives **0.008929 nat**.
`Core/Valve.valve_upward_bound` proves the true value is **≥ 0.011962 nat**. Ratio **0.746**.

Not a contradiction — `a = ½` is far outside any sane validity region, and an `O(a⁴)`-truncated
expansion is not expected to hold there. It is a **free quantitative statement, available before
the run**: the truncated form under-predicts by **at least 25 %** at the boundary point, which
independently corroborates Finding 1 and confirms §4.5's decision to use the exact solver rather
than the closed form wherever hardware strays to large `a`. Worth one line in the results.

---

## FINDING 4 — "share exactly zero at every k" is ARGUED, not proved. §2 Arm C and §5.2 over-reach.

`Core/SignSymmetry.lean` is stated **entirely on `Bool × Bool × Bool`**. Grep confirms it: no
`Fin k → Bool` anywhere in that file, and no sign-symmetry lemma of any kind in `ShareK.lean` or
`HammingCap.lean`. So `share_eq_zero_of_signSymmetric` is a **k = 3 theorem only**.

| where | what it says | what is actually proved |
|---|---|---|
| §2, Arm C | "Sign-symmetric at every k, **hence** share exactly zero at every k" | the *hence* holds at k = 3 only |
| §5.2 plumb lines | "any sign-symmetric state → exactly 0 — `share_eq_zero_of_signSymmetric`" | k = 3 only; the row is unlicensed at k ≥ 4 |
| §4.4 P-K | "P-EVEN's argument runs at every k" | **this one is fine** — P-EVEN is a relabelling symmetry of `share` itself, not the vanishing lemma |

The claim is very likely true (the symmetrisation argument should generalise) but the repository
does not prove it, and `CLAUDE.md`'s rule is that `proved` means machine-checked *here*.

**Amendment:** at k ≥ 4, mark the zero-share-of-repetition-code claim **argued**, and demote it
from a *plumb line* (a known answer the instrument is checked against) to an *instrument check*
(a reading the instrument produces, which is expected to be zero and is reported if it is not).
The two are not the same and only one of them can be used to validate the solver. Arm C's k = 3
rung remains a genuine plumb line via `share_ferro`.

---

## FINDING 5 — reach 3 is not discharged. The `a = 0` control is a zero control, not a mixture null.

§5's table discharges GATES.md reach 3 with: *"the null that must not reproduce the effect is the
same channel with `a` set to zero at the same `s`."*

That is an excellent **zero control** — better than most, because its answer is a theorem — but it
is not what reach 3 asks. Reach 3's gauge gate is: *the mixture null must be able to **manufacture**
the data's generative structure, or it gauges nothing.* A control that provably produces exactly
zero manufactures nothing by construction. **Its being a good control is precisely why it is not
this gate.**

The live manufacture risk in this campaign is the one Kahle et al. 2009 walked into and diagnosed
(and which `PUMP_PRIOR_ART_ADDENDUM.md` §A6 names as their real contribution): **§3.2's `n`-sweep
is a guaranteed interior peak in a swept parameter**, and §4's own reasoning says so ("the curve
**must** be a bulge"). The intermediate states of an amplitude-damping channel *are* convex
combinations of relaxed and unrelaxed components. That is Kahle's failure mode exactly.

**Not fatal** — the campaign's primary observable is the one-step mint `Δ(a,s)`, and §3.2 is
secondary. But the cell must not be marked discharged. **Amendment:** reach 3 reads
**LIVE, undischarged for the `n`-sweep**, discharged by theorem for the one-step mint; and any
interior peak in `n`, `s`, `ρ` or `k` that is reported as a finding carries a mixture null against
the convex combination of its own endpoint states before it is believed.

---

## FINDING 6 — the external calibration is missing, and it is the cheapest gate available

All seven of §5.2's plumb lines are **internal** — our own Lean, checked against our own solver.
Not one is external. `PUMP_PRIOR_ART_ADDENDUM.md` §A1 asked for the one that is, and it did not
land:

> **Reproduce Schneidman et al. 2003, Fig. 2** — nine panels, `I_C^(3)` and `I_C^(2)` against
> noise amplitude for noisy AND, OR and XOR under output noise, input noise, and input-dependent
> output noise. Eight cells, exactly computable, microseconds. `Core/Share`'s `share` **is** their
> `I_C^(3)` (their Eq. 6), so the comparison is definitional, not analogical.

Why it is worth more than any internal plumb line: it checks the instrument against a **published
figure produced by other people with other code**, and it is the paper this campaign is scooped by,
so agreement is also the citation being earned. Their Fig. 1 row for AND/OR (`I_C^(3) = 0`,
`I_C^(2) = 0.8113` bits) is a second, exactly-checkable rung.

An asset already exists: `scratchpad/verify_schneidman.py` (2026-07-25, uncommitted, from the ECA
campaign) reproduces **Fig. 1** — the noiseless table — using this repository's exact k = 3 solver.
It does **not** do Fig. 2. Extending it is the smallest useful piece of work in the campaign.

**Amendment:** add **P-SCHNEIDMAN** to §5.2 as a plumb line, run before the pump curve, with the
Fig. 1 row as an exact check and the Fig. 2 panels as a shape check. Per §A1, which of the three
noise columns creates order-3 on AND is an *inference* from the paper's text and not a quotation,
so Fig. 2 is staked as a **shape** agreement, not a numerical one.

---

## FINDING 7 — one sentence missing from §9, and §7 is where it bites

Every arm A–E is inside the sign-symmetric family, so the `a = 0` control is theorem-pinned
throughout and the campaign is internally safe. But §9's "May not" should say what §7's downstream
mappings otherwise invite:

> **The `a = 0` null is theorem-pinned only on sign-symmetric inputs.** On an input that is not
> sign-symmetric, a unital channel *can* mint whole-only share — this is published and measured
> (Schneidman 2003, the AND and OR panels: a fixed-probability flip is the binary symmetric
> channel, which is unital, and AND is not sign-symmetric). State asymmetry and channel asymmetry
> are independent pumps, and this campaign measures the channel one.

This matters exactly where §7 does its work: the sky, glass and water substrates are **not**
sign-symmetric, so a mapping that carries the `a`-law to them without carrying this caveat would
license a conclusion the campaign has not earned.

---

## THE AMENDED STAKES, in one place, before the run

| # | amendment | severity |
|---|---|---|
| 1 | §4.6 → **`a² ≤ 0.005·min(r₀, 1−r₀)`**, and quote `C` at the output's own raw `r` | **blocking** — P-FORM is uninformative without it |
| 2 | draw `\|a\| = κ√ρ` on §4.5's placement plot; `damp` sits on it, the hardware ray crosses it | reporting |
| 3 | record that the truncated form gives 0.008929 vs the proved ≥ 0.011962 at `damp` (0.746) | reporting |
| 4 | k ≥ 4 zero-share: **argued**, demoted from plumb line to instrument check | honesty |
| 5 | reach 3: **LIVE, undischarged for the `n`-sweep**; mixture null on any interior peak | gate |
| 6 | add **P-SCHNEIDMAN** — the one external calibration | gate |
| 7 | add the sign-symmetry caveat to §9, because §7's mappings need it | scope |

**Nothing here changes P-EVEN, P-EXP, P-K, P-QPU, arms A–G, the solver certificates, the
occupancy gate or the verdict grid**, all of which survive the check unaltered. The `a²` law
itself is re-derived and confirmed. What changes is one validity region, one gate cell, one
honesty label, and two additions.

*No Lean touched, `lake` never run, nothing moves `Stance.lean`. Corrections to `Core/Valve.lean`
remain as named in `PUMP_PRIOR_ART_ADDENDUM.md` §12 — named, not made.*
