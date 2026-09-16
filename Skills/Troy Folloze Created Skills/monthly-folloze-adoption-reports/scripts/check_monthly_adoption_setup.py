#!/usr/bin/env python3
import json
import os
from pathlib import Path


ROOT = Path(os.environ.get("FOLLOZE_ADOPTION_WORKSPACE", Path.home() / "Documents/Playground")).expanduser()
AUTOMATION = Path(
    os.environ.get(
        "FOLLOZE_ADOPTION_AUTOMATION_TOML",
        Path.home() / ".codex/automations/monthly-folloze-adoption-reports-to-customer-slack-channels/automation.toml",
    )
).expanduser()
REQUIRED = [
    ROOT / "batch_adoption_reports.py",
    ROOT / "create_slack_posting_manifest.py",
    AUTOMATION,
]
EXCLUDED = {"Box", "Infinite Edge Consulting"}
SPOT_CHECKS = {"Workday", "Autodesk", "Oracle", "Schoox", "Capgemini", "TELUS", "Schlumberger"}


def latest_manifest(name):
    candidates = sorted(
        (p for p in (ROOT / "output/pdf").glob("monthly_adoption*") if (p / name).exists()),
        key=lambda p: (p / name).stat().st_mtime,
        reverse=True,
    )
    return candidates[0] / name if candidates else None


def main():
    missing = [str(p) for p in REQUIRED if not p.exists()]
    manifest_path = latest_manifest("manifest.json")
    slack_path = latest_manifest("slack_posting_manifest.json")
    result = {"missing_required_files": missing}

    if manifest_path:
        manifest = json.load(open(manifest_path))
        generated = {item["account"] for item in manifest.get("generated", [])}
        result["latest_manifest"] = str(manifest_path)
        result["generated_count"] = len(generated)
        result["excluded_present"] = sorted(generated & EXCLUDED)
        result["spot_checks_missing_from_generated"] = sorted(SPOT_CHECKS - generated)
        result["window"] = manifest.get("window")

    if slack_path:
        slack = json.load(open(slack_path))
        posted = {item["account"] for item in slack.get("posts", [])}
        result["latest_slack_manifest"] = str(slack_path)
        result["post_count"] = len(posted)
        result["unmatched_count"] = len(slack.get("unmatched", []))
        result["spot_checks_missing_from_posts"] = sorted(SPOT_CHECKS - posted)

    automation_text = AUTOMATION.read_text() if AUTOMATION.exists() else ""
    result["automation_active"] = 'status = "ACTIVE"' in automation_text
    result["automation_first_of_month_9am"] = "FREQ=MONTHLY;BYMONTHDAY=1;BYHOUR=9;BYMINUTE=0;BYSECOND=0" in automation_text
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
