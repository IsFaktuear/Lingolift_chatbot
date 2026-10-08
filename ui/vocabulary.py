import streamlit as st

from content import XP_PER_QUIZ_ANSWER, build_vocab_quiz
from storage import Store


class VocabularyPage:
    def __init__(self, store: Store) -> None:
        self.store = store

    def render(self) -> None:
        st.markdown('<div class="eyebrow">Your word bank</div>', unsafe_allow_html=True)
        st.title("My vocabulary")
        st.caption("Words saved from your lessons and conversations.")
        self._quiz_section()
        self._add_word_form()
        search = st.text_input("Search vocabulary", placeholder="Search a phrase or meaning...")
        words = [word for word in self.store.get_words() if self._matches(word, search)]
        if not words:
            st.info("No vocabulary matches that search yet.")
            return
        for word in words:
            st.markdown(f'<div class="card" style="margin:10px 0"><div style="display:flex;justify-content:space-between;align-items:center"><h3 style="margin:0;color:var(--coral)">{word.phrase}</h3><span class="eyebrow">{word.level}</span></div><p class="muted">{word.meaning}</p><p>"{word.example}"</p></div>', unsafe_allow_html=True)

    def _quiz_section(self) -> None:
        words = self.store.get_words()
        with st.expander("🧠 Quiz me"):
            if len(words) < 4:
                st.info("Add at least 4 words to your bank to unlock the quiz.")
                return
            if st.button("Start new round", key="vquiz-start"):
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
                st.caption("5 questions per round · +5 XP per correct answer.")
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
                )
                if quiz["scored"]:
                    choice = st.session_state.get(f"vquiz-{round_id}-{i}")
                    if choice == item.answer:
                        st.success("Correct! ✅")
                    else:
                        st.error(f"Answer: {item.options[item.answer]}")
            if not quiz["scored"]:
                if st.button("Check answers", key="vquiz-check"):
                    correct = sum(
                        1
                        for i, item in enumerate(items)
                        if st.session_state.get(f"vquiz-{round_id}-{i}") == item.answer
                    )
                    gained = correct * XP_PER_QUIZ_ANSWER
                    if gained:
                        self.store.add_xp(gained, "vocabulary quiz")
                    quiz["scored"] = True
                    st.session_state["vquiz-score"] = (correct, len(items), gained)
                    st.rerun()
            else:
                correct, total, gained = st.session_state.get("vquiz-score", (0, len(items), 0))
                st.success(f"Score: {correct}/{total} · +{gained} XP 🎉")

    def _add_word_form(self) -> None:
        with st.expander("＋ Add a new word"):
            with st.form("add-word", clear_on_submit=True):
                phrase = st.text_input("Phrase", placeholder="e.g. break the ice")
                meaning = st.text_input("Meaning", placeholder="e.g. start a conversation")
                example = st.text_input("Example", placeholder="e.g. He told a joke to break the ice.")
                level = st.selectbox("Level", ["A1", "A2", "B1", "B2", "C1"], index=2)
                submitted = st.form_submit_button("Save word")
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
        return not query or query in word.phrase.lower() or query in word.meaning.lower() or query in word.example.lower()
