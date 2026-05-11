def get_css(theme: str = "Light", collapsed: bool = False) -> str:
    is_dark = theme == "Dark"

    bg = "#0f172a" if is_dark else "#ffffff"
    card = "#1e293b" if is_dark else "#ffffff"
    text = "#e5e7eb" if is_dark else "#0f172a"
    muted = "#94a3b8" if is_dark else "#64748b"
    border = "#334155" if is_dark else "#e2e8f0"
    user_bubble = "#2563eb"
    assistant_bubble = "#334155" if is_dark else "#f8fafc"

    sidebar_width = "72px" if collapsed else "290px"

    return f"""
    <style>
    .stApp {{
        background: {bg};
        color: {text};
    }}

    /* ========== SIDEBAR ========== */
    section[data-testid="stSidebar"] {{
        width: {sidebar_width} !important;
        background: {card};
        border-right: 1px solid {border};
    }}

    section[data-testid="stSidebar"] * {{
        text-align: left !important;
    }}

    section[data-testid="stSidebar"] .stButton > button {{
        justify-content: flex-start !important;
        text-align: left !important;
        padding-left: 12px !important;
    }}

    section[data-testid="stSidebar"] .stPopover > button {{
        justify-content: center !important;
        text-align: center !important;
    }}

    .sidebar-space {{
        padding: 12px 4px;
    }}

    .brand-full {{
        font-size: 24px;
        font-weight: 800;
        color: {text};
        padding: 8px 0 16px;
        text-align: left !important;
    }}

    .brand-collapsed {{
        font-size: 26px;
        text-align: center !important;
        padding: 8px 0 16px;
    }}

    .section-title {{
        margin-top: 18px;
        margin-bottom: 8px;
        font-size: 13px;
        color: {muted};
        font-weight: 700;
        text-transform: uppercase;
        text-align: left !important;
    }}

    .soft-divider {{
        height: 1px;
        background: {border};
        margin: 14px 0;
    }}

    .soft-divider.bottom {{
        margin-top: 20px;
    }}

    /* ========== MAIN ========== */
    .app-shell {{
        max-width: 1100px;
        margin: 0 auto;
        padding: 12px 20px 70px;
    }}

    .top-shell {{
        margin-bottom: 20px;
    }}

    .api-pill {{
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 8px;
        color: {muted};
        font-size: 14px;
        padding-top: 8px;
    }}

    .api-dot {{
        width: 10px;
        height: 10px;
        border-radius: 999px;
        background: #22c55e;
        display: inline-block;
    }}

    .api-dot.off {{
        background: #ef4444;
    }}

    .api-warning {{
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #991b1b;
        padding: 14px 16px;
        border-radius: 16px;
        margin-bottom: 18px;
    }}

    .hero-card,
    .page-card {{
        background: {card};
        border: 1px solid {border};
        border-radius: 28px;
        padding: 34px;
        box-shadow: none;
        margin-bottom: 24px;
    }}

    .hero-eyebrow,
    .page-kicker {{
        color: {muted};
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}

    .hero-card h1 {{
        font-size: 42px;
        line-height: 1.1;
        margin-bottom: 12px;
        color: {text};
    }}

    .hero-card p,
    .page-card p {{
        color: {muted};
        font-size: 16px;
    }}

    .page-card h2 {{
        font-size: 32px;
        color: {text};
    }}

    .chat-date {{
        text-align: center;
        color: {muted};
        font-size: 13px;
        margin: 16px 0;
    }}

    .msg-row {{
        display: flex;
        margin: 12px 0;
    }}

    .msg-row.user {{
        justify-content: flex-end;
    }}

    .msg-row.asst {{
        justify-content: flex-start;
    }}

    .asst-wrap {{
        display: flex;
        gap: 10px;
        align-items: flex-start;
        max-width: 78%;
    }}

    .assistant-dot {{
        width: 32px;
        height: 32px;
        background: #2563eb;
        color: white;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        flex-shrink: 0;
    }}

    .bubble {{
        padding: 13px 16px;
        border-radius: 18px;
        white-space: pre-wrap;
        line-height: 1.5;
        font-size: 15px;
    }}

    .bubble.user {{
        background: {user_bubble};
        color: white;
        max-width: 72%;
    }}

    .bubble.asst {{
        background: {assistant_bubble};
        color: {text};
        border: 1px solid {border};
    }}

    /* ========== CHAT INPUT: HILANGKAN BORDER/BACKGROUND/SHADOW ABU ========== */
    div[data-testid="stChatInput"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }}

    div[data-testid="stChatInput"] > div {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    div[data-testid="stChatInput"] textarea {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        color: {text} !important;
    }}

    div[data-testid="stChatInput"] textarea::placeholder {{
        color: {muted} !important;
    }}

    /* ========== AREA BAWAH CHAT ========== */
    .composer-bottom-wrap {{
        margin-top: 10px;
        margin-bottom: 8px;
    }}

    .stFileUploader {{
        margin-top: 0 !important;
    }}

    .stFileUploader section {{
        border-radius: 14px !important;
    }}

    .bottom-note {{
        position: fixed;
        bottom: 8px;
        left: 0;
        right: 0;
        text-align: center;
        color: {muted};
        font-size: 12px;
        pointer-events: none;
    }}
    </style>
    """