from solver.ortools_solver import solve_ortools_makespan


def test_ortools_returns_optimal_result():
    result = solve_ortools_makespan([3, 5, 2, 7], 2)

    assert result["status"] in ("optimal", "feasible")
    assert result["makespan"] == 9
    assert sum(result["loads"]) == 17


def test_ortools_empty_jobs():
    result = solve_ortools_makespan([], 2)

    assert result["status"] == "optimal"
    assert result["makespan"] == 0
    assert result["loads"] == [0, 0]