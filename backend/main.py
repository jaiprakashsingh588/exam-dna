from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.app.routes.health import router as health_router
from backend.app.routes.questions import router as questions_router
from backend.app.routes.syllabus import router as syllabus_router

app = FastAPI(title="ExamDNA API")

app.include_router(health_router)
app.include_router(questions_router)
app.include_router(syllabus_router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
