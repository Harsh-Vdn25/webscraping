from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

# ----------------------------
# Step 1: Get dynamic URLs from main pest alert page
# ----------------------------
session = HTMLSession()
src_url = "https://www.nbair.res.in/pest-alert"

response = session.get(src_url)
response.html.render(timeout=20)  # Executes JS to load content

soup = BeautifulSoup(response.html.html, "html.parser")

# Extract hrefs from div > span.field-content > a
links = []
for div in soup.find_all("div", class_="views-field views-field-title"):
    span_tag = div.find("span", class_="field-content")
    if span_tag:
        a_tag = span_tag.find("a")
        if a_tag and a_tag.get("href"):
            full_url = urljoin(src_url, a_tag["href"])
            links.append(full_url)

print(f"Extracted {len(links)} links from main page.")

# ----------------------------
# Step 2: Scrape header and image from each URL
# ----------------------------
def scrape_pest_info(urls):
    results = []
    for url in urls:
        resp = session.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")

        header_span = soup.select_one("h1.page-header span")
        title = header_span.text.strip() if header_span else None

        img_tag = soup.select_one(
            "div.field.field--name-field-pest-picture div.field--item img"
        )
        img_src = urljoin(url, img_tag["src"]) if img_tag and img_tag.get("src") else None

        results.append({
            "url": url,
            "title": title,
            "image_src": img_src
        })
    return results

data = scrape_pest_info(links)

# ----------------------------
# Step 3: Download images
# ----------------------------
def download_images(data, folder="pest_images"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    for item in data:
        img_url = item.get("image_src")
        title = item.get("title", "unknown").replace("/", "_").replace("\\", "_")

        if img_url:
            try:
                r = session.get(img_url, stream=True)
                if r.status_code == 200:
                    ext = os.path.splitext(img_url)[1] or ".jpg"
                    path = os.path.join(folder, f"{title}{ext}")
                    with open(path, "wb") as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
                    print(f"Downloaded: {path}")
                else:
                    print(f"Failed to download {img_url}")
            except Exception as e:
                print(f"Error downloading {img_url}: {e}")
        else:
            print(f"No image URL for {title}")

download_images(data, folder="pest_alert_images")

# ----------------------------
# Step 4: Print results
# ----------------------------
for item in data:
    print(item)
