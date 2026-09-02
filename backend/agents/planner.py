"""
Planner Agent — v1 (pure logic, no LLM yet).

Calls all connected stores, gathers results, and picks the best deal
based on total cost (price + shipping), while respecting stock and budget.

We start with deterministic logic before adding an LLM reasoning layer,
so we always have a reliable baseline to fall back on and compare against.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import httpx
from models.product import Product

STORE_ENDPOINTS = [
    "http://localhost:8001/search",
    "http://localhost:8002/search",
]


def fetch_all_offers(query: str) -> list[Product]:
    """Query every connected store and collect all matching products."""
    all_products = []
    for endpoint in STORE_ENDPOINTS:
        try:
            response = httpx.get(endpoint, params={"query": query}, timeout=5.0)
            response.raise_for_status()
            for item in response.json():
                all_products.append(Product(**item))
        except httpx.RequestError as e:
            # A store being down shouldn't crash the whole search —
            # just skip it and note it. This matters later for the audit log.
            print(f"[WARN] Could not reach {endpoint}: {e}")
    return all_products


def pick_best_deal(products: list[Product], budget: float | None = None) -> Product | None:
    """
    Pick the best in-stock product within budget, by lowest total cost.
    Returns None if nothing qualifies.
    """
    candidates = [p for p in products if p.in_stock]
    if budget is not None:
        candidates = [p for p in candidates if p.total_cost <= budget]

    if not candidates:
        return None

    return min(candidates, key=lambda p: p.total_cost)


if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from utils.confidence import compute_confidence

    offers = fetch_all_offers("laptop")
    print(f"\nFound {len(offers)} offers:")
    for o in offers:
        print(f"  {o.store}: {o.name} - total cost ₹{o.total_cost} (in stock: {o.in_stock})")

    best = pick_best_deal(offers, budget=60000)
    print("\nBest deal under ₹60,000:")
    if best:
        print(f"  {best.store}: {best.name} - ₹{best.total_cost}")
        confidence = compute_confidence(best, offers, stores_reached=2)
        print(f"\nConfidence: {confidence['overall_score']}/100")
        for item in confidence["breakdown"]:
            print(f"  - {item['factor']}: {item['score']}/100 — {item['reason']}")
    else:
        print("  No qualifying deal found.")