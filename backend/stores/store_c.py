"""
Mock Store C — a third pretend electronics store, for a fuller comparison.
Run standalone with: uvicorn store_c:app --port 8003
"""

from fastapi import FastAPI
from datetime import datetime, timedelta
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from models.product import Product

app = FastAPI(title="Store C - ByteMart")

FAKE_INVENTORY = [
    {"id": "c1", "name": "AeroBook 14 (i5, 8GB)", "category": "laptop", "price": 51500, "in_stock": True, "shipping_cost": 400},
    {"id": "c2", "name": "AeroBook 14 (i5, 16GB)", "category": "laptop", "price": 59200, "in_stock": False, "shipping_cost": 400},
    {"id": "c3", "name": "NovaLite 15 (i3, 8GB)", "category": "laptop", "price": 40200, "in_stock": True, "shipping_cost": 400},
    {"id": "c4", "name": "Pulsar X12 5G Smartphone", "category": "phone", "price": 25499, "in_stock": True, "shipping_cost": 400},
    {"id": "c5", "name": "Pulsar X12 Pro Smartphone", "category": "phone", "price": 30999, "in_stock": True, "shipping_cost": 400},
    {"id": "c6", "name": "OrbitFit S2 Smartwatch", "category": "smartwatch", "price": 4599, "in_stock": True, "shipping_cost": 400},
    {"id": "c7", "name": "EchoBuds Pro Wireless Earbuds", "category": "headphones", "price": 2999, "in_stock": True, "shipping_cost": 400},
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
            product = Product(
                **item,
                store="Store C - ByteMart",
                last_updated=datetime.utcnow() - timedelta(minutes=8),
            )
            results.append(product)
    return results


@app.get("/health")
def health():
    return {"status": "ok", "store": "Store C - ByteMart"}