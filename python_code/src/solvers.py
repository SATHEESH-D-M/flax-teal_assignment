import numpy as np
from typing import Callable
import matplotlib.pyplot as plt
import pandas as pd


class Euler1D_Solve:
    """_summary_
    Class to solve 1D ODE initial value problems using Euler's method.

    Attributes:
        f (Callable): Function defining dy/dt = f(t, y)
        t_start (float): Start of time domain
        t_end (float): End of time domain
        y_0 (float): Initial value of y
        num_steps (int): Number of steps to take (mesh will have num_steps + 1 points)
        mesh (np.ndarray): Array of mesh points (t values)
        h (float): Step size
        solution (np.ndarray): Array of y values at each mesh point

    Methods:
        create_1d_mesh(): Create 1D mesh.
        calc_step_size(): Calculate step size h.
        solve(): Solve the IVP using Euler's method.
        plot_solution(): Plot the numerical solution with h and n in the legend.
        csv_export(filename: str): Export the solution to a CSV file.

    Example:
        def f(t, y):
            return -y + np.cos(t)

        t_start = 0.0
        t_end = 5.0
        y_0 = 1.0
        num_steps = 10

        solver = Euler1D_Solve(f, t_start, t_end, y_0, num_steps)
        solver.plot_solution()
        solver.csv_export("solution.csv")
    """

    def __init__(
        self,
        f: Callable[[float, float], float],
        t_start: float,
        t_end: float,
        y_0: float,
        num_steps: int,
    ):
        """
        Initialize the solver.

        Args:
            f (Callable): Function defining dy/dt = f(t, y)
            t_start (float): Start of time domain
            t_end (float): End of time domain
            y_0 (float): Initial value of y
            num_steps (int): Number of steps to take (mesh will have num_steps + 1 points)
        """
        # Validate function
        if not callable(f):
            raise TypeError("f must be a callable function.")
        self.f = f

        # Validate t_start and t_end
        if not isinstance(t_start, (int, float)) or not isinstance(
            t_end, (int, float)
        ):
            raise TypeError("t_start and t_end must be numbers.")
        if t_start >= t_end:
            raise ValueError("t_start must be less than t_end.")
        self.t_start = float(t_start)
        self.t_end = float(t_end)

        # Validate num_steps
        if not isinstance(num_steps, int) or num_steps <= 0:
            raise ValueError("num_steps must be a pos integer.")
        self.num_steps = num_steps

        # Validate y_0
        if not isinstance(y_0, (int, float)) or isinstance(y_0, bool):
            raise TypeError("y_0 must be a real number.")
        self.y_0 = float(y_0)

        # calculated attributes when the class is initialized
        self.mesh = self.create_1d_mesh()
        self.h = self.calc_step_size()
        self.solution = self.solve()

    def create_1d_mesh(self) -> np.ndarray:
        """
        Create 1D mesh.

        Returns:
            np.ndarray: Array of mesh points (t values)
        """
        return np.linspace(self.t_start, self.t_end, self.num_steps + 1)

    def calc_step_size(self) -> float:
        """
        Calculate step size h.

        Returns:
            float: Step size
        """
        return (self.t_end - self.t_start) / self.num_steps

    def solve(self) -> np.ndarray:
        """
        Solve the IVP using Euler's method.

        Returns:
            np.ndarray: Array of y values at each mesh point
        """
        y = np.zeros(self.num_steps + 1)
        y[0] = self.y_0

        for k in range(self.num_steps):
            t = self.mesh[k]
            y[k + 1] = y[k] + self.h * self.f(t, y[k])

        return y

    def plot_solution(self):
        """
        Plot the numerical solution with h and n in the legend.
        """
        if self.solution is None:
            raise ValueError("You must call .solve() before plotting.")

        plt.figure(figsize=(8, 5))
        plt.plot(
            self.mesh,
            self.solution,
            label=f"Euler method (h = {self.h:.4f}, n = {self.num_steps})",
            marker="o",
        )
        plt.xlabel("t")
        plt.ylabel("y(t)")
        plt.title("Euler Method Solution")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def csv_export(self, filename: str):
        """
        Export the solution to a CSV file.

        Args:
            filename (str): Name of the output CSV file with path
        """
        data = {"t": self.mesh, "y(t)": self.solution}
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Solution exported to {filename}")
