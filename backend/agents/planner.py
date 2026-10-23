
"""
TrustCart planner — compares products from three built-in mock stores.
No separate store servers are required.
"""

from datetime import datetime, timedelta, timezone

from models.product import Product


STORE_INVENTORIES = {
    "Store A - TechBazaar": [
        {"id": "a1", "name": "AeroBook 14 (i5, 8GB)", "category": "laptop", "price": 52000, "in_stock": True, "shipping_cost": 0},
        {"id": "a2", "name": "AeroBook 14 (i5, 16GB)", "category": "laptop", "price": 58500, "in_stock": True, "shipping_cost": 0},
        {"id": "a3", "name": "NovaLite 15 (i3, 8GB)", "category": "laptop", "price": 41000, "in_stock": True, "shipping_cost": 0},
        {"id": "a4", "name": "PixelWave Phone 12", "category": "phone", "price": 29500, "in_stock": True, "shipping_cost": 0},
        {"id": "a5", "name": "EchoBuds Pro", "category": "headphones", "price": 3200, "in_stock": True, "shipping_cost": 0},
        {"id": "a6", "name": "PulseFit Smartwatch", "category": "smartwatch", "price": 4900, "in_stock": True, "shipping_cost": 0},
    ],
    "Store B - GadgetHub": [
        {"id": "b1", "name": "AeroBook 14 (i5, 8GB)", "category": "laptop", "price": 53500, "in_stock": True, "shipping_cost": 250},
        {"id": "b2", "name": "AeroBook 14 (i5, 16GB)", "category": "laptop", "price": 57000, "in_stock": True, "shipping_cost": 250},
        {"id": "b3", "name": "NovaLite 15 (i3, 8GB)", "category": "laptop", "price": 39500, "in_stock": True, "shipping_cost": 250},
        {"id": "b4", "name": "PixelWave Phone 12", "category": "phone", "price": 28900, "in_stock": True, "shipping_cost": 250},
        {"id": "b5", "name": "EchoBuds Pro", "category": "headphones", "price": 3450, "in_stock": True, "shipping_cost": 250},
        {"id": "b6", "name": "PulseFit Smartwatch", "category": "watch", "price": 6800, "in_stock": True, "shipping_cost": 250},
    ],
    "Store C - ByteMart": [
        {"id": "c1", "name": "AeroBook 14 (i5, 8GB)", "category": "laptop", "price": 51500, "in_stock": True, "shipping_cost": 400},
        {"id": "c2", "name": "AeroBook 14 (i5, 16GB)", "category": "laptop", "price": 59200, "in_stock": False, "shipping_cost": 400},
        {"id": "c3", "name": "NovaLite 15 (i3, 8GB)", "category": "laptop", "price": 40200, "in_stock": True, "shipping_cost": 400},
        {"id": "c4", "name": "Pulsar X12 5G Smartphone", "category": "phone", "price": 25499, "in_stock": True, "shipping_cost": 400},
        {"id": "c5", "name": "Pulsar X12 Pro Smartphone", "category": "phone", "price": 30999, "in_stock": True, "shipping_cost": 400},
        {"id": "c6", "name": "OrbitFit S2 Smartwatch", "category": "smartwatch", "price": 4599, "in_stock": True, "shipping_cost": 400},
        {"id": "c7", "name": "EchoBuds Pro Wireless Earbuds", "category": "headphones", "price": 2999, "in_stock": True, "shipping_cost": 400},
    ],
}

STORE_ENDPOINTS = list(STORE_INVENTORIES.keys())


def fetch_all_offers(query: str) -> list[Product]:
    """Search all built-in mock store inventories."""
    q = query.strip().lower()
    results = []

    for store_name, inventory in STORE_INVENTORIES.items():
        for item in inventory:
            category = item["category"].lower()
            name = item["name"].lower()

            # Accept singular/plural category searches and product names.
            normalized_q = q.rstrip("s")
            category_match = normalized_q == category.rstrip("s")
            name_match = q in name or normalized_q in name

            if category_match or name_match:
                results.append(
                    Product(
                        id=item["id"],
                        name=item["name"],
                        price=item["price"],
                        store=store_name,
                        in_stock=item["in_stock"],
                        shipping_cost=item["shipping_cost"],
                        last_updated=datetime.now(timezone.utc) - timedelta(minutes=5),
                    )
                )

    return results


def pick_best_deal(
    products: list[Product], budget: float | None = None
) -> Product | None:
    """Select the lowest-cost in-stock product within budget."""
    candidates = [p for p in products if p.in_stock]

    if budget is not None:
        candidates = [p for p in candidates if p.total_cost <= budget]

    return min(candidates, key=lambda p: p.total_cost, default=None)
