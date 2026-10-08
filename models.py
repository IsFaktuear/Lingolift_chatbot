from dataclasses import dataclass


@dataclass(frozen=True)
class LessonStep:
    heading: str
    body: str


@dataclass(frozen=True)
class QuizQuestion:
    question: str
    options: tuple[str, ...]
    answer: int  # index of the correct option


@dataclass(frozen=True)
class Lesson:
    icon: str
    category: str
    title: str
    meta: str
    featured: bool = False
    xp: int = 0
    intro: str = ""
    steps: tuple[LessonStep, ...] = ()
    quiz: tuple[QuizQuestion, ...] = ()
    practice_prompt: str = ""


@dataclass(frozen=True)
class VocabularyWord:
    phrase: str
    meaning: str
    example: str
    level: str = "B1"
