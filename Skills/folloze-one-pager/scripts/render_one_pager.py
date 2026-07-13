#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from validate_one_pager import is_plain_email_address, validate_brief


TOKEN_PATTERN = re.compile(r"\[\[([A-Z0-9_]+)\]\]")
IDENTIFIER_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]*")
MARKER_PATTERN = re.compile(
    r"<!--\s*(OPTIONAL|CTA):([a-z0-9_]+):(START|END)\s*-->",
    flags=re.IGNORECASE,
)

MODULE_KEYS = {
    "account_logo",
    "proof",
    "proof_1",
    "proof_2",
    "proof_3",
    "resource_1",
    "resource_2",
    "build",
    "activate",
    "signal",
}

NESTED_MODULE_ORDER = (
    "proof_1",
    "proof_2",
    "proof_3",
    "resource_1",
    "resource_2",
    "account_logo",
    "build",
    "activate",
    "signal",
    "proof",
)

EXPECTED_MARKER_PAIRS = {
    ("OPTIONAL", "account_logo"): 1,
    ("OPTIONAL", "proof"): 2,
    ("OPTIONAL", "proof_1"): 1,
    ("OPTIONAL", "proof_2"): 1,
    ("OPTIONAL", "proof_3"): 1,
    ("OPTIONAL", "resource_1"): 1,
    ("OPTIONAL", "resource_2"): 1,
    ("OPTIONAL", "build"): 1,
    ("OPTIONAL", "activate"): 1,
    ("OPTIONAL", "signal"): 1,
    ("CTA", "external"): 3,
}

REQUIRED_SOURCE_ID_TOKENS = {
    "HERO_SOURCE_IDS",
    "BUYER_CHALLENGE_SOURCE_IDS",
    "DESIRED_OUTCOME_SOURCE_IDS",
    "PROOF_SOURCE_IDS",
    "PROOF_1_SOURCE_IDS",
    "PROOF_2_SOURCE_IDS",
    "PROOF_3_SOURCE_IDS",
    "RESOURCE_1_SOURCE_IDS",
    "RESOURCE_2_SOURCE_IDS",
    "PATH_SOURCE_IDS",
    "BUILD_SOURCE_IDS",
    "ACTIVATE_SOURCE_IDS",
    "SIGNAL_SOURCE_IDS",
    "NEXT_STEP_SOURCE_IDS",
}


class RenderError(ValueError):
    pass


def validate_marker_contract(source: str) -> None:
    stack: list[tuple[str, str]] = []
    starts: Counter[tuple[str, str]] = Counter()
    ends: Counter[tuple[str, str]] = Counter()
    for match in MARKER_PATTERN.finditer(source):
        family = match.group(1).upper()
        name = match.group(2).lower()
        edge = match.group(3).upper()
        key = (family, name)
        if key not in EXPECTED_MARKER_PAIRS:
            raise RenderError(f"Template contains unexpected {family}:{name} markers.")
        if edge == "START":
            starts[key] += 1
            stack.append(key)
            continue
        ends[key] += 1
        if not stack or stack[-1] != key:
            raise RenderError(f"Template has misnested {family}:{name} markers.")
        stack.pop()
    if stack:
        family, name = stack[-1]
        raise RenderError(f"Template has an unclosed {family}:{name} marker.")
    for key, expected in EXPECTED_MARKER_PAIRS.items():
        if starts[key] != expected or ends[key] != expected:
            family, name = key
            raise RenderError(
                f"Template requires exactly {expected} {family}:{name} marker pair(s)."
            )


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RenderError(f"{label} does not exist: {path}") from exc
    except UnicodeDecodeError as exc:
        raise RenderError(f"{label} is not UTF-8 text: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RenderError(
            f"{label} is invalid JSON at line {exc.lineno}, column {exc.colno}."
        ) from exc
    if not isinstance(value, dict):
        raise RenderError(f"{label} must contain one JSON object.")
    return value


def require_approved_brief(path: Path) -> dict[str, Any]:
    brief = load_object(path, "Brief")
    gate_errors = sorted(
        {
            item
            for item in validate_brief(brief, "final")
            if item.severity == "error"
        }
    )
    if gate_errors:
        details = "\n".join(
            f"- {item.rule_id}: {item.message}" for item in gate_errors
        )
        raise RenderError(
            "Approved intake gate failed; no HTML was written.\n" + details
        )
    return brief


def is_http_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def replace_marked_blocks(
    source: str,
    family: str,
    name: str,
    include: bool,
) -> str:
    pattern = re.compile(
        rf"<!--\s*{re.escape(family)}:{re.escape(name)}:START\s*-->"
        rf"(.*?)"
        rf"<!--\s*{re.escape(family)}:{re.escape(name)}:END\s*-->",
        flags=re.DOTALL,
    )
    matches = list(pattern.finditer(source))
    if not matches:
        raise RenderError(f"Template is missing {family}:{name} markers.")
    return pattern.sub(lambda match: match.group(1) if include else "", source)


