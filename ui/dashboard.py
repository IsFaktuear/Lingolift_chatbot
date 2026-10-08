import streamlit as st

from content import LESSONS, QUICK_PRACTICE_PROMPTS
from datetime import datetime
from urllib.parse import quote
from storage import Store, level_for_xp


@st.dialog("Batalkan lesson?")
def _confirm_undo_dialog(title: str, xp: int, store: Store) -> None:
    st.write(f'Yakin mau batalkan "{title}"? Progress-nya dihapus dan {xp} XP dikembalikan.')
    yes, no = st.columns(2)
    if yes.button("Ya, batalkan", use_container_width=True):
        if store.uncomplete_lesson(title):
            st.toast("Tandai selesai dibatalkan, XP dikembalikan ↩️")
        st.rerun()
    if no.button("Gak jadi", use_container_width=True):
        st.rerun()


class DashboardPage:
    def __init__(self, store: Store) -> None:
        self.store = store

    def render(self) -> None:
        lesson_param = st.query_params.get("lesson")
        if lesson_param:
            st.query_params.clear()
            if any(lesson.title == lesson_param for lesson in LESSONS):
                st.session_state.active_lesson = lesson_param
            st.rerun()
        active = st.session_state.get("active_lesson")
        if active:
            lesson = next((l for l in LESSONS if l.title == active), None)
            if lesson is not None:
                self._lesson_detail(lesson)
                return
            st.session_state.active_lesson = None
        st.markdown(f'<div class="hero"><div class="eyebrow">{datetime.now().strftime("%A")} · Intermediate track</div><h1>Make English part<br>of your everyday.</h1><div class="hero-copy">A friendly space to listen, speak, and build confidence one useful phrase at a time. <span class="hero-note">You are doing better than you think.</span></div></div>', unsafe_allow_html=True)
        self._stats()
        self._lessons()
        self._audio_and_phrase()
        self._quick_practice()

    def _stats(self) -> None:
        done = self.store.lessons_done()
        progress = round(100 * len(done) / len(LESSONS)) if LESSONS else 0
        words = len(self.store.get_words())
        xp = self.store.total_xp()
        level = level_for_xp(xp)
        stats = [
            (f"{progress}%", "Course progress"),
            (str(words), "Words learned"),
            (level, f"Current level · {xp} XP"),
        ]
        columns = st.columns(3)
        for column, (number, label) in zip(columns, stats):
            with column:
                st.markdown(f'<div class="card"><div class="stat-number">{number}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

    def _lessons(self) -> None:
        done = self.store.lessons_done()
        waiting = len(LESSONS) - len(done & {lesson.title for lesson in LESSONS})
        st.markdown(f'<div class="section-label"><h2>Continue learning</h2><span>{waiting} lessons waiting</span></div>', unsafe_allow_html=True)
        columns = st.columns(3)
        for column, lesson in zip(columns, LESSONS):
            with column:
                is_done = lesson.title in done
                card_class = "card lesson-card lesson-click featured-lesson" if lesson.featured else "card lesson-card lesson-click"
                badge = '<div class="lesson-badge">Featured listening</div>' if (lesson.featured and not is_done) else ""
                done_badge = '<div class="lesson-badge" style="background:var(--green);">✓ Completed</div>' if is_done else ""
                # The whole card is a plain link: robust on every browser, no overlay hacks.
                href = f"?lesson={quote(lesson.title)}"
                st.markdown(
                    f'<a href="{href}" target="_self" class="lesson-link">'
                    f'<div class="{card_class}"><div class="lesson-icon">{lesson.icon}</div>{badge}{done_badge}'
                    f'<div class="eyebrow">{lesson.category}</div><h3>{lesson.title}</h3>'
                    f'<div class="lesson-meta">{lesson.meta}</div></div></a>',
                    unsafe_allow_html=True,
                )
                if is_done:
                    if st.button("Batalkan", key=f"undo-{lesson.title}", use_container_width=True):
                        _confirm_undo_dialog(lesson.title, lesson.xp, self.store)
                    continue
                if st.button(f"Tandai selesai · +{lesson.xp} XP", key=f"done-{lesson.title}", use_container_width=True):
                    if self.store.complete_lesson(lesson.title, lesson.xp):
                        st.toast(f"Lesson selesai! +{lesson.xp} XP 🎉")
                    st.rerun()

    def _lesson_detail(self, lesson) -> None:
        if st.button("← Back to overview", key="back-overview"):
            st.session_state.active_lesson = None
            st.rerun()
        st.markdown(f'<div class="eyebrow">{lesson.icon} {lesson.category}</div>', unsafe_allow_html=True)
        st.title(lesson.title)
        st.caption(lesson.meta)
        st.markdown(lesson.intro)

        st.markdown('<div class="section-label"><h2>What you will learn</h2></div>', unsafe_allow_html=True)
        for index, step in enumerate(lesson.steps, start=1):
            st.markdown(
                f'<div class="card" style="margin:10px 0">'
                f'<div class="eyebrow">Step {index}</div>'
                f"<h3>{step.heading}</h3>"
                f'<p class="muted">{step.body}</p></div>',
                unsafe_allow_html=True,
            )

        if lesson.quiz:
            self._lesson_quiz(lesson)

        st.markdown('<div class="section-label"><h2>Practice</h2></div>', unsafe_allow_html=True)
        if st.button("Practice this with AI 💬", key=f"practice-{lesson.title}", type="primary", use_container_width=True):
            st.session_state.lesson_prompt = lesson.practice_prompt
            st.session_state.active_lesson = None
            st.switch_page(st.session_state.page_routes["Practice with AI"])

        done = self.store.lessons_done()
        if lesson.title in done:
            st.markdown('<div class="eyebrow">✓ Completed</div>', unsafe_allow_html=True)
            if st.button("Batalkan tandai selesai", key=f"undo-detail-{lesson.title}", use_container_width=True):
                _confirm_undo_dialog(lesson.title, lesson.xp, self.store)
        elif st.button(f"Tandai selesai · +{lesson.xp} XP", key=f"done-detail-{lesson.title}", use_container_width=True):
            if self.store.complete_lesson(lesson.title, lesson.xp):
                st.toast(f"Lesson selesai! +{lesson.xp} XP 🎉")
            st.rerun()

    def _lesson_quiz(self, lesson) -> None:
        st.markdown('<div class="section-label"><h2>Quick check</h2><span>Test yourself</span></div>', unsafe_allow_html=True)
        checked_key = f"quiz-checked-{lesson.title}"
        for index, question in enumerate(lesson.quiz):
            st.markdown(f"**{index + 1}. {question.question}**")
            choice = st.radio(
                "Choose an answer",
                options=list(range(len(question.options))),
                format_func=lambda i, opts=question.options: opts[i],
                key=f"quiz-{lesson.title}-{index}",
                label_visibility="collapsed",
            )
            if st.session_state.get(checked_key):
                if choice == question.answer:
                    st.success("Correct! ✅")
                else:
                    st.error(f"Not quite. The answer is: {question.options[question.answer]}")
        col_a, col_b = st.columns([1, 3])
        with col_a:
            if st.button("Check my answers", key=f"quiz-check-{lesson.title}", type="primary"):
                st.session_state[checked_key] = True
                st.rerun()
        if st.session_state.get(checked_key):
            with col_b:
                if st.button("Try again", key=f"quiz-retry-{lesson.title}"):
                    st.session_state[checked_key] = False
                    st.rerun()

    def _audio_and_phrase(self) -> None:
        st.markdown('<div class="section-label"><h2>Listen & notice</h2><span>Real-world English</span></div>', unsafe_allow_html=True)
        media_col, note_col = st.columns([1.4, 1])
        with media_col:
            st.markdown('<div class="audio-shell"><div class="eyebrow" style="color:#b8e7cf">Today\'s audio</div><div class="audio-title">A morning in London</div><div style="color:#c7d8cf;font-size:13px">Listen for the way people talk about routines.</div></div>', unsafe_allow_html=True)
            st.audio("assets/morning-routine.mp3")
        with note_col:
            st.markdown('<div class="card"><div class="eyebrow">Phrase of the day</div><h3>"I\'m up for it."</h3><p class="muted">Use this when you want to say you are interested or willing to do something.</p><p>"Want to try the new cafe?"<br><span class="word">"Sure, I\'m up for it!"</span></p></div>', unsafe_allow_html=True)

    def _quick_practice(self) -> None:
        st.markdown('<div class="section-label"><h2>Quick practice</h2><span>2 minutes</span></div>', unsafe_allow_html=True)
        columns = st.columns(3)
        for index, (column, prompt_text) in enumerate(zip(columns, QUICK_PRACTICE_PROMPTS)):
            with column:
                st.markdown(f'<div class="card"><div class="eyebrow">Prompt 0{index + 1}</div><p>{prompt_text}</p></div>', unsafe_allow_html=True)
                if st.button("Practice with AI", key=f"practice-{index}", use_container_width=True):
                    st.session_state.lesson_prompt = prompt_text
                    st.switch_page(st.session_state.page_routes["Practice with AI"])
