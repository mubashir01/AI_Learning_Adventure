"""
Usage: python -m scripts.clean_questions [db_path]

  db_path: path to SQLite database to clean
           (default: latest app.db.bak-* in database/)

Outputs:
  backend/database/questions_clean.csv
  backend/clean_review.log  (only written when divergent options/answers exist)
"""
import csv
import sqlite3
import sys
from pathlib import Path

_BACKEND = Path(__file__).resolve().parents[1]
_DB_DIR = _BACKEND / "database"
_CSV_PATH = _DB_DIR / "questions_clean.csv"
_LOG_PATH = _BACKEND / "clean_review.log"


def _find_backup() -> Path:
    backups = sorted(_DB_DIR.glob("app.db.bak-*"))
    if not backups:
        raise FileNotFoundError(f"No app.db.bak-* found in {_DB_DIR}")
    return backups[-1]


def main() -> None:
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else _find_backup()
    print(f"Source: {db_path}")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    rows = cur.execute(
        "SELECT id, category, difficulty, question, options, correct_answer "
        "FROM questions ORDER BY id"
    ).fetchall()
    before = len(rows)
    print(f"Before: {before} questions")

    groups: dict[tuple, list] = {}
    for row in rows:
        row_id, category, difficulty, question, options, correct_answer = row
        key = (
            category.lower().strip(),
            difficulty.lower().strip(),
            question.lower().strip(),
        )
        groups.setdefault(key, []).append(row)

    log_lines: list[str] = []
    ids_to_delete: list[int] = []

    for key, group_rows in groups.items():
        if len(group_rows) == 1:
            continue
        group_rows.sort(key=lambda r: r[0])
        keep = group_rows[0]
        for dup in group_rows[1:]:
            if dup[4] != keep[4] or dup[5] != keep[5]:
                log_lines.append(
                    f"DIVERGENT GROUP key={key!r}\n"
                    f"  KEEP id={keep[0]}: options={keep[4]!r} answer={keep[5]!r}\n"
                    f"  DROP id={dup[0]}: options={dup[4]!r} answer={dup[5]!r}\n"
                )
            ids_to_delete.append(dup[0])

    if log_lines:
        _LOG_PATH.write_text("\n".join(log_lines), encoding="utf-8")
        print(f"Divergent groups: {len(log_lines)} -> {_LOG_PATH}")

    if ids_to_delete:
        cur.executemany("DELETE FROM questions WHERE id = ?", [(i,) for i in ids_to_delete])
        conn.commit()

    remaining = cur.execute(
        "SELECT category, difficulty, question, options, correct_answer "
        "FROM questions ORDER BY id"
    ).fetchall()
    after = len(remaining)
    print(f"After:  {after} questions (removed {before - after} duplicates)")

    cur.execute("DELETE FROM questions")
    cur.execute("DELETE FROM sqlite_sequence WHERE name='questions'")
    cur.executemany(
        "INSERT INTO questions (id, category, difficulty, question, options, correct_answer) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        [(new_id, *row) for new_id, row in enumerate(remaining, 1)],
    )
    conn.commit()

    dup_count = cur.execute(
        """
        SELECT COUNT(*) FROM (
            SELECT lower(trim(category)), lower(trim(difficulty)), lower(trim(question))
            FROM questions
            GROUP BY lower(trim(category)), lower(trim(difficulty)), lower(trim(question))
            HAVING COUNT(*) > 1
        )
        """
    ).fetchone()[0]
    assert dup_count == 0, f"Still {dup_count} duplicate groups after cleaning!"

    final_rows = cur.execute(
        "SELECT id, category, difficulty, question, options, correct_answer "
        "FROM questions ORDER BY id"
    ).fetchall()

    _CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "category", "difficulty", "question", "options", "correct_answer"])
        writer.writerows(final_rows)

    print(f"Exported {len(final_rows)} questions -> {_CSV_PATH}")
    conn.close()


if __name__ == "__main__":
    main()
