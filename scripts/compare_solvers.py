import time

from solver.greedy import solve_greedy
from solver.ortools_solver import solve_ortools_makespan
from solver.gurobi_solver import solve_gurobi_makespan

def run_solver(name, func, jobs, machines, **kwargs):
    start_time = time.perf_counter()
    try:
        result = func(jobs=jobs, machines=machines, **kwargs)
        runtime = time.perf_counter() - start_time
        return {
            "solver": name,
            "status": result.get("status", "unknown"),
            "makespan": result.get("makespan"),
            "loads": result.get("loads"),
            "runtime_sec": round(runtime, 6)
        }
    except Exception as e:
        runtime = time.perf_counter() - start_time
        return {
            "solver": name,
            "status": f"error: {str(e)}",
            "makespan": None,
            "loads": None,
            "runtime_sec": round(runtime, 6)
        }

def main():
    jobs = [3, 2, 7, 5, 1, 4]
    machines = 3

    solvers = [
        ("greedy", solve_greedy, {"use_lpt": True}),
        ("ortools", solve_ortools_makespan, {}),
        ("gurobi", solve_gurobi_makespan, {})
    ]

    results = []
    for name, func, kwargs in solvers:
        result = run_solver(name, func, jobs, machines, **kwargs)
        results.append(result)

    print(f"{'solver':<10} {'status':<20} {'makespan':<10} {'runtime_sec':<12} loads")
    print("-" * 70)

    for r in results:
        print(
            f"{r['solver']:<10} "
            f"{str(r['status']):<20} "
            f"{str(r['makespan']):<10} "
            f"{str(r['runtime_sec']):<12} "
            f"{r['loads']}"
        )

if __name__ == "__main__":
    main()