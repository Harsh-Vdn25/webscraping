import requests
from bs4 import BeautifulSoup

API_KEY = "api_live_vuSeDdLoNvz5OctOpdsZKBH5R2LBmELnbhCmlBk6OHRerznoEm2cRa"
URL = "https://api.apitube.io/v1/news/everything"

params = {
    "title": "agriculture",
    "language.code": "en",
    "source.country.code": "in",
    "per_page": 5
}

headers = {"X-API-Key": API_KEY}

def fetch_full_text(url):
    """Scrape full text from the article URL if content field is missing"""
    try:
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        paragraphs = soup.find_all("p")
        full_text = " ".join(p.text.strip() for p in paragraphs if p.text.strip())
        return full_text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

# Fetch news from API
response = requests.get(URL, headers=headers, params=params)
data = response.json()

articles_list = []

for article in data.get("results", []):
    title = article.get("title")
    url = article.get("href")
    published = article.get("published_at")
    
    # Try API content field first; else scrape the URL
    content = article.get("content")
    if not content or content.strip() == "":
        content = fetch_full_text(url)
    
    articles_list.append({
        "title": title,
        "url": url,
        "published": published,
        "content": content
    })

# Print all articles
for art in articles_list:
    print(f"Title: {art['title']}")
    print(f"URL: {art['url']}")
    print(f"Published: {art['published']}")
    print(f"Content: {art['content'][:500]}...")  # Print first 500 chars
    print("-" * 80)
