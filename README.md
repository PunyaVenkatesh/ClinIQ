---
title: ClinIQ
emoji: 🩺
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.55.0
app_file: app.py
pinned: false
---

# ClinIQ — Intelligent Clinical Decision Support

An agentic AI system that analyses patient symptoms, searches 36 million 
PubMed medical papers in real time, generates differential diagnoses with 
cited evidence, and produces downloadable SOAP notes.

---

## What It Does

- Accepts patient symptoms in plain natural language
- Auto-detects patient age from the description
- Searches 36M+ real PubMed medical papers live
- Generates ranked differential diagnoses with likelihood percentages
- Flags emergency cases with a real-time alert
- Produces a structured SOAP note — downloadable as a file
- Cites every diagnosis with real PubMed paper links

---

## Architecture
```
Patient Symptoms (free text)
        │
        ▼
Symptom Agent ──► Extracts structure + search terms
        │
        ▼
PubMed Agent ──► Searches 36M medical papers live
        │
        ▼
Diagnosis Agent ──► Differential diagnosis with citations
        │
        ▼
SOAP Note Agent ──► Professional clinical documentation
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| LangChain | Agent orchestration |
| Groq LLaMA 3.3 70B | Fast, free LLM |
| NCBI E-utilities API | Free PubMed access |
| FAISS | Vector similarity search |
| HuggingFace Embeddings | Local sentence embeddings |
| Streamlit | Interactive web UI |

---

## Run Locally
```bash
git clone https://github.com/PunyaVenkatesh/cliniq.git
cd cliniq
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:
```
GROQ_API_KEY=your_groq_api_key_here
```

Run:
```bash
streamlit run app.py
```

---

## Medical Disclaimer

ClinIQ is an AI research tool for educational purposes only. It is NOT 
a substitute for professional medical advice, diagnosis, or treatment. 
Always consult a qualified healthcare professional.

---

## Author

Punya Venkatesh — Masters of AI, Monash University (2026)

[LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/PunyaVenkatesh)