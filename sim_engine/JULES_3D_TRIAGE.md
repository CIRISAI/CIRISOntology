# JULES_3D_TRIAGE — the external 2D→3D conversion of `holon-sandbox`

Date: 2026-08-23. Branch: `salvage/jules-3d`, against `main` at **b510a68**.
Scope: triage and salvage only. **Nothing here lands on `main`.** This branch is a parts
shelf; `MESH_DESIGN.md` §7 sequences the 2D bit-identity gate before any 3D chart, and
that sequencing is not renegotiated by a salvage lane.

**Provenance, and it is not uniform.** Two kinds of statement appear below and they are
labelled everywhere they occur:

* **VERIFIED** — read out of this repository at b510a68, with the file and line. Anyone
  can re-run it.
* **REPORTED** — Jules' own account of its work, relayed through the lead. **No diff was
  available to this lane** (see §0), so every verdict that depends on hunk detail is
  provisional on arrival and says so.

---

## 0. Arrival: nothing has arrived

VERIFIED, 2026-08-23:

```
git fetch origin && git log --oneline -1 origin/main   → b510a68 (clean)
gh pr list --state open --json number,title,headRefName
    → [{"number":6,"headRefName":"research/dark-state-sim-sota", ...}]   (unrelated draft)
git branch -a --list '*jules*' '*3d*' '*3D*'
    → salvage/jules-3d                                   (this branch, and only this branch)
```

No Jules branch, no Jules PR, no Jules commit reachable from this tree. **Hunk-level
triage is pending arrival.** What follows classifies the deltas Jules described, against
what `main` and `MESH_DESIGN.md` actually contain — which is enough to decide every
verdict except the ones marked *provisional*.

---

## 1. Verdict

**Almost none of it survives, and the reason is the base, not the craft.** Jules forked
before today's holon-sandbox work and did a competent mechanical dimension lift of a tree
that no longer exists. Of the five files it touched: two (`sim.rs`, most of `scene.rs`)
are superseded by work that landed today and would be *destroyed* by applying its diff;
one (`chart.rs`) has a real shape worth keeping, and it is kept here re-implemented rather
than applied; one (`lib.rs`) contributed a hazard worth gating rather than a change worth
taking; and the renderer is deferred on a design question that is not Jules' to answer and
not mine.

The one-line charge: **the conversion is geometrically 3D and frame-blind.** It moves the
chart into three dimensions without touching the ledger, the acuity claim, or the
certificate — and in 3D the acuity claim is the whole of why 3D is affordable
(`MESH_DESIGN.md` §0: 146×, and it is a claim property, not a capacity one).

**But two of the charges in my brief do not survive checking, and are withdrawn below**
(§6, F4 and F5): rebuilding the wasm was *correct*, and the sandbox scene's ledger cap
does *not* need re-deriving for 3D. Both are the design's own words.

---

## 2. The stale base, measured

VERIFIED — commits on `holon-sandbox` that Jules forked before, newest first:

| commit | what it changed | what a naive apply destroys |
|---|---|---|
| `ff27476` | momentum maxima enumerated; a dead-code warning was a correctness hole | `refresh_pairs` (`sim.rs:1597`) |
| `2c01703` | the Sandbox tab joins the published page | the shipped `viewer/` contract |
| `bcc393e` | never coarsen; acuity pin; ~118k resident; working-set substeps; incremental awake sets | `refresh_awake` (`sim.rs:603`), `Nodes::awake/still` |
| `f617ff0` | the landscape impulse counted force that cancels | net-vs-total impulse |
| `18a9a55` | the suite fails under the default runner; CI never ran it | the world-lock test discipline |

`refresh_pairs` is the sharpest of these and it is worth stating in full, because it is
the one no gate catches. Its own doc comment (`sim.rs:1592`) records that restructuring
the substep around working sets left it orphaned, "the compiler reported it as dead code,
which read like tidy-up and was actually a correctness hole: the pair list would have been
built once per throw and never refreshed". A diff that reverts `sim.rs` to a pre-`ff27476`
shape re-opens exactly that hole, and **every test still passes when it is open** — the
contacts that go missing are the ones formed by cells that have moved, and nothing asserts
they exist.

