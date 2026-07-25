# The Hadamard connection, and who got there first

**Companion to `HAMMING_FORM_SCAN.md` (commit 11eb2a9) and `CLASSICAL_MAX_K5.md`.**
Primary sources read in full where marked; every unverified item is flagged.
Nothing here is mechanized; no Lean file, `Stance.lean`, or audit was touched.

---

## Headline, stated before the detail

Two things, and the second one is bad news for us.

> **(A) The connection is real.** The maximum classical whole-only share on `k` slots
> with uniform pair marginals is governed by orthogonal-array existence, and at
> `k ≡ 3 (mod 4)` the formula `maxshare(k) = k·ln2 − ln(k+1)` is **exactly equivalent
> to the Hadamard conjecture** — open since 1893. The smallest `k` at which our own
> formula is an open problem in combinatorics is **k = 667**.
>
> **(B) It is not ours.** The classical maximum, the Hadamard equivalence, and the
> proof route (Shannon ≥ Rényi-2, orthonormal-frame bound) are all **in print**:
> Lancaster 1965, conjectured in the entropy form by Babai 2013, proved by
> **Gavinsky & Pudlák 2016, Theorems 3.1/3.2/4.1**. Independently, **Albanna, Hillar,
> Sohl-Dickstein & DeWeese, *Entropy* 19(8):427 (2017)** set up the identical polytope,
> use the identical Rényi-2 route, and single out our exact case (µ=1/2, ν=1/4).
> **VERDICT: CONVERGENT.** A narrow residue survives as ours and is named in §B.4.

The residue that survives is *not* the headline. It is the sharpening at
`k ≢ 3 (mod 4)`, from `ln(k+1)` up to `ln(4⌈(k+1)/4⌉)` — real, verified by me
independently, and apparently not in print, but a refinement of someone else's theorem.

---

# (A) The exact status of the formula

## A.1 The three ingredients, each verified against a primary source

`N₀(k)` = minimum number of runs of a binary strength-2 orthogonal array on `k` factors.

**(i) Divisibility: `4 | N` for every `OA(N, k, 2, 2)` with `k ≥ 2`.** Elementary and
unconditional: strength 2 requires each of the four symbol pairs in each pair of columns
exactly `N/s^t = N/4` times, so `N/4 ∈ ℤ`. This is the number Beder & McComack call `L_t`
("It is an elementary fact that the size of an orthogonal array of strength `t` on `k`
factors must be a multiple of a certain number, say `L_t`" — *A note on the minimum size
of an orthogonal array*, arXiv:1508.06558, abstract, read).

**(ii) Rao bound: `N ≥ 1 + k` for strength 2, two levels.** Verified in the 2025 review
*Orthogonal Arrays: A Review* (arXiv:2505.15032), §4.2: for even strength `t = 2u`,
`N ≥ Σ_{i=0}^{u} C(k,i)(s−1)^i`; at `s=2, u=1` this is `N ≥ 1 + k`. Original: Rao 1947,
*Supplement to JRSS* 9(1):128–139.

