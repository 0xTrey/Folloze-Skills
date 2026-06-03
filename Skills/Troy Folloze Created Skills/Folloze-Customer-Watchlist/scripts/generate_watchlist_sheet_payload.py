#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_SKILL_DIR = Path(__file__).resolve().parents[1]
HEADER = [
    "run_date",
    "section",
    "account_id",
    "account_name",
    "type",
    "csm_name",
    "event_date",
    "day_offset",
]


class ScriptError(RuntimeError):
    pass


def run_helper(skill_dir: Path, org: str, as_of: str | None) -> dict:
    cmd = [
        "python3",
        str(skill_dir / "scripts" / "folloze_customer_watchlist.py"),
        "--org",
        org,
        "--json",
    ]
    if as_of:
        cmd.extend(["--as-of", as_of])
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise ScriptError(proc.stderr.strip() or proc.stdout.strip() or "watchlist helper failed")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise ScriptError("watchlist helper returned invalid JSON") from exc


def build_rows(payload: dict) -> list[list[str]]:
    run_date = payload["as_of"]
    rows: list[list[str]] = []
    for item in payload.get("recently_started", []):
        rows.append(
            [
                run_date,
                "recent_start",
                item["account_id"],
                item["account_name"],
                item.get("type") or "",
                item.get("csm_name") or "",
                item["contract_start_date"],
                str(item["days_since_start"]),
            ]
        )
    for item in payload.get("upcoming_renewals", []):
        rows.append(
            [
                run_date,
                "upcoming_renewal",
                item["account_id"],
                item["account_name"],
                item.get("type") or "",
                item.get("csm_name") or "",
                item["contract_renewal_date"],
                str(item["days_to_renewal"]),
            ]
        )
    return rows


def to_tsv(rows: list[list[str]], include_header: bool) -> str:
    body = []
    if include_header:
        body.append("\t".join(HEADER))
    body.extend("\t".join(row) for row in rows)
    return "\n".join(body)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate exact Google Sheets payloads for the Folloze customer watchlist.")
    parser.add_argument("--skill-dir", default=str(DEFAULT_SKILL_DIR))
    parser.add_argument("--org", default="folloze-prod")
    parser.add_argument("--as-of", default=None)
    parser.add_argument("--out-dir", default=None)
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir)
    out_dir = Path(args.out_dir) if args.out_dir else skill_dir / "runs"
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = run_helper(skill_dir, args.org, args.as_of)
    rows = build_rows(payload)

    summary = {
        "as_of": payload["as_of"],
        "recently_started_count": len(payload.get("recently_started", [])),
        "upcoming_renewals_count": len(payload.get("upcoming_renewals", [])),
        "history_append_tsv_path": str(out_dir / "history_append.tsv"),
        "snapshot_tsv_path": str(out_dir / "snapshot.tsv"),
        "rows_json_path": str(out_dir / "watchlist_rows.json"),
    }

    (out_dir / "watchlist_rows.json").write_text(json.dumps({"header": HEADER, "rows": rows}, indent=2) + "\n", encoding="utf-8")
    (out_dir / "history_append.tsv").write_text(to_tsv(rows, include_header=False) + ("\n" if rows else ""), encoding="utf-8")
    (out_dir / "snapshot.tsv").write_text(to_tsv(rows, include_header=True) + ("\n" if rows else "\n"), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ScriptError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
