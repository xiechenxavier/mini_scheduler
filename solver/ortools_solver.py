from ortools.sat.python import cp_model

def solve_ortools_makespan(jobs,machines):
    if machines <= 0:
        raise ValueError("machines must be positive")
    if not jobs:
        return {
            "assignment": [[] for _ in range(machines)],
            "makespan": 0,
            "loads": [0] * machines
        }
    
    n = len(jobs)
    m = machines

    model = cp_model.CpModel() # 创建一个新的CP模型

    x = {}
    for i in range(m):
        for j in range(n):
            x[i, j] = model.NewBoolVar(f"x_{i}_{j}")

    cmax = model.NewIntVar(0, sum(jobs), "cmax")

    for j in range(n): # 每个任务必须分配给且仅分配给一台机器
        model.Add(sum(x[i, j] for i in range(m)) == 1)

    for i in range(m):
        model.Add(sum(jobs[j] * x[i, j] for j in range(n)) <= cmax)

    model.Minimize(cmax)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status != cp_model.OPTIMAL: # 如果求解状态不是最优，返回状态信息
        return {"status": str(status)}
    # 反之则构建结果，包括每台机器的任务分配、负载和总完成时间（makespan）
    assignment = [[] for _ in range(m)]
    loads = [0] * m

    for i in range(m):
        for j in range(n):
            if solver.Value(x[i, j]) == 1: # 如果x[i,j]的值为1，表示任务j被分配给了机器i
                assignment[i].append(jobs[j])
                loads[i] += jobs[j]

    return {
        "assignment": assignment,
        "makespan": solver.Value(cmax),
        "loads": loads,
        "status": "optimal"
    }