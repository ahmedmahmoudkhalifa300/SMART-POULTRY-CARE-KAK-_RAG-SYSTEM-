"""
PoultryCare AI — Image Analysis Page
"""

import requests
import streamlit as st

from app.components.header import render_header


def render_image_analysis() -> None:
    """Render the Image Analysis page."""
    render_header(
        title="Image Analysis",
        subtitle="Upload a poultry image for AI-assisted diagnosis",
    )

    # Initialize session state for results
    if "image_result" not in st.session_state:
        st.session_state.image_result = None

    # Upload section
    st.markdown(
        """
        <div style="
            background: #131c2a;
            border: 2px dashed rgba(255, 255, 255, 0.1);
            border-radius: 14px;
            padding: 40px;
            text-align: center;
            margin-bottom: 24px;
        ">
            <div style="font-size: 3rem; margin-bottom: 12px;">📷</div>
            <h3 style="font-size: 1.1rem; font-weight: 600; color: #f0f4f8; margin-bottom: 4px;">
                Upload Poultry Image
            </h3>
            <p style="font-size: 0.875rem; color: #7e8f9a;">
                Drag and drop or click to browse<br>
                <span style="font-size: 0.75rem;">JPG, PNG up to 10MB</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        # Preview
        st.image(uploaded_file, caption="Uploaded image", width=300)

        # Analyze button
        if st.button("🔬 Analyze Image", type="primary", use_container_width=True):
            with st.spinner("Analyzing image..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    resp = requests.post(
                        "http://127.0.0.1:8001/image/diagnose",
                        files=files,
                        timeout=120,
                    )
                    resp.raise_for_status()
                    st.session_state.image_result = resp.json()
                    st.rerun()
                except requests.RequestException as exc:
                    st.error(f"Unable to reach the backend: {exc}")

    # Results
    if st.session_state.image_result:
        result = st.session_state.image_result

        st.markdown(
            """
            <div style="margin-top: 32px;">
                <h2 style="font-size: 1.25rem; font-weight: 600; color: #f0f4f8; margin-bottom: 16px;">
                    Analysis Result
                </h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Disease prediction
        disease = result.get("disease", "Unknown")
        confidence = result.get("confidence", 0)
        confidence_pct = confidence * 100

        st.metric(
            label="Predicted Condition",
            value=disease,
            delta=f"{confidence_pct:.0f}% confidence",
        )

        # Explanation
        if result.get("explanation"):
            st.markdown(
                f"""
                <div class="pc-answer-card" style="margin-top: 16px;">
                    <div class="pc-answer-card-header">
                        <div class="pc-answer-card-avatar">🔬</div>
                        <div class="pc-answer-card-title">Detailed Analysis</div>
                    </div>
                    <div class="pc-answer-card-body">
                        {result["explanation"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # All probabilities
        if result.get("all_probabilities"):
            with st.expander("📊 All Probabilities"):
                for disease_name, prob in result["all_probabilities"].items():
                    st.progress(prob, text=f"{disease_name}: {prob:.1%}")

        # Sources
        if result.get("sources"):
            with st.expander("📚 Sources"):
                for source in result["sources"]:
                    metadata = source.get("metadata", {})
                    source_name = metadata.get("source", "Unknown")
                    page = metadata.get("page", "?")
                    st.write(f"▸ {source_name} (page {page})")

        # Actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📚 Learn More", use_container_width=True):
                st.session_state.selected_disease = disease
                st.session_state.current_page = "Disease Library"
                st.rerun()
        with col2:
            if st.button("💬 Ask AI About This Result", use_container_width=True):
                st.session_state.quick_access_query = f"What is {disease} in poultry?"
                st.session_state.current_page = "AI Assistant"
                st.rerun()

        # Clear result
        if st.button("Clear Result", use_container_width=True):
            st.session_state.image_result = None
            st.rerun()
