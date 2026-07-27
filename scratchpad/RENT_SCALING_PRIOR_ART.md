# PRIOR ART — Q1's objects already have names, and one of them is classified

Required by `RENT_SCALING_PREREG.md` §5.2, which committed to running this sweep **before the
results are written** and to reporting whatever it found "whether or not it pre-empts H-IFF".
Written while the Q1 measurement was still running, so nothing here is chosen to fit a result.

Searched **by mathematical object**, per the standing rule that every findable result in this
programme has already been in print. The objects were named first, then searched:

| our name | the object | what to search |
|---|---|---|
| the support `S` | rows of a normalised Hadamard matrix, truncated to `k` columns; at `k = N−1` the **shortened Hadamard code** of length `N−1`, size `N` | Hadamard codes, rank and kernel |
| `Iso(S) = {(σ,c) : σ(S) ⊕ c = S}` | the isometry group of the Hamming space stabilising the code | code automorphism group |
| **transitive** (our H-IFF) | `Iso(S)` transitive on the codewords | **transitive code** |
| `\|C\|` = orbit of the zero word | index of the stabiliser of a codeword | orbit–stabiliser on codes |
| **restorable** (G7: `R_i(a)` `i`-independent) | the nearest-point decoder's cells all present the same distance profile to `S` | completely regular, uniformly packed, distance invariant |

---

## 1. What the literature already has

**(A) "Transitive code" is a standard, named property, and it is exactly our H-IFF side.**
A code is *transitive* if its automorphism group — the isometry group of the Hamming space
stabilising it — acts transitively on its codewords; if some subgroup acts *regularly* it is
*propelinear* (Rifà–Pujol). The inclusion is strict and there is a named witness: the **Best
code** (length 10, size 40, `d = 4`) is transitive but not propelinear. So the property this
campaign computes is not new, is not ours, and has an established name. **Our contribution on
this side is a computation, not a concept.**

**(B) The regularity/transitivity gap is a known, and known-strict, phenomenon.**
*Completely regular* codes were introduced by **Delsarte (1973)**; *completely transitive*
codes by **Solé (1990)**, as the subfamily whose automorphism group is transitive on every
part of the distance partition. Completely transitive ⟹ completely regular, and the converse
is false — complete transitivity is a *proper* subfamily. This is the exact shape of H-IFF's
necessity direction (`regularity ⟹ symmetry`) in the neighbouring setting, and there it is
known to fail.

**This does not settle H-IFF**, and saying so is not a hedge — the two conditions genuinely
differ:

* complete regularity constrains the *outer distribution* on every distance class of the whole
  space; our restorability constrains only the *decode-cell-weighted* distance profile, one
  statistic per support point;
* complete transitivity demands transitivity on *every* distance class; our transitivity
  demands it only on `S` itself.

