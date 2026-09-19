import streamlit as st

from services import TutorService
from ui.chat import ChatPage
from ui.dashboard import DashboardPage
from ui.styles import configure_page
from ui.vocabulary import VocabularyPage


class LingoLiftApp:
    def __init__(self) -> None:
        self.tutor = TutorService()
        self.pages = {
            "Overview": DashboardPage(),
            "Practice with AI": ChatPage(self.tutor),
            "My vocabulary": VocabularyPage(),
        }

    def initialize_state(self) -> None:
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Hi! I'm your English tutor. What would you like to practice today?",
                }
            ]
        if "lesson_prompt" not in st.session_state:
            st.session_state.lesson_prompt = None

    def run(self) -> None:
        configure_page()
        self.initialize_state()
        page_routes = {
            "Overview": st.Page(
                self.pages["Overview"].render,
                title="Overview",
                url_path="overview",
            ),
            "Practice with AI": st.Page(
                self.pages["Practice with AI"].render,
                title="Practice with AI",
                url_path="practice",
            ),
            "My vocabulary": st.Page(
                self.pages["My vocabulary"].render,
                title="My vocabulary",
                url_path="vocabulary",
            ),
        }
        st.session_state.page_routes = page_routes
        navigation = st.navigation(
            list(page_routes.values()),
            position="top",
        )
        navigation.run()


if __name__ == "__main__":
    LingoLiftApp().run()
