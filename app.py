import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
import re

# -----------------------------
# Configuration
# -----------------------------
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Functions
# -----------------------------
def extract_text_from_pdf(uploaded_file):
    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")

    response = model.generate_content(prompt)

    return response.text


# -----------------------------
# UI
# -----------------------------
st.title("📄 AI Resume Analyzer")
st.write("Analyze your resume using Gemini AI")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=200
)

# -----------------------------
# Resume Text Extraction
# -----------------------------
resume_text = ""

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3 = st.tabs(
    ["📊 Analysis", "🛠 Skills", "📈 Roadmap"]
)

# =====================================================
# TAB 1 - ANALYSIS
# =====================================================
with tab1:

    if st.button("🚀 Analyze Resume"):

        if uploaded_file and job_description:

            try:

                prompt = f"""
                Analyze the resume against the job description.

                Resume:
                {resume_text}

                Job Description:
                {job_description}

                Return EXACTLY:

                MATCH_SCORE: score out of 100

                ATS_SCORE: score out of 100

                STRENGTHS:
                - point 1
                - point 2

                MISSING_SKILLS:
                - skill 1
                - skill 2

                SUGGESTIONS:
                - suggestion 1
                - suggestion 2
                """

                result = get_gemini_response(prompt)

                match_score = re.search(
                    r"MATCH_SCORE:\s*(\d+)",
                    result
                )

                ats_score = re.search(
                    r"ATS_SCORE:\s*(\d+)",
                    result
                )

                col1, col2 = st.columns(2)

                with col1:
                    if match_score:
                        score = int(match_score.group(1))
                        st.metric(
                            "Resume Match Score",
                            f"{score}%"
                        )
                        st.progress(score)

                with col2:
                    if ats_score:
                        score = int(ats_score.group(1))
                        st.metric(
                            "ATS Score",
                            f"{score}%"
                        )
                        st.progress(score)

                st.markdown("---")

                st.subheader("📋 Detailed Analysis")
                st.write(result)

            except Exception as e:

                if "429" in str(e):
                    st.warning(
                        "Gemini rate limit reached. Wait a minute and try again."
                    )
                else:
                    st.error(str(e))

        else:
            st.warning(
                "Please upload resume and enter job description."
            )

# =====================================================
# TAB 2 - SKILLS
# =====================================================
with tab2:

    if st.button("🔍 Extract Skills"):

        if uploaded_file:

            try:

                prompt = f"""
                Extract all technical skills from this resume.

                Resume:
                {resume_text}

                Group them into:

                Programming Languages
                Frameworks
                Databases
                Cloud
                Tools
                Soft Skills
                """

                result = get_gemini_response(prompt)

                st.subheader("🛠 Extracted Skills")
                st.write(result)

            except Exception as e:

                if "429" in str(e):
                    st.warning(
                        "Gemini rate limit reached. Wait a minute and try again."
                    )
                else:
                    st.error(str(e))

        else:
            st.warning("Upload a resume first.")

# =====================================================
# TAB 3 - ROADMAP
# =====================================================
with tab3:

    if st.button("📈 Generate 30-Day Roadmap"):

        if uploaded_file and job_description:

            try:

                roadmap_prompt = f"""
                You are a career coach.

                Resume:
                {resume_text}

                Job Description:
                {job_description}

                Create a practical 30-day roadmap.

                Divide into:

                Week 1
                Week 2
                Week 3
                Week 4

                For each week provide:

                - Skills to learn
                - Projects to build
                - Resume improvements
                - Career advice

                Keep it beginner friendly.
                """

                result = get_gemini_response(
                    roadmap_prompt
                )

                st.subheader(
                    "📈 30-Day Improvement Roadmap"
                )

                st.write(result)

            except Exception as e:

                if "429" in str(e):
                    st.warning(
                        "Gemini rate limit reached. Wait a minute and try again."
                    )
                else:
                    st.error(str(e))

        else:
            st.warning(
                "Upload resume and enter job description."
            )