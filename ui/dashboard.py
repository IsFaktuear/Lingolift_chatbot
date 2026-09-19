import streamlit as st

from content import LESSONS, QUICK_PRACTICE_PROMPTS


class DashboardPage:
    def render(self) -> None:
        st.markdown('<div class="hero"><div class="eyebrow">Tuesday · Intermediate track</div><h1>Make English part<br>of your everyday.</h1><div class="hero-copy">A friendly space to listen, speak, and build confidence one useful phrase at a time. <span class="hero-note">You are doing better than you think.</span></div></div>', unsafe_allow_html=True)
        self._stats()
        self._lessons()
        self._audio_and_phrase()
        self._quick_practice()

    def _stats(self) -> None:
        columns = st.columns(3)
        for column, number, label in zip(columns, ["68%", "24", "B1"], ["Course progress", "Words learned", "Current level"]):
            with column:
                st.markdown(f'<div class="card"><div class="stat-number">{number}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

    def _lessons(self) -> None:
        st.markdown('<div class="section-label"><h2>Continue learning</h2><span>3 lessons waiting</span></div>', unsafe_allow_html=True)
        columns = st.columns(3)
        for column, lesson in zip(columns, LESSONS):
            with column:
                card_class = "card lesson-card featured-lesson" if lesson.featured else "card lesson-card"
                badge = '<div class="lesson-badge">Featured listening</div>' if lesson.featured else ""
                button_label = "Start listening" if lesson.featured else "Open lesson"
                st.markdown(f'<div class="{card_class}"><div class="lesson-icon">{lesson.icon}</div>{badge}<div class="eyebrow">{lesson.category}</div><h3>{lesson.title}</h3><div class="lesson-meta">{lesson.meta}</div></div>', unsafe_allow_html=True)
                if st.button(button_label, key=f"open-{lesson.title}", use_container_width=True):
                    st.session_state.lesson_prompt = f"Help me practice the lesson: {lesson.title}."
                    st.switch_page(st.session_state.page_routes["Practice with AI"])

    def _audio_and_phrase(self) -> None:
        st.markdown('<div class="section-label"><h2>Listen & notice</h2><span>Real-world English</span></div>', unsafe_allow_html=True)
        media_col, note_col = st.columns([1.4, 1])
        with media_col:
            st.markdown('<div class="audio-shell"><div class="eyebrow" style="color:#b8e7cf">Today\'s audio</div><div class="audio-title">A morning in London</div><div style="color:#c7d8cf;font-size:13px">Listen for the way people talk about routines.</div></div>', unsafe_allow_html=True)
            st.audio("https://www2.cs.uic.edu/~i101/SoundFiles/StarWars60.wav")
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
