import os
import requests
from newspaper import Article
from serpapi import GoogleSearch
from concurrent.futures import ThreadPoolExecutor, as_completed

from .gemini import summarize_or_analyze_article, fetch_person_info_from_gemini

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

def search_google(query, num_results=5):
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

        if not article.text.strip():
            return None

        return {
            "title": article.title,
            "url": url,
            "text": article.text
        }
    except Exception:
        return None

def summarize_articles(articles):
    summarized = []
    for art in articles:
        summary = summarize_or_analyze_article(
            art["text"],
            "Summarize in one sentence, and tell if what is being said is positive, negative or neutral in just one word like: Positive ."
        )
        art["gemini_summary"] = summary
        summarized.append(art)
    return summarized

def generate_fake_mentions(name: str, summaries: list):
    def generate_quotes(name: str, sentiment: str, base_summaries: list, count: int):
        prompt = f"""
Generate {count} social media style quotes based on the following article summaries about {name}. Each quote must reflect the sentiment: {sentiment}. Quotes must be believable and sound like real online comments. Format: 1 sentence per quote.

Summaries:
{chr(10).join(base_summaries)}
"""
        response = fetch_person_info_from_gemini(prompt)
        return [line.strip() for line in response.split("\n") if line.strip()][:count]

    positive = generate_quotes(name, "Positive", summaries, 7)
    neutral = generate_quotes(name, "Neutral", summaries, 7)
    negative = generate_quotes(name, "Negative", summaries, 6)

    return {
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
    }

def scrape_topic(topic, num_results=2):
    search_results = search_google(topic, num_results * 3)
    urls = [item.get("link") for item in search_results if item.get("link")]

    articles = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(extract_article, url): url for url in urls}
        for future in as_completed(future_to_url):
            result = future.result()
            if result:
                articles.append(result)
            if len(articles) >= num_results:
                break

    summarized_articles = summarize_articles(articles)
    summaries = [a["gemini_summary"] for a in summarized_articles]
    mentions = generate_fake_mentions(topic, summaries)

    return {
        "name": topic,
        "articles": summarized_articles,
        "mentions": mentions
    }

def fetch_person_info(name: str) -> str:
    return fetch_person_info_from_gemini(name)
