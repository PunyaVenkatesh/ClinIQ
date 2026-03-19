from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from core.embeddings import get_embeddings

def build_vectorstore(papers: list):
    embeddings = get_embeddings()
    docs = []
    for paper in papers:
        content = "Title: " + paper["title"] + "\n\nAbstract: " + paper["abstract"]
        metadata = {
            "title": paper["title"],
            "authors": ", ".join(paper["authors"]),
            "url": paper["url"],
            "year": paper["year"]
        }
        docs.append(Document(page_content=content, metadata=metadata))
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

def search_vectorstore(vectorstore, query: str, k: int = 3):
    return vectorstore.similarity_search(query, k=k)