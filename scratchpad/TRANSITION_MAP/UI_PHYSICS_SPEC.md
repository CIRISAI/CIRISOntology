# UI PHYSICS — driving CIRISClient's graph view with the object's actual physics
(spec, 2026-08-23)

Steward: *literal* physics, fsn/Jurassic-Park style. CIRISClient already has the
machinery — `ForceSimulation.kt` (D3-style Coulomb + spring + center + alpha cooling),
`CylinderLayout.kt` (3D rings, perspective, depth-scaled alpha), `GraphNodeDisplay`
with `x,y,vx,vy` and an `extra` map. What it does not have is physics that MEANS
anything: every constant is chosen by feel.

**The object supplies a measured or proved replacement for each one.** Below, each maps
to a specific file and a specific constant.

## 1. Spring constants — from the measured coupling matrix
`ForceSimulation(linkStrength = 0.3f)` is one number for every edge. Replace with the
per-edge `k_ij` of the object's symmetrised coupling matrix (the sealed disagreement
matrix; 25,286 events, 15.5% empty channels). Edges then have REAL stiffness: kinds
that are genuinely confusable are genuinely bound. The layout stops being decorative and
becomes a measurement rendered.

## 2. Normal modes — the layout's dynamics IS the graph Laplacian
A spring network's motion is governed by the Laplacian of `k_ij`; its eigenvectors are
the layout's normal modes. Precompute them once (11×11 — free). Uses:
- localized modes (high IPR, the S4 diagnostic) mark rigid regions;
- mode frequencies give a principled `alphaDecay` per mode instead of one global cooling.

## 3. THE DEMONSTRABLE ONE — dark states are literally invisible motions
`DarkState.twin_dark_state` + `dark_state_decoupled` (proved, any commutative ring):
under EXACT twin symmetry, pushing Structure `+x` and Circumstances `−x` by equal
amounts is an exact eigenmode that **no other node can feel**. Every other row
annihilates it.

So the UI can offer a gesture — grab a twin pair, pull them apart antisymmetrically —
and under the symmetrised matrix **the rest of the graph provably does not move.**
Then switch to the REAL matrix and it leaks, by exactly `g_DB = Δ_σ/(2√2)`
(`DefectCoupling`, measured 2.284 for Priorities/Process, 8.617 for
Structure/Circumstances — a 3.8× difference the user can SEE).
That is the fsn moment: a gesture with a proved null result, and a measured departure
from it.

## 4. The z-axis is depth — but NOT a hierarchy
`CylinderLayout` currently stacks by time. Depth (`Surface.depth_counts` = [3,2,0,2];
surfaces at 0, Facts→Confidence→Model→Premises at 0..3) is the natural third axis.
**M8 binds the rendering: hierarchy is rare (44/208, ~21%), cycles are generic.** So
render depth as a GRADIENT with cycles visible, never as a tree. A tree view would
display a property the object does not have.

## 5. Node mass — from positional fragility (M9)
`radius`/mass is currently a per-type constant. M9: leakage rate = dose² × a
susceptibility of the FIELD ALONE, computable before any perturbation. So a node's
inertia is derivable: **low susceptibility = heavy, fragile = light.** Perturbation
response becomes predictive rather than cosmetic.

## 6. A genuine magnetic mode — the holonomy
`RouteSymmetry.return_even_of_transpose` (proved): with U(1) phases on edges, return
amplitudes are EVEN in the loop flux, while transfers are chiral. Expose flux Φ as a
control: returns behave symmetrically under Φ → −Φ, transfers do not. Measured on the
lattice: transport suppressed up to −18% at Φ = 90°, exact period-π, replicated at two
densities. This is a real interference effect the object owns, and it looks like
physics because it is.

## 7. Record edges are one-way
Machine-zero backflow (Leg A S4 = 0.0000, `record_not_site_generated`). Render Record
couplings as non-reciprocal: force applies in one direction only. Most force engines
assume symmetric springs; this one must not.

## Implementation order (smallest first)
1. `ForceSimulation`: accept a coupling MATRIX instead of a scalar `linkStrength`.
2. Precompute Laplacian modes; expose them for mode-locked camera/highlighting.
3. **Ship the twin-probe gesture** — it is the demo, and it is proved.
4. Depth as z in `CylinderLayout`, cycles preserved.
5. Mass from susceptibility.
6. Flux control for the holonomy mode.

## Honest limit
The physics here is real and proved; whether it makes a GOOD interface is an empirical
question about people, not about the object. Nothing above is a UX claim. What is
claimed is that each force constant can be replaced by something the repository can
justify by theorem or measurement — so the visualization becomes an instrument rather
than an illustration.
