from fastapi import FastAPI

app = FastAPI(title="Mini Scheduler")

@app.get("/")
def root():
    return {"message": "mini_scheduler running"}