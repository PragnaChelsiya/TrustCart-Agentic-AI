"""
Mock Store B — a second pretend electronics store, for price comparison.
Run standalone with: uvicorn store_b:app --port 8002
"""

from fastapi import FastAPI
from datetime import datetime, timedelta
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from models.product import Product

app = FastAPI(title="Store B - GadgetHub")

FAKE_INVENTORY = [
    {"id": "b1", "name": "AeroBook 14 (i5, 8GB)", "category": "laptop", "price": 53500, "in_stock": True, "shipping_cost": 250},
    {"id": "b2", "name": "AeroBook 14 (i5, 16GB)", "category": "laptop", "price": 57000, "in_stock": True, "shipping_cost": 250},
    {"id": "b3", "name": "NovaLite 15 (i3, 8GB)", "category": "laptop", "price": 39500, "in_stock": True, "shipping_cost": 250},
    {"id": "b4", "name": "PixelWave Phone 12", "category": "phone", "price": 28900, "in_stock": True, "shipping_cost": 250},
    {"id": "b5", "name": "EchoBuds Pro", "category": "headphone", "price": 3450, "in_stock": True, "shipping_cost": 250},
    {"id": "b6", "name": "PulseFit Smartwatch", "category": "watch", "price": 6800, "in_stock": True, "shipping_cost": 250},
]


@app.get("/search")
def search(query: str):
    results = []
    for item in FAKE_INVENTORY:
        if query.lower() in item["category"].lower():
            item_without_category = {k: v for k, v in item.items() if k != "category"}
            product = Product(
                **item_without_category,
                store="Store B - GadgetHub",
                last_updated=datetime.utcnow() - timedelta(minutes=20),
            )
            results.append(product)
    return results


@app.get("/health")
def health():
    return {"status": "ok", "store": "Store B - GadgetHub"}