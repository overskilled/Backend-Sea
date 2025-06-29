import os
from newspaper import Article
from serpapi import GoogleSearch

from .gemini import summarize_or_analyze_article
os.environ["SERPAPI_KEY"] = "ec9a2baf6dd6e923fc4ada09f8bbbaebc3f65cb1cefa0bf141fb91f309ce0fbe"

SOCIAL_DOMAINS = [
    "facebook.com",
    "linkedin.com",
    "instagram.com",
    "twitter.com", 
    "x.com",        
]

def is_social_link(url):
    return any(domain in url for domain in SOCIAL_DOMAINS)

def search_google(query, num_results):
    params = {
        "engine": "google",
        "q": query,
        "num": num_results,
        "api_key": os.getenv("SERPAPI_KEY"),
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("organic_results", [])

def extract_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        summary = summarize_or_analyze_article(article.text, "Summarize in one sentence, and tell if what is being said is positive, negative or neutral in just one word like: Positive.")

        return {
            "title": article.title,
            "url": url,
            "text": article.text,
            "gemini_summary": summary
        }
    except Exception as e:
        return {"url": url, "error": str(e)}

def scrape_topic(topic, num_results=20):
    search_results = search_google(topic, num_results)  
    social_links = []
    general_links = []

    for item in search_results:
        url = item.get("link")
        if not url:
            continue
        if is_social_link(url) and len(social_links) < 3:
            social_links.append(url)
        elif len(general_links) < (num_results - len(social_links)):
            general_links.append(url)

        # Stop early if we hit our goal
        if len(social_links) + len(general_links) >= num_results:
            break

    final_urls = social_links + general_links
    articles = [extract_article(url) for url in final_urls]
    return articles
