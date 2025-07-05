# Euler solver - IVP in python
---
---
### Project Structure

```bash
python_code
├── README.md
├── environment.yml
├── jupyter_nbooks          
│   ├── IVP_Euler_Solver.ipynb
│   └── report_plots.ipynb   
├── requirements.txt
├── README.md
├── src
│   ├── __init__.py
│   ├── config.ini          # user imputs
│   ├── main.py             # entry point (command line executable)
│   ├── solution.csv
│   └── solvers.py          # helper code
└── tests
    ├── __init__.py
    └── test_solvers.py     # tested the code logic
```
---
---
# Implementation

- Step - 1 : Clone this repository.

- Step - 2 : Open it in any IDE of your choice.
- Step - 3 : Create a virtual env.
    - use ```./environment.yml``` in case of conda.

    - use ```./requirements.txt``` in case of venv. It has all the pip requirements.

- Step - 4 : update the ```./src/config.ini``` with the inputs. Follow the instructions below.
``` ini
# Never change the LHS of any statement.
# Only input or modify RHS. To avoid code breakage.

# Mesh configuration
[mesh_1D]
n =                     # positive integer only
domain_start =          # float
domain_end =            # float 

# Initial values for the ODE
[initial_conditions]
y_0 =                   # float

# ODE function definition
#   dy/dt = f(t, y)
#   expression = f(t, y)
[ode_function]
expression = np.cos(t) - y  
; use numpy convention to define the function
```

- Step - 5 : From the folder ```python_code```. execute the following in terminal.
```bash
cd python_code
python src/main.py
```
---
---
### Tests

- pytest is available at ```./tests```

- API from the ```./src/solvers.py``` are tested.

---
---
### API from ```./src/solvers.py```
`Euler1D_Solve`

A Python class to solve 1D first-order ODE initial value problems using the **Euler method**.



### `Euler1D_Solve(f, t_start, t_end, y_0, num_steps)`
Initializes the Euler solver.

**Arguments:**
- `f` *(Callable)*: Function defining the ODE `dy/dt = f(t, y)`
- `t_start` *(float)*: Start of the time domain
- `t_end` *(float)*: End of the time domain
- `y_0` *(float)*: Initial value of `y`
- `num_steps` *(int)*: Number of Euler steps



### `solve() -> np.ndarray`
Solves the ODE using Euler's method.

**Returns**:  
`np.ndarray`: Array of approximated solution values `y` at each mesh point.



### `create_1d_mesh() -> np.ndarray`
Generates a 1D uniform mesh from `t_start` to `t_end`.

**Returns**:  
`np.ndarray`: Time mesh array.



### `calc_step_size() -> float`
Calculates the step size `h = (t_end - t_start) / num_steps`.

**Returns**:  
`float`: Step size.



### `plot_solution()`
Plots the numerical solution with step size `h` and `n` in the legend.



### `csv_export(filename: str)`
Exports the solution as a CSV file with columns `t` and `y(t)`.

**Arguments:**
- `filename` *(str)*: Output file name (e.g., `"solution.csv"`)