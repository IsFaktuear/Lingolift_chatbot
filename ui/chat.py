import streamlit as st

from services import TutorService
from storage import Store, XP_PER_CHAT_MESSAGE


class ChatPage:
    def __init__(self, tutor: TutorService, store: Store) -> None:
        self.tutor = tutor
        self.store = store

    def render(self) -> None:
        st.markdown('<div class="eyebrow">Speaking studio</div>', unsafe_allow_html=True)
        st.title("Practice with your AI tutor")
        st.markdown("Ask in English, mix in Bahasa Indonesia when you get stuck, or use one of the prompts below.")
        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        st.markdown('</div>', unsafe_allow_html=True)

        chat_prompt = st.chat_input("Type a message in English...")
        lesson_prompt = st.session_state.pop("lesson_prompt", None)
        prompt = lesson_prompt or chat_prompt
        if prompt:
            self._send_message(prompt)

    def _send_message(self, prompt: str) -> None:
        st.session_state.messages.append({"role": "user", "content": prompt})
        self.store.add_message("user", prompt)
        self.store.add_xp(XP_PER_CHAT_MESSAGE, "chat message")
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer = self.tutor.reply(st.session_state.messages)
                except Exception:
                    answer = "I couldn't reach the AI service right now. Check your API settings."
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        self.store.add_message("assistant", answer)
