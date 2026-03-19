import requests
import xml.etree.ElementTree as ET

def search_pubmed(query: str, max_results: int = 5) -> list:
    print("PubMed: Searching for '" + query + "'...")
    
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance"
    }
    
    search_response = requests.get(search_url, params=search_params)
    ids = search_response.json()["esearchresult"]["idlist"]
    
    if not ids:
        return []
    
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml"
    }
    
    fetch_response = requests.get(fetch_url, params=fetch_params)
    root = ET.fromstring(fetch_response.content)
    
    papers = []
    for article in root.findall(".//PubmedArticle"):
        try:
            title = article.findtext(".//ArticleTitle", default="No title")
            abstract = article.findtext(".//AbstractText", default="No abstract available")
            
            authors_list = []
            for author in article.findall(".//Author")[:3]:
                lastname = author.findtext("LastName", default="")
                forename = author.findtext("ForeName", default="")
                if lastname:
                    authors_list.append(forename + " " + lastname)
            
            year = article.findtext(".//PubDate/Year", default="Unknown")
            pmid = article.findtext(".//PMID", default="")
            
            papers.append({
                "title": title,
                "abstract": abstract,
                "authors": authors_list,
                "year": year,
                "url": "https://pubmed.ncbi.nlm.nih.gov/" + pmid
            })
        except Exception as e:
            continue
    
    print("PubMed: Found " + str(len(papers)) + " papers.")
    return papers