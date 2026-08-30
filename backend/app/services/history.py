import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from app.models.analysis import ResumeAnalysis
from app.models.career_guidance import CareerGuidance
from app.models.history import HistoryDetail, HistorySummary

DATABASE_PATH = Path(__file__).resolve().parents[2] / "data" / "history.sqlite3"


def _connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("""CREATE TABLE IF NOT EXISTS analysis_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL, target_role TEXT NOT NULL,
        job_description TEXT NOT NULL, resume_name TEXT, analysis_json TEXT NOT NULL, career_plan_json TEXT)""")
    return connection


def _target_role(job_description: str) -> str:
    first_line = next((line.strip() for line in job_description.splitlines() if line.strip()), "Target role")
    return re.sub(r"\s+", " ", first_line)[:100]


def save_analysis(analysis: ResumeAnalysis, job_description: str, resume_name: str | None) -> int:
    with _connection() as connection:
        cursor = connection.execute("INSERT INTO analysis_history (created_at, target_role, job_description, resume_name, analysis_json) VALUES (?, ?, ?, ?, ?)", (datetime.now(timezone.utc).isoformat(), _target_role(job_description), job_description[:4000], resume_name, analysis.model_dump_json()))
        return cursor.lastrowid


def _summary(row: sqlite3.Row) -> HistorySummary:
    analysis = ResumeAnalysis.model_validate_json(row["analysis_json"])
    return HistorySummary(id=row["id"], created_at=datetime.fromisoformat(row["created_at"]), target_role=row["target_role"], match_score=analysis.match_score, matching_skill_count=len(analysis.matching_skills), skill_gap_count=len(analysis.missing_skills))


def list_history() -> list[HistorySummary]:
    with _connection() as connection:
        return [_summary(row) for row in connection.execute("SELECT * FROM analysis_history ORDER BY id DESC")]


def get_history(analysis_id: int) -> HistoryDetail | None:
    with _connection() as connection:
        row = connection.execute("SELECT * FROM analysis_history WHERE id = ?", (analysis_id,)).fetchone()
    if row is None:
        return None
    summary = _summary(row)
    return HistoryDetail(**summary.model_dump(), job_description=row["job_description"], resume_name=row["resume_name"], analysis=ResumeAnalysis.model_validate_json(row["analysis_json"]), career_plan=CareerGuidance.model_validate_json(row["career_plan_json"]) if row["career_plan_json"] else None)


def delete_history(analysis_id: int) -> bool:
    with _connection() as connection:
        return connection.execute("DELETE FROM analysis_history WHERE id = ?", (analysis_id,)).rowcount > 0


def attach_career_plan(analysis: ResumeAnalysis, plan: CareerGuidance) -> None:
    with _connection() as connection:
        connection.execute("UPDATE analysis_history SET career_plan_json = ? WHERE id = (SELECT id FROM analysis_history WHERE analysis_json = ? ORDER BY id DESC LIMIT 1)", (plan.model_dump_json(), analysis.model_dump_json()))
