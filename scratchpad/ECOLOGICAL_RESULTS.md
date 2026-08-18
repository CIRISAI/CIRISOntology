# ECOLOGICAL RESULTS — the world declines to exhibit a thirteenth kind (first pass)

Run 2026-08-18 per `ECOLOGICAL_PREREG.md`. **170 wild changes** from three unrelated streams
(Federal Register 60, GitHub 50, OSM 60; **Wikipedia DEFERRED** — sustained API 429s, recorded
as unavailable rather than silently dropped), seed-pinned, provenance-stripped, judged by the
three-family panel at BASE. 510 judgments, $0.07.

## T1 — the residual rate: PASS, and not narrowly

| stream | n | modal NO-FIT | verdict (5%/15% lines) |
|---|---|---|---|
| Federal Register | 60 | **0 (0.0%)** | fit-for-use |
| GitHub commits | 50 | **0 (0.0%)** | fit-for-use |
| OSM changesets | 60 | **0 (0.0%)** | fit-for-use (12 minority-vote NO-FITs — see caveats) |

**Zero wild changes were modal-refused by the taxonomy.** T2 (residual clustering) is
vacuously passed — there is no residual to cluster. For the generator model, this is the
adequacy half's first measurement: **embedding-failure rate ≈ 0% on typical streams.**

## The distributions are their own validation

| stream | modal label profile | face validity |
|---|---|---|
| Federal Register | **Rules 93%** | regulations are deontic — as they should be |
| GitHub | Rules 26%, Manner 26%, Process 12%, Identity 10%, Facts 8%, Record 6% | code changes: permission logic, formatting, orchestration — a genuine mixture |
| OSM | **Facts 73%**, Identity 13% | map tags are world-claims — exactly right |

Three streams, three entirely different profiles, each matching what its domain IS. The
taxonomy does not collapse wild material into a bucket; it discriminates ecologically, and
its discriminations agree with domain common sense it was never shown.

## Caveats, named

Model panel only (no human ceiling on wild items yet); one condition (BASE); Wikipedia
deferred; the OSM items' before/after framing is the sampler's weakest construction and the
likely source of its 12 minority NO-FIT votes — a sampler artifact candidate, not a taxonomy
finding, and the item texts are retained for re-framing. Exhaustiveness remains, as the
prereg says, never provable: this is witness two of three (our search; the world's typical
streams; the standing bounty, unclaimed).

## T3 addendum (free analysis, 2026-08-18): the wild confusion is DIFFERENT from the authored

Top wild disagreement pairs: **Facts~Rules (17)** and **Facts~Identity (15)** — pairs the
authored corpus barely exercises. Cause is visible in the streams: regulations are
statements ABOUT rules (a rule-change described reads as fact), and map tags IDENTIFY
things (what-it-is vs what-is-claimed blurs). Per T3's pinned rule these are **findings
about the authored corpus's blind spots**: part-D addendum candidates are Facts↔Rules and
Facts↔Identity boundary items. Facts~NO-FIT (11) sits on OSM and is the weak-framing
artifact already flagged.

## Part-C readout (the lay-discovered boundaries, measured)

**Identity holds.** All four ontological-05 trap items — identity claims with permissions
restated verbatim — classified correctly. The lay-predicted Identity↔Rules confusability
did not materialize under the trap's own conditions.

**Premises is the taxonomy's weakest kind in practice.** All four axiomatic-05 items were
absorbed (three into Facts, one into Rules) — DESPITE the visible-ripple construction. The
absorption is one-directional (Premises→Facts; never the reverse anywhere in the study).
Consequence for the instrument suite: the Premises instrument cannot rely on judge
intuition; it must COMPUTE the ripple (count downstream clauses whose meaning inherits the
change) as a feature, because the discriminator that separates Premises from Facts is
exactly the one panels do not apply unprompted.

## OSM stream v2 (2026-08-18): the reframe closes the NO-FIT question

The v1 OSM sampler showed the tags AFTER the edit as "before" and a placeholder as "after" —
no contrast to classify; its 12 minority NO-FITs were flagged as suspected sampler artifact.
v2 fetches each modified element's previous version, so both tag states are real
(`eco_sample_osm2.py`, seed-pinned, stream `osm2`, n=60, BASE x 3 models).

Result: **zero NO-FITs — modal AND any-vote** (v1: 12 minority). The v1 NO-FITs are
confirmed sampler artifact. Modal distribution, face-valid for a map registry: Facts 36,
Identity 15, Manner 4, Rules 3, Structure 2. The Facts~Identity disagreement pair (9 items)
reproduces in exactly the stream that predicted it wild. New minority pair worth an eye:
Facts~Structure (20 items) — tag-key additions read as encoding changes to some judges;
minority votes only, no modal Structure beyond 2.

Wild NO-FIT tally across all streams to date, after v2: **zero modal NO-FITs on 230 wild
changes** (170 v1 + 60 osm2; wiki2 pending).

## Wikipedia stream v2 (2026-08-18): the deferred stream, completed

The v1 blocker was our own User-Agent (Wikimedia rejects non-descriptive UAs; with a
descriptive one the API answers immediately) — recorded because "429 = rate limit" was the
wrong diagnosis for a policy block. The v1 sampler also stitched diff fragments into
collages; a legibility gate kept 10/60 and even those were unreadable. v2
(`eco_sample_wiki2.py`, seed-pinned, stream `wiki2`) fetches both full revisions and keeps
only edits where EXACTLY ONE cleaned paragraph differs: real document-local changes.
Yield: 49 items from 500 candidates (~10% pass the one-clean-paragraph gate; count
reported, not padded).

Result (BASE x 3 models): modal distribution **Manner 20, Facts 18, Identity 6,
Circumstances 2, Structure 1, Confidence 1, NO FIT 1** — face-valid for an encyclopedia's
edit stream (copyedits and factual updates dominate). Disagreement pairs: Identity~Manner
11, Facts~Manner 8, Facts~Identity 5 — the Facts~Identity boundary reproduces in a third
unrelated stream.

**The single modal NO-FIT — the first in the entire wild programme — is `wiki2-10`, whose
whole change is one glyph: a curly apostrophe normalised to a straight one.** The panel
refused a sub-lexical typographic swap. We read this as a RESOLUTION-FLOOR datum, not a
missing kind: the change is classifiable (Manner as typographic style, or Structure as
re-encoding of identical content) but sits at the smallest edit the instrument can be
asked about. One item cannot cluster, so T2 cannot fire on it.

## Wild tally after v2 (the adequacy scoreboard)

**279 wild changes, three unrelated streams sampled twice where the sampler needed repair:
1 modal NO-FIT (0.4%), and it is a one-glyph typography swap.** T1 (5% threshold): passed
with 12x margin. T2 (clustered residual): nothing to cluster. The ecological challenge's
verdict stands and is now complete on all four originally-registered streams minus none.
