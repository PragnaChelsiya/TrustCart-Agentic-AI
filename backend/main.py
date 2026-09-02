"""
TrustCart main API — ties everything together into one endpoint.

GET /find-best-deal?query=laptop&budget=60000

Returns: all offers found, the winning pick, its confidence score,
and a structured audit log explaining the decision.
"""

import sys, os
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

from agents.planner import fetch_all_offers, pick_best_deal, STORE_ENDPOINTS
from utils.confidence import compute_confidence

app = FastAPI(title="TrustCart API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/find-best-deal")
def find_best_deal(query: str, budget: float | None = None):
    audit_log = []

    audit_log.append({
        "step": "search",
        "detail": f"Searching {len(STORE_ENDPOINTS)} store(s) for '{query}'",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    offers = fetch_all_offers(query)
    audit_log.append({
        "step": "offers_found",
        "detail": f"Found {len(offers)} matching offer(s) across all reachable stores",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    if budget is not None:
        audit_log.append({
            "step": "budget_filter",
            "detail": f"Filtering to offers within budget ₹{budget}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    best = pick_best_deal(offers, budget=budget)

    if not best:
        audit_log.append({
            "step": "no_result",
            "detail": "No in-stock offer found within budget",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return {
            "query": query,
            "budget": budget,
            "offers": [o.model_dump() for o in offers],
            "winner": None,
            "confidence": None,
            "audit_log": audit_log,
        }

    confidence = compute_confidence(best, offers, stores_reached=len(STORE_ENDPOINTS))

    audit_log.append({
        "step": "decision",
        "detail": f"Selected '{best.name}' from {best.store} at total cost ₹{best.total_cost}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    return {
        "query": query,
        "budget": budget,
        "offers": [o.model_dump() for o in offers],
        "winner": best.model_dump(),
        "confidence": confidence,
        "audit_log": audit_log,
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "TrustCart API"}