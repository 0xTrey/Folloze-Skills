#!/usr/bin/env python3
"""Render a local ABM playbook review and a Folloze HTML fragment."""
import argparse
import json
import math
import re
from base64 import b64encode
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

STARTER = Path(__file__).resolve().parents[1] / "assets" / "starter"
IMAGE_TYPES = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg",
               ".jpeg": "image/jpeg", ".webp": "image/webp"}
STAGES = {
    "acquire": ("Acquire and engage", "TOFU", "Reach accounts with paid campaigns, industry pages, content hubs, and calculators.", "Dynamic 1:few / 1:many"),
    "educate": ("Educate and accelerate", "MOFU", "Reach more of the buying group with events, nurture, and personalized follow-up.", "Dynamic and selective 1:1"),
    "convert": ("Convert and expand", "BOFU + customer", "Move deals forward in a room that can become the account hub after close.", "Selective 1:1"),
}


def read(name):
    return (STARTER / name).read_text(encoding="utf-8").strip()


def render(name, fields):
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda match: fields[match[1]], read(name))


def data_url(path, media_type):
    return f"data:{media_type};base64,{b64encode(path.read_bytes()).decode('ascii')}"


def image(path):
    media_type = IMAGE_TYPES.get(path.suffix.lower())
    if not media_type:
        raise ValueError(f"Unsupported image format: {path}")
    return data_url(path, media_type)


def url(value):
    if any(char.isspace() for char in value) or "\\" in value:
        raise ValueError("An example URL contains whitespace or a backslash.")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username is not None:
        raise ValueError("Example links need a full HTTPS URL without credentials.")
    return escape(value)


def link(value, label, *, preview="", link_id=""):
    attributes = 'target="_blank" rel="noopener" data-cp-example'
    href = url(value)
    if preview:
        return f'<a class="cp-preview-link" href="{href}" {attributes} aria-label="Open {escape(label)} in a new tab">{preview}</a>'
    if link_id:
        return f'<a id="{link_id}" class="cp-example-button cp-copy-print-link" href="{href}" {attributes}>{escape(label)}</a>'
    return f'<a class="cp-example-button" href="{href}" {attributes}>{escape(label)} ↗</a>'


def preview_card(example, directory, stage):
    title = example["title"]
    destination = example["url"]
    actions = [link(destination, example.get("label", f"Open {title}"))]
    actions.extend(link(item["url"], item["label"]) for item in example.get("links", []))
    thumbnail = ""
    if asset := example.get("thumbnail"):
        src = image(directory / asset["file"])
        tag = f'<img src="{src}" width="640" height="320" alt="{escape(asset["alt"])}">'
        thumbnail = link(destination, title, preview=tag)
    caption = f'<p>{escape(example["caption"])}</p>' if example.get("caption") else ""
    instructions = ""
    copy_links = example.get("copy_links", [])
    for index, item in enumerate(copy_links, start=1):
        link_id = f"cp-{stage}-copy-{index}"
        label = escape(item["label"])
        actions.append(f'<button class="cp-example-button" type="button" data-cp-copy-link="{link_id}" aria-describedby="cp-{stage}-incognito">Copy {label} URL</button>')
        actions.append(link(item["url"], item["label"], link_id=link_id))
    if copy_links:
        instructions = f"""
          <p id="cp-{stage}-incognito" class="cp-incognito-instructions">Paste copied URLs into a new Chrome Incognito window.</p>
          <p class="cp-copy-status" role="status"></p>
          <label class="cp-copy-fallback" hidden>Copy this URL manually <input type="url" readonly></label>"""
    return f"""
        <div class="cp-preview">
          <h4>{escape(title)}</h4>
          {thumbnail}
          <div class="cp-preview-actions">{''.join(actions)}</div>
          {caption}{instructions}
        </div>"""


def stage_cards(stages, directory):
    unexpected = stages.keys() - STAGES.keys()
    if unexpected:
        raise ValueError("Unknown funnel stages: " + ", ".join(sorted(unexpected)))
    cards = []
    for name, (title, badge, description, model) in STAGES.items():
        stage = stages.get(name, {})
        example = stage.get("example")
        cards.append(f"""
      <article>
        <div class="cp-stage-heading"><h3>{title}</h3><span>{badge}</span></div>
        <p>{escape(stage.get("description", description))}</p>
        <p class="cp-stage-model"><strong>Primary model</strong> {escape(stage.get("model", model))}</p>
        {preview_card(example, directory, name) if example else ""}
      </article>""")
    return "".join(cards)


def numeric(value, label, *, allow_zero=False, percentage=False):
    if value is None:
        return ""
    if (type(value) not in (int, float) or not math.isfinite(value)
            or value < 0 or (value == 0 and not allow_zero) or (percentage and value > 100)):
        raise ValueError(f"Invalid calculator value for {label}: {value!r}")
    return str(value)