---

## 3. Per-file triage

Verdicts: **(a) SALVAGEABLE** · **(b) SUPERSEDED** · **(c) WRONG-BY-DESIGN** · **(d) JUNK**.

### 3.1 `src/chart.rs` — the one file with real salvage

| delta (REPORTED) | verdict | reason |
|---|---|---|
| `FANOUT` 4 → 8 | **(a)** — shape taken, value not | `MESH_DESIGN` §2.4 asks for exactly this. Taken as `DIMS = 2` + `FANOUT = 1 << DIMS`, so the flip is one constant. The value stays 2: §7 sequences 2D first. |
| ordinal → octant map | **(a)** — taken | Re-implemented as bit indexing: bit 0 = x, bit 1 = y, bit 2 = z. That is §2.4's `(ordinal % 2, (ordinal / 2) % 2, ordinal / 4)` written so the third axis is a bit nobody reads yet. |
| `Cell` gains `z0` | **(a)** — deferred, not blocked | Ripples into `centre() -> [f64; 2]`, `distance_to([f64; 2])`, and `ResolutionModel::focus`. One-line each, but they cross into `sim.rs`, which is (b) — so the geometry flip wants to land *after* the mesh's 2D gate, not before it. |
| `apportion` / `apportion_exact` | **(c) if touched at all** | VERIFIED dimension-blind, and §2.4 says so independently. `fraction_below` is `(y − y0)/size`: the area fraction of a square below a horizontal line and the *volume* fraction of a cube below a horizontal plane are the same number. Any edit here is a regression. **Provisional** — Jules may not have touched it. |
| `children_seen: Vec<u8>` | fits — now checked | 8 < 255. Was true and remembered; is now a `const` assert against `FANOUT`. |

**On "detects rather than assumes contiguity":** `main` is already the safe form.
`Chart::sync` derives the ordinal from a **per-parent running child count**
(`chart.rs:96`), not from `id − first_child_id`, so it does not assume children are
contiguous in arena order — only that a parent's children arrive in the order the
generator emitted them, which `RuntimeArena::materialize` guarantees by appending the
spec slice. If Jules' octree indexes by id arithmetic, its version is the *weaker* one and
must not be taken. **Provisional on arrival.** The invariant is now a gate either way
(`scene::tests::the_chart_places_a_child_where_the_generator_apportioned_it`).

### 3.2 `src/scene.rs` — one salvageable hunk, one blocked, one design trap

| delta (REPORTED) | verdict | reason |
|---|---|---|
| 8-octant `materialize` | **(a)** — taken, as deduplication | VERIFIED: `main` carried a **second copy** of the child map, open-coded at `scene.rs:119-125`. `MESH_DESIGN` §2.4 names `chart.rs` and does not name this. See §5/F1. |
| `GrossState::aggregate(…, [0, 0])` | **(c) BLOCKED — do not decide** | Momentum arity is **M-G1**, a coordinated core commit reserved to the lead (§8, §9). Nothing in this crate may move it. |
| the acuity claim, untouched | **(c) — the load-bearing one** | See below. |

**The acuity trap, and it is the whole frame-blindness charge in one number.**
`ResolutionModel::allowed_spacing` (`scene.rs:235`) returns the observer's acuity for
*every* cell holding matter, with no notion of visibility. In 2D that is right and cheap.
Lift it mechanically to an octree and it refines the **volume** to acuity — which
`MESH_DESIGN` §0 prices, VERIFIED against that table:

| 3D scene at 0.6 m / 0.5 mm | nodes | at 144 B | |
|---|---:|---:|---|
| every cell at acuity (512³) | 1.534e8 | 22.1 GB | refused, 1.32× over the card |
| matter only, fill 0.45 | 6.90e7 | 9.94 GB | fits, and renders 1.2 mm detail through opaque sand |
| **visible surface only (3 faces)** | **1.049e6** | **151 MB** | **0.9% of the card** |

