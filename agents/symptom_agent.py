import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

def run_symptom_agent(raw_input: str) -> dict:
    print("Symptom Agent: Analysing input...")
    
    prompt = (
        "You are a medical AI assistant. Extract structured clinical information from the following patient description.\n\n"
        "Return your response in this exact format:\n"
        "SYMPTOMS: [list the main symptoms]\n"
        "DURATION: [how long symptoms have been present]\n"
        "SEVERITY: [mild/moderate/severe]\n"
        "KEY FINDINGS: [any important clinical details]\n"
        "SEARCH TERMS: [3-5 medical search terms for PubMed]\n\n"
        "Patient Description: " + raw_input
    )
    
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0.1
    )
    
    response = llm.invoke(prompt)
    
    lines = response.content.split("\n")
    search_terms = ""
    for line in lines:
        if "SEARCH TERMS:" in line:
            search_terms = line.replace("SEARCH TERMS:", "").strip()
    
    return {
        "structured": response.content,
        "search_terms": search_terms if search_terms else raw_input
    }