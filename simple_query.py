import requests
from bs4 import BeautifulSoup

def get_bbc_headlines():
    url = "https://www.bbc.com/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    seen = set()

    # 1) Основні відомі селектори BBC
    for tag in soup.select("h3.gs-c-promo-heading__title, h2.gs-c-promo-heading__title"):
        text = tag.get_text(strip=True)
        if text and text not in seen:
            seen.add(text)
            headlines.append(text)

    # 2) Fallback — будь-які h1/h2/h3 довжиною > 15 символів
    for tag in soup.select("h1, h2, h3"):
        text = tag.get_text(strip=True)
        if text and len(text) > 15 and text not in seen:
            seen.add(text)
            headlines.append(text)

    return headlines

if __name__ == "__main__":
    headlines = get_bbc_headlines()
    print(f"Знайдено {len(headlines)} заголовків")
    for i, h in enumerate(headlines, 1):
        print(f"{i:02d}. {h}")
