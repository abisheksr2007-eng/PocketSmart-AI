from typing import Any

from .catalog_service import search_catalog
from .gemini_service import generate_with_gemini


def _select_items(
    category: str,
    budget: float,
    keywords: list[str],
    limit: int = 5,
):
    products = search_catalog(
        category=category,
        budget=budget,
        keywords=keywords,
    )

    return products[:limit]


def _format_items(
    products: list[dict],
    reasons: list[str],
):
    items = []

    for index, product in enumerate(products):
        reason = (
            reasons[index]
            if index < len(reasons)
            else "Fits the selected budget and plan."
        )

        items.append(
            {
                "name": product["name"],
                "category": product["category"],
                "price": float(product["price"]),
                "reason": reason,
                "platform": product.get("platform"),
                "url": product.get("url"),
            }
        )

    return items


def generate_home_recommendation(
    data: dict[str, Any],
):
    budget = float(data["budget"])

    products = _select_items(
        category="home",
        budget=budget,
        keywords=[
            data.get("style", "modern"),
            *data.get("priorities", []),
        ],
    )

    if not products:
        products = _select_items(
            "home",
            budget,
            [],
        )

    total = sum(
        float(product["price"])
        for product in products
    )

    if total > budget:
        total = budget

    fallback = {
        "planner_type": "home",
        "title": "PocketSmart Home Plan",
        "summary": (
            f"A {data.get('style', 'modern')} "
            f"home setup for a budget of ₹{budget:,.0f}."
        ),
        "estimated_total": total,
        "items": _format_items(
            products,
            [
                "Useful for improving the room without overspending.",
                "Adds practical functionality to the space.",
                "Helps create a cleaner visual appearance.",
                "Flexible option for a student or small home.",
                "Can be purchased gradually as the budget allows.",
            ],
        ),
        "tips": [
            "Prioritize functional furniture before decorative pieces.",
            "Buy larger items first and add decoration later.",
            "Compare prices across marketplaces before purchasing.",
        ],
    }

    result = generate_with_gemini(
        "home",
        data,
        fallback,
    )

    result["planner_type"] = "home"
    result["title"] = "PocketSmart Home Plan"

    return result


def generate_party_recommendation(
    data: dict[str, Any],
):
    budget = float(data["budget"])

    products = _select_items(
        category="party",
        budget=budget,
        keywords=[
            data.get("occasion", ""),
            data.get("theme", ""),
            data.get("food_preference", ""),
        ],
    )

    if not products:
        products = _select_items(
            "party",
            budget,
            [],
        )

    total = sum(
        float(product["price"])
        for product in products
    )

    fallback = {
        "planner_type": "party",
        "title": "PocketSmart Party Plan",
        "summary": (
            f"A budget-friendly "
            f"{data.get('occasion', 'party')} "
            f"for approximately "
            f"{data.get('guests', 10)} guests."
        ),
        "estimated_total": min(total, budget),
        "items": _format_items(
            products,
            [
                "Provides decoration while keeping the cost controlled.",
                "Suitable for the selected guest count.",
                "Useful for serving guests conveniently.",
                "Adds atmosphere without a large expense.",
                "Can be adjusted according to the final guest list.",
            ],
        ),
        "tips": [
            "Set aside part of the budget for unexpected expenses.",
            "Order food according to confirmed guest count.",
            "DIY decorations can reduce the total cost.",
        ],
    }

    result = generate_with_gemini(
        "party",
        data,
        fallback,
    )

    result["planner_type"] = "party"
    result["title"] = "PocketSmart Party Plan"

    return result


def generate_jewelry_recommendation(
    data: dict[str, Any],
):
    budget = float(data["budget"])

    products = _select_items(
        category="jewelry",
        budget=budget,
        keywords=[
            data.get("jewelry_type", ""),
            data.get("style", ""),
            data.get("metal", ""),
        ],
    )

    if not products:
        products = _select_items(
            "jewelry",
            budget,
            [],
        )

    total = sum(
        float(product["price"])
        for product in products
    )

    fallback = {
        "planner_type": "jewelry",
        "title": "PocketSmart Jewelry Plan",
        "summary": (
            f"Jewelry suggestions for a "
            f"{data.get('occasion', 'casual')} occasion "
            f"within ₹{budget:,.0f}."
        ),
        "estimated_total": min(total, budget),
        "items": _format_items(
            products,
            [
                "Simple option that works with multiple outfits.",
                "Easy-to-style design for regular use.",
                "Good budget-conscious accessory option.",
                "Useful when you want a statement without overspending.",
                "Can be combined with other minimal pieces.",
            ],
        ),
        "tips": [
            "Choose the jewelry type based on your outfit neckline.",
            "For frequent use, prioritize comfortable lightweight pieces.",
            "Check material and return information before purchasing.",
        ],
    }

    result = generate_with_gemini(
        "jewelry",
        data,
        fallback,
    )

    result["planner_type"] = "jewelry"
    result["title"] = "PocketSmart Jewelry Plan"

    return result