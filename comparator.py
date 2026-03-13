def find_best(products):
    if not products:
        return None

    # Prefer relevance first, then better rating, then lower price.
    return max(
        products,
        key=lambda product: (
            product.get("score", 0),
            product.get("rating", 0),
            -product.get("price", float("inf")),
        ),
    )