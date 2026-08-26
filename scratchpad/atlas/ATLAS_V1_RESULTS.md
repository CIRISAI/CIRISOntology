# Finite-model atlas v1 — results

**One bridge confirmed exactly, one gap measured, and one bridge KILLED in its naive
form — the killed one is the program's favored candidate, and the kill is a discovery.**
Instrument `atlas_v1.py`; stakes in `ATLAS_V1_STAKES.md`, committed first.

## S1 — CONFIRMED EXACTLY

256/256 deterministic maps on the 2×2 product space: both-coordinate-views-closed and
is-product-map agree on every map (16 each). The enumeration reproduces
`both_closed_iff_product`, so the atlas code passes its own kill. Free extras: 96 of
256 maps are one-way (exactly one coordinate closed); the parity view closes on 64.

## S2 — CONFIRMED, and the gap is measured

Common driver `a'=a⊕n, b'=b⊕n`, shared `n~Bern(q)`: both closure defects are ZERO to
machine precision at every q, while the channel creates 0.325 / 0.562 / 0.693 nats of
correlation at q = 0.1 / 0.25 / 0.5. The one-way control reads correctly (0.096–0.216
forward, 0 reverse). **The stochastic gap between mutual closure and productness IS
common-driver correlation.** Closure defects detect DIRECTED influence, not
correlation — the QPU intervention matrix must carry a common-driver control arm.

## H1 — THE NAIVE AUTONOMY–WORK BRIDGE IS DEAD, and what killed it is the finding

Staked hunt: does `βW* ≥ f(Δ_v)` exist — maintenance cost priced by closure defect?

| ε | Δ_v (unrepaired) | W* (hold code at 0.99) |
|---|---|---|
| 0.02 | **0.00000** | 0.794 |
| 0.05 | **0.00000** | 0.904 |
| 0.10 | **0.00000** | 0.947 |
| 0.20 | **0.00000** | 0.970 |

The code view `c = a⊕b⊕1` is **exactly closed** under iid per-bit flip noise — parity
is linear and the noise is additive, so `c' = c ⊕ (f₁⊕f₂)` with the flip term
independent of the state. Δ_v = 0 identically, while the cost of holding the view runs
0.79–0.97. **No f(Δ_v) can price W*: the left side is zero wherever the right side is
large.** Codex's first-choice bridge, `βW* ≥ f(Δ_v, Q_v)`, is refuted in its naive form
by a two-bit model.

**THE MISFIT READ AS A DISCOVERY.** Closure and maintenance are DIFFERENT AXES of the
object:

- `Closed` measures **autonomy** — the view's future is predictable from itself. A view
  can be perfectly autonomous and decay: its induced chain `φ` is a bona fide Markov
  chain heading to its own equilibrium.
- Maintenance is priced on the **induced dynamics' decay rate**, not on the closure
  defect. Here W* is set by the parity chain's flip rate `2ε(1−ε)` — and pricing
  maintenance by the induced decay is EXACTLY the rent clause (`rent_holds`: pay the
  decay), measured three times over (LFSR, lattice, Wilson-loop holonomy at 9.8%).

So the "autonomy–memory–work theorem" REDUCES, for closed views, to the rent law the
programme already has. The genuinely open question is sharpened, not lost:

> **H1′ — the EXCESS cost of the hidden sector.** For a NON-closed view, maintenance
> must also fight what the view cannot see. Does
> `W*(non-closed) − W*(matched closed model) ≥ g(Δ_v)` hold with g derived? That is
> the residual bridge, and v1 did not test it.

## Standing after v1

| bridge | status |
|---|---|
| mutual closure ↔ no coupling (deterministic) | **proved** + confirmed 256/256 |
| mutual closure ↔ no coupling (stochastic) | **false; gap = common drivers, measured** |
| share ↔ contextual fraction | **refuted as stated** (S3, classical parity); survives only as a functor claim |
| closure defect ↔ maintenance cost | **naive form DEAD** (Δ_v = 0, W* large); reduces to the rent law for closed views; H1′ is the residue |
| closure ↔ curvature | untested — needs the transport layer (atlas v2) |

The atlas did in one run what it was built for: killed two bridges as stated, confirmed
one exactly, and returned the killed ones as sharper questions.
