import requests
from datetime import datetime, timedelta

API_KEY = "872ffde115604dec8d9d3a1ba2b9628e"  # Replace with your NewsAPI key

def fetch_agriculture_news(country="in", keyword="agriculture", from_days_ago=1, page_size=5):
    """
    Fetch agriculture-related news for India.
    
    Parameters:
    - country: country code (default "in")
    - keyword: keyword search (default "agriculture")
    - from_days_ago: number of days ago to start fetching news
    - page_size: number of articles to fetch
    """
    from_date = (datetime.now() - timedelta(days=from_days_ago)).strftime("%Y-%m-%d")
    
    params = {
        "q": keyword,
        "from": from_date,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "country": country
    }
    
    url = "https://newsapi.org/v2/top-headlines"
    params["apiKey"] = API_KEY
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return []
    
    data = response.json()
    return data.get("articles", [])

def display_articles(articles):
    for art in articles:
        print(f"Title: {art.get('title')}")
        print(f"Source: {art.get('source', {}).get('name')}")
        print(f"Published: {art.get('publishedAt')}")
        print(f"URL: {art.get('url')}")
        print(f"Description: {art.get('description')}\n")
        print("-" * 80)

# Fetch Indian agriculture news from yesterday
articles = fetch_agriculture_news(from_days_ago=1, page_size=10)
display_articles(articles)
