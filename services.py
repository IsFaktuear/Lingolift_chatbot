import os
import sys
from pathlib import Path
from typing import Any, Iterator

from dotenv import load_dotenv

try:
    from openai import OpenAI

    OPENAI_IMPORT_ERROR = None
except Exception as exc:  # not installed, or installed but broken
    OpenAI = None
    OPENAI_IMPORT_ERROR = f"{type(exc).__name__}: {exc}"

# Always read the .env next to this file, no matter which folder the app is
# started from. override=True: values in .env win over old system variables.
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH, override=True)

# Only the most recent turns are sent to the model, so cost and latency
# stay flat no matter how long the saved history grows.
MAX_HISTORY_MESSAGES = 20


class TutorError(Exception):
    """Raised when the AI service cannot produce a reply."""


class TutorService:
    DEMO_MESSAGE = (
        "Demo mode: I am your English tutor. Add `OPENAI_API_KEY` to your `.env` file "
        "to activate live AI conversations. Demo chats are not saved and give no XP."
    )
    SYSTEM_MESSAGE = (
        "You are LingoLift, a warm English tutor. Reply mostly in English, "
        "adjusting to the learner's level. Correct mistakes gently, explain "
        "useful points when they matter, and respond naturally to what the learner "
        "actually said. Keep simple replies short, but use a few paragraphs when "
        "the learner asks for an explanation. Do not force a practice question at "
        "the end of every reply, and avoid repetitive filler."
    )

    def __init__(self) -> None:
        self.api_key = (os.getenv("OPENAI_API_KEY") or "").strip() or None
        # Empty/unset -> the official OpenAI endpoint. Set OPENAI_BASE_URL
        # explicitly to use another OpenAI-compatible provider, so your key is
        # never sent to a third party by accident.
        self.base_url = os.getenv("OPENAI_BASE_URL") or None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def setup_problem(self) -> str | None:
        """Explain in plain words why live AI is off, or None when it is on."""
        if OpenAI is None:
            return (
                f"The `openai` package can't be loaded by the Python running this app: `{sys.executable}` "
                f"({OPENAI_IMPORT_ERROR}). Install it into THAT Python: "
                f"`\"{sys.executable}\" -m pip install -r requirements.txt`"
            )
        if self.api_key:
            return None
        if not ENV_PATH.exists():
            return f"No `.env` file found. Create it here: `{ENV_PATH}`"
        return "`.env` was found, but `OPENAI_API_KEY` is empty or missing in it."

    @property
    def is_live(self) -> bool:
        return bool(self.api_key) and OpenAI is not None

    def _client(self) -> Any:
        if not self.is_live:
            return None
        return OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=30.0,
            max_retries=1,
        )

    def reply_stream(self, messages: list[dict[str, str]]) -> Iterator[str]:
        """Yield the assistant reply in chunks. Raises TutorError on failure,
        so callers can avoid saving an error message as if it were a reply."""
        client = self._client()
        if client is None:
            raise TutorError("No API key configured.")
        try:
            stream = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_MESSAGE},
                    *messages[-MAX_HISTORY_MESSAGES:],
                ],
                temperature=0.7,
                max_tokens=800,
                stream=True,
            )
            for chunk in stream:
                choices = getattr(chunk, "choices", None)
                delta = getattr(choices[0].delta, "content", None) if choices else None
                if delta:
                    yield delta
        except Exception as exc:  # network, auth, quota, bad model name...
            raise TutorError(f"{type(exc).__name__}: {exc}") from exc
