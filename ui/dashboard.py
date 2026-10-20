from datetime import datetime
from html import escape
from pathlib import Path

import streamlit as st

from content import LESSON_PASS_RATIO, LESSONS, QUICK_PRACTICE_PROMPTS, shuffled_question
from storage import Store, level_progress

AUDIO_PATH = Path(__file__).resolve().parent.parent / "assets" / "morning-routine.mp3"


def _cat_class(category: str) -> str:
    return "cat-" + category.lower().replace(" ", "-")


@st.dialog("Reset this lesson?")
def _confirm_reset_dialog(title: str, earned: int, store: Store) -> None:
    st.write(
        f'Your best score for "{title}" and the {earned} XP you earned from it will be removed. '
        "You can take the quiz again afterwards."
    )
    yes, no = st.columns(2)
    if yes.button("Yes, reset", type="primary", use_container_width=True):
        if store.reset_lesson(title):
            st.toast("Lesson reset ↩️")
        for key in [k for k in st.session_state if str(k).startswith(f"quiz-") and title in str(k)]:
            del st.session_state[key]
        st.rerun()
    if no.button("Cancel", use_container_width=True):
        st.rerun()


class DashboardPage:
    def __init__(self, store: Store) -> None:
        self.store = store

    # -- overview -----------------------------------------------------------
    def render(self) -> None:
        active = st.session_state.get("active_lesson")
        if active:
            lesson = next((l for l in LESSONS if l.title == active), None)
            if lesson is not None:
                self._lesson_detail(lesson)
                return
            st.session_state.active_lesson = None

        xp = self.store.total_xp()
        done = self.store.lessons_done() & {lesson.title for lesson in LESSONS}
        self._hero(xp)
        self._stats(xp, done)
        self._lessons(done)
        self._audio_and_phrase()
        self._quick_practice()

    def _hero(self, xp: int) -> None:
        level, nxt, pct, to_next = level_progress(xp)
        day = datetime.now().strftime("%A")
        goal = f"{to_next} XP to {nxt}" if nxt else "Top level reached"
        st.markdown(
            f"""
<div class="hero">
  <div class="hero-main">
    <div class="eyebrow eyebrow-light">{day} · Level {level}</div>
    <h1>Make English part<br>of your everyday.</h1>
    <p class="hero-copy">Listen, speak and build confidence one useful phrase at a time.
    <span class="hero-note">You are doing better than you think.</span></p>
  </div>
  <div class="hero-level">
    <div class="level-badge">{level}</div>
    <div class="level-info">
      <div class="level-xp">{xp} XP</div>
      <div class="level-bar"><span style="width:{pct}%"></span></div>
      <div class="level-goal">{goal}</div>
    </div>
  </div>
</div>""",
            unsafe_allow_html=True,
        )

    def _stats(self, xp: int, done: set[str]) -> None:
        words = len(self.store.get_words())
        progress = round(100 * len(done) / len(LESSONS)) if LESSONS else 0
        stats = [
            ("📘", f"{len(done)}/{len(LESSONS)}", f"Lessons done · {progress}%"),
            ("🗂️", str(words), "Words in your bank"),
            ("⚡", str(xp), "Total XP earned"),
        ]
        cards = "".join(
            f'<div class="stat-card"><div class="stat-icon">{icon}</div>'
            f'<div><div class="stat-number">{number}</div><div class="stat-label">{label}</div></div></div>'
            for icon, number, label in stats
        )
        st.markdown(f'<div class="stat-grid">{cards}</div>', unsafe_allow_html=True)

    def _lessons(self, done: set[str]) -> None:
        scores = self.store.lesson_scores()
        waiting = len(LESSONS) - len(done)
        note = f"{waiting} lessons waiting" if waiting else "All done — great job!"
        st.markdown(
            f'<div class="section-label"><h2>Continue learning</h2><span>{note}</span></div>',
            unsafe_allow_html=True,
        )
        for row_start in range(0, len(LESSONS), 3):
            columns = st.columns(3)
            for column, lesson in zip(columns, LESSONS[row_start : row_start + 3]):
                with column:
                    is_done = lesson.title in done
                    score = scores.get(lesson.title)
                    earned = score[2] if score else 0
                    if is_done:
                        badge = '<span class="pill pill-done">✓ Completed</span>'
                    elif score:
                        badge = '<span class="pill pill-progress">Try again</span>'
                    elif lesson.featured:
                        badge = '<span class="pill pill-featured">Featured</span>'
                    else:
                        badge = ""
                    st.markdown(
                        f'<div class="lesson-card {_cat_class(lesson.category)}{" is-done" if is_done else ""}">'
                        f'<div class="lesson-top"><div class="lesson-icon">{lesson.icon}</div>{badge}</div>'
                        f'<div class="lesson-cat">{escape(lesson.category)}</div>'
                        f"<h3>{escape(lesson.title)}</h3>"
                        f'<div class="lesson-meta">⏱ {lesson.meta} · ⚡ {earned}/{lesson.xp} XP</div>'
                        f'<div class="xp-track"><span style="width:{round(100 * earned / lesson.xp) if lesson.xp else 0}%"></span></div></div>',
                        unsafe_allow_html=True,
                    )
                    label = "Review lesson" if is_done else ("Continue lesson" if score else "Start lesson")
                    if st.button(label, key=f"open-{lesson.title}", use_container_width=True,
                                 icon=":material/arrow_forward:"):
                        st.session_state.active_lesson = lesson.title
                        st.rerun()

    def _audio_and_phrase(self) -> None:
        st.markdown(
            '<div class="section-label"><h2>Listen & notice</h2><span>Real-world English</span></div>',
            unsafe_allow_html=True,
        )
        media_col, note_col = st.columns([1.4, 1])
        with media_col:
            st.markdown(
                '<div class="audio-shell"><div class="eyebrow eyebrow-light">Today\'s audio</div>'
                '<div class="audio-title">A morning in London</div>'
                '<div class="audio-sub">Listen for the way people talk about routines.</div></div>',
                unsafe_allow_html=True,
            )
            if AUDIO_PATH.exists():
                st.audio(str(AUDIO_PATH))
            else:
                st.caption("Audio file `assets/morning-routine.mp3` not found.")
        with note_col:
            st.markdown(
                '<div class="card phrase-card"><div class="eyebrow">Phrase of the day</div>'
                "<h3>“I'm up for it.”</h3>"
                '<p class="muted">Say this when you are interested in or willing to do something.</p>'
                '<div class="dialogue"><p>“Want to try the new cafe?”</p>'
                '<p class="word">“Sure, I\'m up for it!”</p></div></div>',
                unsafe_allow_html=True,
            )

    def _quick_practice(self) -> None:
        st.markdown(
            '<div class="section-label"><h2>Quick practice</h2><span>2 minutes each</span></div>',
            unsafe_allow_html=True,
        )
        columns = st.columns(len(QUICK_PRACTICE_PROMPTS))
        for index, (column, prompt_text) in enumerate(zip(columns, QUICK_PRACTICE_PROMPTS)):
            with column:
                st.markdown(
                    f'<div class="prompt-card"><span class="prompt-num">0{index + 1}</span>'
                    f"<p>{escape(prompt_text)}</p></div>",
                    unsafe_allow_html=True,
                )
                if st.button("Practice with AI", key=f"quick-{index}", use_container_width=True,
                             icon=":material/forum:"):
                    st.session_state.lesson_prompt = prompt_text
                    st.switch_page(st.session_state.page_routes["Practice with AI"])

    # -- lesson detail ------------------------------------------------------
    def _lesson_detail(self, lesson) -> None:
        if st.button("Back to overview", key="back-overview", icon=":material/arrow_back:"):
            st.session_state.active_lesson = None
            st.rerun()

        is_done = lesson.title in self.store.lessons_done()
        score = self.store.lesson_scores().get(lesson.title)
        earned = score[2] if score else 0
        status = '<span class="pill pill-done">✓ Completed</span>' if is_done else ""
        st.markdown(
            f'<div class="lesson-hero {_cat_class(lesson.category)}">'
            f'<div class="lesson-hero-icon">{lesson.icon}</div><div>'
            f'<div class="lesson-cat">{escape(lesson.category)} {status}</div>'
            f"<h1>{escape(lesson.title)}</h1>"
            f'<div class="lesson-meta">⏱ {lesson.meta} · ⚡ {earned}/{lesson.xp} XP earned</div>'
            f'<p class="hero-copy">{escape(lesson.intro)}</p></div></div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="section-label"><h2>What you will learn</h2></div>', unsafe_allow_html=True)
        steps = "".join(
            f'<div class="step"><div class="step-num">{index}</div><div>'
            f"<h3>{escape(step.heading)}</h3><p>{escape(step.body)}</p></div></div>"
            for index, step in enumerate(lesson.steps, start=1)
        )
        st.markdown(f'<div class="steps">{steps}</div>', unsafe_allow_html=True)

        if lesson.quiz:
            self._lesson_quiz(lesson, score)
        else:
            st.info("This lesson has no quiz yet, so it gives no XP.")

        st.markdown('<div class="section-label"><h2>Keep practicing</h2></div>', unsafe_allow_html=True)
        practice_col, reset_col = st.columns(2)
        with practice_col:
            if st.button("Practice this with AI", key=f"practice-{lesson.title}", type="primary",
                         use_container_width=True, icon=":material/forum:"):
                st.session_state.lesson_prompt = lesson.practice_prompt
                st.session_state.active_lesson = None
                st.switch_page(st.session_state.page_routes["Practice with AI"])
        with reset_col:
            if score and st.button("Reset lesson progress", key=f"reset-{lesson.title}",
                                   use_container_width=True, icon=":material/restart_alt:"):
                _confirm_reset_dialog(lesson.title, earned, self.store)

    def _lesson_quiz(self, lesson, score) -> None:
        total = len(lesson.quiz)
        xp_per_q = round(lesson.xp / total)
        need = -(-total * LESSON_PASS_RATIO // 1)  # ceil
        st.markdown(
            f'<div class="section-label"><h2>Quiz</h2><span>Up to {lesson.xp} XP</span></div>',
            unsafe_allow_html=True,
        )
        best_note = f" Your best so far: <b>{score[0]}/{score[1]}</b> ({score[2]} XP)." if score else ""
        st.markdown(
            f'<div class="rule-note">Each correct answer = <b>+{xp_per_q} XP</b>. '
            f"Get at least <b>{int(need)}/{total}</b> right to complete the lesson. "
            f"Retrying only adds XP when you beat your best score.{best_note}</div>",
            unsafe_allow_html=True,
        )

        attempt_key = f"quiz-attempt-{lesson.title}"
        result_key = f"quiz-result-{lesson.title}"
        attempt = st.session_state.get(attempt_key, 0)
        result = st.session_state.get(result_key)
        checked = result is not None
        answers = []
        for index, question in enumerate(lesson.quiz):
            options, answer = shuffled_question(question, f"{lesson.title}|{index}|{attempt}")
            st.markdown(f"**{index + 1}. {question.question}**")
            choice = st.radio(
                "Choose an answer",
                options=list(range(len(options))),
                format_func=lambda i, opts=options: opts[i],
                index=None,
                key=f"quiz-{lesson.title}-{attempt}-{index}",
                label_visibility="collapsed",
                disabled=checked,
            )
            answers.append(choice == answer if choice is not None else None)
            if checked:
                if choice == answer:
                    st.success("Correct!", icon=":material/check_circle:")
                else:
                    st.error(f"Not quite. The answer is: {options[answer]}")

        if not checked:
            if st.button("Submit answers", key=f"quiz-check-{lesson.title}", type="primary",
                         icon=":material/task_alt:"):
                if None in answers:
                    st.warning("Answer every question first.")
                    return
                correct = sum(answers)
                result = self.store.record_lesson_quiz(
                    lesson.title, correct, total, lesson.xp, LESSON_PASS_RATIO
                )
                result["correct"] = correct
                st.session_state[result_key] = result
                st.rerun()
            return

        self._quiz_result(result, lesson)
        if st.button("Try again", key=f"quiz-retry-{lesson.title}", icon=":material/refresh:"):
            st.session_state.pop(result_key, None)
            st.session_state[attempt_key] = attempt + 1  # new keys -> fresh radios, new order
            st.rerun()

    @staticmethod
    def _quiz_result(result: dict, lesson) -> None:
        correct, total = result["correct"], result["total"]
        if result["gained"]:
            xp_line = f"+{result['gained']} XP"
        elif result["earned"] >= lesson.xp:
            xp_line = "no new XP — you already earned the full XP for this lesson"
        else:
            xp_line = f"no new XP — your best score ({result['best']}/{total}) is still higher"
        if correct == total:
            title, kind = "Perfect score! 🎉", "success"
        elif result["passed"]:
            title, kind = "Lesson completed ✓", "success"
        else:
            title, kind = "Not passed yet", "warning"
        status = (
            "This lesson is completed." if result["passed"]
            else "Read the steps again and retry to complete the lesson."
        )
        st.markdown(
            f'<div class="quiz-result {kind}"><div class="quiz-score">{correct}/{total}</div>'
            f"<div><b>{title}</b><br>{xp_line} · {result['earned']}/{lesson.xp} XP earned. {status}</div></div>",
            unsafe_allow_html=True,
        )
