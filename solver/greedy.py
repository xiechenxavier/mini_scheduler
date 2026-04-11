def solve_greedy(jobs,machines,use_lpt=False):
    # 初始化每台机器
    if use_lpt:
        jobs = sorted(jobs, reverse = True)
    loads = [0] * machines
    assignment = [[] for _ in range(machines)]

    for job in jobs:
        # 找负载最小的机器
        min_idx = loads.index(min(loads))

        # 分配任务
        assignment[min_idx].append(job)
        loads[min_idx] += job
    
    return {
        "assignment": assignment,
        "makespan": max(loads),
        "loads": loads
    }