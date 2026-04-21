#!/usr/bin/env python3

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from typing import Iterable, List

import requests


DEFAULT_FORM_URL = (
    "https://docs.google.com/forms/d/e/1FAIpQLSehvz2GwGYX3gdOmgKkIyVEdB8d0rLWYgwfwRX4dnl33Zdxww/viewform"
)

CLIENT_TYPES = {
    "direct customer": "Direct Customer",
    "agency": "Agency",
    "agency customer": "Agency Customer",
    "oem customer": "OEM Customer",
}

PLAN_KEYWORDS = {
    "premium": "Premium",
    "agency customer": "Agency Customer",
    "starter": "Professional",
    "professional": "Professional",
    "pro": "Professional",
}

INTEGRATION_OPTIONS = {
    "none": "None",
    "demandbase": "Demandbase",
    "6sense": "6Sense",
    "marketo": "Marketo",
    "eloqua": "Eloqua",
    "salesforce": "Salesforce",
    "ms dynamics": "MS Dynamics",
    "sso": "SSO",
    "advanced cookie settings": "Advanced Cookie Settings",
    "live events purchased": "Live Events purchased",
    "hubspot": "Hubspot",
}


@dataclass
class HiddenFormFields:
    action_url: str
    fbzx: str
    partial_response: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Submit the Folloze New Client Org Request v2 Google Form."
    )
    parser.add_argument("--form-url", default=DEFAULT_FORM_URL)
    parser.add_argument("--work-email", required=True)
    parser.add_argument("--client-domain", required=True)
    parser.add_argument("--client-type", default="Direct Customer")
    parser.add_argument("--plan", default="Professional")
    parser.add_argument(
        "--launch-date",
        required=True,
        help="Launch date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--admin-user",
        action="append",
        default=[],
        help="Confirmed admin user email. Repeat for multiple users.",
    )
    parser.add_argument(
        "--non-admin-user",
        action="append",
        default=[],
        help="Confirmed non-admin user email. Repeat for multiple users.",
    )
    parser.add_argument(
        "--custom-subdomain",
        default="yes",
        choices=["yes", "no", "Yes", "No"],
    )
    parser.add_argument("--subdomain-value", default="")
    parser.add_argument(
        "--integration",
        action="append",
        default=[],
        help="Integration value. Repeat for multiple integrations.",
    )
    parser.add_argument(
        "--cc",
        action="append",
        default=[],
        help="Email to CC on the form response. Repeat for multiple recipients.",
    )
    parser.add_argument("--creator-licenses", required=True, type=int)
    parser.add_argument("--collaborators", required=True, type=int)
    parser.add_argument("--details", default="")
    parser.add_argument("--details-file", default="")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the normalized payload without submitting the form.",
    )
    return parser.parse_args()


def load_details(args: argparse.Namespace) -> str:
    if args.details and args.details_file:
        raise SystemExit("Pass either --details or --details-file, not both.")
    if args.details_file:
        with open(args.details_file, "r", encoding="utf-8") as handle:
            return handle.read().strip()
    return args.details.strip()


def normalize_client_type(value: str) -> str:
    key = value.strip().lower()
    if key in CLIENT_TYPES:
        return CLIENT_TYPES[key]
    raise SystemExit(f"Unsupported client type: {value!r}")


def normalize_plan(value: str) -> str:
    key = value.strip().lower()
    for pattern, normalized in PLAN_KEYWORDS.items():
        if pattern in key:
            return normalized
    return "Professional"


def normalize_integrations(values: Iterable[str]) -> List[str]:
    if not values:
        return ["None"]

    normalized: List[str] = []
    for value in values:
        key = value.strip().lower()
        if key not in INTEGRATION_OPTIONS:
            raise SystemExit(f"Unsupported integration option: {value!r}")
        normalized.append(INTEGRATION_OPTIONS[key])

    deduped = list(dict.fromkeys(normalized))
    if "None" in deduped and len(deduped) > 1:
        raise SystemExit("Do not combine 'None' with other integration options.")
    return deduped


