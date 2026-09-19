import streamlit as st

from content import VOCABULARY


class VocabularyPage:
    def render(self) -> None:
        st.markdown('<div class="eyebrow">Your word bank</div>', unsafe_allow_html=True)
        st.title("My vocabulary")
        st.caption("Words saved from your lessons and conversations.")
        search = st.text_input("Search vocabulary", placeholder="Search a phrase or meaning...")
        words = [word for word in VOCABULARY if self._matches(word, search)]
        if not words:
            st.info("No vocabulary matches that search yet.")
            return
        for word in words:
            st.markdown(f'<div class="card" style="margin:10px 0"><div style="display:flex;justify-content:space-between;align-items:center"><h3 style="margin:0;color:var(--coral)">{word.phrase}</h3><span class="eyebrow">{word.level}</span></div><p class="muted">{word.meaning}</p><p>"{word.example}"</p></div>', unsafe_allow_html=True)

    @staticmethod
    def _matches(word, search: str) -> bool:
        query = search.strip().lower()
        return not query or query in word.phrase.lower() or query in word.meaning.lower() or query in word.example.lower()
