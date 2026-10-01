from urllib.parse import quote


CATALOG = {
    "home": [
        {
            "name": "Minimal Study Table",
            "category": "Furniture",
            "price": 2499,
            "platform": "Amazon",
            "url": "https://www.amazon.in/s?k=study+table",
        },
        {
            "name": "LED Warm Fairy Lights",
            "category": "Lighting",
            "price": 499,
            "platform": "Amazon",
            "url": "https://www.amazon.in/s?k=fairy+lights",
        },
        {
            "name": "Decorative Indoor Plant",
            "category": "Decor",
            "price": 699,
            "platform": "Flipkart",
            "url": "https://www.flipkart.com/search?q=indoor+plant",
        },
        {
            "name": "Cushion Set",
            "category": "Decor",
            "price": 799,
            "platform": "Amazon",
            "url": "https://www.amazon.in/s?k=cushion+set",
        },
        {
            "name": "Wall Art Set",
            "category": "Decor",
            "price": 999,
            "platform": "Amazon",
            "url": "https://www.amazon.in/s?k=wall+art",
        },
    ],
    "party": [
        {
            "name": "Birthday Decoration Kit",
            "category": "Decoration",
            "price": 599,
            "platform": "Amazon",
            "url": "https://www.amazon.in/s?k=birthday+decoration+kit",
        },
        {
            "name": "Cake",
            "category": "Food",
            "price": 699,
            "platform": "Swiggy",
            "url": "https://www.swiggy.com/",
        },
        {
            "name": "Disposable Dinner Set",
            "category": "Tableware",
            "price": 399,
            "platform": "Amazon",
            "url": "https://www.amazon.in/s?k=disposable+dinner+set",
        },
        {
            "name": "Party Balloons",
            "category": "Decoration",
            "price": 299,
            "platform": "Flipkart",
            "url": "https://www.flipkart.com/search?q=party+balloons",
        },
        {
            "name": "Snack Combo",
            "category": "Food",
            "price": 899,
            "platform": "Zomato",
            "url": "https://www.zomato.com/",
        },
    ],
    "jewelry": [
        {
            "name": "Minimal Pendant Necklace",
            "category": "Necklace",
            "price": 799,
            "platform": "Amazon",
            "url": "https://www.amazon.in/s?k=minimal+pendant+necklace",
        },
        {
            "name": "Classic Hoop Earrings",
            "category": "Earrings",
            "price": 499,
            "platform": "Flipkart",
            "url": "https://www.flipkart.com/search?q=hoop+earrings",
        },
        {
            "name": "Minimal Bracelet",
            "category": "Bracelet",
            "price": 599,
            "platform": "Amazon",
            "url": "https://www.amazon.in/s?k=minimal+bracelet",
        },
        {
            "name": "Oxidized Earrings",
            "category": "Earrings",
            "price": 349,
            "platform": "Amazon",
            "url": "https://www.amazon.in/s?k=oxidized+earrings",
        },
        {
            "name": "Artificial Pearl Necklace",
            "category": "Necklace",
            "price": 999,
            "platform": "Amazon",
            "url": "https://www.amazon.in/s?k=pearl+necklace",
        },
    ],
}


def search_catalog(
    category: str,
    budget: float,
    keywords: list[str] | None = None,
):
    products = CATALOG.get(
        category,
        [],
    )

    keywords = [
        keyword.lower()
        for keyword in (keywords or [])
    ]

    matching = []

    for product in products:
        if product["price"] > budget:
            continue

        searchable = (
            product["name"] + " "
            + product["category"]
        ).lower()

        if keywords and not any(
            keyword in searchable
            for keyword in keywords
        ):
            continue

        matching.append(product)

    if not matching:
        matching = [
            product
            for product in products
            if product["price"] <= budget
        ]

    return matching


def marketplace_search_url(
    platform: str,
    query: str,
):
    encoded = quote(query)

    if platform.lower() == "amazon":
        return (
            "https://www.amazon.in/s?k="
            f"{encoded}"
        )

    if platform.lower() == "flipkart":
        return (
            "https://www.flipkart.com/search?q="
            f"{encoded}"
        )

    return "https://www.google.com/search?q=" + encoded