import streamlit as st


def configure_page() -> None:
    st.set_page_config(
        page_title="LingoLift | English Learning",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
        :root { --ink:#17221f; --muted:#6d7771; --paper:#f7f8f3; --mint:#b8e7cf; --green:#1e6b4b; --coral:#ef836d; --line:#dce4dc; }
        * { font-family:'DM Sans',sans-serif; }
        .stApp { background:var(--paper); color:var(--ink); background-image:radial-gradient(#dbe7dd .7px,transparent .7px); background-size:18px 18px; }
        [data-testid='stSidebar'] { background:#eef4ed; border-right:1px solid var(--line); }
        [data-testid='stSidebar'] > div:first-child { padding-top:2rem; }
        .topbar { border-bottom:1px solid var(--line); padding:1rem 0 .8rem; margin-bottom:.7rem; }
        .brand { display:flex; align-items:center; gap:10px; margin-bottom:2rem; }
        .topbar .brand { margin-bottom:0; }
        .brand-mark { width:38px; height:38px; display:grid; place-items:center; background:var(--coral); border-radius:12px; font-size:20px; transform:rotate(-6deg); }
        .brand-name { font-family:'Space Grotesk'; font-size:22px; font-weight:700; }
        .eyebrow { color:var(--green); font-size:12px; font-weight:700; letter-spacing:1.3px; text-transform:uppercase; }
        h1,h2,h3 { font-family:'Space Grotesk',sans-serif; letter-spacing:-1px; color:var(--ink); }
        h1 { font-size:clamp(2.1rem,4vw,4.2rem); line-height:.98; margin:.35rem 0 1rem; }
        h2 { font-size:25px; margin:0; } h3 { font-size:17px; letter-spacing:-.3px; }
        .muted { color:var(--muted); } .hero { padding:1.2rem 0 1.7rem; }
        .hero-copy { max-width:560px; font-size:16px; line-height:1.6; color:var(--muted); }
        .hero-note { color:var(--green); font-weight:700; }
        .section-label { display:flex; justify-content:space-between; align-items:center; margin:1.7rem 0 .9rem; }
        .section-label span { color:var(--muted); font-size:13px; }
        .card { background:rgba(255,255,255,.88); border:1px solid var(--line); border-radius:18px; padding:18px; box-shadow:0 10px 28px rgba(32,61,45,.05); }
        .stat-number { font-family:'Space Grotesk'; font-size:28px; font-weight:700; }
        .stat-label { color:var(--muted); font-size:12px; margin-top:2px; }
        .lesson-card { min-height:172px; position:relative; overflow:hidden; }
        .lesson-card:after { content:''; position:absolute; right:-30px; bottom:-34px; width:110px; height:110px; border-radius:50%; background:var(--mint); opacity:.7; }
        .lesson-icon { font-size:26px; margin-bottom:12px; } .lesson-meta { color:var(--muted); font-size:12px; }
        .featured-lesson { background:#fff4df; border-color:#e4bd7e; }
        .featured-lesson:after { background:#f2c879; opacity:.8; }
        .featured-lesson .eyebrow { color:#a45e20; }
        .lesson-badge { display:inline-block; margin-bottom:10px; padding:4px 8px; border-radius:999px; background:#18382d; color:#fff; font-size:10px; font-weight:700; letter-spacing:.7px; text-transform:uppercase; }
        .audio-shell { background:#18382d; border-radius:17px; padding:16px; color:white; }
        .audio-title { font-family:'Space Grotesk'; font-size:18px; margin-bottom:8px; }
        .word { color:var(--coral); font-weight:700; }
        .chat-wrap { background:rgba(255,255,255,.7); border:1px solid var(--line); border-radius:18px; padding:12px; }
        .tip { background:#fff0db; border-left:4px solid var(--coral); border-radius:8px; padding:12px 14px; font-size:13px; line-height:1.5; }
        .stButton > button { border-radius:10px; border:1px solid var(--line); font-weight:600; color:var(--ink); }
        .stButton > button:hover { border-color:var(--green); color:var(--green); }
        .stProgress > div > div > div { background:var(--green); }
        [data-testid='stChatInput'] { background:transparent; border:0; box-shadow:none; padding:0; }
        [data-testid='stChatInput'] textarea { background:transparent; border:0; border-bottom:1px solid var(--line); border-radius:0; box-shadow:none; padding-left:0; }
        [data-testid='stChatInput'] textarea:focus { border-bottom-color:var(--green); box-shadow:none; }
        [data-testid='stMetricValue'] { font-family:'Space Grotesk'; }
        [data-testid='stChatMessage'] { background:rgba(255,255,255,.78); border-radius:14px; }
        </style>
        """,
        unsafe_allow_html=True,
    )
