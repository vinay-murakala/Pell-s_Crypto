import pytest
from src.pells_equation import solve_pells_equation

def test_solve_pells_equation():
    # Test case for D=2
    x, y = solve_pells_equation(2)
    assert x**2 - 2*y**2 == 1
    assert x == 3 and y == 2  # Fundamental solution for D=2

    # Test case for D=3
    x, y = solve_pells_equation(3)
    assert x**2 - 3*y**2 == 1
    assert x == 2 and y == 1  # Fundamental solution for D=3

def test_invalid_input():
    with pytest.raises(ValueError):
        solve_pells_equation(4)  # Perfect square
