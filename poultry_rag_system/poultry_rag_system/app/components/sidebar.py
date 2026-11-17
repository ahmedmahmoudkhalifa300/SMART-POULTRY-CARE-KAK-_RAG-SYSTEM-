"""
PoultryCare AI — Sidebar Component
"""

import streamlit as st


def render_sidebar(current_page: str = "Dashboard") -> str:
    """
    Render the PoultryCare AI sidebar.
    
    Args:
        current_page: The currently active page name.
    
    Returns:
        The selected page name.
    """
    # Initialize page in session state if not present
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

    # Inject CSS
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a2847 0%, #131c2a 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.3) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        }

        [data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
            background-color: transparent !important;
        }

        [data-testid="stSidebar"] [data-testid="stSidebarNav"] {
            display: none !important;
        }

        .pc-sidebar-brand {
            text-align: center;
            padding: 8px 4px 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
        }

        .pc-sidebar-brand-title {
            color: #ffffff;
            font-size: 1.1rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.01em;
            line-height: 1.4;
        }

        .pc-sidebar-brand-subtitle {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.75rem;
            margin: 8px 0 0;
            font-weight: 400;
        }

        .pc-nav-item {
            display: flex;
            align-items: center;
            width: 100%;
            padding: 11px 16px;
            margin: 5px 0;
            border-radius: 10px;
            border: none;
            background: transparent;
            color: rgba(255, 255, 255, 0.75);
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            text-align: left;
        }

        .pc-nav-item:hover {
            background-color: rgba(255, 255, 255, 0.1);
            transform: translateX(4px);
            color: #ffffff;
        }

        .pc-nav-item.active {
            background-color: rgba(91, 143, 168, 0.2);
            color: #5b8fa8;
            font-weight: 600;
            border-radius: 0 10px 10px 0;
            border-left: 3px solid #5b8fa8;
        }

        .pc-nav-icon {
            margin-right: 12px;
            font-size: 1.15rem;
            width: 28px;
            text-align: center;
            flex-shrink: 0;
        }

        .sidebar-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.12), transparent);
            margin: 18px 0;
            border: none;
        }

        .status-title {
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 12px;
            padding: 0 4px;
        }

        .status-card {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 10px 14px;
            margin: 8px 0;
            display: flex;
            align-items: center;
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.06);
            transition: all 0.2s ease;
        }

        .status-card:hover {
            background-color: rgba(255, 255, 255, 0.08);
        }

        .status-indicator {
            margin-right: 10px;
            font-size: 0.85rem;
        }

        .stButton>button, [data-testid="stSidebar"] button[kind="secondary"] {
            background: transparent !important;
            border-radius: 10px !important;
            border: none !important;
            color: rgba(255, 255, 255, 0.75) !important;
            font-weight: 500 !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        .stButton>button:hover, [data-testid="stSidebar"] button[kind="secondary"]:hover {
            background-color: rgba(255, 255, 255, 0.1) !important;
            transform: translateX(4px);
            color: #ffffff !important;
        }

        .stButton>button[data-active="true"], [data-testid="stSidebar"] button[kind="primary"] {
            background-color: rgba(91, 143, 168, 0.2) !important;
            color: #5b8fa8 !important;
            font-weight: 600 !important;
            border-radius: 0 10px 10px 0 !important;
            border-left: 3px solid #5b8fa8 !important;
        }

        .stButton>button[data-active="true"]:hover, [data-testid="stSidebar"] button[kind="primary"]:hover {
            background-color: rgba(91, 143, 168, 0.3) !important;
            transform: translateX(4px);
            color: #5b8fa8 !important;
        }

        .stButton>button span {
            font-family: 'Inter', sans-serif !important;
        }

        [data-testid="stSidebar"] [data-testid="stVerticalBlock"]::-webkit-scrollbar {
            width: 4px;
        }

        [data-testid="stSidebar"] [data-testid="stVerticalBlock"]::-webkit-scrollbar-track {
            background: transparent;
        }

        [data-testid="stSidebar"] [data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 4px;
        }

        @media (max-width: 768px) {
            [data-testid="stSidebar"] {
                width: 100% !important;
                min-width: 100% !important;
                max-width: 100% !important;
                height: auto !important;
                position: relative !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        # Brand
        st.markdown(
            """
            <div class="pc-sidebar-brand">
                <div class="pc-sidebar-brand-title">🐔 PoultryCare AI</div>
                <div class="pc-sidebar-brand-subtitle">AI-Powered Poultry Health Assistant</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        # Navigation items
        pages = [
            ("🏠", "Dashboard"),
            ("💬", "AI Assistant"),
            ("📷", "Image Analysis"),
            ("📚", "Disease Library"),
            ("🐔", "Farm Health"),
            ("🚨", "Alerts"),
            ("──────────────", "divider"),
            ("⚙️", "Settings"),
            ("ℹ️", "About"),
        ]

        for icon, page in pages:
            if page == "divider":
                st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
                continue

            is_active = st.session_state.current_page == page
            button_key = f"nav_{page.lower().replace(' ', '_')}"

            if st.button(
                f"{icon} {page}",
                key=button_key,
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.current_page = page
                st.rerun()

        # Spacer
        st.markdown("<br>", unsafe_allow_html=True)

        # System Status
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        st.markdown('<div class="status-title">System Status</div>', unsafe_allow_html=True)

        for indicator, text in [
            ("🟢", "System Online"),
            ("📚", "Knowledge Base Ready"),
            ("🤖", "AI Ready"),
        ]:
            st.markdown(
                f"""
                <div class="status-card">
                    <span class="status-indicator">{indicator}</span>
                    <span>{text}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    return st.session_state.current_page
