from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter(prefix="/syllabus", tags=["Syllabus"])

SYLLABUS_FILE = Path("data/syllabus/gate_cs_2027.json")


@router.get("/")
def get_syllabus():
    with SYLLABUS_FILE.open("r", encoding="utf-8") as file:
        syllabus = json.load(file)

    return syllabus
