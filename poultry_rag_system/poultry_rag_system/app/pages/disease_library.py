"""
PoultryCare AI — Disease Library Page
"""

import streamlit as st

from app.components.header import render_header


def render_disease_library() -> None:
    """Render the Disease Library page."""
    render_header(
        title="Disease Library",
        subtitle="Explore poultry diseases and health conditions",
    )

    # Search
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <h3 style="font-size: 1.1rem; font-weight: 600; color: #f0f4f8; margin-bottom: 12px;">
                Search Diseases
            </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    search_query = st.text_input(
        "Search diseases...",
        placeholder="Type disease name, symptom, or keyword...",
        label_visibility="collapsed",
    )

    # Categories
    st.markdown(
        """
        <div style="margin-top: 24px; margin-bottom: 12px;">
            <h3 style="font-size: 1rem; font-weight: 600; color: #f0f4f8; margin-bottom: 12px;">
                Categories
            </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    categories = [
        ("🫁", "Respiratory Diseases", "respiratory breathing lungs"),
        ("🦠", "Viral Diseases", "viral virus infections"),
        ("🧫", "Bacterial Diseases", "bacterial bacterial infections"),
        ("💩", "Digestive Diseases", "digestive stomach intestines"),
        ("🪱", "Parasitic Diseases", "parasites worms external internal"),
        ("🥚", "Egg Production Problems", "egg production layers"),
    ]

    cols = st.columns(3)
    for i, (icon, title, _) in enumerate(categories):
        with cols[i % 3]:
            if st.button(
                f"{icon} {title}",
                key=f"category_{i}",
                use_container_width=True,
            ):
                st.session_state.disease_category = title
                st.rerun()

    # Disease details (if selected)
    if "selected_disease" in st.session_state and st.session_state.selected_disease:
        disease = st.session_state.selected_disease
        st.markdown(
            f"""
            <div style="margin-top: 32px;">
                <h2 style="font-size: 1.5rem; font-weight: 700; color: #f0f4f8; margin-bottom: 16px;">
                    {disease}
                </h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Disease info sections
        sections = [
            ("📋", "Overview", "General information about the disease..."),
            ("🔍", "Symptoms", "Common symptoms to watch for..."),
            ("🦠", "Causes", "What causes this disease..."),
            ("📤", "Transmission", "How the disease spreads..."),
            ("⚠️", "Risk Factors", "Factors that increase risk..."),
            ("🛡️", "Prevention", "How to prevent this disease..."),
            ("💊", "Management", "Treatment and management..."),
        ]

        for icon, title, _ in sections:
            with st.expander(f"{icon} {title}"):
                st.info(f"{title} information would be loaded from the knowledge base here.")

        # Ask AI about this disease
        st.markdown(
            """
            <div style="margin-top: 16px;">
                <button class="stButton" style="
                    background: #5b8fa8;
                    color: #f0f4f8;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 10px;
                    font-weight: 600;
                    cursor: pointer;
                    width: 100%;
                " onclick="document.getElementById('nav_ai_assistant').click()">
                    💬 Ask AI About This Disease
                </button>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("← Back to Library", use_container_width=True):
            del st.session_state.selected_disease
            st.rerun()
