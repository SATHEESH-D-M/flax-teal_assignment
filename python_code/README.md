# Euler solver - IVP in python

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

# Implementation

- Step - 1 : Clone this repository.

- Step - 2 : Open it in any IDE of your choice.
- Step - 3 : Create a virtual env.
    - use ```./environment.yml``` in case of conda.

    - use ```./requirements.txt``` in case of venv. It has all the pip requirements.

- Step - 4 : update the ```./src/config.ini``` with the inputs.
``` ini
# Mesh configuration
[mesh_1D]
n =                     # positive integer only
domain_start =          # float
domain_end =            # float 

; Initial values for the ODE
[initial_conditions]
y_0 =                   # float

# ODE function definition
#   dy/dt = f(t, y)
#   expression = f(t, y)
[ode_function]
expression = np.cos(t) - y  
; use numpy convention to define the function

```