def calculator_fields(config):
    currency = config.get("currency", "USD")
    if not re.fullmatch("[A-Z]{3}", currency):
        raise ValueError("Currency must be a three-letter uppercase ISO currency code.")
    note = config.get("note")
    return {
        "CURRENCY": currency,
        "CURRENCY_LABEL": "$" if currency == "USD" else currency,
        "TARGET": numeric(config.get("target"), "target"),
        "OPP_SIZE": numeric(config.get("opportunity_size"), "opportunity size"),
        "ENGAGEMENT": numeric(config.get("engagement_rate"), "engagement rate", percentage=True),
        "OPPORTUNITY": numeric(config.get("opportunity_rate"), "opportunity rate", percentage=True),
        "WIN_RATE": numeric(config.get("illustrative_win_rate", 25), "illustrative win rate", allow_zero=True, percentage=True) or "25",
        "BENCHMARK_NOTE": f'<p class="cp-benchmark-note">{escape(note)}</p>' if note else "",
    }


def items(values):
    return "".join(f"<li>{escape(value)}</li>" for value in values)


def chips(values, label):
    return f'<ul class="cp-tool-chips" aria-label="{label}">{items(values)}</ul>' if values else ""


def font_css(filename, license_file, family, weight):
    source = data_url(STARTER / "fonts" / filename, "font/woff2")
    license_text = read("fonts/" + license_file)
    return (
        f"/*\n{license_text}\n*/\n"
        f'@font-face {{ font-family: "{family}"; font-style: normal; font-weight: {weight}; '
        f'font-display: swap; src: url("{source}") format("woff2"); }}'
    )


def build(config, directory):
    account = escape(config["account"].strip())
    if not account:
        raise ValueError("Account name is required.")
    logo = config.get("account_logo")
    account_mark = (
        f'<img src="{image(directory / logo)}" width="86" height="20" alt="{account}">'
        if logo else f'<strong class="cp-account-name">{account}</strong>'
    )
    folloze_logo = image(STARTER / "folloze-logo.svg")
    math_fields = calculator_fields(config.get("math", {}))
    stack = render("stack.html", {
        "FOLLOZE_LOGO": folloze_logo,
        "CAMPAIGN_SUMMARY": escape(config["campaign_summary"]),
        "WORKFLOW_INPUTS": escape(config["workflow_inputs"]),
        "RESEARCH_TOOLS": chips(config.get("research_tools", []), "Research and writing tools"),
        "CHANNELS": chips(config.get("channels", []), "Distribution channels"),
        "SELLER_ACTION": escape(config["seller_action"]),
    })
    steps = "".join(
        f'<li><strong>{escape(step["title"])}</strong><span>{escape(step["detail"])}</span></li>'
        for step in config["pilot_steps"]
    )
    markup = render("page.html", {
        **math_fields,
        "ACCOUNT": account,
        "ACCOUNT_MARK": account_mark,
        "FOLLOZE_LOGO": folloze_logo,
        "HERO_SUMMARY": escape(config["hero_summary"]),
        "CALCULATOR": render("calculator.html", math_fields),
        "FUNNEL": render("funnel.html", {"STAGES": stage_cards(config.get("stages", {}), directory)}),
        "STACK": stack,
        "ACCOUNT_BUILDS": items(config["account_builds"]),
        "PILOT_SUMMARY": escape(config["pilot_summary"]),
        "PILOT_STEPS": steps,
    })
    css = "\n".join((
        font_css("instrument-sans-latin.woff2", "OFL-InstrumentSans.txt", "CP Instrument Sans", "500"),
        font_css("inter-latin.woff2", "OFL-Inter.txt", "CP Inter", "400 700"),
        read("page.css"),
        read("components.css"),
    ))
    js = read("page.js") + "\n" + read("calculator.js")
    fragment = f"<style>\n{css}\n</style>\n{markup}\n<script>\n{js}\n</script>\n"
    review = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{account} | ABM Playbook for the AI Era</title>
<style>body {{ margin: 0; }}</style>
</head>
<body>
{fragment}</body>
</html>
"""
    return review, fragment


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path, help="Account brief JSON")
    parser.add_argument("--out", required=True, type=Path, help="Account-specific output directory")
    args = parser.parse_args()
    try:
        config = json.loads(args.brief.read_text(encoding="utf-8"))
        review, fragment = build(config, args.brief.resolve().parent)
        args.out.mkdir(parents=True, exist_ok=True)
        for name, content in (("review.html", review), ("fragment.html", fragment)):
            path = args.out / name
            path.write_text(content, encoding="utf-8")
            print(path)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, OverflowError) as error:
        parser.exit(1, f"Build failed: {error}\n")


if __name__ == "__main__":
    main()
