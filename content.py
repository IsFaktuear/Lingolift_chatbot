from models import Lesson, LessonStep, QuizQuestion, VocabularyWord


LESSONS = [
    Lesson(
        "🎧",
        "Listening",
        "At the coffee shop",
        "8 min · 80 XP",
        featured=True,
        xp=80,
        intro=(
            "Ordering coffee is one of the most useful real-world listening situations. "
            "In this lesson you will learn the phrases baristas actually use and train "
            "your ear to catch them."
        ),
        steps=(
            LessonStep(
                "What you will hear",
                "Baristas use the same few sentences all day: “What can I get for you?”, "
                "“For here or to go?”, and “Anything else?”. If you know these three by heart, "
                "you will never freeze at the counter again.",
            ),
            LessonStep(
                "Sizes and milk",
                "Small / medium / large are safe everywhere. Some shops use tall / grande / venti. "
                "Milk options you will hear: “whole milk, skim, oat, almond, soy”. "
                "“To stay” means you drink there; “to take away” means dibawa pulang.",
            ),
            LessonStep(
                "Listening trick: catch the content words",
                "Do not try to catch every word. Listen for the content words — the drink, "
                "the size, the milk, your name. Everything else is just glue.",
            ),
        ),
        quiz=(
            QuizQuestion(
                'The barista asks “For here or to go?”. What does she want to know?',
                (
                    "Whether you will drink here or take it away",
                    "Whether you want coffee or tea",
                    "Whether you pay by cash or card",
                ),
                0,
            ),
            QuizQuestion(
                'You hear “oat milk latte, please”. What did the customer order?',
                (
                    "A latte with oat milk",
                    "Oatmeal with milk",
                    "A latte to stay",
                ),
                0,
            ),
        ),
        practice_prompt=(
            "Role-play with me: you are the barista and I am the customer ordering coffee. "
            "Correct me if I say something unnatural."
        ),
    ),
    Lesson(
        "💬",
        "Speaking",
        "Small talk starters",
        "12 min · 120 XP",
        xp=120,
        intro=(
            "Small talk opens doors — at work, on campus, while traveling. This lesson gives "
            "you openers that actually work, and shows you what to avoid."
        ),
        steps=(
            LessonStep(
                "Three safe topics",
                "Weather, plans, and the situation around you are always safe: “Busy day today?”, "
                "“Have you been here long?”, “Any plans for the weekend?”.",
            ),
            LessonStep(
                "Open vs closed questions",
                "“Do you like coffee?” ends with yes/no — conversation dies. "
                "“What do you usually do on weekends?” invites a story. Prefer open questions.",
            ),
            LessonStep(
                "Exit gracefully",
                "Leaving well matters too: “It was nice chatting with you!”, "
                "“I won't keep you — see you around!”. Never just walk away mid-topic.",
            ),
        ),
        quiz=(
            QuizQuestion(
                "Which opener is most likely to keep a conversation going?",
                (
                    "What brings you here today?",
                    "Nice weather we're having.",
                    "How old are you?",
                    "You look tired.",
                ),
                0,
            ),
            QuizQuestion(
                'Someone says “I should get going.” What is the best reply?',
                (
                    "It was nice talking to you!",
                    "Why? Stay a bit longer.",
                    "OK. Bye.",
                ),
                0,
            ),
        ),
        practice_prompt=(
            "Let's practice small talk. Start a casual conversation with me as if we just met "
            "at a campus event, and give me feedback on my replies."
        ),
    ),
    Lesson(
        "✍️",
        "Grammar",
        "Past experiences",
        "10 min · 100 XP",
        xp=100,
        intro=(
            "Present perfect vs past simple — the classic headache for Indonesian learners, "
            "because Bahasa Indonesia does not mark this difference. This lesson makes it click."
        ),
        steps=(
            LessonStep(
                "The core difference",
                "Past simple = finished time: “I visited Bali in 2019.” "
                "Present perfect = experience up to now, no time mentioned: "
                "“I've visited Bali twice.” No time → have/has + verb 3.",
            ),
            LessonStep(
                "Signal words",
                "Yesterday, last week, in 2019 → past simple. "
                "Ever, never, already, yet, just, so far → present perfect. "
                "Spot the signal word and the tense chooses itself.",
            ),
            LessonStep(
                "Common mistake",
                "“I have seen him yesterday.” ❌ — “yesterday” is finished time, so it must be "
                "“I saw him yesterday.” ✓. Time mentioned → past simple.",
            ),
        ),
        quiz=(
            QuizQuestion(
                "“I ___ in Jakarta since 2020.” Which fits?",
                ("have lived", "lived", "live", "am living"),
                0,
            ),
            QuizQuestion(
                "“___ you ever ___ sushi?” Which fits?",
                ("Have / eaten", "Did / ate", "Have / ate", "Did / eaten"),
                0,
            ),
        ),
        practice_prompt=(
            "Quiz me: ask me 5 questions using present perfect and past simple about my life "
            "experiences, and correct my answers."
        ),
    ),
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
