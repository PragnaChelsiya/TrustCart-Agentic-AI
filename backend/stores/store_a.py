"""
Mock Store A — pretend electronics store.
This simulates a real merchant API so you don't need real e-commerce integration.
Run standalone with: uvicorn store_a:app --port 8001
"""

from fastapi import FastAPI
from datetime import datetime, timedelta
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from models.product import Product

app = FastAPI(title="Store A - TechBazaar")

# Fake inventory. In a real build you'd load this from a DB.
FAKE_INVENTORY = [
    {"id": "a1", "name": "AeroBook 14 (i5, 8GB)", "price": 52000, "in_stock": True, "shipping_cost": 0},
    {"id": "a2", "name": "AeroBook 14 (i5, 16GB)", "price": 58500, "in_stock": True, "shipping_cost": 0},
    {"id": "a3", "name": "NovaLite 15 (i3, 8GB)", "price": 41000, "in_stock": False, "shipping_cost": 0},
]


@app.get("/search")
def search(query: str):
    """Very basic keyword search over fake inventory."""
    results = []
    for item in FAKE_INVENTORY:
        if query.lower() in item["name"].lower() or query.lower() in "laptop":
            product = Product(
                **item,
                store="Store A - TechBazaar",
                last_updated=datetime.utcnow() - timedelta(minutes=5),  # fake freshness
            )
            results.append(product)
    return results


@app.get("/health")
def health():
    return {"status": "ok", "store": "Store A - TechBazaar"}