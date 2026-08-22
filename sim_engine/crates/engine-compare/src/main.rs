//! ciris-sim-core vs Rapier 0.35.2 (f64) — FSD §10.
//!
//! Read PART 0 before any number below it. The two engines do not do the same job;
//! this measures them only on the workload both can express honestly, and says where
//! that stops being informative.
//!
//! Run: `cargo run --release`

mod engines;
mod scene;

use engines::*;
use scene::Scene;

/// Instantiate the const-generic core at the sizes the scenes need. `ciris-sim-core` is
/// generic in `const N: usize` (gap E10), so each size is its own monomorphisation and
/// the list must be written out. Rapier takes its size at runtime — which is itself one
/// of the differences this comparison is about.
macro_rules! at_size {
    ($scene:expr, $f:ident, $a:expr, $b:expr; $($n:literal),*) => {
        match $scene.n {
            $($n => $f::<$n>($scene, $a, $b),)*
            other => panic!("N = {other} is not instantiated; add it to the at_size! list"),
        }
    };
}

/// Simulated time every accuracy figure is taken over. FIXED across scenes on purpose:
/// error grows with run length, so comparing scenes at different run lengths compares
/// run lengths.
const T_SIM: f64 = 10.0;

struct Row {
    n: usize,
    edges: usize,
    density: f64,
    dt: f64,
    ours_ns: f64,
    rapier_ns: f64,
    ours_err: f64,
    rapier_err: f64,
    setup_ours_us: f64,
    setup_rapier_us: f64,
    mem_ours: usize,
}

fn measure<const N: usize>(scene: &Scene, timing_steps: usize, iters: usize) -> Row {
    let st = build_structure::<N>(scene);
    let x0 = initial_state::<N>(scene).pos;

    // Matched setting: the same fraction of each scene's own stability limit, so a stiff
    // scene gets a small step in BOTH engines and neither is flattered by a step size
    // that happens to suit it.
    let dt = 0.1 / st.lambda_max().max(1e-12).sqrt();
    let acc_steps = ((T_SIM / dt).round() as usize).max(1);

    Row {
        n: N,
        edges: scene.edges.len(),
        density: scene.density(),
        dt,
        ours_ns: time_ours::<N>(&st, &x0, dt, timing_steps, 5),
        rapier_ns: time_rapier(scene, dt, timing_steps, iters, 5),
        ours_err: accuracy_ours::<N>(&st, &x0, dt, acc_steps, 24),
        rapier_err: accuracy_rapier::<N>(&st, &x0, scene, dt, acc_steps, iters, 24),
        setup_ours_us: setup_cost_ours::<N>(scene, if N >= 216 { 1 } else { 3 }) / 1000.0,
        setup_rapier_us: setup_cost_rapier(scene, 3) / 1000.0,
        mem_ours: std::mem::size_of::<ciris_sim_core::structure::Structure<N>>(),
    }
}

fn timing_steps_for(n: usize) -> usize {
    (20_000_000 / (n * n).max(1)).clamp(30, 4000)
}

fn header(title: &str) {
    use std::io::Write;
    let _ = std::io::stdout().flush();
    println!("\n{}", "=".repeat(112));
    println!("{title}");
    println!("{}", "=".repeat(112));
}

fn table(rows: &[Row]) {
    println!(
        "{:>6} {:>7} {:>8} {:>10} {:>12} {:>13} {:>8} {:>11} {:>11} {:>11} {:>10}",
        "N", "edges", "density", "dt", "ours ns/st", "rapier ns/st", "ratio",
        "ours Linf", "rap Linf", "setup ours", "setup rap"
    );
    println!("{}", "-".repeat(112));
    for r in rows {
        println!(
            "{:>6} {:>7} {:>8.3} {:>10.3e} {:>12.1} {:>13.1} {:>7.1}x {:>11.2e} {:>11.2e} {:>10.2}ms {:>9.2}ms",
            r.n, r.edges, r.density, r.dt, r.ours_ns, r.rapier_ns,
            r.rapier_ns / r.ours_ns, r.ours_err, r.rapier_err,
            r.setup_ours_us / 1000.0, r.setup_rapier_us / 1000.0
        );
    }
}

fn main() {
    // Structure<512> is ~16.8 MB and lives by value; give it room.
    std::thread::Builder::new()
        .stack_size(512 * 1024 * 1024)
        .spawn(run)
        .unwrap()
        .join()
        .unwrap();
}

