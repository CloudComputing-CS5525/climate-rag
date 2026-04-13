import os
from pathlib import Path
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:3001").rstrip("/")


def _inject_styles():
    """Claude.ai-matched styling."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        :root {
            --bg:           #FAF9F7;
            --surface:      #FFFFFF;
            --sidebar-bg:   #FFFFFF;
            --sidebar-border:#EBEBEB;
            --border:       #E5E5E2;
            --border-2:     #D4D4D0;
            --text:         #1A1A1A;
            --text-2:       #3D3D3A;
            --muted:        #8C8C89;
            --accent:       #D97757;
            --accent-hover: #C4683E;
            --accent-soft:  #FDF0EB;
            --accent-border:#F5D1C3;
            --radius:       24px;
            --radius-sm:    12px;
        }

        html, body, .stApp {
            background: var(--bg) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif !important;
            color: var(--text) !important;
        }

        [data-testid="stAppViewContainer"] > .main {
            background: var(--bg) !important;
        }
        .block-container {
            max-width: 700px !important;
            padding: 1.5rem 1rem 6rem !important;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background: var(--sidebar-bg) !important;
            border-right: 1px solid var(--sidebar-border) !important;
            min-width: 240px !important;
            max-width: 240px !important;
            width: 240px !important;
        }
        [data-testid="stSidebar"] .block-container {
            padding: 0.75rem 0.6rem !important;
        }
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            gap: 0.35rem !important;
        }

        /* ── Typography ── */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif !important;
            color: var(--text) !important;
        }

        /* ── Welcome screen ── */
        .welcome-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 18vh 1rem 2rem;
            text-align: center;
        }
        .welcome-title {
            font-family: 'Inter', sans-serif;
            font-size: 1.85rem;
            font-weight: 500;
            color: var(--text);
            letter-spacing: -0.02em;
        }
        .welcome-icon {
            color: var(--accent);
            margin-right: 6px;
        }
        .welcome-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            justify-content: center;
            margin-top: 1.25rem;
            max-width: 540px;
        }
        .welcome-chip {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 0.4rem 0.9rem;
            font-size: 0.8rem;
            color: var(--text-2);
            cursor: default;
            transition: border-color 0.15s, background 0.15s;
        }
        .welcome-chip:hover {
            border-color: var(--border-2);
            background: #F5F5F3;
        }

        /* ── Chat messages (shared) ── */
        [data-testid="stChatMessage"] {
            background: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            padding: 0.5rem 0 !important;
            margin-bottom: 0.25rem !important;
            box-shadow: none !important;
            max-width: 700px !important;
        }
        [data-testid="stChatMessage"] p {
            color: var(--text) !important;
            font-size: 0.9rem !important;
            line-height: 1.7 !important;
        }
        /* Hide all avatars */
        [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"],
        [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"],
        [data-testid="stChatMessage"] .stChatMessageAvatarContainer,
        [data-testid="stChatMessage"] > div:first-child:has(img),
        [data-testid="stChatMessage"] > div:first-child:has(svg) {
            display: none !important;
        }

        /* ── User message: right-aligned gray pill ── */
        [data-testid="stChatMessage"][data-testid*="user"],
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            display: flex !important;
            justify-content: flex-end !important;
        }
        [data-testid="stChatMessage"][data-testid*="user"] > div:last-child,
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) > div:last-child {
            background: #E8E8E4 !important;
            border-radius: 18px !important;
            padding: 0.6rem 1rem !important;
            max-width: 75% !important;
            width: fit-content !important;
            margin-left: auto !important;
        }

        /* ── Assistant message: left-aligned, no bubble ── */
        [data-testid="stChatMessage"][data-testid*="assistant"],
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
            display: flex !important;
            justify-content: flex-start !important;
        }
        [data-testid="stChatMessage"][data-testid*="assistant"] > div:last-child,
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) > div:last-child {
            background: transparent !important;
            padding: 0.4rem 0 !important;
            max-width: 100% !important;
        }

        /* ── Chat input — single pill, no double border ── */
        [data-testid="stChatInput"] {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: 20px !important;
            box-shadow: none !important;
        }
        [data-testid="stChatInput"]:focus-within {
            border-color: var(--border-2) !important;
        }
        /* Kill inner container borders/bg */
        [data-testid="stChatInput"] > div,
        [data-testid="stChatInput"] > div > div,
        [data-testid="stChatInput"] form,
        [data-testid="stChatInput"] [data-baseweb] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
        }
        [data-testid="stChatInput"] textarea {
            background: transparent !important;
            color: var(--text) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.85rem !important;
            line-height: 1.5 !important;
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: var(--muted) !important;
            font-size: 0.85rem !important;
        }
        /* Send button — dark circle */
        [data-testid="stChatInput"] button,
        [data-testid="stChatInputSubmitButton"] button {
            border-radius: 50% !important;
            border: none !important;
            background: var(--text) !important;
            color: var(--surface) !important;
            width: 28px !important;
            height: 28px !important;
            min-width: 28px !important;
            min-height: 28px !important;
            padding: 0 !important;
        }
        [data-testid="stChatInput"] button:hover,
        [data-testid="stChatInputSubmitButton"] button:hover {
            background: var(--text-2) !important;
        }
        [data-testid="stChatInput"] button svg {
            width: 14px !important;
            height: 14px !important;
        }

        /* Bottom dock — flush with page bg */
        [data-testid="stBottom"],
        [data-testid="stBottom"] > div,
        [data-testid="stChatFloatingInputContainer"],
        [data-testid="stChatFloatingInputContainer"] > section,
        [data-testid="stChatFloatingInputContainer"] > div {
            background: var(--bg) !important;
            background-color: var(--bg) !important;
            border-top: none !important;
            box-shadow: none !important;
        }

        /* ── Spinner / processing state ── */
        [data-testid="stSpinner"] {
            padding: 0.5rem 0 !important;
        }
        [data-testid="stSpinner"] > div {
            display: flex !important;
            align-items: center !important;
            gap: 0.5rem !important;
        }
        [data-testid="stSpinner"] p {
            color: var(--muted) !important;
            font-size: 0.85rem !important;
            font-family: 'Inter', sans-serif !important;
        }
        /* Style the status/toast messages during processing */
        [data-testid="stStatusWidget"],
        .stAlert {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-sm) !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* ── Sidebar nav buttons (icon + label on one line) ── */
        [data-testid="stSidebar"] .stButton > button {
            background: transparent !important;
            color: var(--text-2) !important;
            border: none !important;
            border-radius: 6px !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.85rem !important;
            padding: 0.4rem 0.6rem !important;
            text-align: left !important;
            justify-content: flex-start !important;
            transition: background 0.12s ease !important;
            font-weight: 400 !important;
            min-height: 0 !important;
            line-height: 1.4 !important;
            letter-spacing: 0 !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: #F0F0EE !important;
            color: var(--text) !important;
        }
        /* Streamlit nests label in flex — force left alignment */
        [data-testid="stSidebar"] .stButton > button > div {
            display: flex !important;
            justify-content: flex-start !important;
            align-items: center !important;
            width: 100% !important;
        }
        [data-testid="stSidebar"] .stButton > button p {
            text-align: left !important;
            width: 100% !important;
        }
        /* Recents section — clear of button hover, slightly larger label */
        p.sidebar-recents-heading {
            font-size: 0.875rem !important;
            font-weight: 400 !important;
            color: #6b6b66 !important;
            font-family: Inter, sans-serif !important;
            text-align: left !important;
            margin: 0.75rem 0 0.15rem 0.15rem !important;
            padding: 0.2rem 0.25rem 0.5rem 0 !important;
            line-height: 1.35 !important;
            position: relative !important;
            z-index: 4 !important;
        }
        .sidebar-recents-spacer {
            display: block;
            height: 10px;
            margin: 0;
            padding: 0;
        }
        /* Remove extra spacing around sidebar dividers */
        [data-testid="stSidebar"] hr {
            margin: 0.4rem 0 !important;
        }

        /* ── Expander (sources) ── */
        [data-testid="stExpander"] {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-sm) !important;
            box-shadow: none !important;
            outline: none !important;
        }
        [data-testid="stExpander"] summary {
            color: var(--muted) !important;
            font-size: 0.85rem !important;
        }
        [data-testid="stExpander"]:focus,
        [data-testid="stExpander"]:focus-within {
            border-color: var(--border) !important;
            outline: none !important;
            box-shadow: none !important;
        }

        /* ── Citation tags ── */
        .cite-tag {
            display: inline-block;
            background: var(--accent-soft);
            color: var(--accent);
            border: 1px solid var(--accent-border);
            border-radius: 6px;
            padding: 1px 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            font-weight: 500;
            margin-right: 4px;
        }
        .score-badge {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--muted);
        }

        /* ── Misc ── */
        [data-testid="stCaptionContainer"] p,
        .stCaption {
            color: var(--muted) !important;
            font-size: 0.8rem !important;
        }
        [data-testid="stSpinner"] p {
            color: var(--muted) !important;
            font-size: 0.85rem !important;
        }

        hr { border-color: var(--border) !important; }

        /* Hide Streamlit chrome */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header[data-testid="stHeader"] { background: transparent !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── Cached fetchers ───────────────────────────────────────────
@st.cache_data(ttl=30)
def fetch_history():
    try:
        res = requests.get(f"{BACKEND_URL}/history", timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception:
        return []


# ── Page setup ────────────────────────────────────────────────
st.set_page_config(
    page_title="Climate Research Assistant",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded",
)
_inject_styles()


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    # ── App title ──
    st.markdown(
        """
        <div style="display:flex;align-items:center;justify-content:flex-start;
                    padding:0.6rem 0.4rem 0.4rem;margin-bottom:0.25rem;">
            <span style="font-size:1.15rem;font-weight:600;color:#1A1A1A;
                         font-family:Inter,sans-serif;letter-spacing:-0.01em;">
                Climate RAG
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("+ New chat", key="nav_new_chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("last_citations", None)
        st.session_state.pop("last_confidence", None)
        st.session_state.chat_id = None
        st.rerun()

    # ── Recents ──
    st.markdown(
        '<p class="sidebar-recents-heading">Recents</p>'
        '<div class="sidebar-recents-spacer" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )

    hist_data = fetch_history() or []
    if hist_data:
        for entry in reversed(hist_data[-15:]):
            title = entry.get("title", "Untitled")[:38]
            if st.button(title, key=f"hist_{entry.get('chat_id','')}",
                         use_container_width=True):
                st.session_state.chat_id = entry.get("chat_id")
                st.session_state.messages = []
                for msg in entry.get("messages", []):
                    st.session_state.messages.extend([
                        {"role": "user",      "content": msg.get("query", "")},
                        {"role": "assistant", "content": msg.get("answer", ""),
                         "meta": {"tool_calls":     msg.get("tool_calls", []),
                                  "num_iterations": msg.get("num_iterations", 0)}},
                    ])
                last_msg = (entry.get("messages") or [{}])[-1]
                st.session_state["last_citations"] = last_msg.get("chunks", [])
                st.session_state["last_confidence"] = last_msg.get("confidence", 0.0)
                st.rerun()
    else:
        st.caption("No conversations yet.")


# ── Main area ─────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

# Welcome screen (shown when no messages)
if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-container">
            <div class="welcome-title">
                <span class="welcome-icon">&#10044;</span>Climate Research Assistant
            </div>
            <div class="welcome-chips">
                <span class="welcome-chip">What causes ocean acidification?</span>
                <span class="welcome-chip">Recent trends in Arctic ice loss</span>
                <span class="welcome-chip">Carbon capture methods</span>
                <span class="welcome-chip">How do aerosols affect climate?</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Render messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        meta = message.get("meta")
        if meta and meta.get("tool_calls"):
            st.caption(f"used {' · '.join(meta['tool_calls'])}")

# Citations panel
if st.session_state.get("last_citations"):
    with st.expander(
        f"Sources ({len(st.session_state['last_citations'])}) "
        f"· confidence {float(st.session_state.get('last_confidence', 0)):.3f}",
        expanded=False,
    ):
        for i, chunk in enumerate(st.session_state["last_citations"], start=1):
            col_a, col_b = st.columns([1, 8])
            with col_a:
                st.markdown(
                    f'<span class="cite-tag">[{i}]</span>',
                    unsafe_allow_html=True,
                )
            with col_b:
                st.markdown(
                    f"**{chunk.get('title', 'Unknown')}** · "
                    f"*{chunk.get('section', '')}*"
                )
                st.markdown(
                    f'<span class="score-badge">'
                    f"score {round(chunk.get('score', 0), 3)}</span>",
                    unsafe_allow_html=True,
                )
                st.caption(chunk.get("text", ""))
            if i < len(st.session_state["last_citations"]):
                st.divider()

# Chat input
prompt = st.chat_input("How can I help you today?")


# ── Handle input ──────────────────────────────────────────────
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {
                    "question":     prompt,
                    "top_k":        5,
                    "chat_id":      st.session_state.get("chat_id"),
                    "chat_history": st.session_state.messages[:-1],
                }
                res = requests.post(
                    f"{BACKEND_URL}/query", json=payload, timeout=60
                )
                res.raise_for_status()
                data = res.json()

                if "chat_id" in data:
                    st.session_state.chat_id = data["chat_id"]

                answer         = data.get("answer", "No answer provided.")
                citations      = data.get("citations", [])
                confidence     = data.get("confidence", 0.0)
                tool_calls     = data.get("tool_calls", [])
                num_iterations = data.get("num_iterations", 0)

                st.markdown(answer)

                st.session_state.messages.append({
                    "role":    "assistant",
                    "content": answer,
                    "meta":    {
                        "tool_calls": tool_calls,
                        "num_iterations": num_iterations,
                    },
                })
                st.session_state["last_citations"] = citations
                st.session_state["last_confidence"] = confidence

                fetch_history.clear()

            except Exception as e:
                err = f"Backend error: {e}"
                st.error(err)
                st.session_state.messages.append(
                    {"role": "assistant", "content": err}
                )

    st.rerun()
