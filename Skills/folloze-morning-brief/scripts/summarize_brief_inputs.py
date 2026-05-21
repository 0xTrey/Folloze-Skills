#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Any


INTERNAL_DOMAIN = "folloze.com"
ADMIN_TITLE_MARKERS = (
    "working location",
    "ooo",
    "out of office",
    "reclaim",
    "focus",
    "gym",
    "hold",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize exported calendar, opportunity, and task inputs for the Folloze morning brief.",
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="JSON input file. Reads stdin when omitted.",
    )
    parser.add_argument(
        "--today",
        default=date.today().isoformat(),
        help="Local date for close-date and stale-activity calculations.",
    )
    return parser.parse_args()


def load_payload(path: str | None) -> dict[str, Any]:
    if path:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.load(sys.stdin)


def parse_date(value: Any) -> date | None:
    if not value:
        return None
    if isinstance(value, date):
        return value
    text = str(value)
    if "T" in text:
        text = text.split("T", 1)[0]
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def parse_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    text = str(value).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def attendee_email(attendee: Any) -> str:
    if isinstance(attendee, str):
        return attendee.lower()
    if isinstance(attendee, dict):
        return str(attendee.get("email") or attendee.get("address") or "").lower()
    return ""


def is_external_event(event: dict[str, Any]) -> bool:
    title = str(event.get("title") or event.get("summary") or "").lower()
    if any(marker in title for marker in ADMIN_TITLE_MARKERS):
        return False
    attendees = event.get("attendees") or []
    emails = [attendee_email(item) for item in attendees]
    return any(email and not email.endswith(f"@{INTERNAL_DOMAIN}") for email in emails)


def event_sort_key(event: dict[str, Any]) -> str:
    start = event.get("start") or event.get("start_time") or event.get("dateTime")
    parsed = parse_datetime(start)
    return parsed.isoformat() if parsed else str(start or "")


def summarize_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    external = [event for event in events if is_external_event(event)]
    return {
        "total_events": len(events),
        "external_events": sorted(external, key=event_sort_key),
        "filtered_events": len(events) - len(external),
    }


def summarize_opportunities(
    opportunities: list[dict[str, Any]],
    today: date,
) -> dict[str, Any]:
    by_account: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for opportunity in opportunities:
        account = (
            opportunity.get("account_name")
            or opportunity.get("AccountName")
            or opportunity.get("account")
            or "Unmapped account"
        )
        by_account[str(account)].append(opportunity)

    accounts: list[dict[str, Any]] = []
    stale_before = today - timedelta(days=14)
    close_before = today + timedelta(days=30)

    for account, items in by_account.items():
        near_term = []
        stale = []
        total_amount = 0.0
        for item in items:
            amount = item.get("amount") or item.get("Amount") or 0
            try:
                total_amount += float(amount)
            except (TypeError, ValueError):
                pass

            close_date = parse_date(item.get("close_date") or item.get("CloseDate"))
            if close_date and today <= close_date <= close_before:
                near_term.append(item)

            last_activity = parse_date(item.get("last_activity_date") or item.get("LastActivityDate"))
            if last_activity and last_activity < stale_before:
                stale.append(item)

        accounts.append(
            {
                "account": account,
                "opportunity_count": len(items),
                "total_amount": total_amount,
                "near_term_count": len(near_term),
                "stale_activity_count": len(stale),
                "opportunities": items,
            }
        )

    accounts.sort(
        key=lambda item: (
            item["near_term_count"],
            item["stale_activity_count"],
            item["total_amount"],
            item["opportunity_count"],
        ),
        reverse=True,
    )
    return {
        "opportunity_count": len(opportunities),
        "account_count": len(accounts),
        "accounts": accounts,
    }


def summarize_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    open_tasks = []
    for task in tasks:
        status = str(task.get("status") or "").lower()
        completed = bool(task.get("completed"))
        if completed or status in {"done", "complete", "completed", "closed"}:
            continue
        open_tasks.append(task)
    return {
        "task_count": len(tasks),
        "open_task_count": len(open_tasks),
        "open_tasks": open_tasks,
    }


def main() -> int:
    args = parse_args()
    payload = load_payload(args.input)
    today = parse_date(args.today) or date.today()

    result = {
        "today": today.isoformat(),
        "calendar": summarize_events(payload.get("calendar_events", [])),
        "pipeline": summarize_opportunities(payload.get("opportunities", []), today),
        "tasks": summarize_tasks(payload.get("tasks", [])),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
