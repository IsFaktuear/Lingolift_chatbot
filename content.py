import random

from models import Lesson, LessonStep, QuizQuestion, VocabQuizItem, VocabularyWord

QUIZ_ROUND_SIZE = 5
XP_PER_QUIZ_ANSWER = 5
# A lesson counts as completed when its quiz score reaches this ratio.
# Lesson XP is always proportional to correct answers.
LESSON_PASS_RATIO = 0.5


LESSONS = [
    Lesson(
        "🎧",
        "Listening",
        "At the coffee shop",
        "8 min",
        featured=True,
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
            QuizQuestion(
                'You are done ordering and the barista asks “Anything else?”. What is the most natural reply?',
                (
                    "No, that's all, thanks.",
                    "Yes, please.",
                    "I don't know.",
                ),
                0,
            ),
            QuizQuestion(
                "To understand an order quickly, which words should you listen for?",
                (
                    "The content words: drink, size, milk and name",
                    "Every single word, in order",
                    "Only the first word of each sentence",
                ),
                0,
            ),
            QuizQuestion(
                'The barista asks “Can I get a name for the order?”. What do you say?',
                (
                    "Sure, it's Rina.",
                    "Large, please.",
                    "To go, please.",
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
        "12 min",
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
            QuizQuestion(
                "Which of these is an open question?",
                (
                    "What do you usually do on weekends?",
                    "Do you like coffee?",
                    "Is it cold today?",
                    "Are you a student?",
                ),
                0,
            ),
            QuizQuestion(
                "Which topic is usually safe with someone you just met?",
                (
                    "Their plans for the weekend",
                    "How much money they earn",
                    "Their weight",
                    "Their religion",
                ),
                0,
            ),
            QuizQuestion(
                'Someone asks “How\'s it going?”. What is a natural reply?',
                (
                    "Pretty good, thanks! How about you?",
                    "I am going to the canteen.",
                    "It is going by bus.",
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
        "10 min",
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
            QuizQuestion(
                "“I ___ him yesterday.” Which fits?",
                ("saw", "have seen", "have saw", "seen"),
                0,
            ),
            QuizQuestion(
                "Which signal word usually goes with the present perfect?",
                ("already", "yesterday", "last week", "in 2019"),
                0,
            ),
            QuizQuestion(
                "“She ___ to Bali twice.” Which fits?",
                ("has been", "have been", "was been", "is been"),
                0,
            ),
        ),
        practice_prompt=(
            "Quiz me: ask me 5 questions using present perfect and past simple about my life "
            "experiences, and correct my answers."
        ),
    ),
    Lesson(
        "🍽️",
        "Everyday",
        "Ordering food at a restaurant",
        "10 min",
        intro=(
            "Eating out is a perfect chance to practice English — the script is short, "
            "the staff are patient, and you get food at the end. This lesson covers "
            "the whole flow from table to bill."
        ),
        steps=(
            LessonStep(
                "Getting seated",
                "“A table for two, please.” “Could we sit by the window?” "
                "If you booked: “I have a reservation under Budi.” "
                "“This way, please” means ikuti saya.",
            ),
            LessonStep(
                "Ordering like a regular",
                "“I'll have the grilled chicken.” “Could I get a coffee, please?” "
                "For special needs: “I am allergic to peanuts.” “Is this dish spicy?” "
                "“I'll have” sounds more natural than “I want”.",
            ),
            LessonStep(
                "Paying and leaving",
                "“Could we get the bill, please?” — in the US people say “check”. "
                "“Keep the change” means kembaliannya buat kamu. "
                "Always end friendly: “The food was great, thank you!”",
            ),
        ),
        quiz=(
            QuizQuestion(
                'The waiter asks “Are you ready to order?”. What does he want to know?',
                (
                    "Whether you have decided what to eat",
                    "Whether you want to see the menu",
                    "Whether you have paid the bill",
                ),
                0,
            ),
            QuizQuestion(
                'You say “I am allergic to shrimp.” Why do you say that?',
                (
                    "To warn the staff so your food is safe",
                    "To ask for extra shrimp",
                    "To complain about the food",
                ),
                0,
            ),
            QuizQuestion(
                "Which sentence sounds most natural when ordering?",
                (
                    "I'll have the grilled chicken, please.",
                    "I want chicken. Give me.",
                    "Chicken is what I order now.",
                ),
                0,
            ),
            QuizQuestion(
                "In the US, what do people usually call the bill at a restaurant?",
                ("The check", "The menu", "The tip"),
                0,
            ),
            QuizQuestion(
                'You pay and say “Keep the change.” What do you mean?',
                (
                    "The waiter can keep the extra money",
                    "You want your change back quickly",
                    "You want to change your order",
                ),
                0,
            ),
        ),
        practice_prompt=(
            "Role-play with me: you are the waiter and I am the customer at an Indonesian "
            "restaurant. Correct me if I say something unnatural."
        ),
    ),
    Lesson(
        "✈️",
        "Travel",
        "At the airport",
        "12 min",
        intro=(
            "Airports run on English. Check-in, security, boarding — the same phrases "
            "repeat everywhere in the world. Learn them once, use them forever."
        ),
        steps=(
            LessonStep(
                "Check-in counter",
                "“I'd like to check in for the flight to Tokyo.” "
                "“Aisle or window?” — aisle is kursi lorong, window is kursi jendela. "
                "“Is my bag over the weight limit?” can save you from extra fees.",
            ),
            LessonStep(
                "Security and boarding",
                "“Boarding pass and passport, please.” Have them ready. "
                "“What time does boarding start?” “Has the gate changed?” — "
                "gates change more often than you think, so always double-check the screens.",
            ),
            LessonStep(
                "When things go wrong",
                "“Is the flight delayed?” “Where is baggage claim?” "
                "“My luggage didn't arrive.” Stay calm and polite — "
                "“Could you help me, please?” opens more doors than anger.",
            ),
        ),
        quiz=(
            QuizQuestion(
                'The screen says “Delayed by 2 hours”. What does it mean?',
                (
                    "The flight will leave 2 hours late",
                    "The flight is cancelled",
                    "The flight leaves in 2 hours",
                ),
                0,
            ),
            QuizQuestion(
                'You hear “Final call for passengers on flight GA 88.” What should you do?',
                (
                    "Go to the gate immediately",
                    "Go to the check-in counter",
                    "Wait for your name to be called",
                ),
                0,
            ),
            QuizQuestion(
                'At check-in the staff asks “Aisle or window?”. What do they want to know?',
                (
                    "Which seat you prefer",
                    "Which gate you need",
                    "Which bag you will check in",
                ),
                0,
            ),
            QuizQuestion(
                "Your bag didn't arrive. What is the best thing to say at the desk?",
                (
                    "My luggage didn't arrive. Could you help me, please?",
                    "Where is my bag?! This is terrible!",
                    "Bag. Lost. Help.",
                ),
                0,
            ),
            QuizQuestion(
                '“Boarding starts at 9:40 at gate 12.” What happens at 9:40?',
                (
                    "Passengers start getting on the plane",
                    "The plane lands",
                    "Check-in opens",
                ),
                0,
            ),
        ),
        practice_prompt=(
            "Role-play with me: you are the check-in staff and I am a nervous first-time "
            "flyer going to Singapore. Correct me if I say something unnatural."
        ),
    ),
    Lesson(
        "💼",
        "Work",
        "Job interview basics",
        "15 min",
        intro=(
            "Interviews are stressful in any language. In English, a few strong, simple "
            "sentences beat complicated ones. This lesson gives you the core answers "
            "every interview needs."
        ),
        steps=(
            LessonStep(
                "“Tell me about yourself”",
                "Use the present-past-future formula, 60 seconds max: "
                "“I'm a fresh graduate in informatics (present). I built a ticketing app "
                "for my final project (past). I'm looking for a junior developer role "
                "where I can keep learning (future).”",
            ),
            LessonStep(
                "Strengths and weaknesses",
                "Strength: “My strength is problem-solving — I enjoy debugging.” "
                "Weakness: pick something real but fixable — “I used to be shy speaking up, "
                "so I joined a study group to practice.” Never say “I have no weaknesses.”",
            ),
            LessonStep(
                "Questions you ask them",
                "Always ask something — “I have no questions” sounds uninterested. "
                "“What does a typical day look like in this role?” "
                "“What would success look like in the first three months?”",
            ),
        ),
        quiz=(
            QuizQuestion(
                'The interviewer says “Tell me about yourself.” What is the best approach?',
                (
                    "A short present-past-future summary, about one minute",
                    "Your full life story from childhood",
                    "“I don't know, what do you want to know?”",
                ),
                0,
            ),
            QuizQuestion(
                '“What is your biggest weakness?” What should you do?',
                (
                    "Name a real, fixable weakness and how you improve it",
                    "Say you have no weaknesses",
                    "Criticize your previous boss",
                ),
                0,
            ),
            QuizQuestion(
                'The interviewer asks “Do you have any questions for us?”. What is best?',
                (
                    "Ask what a typical day in the role looks like",
                    "Say “No, I have no questions.”",
                    "Ask how soon you can take a holiday",
                ),
                0,
            ),
            QuizQuestion(
                'Which is the best answer to “What is your strength?”',
                (
                    "“Problem-solving — I enjoy debugging and finding the cause of a bug.”",
                    "“I am good at everything.”",
                    "“I don't really have one.”",
                ),
                0,
            ),
            QuizQuestion(
                '“Why do you want this job?” Which answer is strongest?',
                (
                    "“I want to grow as a developer, and your team builds things I care about.”",
                    "“I just need any job.”",
                    "“My friend works here.”",
                ),
                0,
            ),
        ),
        practice_prompt=(
            "Do a mock job interview with me for a junior IT support role. Ask one "
            "question at a time and give me feedback on each answer."
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


def shuffled_question(
    question: QuizQuestion, seed: int | str
) -> tuple[tuple[str, ...], int]:
    """Return (options, answer_index) in a stable shuffled order for this seed.

    Lessons are authored with the correct option first; shuffling here keeps
    the right answer from always sitting at the top."""
    rng = random.Random(str(seed))
    order = list(range(len(question.options)))
    rng.shuffle(order)
    return tuple(question.options[i] for i in order), order.index(question.answer)


def build_vocab_quiz(
    words: list[VocabularyWord],
    n: int = QUIZ_ROUND_SIZE,
    seed: int | None = None,
) -> list[VocabQuizItem]:
    """Build a multiple-choice quiz round from the word bank.

    Each item asks for a meaning given a phrase, or a phrase given a meaning,
    with 3 distractors drawn from the other words. Needs at least 4 words.
    """
    rng = random.Random(seed)
    if len(words) < 4:
        return []
    items: list[VocabQuizItem] = []
    for word in rng.sample(words, min(n, len(words))):
        others = [w for w in words if w.phrase != word.phrase]
        if rng.random() < 0.5:
            prompt = f'What does "{word.phrase}" mean?'
            correct, distractors = word.meaning, rng.sample([w.meaning for w in others], 3)
        else:
            prompt = f'Which phrase means "{word.meaning}"?'
            correct, distractors = word.phrase, rng.sample([w.phrase for w in others], 3)
        options = [correct, *distractors]
        order = list(range(len(options)))
        rng.shuffle(order)
        items.append(
            VocabQuizItem(
                prompt=prompt,
                options=tuple(options[i] for i in order),
                answer=order.index(0),
            )
        )
    return items
