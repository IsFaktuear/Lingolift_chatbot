from html import escape

import streamlit as st

from services import TutorError, TutorService
from storage import XP_PER_CHAT_MESSAGE, Store

AVATARS = {"assistant": "🦉", "user": "🙂"}


def markdown_code(text: str) -> str:
    """Escape text and turn `backticks` into <code> for the HTML notice."""
    parts = escape(text).split("`")
    return "".join(f"<code>{p}</code>" if i % 2 else p for i, p in enumerate(parts))


class ChatPage:
    def __init__(self, tutor: TutorService, store: Store) -> None:
        self.tutor = tutor
        self.store = store

    def render(self) -> None:
        head, action = st.columns([4, 1], vertical_alignment="bottom")
        with head:
            st.markdown('<div class="eyebrow">Chat studio</div>', unsafe_allow_html=True)
            st.title("Practice with your AI tutor")
            st.markdown(
                '<p class="page-lead">Write in English, mix in Bahasa Indonesia when you get stuck, '
                "or start from a lesson prompt.</p>",
                unsafe_allow_html=True,
            )
        with action:
            if st.button("Clear chat", icon=":material/delete_sweep:", use_container_width=True):
                self._clear_chat_dialog()

        problem = self.tutor.setup_problem()
        if problem:
            st.markdown(
                '<div class="notice"><b>Demo mode — AI is not connected.</b><br>'
                + markdown_code(problem)
                + "<br>After fixing it, stop the app (Ctrl+C) and run <code>streamlit run app.py</code> again.</div>",
                unsafe_allow_html=True,
            )

        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=AVATARS.get(message["role"])):
                st.markdown(message["content"])
        chat_prompt = st.chat_input("Type a message in English...")
        lesson_prompt = st.session_state.pop("lesson_prompt", None)
        prompt = lesson_prompt or chat_prompt
        if prompt:
            self._send_message(prompt)

    @st.dialog("Clear chat history?")
    def _clear_chat_dialog(self) -> None:
        st.write("All messages will be deleted. Your XP and lessons are kept.")
        yes, no = st.columns(2)
        if yes.button("Yes, clear", type="primary", use_container_width=True):
            self.store.clear_messages()
            st.session_state.pop("messages", None)
            st.rerun()
        if no.button("Cancel", use_container_width=True):
            st.rerun()

    def _send_message(self, prompt: str) -> None:
        with st.chat_message("user", avatar=AVATARS["user"]):
            st.markdown(prompt)

        if not self.tutor.is_live:
            # Demo: show a canned reply, but keep history and XP clean.
            with st.chat_message("assistant", avatar=AVATARS["assistant"]):
                st.markdown(self.tutor.DEMO_MESSAGE)
            return

        history = [*st.session_state.messages, {"role": "user", "content": prompt}]
        with st.chat_message("assistant", avatar=AVATARS["assistant"]):
            try:
                answer = st.write_stream(self.tutor.reply_stream(history))
            except TutorError as exc:
                st.error("I couldn't reach the AI service. Check your API key, base URL and model in `.env`.")
                st.caption(str(exc))
                return  # nothing saved, no XP

        if not isinstance(answer, str) or not answer.strip():
            st.warning("The AI returned an empty reply. Try again.")
            return

        st.session_state.messages = [*history, {"role": "assistant", "content": answer}]
        self.store.add_message("user", prompt)
        self.store.add_message("assistant", answer)
        self.store.add_xp_capped(XP_PER_CHAT_MESSAGE, "chat message")