So H-IFF is a different statement about neighbouring objects. What the literature supplies is
the **prior**, and it points at failure — which is exactly what the prereg §2.2 staked in
advance ("a bet against a well-populated prior… a falsification is the expected outcome under
the prior"). That sentence was written before this sweep and is confirmed by it.

**(C) The `k = 11` object is CLASSIFIED, and the classification matches our numbers.**
Gillespie & Praeger, *Uniqueness of certain completely regular Hadamard codes*
(arXiv:1112.1247, 2011; J. Combin. Theory Ser. A, 2013), classify binary completely regular
codes with `(m, δ) = (12, 6)` and `(11, 5)`: they are **unique up to equivalence**, equivalent
to certain Hadamard codes, their automorphism groups modulo the kernel of a particular action
are **isomorphic to certain Mathieu groups**, and consequently such codes are **necessarily
completely transitive**.

That is our Paley-12 substrate. The programme's own record already reproduces the group
side of it independently: `aut_counts_exact.json` gives orders **7920, 720, 144, 48** at
`k = 11, 10, 9, 8`, the Mathieu stabiliser chain, one point stabiliser per deleted column.
**So the single most striking group-theoretic fact in the rent-islands record is a published
classification, and the campaign should say so rather than present it as a discovery.**

**(D) The kernel of a binary Hadamard code is a published invariant.**
Phelps, Rifà & Villanueva, *Rank and kernel of binary Hadamard codes*, IEEE Trans. Inform.
Theory **51**(11):3931–3937 (2005), and the `Z₂Z₄`-linear line that follows it (Krotov &
Villanueva, arXiv:1408.1147, which computes the **orders of the monomial and permutation
automorphism groups** of the `Z₂Z₄`-linear Hadamard codes). **Note the distinction, because it
is easy to get wrong and this file exists partly to stop it:** the *kernel* is
`K(S) = {c : S ⊕ c = S}` — translations alone. Our `|C|` is the **orbit of the zero word under
the full isometry group**, `{c : ∃σ, σ(S) = S ⊕ c}`, which permits a permutation and is
therefore **≥ |K(S)|**. They coincide only when the stabiliser adds nothing. Our `|Aut| = |P|·|C|`
is orbit–stabiliser and is correct as written; it is simply **not** the published kernel, and
no number of ours should be compared to a published kernel dimension without that correction.

---

## 2. Adjudication — what is pre-empted and what is not

| item | verdict |
|---|---|
| the concept "transitive code" | **fully pre-empted** (Rifà–Pujol). Not claimed |
| the concept "completely regular / completely transitive", and the strictness of the inclusion | **fully pre-empted** (Delsarte 1973, Solé 1990). Not claimed |
| `Aut` of the length-12 Hadamard code ≅ Mathieu, and its complete transitivity | **fully pre-empted** (Gillespie–Praeger 2011/13). The Mathieu chain in `aut_counts_exact.json` is a **reproduction**, and must be labelled one |
| rank/kernel of binary Hadamard codes as classified invariants | **fully pre-empted** (Phelps–Rifà–Villanueva 2005) |
| the elementary observation `R_i(a)` is constant on `Aut(S)`-orbits | elementary; the prereg §2.1 already calls it "not a discovery". Confirmed as such |
| **the restorability criterion itself** — "the nearest-point decoder with uniform tie-breaking fixes the uniform measure on `S` for every radial kernel iff `R_i(a)` is `i`-independent" | **NOT FOUND under this description.** Nearest named relatives are complete regularity, uniform packing, and distance invariance, and it is none of them. Recorded as *not found*, which is weaker than *new* — the search was one afternoon over four query families, not a literature review |
| **H-IFF as a statement** (restorable ⟺ transitive, for these supports) | **NOT FOUND**, and the prior from (B) says the necessity half should fail |

**What this changes about how Q1 must be reported.** Two things, both binding:

1. Any confirmation of H-IFF is a **numerically verified equivalence on a finite roster**, in a
   setting where the analogous general statement is known false. It cannot be written up as
   "the boundary is algebraic" without that sentence attached.
2. The Mathieu chain must be reported as **convergent with a published classification**, with
   the credit in the text and not in a footnote. It is the campaign's strongest-looking
   group-theoretic result and it is somebody else's theorem.

---

## 3. Method and limits of this sweep

Four query families, all run 2026-07-27: (i) completely regular vs completely transitive,
counterexamples; (ii) Hadamard codes — rank, kernel, propelinear, transitive; (iii) transitive
vs distance-invariant, named strictness examples; (iv) Hadamard codes of length 12/20/24/28 and
their automorphism groups. Abstracts fetched and quoted; the survey PDF (arXiv:1703.08684,
*On Completely Regular Codes*) **failed to extract** and its contents are therefore **not**
relied on here — it is cited as a pointer for whoever does the deeper pass, not as a source.

**This is a targeted sweep, not a literature review, and its negative results are weak.**
"Not found" above means four query families did not surface it. The specific gap most likely
to hide a pre-emption is the Voronoi-cell / uniformly-packed literature around Delsarte's
outer distribution, which the failed PDF would have covered.

## Sources

- [Uniqueness of certain completely regular Hadamard codes — Gillespie & Praeger (arXiv:1112.1247)](https://arxiv.org/abs/1112.1247)
- [Classification of the Z2Z4-linear Hadamard codes and their automorphism groups — Krotov & Villanueva (arXiv:1408.1147)](https://arxiv.org/abs/1408.1147)
- [Rank and Kernel of Binary Hadamard Codes — Phelps, Rifà, Villanueva (IEEE T-IT 51(11), 2005)](https://www.researchgate.net/publication/3085615_Rank_and_Kernel_of_Binary_Hadamard_Codes)
- [On Completely Regular Codes — survey (arXiv:1703.08684)](https://arxiv.org/pdf/1703.08684) — *pointer only; extraction failed, not relied on*
- [Classification of a family of completely transitive codes (arXiv:1208.0393)](https://arxiv.org/pdf/1208.0393)
- [On the classification of binary completely transitive codes with almost-simple top-group (arXiv:2012.08436)](https://arxiv.org/pdf/2012.08436)
- [Completely Regular Codes in Distance Regular Graphs — Shi & Solé (book)](https://www.routledge.com/Completely-Regular-Codes-in-Distance-Regular-Graphs/Shi-Sole/p/book/9781032494449)
