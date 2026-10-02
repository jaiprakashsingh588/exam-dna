from fastapi import FastAPI
from backend.app.routes.health import router as health_router
from backend.app.routes.questions import router as questions_router

app = FastAPI(title="ExamDNA API")

app.include_router(health_router)
app.include_router(questions_router)

@app.get("/")
def root():
    return {"message": "ExamDNA API is running"}