Goyeneche & Życzkowski quote the same Rao bounds in the quantum setting and tabulate
them (arXiv:1404.3586v2, Fig. 5 caption, read verbatim): "`r₁ = 2, r₂ = N + 1, r₃ = 2N,
r₄ = N²/2 + N/2 + 1 and r₅ = N² − N + 2`".

**(i)+(ii) give, unconditionally, `N₀(k) ≥ 4⌈(k+1)/4⌉`.**

**(iii) Attainment ⟺ Hadamard.** The standard reference, verified through two independent
routes:

> "There exists an OA(4λ, 4λ − 1, 2, 2) if and only if there exists a Hadamard matrix of
> order 4λ."
> — Wikipedia, *Orthogonal array*, §"Other constructions / Hadamard matrices", citing
> **Hedayat, Sloane & Stufken (1999), Theorem 7.5** and Stinson (2003) p. 225, Thm 10.2.
> (Raw wikitext fetched and read directly.)

Independently quoted, with page number, by Goyeneche & Życzkowski (arXiv:1404.3586v2,
§V, read verbatim from the PDF):

> "Some orthogonal arrays of strength 2 are connected with the famous Hadamard conjecture
> – see Theorem 7.5, p. 148 [31]:
> **THEOREM 6 (Hedayat)** Orthogonal arrays OA(4λ, 4λ − 1, 2, 2) exists if and only if
> there exists a Hadamard matrix of order 4λ."

Their [31] is Hedayat–Sloane–Stufken. So: **HSS Theorem 7.5, page 148.**

## A.2 The index shift, pinned

HSS write `F(k, s, t)` for the minimum run size of an `OA(N, k, s, t)`. Our `N₀(k)` for
`k` slots is `F(k, 2, 2)`. The claim the coordinator's search surfaced —
`F(k−1, 2, 2) = 4⌈k/4⌉` — substituting `k → k+1` becomes

```
F(k, 2, 2) = 4⌈(k+1)/4⌉ = N₀(k)          ✓ agrees with ours
```

and at `k = 4λ−1` it reads `F(4λ−1, 2, 2) = 4λ`, the form in which the equivalence is
usually stated. **The conventions agree; there is no off-by-one in our formula.**

**UNVERIFIED:** I could not open the HSS book text, and the `F(k,s,t)` notation does *not*
appear in the 2025 review (arXiv:2505.15032 — checked, absent), in Sloane's `oadir` library
page (checked, absent), or in the Wikipedia article (raw wikitext checked, absent). The
statement "the Hadamard conjecture is equivalent to `F(4λ−1, 2, 2) = 4λ` for all positive
integers λ" appears only at search-summary level in my sources. **Its mathematical content
is nevertheless fully established** by (i)+(ii)+(iii) above, each of which I verified
against a primary text. Cite the three ingredients, not the `F`-notation, until someone
opens HSS.

## A.3 What is unconditional and what is conjectural — the honest split

For the **minimum support** (= minimum OA run size):

| statement | status |
|---|---|
| `N₀(k) ≥ 4⌈(k+1)/4⌉` | **unconditional** (Rao + divisibility) |
| `N₀(k) = 4⌈(k+1)/4⌉` for `k ≤ 663` | **unconditional** — Hadamard matrices are known for every order `4m ≤ 664` |
| `N₀(4λ−1) = 4λ` for all `λ` | **⟺ Hadamard conjecture** (HSS Thm 7.5) |
| `N₀(k) = 4⌈(k+1)/4⌉` for all `k` | **⟹ Hadamard conjecture** (restrict to `k ≡ 3 mod 4`) |

**Smallest open order of the Hadamard conjecture: 668 = 4 × 167.** Confirmed current as of
2025–2026: "Known constructions cover all multiples of four up to N = 664, but the existence
at N = 668 remains unresolved"; a Legendre pair of length 333 would yield it. Active 2026
work: arXiv:2607.20765 (*Multiplier obstructions for Legendre pairs of length 333*), and a
64-modular Hadamard matrix of order 668 (*Australas. J. Combin.* 93:422) giving modular but
not integer orthogonality.

Therefore, since `N₀(k) = 668` first at `k = 664` and the clean equivalence bites at
`k = 4·167 − 1`:

> **k = 667 is the smallest number of slots at which the value of the classical whole-only
> maximum is an open problem in combinatorics.** For `k = 664, 665, 666` the construction
> half likewise has no known witness (it would need an `OA(668, k, 2, 2)`); whether their
> failure would *imply* Hadamard(668)'s failure I did **not** verify — extension theorems
> for binary strength-2 arrays may or may not close that gap. Claim the equivalence only at
> `k ≡ 3 (mod 4)`.

## A.4 The entropy version — where our problem actually lives

Minimum *support* and minimum *entropy* are different problems, and the difference matters.
A distribution on 20 points can have entropy well below `ln 12`; `H ≤ ln|supp|` runs the
wrong way. So `min H = ln(min support)` needs a genuine lower-bound argument, and that
argument is exactly where the two-sided story lives.

The lower bound that does the work, in our own notation: with
`u_v = (1, χ₁(v), …, χ_k(v)) ∈ {±1}^{k+1}`, pair-uniformity says `Σ_v p_v u_v u_vᵀ = I_{k+1}`,
and taking `‖·‖²_F` gives `Σ_{v,w} p_v p_w ((k+1) − 2d(v,w))² = k+1`. **Dropping every
off-diagonal term** (all are ≥ 0) leaves `(k+1)² · c ≤ k+1` where `c = Σ_v p_v²`, i.e.

```
c ≤ 1/(k+1)   for every k,   hence   H ≥ −ln c ≥ ln(k+1).
```

That one-line bound is unconditional and is all that is needed at `k ≡ 3 (mod 4)`, where
`k+1 = N₀(k)` already. Equality forces `c = 1/(k+1)` *and* `p` uniform on its support, hence
support exactly `k+1`, hence an `OA(k+1, k, 2, 2)`, hence a Hadamard matrix of order `k+1`.

**This is Gavinsky–Pudlák Theorem 4.1. See §B.2 — it is not ours.**

Status of `min H = ln N₀(k)`, combining the above with `HAMMING_FORM_SCAN.md` §4–§5:

| k | proved? | by what |
|---|---|---|
| 2, 3, 7, 11, 15 (`k ≡ 3 mod 4`, plus k=2) | **yes**, unconditional | `c ≤ 1/(k+1)` + Hadamard construction — **in print** |
| 4, 5, 6 | **yes** | sibling's Lemma A (`c ≤ 1/8`) — **stronger than anything in print** |
| 9, 10, 13, 14 | **yes** | frame bound `c ≤ 1/(k+2)` etc. — **stronger than anything in print** |
| **8, 12** | **NO — open** | bound gives `ln 10`, `ln 14`; construction gives `ln 12`, `ln 16` |
| 667 | **NO — open**, and equivalent to Hadamard(668) | |

---

# (B) NOVELTY ADJUDICATION — **VERDICT: CONVERGENT**

I was told to assume our result is convergent until the primary text shows otherwise. The
primary text does not show otherwise. It shows worse: there are **two** independent prior
arts, and the stronger of the two states our headline as a theorem.

## B.1 The paper the coordinator flagged — Albanna et al. 2017: **PARTIAL threat, real**

*Minimum and Maximum Entropy Distributions for Binary Systems with Known Means and Pairwise
Correlations*, Badr F. Albanna, Christopher Hillar, Jascha Sohl-Dickstein, Michael R. DeWeese,
**Entropy 2017, 19(8), 427**; arXiv:1209.3744. MDPI HTML returned 403; I fetched the
publisher PDF from `mdpi-res.com` and extracted the full 33-page text with `pdftotext`.
**Read in full.**

Answering the three questions asked, exactly:

**(i) Does it solve the min-entropy problem for the pairwise-independent uniform case
specifically? — It ADDRESSES it, by name, and does not solve it.**

It is the same polytope: minimize `S(p) = −Σ pᵢ log₂ pᵢ` subject to normalization, means
`{µᵢ}` and pairwise correlations `{νᵢⱼ}`, `pᵢ ≥ 0` (§2.2.1, Eq. 10–11). Our case is
`µ = 1/2, ν = 1/4`, and **they derive that this is the unique case of interest**, Eqs (20)–(21):

> "In the special case ν = µ − 1/4, α vanishes allowing the bound in Equation (15) to scale
> logarithmically with N. … the only values of µ and ν satisfying Equation (20) are
> **µ = 1/2, ν = µ² = 1/4**."

Appendix F is titled, verbatim: "**Another Low Entropy Construction for the Communications
Regime, µ = 1/2 & ν = 1/4**". That is our case, singled out and named.

**(ii) Does it give `ln N₀(k)` or an equivalent? — NO. It gives a two-sided bracket with a
gap it never closes.**

- Lower bound, Eq. (15): `S̃₂ ≥ log₂(N² / (N + Σ_{i≠j} αᵢⱼ))`, `αᵢⱼ = (4νᵢⱼ − 2µᵢ − 2µⱼ + 1)²`.
  At `µ=1/2, ν=1/4` every `α = 0`, so this reads **`S̃₂ ≥ log₂ N`**.
- General upper bound, Eq. (14): `S̃₂ ≤ log₂(1 + N(N+1)/2) ≈ 2 log₂ N`.
- Explicit construction, Appendix F, Eq. (A70)–(A71): the Sylvester recursion on `2N` states,
  `S̃₂^con = log₂(2N)` for `N = 2^q`, extended as `S̃₂^con = ⌈log₂(2N)⌉ ≤ log₂(N) + 2`.

So they bracket the truth in `[log₂ N, ⌈log₂ 2N⌉]` — about one bit wide — and stop. They
explicitly decline to claim exactness (Appendix F, final paragraph, verbatim):

> "We remark that the authors of [31,34] provide a lower bound of Ω(N) for the sample size
> possible for a pairwise independent binary distribution, making the sample size of our
> novel construction **essentially optimal**."

"Essentially optimal" = optimal to within a constant factor. Their [31] is Chor–Goldreich–
Håstad–Friedman–Rudich–Smolensky, [34] is Alon–Babai–Itai 1986.

**And their construction is in fact suboptimal, exactly where our sibling's scan said the
Hamming form breaks.** Their `2N` states at `N = 8` is 16 runs; the Paley-12 array does it in
12. Their Sylvester family *is* the "Hamming form" that `HAMMING_FORM_SCAN.md` falsified at
`k = 8`. They did not notice, because the Ω(N) bound they leaned on is only asymptotic.

**(iii) Does it connect to orthogonal arrays / Hadamard? — It touches both and draws neither
conclusion.**

It cites Hedayat–Sloane–Stufken as reference [62] and "Hadamard matrix theory" in a survey
sentence (§2.6): "Several such designs are known and use tools from finite fields and linear
codes [33,34,60–62], combinatorial block designs [32,63], Hadamard matrix theory [42,64], and
linear programming [41]". And in Appendix F it identifies its own construction: "This is
sometimes referred to as a Hadamard matrix. Interestingly, this specific example goes back to
Sylvester in 1867 [22]". **No OA characterization of the minimizers, and no Hadamard
conjecture.**

**Convergence at the level of METHOD is nonetheless total, and must be conceded.** Their
Eq. (16) is our Lemma C:

> `S(p) ≥ − log₂ ‖p‖²₂`

and their Eqs (17)–(18) are our §5 frame bound in its crude form:

> `‖p‖²₂ ≤ ‖C‖²_F / N²`,  `‖C‖²_F = N + Σ_{i≠j}(4νᵢⱼ − 2µᵢ − 2µⱼ + 1)²`,  `C ≡ ⟨s sᵀ⟩`.

Their `C` is `N×N` (no constant row), so they get `c ≤ 1/N`; ours uses `u_v ∈ {±1}^{k+1}` and
gets `c ≤ 1/(k+1)`. **Our frame bound is theirs, plus the all-ones vector.**

Also convergent: their Eq. (13)/(A31) — minimum entropy is attained at a vertex by concavity,
support `≤ n_c` — is the same opening move as `CLASSICAL_MAX_K5.md` and
`HAMMING_FORM_SCAN.md` §1.

## B.2 The paper that actually decides it — Gavinsky & Pudlák 2016: **DIRECT HIT**

**Dmitry Gavinsky and Pavel Pudlák, *On the Joint Entropy of d-Wise-Independent Variables*,
arXiv:1503.08154v4 [cs.DM], 27 Oct 2016.** Full text extracted and **read in full**. This is
the prior art that settles the question, and it was not in the coordinator's brief.

From the abstract:

> "In particular, we **prove tight lower bounds for the min-entropy (as well as the entropy)
> of pairwise and three-wise independent balanced binary variables for infinitely many values
> of n.**"

From §1, verbatim — this is our headline, in print, with the Hadamard consequence drawn:

> "Furthermore, we prove a lower bound **log(n + 1)**, conjectured by Babai, on the min-entropy
> of pairwise independent balanced binary variables (i.e., when each X_j is equal to 0,
> respectively 1, with probability 1/2). This matches the upper bounds given by the well known
> construction based on Hadamard matrices. **So the bound is tight if an Hadamard matrix of
> dimension n + 1 exists.**"

The theorems:

- **Theorem 3.1** — Shannon entropy: `H[X] ≥ sup_{0<t≤n} log(n+1−t) / (1 + t⁻²Σ(1−2q_j)²/(q_j(1−q_j)))`.
  At `q_j = 1/2`, taking `t → 0`: **`H[X] ≥ log(n+1)`**. Text, §3.1: "If all q_j = 1/2 we get
  H[X] ≥ log(n + 1) by taking t → 0. This is tight for infinitely many values of n (see
  Section 4) and confirms **Conjecture 1.2 of Babai [Bab13]**."
  Its proof builds an `m × (n+1)` matrix `U` with `u_{i0} = √p_i` whose columns "form an
  orthonormal family" — **our frame identity, verbatim in substance.**
- **Theorem 3.2 / Corollary 3.3** — the stronger min-entropy (H_∞) version:
  `H_min[X] ≥ log(1 + nq/(1−q))`, giving at `q = 1/2` **`H_min[X] ≥ log(n+1)`**, "which is
  tight for infinitely many values of n." Since `H_min ≤ H`, this implies the Shannon bound.
- **Theorem 4.1** — **this is our (A), and it is theirs:**

  > "**Theorem 4.1.** The existence of n pairwise independent unbiased binary variables with
  > entropy equal to log(n + 1) is equivalent to the existence of an Hadamard matrix of
  > dimension n + 1."

  Their proof of the converse is our equality analysis, verbatim in substance: "According to
  Theorem 3.2, every point in the probability space has measure at most 1/(n+1). Since the
  entropy is log(n + 1), this implies that there are exactly n + 1 points, each with measure
  1/(n+1)."

And the ancestry runs further back — §4, verbatim:

> "Lancaster [Lan65] proved:
> 1. For every n ≥ 2, there exist at most n pairwise independent random variables on a
>    probability space with n + 1 points.
> 2. **The existence of such random variables where, additionally, each point in the
>    probability space has measure 1/(n+1) is equivalent to the existence of an Hadamard
>    matrix of dimension n + 1.**
> Our proofs of Theorems 3.1 and 3.2 can be viewed as an extension of an argument used by
> Lancaster to prove 2."

[Lan65] = **H. O. Lancaster, "Pairwise Statistical Independence", *Annals of Mathematical
Statistics* 36(4):1313–1317, 1965.** [Bab13] = **L. Babai, *Entropy Versus Pairwise
Independence* (preliminary version), 2013**, `people.cs.uchicago.edu/~laci/papers/13augEntropy.pdf`
(I could not fetch this — TLS certificate failure; **UNVERIFIED** except through Gavinsky–Pudlák's
quotation of Conjecture 1.2).

## B.3 On "min support is classical, but min entropy is ours" — that defence FAILS

The brief asked me to state clearly whether the step from min-support to min-entropy is in
print or is ours. **It is in print.** It is precisely Gavinsky–Pudlák Theorem 3.2 (max atom
`≤ 1/(n+1)`, from which uniformity at equality follows) composed with Theorem 4.1. The
distinction is a real one mathematically — `H ≤ ln|supp|` runs the wrong way, so min-entropy
does not follow from min-support — but it was drawn and closed a decade before us, by the
same argument we reconstructed.

Worth recording as a near-miss on our side: the sibling's **auxiliary conjecture (a)**,
"max atom `≤ 1/N₀(k)`", was tested and found **DEAD at k = 4** (max atom `= 1/6 > 1/8`). The
correct classical statement is Gavinsky–Pudlák Cor. 3.3, max atom `≤ 1/(k+1) = 1/5`, and
`1/6 < 1/5` — so our exact computation is *consistent with* their theorem and simply
overshot in conjecturing the sharper threshold. Our scan re-derived a true theorem's
neighbourhood and mislabelled the boundary.

## B.4 What survives as ours — narrow, real, and I verified it myself

Gavinsky–Pudlák's bound is `log(n+1)`, and they claim tightness only "for infinitely many
values of n" — meaning exactly `n ≡ 3 (mod 4)`, where `n+1` is a Hadamard order. **At the
other three residues their bound is not tight, and they do not give the value.** Their
Conclusions concede open ground but never claim these `n`.

I computed the gap directly (`scratchpad/temporal-share/` working script; independent of the
sibling's code):

| k | Gavinsky–Pudlák `log₂(k+1)` | truth `log₂ N₀(k)` | gap (bits) |
|---|---|---|---|
| 4 | 2.3219 | **3.0000** | 0.678 |
| 5 | 2.5850 | **3.0000** | 0.415 |
| 6 | 2.8074 | **3.0000** | 0.193 |
| 7 | 3.0000 | 3.0000 | 0 (theirs, tight) |
| 9 | 3.3219 | **3.5850** | 0.263 |
| 10 | 3.4594 | **3.5850** | 0.126 |
| 11 | 3.5850 | 3.5850 | 0 (theirs, tight) |
| 13, 14 | 3.8074, 3.9069 | **4.0000** | 0.193, 0.093 |

**Independently verified by me, not taken from the sibling's file:**

1. **`k = 4` minimum entropy is exactly 3 bits**, not `log₂5 = 2.3219`. Computed by 400
   random-objective LP vertex starts plus sequential-linearization descent on the exact
   pair-uniform polytope: `3.000000000` bits. So the sibling's Lemma A is a **genuine
   strengthening of a published theorem** at `k = 4`.
2. **The Paley-12 counterexample is real.** I rebuilt the Paley type-I Hadamard matrix of
   order 12 from quadratic residues mod 11, confirmed `H₁₂H₁₂ᵀ = 12·I`, normalized and
   deleted the first column, and checked pair-uniformity by direct combination counting:
   pair-uniform with **12 distinct rows for every k = 5…11**, in particular `k = 8`.
   (Sibling's result confirmed. Aside: at `k = 4` the same array collapses to 11 distinct
   rows, so it is not a `k=4` witness.)

**So the residue is:** the entropy floor rounds up to the *orthogonal-array divisibility*
bound `4⌈(k+1)/4⌉`, not merely to the *Rao* bound `k+1`. Proved by us at
`k ∈ {4, 5, 6, 9, 10, 13, 14}`; open at `k ≡ 0 (mod 4), k ≥ 8`. **I did not find this in
print** — not in Gavinsky–Pudlák, not in Albanna et al., not in the OA review
(arXiv:2505.15032), not in Beder–McComack. **Mark it "not found in print", not "new";
three passes is the house bar and this is one.**

## B.5 The credit line to add, exactly as worded

> The classical maximum is **not ours**. That the minimum entropy of `k` pairwise-independent
> unbiased bits is `log(k+1)`, and that it is attained exactly when a Hadamard matrix of order
> `k+1` exists, is **Gavinsky and Pudlák** (*On the Joint Entropy of d-Wise-Independent
> Variables*, arXiv:1503.08154, Theorems 3.1, 3.2 and 4.1, 2016), proving a conjecture of
> **Babai** (2013) and extending an argument of **Lancaster** (*Ann. Math. Statist.* 36:1313,
> 1965). The same polytope, the same Shannon-≥-Rényi-2 route, and our exact case (µ=1/2,
> ν=1/4) were independently set out by **Albanna, Hillar, Sohl-Dickstein and DeWeese**
> (*Entropy* 19(8):427, 2017, Eqs. 15–21), who bracket the answer without closing it. The
> orthogonal-array/Hadamard equivalence itself is **Hedayat, Sloane and Stufken** (*Orthogonal
> Arrays*, 1999, Theorem 7.5, p. 148). What we add is a sharpening at `k ≢ 3 (mod 4)`, from
> `log(k+1)` to `log(4⌈(k+1)/4⌉)` — not found in print, proved here at `k = 4, 5, 6, 9, 10,
> 13, 14`, open at `k ≡ 0 (mod 4), k ≥ 8`.

This is the same shape as the two credits the page already carries (the causal past-view
bound, arXiv:2505.13681; the classical multi-time share, Nakahara–Amari–Richmond and Marre
et al.). **Independent, convergent, theirs first in print.**

---

# (C) Orthogonal arrays on both sides of the ceiling

## C.1 The observation

The classical ceiling of the whole-only share on `k` slots is set by the *minimum* run size
of a strength-2 binary orthogonal array. The quantum ceiling — the existence of 2-uniform
(pairwise-maximally-mixed) states — is set by the *existence* of orthogonal arrays with an
extra irredundancy condition. **Both ceilings live in orthogonal-array theory, and both run
into Hadamard.**

The quantum half is already in print, and explicitly Hadamard-limited. Goyeneche &
Życzkowski, *Genuinely multipartite entangled states and orthogonal arrays*, **Phys. Rev. A
90, 022316 (2014)**, arXiv:1404.3586v2 — read in full from the PDF. Abstract, verbatim:

> "We establish a link between the combinatorial notion of orthogonal arrays and k–uniform
> states … In particular, known Hadamard matrices allow us to explicitly construct 2–uniform
> states for an arbitrary number of N > 5 qubits. **We show that finding a different class of
> 2–uniform states would imply the Hadamard conjecture, so the full classification of
> 2–uniform states seems to be currently out of reach.**"

§V, verbatim:

> "Precisely, the 2–uniform states of N = 4λ − 1 qubits connected with the Hadamard conjecture
> are those having r = 4λ terms (λ ∈ N). The Hadamard conjecture states that a κ × κ Hadamard
> matrix exists for κ = 2 and for every κ = 4n, n ∈ N. **It is open since 1893 and it
> represents one of the most important problems in combinatorics.**"

and:

> "the complete classification of 2–uniform states is currently out of reach, as it includes
> the Hadamard conjecture."

Note the exact mirroring: their obstructed case is `N = 4λ − 1` qubits with `r = 4λ` terms.
Ours is `k = 4λ − 1` slots with `N₀ = 4λ` support points. **Same λ, same 4λ, same Hadamard
matrix** — because in both cases the object being counted is the run set of an
`OA(4λ, 4λ−1, 2, 2)`.

## C.2 What this does and does not mean

**It does mean:**

- The counting problem behind the classical ceiling and the counting problem behind the
  quantum 2-uniform ceiling are *the same combinatorial object*, an `OA(4λ, 4λ−1, 2, 2)`,
  read two ways: as the support of a probability distribution, and as the term set of a state
  vector.
- Both are therefore hostage to the same 133-year-old open problem, at the same orders.
- Neither ceiling is "just" an information-theory fact. Where the whole-only share tops out
  is a question in design theory.

**It does NOT mean:**

- **It is not evidence that the classical and quantum shares are the same quantity.** They are
  not: `Core/ShareQuantum.lean` and the space-vs-time result on the page turn on their being
  different (space can exceed any classical bound; causally ordered time cannot). Two problems
  can share a combinatorial skeleton and have different answers.
- **It is not a new result on either side.** The quantum half is Goyeneche–Życzkowski 2014;
  the classical half is Gavinsky–Pudlák 2016 / Lancaster 1965. The *juxtaposition* is an
  observation, not a theorem, and must be labelled as one.
- **It carries no physics.** That a capacity is governed by Hadamard existence is a fact about
  the combinatorics of `±1` matrices, not about the world. It does not license any claim that
  nature "computes" orthogonal arrays, that the Logos is "made of" Hadamard matrices, or that
  the openness of the conjecture reflects any openness in physics. The temptation here is
  exactly the kind this repository's discipline exists to refuse.
- **It does not give a kill.** An observation about which mathematical problem our formula
  reduces to is not a claim about the world and therefore cannot enter the stance as one.

The honest one-line form, if it is ever wanted in prose: *"How much pattern a whole can hide
from all its pairs is, at k slots, a question about orthogonal arrays — and past k = 666 it is
an open question in combinatorics, the same one that limits the classification of pairwise-
maximally-mixed quantum states."*

---

# What to change on the page

**Nothing must change today, and nothing may be added without the §B.5 credit.**

1. **The published claim is safe.** The page's classical ceiling claim is the `k = 3` case
   only — "Three: one bit is the CEILING" in `precedent-is-bits`, witnessed by
   `temporal_third_saturates`. At `k = 3`: `N₀(3) = 4`, so the true maximum is
   `3·ln2 − ln4 = ln2` = one bit. **The page is exactly right, and `k = 3 ≡ 3 (mod 4)` is the
   λ = 1 Hadamard case, where a Hadamard matrix of order 4 unconditionally exists.** No row of
   the published stance rests on the Hadamard conjecture.

2. **No novelty is currently claimed for it, and none may be added.** The `precedent-is-bits`
   novelty note already withdraws the classical half ("We withdraw the classical half of that
   novelty note") and restricts the surviving claim to the *quantum* multi-time form. That
   restriction is correct and is *reinforced* by this scan. **If a general-`k` classical
   maximum ever goes on the page, it must carry the §B.5 credit line in the same breath.**

3. **One wording risk to watch.** The Lean cap `shareK_le_of_pair_uniform` proves
   `share ≤ (k−2)·ln2`. That is the true maximum *only at `k = 3`*; from `k = 4` on it
   over-states by at least `ln2`, and the true classical maximum is `k·ln2 − ln N₀(k)`. Any
   future page sentence generalizing "one bit is the ceiling" beyond three slots would be
   **wrong**, and would also be walking into published territory. Keep the ceiling language
   tied to the three-slot theorem.

4. **For the Lean queue, not the page.** `Core/HammingCap.lean` already carries the `k = 4`
   reproducing-kernel machinery for Lemma A. Worth knowing while that is built: **Lemma A is
   the part of the ladder that is not in print** (it beats Gavinsky–Pudlák's `log 5` at
   `k = 4` by 0.678 bits). The `k ≡ 3 (mod 4)` rungs, by contrast, would be mechanizing a
   known theorem — still worth doing, but it must not be announced as new.

---

## Sources, with what was actually read

| source | how read | what it established |
|---|---|---|
| Gavinsky & Pudlák, arXiv:1503.08154v4 | **full text, `pdftotext`** | Thms 3.1, 3.2, Cor 3.3, **Thm 4.1** — the decisive prior art |
| Albanna, Hillar, Sohl-Dickstein & DeWeese, *Entropy* 19(8):427 | **full 33-page text, `pdftotext` from mdpi-res.com** (MDPI HTML 403'd) | Eqs 14–21, App. B, F — convergent method, bounds not closed |
| Goyeneche & Życzkowski, PRA 90, 022316; arXiv:1404.3586v2 | **full text, `pdftotext`** | Thm 6 (=HSS 7.5), 2-uniform classification ⊇ Hadamard conjecture |
| Hedayat, Sloane & Stufken 1999, Thm 7.5 p. 148 | **quoted via two independent secondary sources** (Wikipedia raw wikitext; Goyeneche–Życzkowski §V) — book text not opened | OA(4λ,4λ−1,2,2) ⟺ Hadamard(4λ) |
| *Orthogonal Arrays: A Review*, arXiv:2505.15032 | fetched, searched | Rao bound §4.2; **no** `F(k,s,t)`, **no** Hadamard conjecture |
| Beder & McComack, arXiv:1508.06558 | abstract | divisibility `L_t` is elementary |
| Lancaster, *Ann. Math. Statist.* 36(4):1313, 1965 | **not opened** — quoted via Gavinsky–Pudlák §4 | n+1 points ⟺ Hadamard(n+1) |
| Babai, *Entropy Versus Pairwise Independence*, 2013 | **NOT VERIFIED** — TLS failure on uchicago.edu; known only via G–P's Conjecture 1.2 | the conjecture G–P proved |
| Hadamard order 668 status | search, 2025–2026 sources incl. arXiv:2607.20765 | smallest open order, all 4m ≤ 664 known |

**Own computation (this agent, independent of the sibling's scripts):** Paley-12 construction
and exact pair-uniformity check for `k = 2…11`; exact `k = 4` entropy minimization
(`3.000000000` bits); the Gavinsky–Pudlák-vs-`N₀` gap table.
