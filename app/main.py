from fastapi import FastAPI
from pydantic import BaseModel 
# 这是Pydantic的数据模型作用是定义API输入格式，也就是告诉FastAPI 输入必须的类型

from solver.dispatcher import solve_schedule

app = FastAPI(title="Mini Scheduler")

class ScheduleRequest(BaseModel):
    jobs: list[int]
    machines: int
    solver: str = "greedy"
    use_lpt: bool = False

@app.get("/")
def root():
    return {"message": "mini_scheduler running"}


@app.post("/schedule")
def schedule(request: ScheduleRequest):
    print(f"Received request: {request}")
    result = solve_schedule(
        jobs=request.jobs,
        machines=request.machines,
        solver=request.solver,
        use_lpt=request.use_lpt
    )
    return result