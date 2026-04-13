from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, field_validator 
# 这是Pydantic的数据模型作用是定义API输入格式，也就是告诉FastAPI 输入必须的类型

from solver.dispatcher import solve_schedule

app = FastAPI(title="Mini Scheduler")

class ScheduleRequest(BaseModel):
    jobs: list[int]
    machines: int
    solver: str = "greedy"
    use_lpt: bool = False
    
    @field_validator("jobs")
    @classmethod
    def validate_jobs(cls, v):
        if not v:
            raise ValueError("jobs list cannot be empty")
        if any(job <= 0 for job in v):
            raise ValueError("all job processing times must be positive integers")
        return v

    @field_validator("machines")
    @classmethod
    def validate_machines(cls, v):
        if v <= 0:
            raise ValueError("machines must be positive")
        return v

@app.get("/")
def root():
    return {"message": "mini_scheduler running"}


@app.post("/schedule")
def schedule(request: ScheduleRequest):
    try:

        return solve_schedule(
            jobs=request.jobs,
            machines=request.machines,
            solver=request.solver,
            use_lpt=request.use_lpt
        )
    except ValueError as e:
        # 400 Bad Request for invalid input
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        # 503 Service Unavailable for solver-related issues
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e: # 为了兜底程序内部意外
        # 500 Internal Server Error for any other unexpected issues
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")