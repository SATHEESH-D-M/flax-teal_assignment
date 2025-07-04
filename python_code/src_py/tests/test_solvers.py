"""Tested only the logical methods of the Euler1D_Solve class.
namely,
- create_1d_mesh
- calc_step_size
- solve
"""

import pytest
from src_py.src.solvers import Euler1D_Solve
import numpy as np


# assumed a function of this type is defined in the module
def f(t, y):
    return -y + np.cos(t)


#######################################
# happy path test cases
@pytest.fixture
def solver1():
    # happy path test case (no exceptions path)
    return Euler1D_Solve(f, t_start=0.0, t_end=5.0, y_0=1.0, num_steps=10)


def test_create_1d_mesh(solver1):
    mesh = solver1.create_1d_mesh()
    # checks that the mesh has the correct number of points
    assert len(mesh) == solver1.num_steps + 1
    # checks that the first point is t_start
    assert mesh[0] == solver1.t_start

    expected_end = (
        solver1.t_start + solver1.calc_step_size() * solver1.num_steps
    )
    # checks that the last point is t_end
    assert np.isclose(mesh[-1], expected_end)


def test_calc_step_size(solver1):
    h = solver1.calc_step_size()
    expected_h = (solver1.t_end - solver1.t_start) / solver1.num_steps
    # checks that the step size is calculated correctly
    assert np.isclose(h, expected_h)


def test_solve_method(solver1):
    solution = solver1.solve()

    # Output is a numpy array
    assert isinstance(solution, np.ndarray), (
        "solve() should return a numpy array"
    )

    # Correct number of points
    assert len(solution) == solver1.num_steps + 1, (
        "Solution length should be num_steps + 1"
    )

    # Initial condition matches y_0
    assert np.isclose(solution[0], solver1.y_0), (
        "First value of solution should equal y_0"
    )

    # Manual test: use simple dy/dt = y → y[0]=1.0, y[1]=1.5, y[2]=2.25
    def simple_f(t, y):
        return y

    test_solver = Euler1D_Solve(
        simple_f, t_start=0.0, t_end=1.0, y_0=1.0, num_steps=2
    )
    expected = np.array([1.0, 1.5, 2.25])
    assert np.allclose(test_solver.solve(), expected, rtol=1e-4), (
        "Euler steps not matching manual calculation"
    )


##########################################
# exception handled test cases
def test_invalid_f_callable_cases():
    # f is a string
    with pytest.raises(TypeError, match="f must be a callable function."):
        Euler1D_Solve("no_fn", t_start=0.0, t_end=5.0, y_0=1.0, num_steps=10)
    # f is an integer
    with pytest.raises(TypeError, match="f must be a callable function."):
        Euler1D_Solve(10.0, t_start=0.0, t_end=5.0, y_0=1.0, num_steps=10)
    # f is a boolean
    with pytest.raises(TypeError, match="f must be a callable function."):
        Euler1D_Solve(True, t_start=0.0, t_end=5.0, y_0=1.0, num_steps=10)
    # f is a float
    with pytest.raises(TypeError, match="f must be a callable function."):
        Euler1D_Solve(11.3, t_start=0.0, t_end=5.0, y_0=1.0, num_steps=10)


def test_invalid_t_start_t_end_cases():
    # t_start is greater than t_end
    with pytest.raises(ValueError, match="t_start must be less than t_end."):
        Euler1D_Solve(f, t_start=5.0, t_end=0.0, y_0=1.0, num_steps=10)
    # t_start is a string
    with pytest.raises(TypeError, match="t_start and t_end must be numbers."):
        Euler1D_Solve(f, t_start="0.0", t_end=5.0, y_0=1.0, num_steps=10)
    # t_start is a boolean
    with pytest.raises(TypeError, match="t_start and t_end must be numbers."):
        Euler1D_Solve(f, t_start=0.0, t_end="5.0", y_0=1.0, num_steps=10)


def test_invalid_num_steps_cases():
    # num_steps is a negative integer
    with pytest.raises(ValueError, match="num_steps must be a pos integer."):
        Euler1D_Solve(f, t_start=0.0, t_end=5.0, y_0=1.0, num_steps=-10)
    # num_steps is zero
    with pytest.raises(ValueError, match="num_steps must be a pos integer."):
        Euler1D_Solve(f, t_start=0.0, t_end=5.0, y_0=1.0, num_steps=0)
    # num_steps is a float
    with pytest.raises(ValueError, match="num_steps must be a pos integer."):
        Euler1D_Solve(f, t_start=0.0, t_end=5.0, y_0=1.0, num_steps=3.5)
    # num_steps is boolean
    with pytest.raises(ValueError, match="num_steps must be a pos integer."):
        Euler1D_Solve(f, t_start=0.0, t_end=5.0, y_0=1.0, num_steps=False)
    # num_steps is a string
    with pytest.raises(ValueError, match="num_steps must be a pos integer."):
        Euler1D_Solve(f, t_start=0.0, t_end=5.0, y_0=1.0, num_steps="100")


def test_invalid_y_0_cases():
    # y_0 is a string
    with pytest.raises(TypeError, match="y_0 must be a real number."):
        Euler1D_Solve(f, t_start=0.0, t_end=5.0, y_0="1.0", num_steps=10)
    # y_0 is a boolean
    with pytest.raises(TypeError, match="y_0 must be a real number."):
        Euler1D_Solve(f, t_start=0.0, t_end=5.0, y_0=True, num_steps=10)
