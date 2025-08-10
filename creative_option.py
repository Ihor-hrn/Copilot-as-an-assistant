import csv
import re
from urllib.parse import urljoin
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news/technology"
KEYWORD_REGEX = r"(technology|tech|ai|artificial intelligence|технолог)"  # можна залишити порожнім "" щоб вимкнути фільтр
MIN_LEN = 15

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

def fetch_html(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    if not resp.encoding:
        resp.encoding = resp.apparent_encoding
    return resp.text

def extract_headings_with_links(html: str, base_url: str):
    """Повертає список (title, abs_url) у порядку появи; бере h1/h2/h3 + посилання поруч/вище."""
    soup = BeautifulSoup(html, "html.parser")
    seen = set()
    out = []
    for tag in soup.find_all(["h1", "h2", "h3"]):
        title = tag.get_text(strip=True)
        if not title or len(title) < MIN_LEN:
            continue
        # знайти <a>: спочатку всередині, потім серед батьків
        a = tag.find("a", href=True) or tag.find_parent("a", href=True)
        href = a["href"] if a else None
        abs_url = urljoin(base_url, href) if href else None
        if title not in seen:
            seen.add(title)
            out.append((title, abs_url))
    return out

def filter_items(items, keyword_regex: str):
    """Пропускає, якщо збіг у тексті АБО якщо url містить '/technology'."""
    if not keyword_regex:
        return items
    pat = re.compile(keyword_regex, re.IGNORECASE)
    filtered = []
    for title, url in items:
        by_title = bool(pat.search(title))
        by_url = bool(url and "/technology" in url)
        if by_title or by_url:
            filtered.append((title, url))
    return filtered

def save_csv(items, source_url: str, out_path: str = None) -> str:
    if out_path is None:
        out_path = f"bbc_headlines_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    ts = datetime.now(timezone.utc).isoformat()
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp_utc", "source_url", "headline", "url"])
        for title, url in items:
            w.writerow([ts, source_url, title, url or ""])
    return out_path

if __name__ == "__main__":
    html = fetch_html(URL)
    all_items = extract_headings_with_links(html, URL)
    kept = filter_items(all_items, KEYWORD_REGEX)
    out = save_csv(kept, URL)
    print(f"Found {len(all_items)} total, kept {len(kept)} → saved to {out}")
