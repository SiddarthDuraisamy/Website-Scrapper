from fastapi import FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin, urlparse
from typing import Dict, Set
import time

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

def create_browser():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def get_text_content(driver, url: str) -> str:
    try:
        driver.get(url)
        time.sleep(2)  # Let JS render
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        return f"[ERROR] {str(e)}"

def extract_links(driver, base_url: str) -> Set[str]:
    driver.get(base_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = set()
    base_domain = urlparse(base_url).netloc

    for tag in soup.find_all("a", href=True):
        href = tag['href']
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)
        if parsed.scheme.startswith("http") and parsed.netloc == base_domain:
            links.add(full_url.split('#')[0])
    return links

def recursive_scrape(start_url: str, max_depth=2) -> Dict[str, str]:
    visited = set()
    to_visit = [(start_url, 0)]
    results = {}

    with create_browser() as driver:
        while to_visit:
            current_url, depth = to_visit.pop()
            if current_url in visited or depth > max_depth:
                continue

            print(f"[SCRAPING] {current_url}")
            visited.add(current_url)

            content = get_text_content(driver, current_url)
            results[current_url] = content

            if depth < max_depth:
                try:
                    links = extract_links(driver, current_url)
                    for link in links:
                        if link not in visited:
                            to_visit.append((link, depth + 1))
                except Exception as e:
                    print(f"[LINK ERROR] {e}")

    return results

@app.post("/scrape")
def scrape_site(request: ScrapeRequest):
    return recursive_scrape(request.url)