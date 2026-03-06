import requests
from bs4 import BeautifulSoup

def search_websites(query):

    url = f"https://www.google.com//html/?q={query}"

    res = requests.get(url)

    soup = BeautifulSoup(res.text, "html.parser")

    links = []

    for a in soup.select(".result__a")[:8]:
        links.append(a["href"])

    return links