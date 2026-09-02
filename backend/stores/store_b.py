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

# Different prices/stock than Store A — this is what makes comparison meaningful.
FAKE_INVENTORY = [
    {"id": "b1", "name": "AeroBook 14 (i5, 8GB)", "price": 53500, "in_stock": True, "shipping_cost": 250},
    {"id": "b2", "name": "AeroBook 14 (i5, 16GB)", "price": 57000, "in_stock": True, "shipping_cost": 250},
    {"id": "b3", "name": "NovaLite 15 (i3, 8GB)", "price": 39500, "in_stock": True, "shipping_cost": 250},
]


@app.get("/search")
def search(query: str):
    results = []
    for item in FAKE_INVENTORY:
        if query.lower() in item["name"].lower() or query.lower() in "laptop":
            product = Product(
                **item,
                store="Store B - GadgetHub",
                last_updated=datetime.utcnow() - timedelta(minutes=20),  # slightly staler than Store A
            )
            results.append(product)
    return results


@app.get("/health")
def health():
    return {"status": "ok", "store": "Store B - GadgetHub"}