fn run() {
    println!("ciris-sim-core  vs  Rapier 0.35.2 (rapier3d-f64) — FSD §10 comparison");
    println!("host: {}, release + LTO + codegen-units=1, best of 5 repetitions", std::env::consts::ARCH);

    header("PART 0 — what is and is not being compared (READ FIRST; FSD §10.1 is binding)");
    println!("Rapier is a rigid-body engine: broad-phase collision, contacts, friction, CCD,");
    println!("joints. ciris-sim-core is an all-pairs coupled integrator on a complete graph");
    println!("with a resistance metric. The ONLY workload both express honestly is a");
    println!("conservative spring network with NO contacts, so that is the whole comparison.");
    println!();
    println!("What this means for the numbers below:");
    println!("  * Rapier's broad phase, narrow phase and contact solver are IDLE. It is");
    println!("    carrying machinery it is not being allowed to use.");
    println!("  * Our engine cannot do contacts AT ALL, so there is no scene in the other");
    println!("    direction. A collision benchmark would read 'ciris-sim-core: cannot run'.");
    println!("  * Rapier is run in f64 to match our precision. Its default is f32 with SIMD,");
    println!("    which is faster; f64 is required for a matched-accuracy claim but it is NOT");
    println!("    the configuration a game would ship. See PART F.");
    println!();
    println!("REGIME (FSD §13): harmonic, rest_scale = 0, so F = -Lx EXACTLY. This is the only");
    println!("regime where the twin-decoupling theorem holds. It is also the regime where the");
    println!("system is LINEAR and therefore has a closed-form solution — which is what both");
    println!("engines are measured against, so the reference is a property of the ODE and of");
    println!("neither competitor. Outside rest_scale = 0 the theorem does not hold and no");
    println!("exact reference is available.");
    println!();
    println!("ACCURACY, defined: Linf = max over 24 sampled times, all nodes, all axes, of");
    println!("|x_sim - x_exact|, over a FIXED simulated time T = {T_SIM}. Absolute, in the same");
    println!("length units as the scene (nodes start on a unit sphere, or a unit lattice).");

    header("PART A — do both engines solve the SAME system? (exactly solvable case)");
    println!("Two unit masses, zero-rest-length spring k=1, released at separation 1.");
    println!("Analytic: r(t) = cos(sqrt(2) t). Neither engine's output is the reference.");
    println!();
    two_body_convergence();

    header("PART B — the object the engine actually runs, and complete graphs");
    println!("Matched generality: on a complete graph BOTH engines do O(N^2) constraint work.");
    let k11 = Scene::k11();
    let mut rows = vec![at_size!(&k11, measure, timing_steps_for(11), 4; 11)];
    for n in [11usize, 32, 64, 128, 256] {
        let s = Scene::complete(n);
        rows.push(at_size!(&s, measure, timing_steps_for(n), 4; 11, 32, 64, 128, 256));
    }
    table(&rows);
    println!("(row 1 is K11 with the MEASURED couplings, 22 edges; the rest are unit-stiffness");
    println!(" complete graphs. Both engines at the same dt, so Linf is comparable within a row.)");

    header("PART C — sparse 3D lattices: the shape a general-purpose engine is built for");
    println!("Our step is all-pairs O(N^2) whatever the edge count; Rapier's work is O(E).");
    println!("This is where the FSD's retracted §11 would have had to save us, and cannot.");
    let mut rows = Vec::new();
    for s in [3usize, 4, 5, 6, 8] {
        let sc = Scene::lattice(s);
        let n = sc.n;
        rows.push(at_size!(&sc, measure, timing_steps_for(n), 4; 27, 64, 125, 216, 512));
    }
    table(&rows);

    header("PART D — total cost at MATCHED ACCURACY (the number that actually compares)");
    println!("Each engine picks its own dt: halve until Linf <= target over T = {T_SIM}, then");
    println!("time that configuration. What is compared is total work for the same physical");
    println!("time at the same fidelity.");
    matched_table();

    header("PART D2 — is the extrapolation honest? (predicted step run directly)");
    verify_extrapolation();

    header("PART E — memory and setup, which per-step cost hides");
    println!("Ours runs an O(N^3) Jacobi eigensolve and holds O(N^2) doubles. Rapier inserts");
    println!("N bodies and E joints. On the sparse scenes this is the dominant asymmetry.");
    println!("{:>18} {:>8} {:>16} {:>14} {:>14} {:>12}", "scene", "N", "ours Structure", "ours setup", "rapier setup", "ratio");
    println!("{}", "-".repeat(88));
    for sc in [Scene::complete(11), Scene::complete(64), Scene::complete(256),
               Scene::lattice(4), Scene::lattice(6), Scene::lattice(8)] {
        let n = sc.n;
        let r = at_size!(&sc, measure, 30, 4; 11, 27, 32, 64, 125, 128, 216, 256, 512);
        println!(
            "{:>18} {:>8} {:>13} KB {:>12.2}ms {:>12.2}ms {:>11.0}x",
            sc.name, n, r.mem_ours / 1024, r.setup_ours_us / 1000.0,
            r.setup_rapier_us / 1000.0, r.setup_ours_us / r.setup_rapier_us
        );
    }
}

