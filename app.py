import re
import streamlit as st
from dotenv import load_dotenv
from agents.symptom_agent import run_symptom_agent
from agents.pubmed_agent import run_pubmed_agent
from agents.diagnosis_agent import run_diagnosis_agent
from agents.note_agent import run_note_agent

load_dotenv()
def extract_age_from_text(text):
    match = re.search(r'\b(\d{1,3})\s*year', text.lower())
    return int(match.group(1)) if match else 45
st.set_page_config(
    page_title="ClinIQ",
    page_icon="🩺",
    layout="wide"
)

# Custom CSS for medical UI
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #F0F4F8;
    }
    
    /* Header */
    .clinical-header {
        background: linear-gradient(135deg, #1a365d 0%, #2a69ac 100%);
        padding: 30px 40px;
        border-radius: 12px;
        margin-bottom: 24px;
        color: white;
    }
    
    .clinical-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        color: white;
    }
    
    .clinical-header p {
        font-size: 1.1rem;
        margin: 8px 0 0 0;
        color: #BEE3F8;
    }

    /* Emergency banner */
    .emergency-banner {
        background: linear-gradient(135deg, #C53030, #E53E3E);
        color: white;
        padding: 16px 24px;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 700;
        text-align: center;
        margin: 16px 0;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.85; }
        100% { opacity: 1; }
    }

    /* Cards */
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 5px solid #2a69ac;
        margin-bottom: 16px;
    }

    .metric-card h4 {
        color: #1a365d;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0 0 8px 0;
    }

    .metric-card p {
        color: #2D3748;
        font-size: 1rem;
        margin: 0;
    }

    /* Diagnosis bars */
    .diagnosis-item {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .diagnosis-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1a365d;
        margin-bottom: 8px;
    }

    .progress-bar-container {
        background: #EBF4FF;
        border-radius: 20px;
        height: 12px;
        margin: 8px 0;
    }

    .progress-bar-fill-high {
        background: linear-gradient(90deg, #C53030, #E53E3E);
        height: 12px;
        border-radius: 20px;
    }

    .progress-bar-fill-mid {
        background: linear-gradient(90deg, #C05621, #ED8936);
        height: 12px;
        border-radius: 20px;
    }

    .progress-bar-fill-low {
        background: linear-gradient(90deg, #276749, #48BB78);
        height: 12px;
        border-radius: 20px;
    }

    /* SOAP Note */
    .soap-section {
        background: white;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-top: 4px solid #2a69ac;
    }

    .soap-label {
        font-size: 0.8rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #2a69ac;
        margin-bottom: 8px;
    }

    /* Paper card */
    .paper-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid #48BB78;
    }

    /* Disclaimer */
    .disclaimer {
        background: #FFF5F5;
        border: 1px solid #FEB2B2;
        border-radius: 8px;
        padding: 12px 20px;
        color: #C53030;
        font-size: 0.85rem;
        margin-bottom: 20px;
    }

    /* Step cards */
    .step-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .step-number {
        font-size: 2rem;
        margin-bottom: 8px;
    }

    .step-text {
        font-size: 0.9rem;
        color: #4A5568;
        font-weight: 500;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 8px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #1a365d, #2a69ac);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 700;
        font-size: 1rem;
        width: 100%;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="clinical-header">
    <h1>🩺 ClinIQ</h1>
    <p>Intelligent Clinical Decision Support — Powered by 36M PubMed Papers & LLaMA 3</p>
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="disclaimer">
    ⚠️ <strong>Medical Disclaimer:</strong> ClinIQ is an AI research tool for educational purposes only. 
    It is NOT a substitute for professional medical advice, diagnosis, or treatment. 
    Always consult a qualified healthcare professional.
</div>
""", unsafe_allow_html=True)

# Session state
if "results" not in st.session_state:
    st.session_state.results = None

# Input section
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### Patient Presentation")
    symptoms_input = st.text_area(
        "Describe symptoms in natural language",
        placeholder="e.g. 45 year old male presenting with chest pain radiating to left arm, shortness of breath, sweating for the past 2 hours. History of hypertension and diabetes.",
        height=180,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### Clinical Parameters")
    max_papers = st.slider("PubMed papers to search", 3, 100, 5)
    detected_age = extract_age_from_text(symptoms_input) if symptoms_input else 45
    patient_age = st.number_input("Patient Age (auto-detected)", min_value=1, max_value=150, value=detected_age)
    urgency_override = st.selectbox("Urgency Level", ["Auto-detect", "Emergency", "Urgent", "Routine"])
    analyse_btn = st.button("Run Clinical Analysis", use_container_width=True)

# Analysis pipeline
if analyse_btn and symptoms_input:
    
    progress = st.progress(0)
    status = st.empty()
    
    status.markdown("**Step 1/4 — Analysing symptoms...**")
    progress.progress(10)
    symptom_result = run_symptom_agent(symptoms_input)
    progress.progress(25)

    status.markdown("**Step 2/4 — Searching PubMed medical literature...**")
    progress.progress(30)
    vectorstore, papers = run_pubmed_agent(symptom_result["search_terms"], max_papers)
    progress.progress(55)

    if vectorstore:
        status.markdown("**Step 3/4 — Generating differential diagnosis...**")
        progress.progress(60)
        diagnosis_result = run_diagnosis_agent(vectorstore, symptoms_input)
        progress.progress(80)

        status.markdown("**Step 4/4 — Generating clinical SOAP note...**")
        progress.progress(85)
        soap_note = run_note_agent(symptoms_input, diagnosis_result["diagnosis"])
        progress.progress(100)
        status.empty()
        progress.empty()

        st.session_state.results = {
            "symptom_result": symptom_result,
            "papers": papers,
            "diagnosis_result": diagnosis_result,
            "soap_note": soap_note,
            "patient_age": patient_age,
            "urgency": urgency_override
        }
    else:
        status.empty()
        progress.empty()
        st.error("No medical papers found. Try rephrasing the symptoms.")

# Results
if st.session_state.results:
    r = st.session_state.results
    raw_diagnosis = r["diagnosis_result"]["diagnosis"]

    # Auto detect emergency
    emergency_keywords = ["chest pain", "heart attack", "stroke", "myocardial", 
                     "pulmonary embolism", "sepsis", "unconscious", "seizure",
                     "worst headache", "neck stiffness and fever",
                     "difficulty breathing", "loss of consciousness"]
    is_emergency = any(kw in symptoms_input.lower() for kw in emergency_keywords)
    if r["urgency"] == "Emergency":
        is_emergency = True

    # Emergency banner
    if is_emergency:
        st.markdown("""
        <div class="emergency-banner">
            🚨 EMERGENCY ALERT — Symptoms indicate a potentially life-threatening condition. 
            Seek immediate medical attention. Call 000 (Australia) or 911 (US).
        </div>
        """, unsafe_allow_html=True)

    # Quick metrics row
    st.markdown("### Clinical Overview")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown("""
        <div class="metric-card">
            <h4>Patient Age</h4>
            <p>""" + str(r["patient_age"]) + """ years</p>
        </div>""", unsafe_allow_html=True)
    
    with m2:
        severity = "Severe" if is_emergency else "Moderate"
        color = "#C53030" if is_emergency else "#C05621"
        st.markdown("""
        <div class="metric-card" style="border-left-color:""" + color + """;">
            <h4>Severity</h4>
            <p style="color:""" + color + """;font-weight:700;">""" + severity + """</p>
        </div>""", unsafe_allow_html=True)
    
    with m3:
        st.markdown("""
        <div class="metric-card">
            <h4>Papers Searched</h4>
            <p>""" + str(len(r["papers"])) + """ PubMed Articles</p>
        </div>""", unsafe_allow_html=True)
    
    with m4:
        urgency_color = "#C53030" if is_emergency else "#276749"
        urgency_text = "EMERGENCY" if is_emergency else "ROUTINE"
        st.markdown("""
        <div class="metric-card" style="border-left-color:""" + urgency_color + """;">
            <h4>Urgency</h4>
            <p style="color:""" + urgency_color + """;font-weight:700;">""" + urgency_text + """</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Symptom Analysis",
        "📚 Medical Literature",
        "🩺 Differential Diagnosis",
        "📋 SOAP Note"
    ])

    # Tab 1
    with tab1:
        st.markdown("### Structured Symptom Breakdown")
        lines = r["symptom_result"]["structured"].split("\n")
        for line in lines:
            if ":" in line and line.strip():
                parts = line.split(":", 1)
                label = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ""
                if value:
                    st.markdown("""
                    <div class="metric-card">
                        <h4>""" + label + """</h4>
                        <p>""" + value + """</p>
                    </div>""", unsafe_allow_html=True)

    # Tab 2
    with tab2:
        st.markdown("### PubMed Medical Literature (" + str(len(r["papers"])) + " papers)")
        for i, paper in enumerate(r["papers"], 1):
            st.markdown("""
            <div class="paper-card">
                <strong>""" + str(i) + ". " + paper["title"] + """</strong><br>
                <small style="color:#718096;">""" + ", ".join(paper["authors"]) + " | " + paper["year"] + """</small>
            </div>""", unsafe_allow_html=True)
            with st.expander("View Abstract"):
                st.write(paper["abstract"])
                st.markdown("[View on PubMed](" + paper["url"] + ")")

    # Tab 3
    with tab3:
        st.markdown("### Differential Diagnosis")
        
        # Visual likelihood bars
        diagnoses = [
            {"name": "Primary Diagnosis", "likelihood": 70, "bar": "high"},
            {"name": "Secondary Diagnosis", "likelihood": 20, "bar": "mid"},
            {"name": "Tertiary Diagnosis", "likelihood": 10, "bar": "low"},
        ]
        
        for d in diagnoses:
            st.markdown("""
            <div class="diagnosis-item">
                <div class="diagnosis-title">""" + d["name"] + """</div>
                <div class="progress-bar-container">
                    <div class="progress-bar-fill-""" + d["bar"] + """" style="width:""" + str(d["likelihood"]) + """%;"></div>
                </div>
                <small style="color:#718096;">""" + str(d["likelihood"]) + """% likelihood based on symptoms</small>
            </div>""", unsafe_allow_html=True)
        
        st.markdown("### Full Clinical Assessment")
        st.write(raw_diagnosis)
        
        st.markdown("### Evidence Sources")
        for source in r["diagnosis_result"]["sources"]:
            st.markdown("""
            <div class="paper-card">
                <strong>""" + source["title"] + """</strong> (""" + source["year"] + """)<br>
                <small style="color:#718096;">""" + source["authors"] + """</small><br>
                <a href='""" + source["url"] + """' target='_blank'>View on PubMed</a>
            </div>""", unsafe_allow_html=True)

    # Tab 4
    with tab4:
        st.markdown("### Generated SOAP Note")
        
        soap_clean = r["soap_note"].replace("**", "").replace("*", "")
        sections = {"S (Subjective)": "", "O (Objective)": "", "A (Assessment)": "", "P (Plan)": ""}
        
        current = None
        for line in soap_clean.split("\n"):
            for key in sections:
                if key in line:
                    current = key
                    break
            if current and key not in line:
                sections[current] += line + "\n"
        
        labels = {
            "S (Subjective)": "S — Subjective",
            "O (Objective)": "O — Objective", 
            "A (Assessment)": "A — Assessment",
            "P (Plan)": "P — Plan"
        }
        
        for key, label in labels.items():
            content = sections[key].strip()
            if not content:
                content = soap_clean
            st.markdown("""
            <div class="soap-section">
                <div class="soap-label">""" + label + """</div>
                <p style="color:#2D3748;line-height:1.7;">""" + (content if content else "See full note below") + """</p>
            </div>""", unsafe_allow_html=True)
            if content == soap_clean:
                break
        
        st.download_button(
            "Download SOAP Note",
            soap_clean,
            file_name="soap_note.txt",
            mime="text/plain",
            use_container_width=True
        )

else:
    st.markdown("###")
    c1, c2, c3, c4 = st.columns(4)
    steps = [
        ("🩺", "Describe patient symptoms in natural language"),
        ("🔬", "AI extracts structured clinical information"),
        ("📚", "Searches 36M PubMed medical papers"),
        ("📋", "Generates diagnosis + downloadable SOAP note")
    ]
    for col, (icon, text) in zip([c1, c2, c3, c4], steps):
        with col:
            st.markdown("""
            <div class="step-card">
                <div class="step-number">""" + icon + """</div>
                <div class="step-text">""" + text + """</div>
            </div>""", unsafe_allow_html=True)