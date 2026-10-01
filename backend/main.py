from fastapi import FastAPI
from backend.app.routes.health import router as health_router

app = FastAPI(title="ExamDNA API")

app.include_router(health_router)

@app.get("/")
def root():
    return {"message": "ExamDNA API is running"}
