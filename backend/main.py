from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from database.sqlite import (
    get_categories,
    get_difficulties,
    get_random_question,
    get_score,
    init_db,
    submit_answer,
)

app = FastAPI(title="AI Learning Adventure")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/score")
def score() -> dict[str, int]:
    return get_score()


@app.get("/categories")
def categories() -> list[str]:
    return get_categories()


@app.get("/difficulties")
def difficulties() -> list[str]:
    return get_difficulties()


@app.get("/questions/random")
def random_question(category: str, difficulty: str) -> dict[str, object]:
    return get_random_question(category, difficulty)


class AnswerRequest(BaseModel):
    question_id: int
    answer: str
    time_left: int


@app.post("/answers")
def answer(payload: AnswerRequest) -> dict[str, object]:
    return submit_answer(payload.question_id, payload.answer, payload.time_left)
