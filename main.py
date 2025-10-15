import streamlit as st
import json
from Loading import load_pdf, OPEN_ROUTER_API_Key
from Prompts import *

from langchain_openai import ChatOpenAI

# -------------  Initialize Model -----------------------
llm = ChatOpenAI(
    model="google/gemma-3n-e4b-it:free",
    temperature=0,
    openai_api_key=OPEN_ROUTER_API_Key,
    openai_api_base="https://openrouter.ai/api/v1"
)

# ---------- Helper Functions ( Chains creation ) ----------

def handle_CVs(cv_files):
    formating_chain = cv_formatting_prompt | llm
    candidates = []

    for file in cv_files:
        try:
            st.info(f"📄 Processing CV: {file.name} ...")
            with open(file.name, "wb") as f:
                f.write(file.getbuffer())
            cv_text = load_pdf(file.name)
            response = formating_chain.invoke({"cv_text": cv_text})
            candidates.append(response.content)
            st.success(f"✅ Done: {file.name}")
        except Exception as e:
            st.error(f"❌ Error processing {file.name}: {e}")
    return candidates


def handle_JD(jd_file):
    job_description_chain = jd_formatting_prompt | llm
    try:
        st.info(f"📋 Processing Job Description: {jd_file.name} ...")
        with open(jd_file.name, "wb") as f:
            f.write(jd_file.getbuffer())
        jd_text = load_pdf(jd_file.name)
        response = job_description_chain.invoke({"jd_text": jd_text})
        st.success("✅ Job description processed successfully!")
        return response.content
    except Exception as e:
        st.error(f"❌ Error processing job description: {e}")


def evaluate_candidates(job_description, candidates):
    compare_chain = comparison_prompt | llm
    response = compare_chain.invoke({
        "job_description": job_description,
        "candidates": candidates
    })
    return response.content

# ------------------ Streamlit UI --------------------------

st.set_page_config(page_title="Job Recommendation System", layout="wide")

# Inject CSS
st.markdown("""
    <style>
        /* Import Merriweather font */
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&display=swap');

        /* Base styling */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], 
        [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            font-family: 'Merriweather', serif !important;
        }
        [data-testid="stAppViewContainer"] {
            margin-top: -30px;
        }

        .main {
            background-color: #ffffff;
            font-family: 'Merriweather', sans-serif !important;
        }

        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 2rem;
            max-width: 1100px;
            margin: auto;
        }

        /* Titles */
        h1, h2, h3, h4, h5, h6 {
            color: #0a1e3f !important;
            font-weight: 700;
            font-family: 'Merriweather', serif !important;
        }

        /* Keep uploader area text white */
        [data-testid="stFileUploader"] div[role="button"] p,
        [data-testid="stFileUploader"] div[role="button"] span {
            color: #ffffff !important;
        }

        /* Uploaded file name (after file is uploaded) */
        [data-testid="stFileUploader"] div[role="alert"],
        [data-testid="stFileUploader"] ul li,
        [data-testid="stFileUploader"] ul li span,
        [data-testid="stFileUploader"] ul li div {
            color: #1b263b !important;
            font-weight: 600 !important;
        }


        /* Markdown / table text */
        [data-testid="stMarkdownContainer"], table, td, tr {
            color: #1b263b !important;
        }

        /* Markdown tables */
        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 10px;
        }
        th, td {
            border: 1px solid #d1d5db;
            text-align: left;
            padding: 8px;
        }
        th {
            background-color: #0a1e3f;
            color: white;
        }

        /* Align button inside the right column to the right */
        div[data-testid="stVerticalBlock"] > div.stButton { 
            display:flex;
            justify-content:flex-end;
        }

        /* Buttons */
        div.stButton > button:first-child {
            background-color: #bee00e !important;
            color: #0a1e3f !important;
            border-radius: 10px;
            font-weight: 700 !important;
            font-family: 'Merriweather', serif !important;
            transition: 0.3s ease;
            border: none;
            padding: 0.8rem;
        }

        div.stButton > button:first-child:hover {
            background-color: #d2ef3a !important;
            transform: scale(1.05);
        }

        /* JSON boxes */
        .stJson {
            border-radius: 12px;
            background-color: #f8f9fa;
            padding: 1em;
        }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(
        """
        <h1 style='font-size: 2.8em; font-weight: 800; margin-bottom: 0;'>
         Job Recommendation System
        </h1>
        <p style='font-size: 1.2em; color: #1b263b; margin-top: 0.2em;'>
        Upload a job description and candidate CVs to see who fits best — 
        powered by intelligent analysis and clean design.
        </p>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.image("Job Search Whiteboard.png")

# File uploaders
st.markdown("<h4 style='color:#0a1e3f;'>📋 Upload Job Description (PDF)</h4>", unsafe_allow_html=True)
jd_file = st.file_uploader("", type=["pdf"], key="jd_uploader")

st.markdown("<h4 style='color:#0a1e3f;'>📄 Upload Candidate CVs (PDFs)</h4>", unsafe_allow_html=True)
cv_files = st.file_uploader("", type=["pdf"], accept_multiple_files=True, key="cv_uploader")

col_left, col_right = st.columns([3, 1])
with col_right:
    run_eval = st.button("Run Evaluation", key="run_eval")

if run_eval:
    if not jd_file:
        st.warning("Please upload a Job Description file first.")
    elif not cv_files:
        st.warning("Please upload at least one CV file.")
    else:
        with st.spinner("Extracting and analyzing data..."):
            job_description = handle_JD(jd_file)
            candidates = handle_CVs(cv_files)
            st.write("### 🏆 Final Evaluation & Ranking")
            result = evaluate_candidates(job_description, candidates)
            try:
                st.json(json.loads(result))
            except:
                st.markdown(result, unsafe_allow_html=True)
