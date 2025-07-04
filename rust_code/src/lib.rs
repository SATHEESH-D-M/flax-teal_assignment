//! Euler ODE Solver Library
//!
//! This library provides a configuration-driven 1D forward Euler solver
//! for solving first-order ODEs of the form dy/dt = f(t, y).
//! It supports configurable mesh, initial conditions, expression parsing,
//! and CSV export of results.

// --- Imports ---

use meval::{Context, Expr};         // Used for parsing and evaluating expressions
use serde::Deserialize;             // Used for config deserialization from .ini
use std::error::Error;              // Generic error handling trait

// ================================
// Section: Configuration Structs
// ================================

/// Configuration for mesh (domain and discretization)
#[derive(Debug, Deserialize)]
pub struct MeshConfig {
    pub n: usize,               // Number of steps
    pub domain_start: f64,      // Start of the time domain
    pub domain_end: f64,        // End of the time domain
}

/// Configuration for the initial condition y(0)
#[derive(Debug, Deserialize)]
pub struct InitialConditions {
    pub y_0: f64,               // Initial value of y
}

/// Configuration for the ODE function to evaluate
#[derive(Debug, Deserialize)]
pub struct OdeConfig {
    pub expression: String,     // String expression, e.g., "cos(t) - y"
}

/// Configuration for output behavior (e.g., CSV file path)
#[derive(Debug, Deserialize)]
pub struct OutputConfig {
    pub csv_file: String,       // File name to export results to
}

/// Aggregated solver configuration loaded from `config.ini`
#[derive(Debug, Deserialize)]
pub struct SolverConfig {
    pub mesh_1_d: MeshConfig,                    // Mesh config section
    pub initial_conditions: InitialConditions,   // Initial condition
    pub ode_function: OdeConfig,                 // ODE function config (matches [ode_function])
    pub output: OutputConfig,                    // Output config
}

// ================================
// Section: Solver Struct & Methods
// ================================

/// Euler 1D solver state and methods
pub struct EulerSolver1D {
    pub expression_fn: Box<dyn Fn(f64, f64) -> f64>, // Evaluated ODE function
    pub t_start: f64,          // Domain start
    pub t_end: f64,            // Domain end
    pub y0: f64,               // Initial condition
    pub num_steps: usize,      // Number of steps
    pub mesh: Vec<f64>,        // Discretized mesh of time points
    pub step_size: f64,        // Time step size
    pub solution: Vec<f64>,    // Computed solution values at mesh points
}

impl EulerSolver1D {
    /// Constructs a new Euler solver instance and computes the solution.
    ///
    /// # Arguments
    /// * `expression_fn` - Parsed ODE function (f64, f64) -> f64
    /// * `t_start`, `t_end` - Time domain bounds
    /// * `y0` - Initial y value
    /// * `num_steps` - Number of steps (mesh resolution)
    ///
    /// # Returns
    /// * `Self` - Solver object with computed mesh and solution
    pub fn new(
        expression_fn: impl Fn(f64, f64) -> f64 + 'static,
        t_start: f64,
        t_end: f64,
        y0: f64,
        num_steps: usize,
    ) -> Self {
        let mesh = Self::generate_mesh(t_start, t_end, num_steps);
        let step_size = (t_end - t_start) / num_steps as f64;
        let mut solver = Self {
            expression_fn: Box::new(expression_fn),
            t_start,
            t_end,
            y0,
            num_steps,
            mesh,
            step_size,
            solution: Vec::new(),
        };
        solver.solution = solver.solve();  // Run computation
        solver
    }

    /// Generates a 1D uniform mesh from `t_start` to `t_end` with `n` steps
    fn generate_mesh(t_start: f64, t_end: f64, n: usize) -> Vec<f64> {
        let h = (t_end - t_start) / n as f64;
        (0..=n).map(|i| t_start + i as f64 * h).collect()
    }

    /// Solves the ODE using the forward Euler method
    ///
    /// Returns a vector `y` containing approximated solution values
    fn solve(&self) -> Vec<f64> {
        let mut y = vec![0.0; self.num_steps + 1];
        y[0] = self.y0;
        for k in 0..self.num_steps {
            y[k + 1] = y[k] + self.step_size * (self.expression_fn)(self.mesh[k], y[k]);
        }
        y
    }

    /// Writes the (t, y) solution pairs to a CSV file
    ///
    /// # Arguments
    /// * `filename` - Path to output CSV file
    ///
    /// # Returns
    /// * `Result<(), Box<dyn Error>>` - Ok or descriptive error
    pub fn export_to_csv(&self, filename: &str) -> Result<(), Box<dyn Error>> {
        let mut writer = csv::Writer::from_path(filename)?;
        writer.write_record(&["t", "y(t)"])?;

        for (&t, &y) in self.mesh.iter().zip(self.solution.iter()) {
            writer.write_record(&[t.to_string(), y.to_string()])?;
        }

        writer.flush()?;  // Ensure data is written
        println!("Solution exported to `{}`", filename);
        Ok(())
    }
}

// ================================
// Section: Expression Parser
// ================================

/// Parses a string expression like "cos(t) - y" into a callable function
///
/// # Arguments
/// * `expr_str` - String representing the mathematical expression
///
/// # Returns
/// * `Result<Box<dyn Fn(f64, f64) -> f64>, Box<dyn Error>>`
///   - Function that takes (t, y) and returns f(t, y)
pub fn parse_expression(
    expr_str: String,
) -> Result<Box<dyn Fn(f64, f64) -> f64 + 'static>, Box<dyn Error>> {
    let expr = expr_str.parse::<Expr>()?;  // Parse using `meval`
    let f = move |t: f64, y: f64| {
        let mut ctx = Context::new();
        ctx.var("t", t);
        ctx.var("y", y);
        expr.eval_with_context(ctx).unwrap()  // Evaluate with context
    };
    Ok(Box::new(f))
}


// ================================
// Section: Unit Tests
// ================================
#[cfg(test)]
mod tests {
    use super::*;

    /// Tests whether the expression parser correctly converts
    /// a string expression into a callable function.
    /// For input "cos(t) - y", the output for (t=0.0, y=0.0) should be 1.0.
    #[test]
    fn test_expression_parser() {
        let expr_str = "cos(t) - y".to_string();
        let f = parse_expression(expr_str).expect("Failed to parse expression");
        let val = f(0.0, 0.0);           // cos(0) - 0 = 1.0
        let expected = 1.0;
        assert!((val - expected).abs() < 1e-6); // Allow small floating-point error
    }

    /// Tests whether the mesh generation method produces the correct
    /// evenly spaced time points over the domain [0.0, 1.0] with 4 intervals.
    #[test]
    fn test_mesh_generation() {
        let mesh = EulerSolver1D::generate_mesh(0.0, 1.0, 4);
        let expected = vec![0.0, 0.25, 0.5, 0.75, 1.0]; // step size = 0.25
        assert_eq!(mesh, expected);
    }

    /// Tests the Euler solver on a known ODE: dy/dt = y with y(0) = 1.
    /// The exact solution is y(t) = exp(t), so y(1) ≈ 2.71828.
    /// This test checks that the numerical solution is reasonably close.
    #[test]
    fn test_euler_solver_linear_case() {
        let f = |_t: f64, y: f64| y; // dy/dt = y
        let solver = EulerSolver1D::new(f, 0.0, 1.0, 1.0, 10); // 10 steps over [0,1]
        let approx = solver.solution.last().unwrap();         // Get y(1)
        let exact = std::f64::consts::E;                      // ~2.71828
        assert!((approx - exact).abs() < 0.5); // Allow loose tolerance for Euler method
    }
}
