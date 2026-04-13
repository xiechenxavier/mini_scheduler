try:
    import gurobipy as gp
    from gurobipy import GRB
except ImportError:
    gp = None
    GRB = None


def solve_gurobi_makespan(jobs, machines):
    if gp is None or GRB is None:
        raise RuntimeError("Gurobi is not available in the current environment.")

    if machines <= 0:
        raise ValueError("machines must be positive")
    if not jobs:
        return {
            "assignment": [[] for _ in range(machines)],
            "makespan": 0,
            "loads": [0] * machines,
            "status": "optimal",
        }

    n = len(jobs)
    m = machines

    model = gp.Model("makespan")
    model.setParam("OutputFlag", 0)

    x = model.addVars(m, n, vtype=GRB.BINARY, name="x")
    cmax = model.addVar(vtype=GRB.CONTINUOUS, name="Cmax")

    for j in range(n):
        model.addConstr(sum(x[i, j] for i in range(m)) == 1, name=f"assign_{j}")

    for i in range(m):
        model.addConstr(
            sum(jobs[j] * x[i, j] for j in range(n)) <= cmax,
            name=f"load_{i}",
        )

    model.setObjective(cmax, GRB.MINIMIZE)
    model.optimize()

    if model.status != GRB.OPTIMAL:
        return {"status": str(model.status)}

    assignment = [[] for _ in range(m)]
    loads = [0] * m

    for i in range(m):
        for j in range(n):
            if x[i, j].X > 0.5:
                assignment[i].append(jobs[j])
                loads[i] += jobs[j]

    return {
        "assignment": assignment,
        "makespan": cmax.X,
        "loads": loads,
        "status": "optimal",
    }