//! h3ere2 response-quality experiment: the SLM perceives and articulates, the physics
//! engine reasons. Built to `scratchpad/h3ere2_eval/PREREG.md` (commit 1dac9a0), which
//! is binding and was sealed before this crate existed.
//!
//! Excluded from the workspace on purpose: it depends on `ciris-nl`'s native inference
//! feature, and an in-workspace dependency on a C++ build script could unify into
//! `ciris-sim-core`'s graph and falsify the isolation gates.

pub mod blocks;
pub mod path;
pub mod scramble;
