from comparator import find_best
from synthetic_data import search_products


def _build_answer(query, products, best):
    if not products:
        return (
            f'"{query}" ke liye abhi koi matching product nahi mila. '
            "Aap thoda aur specific query try karein."
        )

    if not best:
        return f'"{query}" ke liye {len(products)} products mile hain.'

    return (
        f'"{query}" ke liye {len(products)} relevant products mile hain. '
        f'Best recommendation: {best["title"]} ({best["price_label"]}, '
        f'Rating {best["rating"]}/5). Buy link response ke saath add kiya gaya hai.'
    )


async def run_agent(query, send_update):
    clean_query = query.strip()

    await send_update("🔍 Searching products in catalog...")

    products = search_products(clean_query)

    await send_update(f"📦 {len(products)} products matched")

    best = find_best(products)

    if best:
        await send_update(f"🏆 Best product selected: {best['title']}")
    else:
        await send_update("ℹ️ No best product could be selected")

    answer = _build_answer(clean_query, products, best)

    return {"query": clean_query, "answer": answer, "products": products, "best": best}