def validate_modules(raw_modules: Any) -> dict[str, bool]:
    if not isinstance(raw_modules, dict):
        raise RenderError("modules must be an object with explicit true/false values.")
    unknown = set(raw_modules).difference(MODULE_KEYS)
    missing = MODULE_KEYS.difference(raw_modules)
    if unknown:
        raise RenderError("Unknown modules: " + ", ".join(sorted(unknown)) + ".")
    if missing:
        raise RenderError("Missing module decisions: " + ", ".join(sorted(missing)) + ".")
    if any(not isinstance(raw_modules[key], bool) for key in MODULE_KEYS):
        raise RenderError("Every module decision must be true or false.")

    modules = {key: bool(raw_modules[key]) for key in MODULE_KEYS}
    if modules["proof"] != any(modules[f"proof_{index}"] for index in range(1, 4)):
        raise RenderError("proof must be true exactly when at least one proof card is included.")
    if not modules["proof"]:
        raise RenderError("The standard Proof module requires at least one evidence card.")
    if modules["resource_2"] and not modules["resource_1"]:
        raise RenderError("resource_2 can be enabled only when resource_1 is enabled.")
    if not any(modules[key] for key in ("build", "activate", "signal")):
        raise RenderError("At least one approved path pillar must be included.")
    return modules


def normalize_cta(raw_cta: Any) -> dict[str, str]:
    if not isinstance(raw_cta, dict):
        raise RenderError("cta must be an object.")
    required = {"type", "label", "destination"}
    if set(raw_cta) != required:
        raise RenderError("cta must contain exactly type, label, and destination.")
    if any(not isinstance(raw_cta[key], str) for key in required):
        raise RenderError("CTA type, label, and destination must be strings.")
    cta_type = raw_cta["type"].strip()
    label = raw_cta["label"].strip()
    destination = raw_cta["destination"].strip()
    if cta_type not in {"url", "meeting", "mailto"}:
        raise RenderError("CTA type must be url, meeting, or mailto.")
    if not label:
        raise RenderError("CTA label cannot be empty.")
    if cta_type in {"url", "meeting"}:
        if not is_http_url(destination):
            raise RenderError("URL and meeting CTAs require an HTTP(S) destination.")
    elif cta_type == "mailto":
        address = destination.removeprefix("mailto:")
        if not is_plain_email_address(address):
            raise RenderError(
                "Mailto CTA requires one plain email address without parameters."
            )
        destination = f"mailto:{address}"
    return {"type": cta_type, "label": label, "destination": destination}


def encode_source_ids(token: str, value: Any) -> str:
    if isinstance(value, list):
        if any(not isinstance(item, str) for item in value):
            raise RenderError(f"{token} arrays may contain only strings.")
        raw_ids = [item.strip() for item in value]
    elif isinstance(value, str):
        raw_ids = [item for item in re.split(r"[\s,]+", value.strip()) if item]
    else:
        raise RenderError(f"{token} must be a string or array of source IDs.")
    if token in REQUIRED_SOURCE_ID_TOKENS and not raw_ids:
        raise RenderError(
            f"{token} requires at least one approved source ID; use rep_input or skill_reference when appropriate."
        )
    if any(not IDENTIFIER_PATTERN.fullmatch(item) for item in raw_ids):
        raise RenderError(f"{token} contains an invalid source ID.")
    if len(set(raw_ids)) != len(raw_ids):
        raise RenderError(f"{token} contains a duplicate source ID.")
    return html.escape(" ".join(raw_ids), quote=True)


def encode_token(token: str, value: Any) -> str:
    if token.endswith("_SOURCE_IDS"):
        return encode_source_ids(token, value)
    if not isinstance(value, str):
        raise RenderError(f"{token} must be a string.")
    if token == "ACCOUNT_ACCENT":
        text = value.strip()
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", text):
            raise RenderError("ACCOUNT_ACCENT must be a six-digit hex color.")
        return text
    if token == "ACCOUNT_LOGO_URL" or re.fullmatch(r"RESOURCE_[12]_URL", token):
        text = value.strip()
        if not is_http_url(text):
            raise RenderError(f"{token} must be an HTTP(S) URL.")
        return html.escape(text, quote=True)
    if (
        token.endswith("_CLAIM_ID")
        or re.fullmatch(r"PROOF_[123]_ID", token)
        or re.fullmatch(r"RESOURCE_[12]_ID", token)
    ):
        text = value.strip()
        if not IDENTIFIER_PATTERN.fullmatch(text):
            raise RenderError(f"{token} must be one opaque identifier.")
        return text
    if re.fullmatch(r"PROOF_[123]_KIND", token):
        text = value.strip()
        if text not in {"proof", "claim"}:
            raise RenderError(f"{token} must be proof or claim.")
        return text
    if not value.strip():
        raise RenderError(f"{token} cannot be empty in an included module.")
    return html.escape(value, quote=True)


