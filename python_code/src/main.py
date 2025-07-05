from solvers import Euler1D_Solve
import numpy as np
import configparser


# Define f(t, y) dynamically using eval
def f(t, y):
    return eval(expr, {"np": np, "t": t, "y": y})


if __name__ == "__main__":
    # This block is executed when the script is run directly
    # Read configuration from config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")

    n = config.getint("mesh_1D", "n")
    domain_start = config.getfloat("mesh_1D", "domain_start")
    domain_end = config.getfloat("mesh_1D", "domain_end")
    y_0 = config.getfloat("initial_conditions", "y_0")
    # Derivative function
    expr = config.get("ode_function", "expression")

    # Create an instance of the solver
    solver = Euler1D_Solve(f, domain_start, domain_end, y_0, n)
    # Plot the solution
    solver.plot_solution()
    # Save the solution to a file
    solver.csv_export("solution.csv")
