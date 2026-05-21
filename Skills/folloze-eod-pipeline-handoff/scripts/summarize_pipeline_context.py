#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


STALE_ACTIVITY_DAYS = 21
NEAR_CLOSE_DAYS = 14
HIGH_VALUE_AMOUNT = 50000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize legacy Folloze pipeline context into compact risk candidates.",
    )
    parser.add_argument(
        "--deal-index",
        type=Path,
        default=None,
        help="Optional path to a legacy deal-index JSON file.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=7,
        help="Maximum risks to return.",
    )
    parser.add_argument(
        "--today",
        default=None,
        help="Override today's date as YYYY-MM-DD for deterministic tests.",
    )
    return parser.parse_args()


def parse_date(value: Any) -> date | None:
    if not value:
        return None
    text = str(value).strip()
    if not text:
        return None
    for candidate in (text[:10], text):
        try:
            return date.fromisoformat(candidate)
        except ValueError:
            continue
    return None


def parse_amount(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(str(value).replace(",", "").replace("$", ""))
    except ValueError:
        return None


def load_json(path: Path) -> dict[str, Any]:
    with path.expanduser().open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"Expected JSON object in {path}")
    return data


def iter_deals(data: dict[str, Any]) -> list[dict[str, Any]]:
    raw = data.get("deals", data)
    if isinstance(raw, dict):
        values = raw.values()
    elif isinstance(raw, list):
        values = raw
    else:
        return []
    return [deal for deal in values if isinstance(deal, dict)]


def deal_name(deal: dict[str, Any]) -> str:
    return str(
        deal.get("name")
        or deal.get("opportunity_name")
        or deal.get("sf_opportunity_name")
        or deal.get("title")
        or "Unknown opportunity"
    )


def account_name(deal: dict[str, Any]) -> str:
    return str(
        deal.get("account")
        or deal.get("account_name")
        or deal.get("company")
        or deal.get("domain")
        or "Unknown account"
    )


def is_active(deal: dict[str, Any]) -> bool:
    status = str(deal.get("status") or "").lower()
    stage = str(deal.get("sf_stage") or deal.get("stage") or "").lower()
    closed_markers = ("closed lost", "closed won", "lost", "won", "inactive", "archived")
    return not any(marker in status or marker in stage for marker in closed_markers)


def risk_for_deal(deal: dict[str, Any], today: date) -> dict[str, Any] | None:
    close_date = parse_date(deal.get("sf_close_date") or deal.get("close_date"))
    last_activity = parse_date(deal.get("sf_last_activity") or deal.get("last_activity"))
    amount = parse_amount(deal.get("sf_amount") or deal.get("amount"))
    stage = str(deal.get("sf_stage") or deal.get("stage") or "")
    forecast = str(deal.get("sf_forecast_category") or deal.get("forecast_category") or "")
    next_step = str(deal.get("next_step") or deal.get("sf_next_step") or "").strip()

    score = 0
    reasons: list[str] = []

    if close_date:
        days_to_close = (close_date - today).days
        if days_to_close < 0:
            score += 70
            reasons.append(f"close date passed {abs(days_to_close)} days ago")
        elif days_to_close <= 7:
            score += 55
            reasons.append(f"close date in {days_to_close} days")
        elif days_to_close <= NEAR_CLOSE_DAYS:
            score += 35
            reasons.append(f"close date in {days_to_close} days")

    if last_activity:
        stale_days = (today - last_activity).days
        if stale_days >= STALE_ACTIVITY_DAYS:
            score += 30
            reasons.append(f"no Salesforce activity in {stale_days} days")
    else:
        score += 20
        reasons.append("missing last activity date")

    stage_lower = stage.lower()
    if any(term in stage_lower for term in ("proposal", "solution", "validation", "discovery", "meeting booked")):
        score += 15
        reasons.append(f"stage is {stage or 'unknown'}")

    forecast_lower = forecast.lower()
    if forecast_lower in {"bestcase", "best case", "commit"}:
        score += 15
        reasons.append(f"forecast is {forecast}")

    if amount and amount >= HIGH_VALUE_AMOUNT:
        score += 10
        reasons.append(f"amount is {amount:,.0f}")

    if not next_step:
        score += 20
        reasons.append("missing next step")

    if score == 0:
        return None

    return {
        "account": account_name(deal),
        "opportunity": deal_name(deal),
        "score": score,
        "stage": stage or None,
        "amount": amount,
        "close_date": close_date.isoformat() if close_date else None,
        "last_activity": last_activity.isoformat() if last_activity else None,
        "forecast_category": forecast or None,
        "risk_reason": "; ".join(reasons[:4]),
        "recommended_action": "Confirm owner, next step, and customer timeline.",
        "confidence": "medium",
        "freshness": str(deal.get("sf_synced_at") or deal.get("updated_at") or "local fallback data"),
    }


def summarize(deal_index: Path | None, limit: int, today: date) -> dict[str, Any]:
    if not deal_index:
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source": None,
            "active_deals": 0,
            "salesforce_linked_deals": 0,
            "top_risks": [],
            "caveats": ["No deal-index path provided."],
        }

    data = load_json(deal_index)
    deals = iter_deals(data)
    active = [deal for deal in deals if is_active(deal)]
    linked = [deal for deal in active if deal.get("sf_opportunity_id")]
    risks = [risk for deal in active if (risk := risk_for_deal(deal, today))]
    risks.sort(key=lambda item: item["score"], reverse=True)

    caveats: list[str] = []
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    if metadata:
        updated = metadata.get("updated_at") or metadata.get("generated_at")
        if updated:
            caveats.append(f"Deal-index metadata timestamp: {updated}")

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(deal_index.expanduser()),
        "active_deals": len(active),
        "salesforce_linked_deals": len(linked),
        "top_risks": risks[: max(0, limit)],
        "caveats": caveats,
    }


def main() -> int:
    args = parse_args()
    today = parse_date(args.today) if args.today else date.today()
    if not today:
        raise SystemExit("--today must be YYYY-MM-DD")
    print(json.dumps(summarize(args.deal_index, args.limit, today), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
