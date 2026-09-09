#!/usr/bin/env python3
import argparse
import html
import re
from pathlib import Path


DEFAULT_TEMPLATE = Path(__file__).resolve().parents[1] / "assets" / "renewal-board-template.html"


def slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "customer"


def render(template_text, values):
    rendered = template_text
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", html.escape(value, quote=False))
    missing = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", rendered)))
    if missing:
        raise SystemExit("Missing placeholder values: " + ", ".join(missing))
    return rendered


def main():
    parser = argparse.ArgumentParser(description="Generate a Folloze renewal board HTML file from the customer template.")
    parser.add_argument("--customer-name", required=True, help="Customer account name to show throughout the board.")
    parser.add_argument("--current-use-cases", default="events and ABM", help="Current Folloze footprint, such as 'events and ABM'.")
    parser.add_argument("--customer-segment", default="customer growth", help="Segment or audience label for the cockpit, such as 'enterprise renewal'.")
    parser.add_argument("--customer-value-story", default="business-value and solution", help="Short value narrative, such as 'AI revenue operations'.")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE), help="Path to the HTML template.")
    parser.add_argument("--output", help="Output HTML path. Defaults to ./<customer>-renewal-board.html")
    args = parser.parse_args()

    template_path = Path(args.template).expanduser().resolve()
    output_path = Path(args.output or f"{slugify(args.customer_name)}-renewal-board.html").expanduser().resolve()

    values = {
        "CUSTOMER_NAME": args.customer_name,
        "CURRENT_USE_CASES": args.current_use_cases,
        "CUSTOMER_SEGMENT": args.customer_segment,
        "CUSTOMER_VALUE_STORY": args.customer_value_story,
    }

    rendered = render(template_path.read_text(), values)
    output_path.write_text(rendered)
    print(output_path)


if __name__ == "__main__":
    main()
