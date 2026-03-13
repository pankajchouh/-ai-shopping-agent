import re
from urllib.parse import quote_plus


SYNTHETIC_PRODUCTS = [
    {
        "id": "p-1001",
        "title": "Noise Cancellation Wireless Earbuds Pro",
        "category": "audio",
        "brand": "SonicBeat",
        "description": "ANC earbuds with deep bass, quad mic calling, and 36-hour battery.",
        "price": 2999,
        "rating": 4.4,
        "delivery": "1 day delivery",
        "image_url": "https://picsum.photos/seed/earbuds-pro/640/420",
        "highlights": ["ANC", "Bluetooth 5.3", "Fast charging"],
    },
    {
        "id": "p-1002",
        "title": "Smart Fitness Watch AMOLED",
        "category": "wearables",
        "brand": "FitPulse",
        "description": "AMOLED display smartwatch with heart tracking and 100+ sports modes.",
        "price": 4499,
        "rating": 4.2,
        "delivery": "2 day delivery",
        "image_url": "https://picsum.photos/seed/smart-watch/640/420",
        "highlights": ["AMOLED", "GPS", "7 day battery"],
    },
    {
        "id": "p-1003",
        "title": '43" 4K Ultra HD Smart TV',
        "category": "television",
        "brand": "ViewMax",
        "description": "4K smart TV with HDR10 support, voice remote, and OTT app integration.",
        "price": 28999,
        "rating": 4.5,
        "delivery": "3 day delivery",
        "image_url": "https://picsum.photos/seed/4k-tv/640/420",
        "highlights": ["4K HDR", "Dolby Audio", "Voice Remote"],
    },
    {
        "id": "p-1004",
        "title": "Gaming Laptop Ryzen 7 RTX 4060",
        "category": "laptop",
        "brand": "NeoCore",
        "description": "High-performance gaming laptop with 16GB RAM and 1TB SSD.",
        "price": 104990,
        "rating": 4.6,
        "delivery": "2 day delivery",
        "image_url": "https://picsum.photos/seed/gaming-laptop/640/420",
        "highlights": ["RTX 4060", "144Hz display", "Backlit keyboard"],
    },
    {
        "id": "p-1005",
        "title": "Cotton Casual Shirt for Men",
        "category": "fashion",
        "brand": "UrbanWeave",
        "description": "Breathable cotton shirt with slim fit and all-day comfort.",
        "price": 999,
        "rating": 4.1,
        "delivery": "1 day delivery",
        "image_url": "https://picsum.photos/seed/cotton-shirt/640/420",
        "highlights": ["100% cotton", "Machine washable", "Slim fit"],
    },
    {
        "id": "p-1006",
        "title": "Non-Stick Cookware Set 5 Pcs",
        "category": "kitchen",
        "brand": "HomeChef",
        "description": "Induction compatible cookware set with durable non-stick coating.",
        "price": 2599,
        "rating": 4.3,
        "delivery": "2 day delivery",
        "image_url": "https://picsum.photos/seed/cookware-set/640/420",
        "highlights": ["Induction base", "5 pieces", "Easy to clean"],
    },
    {
        "id": "p-1007",
        "title": "Mirrorless Camera 24MP with Lens Kit",
        "category": "camera",
        "brand": "PixelCraft",
        "description": "24MP mirrorless camera with 4K video recording and kit lens.",
        "price": 57999,
        "rating": 4.7,
        "delivery": "3 day delivery",
        "image_url": "https://picsum.photos/seed/mirrorless-camera/640/420",
        "highlights": ["24MP sensor", "4K recording", "Interchangeable lens"],
    },
    {
        "id": "p-1008",
        "title": "Air Purifier HEPA Filter Room Size 400 sq.ft.",
        "category": "home-appliance",
        "brand": "PureNest",
        "description": "HEPA air purifier with PM2.5 display and silent night mode.",
        "price": 8999,
        "rating": 4.0,
        "delivery": "2 day delivery",
        "image_url": "https://picsum.photos/seed/air-purifier/640/420",
        "highlights": ["HEPA H13", "PM2.5 monitor", "Silent mode"],
    },
    {
        "id": "p-1009",
        "title": "Running Shoes Lightweight Cushion",
        "category": "footwear",
        "brand": "StrideX",
        "description": "Lightweight running shoes with breathable mesh and anti-slip sole.",
        "price": 2199,
        "rating": 4.2,
        "delivery": "1 day delivery",
        "image_url": "https://picsum.photos/seed/running-shoes/640/420",
        "highlights": ["Breathable mesh", "Anti-slip", "Cloud cushioning"],
    },
    {
        "id": "p-1010",
        "title": "10,000mAh Power Bank Fast Charge",
        "category": "mobile-accessories",
        "brand": "ChargeGo",
        "description": "Compact power bank with dual output and 22.5W fast charging.",
        "price": 1499,
        "rating": 4.3,
        "delivery": "1 day delivery",
        "image_url": "https://picsum.photos/seed/power-bank/640/420",
        "highlights": ["22.5W output", "Dual USB", "Pocket size"],
    },
    {
        "id": "p-1011",
        "title": "Office Ergonomic Chair with Lumbar Support",
        "category": "furniture",
        "brand": "WorkEase",
        "description": "Adjustable ergonomic chair with breathable mesh and lumbar support.",
        "price": 6999,
        "rating": 4.4,
        "delivery": "4 day delivery",
        "image_url": "https://picsum.photos/seed/office-chair/640/420",
        "highlights": ["Lumbar support", "Height adjustable", "Mesh back"],
    },
    {
        "id": "p-1012",
        "title": "Organic Green Tea 100 Bags",
        "category": "grocery",
        "brand": "LeafAura",
        "description": "Antioxidant-rich organic green tea bags for daily wellness routine.",
        "price": 649,
        "rating": 4.1,
        "delivery": "1 day delivery",
        "image_url": "https://picsum.photos/seed/green-tea/640/420",
        "highlights": ["Organic leaves", "100 tea bags", "No added sugar"],
    },
]


def _tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def _search_buy_link(title):
    return f"https://www.amazon.in/s?k={quote_plus(title)}"


def _enrich_product(product, score):
    return {
        **product,
        "score": score,
        "price_label": f"Rs. {product['price']:,}",
        "buy_link": _search_buy_link(product["title"]),
    }


def _match_score(product, query_tokens):
    title = product["title"].lower()
    category = product["category"].lower()
    description = product["description"].lower()
    highlights = " ".join(product.get("highlights", [])).lower()

    score = 0
    for token in query_tokens:
        if token in title:
            score += 4
        if token in category:
            score += 3
        if token in description:
            score += 2
        if token in highlights:
            score += 1
    return score


def search_products(query, limit=8):
    query_tokens = _tokenize(query)
    scored_products = []

    if query_tokens:
        for product in SYNTHETIC_PRODUCTS:
            score = _match_score(product, query_tokens)
            if score > 0:
                scored_products.append(_enrich_product(product, score))

    if not scored_products:
        for product in SYNTHETIC_PRODUCTS:
            scored_products.append(_enrich_product(product, 1))

    scored_products.sort(
        key=lambda item: (item["score"], item["rating"], -item["price"]),
        reverse=True,
    )
    return scored_products[:limit]
