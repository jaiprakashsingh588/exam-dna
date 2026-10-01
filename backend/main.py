from fastapi import FastAPI

app = FastAPI(title="ExamDNA API")

@app.get("/")
def root():
    return {"message": "ExamDNA API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
