from fastapi import FastAPI, Query
from pydantic import HttpUrl
from typing import Dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time
import os
import json

app = FastAPI()

visited_urls = set()

def init_driver():
    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def scrape_page(driver, url):
    print(f"[SCRAPING] {url}")
    try:
        driver.get(url)
        time.sleep(1.5)  # Let JS load
        soup = BeautifulSoup(driver.page_source, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        links = {
            urljoin(url, a['href'])
            for a in soup.find_all("a", href=True)
            if urlparse(urljoin(url, a['href'])).netloc == urlparse(url).netloc
        }
        return text, links
    except Exception as e:
        return f"Error scraping {url}: {str(e)}", set()

def crawl_site(start_url, limit=25):
    driver = init_driver()
    to_visit = [start_url]
    scraped = {}

    while to_visit and len(scraped) < limit:
        url = to_visit.pop(0)
        if url in visited_urls:
            continue
        visited_urls.add(url)

        content, links = scrape_page(driver, url)
        scraped[url] = content
        to_visit.extend(links - visited_urls)

    driver.quit()
    return scraped

@app.get("/scrape")
def scrape(url: HttpUrl, limit: int = Query(25, le=100)):
    scraped_data = crawl_site(str(url), limit=limit)

    # Convert all keys to string
    stringified_data = {str(k): v for k, v in scraped_data.items()}

    # Save to output file
    os.makedirs("output", exist_ok=True)
    output_path = f"output/scraped_{int(time.time())}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(stringified_data, f, indent=2, ensure_ascii=False)

    return {
        "status": "success",
        "total_pages": len(stringified_data),
        "output_file": output_path
    }
