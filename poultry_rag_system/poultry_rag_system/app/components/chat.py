"""
PoultryCare AI — Chat Components
"""

import streamlit as st


def render_chat_message(role: str, content: str) -> None:
    """
    Render a single chat message.
    
    Args:
        role: "user" or "assistant"
        content: Message content (supports markdown)
    """
    with st.chat_message(role):
        if role == "user":
            st.markdown(content)
        else:
            st.markdown(content)


def render_answer_card(
    answer: str,
    sources: list[dict] | None = None,
    feedback_enabled: bool = True,
    key_prefix: str = "",
) -> None:
    """
    Render a professional AI answer card with optional sources and feedback.
    
    Args:
        answer: The AI-generated answer text.
        sources: Optional list of source documents.
        feedback_enabled: Whether to show feedback buttons.
        key_prefix: Prefix for widget keys to avoid collisions.
    """
    st.markdown(
        """
        <style>
        .pc-answer-card {
            background: #131c2a;
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 14px;
            padding: 20px;
            margin: 12px 0;
        }

        .pc-answer-card-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 14px;
            padding-bottom: 14px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.07);
        }

        .pc-answer-card-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #5b8fa8 0%, #7eb8d4 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            flex-shrink: 0;
        }

        .pc-answer-card-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: #f0f4f8;
        }

        .pc-answer-card-body {
            font-size: 1.1rem;
            color: #ffffff;
            line-height: 1.7;
        }

        .pc-sources {
            margin-top: 14px;
            padding-top: 14px;
            border-top: 1px solid rgba(255, 255, 255, 0.07);
        }

        .pc-sources-title {
            font-size: 0.8rem;
            font-weight: 600;
            color: #7e8f9a;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .pc-source-item {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 4px 0;
            font-size: 0.8rem;
            color: #b0bec5;
        }

        .pc-source-icon {
            color: #5b8fa8;
            font-size: 0.7rem;
        }

        .pc-feedback {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 14px;
            padding-top: 14px;
            border-top: 1px solid rgba(255, 255, 255, 0.07);
        }

        .pc-feedback-label {
            font-size: 0.8rem;
            color: #7e8f9a;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Answer card
    st.markdown(
        """
        <div class="pc-answer-card">
            <div class="pc-answer-card-header">
                <div class="pc-answer-card-avatar">🐔</div>
                <div class="pc-answer-card-title">PoultryCare AI</div>
            </div>
            <div class="pc-answer-card-body">
        """,
        unsafe_allow_html=True,
    )

    st.markdown(answer)

    st.markdown("</div>", unsafe_allow_html=True)

    # Sources
    if False and sources: # Hiding sources as requested
        st.markdown('<div class="pc-sources">', unsafe_allow_html=True)
        st.markdown('<div class="pc-sources-title">📚 Sources</div>', unsafe_allow_html=True)

        for source in sources[:3]:
            metadata = source.get("metadata", {})
            source_name = metadata.get("source", "Unknown")
            page = metadata.get("page", "?")
            st.markdown(
                f"""
                <div class="pc-source-item">
                    <span class="pc-source-icon">▸</span>
                    <span>{source_name} (page {page})</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # Feedback
    if feedback_enabled:
        st.markdown(
            """
            <div class="pc-feedback">
                <span class="pc-feedback-label">Was this answer helpful?</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Yes", key=f"{key_prefix}_feedback_yes", use_container_width=True):
                st.toast("Thank you for your feedback!", icon="✅")
        with col2:
            if st.button("👎 No", key=f"{key_prefix}_feedback_no", use_container_width=True):
                st.toast("Thank you for your feedback!", icon="📝")


def render_suggested_questions(questions: list[str], key_prefix: str = "") -> None:
    """
    Render suggested question chips.
    
    Args:
        questions: List of suggested question strings.
        key_prefix: Prefix for widget keys.
    """
    st.markdown(
        """
        <style>
        .pc-suggested-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin: 16px 0;
        }

        .pc-suggested-chip {
            background: #131c2a;
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 10px;
            padding: 12px 16px;
            font-size: 0.85rem;
            color: #b0bec5;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
        }

        .pc-suggested-chip:hover {
            border-color: #5b8fa8;
            color: #f0f4f8;
            background: rgba(91, 143, 168, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="pc-suggested-grid">', unsafe_allow_html=True)

    for i, question in enumerate(questions):
        if st.button(
            question,
            key=f"{key_prefix}_suggested_{i}",
            use_container_width=True,
        ):
            st.session_state[f"{key_prefix}_selected_question"] = question
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
