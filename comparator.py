def find_best(products):

    best = None

    for p in products:

        if best is None:
            best = p
        else:
            if p["price"] < best["price"]:
                best = p

    return best