def render(template: str, values: dict[str, Any]) -> str:
    validate_marker_contract(template)
    modules = validate_modules(values.get("modules"))
    cta = normalize_cta(values.get("cta"))
    raw_tokens = values.get("tokens")
    if not isinstance(raw_tokens, dict):
        raise RenderError("tokens must be an object.")

    template_tokens = set(TOKEN_PATTERN.findall(template))
    source = template
    for module in NESTED_MODULE_ORDER:
        source = replace_marked_blocks(
            source,
            "OPTIONAL",
            module,
            modules[module],
        )

    source = replace_marked_blocks(source, "CTA", "external", True)

    token_values = dict(raw_tokens)
    token_values.update(
        {
            "PRIMARY_CTA_TYPE": cta["type"],
            "PRIMARY_CTA_LABEL": cta["label"],
            "PRIMARY_CTA_URL": cta["destination"],
        }
    )
    account_name = raw_tokens.get("ACCOUNT_NAME")
    if not isinstance(account_name, str) or not account_name.strip():
        raise RenderError("ACCOUNT_NAME is required to compute the page title.")
    token_values["PAGE_TITLE"] = f"Folloze for {account_name.strip()}"
    pillar_tokens = {
        "build": "BUILD_STEP_INDEX",
        "activate": "ACTIVATE_STEP_INDEX",
        "signal": "SIGNAL_STEP_INDEX",
    }
    position = 0
    for pillar, token in pillar_tokens.items():
        if modules[pillar]:
            position += 1
            token_values[token] = f"{position:02d}"

    if not modules["account_logo"]:
        fallback_with_hidden = (
            '<span class="account-name" data-role="account-name" '
            'data-non-claim-number hidden>'
        )
        fallback_visible = (
            '<span class="account-name" data-role="account-name" '
            'data-non-claim-number>'
        )
        if fallback_with_hidden not in source:
            raise RenderError("Template account-name fallback contract changed.")
        source = source.replace(
            fallback_with_hidden,
            fallback_visible,
        )
    if not str(token_values.get("SELLER_ROLE", "")).strip():
        source = source.replace(
            "[[SELLER_NAME]] · [[SELLER_ROLE]]",
            "[[SELLER_NAME]]",
        )

    required_tokens = set(TOKEN_PATTERN.findall(source))
    unknown_values = set(token_values).difference(template_tokens)
    allowed_computed = {
        "PRIMARY_CTA_TYPE",
        "PRIMARY_CTA_LABEL",
        "PRIMARY_CTA_URL",
        "PAGE_TITLE",
        *pillar_tokens.values(),
    }
    unknown_values.difference_update(allowed_computed)
    if unknown_values:
        raise RenderError(
            "Token values are not recognized by this template: "
            + ", ".join(sorted(unknown_values))
            + "."
        )
    missing_values = required_tokens.difference(token_values)
    if missing_values:
        raise RenderError(
            "Missing token values: " + ", ".join(sorted(missing_values)) + "."
        )

    encoded_values = {
        token: encode_token(token, token_values[token])
        for token in required_tokens
    }
    source = TOKEN_PATTERN.sub(lambda match: encoded_values[match.group(1)], source)
    source = re.sub(r'\sdata-source-ids=""', "", source)
    if TOKEN_PATTERN.search(source):
        raise RenderError("Rendered HTML still contains an unresolved token.")
    if MARKER_PATTERN.search(source):
        raise RenderError("Rendered HTML still contains an authoring marker.")
    return source


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Safely render a Folloze prospect one-pager template."
    )
    parser.add_argument(
        "--brief",
        type=Path,
        required=True,
        help="Current intake.json with an approved, digest-bound Stage 2 handoff.",
    )
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--values", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing output file.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        if args.output.exists() and not args.force:
            raise RenderError("Output exists; use --force only after confirming replacement.")
        require_approved_brief(args.brief)
        try:
            template = args.template.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise RenderError(f"Template does not exist: {args.template}") from exc
        except UnicodeDecodeError as exc:
            raise RenderError("Template must be UTF-8 text.") from exc
        values = load_object(args.values, "Values file")
        output = render(template, values)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    except (OSError, RenderError) as exc:
        print(f"RENDER FAILED: {exc}", file=sys.stderr)
        return 1
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
