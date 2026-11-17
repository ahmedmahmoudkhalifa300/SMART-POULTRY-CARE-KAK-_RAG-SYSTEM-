"""
PoultryCare AI — AI Assistant Page
"""

import uuid

import requests
import streamlit as st

from app.components.chat import render_answer_card, render_chat_message, render_suggested_questions
from app.components.header import render_header

API_BASE_URL = "http://localhost:8001"


def render_assistant() -> None:
    """Render the AI Assistant page."""
    render_header(
        title="AI Assistant",
        subtitle="Ask questions about poultry diseases and health",
    )

    # Initialize session state
    if "chat_session_id" not in st.session_state:
        st.session_state.chat_session_id = str(uuid.uuid4())
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Check if user came from quick access
    if "quick_access_query" in st.session_state and st.session_state.quick_access_query:
        query = st.session_state.quick_access_query
        st.session_state.quick_access_query = None
        _process_question(query)
        st.rerun()

    # Show suggested questions if no history
    if not st.session_state.chat_history:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 24px;">
                <h3 style="font-size: 1.1rem; font-weight: 600; color: #f0f4f8; margin-bottom: 4px;">
                    إيه المشكلة اللي بتواجهها في القطيع؟
                </h3>
                <p style="font-size: 0.875rem; color: #7e8f9a;">
                    Choose a topic or type your question below
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        suggested = [
            "🫁 مشاكل التنفس عند الدواجن",
            "💩 إسهال ومشاكل هضمية",
            "🥚 انخفاض إنتاج البيض",
            "🌡️ أعراض عامة للمرض",
            "🦠 الأمراض الفيروسية الشائعة",
            "🛡️ طرق الوقاية من الأمراض",
        ]

        render_suggested_questions(suggested, key_prefix="main")

        # Handle suggested question selection
        if f"main_selected_question" in st.session_state and st.session_state[f"main_selected_question"]:
            question = st.session_state[f"main_selected_question"]
            del st.session_state[f"main_selected_question"]
            _process_question(question)
            st.rerun()

    # Chat history
    for i, turn in enumerate(st.session_state.chat_history):
        render_chat_message("user", turn["question"])
        render_answer_card(
            turn["answer"],
            turn.get("sources", []),
            feedback_enabled=True,
            key_prefix=f"chat_{i}",
        )

    # Chat input
    if prompt := st.chat_input("Ask about poultry diseases..."):
        _process_question(prompt)
        st.rerun()


def _process_question(question: str) -> None:
    """Process a user question and add to history."""
    st.session_state.chat_history.append({
        "role": "user",
        "question": question,
        "answer": "",
        "sources": [],
    })

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the knowledge base..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/chat/",
                    json={
                        "question": question,
                        "session_id": st.session_state.chat_session_id,
                    },
                    timeout=120,
                )
                response.raise_for_status()
                data = response.json()
                answer = data["answer"]
                sources = data.get("sources", [])

                render_answer_card(
                    answer,
                    sources,
                    feedback_enabled=True,
                    key_prefix=f"chat_{len(st.session_state.chat_history) - 1}",
                )

                st.session_state.chat_history[-1]["answer"] = answer
                st.session_state.chat_history[-1]["sources"] = sources

            except requests.RequestException as exc:
                st.error(f"Unable to reach the backend: {exc}")
                st.session_state.chat_history[-1]["answer"] = f"Error: {exc}"