def join_lines(values: Iterable[str]) -> str:
    return "\n".join(v.strip() for v in values if v.strip())


def fetch_hidden_fields(session: requests.Session, form_url: str) -> HiddenFormFields:
    response = session.get(form_url, timeout=30)
    response.raise_for_status()
    text = response.text

    fbzx_match = re.search(r'name="fbzx" value="([^"]+)"', text)
    partial_match = re.search(r'name="partialResponse" value="([^"]+)"', text)
    action_match = re.search(r'<form[^>]+action="([^"]+)"', text)

    if not fbzx_match or not partial_match or not action_match:
        raise SystemExit("Could not parse the Google Form hidden fields.")

    return HiddenFormFields(
        action_url=html.unescape(action_match.group(1)),
        fbzx=fbzx_match.group(1),
        partial_response=html.unescape(partial_match.group(1)),
    )


def build_payload(args: argparse.Namespace, hidden: HiddenFormFields) -> List[tuple]:
    launch_date = date.fromisoformat(args.launch_date)
    subdomain_answer = "Yes" if args.custom_subdomain.lower() == "yes" else "No"
    subdomain_value = args.subdomain_value.strip()
    if subdomain_answer == "Yes" and not subdomain_value:
        subdomain_value = "TBD"

    details = load_details(args)

    payload: List[tuple] = [
        ("entry.1647054609", args.work_email.strip()),
        ("entry.784997538", args.client_domain.strip()),
        ("entry.653536717", normalize_client_type(args.client_type)),
        ("entry.1166270677", normalize_plan(args.plan)),
        ("entry.851012498_month", f"{launch_date.month:02d}"),
        ("entry.851012498_day", f"{launch_date.day:02d}"),
        ("entry.851012498_year", f"{launch_date.year:04d}"),
        ("entry.1447814038", join_lines(args.admin_user)),
        ("entry.869798197", join_lines(args.non_admin_user)),
        ("entry.2054741714", subdomain_answer),
        ("entry.298855314", subdomain_value),
        ("entry.1331947512", join_lines(args.cc)),
        ("entry.1688581247", str(args.creator_licenses)),
        ("entry.1422600127", str(args.collaborators)),
        ("entry.1859564084", details),
        ("fvv", "1"),
        ("draftResponse", "[]"),
        ("pageHistory", "0"),
        ("fbzx", hidden.fbzx),
        ("partialResponse", hidden.partial_response),
        ("submissionTimestamp", "-1"),
    ]

    for integration in normalize_integrations(args.integration):
        payload.append(("entry.541351615", integration))

    return payload


def summarize_payload(payload: List[tuple]) -> dict:
    summary = {}
    for key, value in payload:
        if key.startswith("entry.") and key not in summary:
            summary[key] = []
        if key.startswith("entry."):
            summary[key].append(value)
    return summary


def submit_form(
    session: requests.Session,
    hidden: HiddenFormFields,
    payload: List[tuple],
    referer: str,
) -> requests.Response:
    response = session.post(
        hidden.action_url,
        data=payload,
        headers={"Referer": referer},
        allow_redirects=True,
        timeout=30,
    )
    response.raise_for_status()
    return response


def main() -> int:
    args = parse_args()
    session = requests.Session()
    hidden = fetch_hidden_fields(session, args.form_url)
    payload = build_payload(args, hidden)

    print(
        json.dumps(
            {
                "form_url": args.form_url,
                "action_url": hidden.action_url,
                "payload": summarize_payload(payload),
                "dry_run": args.dry_run,
            },
            indent=2,
            sort_keys=True,
        )
    )

    if args.dry_run:
        return 0

    response = submit_form(session, hidden, payload, args.form_url)
    if "Your response has been recorded" not in response.text:
        print(response.text[:4000], file=sys.stderr)
        raise SystemExit("Form submission did not reach the recorded-response page.")

    print("SUCCESS: form submission recorded.")
    print(response.url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
