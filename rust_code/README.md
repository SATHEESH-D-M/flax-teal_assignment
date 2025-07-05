# Euler Solver -  IVP in Rust 
This module implements the same Euler ODE solver as the Python version — but fully in Rust, using strong type-checking and fast performance.

---
## Project Structure

```
rust_code/
├── src/
│   ├── lib.rs          # Euler solver implementation
│   ├── main.rs         # Main runner
│   └── tests.rs        # Unit tests (moved if separated)
├── config.ini          # User input config file
├── Cargo.toml          # Rust dependencies
└── output.csv          # (Generated) Solution output
```
---


##  Setup and Implementation

### Step 1: Clone the Repository

```bash
git clone https://github.com/SATHEESH-D-M/flax-teal_assignment.git
cd flax-teal_assignment/rust_code
```

### Step 2: Build the Project

```bash
cargo build
```

### Step 3: Update the Configuration File

Update the configuration file at `./config.ini`. **Do not modify the LHS keys**.

```ini
# Mesh configuration
[mesh_1D]
n = 10                  # positive integer only
domain_start = 0.0      # float
domain_end = 5.0        # float 

# Initial values for the ODE
[initial_conditions]
y_0 = 1.0               # float

# ODE function definition
[ode_function]
expression = cos(t) - y  ; use mathematical syntax (NOT numpy)

# Output configuration
[output]
csv_file = output.csv
```

### Step 4: Run the Solver

```bash
cargo run
```

The solution will be printed and also exported to the specified CSV file.

---

## Tests

Unit tests are defined in `src/tests.rs` and test:

- Expression parsing
- Mesh generation
- Euler solver for a known analytical solution

To run the tests:

```bash
cargo test
```

---

## API Summary — `EulerSolver1D`

Main struct for solving ODEs of the form `dy/dt = f(t, y)` using Euler’s method.

---

### `EulerSolver1D::new(f, t_start, t_end, y_0, num_steps) -> Self`

**Arguments:**
- `f`: Function implementing `Fn(f64, f64) -> f64`
- `t_start`: Start of time domain
- `t_end`: End of time domain
- `y_0`: Initial value of `y`
- `num_steps`: Number of Euler steps

Initializes and solves the IVP on construction.

---

### `.generate_mesh(t_start, t_end, n) -> Vec<f64>`

Generates the uniform mesh of `n + 1` points between `t_start` and `t_end`.

---

### `.solve() -> Vec<f64>`

Executes Euler’s method to return solution values corresponding to the mesh.

---

### `.export_to_csv(filename: &str) -> Result<(), Box<dyn Error>>`

Exports the mesh and solution pair as a CSV file.

---

## Type Safety and Design Highlights

- **Strong Typing**: Uses `serde` to deserialize and validate `.ini` configs at compile time.
- **Error Handling**: Proper error propagation using `Result<T, E>` and descriptive panics.
- **Expression Parsing**: Uses the [`meval`](https://crates.io/crates/meval) crate for safe mathematical expression evaluation.


