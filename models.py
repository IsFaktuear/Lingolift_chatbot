from dataclasses import dataclass

# Every correct quiz answer in a lesson is worth this much XP.
XP_PER_LESSON_QUESTION = 20


@dataclass(frozen=True)
class LessonStep:
    heading: str
    body: str


@dataclass(frozen=True)
class QuizQuestion:
    question: str
    options: tuple[str, ...]
    answer: int  # authoring convention: option 0 is correct; shuffled at display time


@dataclass(frozen=True)
class VocabQuizItem:
    prompt: str
    options: tuple[str, ...]
    answer: int  # index of the correct option


@dataclass(frozen=True)
class Lesson:
    icon: str
    category: str
    title: str
    meta: str
    featured: bool = False
    intro: str = ""
    steps: tuple[LessonStep, ...] = ()
    quiz: tuple[QuizQuestion, ...] = ()
    practice_prompt: str = ""

    @property
    def xp(self) -> int:
        """Max XP for the lesson = number of quiz questions x XP per question."""
        return len(self.quiz) * XP_PER_LESSON_QUESTION


@dataclass(frozen=True)
class VocabularyWord:
    phrase: str
    meaning: str
    example: str
    level: str = "B1"
