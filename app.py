import streamlit as st

from services import TutorService
from storage import get_store
from ui.chat import ChatPage
from ui.dashboard import DashboardPage
from ui.styles import configure_page
from ui.vocabulary import VocabularyPage

GREETING = "Hi! I'm your English tutor. What would you like to practice today?"


@st.cache_resource(show_spinner=False)
def _store():
    return get_store()


class LingoLiftApp:
    def __init__(self) -> None:
        self.tutor = TutorService()
        self.store = _store()
        self.pages = {
            "Overview": DashboardPage(self.store),
            "Practice with AI": ChatPage(self.tutor, self.store),
            "My vocabulary": VocabularyPage(self.store),
        }

    def initialize_state(self) -> None:
        if "messages" not in st.session_state:
            messages = self.store.get_messages()
            if not messages:
                messages = [{"role": "assistant", "content": GREETING}]
                self.store.add_message("assistant", GREETING)
            st.session_state.messages = messages
        if "lesson_prompt" not in st.session_state:
            st.session_state.lesson_prompt = None

    def run(self) -> None:
        page_routes = {
            "Overview": st.Page(
                self.pages["Overview"].render,
                title="Overview",
                icon=":material/home:",
                url_path="overview",
            ),
            "Practice with AI": st.Page(
                self.pages["Practice with AI"].render,
                title="Practice with AI",
                icon=":material/forum:",
                url_path="practice",
            ),
            "My vocabulary": st.Page(
                self.pages["My vocabulary"].render,
                title="My vocabulary",
                icon=":material/menu_book:",
                url_path="vocabulary",
            ),
        }
        st.session_state.page_routes = page_routes
        navigation = st.navigation(list(page_routes.values()), position="top")
        self.initialize_state()
        navigation.run()


if __name__ == "__main__":
    # set_page_config must be the first Streamlit call of every run.
    configure_page()
    LingoLiftApp().run()
