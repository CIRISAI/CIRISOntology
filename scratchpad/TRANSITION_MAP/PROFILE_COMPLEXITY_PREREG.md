# COMPLETE BATH-PROFILE COMPLEXITY — PREREG

Frozen 2026-08-22 after the smooth two-coordinate approximate-class pass, before any rough-profile screen is implemented.

## Question

The favorable smooth-ring result has exact algebra dimension N but finite-time class complexity G=64 independent of N at error 1e-3. Is that robustness tied to a genuinely low-complexity profile manifold, or does approximate bath-equivalence remain useful as the number/roughness of physically active bath coordinates grows?

This is a kill test before any expensive HEOM/HOPS/MPS implementation.

## Frozen families

Use N in {256,512,1024}, T=20 and the same cavity coupling/observable conventions as `APPROX_BATH_CLASSES_PREREG.md`.

Construct complete emitter profile matrices A with coordinate count r in {2,4,8,16,32}:

1. FOURIER-SMOOTH-r: columns are normalized sine/cosine harmonics around the ring using the first r/2 spatial harmonics.
2. FOURIER-ROUGH-r: use logarithmically spaced higher harmonics up to O(N/4), still deterministic and normalized.
3. RANDOM-FEATURE-r: seeded smooth random Fourier mixtures with frozen seed 20260822.
4. IID-PROFILES-r: seeded independent Gaussian row profiles normalized to unit row norm; this is the negative control expected to destroy class compression.

Temporal coordinates xi_alpha(t) are deterministic sums of two incommensurate sinusoids with amplitudes scaled so total RMS disorder is independent of r. Frequencies/amplitudes are generated once from seed 20260822 and written into results provenance.

## Clustering

Use complete-profile Euclidean distance, not emitter order or instantaneous energy. For G in {8,16,32,64,128,256}, construct deterministic farthest-point seeds followed by Lloyd k-means to a frozen convergence tolerance. Relabeling controls must reproduce the same error distribution.

## Observable and target

Primary target: max cavity-population error <=1e-3 over the full trajectory.

Report for each cell:
- minimum G meeting target;
- G/N;
- profile covering radius at that G;
- empirical relation between covering radius and observable error;
- full/reduced propagation work descriptively.

## Gates

C1. r=2 FOURIER-SMOOTH reproduces the prior smooth-ring minimum-G result within one frozen G grid step.
C2. deterministic relabeling leaves minimum G and errors invariant to numerical tolerance.
C3. G=N/full singleton control reproduces truth at machine floor on N=256 check cells.

## Scientific stakes

P1 — bounded-complexity regime: for FOURIER-SMOOTH, minimum G remains <=128 and changes by at most factor 2 from N=256 to 1024 for every r<=16.

P2 — coordinate-complexity scaling: minimum G grows subexponentially in r; specifically G(r=16) <=4*G(r=2) at fixed N=1024. Failure means the two-coordinate pass does not generalize even to smooth multi-coordinate baths.

P3 — roughness sensitivity: FOURIER-ROUGH requires strictly more G than FOURIER-SMOOTH at matched r in the majority of cells. If not, spatial roughness is not the controlling variable in this construction.

P4 — negative control: IID-PROFILES at r>=8 requires G>=N/2 at N=1024 or fails to meet 1e-3 on the grid. If IID remains strongly compressible, the screen is too easy to discriminate realistic complexity.

## Physics interpretation

If P1/P2 survive while P3/P4 discriminate rough/IID profiles, the measurable chemistry quantity is the covering-number curve of complete molecule-to-bath coupling profiles at a physically weighted tolerance. That becomes a concrete input to any soft-symmetry compiler.

If smooth multi-coordinate families already require extensive G, approximate bath-equivalence is not a plausible general solver route and should be cut before HEOM.

## Fence

These synthetic profile families are geometric stress tests, not molecular-environment models. They identify which empirical descriptors of a realistic bath would have to be measured or extracted from electronic/vibrational calculations before claiming computational opportunity.
