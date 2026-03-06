from bs4 import BeautifulSoup

def extract_products(html, source):

    soup = BeautifulSoup(html, "html.parser")

    products = []

    for item in soup.find_all("a")[:20]:

        title = item.text.strip()

        if len(title) > 30:

            products.append({
                "title": title,
                "price": 0,
                "website": source
            })

    return products