import html
import os
import uuid
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types


# =========================
# LOAD ENV & BASIC CONFIG
# =========================

load_dotenv()

APP_NAME = "ChatinMe"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_OPTIONS = {
    "Gemini 2.5 Flash": "gemini-2.5-flash",
    "Gemini 2.0 Flash": "gemini-2.0-flash",
    "Gemini 1.5 Flash": "gemini-1.5-flash",
}

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================
# SESSION STATE
# =========================

def create_chat(title="New Chat"):
    chat_id = str(uuid.uuid4())

    st.session_state.chats[chat_id] = {
        "title": title,
        "created_at": datetime.now().strftime("%d %b %Y, %H:%M"),
        "messages": [],
        "instructions": "",
        "tone": "Santai",
        "mode": "Daily Planner",
    }

    st.session_state.current_chat_id = chat_id


def init_state():
    defaults = {
        "chats": {},
        "current_chat_id": None,
        "theme": "Light",
        "model_label": list(MODEL_OPTIONS.keys())[0],
        "active_view": "chat",
        "notes": "",
        "todos": [],
        "sidebar_collapsed": False,
        "quick_prompt": None,
        "uploader_key": 0,
        "open_chat_menu": None,
        "prompt_input": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if not st.session_state.chats:
        create_chat("New Chat")


init_state()

ss = st.session_state
current_chat = ss.chats[ss.current_chat_id]


# =========================
# STYLE
# =========================

def colors():
    if ss.theme == "Dark":
        return {
            "bg": "#212121",
            "sidebar": "#171717",
            "surface": "#212121",
            "panel": "#2f2f2f",
            "panel_hover": "#303030",
            "input": "#212121",
            "text": "#ececec",
            "muted": "#b4b4b4",
            "border": "#3f3f3f",
            "active": "#343434",
        }

    return {
        "bg": "#ffffff",
        "sidebar": "#f9f9f9",
        "surface": "#ffffff",
        "panel": "#f7f7f8",
        "panel_hover": "#eeeeee",
        "input": "#ffffff",
        "text": "#202123",
        "muted": "#6b7280",
        "border": "#e5e5e5",
        "active": "#e7e7e7",
    }


def side_width():
    return "68px" if ss.sidebar_collapsed else "292px"


def load_css():
    c = colors()
    width = side_width()

    st.markdown(
        f"""
        <style>
        #MainMenu,
        footer,
        header {{
            visibility: hidden;
        }}

        .stApp {{
            background: {c["bg"]};
            color: {c["text"]};
        }}

        html,
        body,
        [class*="css"] {{
            font-size: 15px;
        }}

        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapseButton"] {{
            display: none !important;
        }}

        .block-container {{
            max-width: 920px;
            padding-top: 0.25rem;
            padding-bottom: 7rem;
        }}

        /* SIDEBAR */
        [data-testid="stSidebar"] {{
            background: {c["sidebar"]};
            border-right: 1px solid {c["border"]};
            min-width: {width} !important;
            width: {width} !important;
        }}

        [data-testid="stSidebar"] .block-container {{
            padding-left: 0.45rem;
            padding-right: 0.45rem;
        }}

        [data-testid="stSidebar"] * {{
            color: {c["text"]};
            text-align: left !important;
        }}

        [data-testid="stSidebar"] .stButton > button {{
            justify-content: flex-start !important;
            text-align: left !important;
            padding-left: 10px !important;
        }}

        [data-testid="stSidebar"] .stButton > button p {{
            text-align: left !important;
            width: 100%;
        }}

        .brand {{
            font-size: 20px;
            font-weight: 700;
            letter-spacing: -0.03em;
            margin: 10px 4px 12px 4px;
        }}

        .brand-icon {{
            align-items: center;
            border-radius: 10px;
            display: inline-flex;
            height: 34px;
            justify-content: center;
            margin: 10px 4px 12px 4px;
            width: 34px;
        }}

        .side-section {{
            color: {c["muted"]} !important;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.04em;
            margin: 18px 10px 8px 10px;
            text-transform: uppercase;
        }}

        .collapsed-spacer {{
            height: 6px;
        }}

        /* TOP */
        .top-shell {{
            align-items: center;
            background: {c["bg"]};
            display: flex;
            justify-content: flex-end;
            min-height: 50px;
            padding: 6px 0 8px 0;
            position: sticky;
            top: 0;
            z-index: 30;
        }}

        .api-pill {{
            align-items: center;
            background: transparent;
            border: 1px solid {c["border"]};
            border-radius: 999px;
            color: {c["muted"]};
            display: flex;
            font-size: 12px;
            gap: 7px;
            justify-content: center;
            min-height: 38px;
            padding: 0 13px;
            white-space: nowrap;
        }}

        .api-dot {{
            background: #10a37f;
            border-radius: 999px;
            height: 7px;
            width: 7px;
        }}

        .api-dot.off {{
            background: #ef4444;
        }}

        /* LANDING */
        .landing {{
            align-items: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 55vh;
            text-align: center;
        }}

        .landing-title {{
            color: {c["text"]};
            font-size: 28px;
            font-weight: 500;
            letter-spacing: -0.03em;
            margin-bottom: 28px;
        }}

        .suggestion-grid {{
            display: grid;
            gap: 12px;
            grid-template-columns: repeat(3, 1fr);
            max-width: 760px;
            width: 100%;
        }}

        .suggestion-card {{
            background: transparent;
            border: 1px solid {c["border"]};
            border-radius: 16px;
            min-height: 94px;
            padding: 16px;
            text-align: left;
        }}

        .suggestion-card b {{
            color: {c["text"]};
            display: block;
            font-size: 14.5px;
            margin-bottom: 7px;
        }}

        .suggestion-card span {{
            color: {c["muted"]};
            font-size: 13.5px;
            line-height: 1.4;
        }}

        /* CHAT */
        .chat-date {{
            color: {c["muted"]};
            font-size: 12px;
            margin: 12px 0 20px 0;
            text-align: center;
        }}

        .msg-row {{
            display: flex;
            margin-bottom: 18px;
            width: 100%;
        }}

        .msg-row.user {{
            justify-content: flex-end;
        }}

        .msg-row.assistant {{
            justify-content: flex-start;
        }}

        .bubble {{
            border-radius: 20px;
            color: {c["text"]};
            font-size: 15.5px;
            line-height: 1.58;
            max-width: 78%;
            padding: 12px 16px;
            white-space: pre-wrap;
            word-break: break-word;
        }}

        .bubble.user {{
            background: {c["panel"]};
            border-bottom-right-radius: 6px;
        }}

        .bubble.assistant {{
            background: transparent;
            border-bottom-left-radius: 6px;
            padding-left: 0;
        }}

        .assistant-wrap {{
            align-items: flex-start;
            display: flex;
            max-width: 100%;
        }}

        .avatar {{
            align-items: center;
            background: transparent;
            border: 1px solid {c["border"]};
            border-radius: 50%;
            color: {c["text"]};
            display: inline-flex;
            flex-shrink: 0;
            font-size: 12px;
            height: 30px;
            justify-content: center;
            margin-right: 10px;
            width: 30px;
        }}

        /* COMPOSER */
        .composer-box {{
            margin: 26px auto 8px auto;
            max-width: 820px;
        }}

        .composer-bottom-wrap {{
            margin-top: 8px;
        }}

        textarea,
        input,
        div[data-baseweb="select"] > div {{
            background: {c["input"]} !important;
            border-color: {c["border"]} !important;
            border-radius: 14px !important;
            color: {c["text"]} !important;
        }}

        .composer-box textarea {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
        }}

        .composer-box [data-testid="stTextArea"] > div > div {{
            background: transparent !important;
            border: 1px solid {c["border"]} !important;
            box-shadow: none !important;
            border-radius: 28px !important;
        }}

        .composer-box [data-testid="stTextArea"] textarea {{
            min-height: 54px !important;
            padding: 15px 18px !important;
            resize: none !important;
        }}

        .stFileUploader section {{
            background: transparent !important;
            border: 1px dashed {c["border"]} !important;
            border-radius: 14px !important;
            box-shadow: none !important;
        }}

        .stFileUploader label {{
            font-size: 13px !important;
            color: {c["muted"]} !important;
        }}

        /* BUTTONS */
        .stButton > button {{
            background: transparent !important;
            border: 1px solid transparent !important;
            border-radius: 10px !important;
            color: {c["text"]} !important;
            font-size: 15px !important;
            font-weight: 500 !important;
            justify-content: flex-start !important;
            min-height: 38px;
            padding-left: 10px !important;
            text-align: left !important;
            width: 100%;
        }}

        .stButton > button:hover {{
            background: {c["panel_hover"]} !important;
        }}

        .stButton > button:focus {{
            box-shadow: none !important;
        }}

        .stButton > button p,
        .stButton > button div,
        .stButton > button span {{
            text-align: left !important;
        }}

        /* PAGE */
        .page-card {{
            background: transparent;
            border: 1px solid {c["border"]};
            border-radius: 18px;
            margin-top: 20px;
            padding: 20px;
        }}

        .page-title {{
            color: {c["text"]};
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }}

        .page-subtitle {{
            color: {c["muted"]};
            margin-bottom: 20px;
        }}

        .api-warning {{
            background: rgba(245, 158, 11, 0.08);
            border: 1px solid rgba(245, 158, 11, 0.35);
            border-radius: 14px;
            color: {c["text"]};
            font-size: 14.5px;
            margin-bottom: 14px;
            padding: 12px 14px;
        }}

        .bottom-note {{
            bottom: 4px;
            color: {c["muted"]};
            font-size: 12px;
            left: {width};
            pointer-events: none;
            position: fixed;
            right: 0;
            text-align: center;
        }}

        .back-top {{
            bottom: 24px;
            position: fixed;
            right: 24px;
            z-index: 120;
        }}

        .back-top a {{
            align-items: center;
            background: transparent;
            border: 1px solid {c["border"]};
            border-radius: 50%;
            color: {c["text"]};
            display: flex;
            font-size: 18px;
            height: 42px;
            justify-content: center;
            text-decoration: none;
            width: 42px;
        }}

        @media screen and (max-width: 920px) {{
            [data-testid="stSidebar"] {{
                min-width: 68px !important;
                width: 68px !important;
            }}

            .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}

            .suggestion-grid {{
                grid-template-columns: 1fr;
            }}

            .bubble {{
                max-width: 88%;
            }}

            .bottom-note {{
                left: 0;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


load_css()


# =========================
# GEMINI FUNCTIONS
# =========================

def get_client():
    if not GEMINI_API_KEY:
        return None

    return genai.Client(api_key=GEMINI_API_KEY)


def get_model_name():
    return MODEL_OPTIONS[ss.model_label]


def build_system_prompt(chat):
    tone_map = {
        "Santai": "Gunakan bahasa santai, ramah, dan mudah dipahami.",
        "Formal": "Gunakan bahasa formal, profesional, dan terstruktur.",
        "Motivatif": "Gunakan bahasa suportif, positif, dan memotivasi.",
    }

    mode_map = {
        "Daily Planner": "Fokus membuat jadwal harian yang realistis.",
        "Task Breakdown": "Fokus memecah tugas besar menjadi langkah kecil.",
        "Priority Coach": "Fokus membantu menentukan prioritas utama.",
        "Study Planner": "Fokus membantu membuat rencana belajar efektif.",
    }

    tone_instruction = tone_map.get(chat["tone"], tone_map["Santai"])
    mode_instruction = mode_map.get(chat["mode"], mode_map["Daily Planner"])
    personalization = chat.get("instructions") or "Tidak ada personalisasi."

    return f"""
Kamu adalah ChatinMe, AI personal assistant untuk produktivitas.

Peranmu:
- Membantu membuat jadwal.
- Membantu memecah tugas besar.
- Membantu menentukan prioritas.
- Membantu membuat catatan dan rencana kerja.
- Memberikan jawaban praktis, rapi, dan mudah dieksekusi.

Gaya bahasa:
{tone_instruction}

Mode:
{mode_instruction}

Customisasi atau personalisasi pengguna:
{personalization}

Aturan:
- Jawab dalam Bahasa Indonesia.
- Jangan terlalu panjang jika tidak perlu.
- Gunakan bullet point, tabel, atau langkah-langkah jika membantu.
- Jika user meminta jadwal, buat dengan format jam yang jelas.
"""


def file_part(uploaded_file):
    if uploaded_file is None:
        return None

    return types.Part.from_bytes(
        data=uploaded_file.getvalue(),
        mime_type=uploaded_file.type or "application/octet-stream",
    )


def generate_response(prompt, chat, files=None, audio_file=None):
    client = get_client()

    if not client:
        return (
            "⚠️ **API key belum terbaca.**\n\n"
            "Pastikan file `.env` berisi:\n\n"
            "`GEMINI_API_KEY=api_key_kamu`"
        )

    history = ""

    for message in chat["messages"][-8:]:
        role = "User" if message["role"] == "user" else "Assistant"
        history += f"{role}: {message['content']}\n"

    final_prompt = f"""
{build_system_prompt(chat)}

Riwayat chat:
{history}

Pesan terbaru:
{prompt}
"""

    contents = [final_prompt]

    if files:
        for item in files:
            part = file_part(item)
            if part is not None:
                contents.append(part)

    if audio_file is not None:
        part = file_part(audio_file)
        if part is not None:
            contents.append(part)

    try:
        response = client.models.generate_content(
            model=get_model_name(),
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=1200,
            ),
        )

        if response.text:
            return response.text

        return "Maaf, saya belum mendapatkan respon. Coba ulangi pertanyaanmu."

    except Exception as error:
        error_text = str(error)

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            return (
                "⚠️ **Kuota Gemini API sedang habis atau terkena limit.**\n\n"
                "Aplikasi sudah terhubung ke Gemini, tetapi request ditolak "
                "karena quota atau rate limit.\n\n"
                "**Solusi:**\n"
                "- Tunggu beberapa menit lalu coba lagi.\n"
                "- Ganti model di top bar.\n"
                "- Gunakan API key atau project lain.\n"
                "- Aktifkan billing jika diperlukan."
            )

        if "503" in error_text or "UNAVAILABLE" in error_text:
            return "⚠️ **Server Gemini sedang sibuk.**\n\nCoba lagi beberapa saat lagi."

        return f"⚠️ **Terjadi error:**\n\n```text\n{error_text}\n```"


# =========================
# CHAT LOGIC
# =========================

def update_chat_title(chat, prompt):
    if chat["title"] in ["New Chat", "Final Project Planner"]:
        title = prompt.strip().replace("\n", " ")
        suffix = "..." if len(title) > 34 else ""
        chat["title"] = title[:34] + suffix


def render_message(role, content):
    safe_content = html.escape(content)

    if role == "user":
        st.markdown(
            f"""
            <div class="msg-row user">
                <div class="bubble user">{safe_content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f"""
        <div class="msg-row assistant">
            <div class="assistant-wrap">
                <div class="avatar">CM</div>
                <div class="bubble assistant">{safe_content}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def process_prompt(prompt, files=None, audio_file=None):
    if not prompt and audio_file is not None:
        prompt = "Transkrip dan jawab pesan suara ini."

    if not prompt:
        return

    shown_prompt = prompt

    if files:
        names = ", ".join(item.name for item in files)
        shown_prompt = f"{prompt}\n\nLampiran: {names}"

    current_chat["messages"].append(
        {
            "role": "user",
            "content": shown_prompt,
        }
    )

    update_chat_title(current_chat, prompt)

    with st.spinner("ChatinMe sedang menjawab..."):
        reply = generate_response(
            prompt,
            current_chat,
            files=files,
            audio_file=audio_file,
        )

        current_chat["messages"].append(
        {
            "role": "assistant",
            "content": reply,
        }
    )

    ss.uploader_key += 1
    st.rerun()


def navigate(view):
    ss.active_view = view
    st.rerun()


def delete_chat(chat_id):
    if len(ss.chats) == 1:
        ss.chats[chat_id]["messages"] = []
        ss.chats[chat_id]["title"] = "New Chat"
        st.rerun()

    del ss.chats[chat_id]
    ss.current_chat_id = next(iter(ss.chats))
    ss.active_view = "chat"
    st.rerun()


# =========================
# DIALOGS
# =========================

@st.dialog("Settings")
def settings_dialog():
    st.write("Atur personalisasi ChatinMe.")

    tone_options = ["Santai", "Formal", "Motivatif"]
    mode_options = [
        "Daily Planner",
        "Task Breakdown",
        "Priority Coach",
        "Study Planner",
    ]

    selected_tone = st.selectbox(
        "Gaya bahasa",
        tone_options,
        index=tone_options.index(current_chat["tone"]),
    )

    selected_mode = st.selectbox(
        "Mode planner",
        mode_options,
        index=mode_options.index(current_chat["mode"]),
    )

    selected_instructions = st.text_area(
        "Customisasi / Personalisasi",
        value=current_chat["instructions"],
        height=180,
        placeholder=(
            "Contoh: Jawab ringkas, pakai checklist, "
            "dan prioritaskan final project saya."
        ),
    )

    col_save, col_close = st.columns(2)

    with col_save:
        if st.button("Simpan", use_container_width=True):
            current_chat["tone"] = selected_tone
            current_chat["mode"] = selected_mode
            current_chat["instructions"] = selected_instructions
            st.rerun()

    with col_close:
        if st.button("Tutup", use_container_width=True):
            st.rerun()


@st.dialog("Dikte Teks")
def dictate_dialog():
    st.caption("Tulis atau tempel hasil dikte, lalu kirim ke ChatinMe.")

    text = st.text_area(
        "Hasil dikte",
        height=130,
        placeholder="Contoh: Buatkan jadwal belajar saya hari ini...",
        label_visibility="collapsed",
    )

    if st.button("Kirim", use_container_width=True):
        if text.strip():
            process_prompt(text.strip())


@st.dialog("Rekam Suara")
def voice_dialog():
    audio = st.audio_input("Rekam pesan suara")

    note = st.text_input(
        "Instruksi tambahan",
        placeholder="Contoh: Buatkan jadwal dari pesan suara ini",
    )

    if st.button("Kirim suara", use_container_width=True):
        prompt = note.strip() or "Transkrip dan jawab pesan suara ini."
        process_prompt(prompt, audio_file=audio)


# =========================
# SIDEBAR
# =========================

def sidebar_button(label, key, icon_name, view=None, new_chat=False):
    icon_map = {
        "new": "✎",
        "search": "⌕",
        "note": "□",
        "todo": "☑",
        "settings": "⚙",
    }

    symbol = icon_map.get(icon_name, "○")

    if ss.sidebar_collapsed:
        button_text = symbol
    else:
        button_text = f"{symbol}  {label}"

    if st.button(button_text, key=key, use_container_width=True):
        if new_chat:
            create_chat("New Chat")
            ss.active_view = "chat"
            st.rerun()

        if view:
            navigate(view)


with st.sidebar:
    collapsed = ss.sidebar_collapsed

    head_left, head_right = st.columns([0.78, 0.22])

    with head_left:
        if collapsed:
            st.markdown(
                "<div class='brand-icon'>◎</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='brand'>ChatinMe</div>",
                unsafe_allow_html=True,
            )

    with head_right:
        collapse_label = "»" if collapsed else "«"
        if st.button(collapse_label, key="collapse_btn"):
            ss.sidebar_collapsed = not collapsed
            st.rerun()

    st.markdown("<div class='collapsed-spacer'></div>", unsafe_allow_html=True)

    sidebar_button("New Chat", "nav_new_chat", "new", new_chat=True)
    sidebar_button("Search Chat", "nav_search", "search", view="chat")
    sidebar_button("Note", "nav_note", "note", view="note")
    sidebar_button("To Do List", "nav_todo", "todo", view="todo")

    if not collapsed:
        st.markdown(
            "<div class='side-section'>Recent Chats</div>",
            unsafe_allow_html=True,
        )

    for chat_id, chat_data in reversed(list(ss.chats.items())):
        if collapsed:
            if st.button("○", key=f"chat_icon_{chat_id}"):
                ss.current_chat_id = chat_id
                ss.active_view = "chat"
                st.rerun()
            continue

        item_col, menu_col = st.columns([0.86, 0.14])

        with item_col:
            active_symbol = "●" if chat_id == ss.current_chat_id else "○"
            title = chat_data["title"]
            short_title = title[:28] + ("..." if len(title) > 28 else "")

            if st.button(
                f"{active_symbol}  {short_title}",
                key=f"history_{chat_id}",
                use_container_width=True,
            ):
                ss.current_chat_id = chat_id
                ss.active_view = "chat"
                st.rerun()

        with menu_col:
            if st.button("⋯", key=f"menu_{chat_id}"):
                ss.open_chat_menu = None if ss.open_chat_menu == chat_id else chat_id
                st.rerun()

        if ss.open_chat_menu == chat_id:
            with st.container():
                new_title = st.text_input(
                    "Rename chat",
                    value=chat_data["title"],
                    key=f"rename_{chat_id}",
                    label_visibility="collapsed",
                )

                menu_action_col, delete_action_col = st.columns(2)

                with menu_action_col:
                    if st.button("Rename", key=f"save_rename_{chat_id}"):
                        clean_title = new_title.strip()
                        if clean_title:
                            ss.chats[chat_id]["title"] = clean_title
                        ss.open_chat_menu = None
                        st.rerun()

                with delete_action_col:
                    if st.button("Delete", key=f"delete_chat_{chat_id}"):
                        delete_chat(chat_id)

    st.markdown("---")

    if st.button(
        "⚙" if collapsed else "⚙  Settings",
        key="open_settings",
        use_container_width=True,
    ):
        settings_dialog()


# =========================
# TOP BAR
# =========================

st.markdown(
    """
    <div id="top"></div>
    <div class="back-top">
        <a href="#top" title="Back to top">↑</a>
    </div>
    """,
    unsafe_allow_html=True,
)

api_text = "API connected" if GEMINI_API_KEY else "API not found"
api_class = "api-dot" if GEMINI_API_KEY else "api-dot off"

model_labels = list(MODEL_OPTIONS.keys())

st.markdown("<div class='top-shell'>", unsafe_allow_html=True)

ctrl_one, ctrl_two, ctrl_three = st.columns([0.18, 0.25, 0.30])

with ctrl_one:
    selected_theme = st.selectbox(
        "Theme",
        ["Light", "Dark"],
        index=0 if ss.theme == "Light" else 1,
        label_visibility="collapsed",
    )

with ctrl_two:
    selected_model = st.selectbox(
        "Model",
        model_labels,
        index=model_labels.index(ss.model_label),
        label_visibility="collapsed",
    )

with ctrl_three:
    st.markdown(
        f"""
        <div class="api-pill">
            <span class="{api_class}"></span>
            <span>{api_text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

if selected_theme != ss.theme:
    ss.theme = selected_theme
    st.rerun()

if selected_model != ss.model_label:
    ss.model_label = selected_model
    st.rerun()


# =========================
# MAIN CONTENT
# =========================

if ss.active_view == "chat":
    if not GEMINI_API_KEY:
        st.markdown(
            """
            <div class="api-warning">
                API key belum terbaca. Pastikan file <b>.env</b> benar.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if not current_chat["messages"]:
        st.markdown(
            """
            <div class="landing">
                <div class="landing-title">
                    Apa rencana anda hari ini?
                </div>
                <div class="suggestion-grid">
                    <div class="suggestion-card">
                        <b>⟡ Buat jadwal</b>
                        <span>
                            Susun jadwal harian untuk target penting.
                        </span>
                    </div>
                    <div class="suggestion-card">
                        <b>⌘ Pecah tugas</b>
                        <span>
                            Ubah project besar menjadi langkah kecil.
                        </span>
                    </div>
                    <div class="suggestion-card">
                        <b>↯ Tentukan prioritas</b>
                        <span>
                            Pilih pekerjaan paling penting.
                        </span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div class='chat-date'>{current_chat['created_at']}</div>",
            unsafe_allow_html=True,
        )

        for message in current_chat["messages"]:
            render_message(message["role"], message["content"])

    st.markdown("<div class='composer-box'>", unsafe_allow_html=True)

    prompt_text = st.text_area(
        "Tanyakan apa saja",
        key="prompt_input",
        placeholder="Tanyakan apa saja",
        height=68,
        label_visibility="collapsed",
    )

    st.markdown(
        "<div class='composer-bottom-wrap'>",
        unsafe_allow_html=True,
    )

    upload_col, dictate_col, voice_col, send_col = st.columns(
        [0.50, 0.16, 0.16, 0.18]
    )

    with upload_col:
        uploaded_files = st.file_uploader(
            "Upload atau drag and drop file",
            accept_multiple_files=True,
            type=[
                "txt",
                "md",
                "csv",
                "pdf",
                "png",
                "jpg",
                "jpeg",
                "wav",
            ],
            key=f"chat_files_{ss.uploader_key}",
        )

    with dictate_col:
        if st.button("🎙 Dikte", key="composer_dictate", use_container_width=True):
            dictate_dialog()

    with voice_col:
        if st.button("◉ Suara", key="composer_voice", use_container_width=True):
            voice_dialog()

    with send_col:
        if st.button("Kirim ↑", key="send_prompt", use_container_width=True):
            process_prompt(
                prompt_text.strip(),
                files=uploaded_files if uploaded_files else None,
            )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


elif ss.active_view == "note":
    st.markdown(
        """
        <div class="page-card">
            <div class="page-title">Note</div>
            <div class="page-subtitle">
                Gunakan halaman ini untuk mencatat ide, prompt,
                ringkasan, atau rencana final project.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    ss.notes = st.text_area(
        "Catatan",
        value=ss.notes,
        height=420,
        placeholder="Tulis catatan kamu di sini...",
        label_visibility="collapsed",
    )

    note_col_one, note_col_two = st.columns(2)

    with note_col_one:
        if st.button("Simpan Note", use_container_width=True):
            st.success("Note tersimpan selama sesi aplikasi berjalan.")

    with note_col_two:
        if st.button("Bersihkan Note", use_container_width=True):
            ss.notes = ""
            st.rerun()


elif ss.active_view == "todo":
    st.markdown(
        """
        <div class="page-card">
            <div class="page-title">To Do List</div>
            <div class="page-subtitle">
                Buat daftar tugas untuk planner atau final project kamu.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    todo_text = st.text_input(
        "Tambah task",
        placeholder="Contoh: Rapikan README.md untuk GitHub",
        label_visibility="collapsed",
    )

    if st.button("Tambah Task", use_container_width=True):
        if todo_text.strip():
            ss.todos.append(
                {
                    "id": str(uuid.uuid4()),
                    "text": todo_text.strip(),
                    "done": False,
                }
            )
            st.rerun()

    if not ss.todos:
        st.info("Belum ada task. Tambahkan task pertama kamu.")
    else:
        for index, todo in enumerate(ss.todos):
            check_col, text_col, delete_col = st.columns([0.12, 0.72, 0.16])

            with check_col:
                checked = st.checkbox(
                    "",
                    value=todo["done"],
                    key=f"todo_check_{todo['id']}",
                    label_visibility="collapsed",
                )
                ss.todos[index]["done"] = checked

            with text_col:
                if todo["done"]:
                    st.markdown(f"~~{todo['text']}~~")
                else:
                    st.markdown(todo["text"])

            with delete_col:
                if st.button(
                    "Delete",
                    key=f"delete_{todo['id']}",
                    use_container_width=True,
                ):
                    ss.todos.pop(index)
                    st.rerun()

        if st.button("Clear Completed", use_container_width=True):
            ss.todos = [todo for todo in ss.todos if not todo["done"]]
            st.rerun()


st.markdown(
    (
        "<div class='bottom-note'>"
        "ChatinMe dapat membuat kesalahan. "
        "Periksa kembali jawaban penting."
        "</div>"
    ),
    unsafe_allow_html=True,
)