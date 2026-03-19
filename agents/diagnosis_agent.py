import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from core.vectorstore import search_vectorstore
load_dotenv()

def run_diagnosis_agent(vectorstore, symptoms: str) -> dict:
    print("Diagnosis Agent: Generating differential diagnosis...")
    
    relevant_docs = search_vectorstore(vectorstore, symptoms, k=3)
    
    context = ""
    sources = []
    for doc in relevant_docs:
        context += "Paper: " + doc.metadata["title"] + "\n"
        context += "Authors: " + doc.metadata["authors"] + "\n"
        context += "Year: " + doc.metadata["year"] + "\n"
        context += "Content: " + doc.page_content + "\n"
        context += "-" * 40 + "\n"
        sources.append({
            "title": doc.metadata["title"],
            "authors": doc.metadata["authors"],
            "url": doc.metadata["url"],
            "year": doc.metadata["year"]
        })
    
    prompt = (
        "You are an expert clinical AI assistant supporting a doctor.\n\n"
        "Based on the symptoms and medical literature below, provide:\n\n"
        "1. DIFFERENTIAL DIAGNOSIS: Top 3 possible diagnoses with likelihood\n"
        "2. SUPPORTING EVIDENCE: Which papers support each diagnosis\n"
        "3. RED FLAGS: Any urgent symptoms requiring immediate attention\n"
        "4. RECOMMENDED WORKUP: Tests or investigations to confirm diagnosis\n"
        "5. DISCLAIMER: Always remind this is AI assistance, not medical advice\n\n"
        "Patient Symptoms:\n" + symptoms + "\n\n"
        "Medical Literature:\n" + context
    )
    
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0.2
    )
    
    response = llm.invoke(prompt)
    
    return {
        "diagnosis": response.content,
        "sources": sources
    }