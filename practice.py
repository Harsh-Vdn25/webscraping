import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

BASE_URL = "https://malayalam.krishijagran.com/farm-management/organic-farming/importance-of-magnolia-garden/"

def get_homepage_articles():
    resp = requests.get(BASE_URL)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")
    
    articles = []
    for h2 in soup.select("h2"):
        a = h2.find("a")
        if a and a.get("href"):
            title = a.get_text(strip=True)
            link = urljoin(BASE_URL, a["href"])
            articles.append({"title": title, "link": link})
    return articles

def get_article_content(article_url):
    resp = requests.get(article_url)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    # Title
    title = soup.select_one("h1").get_text(strip=True) if soup.select_one("h1") else ""

    # Publish date (if available)
    date = soup.select_one("time")
    date = date.get_text(strip=True) if date else None

    # Article body
    paragraphs = []
    for p in soup.select("div.entry-content p, div.article-content p"):
        text = p.get_text(strip=True)
        if text:
            paragraphs.append(text)
    body = "\n\n".join(paragraphs)

    return {
        "title": title,
        "date": date,
        "body": body,
        "url": article_url
    }

if __name__ == "__main__":
    articles = get_homepage_articles()
    all_data = []
    
    for art in articles[:10]:  # scrape first 10 for testing
        content = get_article_content(art["link"])
        all_data.append(content)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    print(df.head())

    # Save as CSV or JSON
    df.to_csv("krishijagran_articles.csv", index=False, encoding="utf-8-sig")
    df.to_json("krishijagran_articles.json", orient="records", force_ascii=False, indent=2)
