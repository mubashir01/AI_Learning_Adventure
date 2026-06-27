from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Score(Base):
    __tablename__ = "score"
    __table_args__ = (CheckConstraint("id = 1", name="ck_score_single_row"),)

    id = Column(Integer, primary_key=True)
    xp = Column(Integer, nullable=False)
    coins = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    streak = Column(Integer, nullable=False, server_default="0")
    badges = Column(Text, nullable=False, server_default="''")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)


class Question(Base):
    __tablename__ = "questions"
    __table_args__ = (UniqueConstraint("category", "difficulty", "question", name="uq_questions_key"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(Text, nullable=False)
    difficulty = Column(Text, nullable=False)
    question = Column(Text, nullable=False)
    options = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
