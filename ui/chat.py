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
        voice = st.audio_input("🎤 Or speak instead", key="voice-input")
        lesson_prompt = st.session_state.pop("lesson_prompt", None)
        prompt = lesson_prompt or chat_prompt
        if prompt:
            self._send_message(prompt)
        elif voice is not None:
            self._handle_voice(voice)

    def _handle_voice(self, voice) -> None:
        # Guard against re-processing the same recording on reruns.
        if st.session_state.get("last_voice_id") == voice.id:
            return
        st.session_state.last_voice_id = voice.id
        with st.spinner("Transcribing your voice..."):
            text = self.tutor.transcribe(voice.getvalue())
        if text:
            self._send_message(text)
        else:
            st.info(
                "Voice transcription needs an AI API key (`OPENAI_API_KEY`). "
                "You can still type your message."
            )

    def _send_message(self, prompt: str) -> None:
        st.session_state.messages.append({"role": "user", "content": prompt})
        self.store.add_message("user", prompt)
        self.store.add_xp(XP_PER_CHAT_MESSAGE, "chat message")
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                answer = st.write_stream(self.tutor.reply_stream(st.session_state.messages))
            except Exception:
                answer = self.tutor.reply(st.session_state.messages)
                st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        self.store.add_message("assistant", answer)
