from solver.greedy import solve_greedy


def test_greedy_returns_valid_result():
    result = solve_greedy([3, 5, 2, 7], 2)

    assert "assignment" in result
    assert "makespan" in result
    assert "loads" in result
    assert result["makespan"] == 12
    assert sum(result["loads"]) == 17


def test_greedy_with_lpt():
    result = solve_greedy([3, 5, 2, 7], 2, use_lpt=True)

    assert "makespan" in result
    assert sum(result["loads"]) == 17
    assert result["makespan"] <= 12


def test_greedy_invalid_machines():
    try:
        solve_greedy([3, 5], 0)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "machines must be positive"