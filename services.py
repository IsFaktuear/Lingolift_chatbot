import os
from typing import Any

from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

load_dotenv(override=True)


class TutorService:
    DEMO_MESSAGE = (
        "Demo mode: I am your English tutor. Add `OPENAI_API_KEY` to your environment "
        "to activate live AI conversations. For now, try asking: *How do I use present perfect?*"
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
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://agentrouter.org/v1")
        self.model = os.getenv("OPENAI_MODEL", "deepseek-v4-flash")
        self.stt_model = os.getenv("OPENAI_STT_MODEL", "whisper-1")

    def _client(self) -> Any:
        if not self.api_key or OpenAI is None:
            return None
        return OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=20.0,
            max_retries=0,
        )

    def reply(self, messages: list[dict[str, str]]) -> str:
        client = self._client()
        if client is None:
            return self.DEMO_MESSAGE

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.SYSTEM_MESSAGE},
                *messages,
            ],
            temperature=0.7,
            max_tokens=350,
        )
        return response.choices[0].message.content or "Let's practice that together."

    def reply_stream(self, messages: list[dict[str, str]]):
        """Yield the assistant reply in chunks for a streaming UI."""
        client = self._client()
        if client is None:
            yield self.DEMO_MESSAGE
            return
        try:
            stream = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_MESSAGE},
                    *messages,
                ],
                temperature=0.7,
                max_tokens=350,
                stream=True,
            )
            for chunk in stream:
                choices = getattr(chunk, "choices", None)
                delta = getattr(choices[0].delta, "content", None) if choices else None
                if delta:
                    yield delta
        except Exception:
            yield "I couldn't reach the AI service right now. Check your API settings."

    def transcribe(self, audio_bytes: bytes) -> str | None:
        """Speech-to-text via the configured OpenAI-compatible API.

        Returns the transcribed text, or None when transcription is unavailable
        (no API key, unsupported endpoint, network error)."""
        client = self._client()
        if client is None or not audio_bytes:
            return None
        try:
            result = client.audio.transcriptions.create(
                model=self.stt_model,
                file=("speech.wav", audio_bytes),
            )
            text = (getattr(result, "text", "") or "").strip()
            return text or None
        except Exception:
            return None
