"""Streamlit Web UI for the AI Development Team."""

import os
import re
import time
import shutil
import streamlit as st
from dotenv import load_dotenv
from orchestrator import TeamOrchestrator

# Load environment variables early (useful for local)
load_dotenv()

st.set_page_config(page_title="AI Software Team", page_icon="🤖", layout="centered")

# Custom CSS for a centered, modern card UI
st.markdown("""
<style>
    .main {
        background-color: #f0f2f5;
    }
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    h1 {
        color: navy;
        text-align: center;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    /* Simple Card Styling */
    .css-1r6slb0, .css-12oz5g7 {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🤖 Automated Software Development Team</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Provide your requirements below, and our AI team (Product Manager, Architect, Developer, QA, DevOps) will generate the full project for you!</p>", unsafe_allow_html=True)

with st.form("project_form"):
    project_name = st.text_input("Project Name (Folder) *", placeholder="Example: blog-api")
    
    language = st.selectbox(
        "Programming Language / Framework *",
        ["", "Python / FastAPI", "Python / Django", "Python / Flask", "Node.js / Express", "React / Next.js", "Go", "Java / Spring Boot", "Other (Type it in)"]
    )
    
    requirement = st.text_area(
        "What would you like to build? (Requirement) *",
        placeholder="Example: A REST API for a blog with user authentication...",
        height=150
    )
    
    submit_button = st.form_submit_button("🚀 Generate Project", type="primary", use_container_width=True)

if submit_button:
    # Validation
    if not requirement or not requirement.strip():
        st.error("Requirement cannot be empty! Please describe what you want to build.")
        st.stop()
        
    project_name = project_name.strip() if project_name else ""
    if not project_name:
        st.error("Project Name is required!")
        st.stop()
        
    language = language.strip() if language else ""
    if not language:
        st.error("Please select a specific Programming Language / Framework.")
        st.stop()
        
    # Check for API Key in Streamlit Secrets, then Environment Variable
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except FileNotFoundError:
        api_key = None
        
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
        
    if not api_key:
        st.error("OPENAI_API_KEY is not set! Please set it in Streamlit Secrets or your .env file.")
        st.stop()
        
    # Set the key in env so CrewAI can find it
    os.environ["OPENAI_API_KEY"] = api_key
        
    folder_name = "".join([c if c.isalnum() or c in ['-', '_'] else '_' for c in project_name])
    
    st.info(f"🚀 Initializing AI Development Team for project: **{folder_name}**...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    log_area = st.empty()
    
    try:
        orchestrator = TeamOrchestrator(recipient_email=None, project_name=folder_name)
        
        full_log = ""
        current_progress = 0.0
        
        for update in orchestrator.run_with_progress(requirement, language):
            full_log += update + "\\n"
            log_area.code(full_log, language="bash")
            
            # Update progress bar based on phase
            if "Product Manager analyzing" in update:
                current_progress = 0.1
                status_text.text("📋 Product Manager analyzing requirements...")
            elif "Architect designing" in update:
                current_progress = 0.4
                status_text.text("🏗️ Architect designing system...")
            elif "Architect completed" in update:
                current_progress = 0.5
                status_text.text("✅ Architect completed")
            elif "Developer writing" in update:
                current_progress = 0.6
                status_text.text("💻 Developer writing code...")
            elif "Developer completed" in update:
                current_progress = 0.7
                status_text.text("✅ Developer completed")
            elif "QA Tester validating" in update:
                current_progress = 0.8
                status_text.text("🧪 QA Tester validating...")
            elif "QA completed" in update:
                current_progress = 0.85
                status_text.text("✅ QA Tester completed")
            elif "DevOps setting up" in update:
                current_progress = 0.9
                status_text.text("🚀 DevOps setting up deployment...")
            elif "DevOps completed" in update:
                current_progress = 0.95
                status_text.text("✅ DevOps completed")
            
            progress_bar.progress(current_progress)
            
        progress_bar.progress(1.0)
        status_text.success("✅ Project Complete!")
        
        zip_path = orchestrator.get_zip_path()
        
        if zip_path and os.path.exists(zip_path):
            with open(zip_path, "rb") as fp:
                st.download_button(
                    label="🎁 Download Generated Project (Zip)",
                    data=fp,
                    file_name=os.path.basename(zip_path),
                    mime="application/zip",
                    type="primary",
                    use_container_width=True
                )
        else:
            st.error("Zip file was not created successfully.")
            
    except Exception as e:
        st.error(f"Workflow failed: {str(e)}")
