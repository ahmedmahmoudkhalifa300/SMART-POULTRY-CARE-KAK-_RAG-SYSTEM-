"""
PoultryCare AI — Header Component
"""

import streamlit as st


def render_header(title: str = "PoultryCare AI", subtitle: str = "AI-Powered Poultry Health Assistant") -> None:
    """
    Render the PoultryCare AI header.
    
    Args:
        title: Main title text.
        subtitle: Subtitle text.
    """
    st.markdown(
        """
        <style>
        .pc-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 24px;
            background: #131c2a;
            border-bottom: 1px solid rgba(255, 255, 255, 0.07);
            position: sticky;
            top: 0;
            z-index: 200;
            margin-bottom: 24px;
        }

        .pc-header-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .pc-header-logo {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #5b8fa8 0%, #7eb8d4 100%);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            flex-shrink: 0;
        }

        .pc-header-text {
            display: flex;
            flex-direction: column;
        }

        .pc-header-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #f0f4f8;
            line-height: 1.2;
        }

        .pc-header-subtitle {
            font-size: 0.75rem;
            color: #7e8f9a;
            font-weight: 400;
        }

        .pc-header-status {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .pc-status-badge {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            background: rgba(91, 143, 168, 0.15);
            border-radius: 9999px;
            font-size: 0.75rem;
            color: #5b8fa8;
            font-weight: 500;
        }

        .pc-status-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: #5b8fa8;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="pc-header">
            <div class="pc-header-brand">
                <div class="pc-header-logo">🐔</div>
                <div class="pc-header-text">
                    <div class="pc-header-title">{title}</div>
                    <div class="pc-header-subtitle">{subtitle}</div>
                </div>
            </div>
            <div class="pc-header-status">
                <div class="pc-status-badge">
                    <span class="pc-status-dot"></span>
                    System Online
                </div>
                <div class="pc-status-badge">
                    📚 Knowledge Ready
                </div>
                <div class="pc-status-badge">
                    🤖 AI Ready
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
