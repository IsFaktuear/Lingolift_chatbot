"""Local persistence for LingoLift.

Stores chat history, XP, completed lessons and the vocabulary bank in a
small SQLite database (stdlib only, no new dependencies). The database
lives under <repo>/data/ so it never gets committed.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from models import VocabularyWord

DB_PATH = Path(__file__).resolve().parent / "data" / "lingolift.db"

# XP thresholds -> CEFR-ish level label shown on the dashboard.
_LEVELS = [
    (700, "C1"),
    (350, "B2"),
    (150, "B1"),
    (50, "A2"),
    (0, "A1"),
]

XP_PER_CHAT_MESSAGE = 2


def level_for_xp(xp: int) -> str:
    for threshold, label in _LEVELS:
        if xp >= threshold:
            return label
    return "A1"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Store:
    """Thin SQLite wrapper. Opens a short-lived connection per operation so
    it stays safe across Streamlit reruns."""

    def __init__(self, path: Path | str = DB_PATH) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()
        self._seed_vocabulary()

    @contextmanager
    def _db(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_schema(self) -> None:
        with self._db() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS xp_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS lessons_done (
                    title TEXT PRIMARY KEY,
                    completed_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS vocabulary (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phrase TEXT NOT NULL UNIQUE,
                    meaning TEXT NOT NULL,
                    example TEXT NOT NULL,
                    level TEXT NOT NULL DEFAULT 'B1',
                    created_at TEXT NOT NULL
                );
                """
            )

    def _seed_vocabulary(self) -> None:
        # First run only: copy the built-in word list so the bank is not empty.
        from content import VOCABULARY  # local import to avoid a cycle

        with self._db() as conn:
            count = conn.execute("SELECT COUNT(*) FROM vocabulary").fetchone()[0]
            if count:
                return
            for word in VOCABULARY:
                conn.execute(
                    "INSERT OR IGNORE INTO vocabulary "
                    "(phrase, meaning, example, level, created_at) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (word.phrase, word.meaning, word.example, word.level, _now()),
                )

    # -- chat history ----------------------------------------------------
    def add_message(self, role: str, content: str) -> None:
        with self._db() as conn:
            conn.execute(
                "INSERT INTO messages (role, content, created_at) VALUES (?, ?, ?)",
                (role, content, _now()),
            )

    def get_messages(self) -> list[dict[str, str]]:
        with self._db() as conn:
            rows = conn.execute(
                "SELECT role, content FROM messages ORDER BY id ASC"
            ).fetchall()
        return [{"role": role, "content": content} for role, content in rows]

    # -- XP ----------------------------------------------------------------
    def add_xp(self, amount: int, reason: str) -> None:
        with self._db() as conn:
            conn.execute(
                "INSERT INTO xp_events (amount, reason, created_at) VALUES (?, ?, ?)",
                (amount, reason, _now()),
            )

    def total_xp(self) -> int:
        with self._db() as conn:
            row = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM xp_events").fetchone()
        return int(row[0])

    # -- lessons ------------------------------------------------------------
    def complete_lesson(self, title: str, xp: int) -> bool:
        """Mark a lesson done and award XP. Returns True if this was new."""
        with self._db() as conn:
            cur = conn.execute(
                "INSERT OR IGNORE INTO lessons_done (title, completed_at) VALUES (?, ?)",
                (title, _now()),
            )
            if cur.rowcount:
                conn.execute(
                    "INSERT INTO xp_events (amount, reason, created_at) VALUES (?, ?, ?)",
                    (xp, f"lesson: {title}", _now()),
                )
                return True
        return False

    def lessons_done(self) -> set[str]:
        with self._db() as conn:
            rows = conn.execute("SELECT title FROM lessons_done").fetchall()
        return {row[0] for row in rows}

    # -- vocabulary ----------------------------------------------------------
    def add_word(self, phrase: str, meaning: str, example: str, level: str = "B1") -> bool:
        """Returns False when the phrase is already in the bank."""
        with self._db() as conn:
            cur = conn.execute(
                "INSERT OR IGNORE INTO vocabulary "
                "(phrase, meaning, example, level, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (phrase.strip(), meaning.strip(), example.strip(), level, _now()),
            )
            return cur.rowcount > 0

    def get_words(self) -> list[VocabularyWord]:
        with self._db() as conn:
            rows = conn.execute(
                "SELECT phrase, meaning, example, level FROM vocabulary ORDER BY id ASC"
            ).fetchall()
        return [
            VocabularyWord(phrase=p, meaning=m, example=e, level=lv)
            for p, m, e, lv in rows
        ]


def get_store(path: Path | str = DB_PATH) -> Store:
    return Store(path)
