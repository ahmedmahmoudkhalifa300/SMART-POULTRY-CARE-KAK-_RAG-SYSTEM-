"""
PoultryCare AI — Main Application Entry Point

This is the main Streamlit application that ties together all pages and components.
"""

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

CSS_PATH = PROJECT_ROOT / "app" / "styles" / "main.css"
if CSS_PATH.exists():
    st.markdown(f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

from app.components.header import render_header
from app.components.sidebar import render_sidebar
from app.pages.dashboard import render_dashboard
from app.pages.assistant import render_assistant
from app.pages.image_analysis import render_image_analysis
from app.pages.disease_library import render_disease_library

# Page configuration
st.set_page_config(
    page_title="PoultryCare AI",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Render sidebar and get current page
current_page = render_sidebar()

# Route to pages
if current_page == "Dashboard":
    render_dashboard()
elif current_page == "AI Assistant":
    render_assistant()
elif current_page == "Image Analysis":
    render_image_analysis()
elif current_page == "Disease Library":
    render_disease_library()
elif current_page == "Farm Health":
    st.header("🐔 Farm Health")
    st.info("Farm Health monitoring coming soon. Connect your farm data to enable intelligent health tracking.")
elif current_page == "Alerts":
    st.header("🚨 Alerts")
    st.info("No active alerts. Connect farm data to enable intelligent alerts.")
elif current_page == "Settings":
    st.header("⚙️ Settings")
    st.info("Settings page coming soon.")
elif current_page == "About":
    st.header("ℹ️ About")
    st.markdown(
        """
        <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #f0f4f8; margin-bottom: 16px;">About PoultryCare AI</h2>
            <p style="color: #b0bec5; line-height: 1.7; margin-bottom: 16px;">
                PoultryCare AI is an intelligent poultry health assistant that helps farmers 
                understand problems in their flock, access reliable poultry health information, 
                analyze poultry images, and make better-informed decisions.
            </p>
            <h3 style="color: #f0f4f8; margin-bottom: 12px;">Current Capabilities</h3>
            <ul style="color: #b0bec5; line-height: 1.7; margin-bottom: 16px;">
                <li>Poultry Q&A powered by RAG technology</li>
                <li>Knowledge retrieval from veterinary documents</li>
                <li>Image analysis for disease identification</li>
                <li>Disease information library</li>
            </ul>
            <h3 style="color: #f0f4f8; margin-bottom: 12px;">Future Capabilities</h3>
            <ul style="color: #b0bec5; line-height: 1.7; margin-bottom: 16px;">
                <li>Farm monitoring and analytics</li>
                <li>Intelligent alerts and notifications</li>
                <li>IoT sensor integration</li>
                <li>Farm analytics dashboard</li>
            </ul>
            <div style="
                margin-top: 32px;
                padding: 16px;
                background: rgba(91, 143, 168, 0.1);
                border: 1px solid rgba(91, 143, 168, 0.2);
                border-radius: 10px;
                text-align: center;
            ">
                <p style="font-size: 0.8rem; color: #7e8f9a; margin: 0;">
                    ⚠️ This system provides informational support and does not replace 
                    professional veterinary diagnosis.
                </p>
                <p style="font-size: 0.75rem; color: #7e8f9a; margin-top: 8px;">
                    © 2026 PoultryCare AI. All rights reserved.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.header(f"Page: {current_page}")
    st.info("This page is under construction.")

# Footer
st.markdown(
    """
    <div style="
        text-align: center;
        padding: 24px;
        color: #7e8f9a;
        font-size: 0.8rem;
        border-top: 1px solid rgba(255, 255, 255, 0.07);
        margin-top: 48px;
    ">
        🐔 PoultryCare AI — AI-powered poultry health information and decision-support assistant.
    </div>
    """,
    unsafe_allow_html=True,
)
