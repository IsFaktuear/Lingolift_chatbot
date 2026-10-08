from dataclasses import dataclass


@dataclass(frozen=True)
class Lesson:
    icon: str
    category: str
    title: str
    meta: str
    featured: bool = False
    xp: int = 0


@dataclass(frozen=True)
class VocabularyWord:
    phrase: str
    meaning: str
    example: str
    level: str = "B1"
