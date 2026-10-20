from html import escape

import streamlit as st

from content import XP_PER_QUIZ_ANSWER, build_vocab_quiz
from storage import DAILY_XP_CAPS, Store


class VocabularyPage:
    def __init__(self, store: Store) -> None:
        self.store = store

    def render(self) -> None:
        words_all = self.store.get_words()
        st.markdown('<div class="eyebrow">Your word bank</div>', unsafe_allow_html=True)
        st.title("My vocabulary")
        st.markdown(
            f'<p class="page-lead">{len(words_all)} words saved from your lessons and conversations.</p>',
            unsafe_allow_html=True,
        )

        quiz_col, add_col = st.columns(2)
        with quiz_col:
            self._quiz_section(words_all)
        with add_col:
            self._add_word_form()

        search = st.text_input(
            "Search vocabulary",
            placeholder="Search a phrase or meaning...",
            label_visibility="collapsed",
        )
        words = [word for word in words_all if self._matches(word, search)]
        if not words:
            st.info("No vocabulary matches that search yet.")
            return
        cards = "".join(self._word_card(word) for word in words)
        st.markdown(f'<div class="word-grid">{cards}</div>', unsafe_allow_html=True)

    @staticmethod
    def _word_card(word) -> str:
        example = f'<p class="word-example">“{escape(word.example)}”</p>' if word.example else ""
        return (
            '<div class="word-card">'
            f'<div class="word-head"><h3>{escape(word.phrase)}</h3>'
            f'<span class="pill pill-level">{escape(word.level)}</span></div>'
            f'<p class="muted">{escape(word.meaning)}</p>{example}</div>'
        )

    def _quiz_section(self, words) -> None:
        with st.expander("Quiz me", icon=":material/psychology:"):
            if len(words) < 4:
                st.info(f"Add at least 4 words to unlock the quiz (you have {len(words)}).")
                return
            if st.button("Start new round", key="vquiz-start", type="primary"):
                round_id = st.session_state.get("vquiz-round", 0) + 1
                st.session_state["vquiz-round"] = round_id
                st.session_state.vquiz = {
                    "round_id": round_id,
                    "items": build_vocab_quiz(words),
                    "scored": False,
                }
                st.session_state.pop("vquiz-score", None)
                st.rerun()
            quiz = st.session_state.get("vquiz")
            if not quiz:
                cap = DAILY_XP_CAPS["vocabulary quiz"]
                st.caption(f"5 questions per round · +{XP_PER_QUIZ_ANSWER} XP per correct answer · max {cap} XP/day")
                return
            items = quiz["items"]
            round_id = quiz["round_id"]
            for i, item in enumerate(items):
                st.markdown(f"**{i + 1}. {item.prompt}**")
                st.radio(
                    "Choose an answer",
                    options=list(range(len(item.options))),
                    format_func=lambda j, opts=item.options: opts[j],
                    index=None,
                    key=f"vquiz-{round_id}-{i}",
                    label_visibility="collapsed",
                    disabled=quiz["scored"],
                )
                if quiz["scored"]:
                    choice = st.session_state.get(f"vquiz-{round_id}-{i}")
                    if choice == item.answer:
                        st.success("Correct!", icon=":material/check_circle:")
                    else:
                        st.error(f"Answer: {item.options[item.answer]}")
            if not quiz["scored"]:
                if st.button("Check answers", key="vquiz-check", type="primary"):
                    answered = [st.session_state.get(f"vquiz-{round_id}-{i}") for i in range(len(items))]
                    if None in answered:
                        st.warning("Answer every question first.")
                        return
                    correct = sum(1 for a, item in zip(answered, items) if a == item.answer)
                    gained = self.store.add_xp_capped(correct * XP_PER_QUIZ_ANSWER, "vocabulary quiz")
                    quiz["scored"] = True
                    st.session_state["vquiz-score"] = (correct, len(items), gained)
                    st.rerun()
            else:
                correct, total, gained = st.session_state.get("vquiz-score", (0, len(items), 0))
                note = f" · +{gained} XP" if gained else " · daily quiz XP limit reached"
                st.success(f"Score: {correct}/{total}{note}")

    def _add_word_form(self) -> None:
        with st.expander("Add a new word", icon=":material/add:"):
            with st.form("add-word", clear_on_submit=True, border=False):
                phrase = st.text_input("Phrase", placeholder="e.g. break the ice")
                meaning = st.text_input("Meaning", placeholder="e.g. start a conversation")
                example = st.text_input("Example", placeholder="e.g. He told a joke to break the ice.")
                level = st.selectbox("Level", ["A1", "A2", "B1", "B2", "C1"], index=2)
                submitted = st.form_submit_button("Save word", type="primary")
            if submitted:
                if not phrase.strip() or not meaning.strip():
                    st.warning("Phrase and meaning are required.")
                elif self.store.add_word(phrase, meaning, example, level):
                    st.toast(f"Saved “{phrase.strip()}” to your word bank 📚")
                    st.rerun()
                else:
                    st.info("That phrase is already in your word bank.")

    @staticmethod
    def _matches(word, search: str) -> bool:
        query = search.strip().lower()
        return (
            not query
            or query in word.phrase.lower()
            or query in word.meaning.lower()
            or query in word.example.lower()
        )
