import requests
from bs4 import BeautifulSoup

def get_bbc_headlines():
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    for h in soup.find_all(['h3', 'h2']):
        text = h.get_text(strip=True)
        if text and len(text) > 20 and text not in headlines:
            headlines.append(text)
    with open("bbc_headlines.txt", "w", encoding="utf-8") as f:
        for line in headlines:
            f.write(line + "\n")

if __name__ == "__main__":
    get_bbc_headlines()

# Приклад результату у файлі:
# Ukraine war: Russia launches new missile attack on Kyiv
# Climate change: UN warns of record-breaking heat
# UK economy: Inflation falls to 2%