A mechanically converted acuity claim asks for the first or second row. The design's whole
affordability argument is the third. **This is the thing a dimension lift cannot produce**,
because it is not a geometry change — it is the observation that in 3D the observer's claim
is a claim about a 2-manifold. No amount of `[x,y]` → `[x,y,z]` gets there.

Deliberately *not* claimed here: what the 3D resident set actually costs. `MESH_DESIGN`
§3 marks it **PENDING** (M-G2) and records that geometric extrapolation of residency was
wrong by five orders of magnitude on this exact quantity once already. It is not
extrapolated again in this document.

### 3.3 `src/sim.rs` — superseded, and broken by Jules' own account

| delta (REPORTED) | verdict | reason |
|---|---|---|
| substep / awake-set / pair machinery | **(b) SUPERSEDED, hard** | `refresh_pairs`, `refresh_awake`, working-set substeps, net-vs-total impulse all landed today (§2). A naive apply reverts them and the suite still passes. |
| 3D positions, velocities, distances | **(b)** — redo, do not apply | Mechanical, and mechanical against the wrong tree is worth less than mechanical against the right one. |
| `Broadphase::pairs` — "lacks Z constraints and rest boundaries" | **(b) + broken by admission** | Jules says it is broken; it is also superseded. Not salvaged. |

**Three concrete 3D hazards in `Broadphase`, recorded so whoever writes the real one does
not re-find them** (VERIFIED against `sim.rs:238-388`):

1. **The neighbour stencil is not a dimension parameter.** `pairs()` walks four half
   neighbours `[(0,1), (1,−1), (1,0), (1,1)]` — half of the eight 2D neighbours, so each
   bucket pair is visited once. In 3D that is **thirteen** of twenty-six. A converted loop
   that keeps four silently misses two thirds of the cross-bucket pairs, and no test in the
   crate would fail. This is very likely what "lacks Z constraints" is.
2. **The 512 clamp becomes an allocation.** `columns` is `clamp(1, 512)` and buckets are
   `columns × rows`; at 512 that is 2.6e5 buckets. Cubed it is **1.34e8 buckets**, and
   `counts`, `starts` and the `cursor` clone of `starts` are each a `Vec<u32>` of
   `buckets + 1` — **about 1.6 GB of index arrays before a single node is placed.** The
   clamp must be re-derived in 3D, not carried.
3. **The oversized set is `O(N)` per member.** `pairs()` pairs each oversized node against
   every node. On a graded quadtree the sizes are geometric and the set stays small
   (`sim.rs:246`); whether that survives an octree's grading is **unmeasured**, and it is
   the term that turns quadratic first.

### 3.4 `src/lib.rs` — a hazard worth gating, not a change worth taking

| delta (REPORTED) | verdict | reason |
|---|---|---|
| `NODE_STRIDE` 5 → 6 (`x,y,z,radius,anchored,speed`) | **(a)** — shape right, number not ours | `main` is 2D. |
| `BOND_STRIDE` 5 → 7 (`ax,ay,az,bx,by,bz,damage`) | **(a)** — same | |
| the `viewer/app.js` half of the same change | **(a)** — **the salvage is the gate** | VERIFIED: the stride is declared twice — `lib.rs:33,35` and `viewer/app.js:58,59` — and nothing held them together. |

That duplication is the one cross-boundary constant whose disagreement is **silent**: the
buffer stays well-formed, every read is a float in range, no length check fails, and the
page draws radius as a position. The crate's existing
`the_frame_buffers_are_packed_at_their_declared_stride` gates the Rust side against itself
— the half that does not move. The missing half is now gated and mutation-tested (§7).

### 3.5 `viewer/app.js` — the renderer, deferred with reasons

**(a) in principle, DEFERRED in practice, and not written on this branch.** Three reasons,
in order of weight:

