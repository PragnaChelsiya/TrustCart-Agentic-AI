# TrustCart — Agentic AI Shopping Assistant

TrustCart is an agentic shopping assistant that finds the best deal across multiple stores —
and shows exactly *why* it trusts the pick, with a real computed confidence score and a full
decision audit trail. Built as a demonstration of the "trust layer" agentic commerce systems
need but rarely show.

## Why this exists

Most agentic commerce demos show an AI completing a purchase, but skip the harder question:
**how does the user know the agent made a good decision?** TrustCart treats that as the core
product problem, not an afterthought. Every recommendation comes with:

- A **confidence score** computed from real signals (price competitiveness, data freshness,
  sample size) — not an LLM guessing a number
- A **structured audit log** showing every step the agent took and why
- Full transparency into every offer that was compared, not just the winner

## Features

- Multi-store price comparison across 3 independent mock merchant APIs
- Multi-category support: laptops, phones, smartwatches, and earbuds
- Real-time confidence scoring with a transparent, weighted formula
- Structured, timestamped decision audit trail
- Animated "agent reasoning" console showing the agent's steps live
- Interactive dark UI with a live confidence gauge, sortable comparison table, and
  expandable audit steps

## Architecture
trustcart/
├── backend/
│ ├── agents/
│ │ └── planner.py # Queries all stores, picks best deal within budget
│ ├── stores/
│ │ ├── store_a.py # Mock merchant API — TechBazaar
│ │ ├── store_b.py # Mock merchant API — GadgetHub
│ │ └── store_c.py # Mock merchant API — ByteMart
│ ├── models/
│ │ └── product.py # Shared Product data model
│ ├── utils/
│ │ └── confidence.py # Confidence scoring logic
│ └── main.py # Unified FastAPI endpoint tying it all together
└── frontend/
└── index.html # Interactive UI (no framework — vanilla HTML/CSS/JS)


### How the confidence score works

The overall score (0–100) is a weighted combination of three factors:

| Factor | Weight | What it measures |
|---|---|---|
| Price competitiveness | 50% | How much cheaper the winner is vs. the next-best offer |
| Data freshness | 25% | How recently the price was checked |
| Sample size | 25% | How many stores/offers were compared |

This keeps the score explainable — every number in the breakdown traces back to a concrete,
inspectable reason, shown directly in the UI.

## Running locally

You'll need Python 3.10+ and `pip`.

```bash
pip install fastapi uvicorn pydantic httpx
```

Start each service in its own terminal:

```bash
# Terminal 1
cd backend/stores && uvicorn store_a:app --port 8001 --reload

# Terminal 2
cd backend/stores && uvicorn store_b:app --port 8002 --reload

# Terminal 3
cd backend/stores && uvicorn store_c:app --port 8003 --reload

# Terminal 4
cd backend && uvicorn main:app --port 8000 --reload

# Terminal 5
cd frontend && python -m http.server 5500
```

Then open `http://localhost:5500/index.html` in your browser.

## API

**`GET /find-best-deal?query=laptop&budget=60000`**

Returns the winning offer, its confidence score with a full breakdown, every offer that was
compared, and a timestamped audit log of the decision process.

## What's next

- Natural-language query understanding via an LLM layer, so requests aren't limited to exact
  keyword matches
- Human-in-the-loop approval flow for purchases above a configurable spend threshold
- Real merchant API integrations in place of the mock stores
- Persistent purchase history and preference-aware recommendations via RAG

## Built by

Pragna Chelsiya — built as part of an internship project submission.
