
## Gate: no tree-restoring git on a shared worktree (2026-08-20)
An agent restored `RECOGNITION_PREREG.md` to HEAD while its author held a 23KB uncommitted
expansion in flight — the expansion was destroyed. The prereg's own default G13 (one-call
pathspec commits) guards the COMMIT side; this gate guards the CHECKOUT side: **no agent may
run `git checkout`/`restore`/`stash`/`clean` on any path of a shared worktree, ever** — the
tree carries other agents' uncommitted work. Recovery duty on violation: re-request from the
author agent (which may still hold the content), never reconstruct by hand and never pass
off a reconstruction as the original.
