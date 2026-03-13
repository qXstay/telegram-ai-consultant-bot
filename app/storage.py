from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "leads.db"


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_user_id INTEGER NOT NULL,
                username TEXT,
                name TEXT NOT NULL,
                contact TEXT NOT NULL,
                task TEXT NOT NULL,
                comment TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.commit()


def save_lead(
    *,
    telegram_user_id: int,
    username: str | None,
    name: str,
    contact: str,
    task: str,
    comment: str,
) -> int:
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            INSERT INTO leads (
                telegram_user_id,
                username,
                name,
                contact,
                task,
                comment,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (telegram_user_id, username, name, contact, task, comment, created_at),
        )
        connection.commit()
        return int(cursor.lastrowid)