1. **It presumes the volume is resident.** A depth-sorted painter over every published
   node is a renderer for the 6.9e7-node row of §3.2's table. What the engine publishes in
   3D is the surface-claim question `MESH_DESIGN` §3 marks **PENDING** — a design decision
   this lane does not hold. Writing the renderer first would quietly answer it.
2. **There is nothing to render.** The engine publishes `[x, y]`. A 3D projection on this
   branch is untestable dead code in a language the crate's test harness cannot reach
   except as a string.
3. **Painter's algorithm fights a cache that already works.** `drawStillLayer`
   (`app.js:443`) caches the resting scene and rebuilds only when `ciris_sleep_generation`
   moves — which is what makes ~118k resident cells affordable to draw. A depth sort of the
   still set can ride the same key; a depth sort of the live set is `O(n log n)` **per
   frame**. That is a real cost to design against, not a stopgap.

**The reusable residue, recorded rather than discarded:** 30° isometric projection, depth
key monotone in `x + y + z`, painter order back-to-front, and the constraint that the
still-layer cache must survive the change. That is the useful part of Jules' renderer and
it fits in one sentence, which is the honest measure of it.

### 3.6 Process artifacts

| artifact (REPORTED) | verdict |
|---|---|
| `output.log`, `check_tests.log`, `test_workspace.log`, `verify_workspace*.log`, `test_mutation.log` | **(d) JUNK.** VERIFIED: no `.log` is tracked under `sim_engine/crates/`. |
| the lost commit | **(d)** — process debris, nothing to salvage |
| the rebuilt wasm binary | **NOT junk — see §6/F4. Rebuilding it was correct.** |

---

## 4. What Jules got right

A stale-base mechanical conversion is not worthless, and this one is not. It found the
touch-points for 3D by the only method that cannot miss one — trying to compile it — and
its list is **almost exactly right about geometry**: `chart.rs`, `scene.rs`'s generator,
the solver's vectors, the render stride, and the viewer's parsing are, in fact, the five
places the third dimension shows up in this crate, and it got the stride *shapes* right in
both buffers (6 and 7 are the correct widths) without being told them. It reported its own
breakage plainly rather than shipping a green-looking `Broadphase`, which is more than the
crate's own tests would have caught. And it surfaced one defect in `main` that had nothing
to do with 3D and had been sitting there unnoticed: the child map was written out twice,
in two files, with nothing checking the two agreed — a conversion has to edit both, which
is how the duplicate became visible at all. That finding is now a gate, and it would not
have been found this week without it.

---

## 5. Touch points: Jules' list against `MESH_DESIGN`'s

The comparison is itself the useful artifact, because the two lists disagree in both
directions and each disagreement is a finding.

| touch point | Jules | `MESH_DESIGN` | reading |
|---|---|---|---|
| `chart.rs` octree | yes | yes (§2.4) | agree |
| **`scene.rs`'s copy of the child map** | yes | **no** | **F1 — the design's §2.4 undercounts by one file.** Fixed on this branch. |
| `sim.rs` solver vectors | yes | not named | agree by omission: the design sequences the mesh gate on the 2D scene (§7), so the solver's dimension lift is deliberately later |
| render stride + viewer | yes | not named | the design is a mesh document and does not cover the exhibit; the stride hazard (§3.4) is real and was unowned |
| **`GrossState` momentum arity** | **no** | yes — **M-G1**, §2.2/§9 | the frame-blindness, precisely located: geometrically 3D, ledger untouched |
| **FCHC-24 direction table** | **no** | yes (§2.1) | the chart's *warrant*. D3Q6 is four times cheaper and drops fourth-rank isotropy silently |
| **acuity → visible surface** | **no** | yes (§0) | the affordability argument (§3.2) |
| **ledger cap re-derivation** | **no** | yes (§2.3) | **but see F5 — not for this scene** |
| certificate / re-root adaptation | no | §1, single-tier fence | untouched by either; still owed |

---

## 6. Findings about `main`, turned up by this triage

