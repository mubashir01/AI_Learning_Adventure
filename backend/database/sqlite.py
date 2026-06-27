import shutil
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path
from random import choice, shuffle

from database.db import SessionLocal
from database.models import Question, Score
from services.badges import calculate_badges
from services.coins import calculate_coins
from services.levels import calculate_level
from services.streaks import calculate_streak
from services.xp import calculate_xp

RECENT_QUESTIONS = defaultdict(lambda: deque(maxlen=12))


def _backup_pre_migration(db_path: Path) -> None:
    if not db_path.exists():
        return
    import sqlite3
    try:
        with sqlite3.connect(db_path) as conn:
            tables = {
                r[0]
                for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            }
            if "alembic_version" not in tables:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                shutil.copy2(db_path, db_path.with_name(f"app.db.bak-{ts}"))
    except Exception:
        pass


def _run_migrations() -> None:
    from alembic import command
    from alembic.config import Config
    cfg = Config(Path(__file__).resolve().parents[1] / "alembic.ini")
    command.upgrade(cfg, "head")


def init_db() -> None:
    from config import DATABASE_URL
    if DATABASE_URL.startswith("sqlite:///"):
        raw = DATABASE_URL[len("sqlite:///"):]
        db_path = Path(raw) if Path(raw).is_absolute() else Path.cwd() / raw
        db_path.parent.mkdir(parents=True, exist_ok=True)
        _backup_pre_migration(db_path)

    _run_migrations()

    db = SessionLocal()
    try:
        if db.get(Score, 1) is None:
            db.add(Score(id=1, xp=0, coins=0, level=1, streak=0, badges=""))
            db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_score() -> dict[str, object]:
    db = SessionLocal()
    try:
        row = db.get(Score, 1)
        if row is None:
            return {"xp": 0, "coins": 0, "level": 1, "streak": 0, "badges": []}
        return {
            "xp": row.xp,
            "coins": row.coins,
            "level": row.level,
            "streak": row.streak,
            "badges": row.badges.split(",") if row.badges else [],
        }
    finally:
        db.close()


def get_categories() -> list[str]:
    db = SessionLocal()
    try:
        rows = db.query(Question.category).distinct().order_by(Question.category).all()
        return [r[0] for r in rows]
    finally:
        db.close()


def get_difficulties() -> list[str]:
    return ["Easy", "Medium", "Hard"]


def get_random_question(category: str, difficulty: str) -> dict[str, object]:
    db = SessionLocal()
    try:
        rows = (
            db.query(Question)
            .filter(Question.category == category, Question.difficulty == difficulty)
            .all()
        )
    finally:
        db.close()

    if not rows:
        return {}

    recent_key = (category, difficulty)
    recent = RECENT_QUESTIONS[recent_key]
    candidates = [r for r in rows if r.id not in recent] or rows
    row = choice(candidates)
    recent.append(row.id)

    options = [o for o in row.options.split("|") if o]
    if row.correct_answer and row.correct_answer not in options:
        options.append(row.correct_answer)
    shuffle(options)

    return {
        "id": row.id,
        "category": row.category,
        "difficulty": row.difficulty,
        "question": row.question,
        "options": options,
        "seconds": 30,
    }


def submit_answer(question_id: int, answer: str, time_left: int) -> dict[str, object]:
    db = SessionLocal()
    try:
        q_row = db.get(Question, question_id)
        if q_row is None:
            return {
                "correct": False,
                "correct_answer": "",
                "earned_xp": 0,
                "earned_coins": 0,
                "score": get_score(),
            }

        correct_answer = q_row.correct_answer or ""
        correct = answer == correct_answer
        earned_xp = calculate_xp(correct, time_left)
        earned_coins = calculate_coins(correct)

        score_row = db.get(Score, 1)
        next_streak = calculate_streak(score_row.streak, correct)
        next_badges = calculate_badges(score_row.badges, 100 if correct else 0)

        if correct:
            next_level = calculate_level(score_row.xp + earned_xp)
            score_row.xp = score_row.xp + earned_xp
            score_row.coins = score_row.coins + earned_coins
            score_row.level = next_level
            score_row.streak = next_streak
            score_row.badges = next_badges
        else:
            score_row.streak = next_streak
            score_row.badges = next_badges

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    return {
        "correct": correct,
        "correct_answer": correct_answer,
        "earned_xp": earned_xp,
        "earned_coins": earned_coins,
        "score": get_score(),
    }
