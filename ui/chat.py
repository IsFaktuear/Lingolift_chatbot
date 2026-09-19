import streamlit as st

from services import TutorService


class ChatPage:
    def __init__(self, tutor: TutorService) -> None:
        self.tutor = tutor

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
