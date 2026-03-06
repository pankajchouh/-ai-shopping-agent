from search_agent import search_websites
from browser_agent import open_page
from extractor import extract_products
from comparator import find_best

async def run_agent(query, send_update):

    await send_update("🔍 Searching websites...")

    links = search_websites(query)

    all_products = []

    for link in links:

        await send_update(f"🌐 Opening {link}")

        html = open_page(link)

        products = extract_products(html, link)

        all_products.extend(products)

    await send_update("📦 Extracting products")

    best = find_best(all_products)

    await send_update("🏆 Best product selected")

    return {
        "products": all_products,
        "best": best
    }