Five, three of which are corrections to documents rather than to code. **None is fixed
here** — `tier.rs` and `MESH_DESIGN.md` belong to lanes that are mid-edit, and this is a
salvage branch.

**F1 — `MESH_DESIGN` §2.4 names one file where the change is two.** VERIFIED: the child
map was open-coded in `scene.rs:119-125` as well as `chart.rs:102-106`, and nothing checked
that the two agreed. One apportions the REG+ ledger between children; the other places the
cell that ledger is drawn in. Fixed on this branch, with the gate.

**F2 — `MESH_DESIGN` §8's M-G4 is stale: it was closed on `main` at `ff27476`.**
VERIFIED: `tier.rs:228-231` now reads `REG_PLUS_MAX = { occupancy: 6, momentum: 2 }`,
with a SUPERSEDES note crediting the FCHC enumeration in `MESH_DESIGN` M-G4 for catching
it, and a test that derives both from the shipped lattice. The design still lists it as
"relayed, not mine".
**F2b — and the file now contradicts itself.** `tier.rs:199`'s doc comment still says the
REG+ maximum is "3 for either momentum component", thirty-one lines above the constant
that says 2 and explains why 3 was wrong. One stale prose line; the sandbox lane's to fix.

**F3 — `MESH_DESIGN` §9.1 undercounts `holon-sandbox`'s share of the M-G1 arity flip.**
It records "`tier.rs`, 2 sites". VERIFIED actual: four `GrossState::aggregate` construction
sites (`scene.rs:139`, `scene.rs:607`, `incremental.rs:996`, `incremental.rs:1018`) and two
momentum-literal assertions (`scene.rs:751`, `scene.rs:767`), on top of `tier.rs`'s two.
§9.3's zero-extending constructor covers the construction sites by design; the two
assertions are test-side and need the same treatment. **A count correction, not a plan
defect** — and §9.2's argument that the compiler is the instrument still holds, because
every one of these is an explicit array literal.

