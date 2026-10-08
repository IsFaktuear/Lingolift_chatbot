import streamlit as st
from pathlib import Path


def configure_page() -> None:
    st.set_page_config(
        page_title="LingoLift | English Learning",
        page_icon="\U0001F4DA",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    # Read the CSS fresh from disk on every run, so style tweaks apply
    # without restarting the app.
    css_path = Path(__file__).with_name("styles.css")
    st.markdown(
        "<style>" + css_path.read_text(encoding="utf-8") + "</style>",
        unsafe_allow_html=True,
    )