/// PART A, ported from the standalone fairness probe.
fn two_body_convergence() {
    use ciris_sim_core::dynamics::{step, State};
    use ciris_sim_core::structure::{Structure, NO_TWINS};
    use rapier3d_f64::prelude::*;

    const K: f64 = 1.0;
    let w = (2.0f64 * K).sqrt();
    let t_end = 5.0 * 2.0 * std::f64::consts::PI / w;
    let exact = |t: f64| (w * t).cos();

    let mut c = [[0.0f64; 2]; 2];
    c[0][1] = K;
    c[1][0] = K;
    let st = Structure::<2>::from_coupling(&c, NO_TWINS);

    let ours = |n: usize| {
        let dt = t_end / n as f64;
        let p = harmonic(dt);
        let mut s = State::<2>::at_rest([[-0.5, 0.0, 0.0], [0.5, 0.0, 0.0]]);
        let mut worst = 0.0f64;
        for i in 1..=n {
            step(&mut s, &st, &p, false);
            worst = worst.max(((s.pos[1][0] - s.pos[0][0]) - exact(i as f64 * dt)).abs());
        }
        worst
    };
    let rap = |n: usize, iters: usize| {
        let dt = t_end / n as f64;
        let mut world = PhysicsWorld::new();
        world.gravity = Vec3::new(0.0, 0.0, 0.0);
        world.integration_parameters.dt = dt;
        world.integration_parameters.num_solver_iterations = iters;
        let b0 = world.insert_body(RigidBodyBuilder::dynamic().translation(Vec3::new(-0.5, 0.0, 0.0))
            .additional_mass(1.0).lock_rotations().can_sleep(false));
        let b1 = world.insert_body(RigidBodyBuilder::dynamic().translation(Vec3::new(0.5, 0.0, 0.0))
            .additional_mass(1.0).lock_rotations().can_sleep(false));
        world.insert_impulse_joint(b0, b1,
            SpringJointBuilder::new(0.0, K, 0.0).spring_model(MotorModel::ForceBased));
        let mut worst = 0.0f64;
        for i in 1..=n {
            world.step();
            let r = world.bodies[b1].translation().x - world.bodies[b0].translation().x;
            worst = worst.max((r - exact(i as f64 * dt)).abs());
        }
        worst
    };
    let ord = |p: f64, c: f64| if p.is_nan() { "   -".to_string() } else { format!("{:.2}", (p / c).log2()) };

    println!("{:>8} {:>11} {:>13} {:>7} {:>13} {:>7}", "steps", "dt", "ours Linf", "order", "rapier Linf", "order");
    let (mut po, mut pr) = (f64::NAN, f64::NAN);
    let mut n = 512usize;
    for _ in 0..7 {
        let (eo, er) = (ours(n), rap(n, 4));
        println!("{:>8} {:>11.3e} {:>13.4e} {:>7} {:>13.4e} {:>7}",
            n, t_end / n as f64, eo, ord(po, eo), er, ord(pr, er));
        po = eo; pr = er; n *= 2;
    }
    println!();
    println!("Both converge to the same exact solution, so a matched-accuracy comparison");
    println!("EXISTS. But the ORDERS differ: ours is 2 (velocity Verlet), Rapier's is 1.");
    println!("That is why PART D is a curve and not a single ratio — the gap widens as the");
    println!("accuracy target tightens, and any single 'Nx faster' number is meaningless");
    println!("without the accuracy it was taken at.");
}

