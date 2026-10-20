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
# Daily caps stop XP farming (spamming chat or re-rolling the vocab quiz).
DAILY_XP_CAPS = {"chat message": 20, "vocabulary quiz": 50}


def level_for_xp(xp: int) -> str:
    for threshold, label in _LEVELS:
        if xp >= threshold:
            return label
    return "A1"


def level_progress(xp: int) -> tuple[str, str | None, int, int]:
    """Return (level, next_level, percent_to_next, xp_to_next)."""
    ordered = sorted(_LEVELS)  # ascending by threshold
    for i, (threshold, label) in enumerate(ordered):
        nxt = ordered[i + 1] if i + 1 < len(ordered) else None
        if nxt is None or xp < nxt[0]:
            if nxt is None:
                return label, None, 100, 0
            span = nxt[0] - threshold
            return label, nxt[1], round(100 * (xp - threshold) / span), nxt[0] - xp
    return "A1", None, 100, 0


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
        self._reconcile_lesson_xp()

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
                CREATE TABLE IF NOT EXISTS lesson_scores (
                    title TEXT PRIMARY KEY,
                    best_correct INTEGER NOT NULL,
                    total INTEGER NOT NULL,
                    xp_awarded INTEGER NOT NULL,
                    updated_at TEXT NOT NULL
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

    def _reconcile_lesson_xp(self) -> None:
        """Make lesson XP and completions match quiz results only.

        Older versions had a "mark as complete" button that gave full XP
        without a quiz. On every start this removes that unearned XP and
        those completions, so each lesson's XP equals its best quiz score.
        Safe to run repeatedly (does nothing when data is already consistent).
        """
        from content import LESSONS  # local import to avoid a cycle

        question_counts = {lesson.title: len(lesson.quiz) for lesson in LESSONS}
        with self._db() as conn:
            # A quiz that changed (different number of questions) must be retaken:
            # drop its old score so the XP below is recalculated from zero.
            for title, total in conn.execute("SELECT title, total FROM lesson_scores").fetchall():
                if question_counts.get(title) != total:
                    conn.execute("DELETE FROM lesson_scores WHERE title = ?", (title,))
            earned = dict(conn.execute("SELECT title, xp_awarded FROM lesson_scores").fetchall())
            rows = conn.execute(
                "SELECT reason, SUM(amount) FROM xp_events WHERE reason LIKE 'lesson: %' GROUP BY reason"
            ).fetchall()
            for reason, total in rows:
                title = reason[len("lesson: "):]
                should_be = earned.get(title, 0)
                if total != should_be:
                    conn.execute("DELETE FROM xp_events WHERE reason = ?", (reason,))
                    if should_be:
                        conn.execute(
                            "INSERT INTO xp_events (amount, reason, created_at) VALUES (?, ?, ?)",
                            (should_be, reason, _now()),
                        )
            # A lesson only counts as done if it has a quiz score.
            conn.execute("DELETE FROM lessons_done WHERE title NOT IN (SELECT title FROM lesson_scores)")

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

    def xp_today(self, reason: str) -> int:
        """XP earned today (local time) for one reason."""
        midnight = datetime.now().astimezone().replace(hour=0, minute=0, second=0, microsecond=0)
        since = midnight.astimezone(timezone.utc).isoformat(timespec="seconds")
        with self._db() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) FROM xp_events WHERE reason = ? AND created_at >= ?",
                (reason, since),
            ).fetchone()
        return int(row[0])

    def add_xp_capped(self, amount: int, reason: str) -> int:
        """Add XP but respect the daily cap for this reason. Returns XP granted."""
        cap = DAILY_XP_CAPS.get(reason)
        if cap is not None:
            amount = max(0, min(amount, cap - self.xp_today(reason)))
        if amount:
            self.add_xp(amount, reason)
        return amount

    def clear_messages(self) -> None:
        with self._db() as conn:
            conn.execute("DELETE FROM messages")

    def total_xp(self) -> int:
        with self._db() as conn:
            row = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM xp_events").fetchone()
        return int(row[0])

    # -- lessons ------------------------------------------------------------
    def record_lesson_quiz(
        self, title: str, correct: int, total: int, max_xp: int, pass_ratio: float
    ) -> dict:
        """Score a lesson quiz attempt.

        XP is proportional to correct answers (max_xp * correct / total).
        Only the best attempt counts: retrying gives just the extra XP above
        what was already earned, so a lesson can never pay out more than max_xp.
        The lesson counts as completed once a score reaches pass_ratio.
        """
        if total <= 0:
            return {"gained": 0, "earned": 0, "best": 0, "total": 0, "passed": False, "improved": False}
        earned_now = round(max_xp * correct / total)
        with self._db() as conn:
            row = conn.execute(
                "SELECT best_correct, xp_awarded FROM lesson_scores WHERE title = ?", (title,)
            ).fetchone()
            prev_best, prev_xp = row if row else (0, 0)
            gained = max(0, earned_now - prev_xp)
            best = max(prev_best, correct)
            if gained:
                conn.execute(
                    "INSERT INTO xp_events (amount, reason, created_at) VALUES (?, ?, ?)",
                    (gained, f"lesson: {title}", _now()),
                )
            conn.execute(
                "INSERT INTO lesson_scores (title, best_correct, total, xp_awarded, updated_at) "
                "VALUES (?, ?, ?, ?, ?) ON CONFLICT(title) DO UPDATE SET "
                "best_correct = excluded.best_correct, total = excluded.total, "
                "xp_awarded = excluded.xp_awarded, updated_at = excluded.updated_at",
                (title, best, total, prev_xp + gained, _now()),
            )
            passed = best / total >= pass_ratio
            if passed:
                conn.execute(
                    "INSERT OR IGNORE INTO lessons_done (title, completed_at) VALUES (?, ?)",
                    (title, _now()),
                )
        return {
            "gained": gained,
            "earned": prev_xp + gained,
            "best": best,
            "total": total,
            "passed": passed,
            "improved": correct > prev_best,
        }

    def lesson_scores(self) -> dict[str, tuple[int, int, int]]:
        """title -> (best_correct, total, xp_awarded)."""
        with self._db() as conn:
            rows = conn.execute(
                "SELECT title, best_correct, total, xp_awarded FROM lesson_scores"
            ).fetchall()
        return {t: (b, n, x) for t, b, n, x in rows}

    def reset_lesson(self, title: str) -> bool:
        """Remove a lesson's completion, best score and all its XP."""
        with self._db() as conn:
            done = conn.execute("DELETE FROM lessons_done WHERE title = ?", (title,)).rowcount
            scored = conn.execute("DELETE FROM lesson_scores WHERE title = ?", (title,)).rowcount
            conn.execute("DELETE FROM xp_events WHERE reason = ?", (f"lesson: {title}",))
        return bool(done or scored)

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
