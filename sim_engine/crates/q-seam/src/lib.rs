//! # q-seam — the certified seam
//!
//! An exact quantum reference and a Boolean-occupancy chart over the *same* system, with a
//! refusal criterion staked before this crate existed. The product is not a better solver; it is
//! the machine declining to speak where correlation makes the chart lie.
//!
//! Everything here is governed by `sim_engine/Q_SEAM_PREREG.md`, frozen at commit `3b6eed0` with
//! amendment A1 at `dab10aa`, both before the first line of this crate was written. Thresholds
//! marked STAKED there are constants here; nothing in this crate may adjust one.
//!
//! **Exactness first.** `Q_SEAM_PREREG.md` §3 is a ladder of sixteen gates, and no configuration
//! reaches the chart, the certificate or the share until it has passed them. A gate failure makes
//! a configuration VOID — excluded and reported as excluded — never a refusal and never a datum.

pub mod audit;
pub mod certificate;
pub mod chart;
pub mod dense;
pub mod hubbard;
pub mod lanczos;
pub mod observables;
pub mod share;

/// Chain lengths of the pinned sweep (`Q_SEAM_PREREG.md` §1).
pub const SWEEP_SITES: [usize; 5] = [2, 4, 6, 8, 10];

/// Interaction strengths of the pinned sweep, in units of `t`.
pub const SWEEP_U: [f64; 14] = [
    0.0, 0.125, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0,
];

/// The plant: the sweep's far end, which every surviving criterion must refuse.
pub const PLANT_U: f64 = 16.0;

/// Staked tolerances for the six observables (`Q_SEAM_PREREG.md` §2.1), in the order
/// e, d, n_i, m_i, bond, D_bool.
pub const TAU: [f64; 6] = [0.02, 0.02, 0.02, 0.05, 0.02, 0.05];

/// The staked safety factor shared by C1 and C3.
pub const KAPPA: f64 = 0.5;
