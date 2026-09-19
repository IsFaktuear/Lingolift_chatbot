from models import Lesson, VocabularyWord


LESSONS = [
    Lesson("🎧", "Listening", "At the coffee shop", "8 min · 80 XP", featured=True),
    Lesson("💬", "Speaking", "Small talk starters", "12 min · 120 XP"),
    Lesson("✍️", "Grammar", "Past experiences", "10 min · 100 XP"),
]

VOCABULARY = [
    VocabularyWord("up for it", "willing to do something", "I'm up for it!"),
    VocabularyWord("routine", "the usual way you do things", "My morning routine is simple."),
    VocabularyWord("catch up", "talk to someone you have not seen recently", "Let's catch up soon."),
]

QUICK_PRACTICE_PROMPTS = [
    "Describe your morning",
    "Order a coffee",
    "Talk about last weekend",
]
