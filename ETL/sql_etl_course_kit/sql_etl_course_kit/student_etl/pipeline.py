"""Student database ETL: raw CSV -> clean SQLite, CSV and Excel."""
import json
import logging
import os
import sqlite3
import uuid
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
FMT = "%(asctime)s %(levelname)s %(message)s"
log = logging.getLogger("student_etl")


class ValidationError(Exception):
    """Raised when the data fails a critical check."""


def load_config(path: Path = BASE / "config.json") -> dict:
    cfg = json.loads(path.read_text())
    for key in ("raw_file", "db_file", "export_dir"):
        cfg[key] = BASE / cfg[key]          # relative -> absolute
    cfg["log_level"] = os.getenv("ETL_LOG_LEVEL", cfg["log_level"])
    return cfg


def extract(csv_path: Path) -> pd.DataFrame:
    """Read the raw CSV as text, exactly as it is."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing file: {csv_path}")
    df = pd.read_csv(csv_path, dtype=str)
    log.info("Extracted %d rows from %s",
             len(df), csv_path.name)
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Clean formats. Never changes the input DataFrame."""
    df = df.copy()
    df["name"] = df["name"].str.strip().str.title()
    df["email"] = df["email"].str.strip().str.lower()
    df["city"] = df["city"].str.strip().str.title()
    df["marks_raw"] = df["marks"]            # keep for audit
    df["marks"] = pd.to_numeric(df["marks"], errors="coerce")
    df["student_id"] = df["student_id"].astype(int)
    df["course_id"] = df["course"].astype(int)
    before = len(df)
    df = df.drop_duplicates(subset=["student_id", "course_id"])
    log.info("Removed %d duplicate rows", before - len(df))
    return df


def validate(df: pd.DataFrame, lo: float, hi: float):
    """Return (good, rejects); each reject gets a reason."""
    reason = pd.Series("", index=df.index)
    not_num = df["marks_raw"].notna() & df["marks"].isna()
    in_range = df["marks"].between(lo, hi)
    out_rng = df["marks"].notna() & ~in_range
    reason[not_num] = "marks not a number"
    reason[out_rng] = "marks out of range"
    bad = reason != ""
    rejects = df[bad].assign(reason=reason[bad])
    good = df[~bad]
    if good.empty:
        raise ValidationError("No valid rows left")
    log.info("Validation: %d valid, %d rejected",
             len(good), len(rejects))
    return good, rejects


def add_lineage(df: pd.DataFrame, source: str, run_id: str) -> pd.DataFrame:
    now = datetime.now(timezone.utc)
    stamp = now.isoformat(timespec="seconds")
    return df.assign(source_file=source, run_id=run_id,
                     loaded_at=stamp)


def load(df: pd.DataFrame, db_path: Path) -> None:
    cols = ["student_id", "name", "email", "city", "dept"]
    students = df[cols].drop_duplicates("student_id")
    enrol = df[["student_id", "course_id", "marks",
                "source_file", "run_id", "loaded_at"]]
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(db_path)) as con, con:
        for name, table in [("students", students),
                            ("enrollments", enrol)]:
            table.to_sql(name, con, if_exists="replace",
                         index=False)
    log.info("Loaded %d students, %d enrollments",
             len(students), len(enrol))


def export(df: pd.DataFrame, rejects: pd.DataFrame, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "students_clean.csv", index=False)
    df.to_excel(out_dir / "students_clean.xlsx", index=False)
    rejects.to_csv(out_dir / "rejects.csv", index=False)
    log.info("Exported CSV, Excel and rejects to %s", out_dir.name)


def run() -> None:
    cfg = load_config()
    logging.basicConfig(level=cfg["log_level"], format=FMT)
    run_id = uuid.uuid4().hex[:8]
    log.info("Run %s started", run_id)
    try:
        raw = extract(cfg["raw_file"])
        clean = transform(raw)
        good, rejects = validate(clean, *cfg["marks_range"])
        good = add_lineage(good, cfg["raw_file"].name, run_id)
        load(good, cfg["db_file"])
        export(good, rejects, cfg["export_dir"])
    except Exception:
        log.exception("Run %s failed", run_id)
        raise
    log.info("Run %s finished OK", run_id)


if __name__ == "__main__":
    run()
