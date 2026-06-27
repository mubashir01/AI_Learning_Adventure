"""initial schema and data load

Revision ID: 001
Revises:
Create Date: 2026-06-26
"""
import csv
from pathlib import Path

import sqlalchemy as sa
from alembic import op

revision = "001"
down_revision = None
branch_labels = None
depends_on = None

_CSV = Path(__file__).resolve().parents[2] / "database" / "questions_clean.csv"


def upgrade() -> None:
    op.create_table(
        "score",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("xp", sa.Integer, nullable=False),
        sa.Column("coins", sa.Integer, nullable=False),
        sa.Column("level", sa.Integer, nullable=False),
        sa.Column("streak", sa.Integer, nullable=False, server_default="0"),
        sa.Column("badges", sa.Text, nullable=False, server_default="''"),
        sa.CheckConstraint("id = 1", name="ck_score_single_row"),
    )

    op.create_table(
        "skills",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.Text, nullable=False, unique=True),
    )

    op.create_table(
        "questions",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("category", sa.Text, nullable=False),
        sa.Column("difficulty", sa.Text, nullable=False),
        sa.Column("question", sa.Text, nullable=False),
        sa.Column("options", sa.Text, nullable=False),
        sa.Column("correct_answer", sa.Text, nullable=False),
        sa.Column("skill_id", sa.Integer, sa.ForeignKey("skills.id"), nullable=True),
        sa.UniqueConstraint("category", "difficulty", "question", name="uq_questions_key"),
    )

    bind = op.get_bind()
    bind.execute(
        sa.text(
            "INSERT INTO score (id, xp, coins, level, streak, badges) "
            "VALUES (1, 0, 0, 1, 0, '')"
        )
    )

    if not _CSV.exists():
        print(f"WARNING: {_CSV} not found — questions table left empty. Run scripts/clean_questions.py first.")
        return

    with _CSV.open(newline="", encoding="utf-8") as f:
        rows = [{**r, "id": int(r["id"])} for r in csv.DictReader(f)]

    if not rows:
        return

    bind.execute(
        sa.text(
            "INSERT INTO questions "
            "(id, category, difficulty, question, options, correct_answer) "
            "VALUES (:id, :category, :difficulty, :question, :options, :correct_answer)"
        ),
        rows,
    )

    if bind.engine.dialect.name == "postgresql":
        max_id = max(r["id"] for r in rows)
        bind.execute(sa.text(f"SELECT setval('questions_id_seq', {max_id})"))


def downgrade() -> None:
    op.drop_table("questions")
    op.drop_table("skills")
    op.drop_table("score")
