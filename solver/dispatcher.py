from solver.greedy import solve_greedy
from solver.gurobi_solver import solve_gurobi_makespan

def solve_schedule(jobs, machines, solver="gurobi", use_lpt=False):
    if solver == "gurobi":
        return solve_gurobi_makespan(jobs=jobs, machines=machines)
    elif solver == "greedy":
        return solve_greedy(jobs=jobs, machines=machines, use_lpt=use_lpt)
    else:
        raise ValueError(f"Unknown solver: {solver}")