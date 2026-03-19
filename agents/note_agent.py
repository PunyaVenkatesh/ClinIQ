import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

def run_note_agent(symptoms: str, diagnosis: str) -> str:
    print("Note Agent: Generating clinical note...")
    
    prompt = (
        "You are a clinical documentation AI. Generate a structured SOAP note based on the following.\n\n"
        "SOAP Note Format:\n"
        "S (Subjective): What the patient reports\n"
        "O (Objective): Observable/measurable findings\n"
        "A (Assessment): Clinical assessment and differential diagnosis\n"
        "P (Plan): Recommended next steps and investigations\n\n"
        "Patient Symptoms: " + symptoms + "\n\n"
        "Clinical Assessment: " + diagnosis + "\n\n"
        "Generate a professional, concise SOAP note."
    )
    
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0.1
    )
    
    response = llm.invoke(prompt)
    return response.content