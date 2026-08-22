//! PART F — the f32 caveat, measured rather than guessed.
//!
//! The main comparison runs Rapier in f64 (`rapier3d-f64`) because a matched-ACCURACY
//! claim against a f64 engine cannot be made against a f32 competitor: f32 has ~7
//! decimal digits, so it cannot reach the tighter targets at any step size. But f32 is
//! Rapier's default and what a game actually ships, and it enables SIMD paths f64 does
//! not have. So: how much throughput does the f64 requirement cost Rapier?
//!
//! Throughput only. No accuracy claim is made for the f32 build, because there is no
//! honest one to make against an f64 reference.

#[path = "../scene.rs"]
mod scene;
use scene::Scene;
use std::time::Instant;

fn time_f64(s: &Scene, dt: f64, steps: usize, iters: usize) -> f64 {
    use rapier3d_f64::prelude::*;
    let mut best = f64::INFINITY;
    for _ in 0..5 {
        let mut w = PhysicsWorld::new();
        w.gravity = Vec3::new(0.0, 0.0, 0.0);
        w.integration_parameters.dt = dt;
        w.integration_parameters.num_solver_iterations = iters;
        let b: Vec<_> = (0..s.n)
            .map(|i| {
                let p = s.pos0[i];
                w.insert_body(
                    RigidBodyBuilder::dynamic()
                        .translation(Vec3::new(p[0], p[1], p[2]))
                        .additional_mass(1.0)
                        .lock_rotations()
                        .can_sleep(false),
                )
            })
            .collect();
        for &(i, j, k) in &s.edges {
            w.insert_impulse_joint(
                b[i],
                b[j],
                SpringJointBuilder::new(0.0, k, 0.0).spring_model(MotorModel::ForceBased),
            );
        }
        let t0 = Instant::now();
        for _ in 0..steps {
            w.step();
        }
        best = best.min(t0.elapsed().as_secs_f64() * 1e9 / steps as f64);
    }
    best
}

fn time_f32(s: &Scene, dt: f32, steps: usize, iters: usize) -> f64 {
    use rapier3d::prelude::*;
    let mut best = f64::INFINITY;
    for _ in 0..5 {
        let mut w = PhysicsWorld::new();
        w.gravity = Vec3::new(0.0, 0.0, 0.0);
        w.integration_parameters.dt = dt;
        w.integration_parameters.num_solver_iterations = iters;
        let b: Vec<_> = (0..s.n)
            .map(|i| {
                let p = s.pos0[i];
                w.insert_body(
                    RigidBodyBuilder::dynamic()
                        .translation(Vec3::new(p[0] as f32, p[1] as f32, p[2] as f32))
                        .additional_mass(1.0)
                        .lock_rotations()
                        .can_sleep(false),
                )
            })
            .collect();
        for &(i, j, k) in &s.edges {
            w.insert_impulse_joint(
                b[i],
                b[j],
                SpringJointBuilder::new(0.0, k as f32, 0.0).spring_model(MotorModel::ForceBased),
            );
        }
        let t0 = Instant::now();
        for _ in 0..steps {
            w.step();
        }
        best = best.min(t0.elapsed().as_secs_f64() * 1e9 / steps as f64);
    }
    best
}

fn main() {
    println!("PART F — what the f64 requirement costs Rapier (throughput only)");
    println!("Same scene, same dt, same 4 solver iterations. Best of 5.\n");
    println!("{:<24} {:>6} {:>8} {:>14} {:>14} {:>10}", "scene", "N", "edges", "rapier f64", "rapier f32", "f32 gain");
    println!("{}", "-".repeat(80));
    for s in [
        Scene::k11(),
        Scene::complete(64),
        Scene::complete(256),
        Scene::lattice(4),
        Scene::lattice(8),
    ] {
        let steps = (2_000_000 / (s.n * s.n).max(1)).clamp(30, 3000);
        let dt = 1e-2;
        let a = time_f64(&s, dt, steps, 4);
        let b = time_f32(&s, dt as f32, steps, 4);
        println!(
            "{:<24} {:>6} {:>8} {:>11.1} ns {:>11.1} ns {:>9.2}x",
            s.name, s.n, s.edges.len(), a, b, a / b
        );
    }
    println!("\nEvery Rapier figure in the main comparison is the f64 column. Divide the");
    println!("reported ratios by the f32 gain to get what a shipping f32 Rapier would show");
    println!("on THROUGHPUT — but note it could not have met the matched-accuracy targets");
    println!("at all, which is why the main table is f64.");
}