fn matched_table() {
    println!("Each engine's error model is MEASURED on each scene (three step sizes), then");
    println!("the step needed for the target is solved from it. Orders are printed so the");
    println!("extrapolation can be judged; one row is then verified by a direct run.");
    println!();
    for sc in [Scene::k11(), Scene::complete(64), Scene::lattice(4)] {
        let (fo, fr) = at_size!(&sc, fits_for, 256, 4; 11, 64);
        println!("  {}  (N = {}, {} edges)", sc.name, sc.n, sc.edges.len());
        println!("    ours   Linf = {:.3e} * dt^{:.3}   [{:.2e}->{:.2e}, {:.2e}->{:.2e}, {:.2e}->{:.2e}]  {:.0} ns/step",
            fo.c, fo.order,
            fo.points[0].0, fo.points[0].1, fo.points[1].0, fo.points[1].1, fo.points[2].0, fo.points[2].1, fo.ns_per_step);
        println!("    rapier Linf = {:.3e} * dt^{:.3}   [{:.2e}->{:.2e}, {:.2e}->{:.2e}, {:.2e}->{:.2e}]  {:.0} ns/step",
            fr.c, fr.order,
            fr.points[0].0, fr.points[0].1, fr.points[1].0, fr.points[1].1, fr.points[2].0, fr.points[2].1, fr.ns_per_step);
        println!("    {:>8} {:>11} {:>11} {:>12} {:>11} {:>11} {:>12} {:>9}",
            "target", "ours dt", "ours steps", "ours total", "rap dt", "rap steps", "rap total", "ratio");
        for &target in &[1e-1f64, 1e-2, 1e-3, 1e-4] {
            let (odt, ost, oms) = fo.cost_for(T_SIM, target);
            let (rdt, rst, rms) = fr.cost_for(T_SIM, target);
            println!("    {:>8.0e} {:>11.3e} {:>11} {:>10.2}ms {:>11.3e} {:>11} {:>10.1}ms {:>8.0}x",
                target, odt, ost, oms, rdt, rst, rms, rms / oms);
        }
        println!();
    }
    println!("Ratio = rapier total / ours total, both to simulate T = {T_SIM} at the same Linf.");
    println!("The ratio GROWS as the target tightens because the convergence orders differ");
    println!("(2 vs 1): ours needs steps ~ eps^-1/2, Rapier ~ eps^-1. Quoting a single");
    println!("'Nx faster' without naming the accuracy it was taken at would be meaningless.");
}

/// Verify the extrapolation on the one scene where it is cheap to check.
fn verify_extrapolation() {
    let sc = Scene::k11();
    let (fo, fr) = fits_for::<11>(&sc, 256, 4);
    println!("{:>8} {:>10} {:>14} {:>14} {:>9}", "engine", "target", "predicted dt", "measured Linf", "pred/meas");
    println!("{}", "-".repeat(60));
    let st = build_structure::<11>(&sc);
    let x0 = initial_state::<11>(&sc).pos;
    for &target in &[1e-2f64, 1e-3] {
        let (odt, _, _) = fo.cost_for(T_SIM, target);
        let om = verify_ours::<11>(&st, &x0, T_SIM, odt);
        println!("{:>8} {:>10.0e} {:>14.3e} {:>14.3e} {:>8.2}x", "ours", target, odt, om, target / om);
        let (rdt, _, _) = fr.cost_for(T_SIM, target);
        let rm = verify_rapier::<11>(&st, &x0, &sc, T_SIM, rdt, 4);
        println!("{:>8} {:>10.0e} {:>14.3e} {:>14.3e} {:>8.2}x", "rapier", target, rdt, rm, target / rm);
    }
    println!("\nA ratio near 1.0 means the extrapolated step really does hit the target.");
}

fn fits_for<const N: usize>(scene: &Scene, base: usize, iters: usize) -> (Fit, Fit) {
    let st = build_structure::<N>(scene);
    let x0 = initial_state::<N>(scene).pos;
    (
        fit_ours::<N>(&st, &x0, T_SIM, base),
        fit_rapier::<N>(&st, &x0, scene, T_SIM, iters, base),
    )
}
