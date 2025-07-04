//! Euler ODE Solver (1D)
//!
//! This program solves a first-order ODE of the form dy/dt = f(t, y)
//! using the forward Euler method. Solver parameters and the ODE function
//! are provided through a config.ini file.
//!
//! The solution is printed to the console and saved to a CSV file.

// --- Imports ---

use config::Config as IniConfig;
use rust_code::{SolverConfig, EulerSolver1D, parse_expression};
use std::path::Path;

/// Main entry point for the Euler solver.
///
/// Loads configuration from `config.ini`, parses the ODE function,
/// runs the solver, prints the result, and writes it to a CSV file.
///
/// # Arguments
/// None. Configuration is read from the `config.ini` file.
///
/// # Returns
/// None. Results are printed and written to file.
fn main() {
    // Load and parse the configuration file
    let settings = IniConfig::builder()
        .add_source(config::File::from(Path::new("config.ini")))
        .build()
        .expect("Failed to read config");

    // Deserialize the config file into typed struct
    let config: SolverConfig = settings
        .try_deserialize()
        .expect("Failed to deserialize config");

    // Parse the user-defined ODE expression into a callable function
    let expression_fn = parse_expression(config.ode_function.expression)
        .expect("Failed to parse expression");

    // Create and run the Euler solver
    let solver = EulerSolver1D::new(
        expression_fn,
        config.mesh_1_d.domain_start,
        config.mesh_1_d.domain_end,
        config.initial_conditions.y_0,
        config.mesh_1_d.n,
    );

    // Print the results to the console
    for (t, y) in solver.mesh.iter().zip(solver.solution.iter()) {
        println!("t = {:>5.2}, y = {:>8.5}", t, y);
    }

    // Write the results to a CSV file
    if let Err(e) = solver.export_to_csv(&config.output.csv_file) {
        eprintln!("Failed to export to CSV: {}", e);
    }
}
