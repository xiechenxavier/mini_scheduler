import pytest

from solver.dispatcher import solve_schedule


def test_dispatcher_greedy():
    result = solve_schedule([3, 5, 2, 7], 2, solver="greedy")

    assert result["makespan"] == 12
    assert sum(result["loads"]) == 17


def test_dispatcher_ortools():
    result = solve_schedule([3, 5, 2, 7], 2, solver="ortools")

    assert result["makespan"] == 9
    assert sum(result["loads"]) == 17


def test_dispatcher_invalid_solver():
    with pytest.raises(ValueError, match="Unsupported solver: abc"):
        solve_schedule([3, 5, 2, 7], 2, solver="abc")