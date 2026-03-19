from utils.pubmed_fetcher import search_pubmed
from core.vectorstore import build_vectorstore

def run_pubmed_agent(search_terms: str, max_results: int = 5):
    print("PubMed Agent: Fetching medical literature...")
    papers = search_pubmed(search_terms, max_results)
    
    if not papers:
        return None, []
    
    vectorstore = build_vectorstore(papers)
    return vectorstore, papers