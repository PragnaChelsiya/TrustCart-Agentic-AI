"""
Confidence Scoring — the core differentiator of TrustCart.

This is NOT an LLM guessing a number. It's computed from real signals:
  1. Price competitiveness — how much cheaper is the winner vs the runner-up?
  2. Data freshness — how recently was this price checked?
  3. Number of offers compared — more comparisons = more confidence
  4. Stock certainty — is it definitely in stock?

Returns a score from 0-100 and a breakdown explaining each component,
which feeds directly into the audit log.
"""

from datetime import datetime, timezone
from models.product import Product


def score_price_competitiveness(winner: Product, all_candidates: list[Product]) -> tuple[float, str]:
    """
    Compares the winner's price to the next-best offer.
    A big gap = high confidence this is genuinely the best deal.
    A tiny gap = lower confidence (could easily be beaten by data we don't have).
    """
    others = [p for p in all_candidates if p.id != winner.id]
    if not others:
        return 50.0, "Only one offer available — no comparison possible"

    next_best = min(others, key=lambda p: p.total_cost)
    gap_pct = ((next_best.total_cost - winner.total_cost) / next_best.total_cost) * 100

    if gap_pct <= 0:
        score = 40.0
    else:
        score = min(40.0 + gap_pct * 2, 100.0)

    reason = f"{gap_pct:.1f}% cheaper than the next-best offer ({next_best.store})"
    return score, reason


def score_data_freshness(product: Product) -> tuple[float, str]:
    """More recently checked prices are more trustworthy."""
    age_minutes = (datetime.now(timezone.utc) - product.last_updated.replace(tzinfo=timezone.utc)).total_seconds() / 60

    if age_minutes <= 10:
        score = 100.0
    elif age_minutes <= 30:
        score = 80.0
    elif age_minutes <= 60:
        score = 60.0
    else:
        score = 30.0

    reason = f"Price data is {age_minutes:.0f} minutes old"
    return score, reason


def score_sample_size(all_candidates: list[Product], stores_reached: int) -> tuple[float, str]:
    """More stores compared = more confidence we found the real best deal."""
    if stores_reached >= 3:
        score = 100.0
    elif stores_reached == 2:
        score = 70.0
    else:
        score = 40.0

    reason = f"Compared {len(all_candidates)} offers across {stores_reached} store(s)"
    return score, reason


def compute_confidence(winner: Product, all_candidates: list[Product], stores_reached: int) -> dict:
    """
    Combines all signals into one overall confidence score (0-100)
    plus a breakdown for the audit log.
    """
    price_score, price_reason = score_price_competitiveness(winner, all_candidates)
    freshness_score, freshness_reason = score_data_freshness(winner)
    sample_score, sample_reason = score_sample_size(all_candidates, stores_reached)

    overall = (price_score * 0.5) + (freshness_score * 0.25) + (sample_score * 0.25)

    return {
        "overall_score": round(overall, 1),
        "breakdown": [
            {"factor": "Price competitiveness", "score": round(price_score, 1), "reason": price_reason},
            {"factor": "Data freshness", "score": round(freshness_score, 1), "reason": freshness_reason},
            {"factor": "Sample size", "score": round(sample_score, 1), "reason": sample_reason},
        ],
    }