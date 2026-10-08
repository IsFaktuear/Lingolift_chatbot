import streamlit as st

from storage import Store


class VocabularyPage:
    def __init__(self, store: Store) -> None:
        self.store = store

    def render(self) -> None:
        st.markdown('<div class="eyebrow">Your word bank</div>', unsafe_allow_html=True)
        st.title("My vocabulary")
        st.caption("Words saved from your lessons and conversations.")
        self._add_word_form()
        search = st.text_input("Search vocabulary", placeholder="Search a phrase or meaning...")
        words = [word for word in self.store.get_words() if self._matches(word, search)]
        if not words:
            st.info("No vocabulary matches that search yet.")
            return
        for word in words:
            st.markdown(f'<div class="card" style="margin:10px 0"><div style="display:flex;justify-content:space-between;align-items:center"><h3 style="margin:0;color:var(--coral)">{word.phrase}</h3><span class="eyebrow">{word.level}</span></div><p class="muted">{word.meaning}</p><p>"{word.example}"</p></div>', unsafe_allow_html=True)

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
