import os
from typing import Any

from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

load_dotenv(override=True)


class TutorService:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://agentrouter.org/v1")
        self.model = os.getenv("OPENAI_MODEL", "deepseek-v4-flash")

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
            return (
                "Demo mode: I am your English tutor. Add `OPENAI_API_KEY` to your environment "
                "to activate live AI conversations. For now, try asking: *How do I use present perfect?*"
            )

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are LingoLift, a warm English tutor. Reply mostly in English, "
                        "adjusting to the learner's level. Correct mistakes gently, explain "
                        "useful points when they matter, and respond naturally to what the learner "
                        "actually said. Keep simple replies short, but use a few paragraphs when "
                        "the learner asks for an explanation. Do not force a practice question at "
                        "the end of every reply, and avoid repetitive filler."
                    ),
                },
                *messages,
            ],
            temperature=0.7,
            max_tokens=350,
        )
        return response.choices[0].message.content or "Let's practice that together."
