"""
Mock Store A — pretend electronics store.
Run standalone with: uvicorn store_a:app --port 8001
"""

from fastapi import FastAPI
from datetime import datetime, timedelta
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from models.product import Product

app = FastAPI(title="Store A - TechBazaar")

FAKE_INVENTORY = [
    {"id": "a1", "name": "AeroBook 14 (i5, 8GB)", "category": "laptop", "price": 52000, "in_stock": True, "shipping_cost": 0},
    {"id": "a2", "name": "AeroBook 14 (i5, 16GB)", "category": "laptop", "price": 58500, "in_stock": True, "shipping_cost": 0},
    {"id": "a3", "name": "NovaLite 15 (i3, 8GB)", "category": "laptop", "price": 41000, "in_stock": False, "shipping_cost": 0},
    {"id": "a4", "name": "PixelWave Phone 12", "category": "phone", "price": 27500, "in_stock": True, "shipping_cost": 0},
    {"id": "a5", "name": "EchoBuds Pro", "category": "headphone", "price": 3200, "in_stock": True, "shipping_cost": 0},
    {"id": "a6", "name": "PulseFit Smartwatch", "category": "watch", "price": 6200, "in_stock": True, "shipping_cost": 0},
]


@app.get("/search")
def search(query: str):
    """Keyword search — matches product name substring OR exact category."""
    results = []
    q = query.lower()
    for item in FAKE_INVENTORY:
        category_match = q == item.get("category", "").lower()
        name_match = q in item["name"].lower()
        if category_match or name_match:
            item_without_category = {k: v for k, v in item.items() if k != "category"}
            product = Product(
                **item_without_category,
                store="Store A - TechBazaar",
                last_updated=datetime.utcnow() - timedelta(minutes=5),
            )
            results.append(product)
    return results


@app.get("/health")
def health():
    return {"status": "ok", "store": "Store A - TechBazaar"}