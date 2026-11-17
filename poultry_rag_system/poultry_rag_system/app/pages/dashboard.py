"""
PoultryCare AI — Dashboard Page
"""

import streamlit as st

from app.components.header import render_header
from app.components.chat import render_suggested_questions


def render_dashboard() -> None:
    """Render the PoultryCare AI Dashboard."""
    render_header(
        title="PoultryCare AI",
        subtitle="AI-Powered Poultry Health Assistant",
    )

    st.markdown(
        """
        <style>
        .pc-hero-video-wrapper {
            position: relative;
            width: 100%;
            height: 520px;
            overflow: hidden;
            border-radius: 18px;
            margin-bottom: 24px;
            background: #1a2847;
        }

        .pc-hero-video-wrapper video {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.9;
        }

        .pc-hero-overlay {
            position: absolute;
            inset: 0;
            background:
                linear-gradient(180deg, rgba(26,40,71,0.2) 0%, rgba(26,40,71,0.55) 50%, rgba(26,40,71,0.85) 100%),
                linear-gradient(90deg, rgba(26,40,71,0.4) 0%, transparent 40%, rgba(26,40,71,0.4) 100%);
            pointer-events: none;
            z-index: 1;
        }

        .pc-hero-content {
            position: relative;
            z-index: 2;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 48px 24px;
        }

        .pc-hero-title {
            font-size: 3rem;
            font-weight: 800;
            color: #f0f4f8;
            margin-bottom: 16px;
            line-height: 1.15;
            text-shadow: 0 2px 16px rgba(0,0,0,0.6);
            max-width: 800px;
        }

        .pc-hero-subtitle {
            font-size: 1.25rem;
            color: rgba(220, 228, 234, 0.9);
            margin-bottom: 32px;
            text-shadow: 0 1px 10px rgba(0,0,0,0.5);
            max-width: 600px;
        }

        .pc-hero-actions {
            display: flex;
            gap: 16px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .pc-hero-actions .stButton > button {
            background: #5b8fa8;
            color: #f0f4f8;
            border: none;
            padding: 14px 28px;
            border-radius: 12px;
            font-weight: 700;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.25s ease;
            box-shadow: 0 4px 20px rgba(91, 143, 168, 0.4);
        }

        .pc-hero-actions .stButton > button:hover {
            background: #4a7a95;
            transform: translateY(-2px);
            box-shadow: 0 6px 24px rgba(91, 143, 168, 0.5);
        }

        .pc-hero-actions .stButton:nth-child(2) > button {
            background: rgba(255,255,255,0.06);
            color: #f0f4f8;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: none;
        }

        .pc-hero-actions .stButton:nth-child(2) > button:hover {
            background: rgba(255,255,255,0.12);
            border-color: rgba(255,255,255,0.35);
            transform: translateY(-2px);
        }

        @media (max-width: 768px) {
            .pc-hero-video-wrapper {
                height: 420px;
            }
            .pc-hero-title {
                font-size: 2rem;
            }
            .pc-hero-subtitle {
                font-size: 1rem;
            }
            .pc-hero-actions {
                flex-direction: column;
                width: 100%;
                padding: 0 24px;
            }
            .pc-hero-actions .stButton > button {
                width: 100% !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="pc-hero-video-wrapper">
            <video autoplay muted loop playsinline>
                <source src="/static/hero.mp4" type="video/mp4">
            </video>
            <div class="pc-hero-overlay"></div>
            <div class="pc-hero-content">
                <div class="pc-hero-title">Your Intelligent Assistant for Healthier Flocks</div>
                <div class="pc-hero-subtitle">افهم مشاكل القطيع ووصل للمعلومة المناسبة بسرعة.</div>
                <div class="pc-hero-actions">
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💬 Ask AI", key="hero_ask_ai", use_container_width=True):
            st.session_state.current_page = "AI Assistant"
            st.rerun()
    with col2:
        if st.button("📷 Analyze Image", key="hero_analyze", use_container_width=True):
            st.session_state.current_page = "Image Analysis"
            st.rerun()

    st.markdown(
        """
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick Access Section
    st.markdown(
        """
        <div style="margin-top: 32px; margin-bottom: 16px;">
            <h2 style="font-size: 1.25rem; font-weight: 600; color: #f0f4f8; margin-bottom: 4px;">
                What can I help with?
            </h2>
            <p style="font-size: 0.875rem; color: #8899a6;">
                Select a topic to get started with AI-assisted information
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick access cards
    quick_access = [
        ("🫁", "Respiratory Problems", "respiratory problems breathing issues in poultry"),
        ("💩", "Digestive Problems", "digestive issues diarrhea in chickens"),
        ("🥚", "Egg Production", "egg production problems layers"),
        ("🦠", "Diseases", "poultry diseases identification"),
        ("🌡️", "Symptoms", "general symptoms sick birds"),
        ("🛡️", "Prevention", "disease prevention biosecurity"),
    ]

    cols = st.columns(3)
    for i, (icon, title, query) in enumerate(quick_access):
        with cols[i % 3]:
            if st.button(
                f"{icon} {title}",
                key=f"quick_access_{i}",
                use_container_width=True,
            ):
                st.session_state.quick_access_query = query
                st.session_state.current_page = "AI Assistant"
                st.rerun()

    # Why PoultryCare AI
    st.markdown(
        """
        <div style="margin-top: 48px; margin-bottom: 16px;">
            <h2 style="font-size: 1.25rem; font-weight: 600; color: #f0f4f8; margin-bottom: 4px;">
                Why PoultryCare AI?
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    features = [
        ("⚡", "Fast Information", "Get instant answers about poultry health, diseases, and management practices."),
        ("📚", "Knowledge-Based Answers", "All responses are grounded in verified veterinary knowledge bases."),
        ("🛡️", "Prevention & Decision Support", "Make informed decisions about disease prevention and flock management."),
    ]

    feature_cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with feature_cols[i]:
            st.markdown(
                f"""
                <div class="pc-feature-card">
                    <div class="pc-feature-card-icon">{icon}</div>
                    <div class="pc-feature-card-title">{title}</div>
                    <div class="pc-feature-card-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Trust Notice
    st.markdown(
        """
        <div style="
            margin-top: 32px;
            padding: 16px;
            background: rgba(91, 143, 168, 0.1);
            border: 1px solid rgba(91, 143, 168, 0.2);
            border-radius: 10px;
            text-align: center;
        ">
            <p style="font-size: 0.8rem; color: #8899a6; margin: 0;">
                ⚠️ AI-generated information is intended for educational and decision-support purposes 
                and does not replace professional veterinary diagnosis.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