**F4 — the brief's "rebuilt the wasm into its diffs" charge is withdrawn: that is
required here.** VERIFIED: `viewer/holon_sandbox.wasm` **is tracked**
(`git ls-files` finds it; only `holon-ball-game`'s is gitignored), and `pages.yml:65-66`
copies `viewer/` verbatim with no Rust toolchain in CD. Any Rust change that ships must
rebuild it via `build-web.sh`. Jules was right and the process charge was wrong.

**F5 — and "no cap re-derivation" does not apply to this scene.** VERIFIED against
`MESH_DESIGN` §2.3 point 2: the **geometric** cap of 3.54 grains is dimension-independent,
because the `constituents` lane does not know what a direction is. The 0.59 → **0.1475**
tightening is the **REG+ FCHC-24** cap, and the sandbox's chart writes neither occupancy
nor momentum — gated by `scene::tests::the_sandbox_chart_writes_no_occupancy`. So *"the
shipping sandbox scene's cap is unchanged by going 3D"*, in the design's own words. The
charge is correct against a general 3D claim and incorrect against this crate.

**F6 — the committed wasm is not what `main`'s source builds, and CI does not check that
it is.** VERIFIED, and this one is about the published page rather than about Jules:

| | sha256 | bytes |
|---|---|---:|
| committed `viewer/holon_sandbox.wasm` | `b5a2c2fd…` | 139,993 |
| rebuilt from b510a68 with `build-web.sh`'s profile, rustc 1.95.0 | `78c17819…` | 139,490 |

The rebuild is **reproducible**: byte-identical from two different build paths
(`/home/emoore/CIRISOntology` and a `/tmp` worktree) and two different target dirs. The
committed binary was last written at `ff27476`, the same commit as the last source change,
and `ciris-sim-core` has not moved since (`git log ff27476..b510a68 -- crates/ciris-sim-core`
is empty) — so this is not source drift under it. Either the toolchain differs from
whoever last ran `build-web.sh`, or the binary was built before the source it was committed
alongside.

`pages.yml:63-64` states the invariant as *"the wasm is committed, and ci-gates verifies it
builds and passes on every push, so what ships is what was gated."* **The second clause
does not follow from the first.** `ci-gates.sh:59` builds the source for
`wasm32-unknown-unknown`; nothing anywhere compares the built artifact to the committed
one. A 503-byte counterexample is sitting in the tree. The gate that would close it is a
byte comparison in `ci-gates.sh` — a shared file, and outside this lane's brief, so it is
reported.

---

## 7. What is on this branch

Two commits, both against **current** `main`, both re-implemented rather than applied.
Neither is 3D and neither claims to be.

**`b706bb1` — one child map, bit-indexed.** `DIMS = 2`, `FANOUT = 1 << DIMS`,
`Cell::child(ordinal)` with the ordinal's bits as the axes, called by both `Chart::sync`
and `scene::QuadrantMaterializer`. A `const` assert holds `children_seen`'s `u8` against
`FANOUT`. Three gates: the bit map is checked against the arithmetic it replaced at every
ordinal; the children tile the parent, stated so it survives `DIMS` moving; and the chart
places a child exactly where the generator apportioned it — the third has content, because
the two sides *index* the one map differently (the generator by the ordinal it is building,
the chart by a running child count as holons arrive) and agree only because materialization
is append-only in spec order. That is an assumption about the core, held in this crate, and
it is what a fanout change breaks silently.

**`d85922d` — the frame-buffer stride is gated across the wasm boundary.**
`the_viewer_cuts_the_frame_buffers_at_the_engine_s_stride` reads `viewer/app.js` and
requires it to declare the engine's own `NODE_STRIDE` and `BOND_STRIDE`. **Mutation-tested:**
with `app.js` declaring `NODE_STRIDE = 6` against the engine's 5, exactly one test fails
and it is this one. The verdict codes and re-root kinds are also mirrored in the viewer and
are deliberately *not* covered — they fail loudly (an unknown code renders as a missing
label), and widening the gate to them is a separate change rather than a free rider.

**Gates on this branch:** 61 tests, 0 failures, `--release`; zero warnings.
`--release` is the gate `ci-gates.sh:57` and `verify.yml:46` both run, and it is the only
one that can pass: `a_sandbox_throw_certifies_within_the_declared_budget` (`sim.rs:1659`)
asserts wall-clock `elapsed < 0.5` s on a throw that materializes ~118k cells, which a
debug build cannot meet. Pre-existing on `main`, unrelated to anything here.

**The committed wasm on this branch is deliberately stale.** The salvaged refactor *does*
move the binary (`a1d6cb15…`, 139,489 B, against b510a68's `78c17819…`, 139,490 B) — the
compiler cannot see that `ordinal < FANOUT`, so `(ordinal >> 1) & 1` and `ordinal / 2`
generate different code even though they agree on every value that reaches them. It is not
rebuilt here because F6 says the committed artifact is already 503 bytes off from `main`'s
own source, and bundling that unrelated delta into a parts-shelf commit would hide it.
**Anything landed from this branch must re-run `build-web.sh`.**

---

## 8. Blocked — decisions `MESH_DESIGN` reserves

Listed, not decided.

| # | blocked item | reserved by |
|---|---|---|
| B1 | `GrossState` momentum arity — 3 lanes or 4 | **M-G1**: one coordinated commit, merge-gated by the lead (§8, §9.4) |
| B2 | the FCHC-24 direction table and its Lean instantiation | §2.1 / M-G3; the Lean carries the chart and the caps, **not** the 72,047 sector count |
| B3 | what the engine publishes in 3D — surface claim vs volume | §0 and §3's **PENDING** (M-G2): measure, do not guess |
| B4 | `Cell`'s `z0` and the `[f64; 3]` ripple into `sim.rs` | §7 sequencing: the 2D bit-identity gate lands first |
| B5 | `tier.rs:199`'s stale doc line (F2b) | the sandbox lane's file, mid-edit |
| B6 | a committed-artifact gate in `ci-gates.sh` (F6) | shared file, outside this lane |
