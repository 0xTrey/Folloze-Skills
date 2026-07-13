#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


EXPECTED_TEMPLATE_TOKENS = {
    "ACCOUNT_ACCENT",
    "ACCOUNT_CONTEXT",
    "ACCOUNT_LOGO_URL",
    "ACCOUNT_NAME",
    "ACTIVATE_CLAIM_ID",
    "ACTIVATE_COPY",
    "ACTIVATE_HEADLINE",
    "ACTIVATE_SOURCE_IDS",
    "ACTIVATE_STEP_INDEX",
    "BUILD_CLAIM_ID",
    "BUILD_COPY",
    "BUILD_HEADLINE",
    "BUILD_SOURCE_IDS",
    "BUILD_STEP_INDEX",
    "BUYER_CHALLENGE",
    "BUYER_CHALLENGE_SOURCE_IDS",
    "DESIRED_OUTCOME",
    "DESIRED_OUTCOME_SOURCE_IDS",
    "HERO_HEADLINE",
    "HERO_SUPPORT",
    "HERO_SOURCE_IDS",
    "META_DESCRIPTION",
    "NEXT_STEP_COPY",
    "NEXT_STEP_HEADLINE",
    "NEXT_STEP_SOURCE_IDS",
    "PAGE_TITLE",
    "PATH_HEADLINE",
    "PATH_INTRO",
    "PATH_SOURCE_IDS",
    "PRIMARY_CTA_LABEL",
    "PRIMARY_CTA_TYPE",
    "PRIMARY_CTA_URL",
    "PROOF_1_COPY",
    "PROOF_1_ID",
    "PROOF_1_KIND",
    "PROOF_1_SOURCE_IDS",
    "PROOF_1_VALUE",
    "PROOF_2_COPY",
    "PROOF_2_ID",
    "PROOF_2_KIND",
    "PROOF_2_SOURCE_IDS",
    "PROOF_2_VALUE",
    "PROOF_3_COPY",
    "PROOF_3_ID",
    "PROOF_3_KIND",
    "PROOF_3_SOURCE_IDS",
    "PROOF_3_VALUE",
    "PROOF_HEADLINE",
    "PROOF_INTRO",
    "PROOF_SOURCE_IDS",
    "RESOURCE_1_ID",
    "RESOURCE_1_LABEL",
    "RESOURCE_1_SOURCE_IDS",
    "RESOURCE_1_URL",
    "RESOURCE_2_ID",
    "RESOURCE_2_LABEL",
    "RESOURCE_2_SOURCE_IDS",
    "RESOURCE_2_URL",
    "SELLER_NAME",
    "SELLER_ROLE",
    "SIGNAL_CLAIM_ID",
    "SIGNAL_COPY",
    "SIGNAL_HEADLINE",
    "SIGNAL_SOURCE_IDS",
    "SIGNAL_STEP_INDEX",
}

REQUIRED_CSS_TOKENS = {
    "--color-ink",
    "--color-navy",
    "--color-brand",
    "--color-brand-strong",
    "--color-accent",
    "--color-account-accent",
    "--color-surface",
    "--color-surface-muted",
    "--color-border",
    "--color-muted",
    "--font-display",
    "--font-body",
    "--radius-sm",
    "--radius-md",
    "--radius-lg",
    "--radius-pill",
    "--shadow-card",
    "--content-max",
    "--header-offset",
    "--space-1",
    "--space-2",
    "--space-3",
    "--space-4",
    "--space-5",
    "--space-6",
    "--space-7",
    "--space-8",
}

SUPPORTED_SOURCES = {
    "rep_input",
    "skill_reference",
    "public_web",
    "salesforce",
    "granola",
    "google_drive",
    "gmail",
    "calendar",
    "slack_channels",
    "slack_dms",
}

POST_APPROVAL_STATES = {
    "intake_approved",
    "stage2_building",
    "local_preview_ready",
    "local_preview_approved",
    "mcp_save_authorized",
    "mcp_saved",
    "public_deployment_pending",
    "public_verified",
}

MCP_AUTHORIZED_STATES = {
    "mcp_save_authorized",
    "mcp_saved",
    "public_deployment_pending",
    "public_verified",
}

MCP_SAVED_STATES = {
    "mcp_saved",
    "public_deployment_pending",
    "public_verified",
}

PUBLIC_AUTHORIZED_STATES = {
    "public_deployment_pending",
    "public_verified",
}

PREVIEW_APPROVED_STATES = {
    "local_preview_approved",
    "mcp_save_authorized",
    "mcp_saved",
    "public_deployment_pending",
    "public_verified",
}

PRIVATE_CONTEXT_SOURCES = {
    "salesforce",
    "granola",
    "google_drive",
    "gmail",
    "calendar",
    "slack_channels",
    "slack_dms",
}

STANDARD_MODULES = {
    "hero",
    "desired_outcome",
    "folloze_capabilities",
    "proof",
    "cta",
}

BUYER_COPY_PLACEMENTS = {
    "hero",
    "buyer_challenge",
    "desired_outcome",
    "proof",
    "folloze_capabilities",
    "path_build",
    "path_activate",
    "path_signal",
    "cta",
    "resource",
    "metadata",
}

PLACEMENT_SECTION_IDS = {
    "hero": "promise",
    "buyer_challenge": "promise",
    "desired_outcome": "promise",
    "proof": "proof",
    "folloze_capabilities": "path",
    "path_build": "path",
    "path_activate": "path",
    "path_signal": "path",
    "cta": "next-step",
    "resource": "next-step",
}

BUYER_VISIBLE_USES = {"public_fact", "paraphrase_only", "exact_use"}

PERMISSION_USE_COMPATIBILITY = {
    "per_item": {
        "public_fact",
        "paraphrase_only",
        "strategy_only",
        "exact_use",
        "blocked",
    },
    "public_fact": {"public_fact", "strategy_only", "blocked"},
    "paraphrase_only": {"paraphrase_only", "strategy_only", "blocked"},
    "exact_use": {
        "exact_use",
        "paraphrase_only",
        "strategy_only",
        "blocked",
    },
    "strategy_only": {"strategy_only", "blocked"},
    "blocked": {"blocked"},
}

VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}

ALLOWED_MICROSITE_TAGS = {
    "a",
    "article",
    "aside",
    "body",
    "button",
    "div",
    "footer",
    "h1",
    "h2",
    "h3",
    "head",
    "header",
    "html",
    "img",
    "link",
    "main",
    "meta",
    "nav",
    "p",
    "script",
    "section",
    "span",
    "style",
    "title",
}

ALLOWED_ATTRIBUTES_BY_TAG = {
    "a": {
        "class",
        "data-cta",
        "data-cta-label",
        "data-cta-type",
        "data-non-claim-number",
        "data-placement",
        "data-resource",
        "data-source-id",
        "data-source-ids",
        "href",
        "onclick",
        "rel",
        "target",
    },
    "article": {
        "class",
        "data-claim-id",
        "data-evidence-id",
        "data-evidence-kind",
        "data-pillar",
        "data-placement",
        "data-proof-id",
        "data-source-id",
        "data-source-ids",
    },
    "aside": {"aria-label", "class"},
    "body": set(),
    "button": {"aria-controls", "class", "data-scroll-target", "type"},
    "div": {"class"},
    "footer": {"class"},
    "h1": {"data-claim-id", "data-placement", "data-proof-id", "data-source-id", "data-source-ids", "id"},
    "h2": {"data-claim-id", "data-placement", "data-proof-id", "data-source-id", "data-source-ids", "id"},
    "h3": {"class", "data-claim-id", "data-proof-id", "data-source-id", "data-source-ids"},
    "head": set(),
    "header": {"class", "data-component"},
    "html": {"data-template", "lang"},
    "img": {"alt", "class", "data-role", "src"},
    "link": {"data-folloze-theme", "href", "rel"},
    "main": {"id"},
    "meta": {"charset", "content", "name"},
    "nav": {"aria-label", "class"},
    "p": {"class", "data-claim-id", "data-placement", "data-proof-id", "data-role", "data-source-id", "data-source-ids"},
    "script": set(),
    "section": {"aria-labelledby", "class", "id"},
    "span": {"aria-hidden", "class", "data-non-claim-number", "data-role", "hidden"},
    "style": set(),
    "title": set(),
}

UNEXPECTED_URL_ATTRIBUTES = {
    "action",
    "background",
    "cite",
    "data",
    "formaction",
    "manifest",
    "ping",
    "poster",
    "srcdoc",
    "srcset",
}

FOLLOZE_LOGO_URL = (
    "https://cdn.prod.website-files.com/6464087fdf877a12a8bd4cd6/"
    "6464087fdf877a12a8bd4d26_folloze-logo.svg"
)

TRUSTED_THEME_SLOT_COMMENT = (
    "FOLLOZE_THEME_LINK_SLOT: replace with the exact MCP-returned link before an authorized save."
)

STATIC_BUYER_TEXT = {
    "Skip to main content",
    "Proof",
    "Capabilities",
    "Next step",
    "See the path",
    "Desired outcome",
    "Buyer challenge",
    "What changes with Folloze",
    "Folloze capabilities",
    "Folloze",
    "×",
    "↗",
}

NUMERIC_CLAIM_PATTERN = re.compile(
    r"(?:"
    r"\b\d\b|"
    r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|"
    r"eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|"
    r"ninety|dozen|hundreds?|thousands?|millions?|billions?|"
    r"twice|double|doubles|doubled|doubling|triple|triples|tripled|"
    r"tripling|quadruple|quadruples|quadrupled|quadrupling|half)\b|"
    r"\$\s?\d|"
    r"\b\d[\d,]*(?:\.\d+)?\s*%|"
    r"\b\d[\d,]*(?:\.\d+)?\s*[kKmMbB]\b|"
    r"\b\d[\d,]*(?:\.\d+)?\s*[xX×](?!\w)|"
    r"\b\d[\d,]*(?:\.\d+)?\s*(?:-\s*)?fold\b|"
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|"
    r"twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|"
    r"nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|"
    r"hundred|thousand|million|billion)(?:-|\s)?fold\b|"
    r"\b\d[\d,]*(?:\.\d+)?\s+times?\b|"
    r"\b\d[\d,]*(?:\.\d+)?\s+"
    r"(?:users?|months?|days?|weeks?|years?|accounts?|buyers?|"
    r"customers?|campaigns?|minutes?|mins?|hours?|hrs?|seconds?|secs?|"
    r"teams?|people|visitors?|engagements?|points?|leads?|"
    r"opportunities?|meetings?)\b|"
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten)\s+"
    r"(?:users?|months?|days?|weeks?|years?|accounts?|buyers?|"
    r"customers?|campaigns?|minutes?|hours?|teams?|people|visitors?|"
    r"engagements?|points?|leads?|opportunities?|meetings?)\b|"
    r"\b\d{2,}(?:,\d{3})*\b"
    r")",
    flags=re.IGNORECASE,
)

PLAIN_EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9.!#$&'*+/=_`{|}~-]+@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63}"
)


@dataclass(frozen=True, order=True)
class Issue:
    rule_id: str
    message: str
    severity: str = "error"


@dataclass(frozen=True)
class Element:
    tag: str
    attrs: dict[str, str]
    in_head: bool
    parent_tag: str
    parent_id: str
    section_id: str
    sequence: int


@dataclass(frozen=True)
class TextNode:
    text: str
    proof_id: str
    claim_id: str
    evidence_kind: str
    evidence_id: str
    placement: str
    source_ids: tuple[str, ...]
    non_claim_number: bool
    hidden_from_buyers: bool


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[Element] = []
        self.elements: list[Element] = []
        self.ids: Counter[str] = Counter()
        self.h1_count = 0
        self.title_parts: list[str] = []
        self.style_parts: list[str] = []
        self.script_parts: list[str] = []
        self.visible_nodes: list[TextNode] = []
        self.comments: list[str] = []
        self.direct_text_parts: dict[int, list[str]] = {}
        self.semantic_text_parts: dict[int, list[str]] = {}
        self.html_attrs: dict[str, str] = {}
        self.has_viewport = False
        self.has_description = False
        self.description_contents: list[str] = []
        self.duplicate_attributes: list[tuple[str, str]] = []

    @staticmethod
    def _attrs(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {key.lower(): value or "" for key, value in attrs}

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        tag = tag.lower()
        attribute_names = [key.lower() for key, _ in attrs]
        for attribute_name, count in Counter(attribute_names).items():
            if count > 1:
                self.duplicate_attributes.append((tag, attribute_name))
        attr_map = self._attrs(attrs)
        section_id = ""
        if tag == "section":
            section_id = attr_map.get("id", "")
        else:
            for parent in reversed(self.stack):
                if parent.tag == "section":
                    section_id = parent.attrs.get("id", "")
                    break
        element = Element(
            tag=tag,
            attrs=attr_map,
            in_head=any(parent.tag == "head" for parent in self.stack),
            parent_tag=self.stack[-1].tag if self.stack else "",
            parent_id=self.stack[-1].attrs.get("id", "") if self.stack else "",
            section_id=section_id,
            sequence=len(self.elements),
        )
        self.elements.append(element)

        element_id = attr_map.get("id")
        if element_id:
            self.ids[element_id] += 1

        if tag == "html":
            self.html_attrs = attr_map
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta":
            if attr_map.get("name", "").lower() == "viewport":
                self.has_viewport = bool(attr_map.get("content"))
            if attr_map.get("name", "").lower() == "description":
                self.has_description = bool(attr_map.get("content"))
                self.description_contents.append(attr_map.get("content", ""))

        if tag not in VOID_TAGS:
            self.stack.append(element)

    def handle_startendtag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1].tag == tag.lower():
            self.stack.pop()

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        if not data:
            return
        ancestors = {element.tag for element in self.stack}
        if "style" in ancestors:
            self.style_parts.append(data)
            return
        if "script" in ancestors:
            self.script_parts.append(data)
            return
        if "title" in ancestors:
            self.title_parts.append(data)
            return
        if ancestors.intersection({"noscript", "template"}):
            return
        if not data.strip():
            return

        if self.stack:
            self.direct_text_parts.setdefault(self.stack[-1].sequence, []).append(
                data.strip()
            )
        hidden_from_buyers = bool(
            self.stack
            and any(
                element.attrs.get("aria-hidden") == "true"
                or "hidden" in element.attrs
                for element in self.stack
            )
        )
        if self.stack and not hidden_from_buyers:
            for element in self.stack:
                self.semantic_text_parts.setdefault(element.sequence, []).append(
                    data.strip()
                )

        proof_id = ""
        claim_id = ""
        evidence_kind = ""
        evidence_id = ""
        placement = ""
        source_ids: set[str] = set()
        candidate_non_claim_number = bool(
            self.stack
            and "data-non-claim-number" in self.stack[-1].attrs
        )
        for element in reversed(self.stack):
            proof_id = proof_id or element.attrs.get("data-proof-id", "")
            claim_id = claim_id or element.attrs.get("data-claim-id", "")
            evidence_kind = evidence_kind or element.attrs.get(
                "data-evidence-kind", ""
            )
            evidence_id = evidence_id or element.attrs.get(
                "data-evidence-id", ""
            )
            placement = placement or element.attrs.get("data-placement", "")
            raw_source_ids = " ".join(
                filter(
                    None,
                    (
                        element.attrs.get("data-source-id", ""),
                        element.attrs.get("data-source-ids", ""),
                    ),
                )
            )
            source_ids.update(
                token
                for token in re.split(r"[\s,]+", raw_source_ids.strip())
                if token
            )
        non_claim_number = candidate_non_claim_number and not any(
            (
                proof_id,
                claim_id,
                evidence_kind,
                evidence_id,
                source_ids,
            )
        )
        self.visible_nodes.append(
            TextNode(
                text=data.strip(),
                proof_id=proof_id,
                claim_id=claim_id,
                evidence_kind=evidence_kind,
                evidence_id=evidence_id,
                placement=placement,
                source_ids=tuple(sorted(source_ids)),
                non_claim_number=non_claim_number,
                hidden_from_buyers=hidden_from_buyers,
            )
        )

    def handle_comment(self, data: str) -> None:
        self.comments.append(data)

    def elements_with(self, attribute: str) -> list[Element]:
        return [element for element in self.elements if attribute in element.attrs]

    def elements_by_role(self, role: str) -> list[Element]:
        return [
            element
            for element in self.elements
            if element.attrs.get("data-role") == role
        ]

    def direct_text(self, element: Element) -> str:
        return " ".join(self.direct_text_parts.get(element.sequence, [])).strip()

    def semantic_text(self, element: Element) -> str:
        return canonical_display_text(
            " ".join(self.semantic_text_parts.get(element.sequence, []))
        )

    @property
    def title(self) -> str:
        return " ".join(part.strip() for part in self.title_parts if part.strip())

    @property
    def style_text(self) -> str:
        return "\n".join(self.style_parts)

    @property
    def script_text(self) -> str:
        return "\n".join(self.script_parts)

    @property
    def visible_text(self) -> str:
        return " ".join(node.text for node in self.visible_nodes)


def issue(rule_id: str, message: str, severity: str = "error") -> Issue:
    return Issue(rule_id=rule_id, message=message, severity=severity)


def get_path(data: dict[str, Any], dotted_path: str, default: Any = None) -> Any:
    value: Any = data
    for part in dotted_path.split("."):
        if not isinstance(value, dict) or part not in value:
            return default
        value = value[part]
    return value


def parse_rfc3339(value: Any) -> datetime | None:
    if not isinstance(value, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})",
        value,
    ):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed


def nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value)
    return value is not None


def canonical_display_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value)).strip()


def is_http_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_plain_email_address(value: str) -> bool:
    return len(value) <= 254 and bool(PLAIN_EMAIL_PATTERN.fullmatch(value))


def normalize_cta_destination(cta_type: str, destination: str) -> str:
    destination = destination.strip()
    if cta_type == "mailto" and destination and not destination.startswith("mailto:"):
        return f"mailto:{destination}"
    return destination


def valid_cta_onclick(value: str) -> bool:
    return bool(
        re.fullmatch(
            r"flzAnalytic\('cta_click', \{text:this\.dataset\.ctaLabel, "
            r"area:'(?:header|hero|next step)', "
            r"url:this\.href\}, this\)",
            value,
        )
    )


def valid_resource_onclick(value: str) -> bool:
    return value == (
        "flzAnalytic('resource_click', "
        "{text:this.innerText.trim(), area:'resources', url:this.href}, this)"
    )


def trusted_microsite_script() -> tuple[str | None, Issue | None]:
    template_path = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "one-pager-microsite-template.html"
    )
    try:
        raw_template = template_path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError):
        return None, issue(
            "SCRIPT006",
            "Trusted microsite template script could not be loaded.",
        )
    trusted_parser = PageParser()
    try:
        trusted_parser.feed(raw_template)
        trusted_parser.close()
    except Exception as exc:
        return None, issue(
            "SCRIPT006",
            f"Trusted microsite template script could not be parsed: {exc}.",
        )
    return trusted_parser.script_text.strip(), None


def normalize_trusted_style(style_text: str) -> str:
    return re.sub(
        r"(--color-account-accent\s*:\s*)[^;]+;",
        r"\1[[ACCOUNT_ACCENT]];",
        style_text.strip(),
        count=1,
        flags=re.IGNORECASE,
    )


def trusted_microsite_style() -> tuple[str | None, Issue | None]:
    template_path = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "one-pager-microsite-template.html"
    )
    try:
        raw_template = template_path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError):
        return None, issue(
            "CSS007",
            "Trusted microsite template style could not be loaded.",
        )
    trusted_parser = PageParser()
    try:
        trusted_parser.feed(raw_template)
        trusted_parser.close()
    except Exception as exc:
        return None, issue(
            "CSS007",
            f"Trusted microsite template style could not be parsed: {exc}.",
        )
    return normalize_trusted_style(trusted_parser.style_text), None


def element_source_ids(element: Element) -> set[str]:
    raw = " ".join(
        filter(
            None,
            (
                element.attrs.get("data-source-id", ""),
                element.attrs.get("data-source-ids", ""),
            ),
        )
    )
    return {
        token
        for token in re.split(r"[\s,]+", raw.strip())
        if token
    }


def expected_element_placement(element: Element) -> str:
    classes = set(element.attrs.get("class", "").split())
    element_id = element.attrs.get("id", "")
    if "eyebrow" in classes or "hero-support" in classes or element_id == "promise-title":
        return "hero"
    if "buyer-challenge-copy" in classes:
        return "buyer_challenge"
    if "desired-outcome-copy" in classes:
        return "desired_outcome"
    if (
        "proof-card" in classes
        or "proof-intro" in classes
        or element_id == "proof-title"
    ):
        return "proof"
    if "capabilities-intro" in classes or element_id == "path-title":
        return "folloze_capabilities"
    if "path-step" in classes:
        return {
            "Build": "path_build",
            "Activate": "path_activate",
            "Signal": "path_signal",
        }.get(element.attrs.get("data-pillar", ""), "")
    if "next-step-copy" in classes or element_id == "next-step-title":
        return "cta"
    if "resource-link" in classes and "data-resource" in element.attrs:
        return "resource"
    return ""


def build_approved_content_registry(
    brief: dict[str, Any],
    kind: str,
) -> tuple[dict[str, dict[str, Any]], list[Issue]]:
    if kind not in {"proof", "claim"}:
        raise ValueError("Approved content kind must be proof or claim.")
    path = f"claims_policy.approved_{kind}_content"
    id_key = f"{kind}_id"
    raw_records = get_path(brief, path, [])
    if not isinstance(raw_records, list):
        return {}, [issue("CONTENT001", f"Approved {kind} content must be an array.")]

    raw_ids = [
        canonical_display_text(record.get(id_key, ""))
        for record in raw_records
        if isinstance(record, dict)
    ]
    duplicate_ids = {
        content_id
        for content_id, count in Counter(raw_ids).items()
        if content_id and count > 1
    }
    registry: dict[str, dict[str, Any]] = {}
    issues: list[Issue] = []
    if duplicate_ids:
        issues.append(
            issue(
                "CONTENT002",
                f"Duplicate approved {kind} content IDs: "
                + ", ".join(sorted(duplicate_ids))
                + ".",
            )
        )

    for record in raw_records:
        if not isinstance(record, dict):
            issues.append(
                issue("CONTENT003", f"Approved {kind} content must be an object.")
            )
            continue
        content_id = canonical_display_text(record.get(id_key, ""))
        if not content_id:
            issues.append(
                issue("CONTENT004", f"Approved {kind} content has an empty ID.")
            )
            continue
        raw_texts = record.get("approved_display_text", [])
        texts = {
            canonical_display_text(value)
            for value in raw_texts
            if isinstance(value, str) and canonical_display_text(value)
        } if isinstance(raw_texts, list) else set()
        if not texts:
            issues.append(
                issue(
                    "CONTENT005",
                    f"Approved {kind} content {content_id!r} has no display text.",
                )
            )
        raw_sources = record.get("source_ids", [])
        source_ids = {
            canonical_display_text(value)
            for value in raw_sources
            if isinstance(value, str) and canonical_display_text(value)
        } if isinstance(raw_sources, list) else set()
        if not source_ids:
            issues.append(
                issue(
                    "CONTENT006",
                    f"Approved {kind} content {content_id!r} has no source IDs.",
                )
            )
        pillar = ""
        if kind == "claim":
            pillar = canonical_display_text(record.get("pillar", ""))
            if pillar not in {"Build", "Activate", "Signal"}:
                issues.append(
                    issue(
                        "CONTENT013",
                        f"Approved claim content {content_id!r} needs a Build, Activate, or Signal pillar.",
                    )
                )
        if content_id not in duplicate_ids:
            registry[content_id] = {
                "texts": texts,
                "source_ids": source_ids,
                "pillar": pillar,
            }
    return registry, issues


def build_approved_resource_registry(
    brief: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], list[Issue]]:
    raw_resources = get_path(
        brief,
        "seller_inputs.page_goal.approved_resources",
        [],
    )
    if not isinstance(raw_resources, list):
        return {}, [issue("RESOURCE006", "Approved resources must be an array.")]

    raw_ids = [
        canonical_display_text(record.get("resource_id", ""))
        for record in raw_resources
        if isinstance(record, dict)
    ]
    duplicate_ids = {
        resource_id
        for resource_id, count in Counter(raw_ids).items()
        if resource_id and count > 1
    }
    issues: list[Issue] = []
    if duplicate_ids:
        issues.append(
            issue(
                "RESOURCE007",
                "Duplicate approved resource IDs: "
                + ", ".join(sorted(duplicate_ids))
                + ".",
            )
        )

    registry: dict[str, dict[str, Any]] = {}
    for record in raw_resources:
        if not isinstance(record, dict):
            issues.append(
                issue("RESOURCE008", "Each approved resource must be an object.")
            )
            continue
        resource_id = canonical_display_text(record.get("resource_id", ""))
        label = canonical_display_text(record.get("label", ""))
        url = str(record.get("url", "")).strip()
        raw_source_ids = record.get("source_ids", [])
        source_ids = {
            canonical_display_text(value)
            for value in raw_source_ids
            if isinstance(value, str) and canonical_display_text(value)
        } if isinstance(raw_source_ids, list) else set()
        if not resource_id or not IDENTIFIER_PATTERN.fullmatch(resource_id):
            issues.append(
                issue("RESOURCE009", "Approved resource needs one opaque resource ID.")
            )
            continue
        if not label:
            issues.append(
                issue(
                    "RESOURCE010",
                    f"Approved resource {resource_id!r} needs a buyer-visible label.",
                )
            )
        if not is_http_url(url):
            issues.append(
                issue(
                    "RESOURCE011",
                    f"Approved resource {resource_id!r} needs an HTTP(S) URL.",
                )
            )
        if not source_ids:
            issues.append(
                issue(
                    "RESOURCE012",
                    f"Approved resource {resource_id!r} needs at least one source ID.",
                )
            )
        if resource_id not in duplicate_ids:
            registry[resource_id] = {
                "label": label,
                "url": url,
                "source_ids": source_ids,
            }
    return registry, issues


def compute_approval_digest(brief: dict[str, Any]) -> str:
    payload = {
        "brief_version": get_path(brief, "metadata.brief_version"),
        "seller_inputs": brief.get("seller_inputs"),
        "research_policy": brief.get("research_policy"),
        "claims_policy": brief.get("claims_policy"),
        "normalized_brief": brief.get("normalized_brief"),
        "stage2_constraints": get_path(
            brief,
            "stage2_handoff.constraints",
            {},
        ),
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


def compute_preview_html_digest(raw_html: str) -> str:
    normalized = re.sub(
        r"<!--\s*FOLLOZE_THEME_LINK_SLOT:.*?-->\s*",
        "",
        raw_html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    normalized = re.sub(
        r"<link\b(?=[^>]*\bdata-folloze-theme\b)[^>]*>\s*",
        "",
        normalized,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return "sha256:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def digest_payload(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


def compute_mcp_authorization_digest(brief: dict[str, Any]) -> str:
    mcp_state = get_path(brief, "stage2_handoff.mcp_state", {})
    if not isinstance(mcp_state, dict):
        mcp_state = {}
    save_intent = mcp_state.get("save_intent")
    payload = {
        "contract": "folloze.mcp_save_authorization.v1",
        "intake_id": get_path(brief, "metadata.intake_id"),
        "brief_version": get_path(brief, "metadata.brief_version"),
        "approval_digest": get_path(brief, "approval.approval_digest"),
        "preview_html_digest": get_path(
            brief,
            "stage2_handoff.preview_approval.html_digest",
        ),
        "save_authorization": {
            "authorized_by": mcp_state.get("save_authorized_by"),
            "authorized_at": mcp_state.get("save_authorized_at"),
            "authorization_text": mcp_state.get("save_authorization_text"),
        },
        "save_request": {
            "save_intent": save_intent,
            "board_name": mcp_state.get("board_name"),
            "target_board_id": (
                mcp_state.get("board_id") if save_intent == "update" else None
            ),
            "local_html_path": mcp_state.get("local_html_path"),
            "theme_mode": mcp_state.get("theme_mode"),
            "theme_id": mcp_state.get("theme_id"),
            "theme_url": mcp_state.get("theme_url"),
            "qa_status": mcp_state.get("qa_status"),
        },
    }
    return digest_payload(payload)


def compute_mcp_save_result_digest(brief: dict[str, Any]) -> str:
    mcp_state = get_path(brief, "stage2_handoff.mcp_state", {})
    if not isinstance(mcp_state, dict):
        mcp_state = {}
    return digest_payload(
        {
            "contract": "folloze.mcp_save_result.v1",
            "intake_id": get_path(brief, "metadata.intake_id"),
            "brief_version": get_path(brief, "metadata.brief_version"),
            "account_name": get_path(
                brief,
                "seller_inputs.prospect.account_name",
            ),
            "preview_html_digest": get_path(
                brief,
                "stage2_handoff.preview_approval.html_digest",
            ),
            "mcp_authorization_digest": mcp_state.get("authorization_digest"),
            "result": {
                "status": mcp_state.get("save_result_status"),
                "recorded_by": mcp_state.get("save_result_recorded_by"),
                "recorded_at": mcp_state.get("save_result_recorded_at"),
                "account_name": mcp_state.get("save_result_account_name"),
                "board_id": mcp_state.get("save_result_board_id"),
                "designer_url": mcp_state.get("save_result_designer_url"),
                "evidence": mcp_state.get("save_result_evidence"),
            },
        }
    )


def compute_public_deployment_authorization_digest(
    brief: dict[str, Any],
) -> str:
    mcp_state = get_path(brief, "stage2_handoff.mcp_state", {})
    if not isinstance(mcp_state, dict):
        mcp_state = {}
    return digest_payload(
        {
            "contract": "folloze.public_deployment_authorization.v1",
            "intake_id": get_path(brief, "metadata.intake_id"),
            "brief_version": get_path(brief, "metadata.brief_version"),
            "account_name": get_path(
                brief,
                "seller_inputs.prospect.account_name",
            ),
            "seller_motion": get_path(brief, "seller_inputs.seller.motion"),
            "approval_digest": get_path(brief, "approval.approval_digest"),
            "preview_html_digest": get_path(
                brief,
                "stage2_handoff.preview_approval.html_digest",
            ),
            "mcp_authorization_digest": mcp_state.get("authorization_digest"),
            "mcp_save_result_digest": mcp_state.get("save_result_digest"),
            "board_id": mcp_state.get("board_id"),
            "designer_url": mcp_state.get("designer_url"),
            "public_deployment_authorization": {
                "authorized_by": mcp_state.get(
                    "public_deployment_authorized_by"
                ),
                "authorized_at": mcp_state.get(
                    "public_deployment_authorized_at"
                ),
                "authorization_text": mcp_state.get(
                    "public_deployment_authorization_text"
                ),
            },
        }
    )


def compute_public_verification_digest(brief: dict[str, Any]) -> str:
    mcp_state = get_path(brief, "stage2_handoff.mcp_state", {})
    if not isinstance(mcp_state, dict):
        mcp_state = {}
    return digest_payload(
        {
            "contract": "folloze.public_verification.v1",
            "intake_id": get_path(brief, "metadata.intake_id"),
            "brief_version": get_path(brief, "metadata.brief_version"),
            "preview_html_digest": get_path(
                brief,
                "stage2_handoff.preview_approval.html_digest",
            ),
            "mcp_save_result_digest": mcp_state.get("save_result_digest"),
            "public_deployment_authorization_digest": mcp_state.get(
                "public_deployment_authorization_digest"
            ),
            "board_id": mcp_state.get("board_id"),
            "public_url": mcp_state.get("public_url"),
            "verification": {
                "method": mcp_state.get("public_verification_method"),
                "verified_by": mcp_state.get("public_verified_by"),
                "verified_at": mcp_state.get("public_verified_at"),
                "account_name": mcp_state.get(
                    "public_verification_account_name"
                ),
                "board_id": mcp_state.get("public_verification_board_id"),
                "evidence": mcp_state.get("public_verification_evidence"),
            },
        }
    )


def load_json(path: Path, label: str) -> tuple[dict[str, Any] | None, list[Issue]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [issue("INPUT001", f"{label} file does not exist.")]
    except UnicodeDecodeError:
        return None, [issue("INPUT002", f"{label} file is not UTF-8 text.")]
    except json.JSONDecodeError as exc:
        return None, [
            issue(
                "INPUT003",
                f"{label} is not valid JSON at line {exc.lineno}, column {exc.colno}.",
            )
        ]
    if not isinstance(value, dict):
        return None, [issue("INPUT004", f"{label} must contain one JSON object.")]
    return value, []


def schema_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def resolve_schema_ref(root_schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"Unsupported schema reference {ref!r}")
    value: Any = root_schema
    for raw_part in ref[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or part not in value:
            raise ValueError(f"Unresolved schema reference {ref!r}")
        value = value[part]
    if not isinstance(value, dict):
        raise ValueError(f"Schema reference {ref!r} is not an object")
    return value


def validate_schema_node(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str,
) -> list[str]:
    errors: list[str] = []

    if "$ref" in schema:
        try:
            target = resolve_schema_ref(root_schema, str(schema["$ref"]))
        except ValueError as exc:
            return [f"{path}: {exc}"]
        return validate_schema_node(value, target, root_schema, path)

    if "anyOf" in schema:
        branches = schema.get("anyOf")
        if not isinstance(branches, list):
            return [f"{path}: anyOf must be an array"]
        branch_results = [
            validate_schema_node(value, branch, root_schema, path)
            for branch in branches
            if isinstance(branch, dict)
        ]
        if not branch_results or not any(not result for result in branch_results):
            return [f"{path}: value does not match any allowed schema"]

    expected_types = schema.get("type")
    if expected_types is not None:
        if isinstance(expected_types, str):
            expected_types = [expected_types]
        if not isinstance(expected_types, list) or not any(
            isinstance(expected, str) and schema_type_matches(value, expected)
            for expected in expected_types
        ):
            return [
                f"{path}: expected type "
                + "/".join(str(item) for item in expected_types)
            ]

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: value must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value is not in the allowed enum")

    if isinstance(value, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in value:
                    errors.append(f"{path}.{key}: required property is missing")

        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, item in value.items():
                child_path = f"{path}.{key}"
                child_schema = properties.get(key)
                if isinstance(child_schema, dict):
                    errors.extend(
                        validate_schema_node(
                            item,
                            child_schema,
                            root_schema,
                            child_path,
                        )
                    )
                elif schema.get("additionalProperties") is False:
                    errors.append(f"{child_path}: additional property is not allowed")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < int(schema["minItems"]):
            errors.append(f"{path}: array has fewer than minItems")
        if "maxItems" in schema and len(value) > int(schema["maxItems"]):
            errors.append(f"{path}: array has more than maxItems")
        if schema.get("uniqueItems"):
            seen: set[str] = set()
            for item in value:
                marker = json.dumps(
                    item,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                if marker in seen:
                    errors.append(f"{path}: array items must be unique")
                    break
                seen.add(marker)
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(
                    validate_schema_node(
                        item,
                        item_schema,
                        root_schema,
                        f"{path}[{index}]",
                    )
                )

    if isinstance(value, str) and "pattern" in schema:
        if not re.search(str(schema["pattern"]), value):
            errors.append(f"{path}: string does not match required pattern")

    if (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and "minimum" in schema
        and value < schema["minimum"]
    ):
        errors.append(f"{path}: value is below minimum")

    return errors


def validate_against_intake_schema(brief: dict[str, Any]) -> list[Issue]:
    schema_path = (
        Path(__file__).resolve().parents[1] / "schemas" / "intake.schema.json"
    )
    schema, load_issues = load_json(schema_path, "Intake schema")
    if load_issues:
        return [
            issue("SCHEMA000", item.message)
            for item in load_issues
        ]
    if schema is None:
        return [issue("SCHEMA000", "Intake schema could not be loaded.")]
    errors = validate_schema_node(brief, schema, schema, "$")
    return [
        issue("SCHEMA001", message)
        for message in sorted(set(errors))
    ]


def validate_brief(brief: dict[str, Any], mode: str) -> list[Issue]:
    issues: list[Issue] = validate_against_intake_schema(brief)

    if brief.get("schema_version") != "1.0":
        issues.append(issue("BRIEF001", "schema_version must be 1.0."))
    if brief.get("kind") != "folloze.prospect_one_pager_intake":
        issues.append(issue("BRIEF002", "kind is not the one-pager intake contract."))

    metadata = brief.get("metadata")
    if not isinstance(metadata, dict):
        return issues + [issue("BRIEF003", "metadata must be an object.")]

    intake_id = metadata.get("intake_id", "")
    brief_version = metadata.get("brief_version")
    state = metadata.get("state")

    if not nonempty(intake_id):
        issues.append(issue("BRIEF004", "intake_id is required."))
    if not isinstance(brief_version, int) or brief_version < 1:
        issues.append(issue("BRIEF005", "brief_version must be a positive integer."))
    if mode in {"final", "mcp"} and state not in POST_APPROVAL_STATES:
        issues.append(
            issue("GATE001", "Stage 2 requires an intake-approved state.")
        )

    required_fields = {
        "seller_inputs.seller.name": "seller name",
        "seller_inputs.seller.email": "seller email",
        "seller_inputs.seller.motion": "seller motion",
        "seller_inputs.prospect.account_name": "prospect account name",
        "seller_inputs.audience.primary_persona": "primary persona",
        "seller_inputs.audience.lifecycle_stage": "lifecycle stage",
        "seller_inputs.business_context.initiative": "business initiative",
        "seller_inputs.business_context.challenges": "at least one challenge",
        "seller_inputs.business_context.desired_outcomes": "at least one desired outcome",
        "seller_inputs.page_goal.page_job": "page job",
        "seller_inputs.page_goal.meta_description": "buyer-safe meta description",
        "seller_inputs.page_goal.primary_cta.label": "primary CTA label",
        "seller_inputs.page_goal.primary_cta.destination": "primary CTA destination",
        "normalized_brief.buyer_situation": "buyer situation",
        "normalized_brief.holistic_page_goal": "holistic page goal",
        "normalized_brief.message_spine.account_context": "account context",
        "normalized_brief.message_spine.buyer_priority": "buyer priority",
        "normalized_brief.message_spine.why_change": "why change",
        "normalized_brief.message_spine.folloze_promise": "Folloze promise",
        "normalized_brief.message_spine.proof_strategy": "proof strategy",
        "normalized_brief.message_spine.next_action": "next action",
        "normalized_brief.selected_folloze_pillars": "at least one Folloze pillar",
        "normalized_brief.message_fit_matrix": "message-fit matrix",
    }
    if mode in {"final", "mcp"}:
        for dotted_path, label in required_fields.items():
            if not nonempty(get_path(brief, dotted_path)):
                issues.append(issue("GATE002", f"Approved brief is missing {label}."))

        challenges = get_path(
            brief,
            "seller_inputs.business_context.challenges",
            [],
        )
        outcomes = get_path(
            brief,
            "seller_inputs.business_context.desired_outcomes",
            [],
        )
        if (
            not isinstance(challenges, list)
            or len(challenges) != 1
            or not nonempty(challenges[0])
        ):
            issues.append(
                issue("GATE014", "Approved brief requires exactly one buyer challenge.")
            )
        if (
            not isinstance(outcomes, list)
            or len(outcomes) != 1
            or not nonempty(outcomes[0])
        ):
            issues.append(
                issue("GATE015", "Approved brief requires exactly one desired outcome.")
            )

        raw_requested_modules = get_path(
            brief,
            "seller_inputs.page_goal.requested_modules",
            [],
        ) or []
        requested_modules = {
            item
            for item in raw_requested_modules
            if isinstance(item, str)
        } if isinstance(raw_requested_modules, list) else set()
        if requested_modules != STANDARD_MODULES:
            issues.append(
                issue(
                    "GATE016",
                    "Approved page must use the five standard modules: hero, desired outcome, Folloze capabilities, proof, and CTA.",
                )
            )
        raw_recommended_sections = get_path(
            brief,
            "normalized_brief.recommended_sections",
            [],
        )
        recommended_sections = {
            item
            for item in raw_recommended_sections
            if isinstance(item, str)
        } if isinstance(raw_recommended_sections, list) else set()
        if (
            recommended_sections != STANDARD_MODULES
            or not isinstance(raw_recommended_sections, list)
            or len(raw_recommended_sections) != len(STANDARD_MODULES)
        ):
            issues.append(
                issue(
                    "GATE021",
                    "The normalized brief must recommend exactly the five standard modules.",
                )
            )
        if get_path(
            brief,
            "seller_inputs.page_goal.modules_to_omit",
            [],
        ):
            issues.append(
                issue(
                    "GATE018",
                    "The five standard one-pager modules cannot be omitted.",
                )
            )
        if get_path(
            brief,
            "seller_inputs.page_goal.secondary_cta",
            None,
        ) is not None:
            issues.append(
                issue(
                    "GATE019",
                    "The short one-pager supports one primary CTA; use approved resource links for supporting actions.",
                )
            )

    account_domain = get_path(brief, "seller_inputs.prospect.domain", "")
    entity_confirmed = get_path(
        brief, "seller_inputs.prospect.entity_confirmed", False
    )
    if mode in {"final", "mcp"} and not account_domain and not entity_confirmed:
        issues.append(
            issue(
                "GATE003",
                "Prospect identity needs a domain or explicit entity confirmation.",
            )
        )

    personalization_mode = get_path(
        brief,
        "seller_inputs.page_goal.personalization_mode",
        "account_specific",
    )
    account_signal = get_path(
        brief, "seller_inputs.business_context.account_signal", ""
    )
    seller_motion = str(
        get_path(brief, "seller_inputs.seller.motion", "")
    ).strip()
    buyer_visible_assumptions = get_path(
        brief,
        "normalized_brief.buyer_visible_assumptions",
        [],
    ) or []
    if (
        mode in {"final", "mcp"}
        and personalization_mode == "account_specific"
        and not nonempty(account_signal)
        and not (
            seller_motion == "sdr_net_new"
            and isinstance(buyer_visible_assumptions, list)
            and any(nonempty(item) for item in buyer_visible_assumptions)
        )
    ):
        issues.append(
            issue(
                "GATE004",
                "Account-specific mode requires a buyer-safe account signal or an approved SDR hypothesis.",
            )
        )

    cta_type = get_path(brief, "seller_inputs.page_goal.primary_cta.type", "")
    cta_destination = get_path(
        brief, "seller_inputs.page_goal.primary_cta.destination", ""
    )
    normalized_destination = normalize_cta_destination(
        str(cta_type), str(cta_destination)
    )
    if mode in {"final", "mcp"}:
        if cta_type in {"url", "meeting"} and not is_http_url(
            normalized_destination
        ):
            issues.append(
                issue("CTA001", "URL and meeting CTAs require a real HTTP(S) URL.")
            )
        elif cta_type == "mailto":
            address = normalized_destination.removeprefix("mailto:")
            if not is_plain_email_address(address):
                issues.append(
                    issue(
                        "CTA002",
                        "Mail CTA requires one plain email address without parameters.",
                    )
                )
        elif cta_type not in {"url", "meeting", "mailto"}:
            issues.append(issue("CTA004", "Primary CTA type is not supported."))

        cta_label = str(
            get_path(brief, "seller_inputs.page_goal.primary_cta.label", "")
        ).strip()
        seller_email = str(
            get_path(brief, "seller_inputs.seller.email", "")
        ).strip()
        if not is_plain_email_address(seller_email):
            issues.append(issue("GATE020", "Seller email must be one plain email address."))
        if seller_motion == "sdr_net_new":
            if cta_type != "meeting" or cta_label != "Book a Meeting":
                issues.append(
                    issue(
                        "CTA005",
                        "SDR net-new pages require a meeting CTA labeled exactly 'Book a Meeting'.",
                    )
                )
        elif seller_motion == "ae_active_deal":
            valid_ae_cta = (
                cta_type == "url"
                and cta_label == "Continue to the Deal Room"
            ) or (
                cta_type == "mailto"
                and cta_label == "Reply to the Seller"
            )
            if not valid_ae_cta:
                issues.append(
                    issue(
                        "CTA006",
                        "AE active-deal pages require 'Continue to the Deal Room' or 'Reply to the Seller'.",
                    )
                )
            if cta_type == "mailto":
                address = normalized_destination.removeprefix("mailto:")
                if not seller_email or address.casefold() != seller_email.casefold():
                    issues.append(
                        issue(
                            "CTA007",
                            "Reply-to-seller CTA must use the seller email from the brief.",
                        )
                    )

        requested_delivery = get_path(
            brief,
            "seller_inputs.page_goal.requested_delivery",
            "",
        )
        if requested_delivery == "public_share" and seller_motion != "ae_active_deal":
            issues.append(
                issue(
                    "GATE017",
                    "Public deployment authorization is limited to the AE active-deal path.",
                )
            )

    permissions = get_path(brief, "research_policy.source_permissions", [])
    if not isinstance(permissions, list):
        permissions = []
    permission_sources = [
        item.get("source")
        for item in permissions
        if isinstance(item, dict) and item.get("source")
    ]
    missing_sources = SUPPORTED_SOURCES.difference(permission_sources)
    duplicate_sources = {
        source for source, count in Counter(permission_sources).items() if count > 1
    }
    if mode in {"final", "mcp"} and missing_sources:
        issues.append(
            issue(
                "SOURCE001",
                "Source permissions are missing: "
                + ", ".join(sorted(missing_sources))
                + ".",
            )
        )
    if duplicate_sources:
        issues.append(
            issue(
                "SOURCE002",
                "Duplicate source permissions: "
                + ", ".join(sorted(duplicate_sources))
                + ".",
            )
        )

    permission_counts = Counter(permission_sources)
    permission_by_source = {
        item.get("source"): item
        for item in permissions
        if isinstance(item, dict)
        and item.get("source")
        and permission_counts[item.get("source")] == 1
    }

    for permission in permissions:
        if not isinstance(permission, dict):
            issues.append(issue("SOURCE003", "Source permission must be an object."))
            continue
        if permission.get("read") not in {"allow", "deny", "not_available"}:
            issues.append(
                issue(
                    "SOURCE004",
                    f"Source {permission.get('source', 'unknown')} has unresolved read permission.",
                )
            )
        if permission.get("buyer_use") not in {
            "per_item",
            "public_fact",
            "paraphrase_only",
            "strategy_only",
            "exact_use",
            "blocked",
        }:
            issues.append(
                issue(
                    "SOURCE005",
                    f"Source {permission.get('source', 'unknown')} has unresolved buyer-use permission.",
                )
            )

    private_read_enabled = get_path(
        brief,
        "research_policy.stage2_may_read_private_sources",
        False,
    )
    allowed_private_sources = {
        source
        for source in PRIVATE_CONTEXT_SOURCES
        if permission_by_source.get(source, {}).get("read") == "allow"
    }
    if mode in {"final", "mcp"}:
        if seller_motion == "sdr_net_new" and private_read_enabled:
            issues.append(
                issue(
                    "SOURCE012",
                    "The SDR net-new path must not enable private-context refreshes.",
                )
            )
        if not private_read_enabled and allowed_private_sources:
            issues.append(
                issue(
                    "SOURCE013",
                    "Private sources are marked readable while private-source refresh is disabled.",
                )
            )
        if private_read_enabled and not allowed_private_sources:
            issues.append(
                issue(
                    "SOURCE017",
                    "Private-source refresh is enabled without an explicitly allowed private source family.",
                )
            )
    source_ledger = get_path(brief, "research_policy.source_ledger", [])
    if not isinstance(source_ledger, list):
        source_ledger = []
    source_ids = {
        item.get("source_id")
        for item in source_ledger
        if isinstance(item, dict) and item.get("source_id")
    }
    source_id_values = [
        item.get("source_id")
        for item in source_ledger
        if isinstance(item, dict) and item.get("source_id")
    ]
    duplicate_source_ids = {
        source_id
        for source_id, count in Counter(source_id_values).items()
        if count > 1
    }
    if duplicate_source_ids:
        issues.append(
            issue(
                "SOURCE009",
                "Duplicate source ledger IDs: "
                + ", ".join(sorted(duplicate_source_ids))
                + ".",
            )
        )
    source_by_id = {
        item.get("source_id"): item
        for item in source_ledger
        if isinstance(item, dict) and item.get("source_id")
    }
    for source in source_ledger:
        if not isinstance(source, dict):
            issues.append(issue("SOURCE006", "Source ledger entry must be an object."))
            continue
        if source.get("confidence") not in {"high", "medium", "low"}:
            issues.append(
                issue(
                    "SOURCE007",
                    f"Source {source.get('source_id', 'unknown')!r} needs a confidence level.",
                )
            )
        source_id = source.get("source_id", "unknown")
        source_type = source.get("source_type")
        source_permission = permission_by_source.get(source_type)
        if source_permission is None:
            issues.append(
                issue(
                    "SOURCE010",
                    f"Source {source_id!r} has no unique source-level permission.",
                )
            )
        elif source_permission.get("read") != "allow":
            issues.append(
                issue(
                    "SOURCE010",
                    f"Source {source_id!r} comes from a denied or unavailable source.",
                )
            )
        else:
            allowed_uses = PERMISSION_USE_COMPATIBILITY.get(
                str(source_permission.get("buyer_use")),
                set(),
            )
            if source.get("buyer_use") not in allowed_uses:
                issues.append(
                    issue(
                        "SOURCE011",
                        f"Source {source_id!r} exceeds its source-level buyer-use permission.",
                    )
                )
        if (
            source_type in PRIVATE_CONTEXT_SOURCES
            and (
                seller_motion != "ae_active_deal"
                or private_read_enabled is not True
            )
        ):
            issues.append(
                issue(
                    "SOURCE014",
                    f"Private source {source_id!r} is only allowed in an authorized AE active-deal intake.",
                )
            )
        if (
            (
                source_type in PRIVATE_CONTEXT_SOURCES
                or source.get("classification") != "public"
            )
            and source.get("buyer_use") == "exact_use"
            and (
                not nonempty(source.get("approved_by"))
                or not nonempty(source.get("approved_at"))
            )
        ):
            issues.append(
                issue(
                    "SOURCE008",
                    f"Private exact-use source {source.get('source_id', 'unknown')!r} lacks item approval.",
                )
            )
        if (
            source_type in PRIVATE_CONTEXT_SOURCES
            and source.get("classification") == "public"
        ):
            issues.append(
                issue(
                    "SOURCE018",
                    f"Private source {source_id!r} cannot be classified as public.",
                )
            )
        if source.get("buyer_use") == "exact_use":
            exact_facts = source.get("extracted_facts", [])
            if (
                not isinstance(exact_facts, list)
                or len(exact_facts) != 1
                or not nonempty(exact_facts[0])
            ):
                issues.append(
                    issue(
                        "SOURCE015",
                        f"Exact-use source {source_id!r} must represent exactly one item-approved fact.",
                    )
                )
        if nonempty(source.get("approved_at")) and parse_rfc3339(
            source.get("approved_at")
        ) is None:
            issues.append(
                issue(
                    "SOURCE016",
                    f"Source {source_id!r} approval time must be RFC3339.",
                )
            )

    if mode in {"final", "mcp"}:
        account_accent = get_path(
            brief,
            "seller_inputs.visual_preferences.account_accent",
            {},
        )
        if not isinstance(account_accent, dict):
            issues.append(issue("BRAND001", "Account accent must be an approved object."))
        else:
            accent_mode = account_accent.get("mode")
            accent_hex = str(account_accent.get("hex", "")).strip()
            accent_source_id = str(account_accent.get("source_id", "")).strip()
            accent_source_fact = canonical_display_text(
                account_accent.get("source_fact", "")
            )
            if accent_mode not in {"folloze_default", "verified_prospect"}:
                issues.append(issue("BRAND002", "Account accent mode is not supported."))
            if not re.fullmatch(r"#[0-9A-Fa-f]{6}", accent_hex):
                issues.append(
                    issue("BRAND003", "Account accent requires one exact six-digit hex value.")
                )
            accent_source = source_by_id.get(accent_source_id)
            if not accent_source_id or accent_source is None:
                issues.append(
                    issue("BRAND004", "Account accent requires an approved source-ledger ID.")
                )
            elif accent_source.get("buyer_use") not in BUYER_VISIBLE_USES:
                issues.append(
                    issue("BRAND005", "Account accent source is not approved for buyer-visible use.")
                )
            elif (
                accent_mode == "folloze_default"
                and accent_source.get("source_type")
                not in {"skill_reference", "public_web"}
            ):
                issues.append(
                    issue(
                        "BRAND006",
                        "The Folloze default accent must come from an approved brand-kit or public-site source.",
                    )
                )
            if accent_source is not None:
                extracted_facts = {
                    canonical_display_text(fact)
                    for fact in accent_source.get("extracted_facts", [])
                    if isinstance(fact, str) and canonical_display_text(fact)
                }
                if not accent_source_fact or accent_source_fact not in extracted_facts:
                    issues.append(
                        issue(
                            "BRAND008",
                            "Account accent must cite one exact extracted source fact.",
                        )
                    )
                fact_hexes = re.findall(
                    r"#[0-9A-Fa-f]{6}(?![0-9A-Fa-f])",
                    accent_source_fact,
                )
                if (
                    len(fact_hexes) != 1
                    or not re.fullmatch(r"#[0-9A-Fa-f]{6}", accent_hex)
                    or fact_hexes[0].casefold() != accent_hex.casefold()
                ):
                    issues.append(
                        issue(
                            "BRAND009",
                            "Account accent source fact must contain exactly the approved hex.",
                        )
                    )

    proof_registry, proof_registry_issues = build_approved_content_registry(
        brief,
        "proof",
    )
    claim_registry, claim_registry_issues = build_approved_content_registry(
        brief,
        "claim",
    )
    issues.extend(proof_registry_issues)
    issues.extend(claim_registry_issues)
    approved_proof_ids = {
        canonical_display_text(value)
        for value in (
            get_path(brief, "claims_policy.approved_proof_ids", []) or []
        )
        if isinstance(value, str) and canonical_display_text(value)
    }
    approved_claim_ids = {
        canonical_display_text(value)
        for value in (
            get_path(brief, "claims_policy.approved_claim_ids", []) or []
        )
        if isinstance(value, str) and canonical_display_text(value)
    }
    blocked_claims = {
        canonical_display_text(value)
        for value in (get_path(brief, "claims_policy.blocked_claims", []) or [])
        if isinstance(value, str) and canonical_display_text(value)
    }
    forbidden_topics = {
        canonical_display_text(value)
        for value in (
            get_path(
                brief,
                "seller_inputs.business_context.forbidden_topics",
                [],
            )
            or []
        )
        if isinstance(value, str) and canonical_display_text(value)
    }
    if mode in {"final", "mcp"}:
        if set(proof_registry) != approved_proof_ids:
            issues.append(
                issue(
                    "CONTENT007",
                    "Approved proof ID list and proof-content registry do not match.",
                )
            )
        if set(claim_registry) != approved_claim_ids:
            issues.append(
                issue(
                    "CONTENT008",
                    "Approved claim ID list and claim-content registry do not match.",
                )
            )
        blocked_approved_ids = blocked_claims.intersection(
            approved_proof_ids | approved_claim_ids
        )
        if blocked_approved_ids:
            issues.append(
                issue(
                    "CONTENT015",
                    "Blocked claim IDs are also approved: "
                    + ", ".join(sorted(blocked_approved_ids))
                    + ".",
                )
            )
        prohibited_constraint_terms = {
            canonical_display_text(value).casefold()
            for value in (
                get_path(
                    brief,
                    "stage2_handoff.constraints.prohibited_visible_terms",
                    [],
                )
                or []
            )
            if isinstance(value, str) and canonical_display_text(value)
        }
        missing_forbidden_constraints = {
            value
            for value in forbidden_topics
            if value.casefold() not in prohibited_constraint_terms
        }
        if missing_forbidden_constraints:
            issues.append(
                issue(
                    "CONTENT016",
                    "Seller-forbidden topics are missing from Stage 2 prohibited terms: "
                    + ", ".join(sorted(missing_forbidden_constraints))
                    + ".",
                )
            )
        approved_copy_values = {
            text
            for registry in (proof_registry, claim_registry)
            for record in registry.values()
            for text in record["texts"]
        }
        approved_copy_values.update(
            canonical_display_text(row.get("buyer_safe_claim", ""))
            for row in (get_path(brief, "normalized_brief.message_fit_matrix", []) or [])
            if isinstance(row, dict)
            and canonical_display_text(row.get("buyer_safe_claim", ""))
        )
        approved_copy_values.add(
            canonical_display_text(
                get_path(brief, "seller_inputs.page_goal.meta_description", "")
            )
        )
        restricted_phrases = forbidden_topics | blocked_claims
        for restricted_phrase in sorted(restricted_phrases):
            if any(
                restricted_phrase.casefold() in approved_copy.casefold()
                for approved_copy in approved_copy_values
                if approved_copy
            ):
                issues.append(
                    issue(
                        "CONTENT017",
                        f"Approved buyer copy contains blocked or forbidden phrase {restricted_phrase!r}.",
                    )
                )
        for kind, registry in (
            ("proof", proof_registry),
            ("claim", claim_registry),
        ):
            for content_id, record in registry.items():
                for source_id in sorted(record["source_ids"]):
                    ledger_entry = source_by_id.get(source_id)
                    if ledger_entry is None:
                        issues.append(
                            issue(
                                "CONTENT009",
                                f"Approved {kind} content {content_id!r} references unknown source {source_id!r}.",
                            )
                        )
                    elif ledger_entry.get("buyer_use") not in BUYER_VISIBLE_USES:
                        issues.append(
                            issue(
                                "CONTENT010",
                                f"Approved {kind} content {content_id!r} references non-visible source {source_id!r}.",
                            )
                        )

    message_rows = get_path(brief, "normalized_brief.message_fit_matrix", [])
    if not isinstance(message_rows, list):
        message_rows = []
    for row in message_rows:
        if not isinstance(row, dict):
            issues.append(issue("MATRIX001", "Message-fit row must be an object."))
            continue
        source_id = row.get("source_id", "")
        if mode in {"final", "mcp"} and source_id not in source_ids:
            issues.append(
                issue(
                    "MATRIX002",
                    f"Message-fit row references unknown source ID {source_id!r}.",
                )
            )
        elif mode in {"final", "mcp"}:
            source = source_by_id.get(source_id, {})
            if source.get("buyer_use") not in BUYER_VISIBLE_USES:
                issues.append(
                    issue(
                        "MATRIX004",
                        f"Message-fit row uses source {source_id!r} that is not buyer-visible.",
                    )
                )
            if row.get("source_use") != source.get("buyer_use"):
                issues.append(
                    issue(
                        "MATRIX005",
                        f"Message-fit row source-use rule does not match ledger source {source_id!r}.",
                    )
                )
            if source.get("buyer_use") == "exact_use":
                raw_exact_texts = source.get("extracted_facts", [])
                if not isinstance(raw_exact_texts, list):
                    raw_exact_texts = []
                approved_exact_texts = {
                    canonical_display_text(value)
                    for value in raw_exact_texts
                    if isinstance(value, str) and canonical_display_text(value)
                }
                buyer_safe_claim = canonical_display_text(
                    row.get("buyer_safe_claim", "")
                )
                if buyer_safe_claim not in approved_exact_texts:
                    issues.append(
                        issue(
                            "MATRIX009",
                            f"Exact-use copy for source {source_id!r} is not present in its item-approved extracted facts.",
                        )
                    )
        if mode in {"final", "mcp"} and not nonempty(
            row.get("buyer_safe_claim")
        ):
            issues.append(
                issue("MATRIX003", "Message-fit row lacks a buyer-safe claim.")
            )
        placement = canonical_display_text(row.get("placement", ""))
        if mode in {"final", "mcp"} and placement not in BUYER_COPY_PLACEMENTS:
            issues.append(
                issue(
                    "MATRIX010",
                    f"Message-fit row has unsupported placement {placement!r}.",
                )
            )
        value_prop_id = row.get("folloze_value_prop_id", "")
        if mode in {"final", "mcp"} and value_prop_id not in approved_claim_ids:
            issues.append(
                issue(
                    "MATRIX006",
                    f"Message-fit row uses unapproved Folloze claim ID {value_prop_id!r}.",
                )
            )
        elif mode in {"final", "mcp"}:
            claim_record = claim_registry.get(str(value_prop_id), {})
            approved_copy = canonical_display_text(
                row.get("buyer_safe_claim", "")
            )
            if approved_copy not in claim_record.get("texts", set()):
                issues.append(
                    issue(
                        "MATRIX007",
                        f"Message-fit copy is not exact-approved under claim ID {value_prop_id!r}.",
                    )
                )
            if source_id not in claim_record.get("source_ids", set()):
                issues.append(
                    issue(
                        "MATRIX008",
                        f"Message-fit source {source_id!r} is not bound to claim ID {value_prop_id!r}.",
                    )
                )

    resource_registry, resource_registry_issues = build_approved_resource_registry(
        brief
    )
    issues.extend(resource_registry_issues)
    if mode in {"final", "mcp"}:
        matrix_pairs = {
            (
                canonical_display_text(row.get("source_id", "")),
                canonical_display_text(row.get("buyer_safe_claim", "")),
                canonical_display_text(row.get("placement", "")),
            )
            for row in message_rows
            if isinstance(row, dict)
            and canonical_display_text(row.get("source_id", ""))
            and canonical_display_text(row.get("buyer_safe_claim", ""))
        }
        meta_description = canonical_display_text(
            get_path(brief, "seller_inputs.page_goal.meta_description", "")
        )
        raw_meta_source_ids = get_path(
            brief,
            "seller_inputs.page_goal.meta_description_source_ids",
            [],
        )
        meta_source_ids = {
            canonical_display_text(value)
            for value in raw_meta_source_ids
            if isinstance(value, str) and canonical_display_text(value)
        } if isinstance(raw_meta_source_ids, list) else set()
        if not meta_source_ids:
            issues.append(
                issue(
                    "META001",
                    "Buyer-safe meta description needs at least one approved source ID.",
                )
            )
        for source_id in sorted(meta_source_ids):
            source = source_by_id.get(source_id)
            if source is None:
                issues.append(
                    issue(
                        "META002",
                        f"Meta description references unknown source {source_id!r}.",
                    )
                )
            elif source.get("buyer_use") not in BUYER_VISIBLE_USES:
                issues.append(
                    issue(
                        "META003",
                        f"Meta description references non-visible source {source_id!r}.",
                    )
                )
            if (source_id, meta_description, "metadata") not in matrix_pairs:
                issues.append(
                    issue(
                        "META004",
                        f"Meta description lacks exact message-fit approval for source {source_id!r}.",
                    )
                )
        if NUMERIC_CLAIM_PATTERN.search(meta_description):
            issues.append(
                issue(
                    "META005",
                    "Meta descriptions cannot contain numeric claims; keep verified metrics in traced proof content.",
                )
            )
        for resource_id, record in resource_registry.items():
            for source_id in sorted(record["source_ids"]):
                source = source_by_id.get(source_id)
                if source is None:
                    issues.append(
                        issue(
                            "RESOURCE013",
                            f"Approved resource {resource_id!r} references unknown source {source_id!r}.",
                        )
                    )
                elif source.get("buyer_use") not in BUYER_VISIBLE_USES:
                    issues.append(
                        issue(
                            "RESOURCE014",
                            f"Approved resource {resource_id!r} references non-visible source {source_id!r}.",
                        )
                    )
                if (source_id, record["label"], "resource") not in matrix_pairs:
                    issues.append(
                        issue(
                            "RESOURCE015",
                            f"Approved resource label {record['label']!r} lacks exact message-fit approval for source {source_id!r}.",
                        )
                    )

    approval = brief.get("approval")
    if not isinstance(approval, dict):
        approval = {}
    if mode in {"final", "mcp"}:
        if approval.get("decision") != "approved":
            issues.append(issue("GATE005", "The normalized brief is not approved."))
        if approval.get("brief_version") != brief_version:
            issues.append(
                issue("GATE006", "Approval version does not match brief version.")
            )
        if not nonempty(approval.get("approved_by")):
            issues.append(issue("GATE007", "Approved brief lacks an approver."))
        if not nonempty(approval.get("approved_at")):
            issues.append(issue("GATE008", "Approved brief lacks an approval time."))
        if not nonempty(approval.get("approval_text")):
            issues.append(issue("GATE013", "Approved brief lacks approval text."))
        if not nonempty(approval.get("approval_digest")):
            issues.append(issue("GATE009", "Approved brief lacks an approval digest."))
        elif not re.fullmatch(
            r"sha256:[a-f0-9]{64}",
            str(approval.get("approval_digest")),
        ):
            issues.append(
                issue(
                    "GATE011",
                    "Approval digest must use sha256:<64 lowercase hex characters>.",
                )
            )
        elif approval.get("approval_digest") != compute_approval_digest(brief):
            issues.append(
                issue(
                    "GATE012",
                    "Approval digest does not match the current brief and source boundary.",
                )
            )
        if approval.get("approved_scope") != "local_build":
            issues.append(
                issue("GATE010", "Intake approval scope must be local_build.")
            )

    handoff = brief.get("stage2_handoff")
    if not isinstance(handoff, dict):
        handoff = {}
    if mode in {"final", "mcp"}:
        if handoff.get("intake_id") != intake_id:
            issues.append(issue("HANDOFF001", "Handoff intake ID does not match."))
        if handoff.get("approved_brief_version") != brief_version:
            issues.append(
                issue("HANDOFF002", "Handoff brief version does not match.")
            )

    preview_approval = handoff.get("preview_approval")
    if not isinstance(preview_approval, dict):
        preview_approval = {}
    if state in PREVIEW_APPROVED_STATES or mode == "mcp":
        if preview_approval.get("decision") != "approved":
            issues.append(
                issue("PREVIEW001", "Local preview has not been approved.")
            )
        if preview_approval.get("brief_version") != brief_version:
            issues.append(
                issue(
                    "PREVIEW007",
                    "Preview approval version does not match the current brief.",
                )
            )
        if not nonempty(preview_approval.get("approved_by")):
            issues.append(issue("PREVIEW002", "Preview approval lacks an approver."))
        if not nonempty(preview_approval.get("approved_at")):
            issues.append(issue("PREVIEW003", "Preview approval lacks a time."))
        if not nonempty(preview_approval.get("approval_text")):
            issues.append(issue("PREVIEW004", "Preview approval lacks approval text."))
        if not re.fullmatch(
            r"sha256:[a-f0-9]{64}",
            str(preview_approval.get("html_digest", "")),
        ):
            issues.append(
                issue(
                    "PREVIEW005",
                    "Preview HTML digest must use sha256:<64 lowercase hex characters>.",
                )
            )

    mcp_state = handoff.get("mcp_state")
    if not isinstance(mcp_state, dict):
        mcp_state = {}
    if mode == "mcp" and state not in MCP_AUTHORIZED_STATES:
        issues.append(
            issue("MCP001", "MCP mode requires explicit save authorization.")
        )
    if state in MCP_AUTHORIZED_STATES or mode == "mcp":
        if mcp_state.get("save_intent") not in {"net_new", "update"}:
            issues.append(
                issue("MCP002", "MCP save intent must be net_new or update.")
            )
        if not nonempty(mcp_state.get("save_authorized_by")):
            issues.append(issue("MCP007", "MCP authorization lacks an approver."))
        if not nonempty(mcp_state.get("save_authorized_at")):
            issues.append(issue("MCP008", "MCP authorization lacks a time."))
        if not nonempty(mcp_state.get("save_authorization_text")):
            issues.append(
                issue("MCP009", "MCP authorization lacks the explicit instruction.")
            )
        authorization_digest = str(
            mcp_state.get("authorization_digest", "")
        )
        if not re.fullmatch(r"sha256:[a-f0-9]{64}", authorization_digest):
            issues.append(
                issue(
                    "MCP023",
                    "MCP authorization digest must use sha256:<64 lowercase hex characters>.",
                )
            )
        elif authorization_digest != compute_mcp_authorization_digest(brief):
            issues.append(
                issue(
                    "MCP024",
                    "MCP authorization digest does not match the approved save request.",
                )
            )
        if mcp_state.get("theme_mode") not in {"yes", "no"}:
            issues.append(issue("MCP003", "MCP theme mode is unresolved."))
        if mcp_state.get("theme_authorized") is not True:
            issues.append(issue("MCP004", "MCP theme mode is not authorized."))
        theme_url = mcp_state.get("theme_url") or ""
        if not is_http_url(theme_url):
            issues.append(issue("MCP005", "MCP theme URL is missing or invalid."))
        if not nonempty(mcp_state.get("theme_id")):
            issues.append(issue("MCP015", "MCP theme ID is required."))
        if not nonempty(mcp_state.get("board_name")):
            issues.append(issue("MCP016", "MCP board name is required."))
        if not nonempty(mcp_state.get("local_html_path")):
            issues.append(issue("MCP017", "MCP local HTML path is required."))
        if mcp_state.get("qa_status") != "ready":
            issues.append(
                issue("MCP018", "MCP save requires qa_status ready.")
            )
        if (
            mcp_state.get("save_intent") == "update"
            and not nonempty(mcp_state.get("board_id"))
        ):
            issues.append(
                issue("MCP006", "Existing-board update requires a board ID.")
            )

    if state in MCP_SAVED_STATES:
        if not nonempty(mcp_state.get("board_id")):
            issues.append(issue("MCP025", "Saved MCP state requires a board ID."))
        if not is_http_url(str(mcp_state.get("designer_url") or "")):
            issues.append(
                issue("MCP026", "Saved MCP state requires a designer URL.")
            )
        if mcp_state.get("save_result_status") != "saved":
            issues.append(
                issue("MCP050", "Saved MCP state requires a recorded save result.")
            )
        for field, label in {
            "save_result_recorded_by": "recorder",
            "save_result_recorded_at": "result time",
            "save_result_evidence": "MCP response evidence",
        }.items():
            if not nonempty(mcp_state.get(field)):
                issues.append(
                    issue("MCP051", f"Saved MCP result lacks its {label}.")
                )
        if canonical_display_text(
            mcp_state.get("save_result_account_name", "")
        ) != canonical_display_text(
            get_path(brief, "seller_inputs.prospect.account_name", "")
        ):
            issues.append(
                issue(
                    "MCP052",
                    "Saved MCP result account differs from the approved prospect.",
                )
            )
        if mcp_state.get("save_result_board_id") != mcp_state.get("board_id"):
            issues.append(
                issue(
                    "MCP053",
                    "Saved MCP result board ID differs from the canonical board ID.",
                )
            )
        if mcp_state.get("save_result_designer_url") != mcp_state.get(
            "designer_url"
        ):
            issues.append(
                issue(
                    "MCP054",
                    "Saved MCP result designer URL differs from the canonical designer URL.",
                )
            )
        save_result_digest = str(mcp_state.get("save_result_digest", ""))
        if not re.fullmatch(r"sha256:[a-f0-9]{64}", save_result_digest):
            issues.append(
                issue(
                    "MCP055",
                    "MCP save-result digest must use sha256:<64 lowercase hex characters>.",
                )
            )
        elif save_result_digest != compute_mcp_save_result_digest(brief):
            issues.append(
                issue(
                    "MCP056",
                    "MCP save-result digest does not match the approved HTML, authorization, account, and returned result.",
                )
            )
    else:
        stale_save_result = (
            mcp_state.get("save_result_status") != "not_recorded"
            or nonempty(mcp_state.get("save_result_recorded_by"))
            or nonempty(mcp_state.get("save_result_recorded_at"))
            or nonempty(mcp_state.get("save_result_account_name"))
            or mcp_state.get("save_result_board_id") is not None
            or mcp_state.get("save_result_designer_url") is not None
            or nonempty(mcp_state.get("save_result_evidence"))
            or nonempty(mcp_state.get("save_result_digest"))
        )
        if stale_save_result:
            issues.append(
                issue(
                    "MCP057",
                    "MCP save-result evidence must be empty until an MCP-saved state.",
                )
            )

    if state in PUBLIC_AUTHORIZED_STATES:
        if seller_motion != "ae_active_deal":
            issues.append(
                issue(
                    "MCP027",
                    "Public deployment is limited to the AE active-deal path.",
                )
            )
        public_auth_fields = {
            "public_deployment_authorized_by": "approver",
            "public_deployment_authorized_at": "time",
            "public_deployment_authorization_text": "instruction",
        }
        for field, label in public_auth_fields.items():
            if not nonempty(mcp_state.get(field)):
                issues.append(
                    issue(
                        "MCP029",
                        f"Public deployment authorization lacks its {label}.",
                    )
                )
        public_digest = str(
            mcp_state.get("public_deployment_authorization_digest", "")
        )
        if not re.fullmatch(r"sha256:[a-f0-9]{64}", public_digest):
            issues.append(
                issue(
                    "MCP030",
                    "Public deployment digest must use sha256:<64 lowercase hex characters>.",
                )
            )
        elif public_digest != compute_public_deployment_authorization_digest(
            brief
        ):
            issues.append(
                issue(
                    "MCP031",
                    "Public deployment digest does not match the authorized board and instruction.",
                )
            )
    elif any(
        nonempty(mcp_state.get(field))
        for field in (
            "public_deployment_authorized_by",
            "public_deployment_authorized_at",
            "public_deployment_authorization_text",
            "public_deployment_authorization_digest",
        )
    ):
        issues.append(
            issue(
                "MCP049",
                "Public-deployment authorization fields must be empty outside an authorized public state.",
            )
        )

    if state == "public_verified":
        if mcp_state.get("public_url_status") != "verified":
            issues.append(
                issue("MCP032", "public_verified requires verified URL status.")
            )
        if not is_http_url(str(mcp_state.get("public_url") or "")):
            issues.append(
                issue("MCP033", "public_verified requires a valid public URL.")
            )
        if mcp_state.get("public_verification_method") not in {
            "folloze_readback",
            "public_http_readback",
        }:
            issues.append(
                issue(
                    "MCP042",
                    "public_verified requires a Folloze or public HTTP readback method.",
                )
            )
        for field, label in {
            "public_verified_by": "verifier",
            "public_verified_at": "verification time",
            "public_verification_evidence": "readback evidence",
        }.items():
            if not nonempty(mcp_state.get(field)):
                issues.append(
                    issue(
                        "MCP043",
                        f"public_verified lacks its {label}.",
                    )
                )
        approved_account_name = canonical_display_text(
            get_path(brief, "seller_inputs.prospect.account_name", "")
        )
        if canonical_display_text(
            mcp_state.get("public_verification_account_name", "")
        ) != approved_account_name:
            issues.append(
                issue(
                    "MCP044",
                    "Public readback account name differs from the approved prospect.",
                )
            )
        if mcp_state.get("public_verification_board_id") != mcp_state.get(
            "board_id"
        ):
            issues.append(
                issue(
                    "MCP045",
                    "Public readback board ID differs from the saved Folloze board.",
                )
            )
        public_verification_digest = str(
            mcp_state.get("public_verification_digest", "")
        )
        if not re.fullmatch(
            r"sha256:[a-f0-9]{64}",
            public_verification_digest,
        ):
            issues.append(
                issue(
                    "MCP046",
                    "Public verification digest must use sha256:<64 lowercase hex characters>.",
                )
            )
        elif public_verification_digest != compute_public_verification_digest(
            brief
        ):
            issues.append(
                issue(
                    "MCP047",
                    "Public verification digest does not match the recorded URL readback.",
                )
            )
    else:
        stale_public_verification = (
            mcp_state.get("public_verification_method") != "not_run"
            or nonempty(mcp_state.get("public_verified_by"))
            or nonempty(mcp_state.get("public_verified_at"))
            or nonempty(mcp_state.get("public_verification_account_name"))
            or mcp_state.get("public_verification_board_id") is not None
            or nonempty(mcp_state.get("public_verification_evidence"))
            or nonempty(mcp_state.get("public_verification_digest"))
        )
        if stale_public_verification:
            issues.append(
                issue(
                    "MCP048",
                    "Public verification evidence must be empty until the public_verified state.",
                )
            )

    public_url_status = mcp_state.get("public_url_status")
    public_url = str(mcp_state.get("public_url") or "")
    if public_url_status in {"returned", "user_supplied", "verified"}:
        if state not in PUBLIC_AUTHORIZED_STATES:
            issues.append(
                issue(
                    "MCP036",
                    "A returned, supplied, or verified public URL requires an authorized public-deployment state.",
                )
            )
        if not is_http_url(public_url):
            issues.append(
                issue(
                    "MCP037",
                    "A returned, supplied, or verified public URL status requires a valid URL.",
                )
            )
    if public_url_status == "verified" and state != "public_verified":
        issues.append(
            issue(
                "MCP038",
                "Verified public URL status requires the public_verified state.",
            )
        )
    if public_url_status == "pending" and public_url:
        issues.append(
            issue(
                "MCP039",
                "Pending public URL status must not retain a public URL.",
            )
        )

    if mcp_state.get("manual_share_status") == "seller_reported_shared":
        if state != "public_verified":
            issues.append(
                issue(
                    "MCP034",
                    "Manual sharing can be recorded only after public verification.",
                )
            )
        if not nonempty(mcp_state.get("manual_share_reported_by")) or not nonempty(
            mcp_state.get("manual_share_reported_at")
        ):
            issues.append(
                issue(
                    "MCP035",
                    "Seller-reported manual sharing requires reporter and timestamp.",
                )
            )
        manual_share_reporter = canonical_display_text(
            mcp_state.get("manual_share_reported_by", "")
        ).casefold()
        approved_reporters = {
            canonical_display_text(
                get_path(brief, "seller_inputs.seller.name", "")
            ).casefold(),
            canonical_display_text(
                get_path(brief, "seller_inputs.seller.email", "")
            ).casefold(),
        }
        approved_reporters.discard("")
        if manual_share_reporter not in approved_reporters:
            issues.append(
                issue(
                    "MCP041",
                    "Manual sharing reporter must exactly match the approved seller name or email.",
                )
            )
    elif mcp_state.get("manual_share_status") == "not_shared" and (
        nonempty(mcp_state.get("manual_share_reported_by"))
        or nonempty(mcp_state.get("manual_share_reported_at"))
    ):
        issues.append(
            issue(
                "MCP040",
                "not_shared status must not retain a manual-share reporter or timestamp.",
            )
        )

    audit_time_fields = [
        ("intake approval", "approval.approved_at"),
        ("preview approval", "stage2_handoff.preview_approval.approved_at"),
        ("MCP save authorization", "stage2_handoff.mcp_state.save_authorized_at"),
        ("MCP save result", "stage2_handoff.mcp_state.save_result_recorded_at"),
        (
            "public deployment authorization",
            "stage2_handoff.mcp_state.public_deployment_authorized_at",
        ),
        ("public verification", "stage2_handoff.mcp_state.public_verified_at"),
        ("manual sharing", "stage2_handoff.mcp_state.manual_share_reported_at"),
    ]
    parsed_audit_times: list[tuple[str, datetime]] = []
    for label, path in audit_time_fields:
        raw_time = get_path(brief, path, "")
        if not nonempty(raw_time):
            continue
        parsed_time = parse_rfc3339(raw_time)
        if parsed_time is None:
            issues.append(
                issue("TIME001", f"{label.capitalize()} time must be RFC3339.")
            )
            continue
        parsed_audit_times.append((label, parsed_time))
    for (earlier_label, earlier_time), (later_label, later_time) in zip(
        parsed_audit_times,
        parsed_audit_times[1:],
    ):
        if later_time < earlier_time:
            issues.append(
                issue(
                    "TIME002",
                    f"{later_label.capitalize()} cannot precede {earlier_label}.",
                )
            )

    return issues


def validate_document_basics(
    raw_html: str,
    parser: PageParser,
    profile: str,
    mode: str,
) -> list[Issue]:
    issues: list[Issue] = []
    if not re.match(r"\s*<!doctype\s+html", raw_html, flags=re.IGNORECASE):
        issues.append(issue("HTML001", "Missing HTML5 doctype."))
    if not parser.html_attrs.get("lang"):
        issues.append(issue("HTML002", "The html element needs a lang attribute."))
    if not parser.title.strip():
        issues.append(issue("HTML003", "The document needs a non-empty title."))
    if not parser.has_viewport:
        issues.append(issue("HTML004", "Missing viewport meta tag."))
    if not parser.has_description:
        issues.append(issue("HTML005", "Missing non-empty meta description."))
    singular_document_tags = {"html", "head", "body", "title", "style"}
    invalid_document_tag_counts = {
        tag: sum(1 for element in parser.elements if element.tag == tag)
        for tag in singular_document_tags
        if sum(1 for element in parser.elements if element.tag == tag) != 1
    }
    if profile == "microsite" and invalid_document_tag_counts:
        issues.append(
            issue(
                "HTML014",
                "Microsite document-shell tags must appear exactly once: "
                + ", ".join(
                    f"{tag}={count}"
                    for tag, count in sorted(invalid_document_tag_counts.items())
                )
                + ".",
            )
        )
    meta_elements = [
        element for element in parser.elements if element.tag == "meta"
    ]
    charset_meta = [
        element
        for element in meta_elements
        if set(element.attrs) == {"charset"}
        and element.attrs.get("charset", "").casefold() == "utf-8"
    ]
    viewport_meta = [
        element
        for element in meta_elements
        if element.attrs
        == {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
    description_meta = [
        element
        for element in meta_elements
        if set(element.attrs) == {"name", "content"}
        and element.attrs.get("name", "").casefold() == "description"
        and bool(element.attrs.get("content", "").strip())
    ]
    if profile == "microsite" and (
        len(meta_elements) != 3
        or len(charset_meta) != 1
        or len(viewport_meta) != 1
        or len(description_meta) != 1
    ):
        issues.append(
            issue(
                "HTML010",
                "Head metadata must contain only the trusted charset, viewport, and one approved description entry.",
            )
        )
    head_content = [
        element
        for element in parser.elements
        if element.tag in {"meta", "title", "style"}
    ]
    if profile == "microsite" and any(
        not element.in_head for element in head_content
    ):
        issues.append(
            issue(
                "HTML015",
                "Charset, viewport, description, title, and style must remain inside <head>.",
            )
        )
    if profile == "microsite":
        stripped_comments = [comment.strip() for comment in parser.comments]
        marker_comment_pattern = re.compile(
            r"(?:OPTIONAL|CTA):[a-z0-9_]+:(?:START|END)",
            flags=re.IGNORECASE,
        )
        if mode == "template":
            unexpected_comments = [
                comment
                for comment in stripped_comments
                if comment != TRUSTED_THEME_SLOT_COMMENT
                and not marker_comment_pattern.fullmatch(comment)
            ]
            if unexpected_comments:
                issues.append(
                    issue(
                        "HTML011",
                        "Microsite template contains an untrusted HTML comment.",
                    )
                )
        elif mode == "final" and stripped_comments != [TRUSTED_THEME_SLOT_COMMENT]:
            issues.append(
                issue(
                    "HTML012",
                    "Final local HTML may retain only the canonical Folloze theme-slot comment.",
                )
            )
        elif mode == "mcp" and stripped_comments:
            issues.append(
                issue(
                    "HTML013",
                    "MCP-ready HTML must not contain HTML comments.",
                )
            )

    token_pattern = re.compile(r"\[\[([A-Z0-9_]+)\]\]")
    template_tokens = set(token_pattern.findall(raw_html))
    if mode == "template" and profile == "microsite":
        missing = EXPECTED_TEMPLATE_TOKENS.difference(template_tokens)
        unexpected = template_tokens.difference(EXPECTED_TEMPLATE_TOKENS)
        if missing:
            issues.append(
                issue(
                    "TOKEN001",
                    "Template tokens missing: " + ", ".join(sorted(missing)) + ".",
                )
            )
        if unexpected:
            issues.append(
                issue(
                    "TOKEN002",
                    "Unexpected template tokens: "
                    + ", ".join(sorted(unexpected))
                    + ".",
                )
            )
    else:
        unresolved_patterns = [
            (r"\[\[[A-Z0-9_]+\]\]", "[[TOKEN]]"),
            (r"\{\{[^{}]+\}\}", "{{TOKEN}}"),
            (r"\[PROOF\]", "[PROOF]"),
            (r"\b(?:TBD|TK)\b", "TBD/TK"),
            (r"lorem\s+ipsum", "Lorem Ipsum"),
        ]
        for pattern, label in unresolved_patterns:
            if re.search(pattern, raw_html, flags=re.IGNORECASE):
                issues.append(
                    issue("TOKEN003", f"Final HTML contains unresolved {label}.")
                )
        if re.search(r"<!--\s*(?:OPTIONAL|CTA):", raw_html):
            issues.append(
                issue(
                    "TOKEN004",
                    "Final HTML contains unprocessed renderer block markers.",
                )
            )

    duplicate_ids = sorted(
        element_id for element_id, count in parser.ids.items() if count > 1
    )
    if duplicate_ids:
        issues.append(
            issue(
                "HTML006",
                "Duplicate IDs: " + ", ".join(duplicate_ids) + ".",
            )
        )
    if parser.duplicate_attributes:
        duplicate_attributes = sorted(
            {f"<{tag}>[{attribute}]" for tag, attribute in parser.duplicate_attributes}
        )
        issues.append(
            issue(
                "HTML007",
                "Duplicate HTML attributes are not allowed: "
                + ", ".join(duplicate_attributes)
                + ".",
            )
        )
    return issues


def validate_microsite_structure(
    raw_html: str,
    parser: PageParser,
    brief: dict[str, Any] | None,
    mode: str,
    html_path: Path | None = None,
) -> list[Issue]:
    issues: list[Issue] = []

    if parser.html_attrs.get("data-template") != "folloze-prospect-one-pager":
        issues.append(issue("STRUCT001", "Missing one-pager template identifier."))
    if parser.h1_count != 1:
        issues.append(issue("STRUCT002", "Microsite must contain exactly one H1."))

    main_elements = [
        element
        for element in parser.elements
        if element.tag == "main" and element.attrs.get("id") == "main"
    ]
    if len(main_elements) != 1:
        issues.append(issue("STRUCT003", "Microsite needs exactly one main#main."))

    headers = [
        element
        for element in parser.elements
        if element.attrs.get("data-component") == "site-header"
    ]
    if len(headers) != 1:
        issues.append(issue("STRUCT004", "Missing stable site-header component."))
    if not parser.elements_by_role("folloze-logo"):
        issues.append(issue("STRUCT005", "Missing Folloze logo role."))
    if len(parser.elements_by_role("account-name")) != 2:
        issues.append(
            issue(
                "STRUCT006",
                "Microsite requires exactly the two trusted prospect-name fallbacks.",
            )
        )

    required_section_ids = {"promise", "path", "next-step"}
    missing_sections = required_section_ids.difference(parser.ids)
    if missing_sections:
        issues.append(
            issue(
                "STRUCT007",
                "Required sections missing: "
                + ", ".join(sorted(missing_sections))
                + ".",
            )
        )
    canonical_section_order = ["promise", "proof", "path", "next-step"]
    section_elements = [
        element for element in parser.elements if element.tag == "section"
    ]
    if (
        [element.attrs.get("id", "") for element in section_elements]
        != canonical_section_order
        or any(
            element.parent_tag != "main" or element.parent_id != "main"
            for element in section_elements
        )
    ):
        issues.append(
            issue(
                "STRUCT008",
                "Microsite sections must be exactly Promise, Proof, Path, and Next step as direct children of main#main in that order.",
            )
        )

    style_text = parser.style_text
    for css_token in sorted(REQUIRED_CSS_TOKENS):
        if not re.search(rf"{re.escape(css_token)}\s*:", style_text):
            issues.append(issue("CSS001", f"Missing CSS token {css_token}."))
    if ":focus-visible" not in style_text:
        issues.append(issue("A11Y001", "Missing visible focus treatment."))
    if "prefers-reduced-motion" not in style_text:
        issues.append(issue("A11Y002", "Missing reduced-motion CSS."))
    if re.search(r"transition\s*:\s*all\b", style_text, flags=re.IGNORECASE):
        issues.append(issue("CSS002", "Do not use transition: all."))
    if re.search(r"@import\b", style_text, flags=re.IGNORECASE):
        issues.append(issue("CSS004", "Remote CSS imports are not allowed."))
    if re.search(
        r"url\(\s*['\"]?(?:https?:)?//",
        style_text,
        flags=re.IGNORECASE,
    ):
        issues.append(issue("CSS005", "Remote CSS URL assets are not allowed."))
    accent_match = re.search(
        r"--color-account-accent\s*:\s*([^;]+);",
        style_text,
        flags=re.IGNORECASE,
    )
    if (
        accent_match
        and mode != "template"
        and not re.fullmatch(r"#[0-9a-fA-F]{6}", accent_match.group(1).strip())
    ):
        issues.append(
            issue("CSS003", "Account accent must be a six-digit hex color.")
        )
    if accent_match and mode != "template" and brief is not None:
        approved_accent = str(
            get_path(
                brief,
                "seller_inputs.visual_preferences.account_accent.hex",
                "",
            )
        ).strip()
        if (
            re.fullmatch(r"#[0-9A-Fa-f]{6}", approved_accent)
            and accent_match.group(1).strip().casefold()
            != approved_accent.casefold()
        ):
            issues.append(
                issue(
                    "BRAND007",
                    "Rendered account accent differs from the approved intake value.",
                )
            )
    expected_style, trusted_style_issue = trusted_microsite_style()
    if trusted_style_issue is not None:
        issues.append(trusted_style_issue)
    elif normalize_trusted_style(style_text) != expected_style:
        issues.append(
            issue(
                "CSS008",
                "Microsite CSS differs from the trusted template outside the approved account accent.",
            )
        )

    script_text = parser.script_text
    if "prefers-reduced-motion" not in script_text:
        issues.append(issue("A11Y003", "Missing reduced-motion interaction logic."))
    if "scrollIntoView" not in script_text:
        issues.append(issue("NAV001", "Missing shell-safe scroll behavior."))
    if not re.search(r"flzAnalytic\(\s*['\"]anchor_click['\"]", script_text):
        issues.append(issue("NAV002", "Missing anchor_click analytics."))
    if re.search(r"location\.hash", raw_html):
        issues.append(issue("NAV003", "location.hash is unsafe in Folloze pages."))

    inline_scripts = [
        element
        for element in parser.elements
        if element.tag == "script" and not element.attrs.get("src")
    ]
    if len(inline_scripts) != 1:
        issues.append(
            issue("SCRIPT001", "Microsite must contain exactly one inline script.")
        )
    if re.search(r"\b(?:eval|document\.write|new\s+Function)\s*\(", script_text):
        issues.append(issue("SCRIPT002", "Unsafe dynamic script execution is not allowed."))
    expected_script, trusted_script_issue = trusted_microsite_script()
    if trusted_script_issue is not None:
        issues.append(trusted_script_issue)
    elif script_text.strip() != expected_script:
        issues.append(
            issue(
                "SCRIPT007",
                "Inline script differs from the trusted one-pager interaction script.",
            )
        )

    for element in parser.elements:
        attrs = element.attrs
        if element.tag not in ALLOWED_MICROSITE_TAGS:
            issues.append(
                issue(
                    "HTML008",
                    f"Element <{element.tag}> is not allowed in the microsite template.",
                )
            )
        allowed_attributes = ALLOWED_ATTRIBUTES_BY_TAG.get(element.tag, set())
        unexpected_attributes = set(attrs).difference(allowed_attributes)
        if unexpected_attributes:
            issues.append(
                issue(
                    "HTML009",
                    f"Unexpected attribute(s) on <{element.tag}>: "
                    + ", ".join(sorted(unexpected_attributes))
                    + ".",
                )
            )
        unexpected_url_attributes = UNEXPECTED_URL_ATTRIBUTES.intersection(attrs)
        if unexpected_url_attributes:
            issues.append(
                issue(
                    "ASSET003",
                    f"Unexpected URL-bearing attribute(s) on <{element.tag}>: "
                    + ", ".join(sorted(unexpected_url_attributes))
                    + ".",
                )
            )
        if element.tag == "meta" and "http-equiv" in attrs:
            issues.append(
                issue(
                    "NAV008",
                    "HTTP-equivalent meta directives, including refresh redirects, are not allowed.",
                )
            )
        if "aria-label" in attrs:
            classes = set(attrs.get("class", "").split())
            expected_aria_label = None
            if element.tag == "nav" and "header-nav" in classes:
                expected_aria_label = "One-pager sections"
            elif element.tag == "aside" and "hero-visual" in classes:
                expected_aria_label = "Buyer challenge and desired outcome"
            if attrs.get("aria-label") != expected_aria_label:
                issues.append(
                    issue(
                        "A11Y005",
                        "ARIA labels must exactly match the trusted template semantics.",
                    )
                )
        if "hidden" in attrs:
            classes = set(attrs.get("class", "").split())
            trusted_hidden_fallback = (
                element.tag == "span"
                and classes == {"account-name"}
                and attrs.get("data-role") == "account-name"
                and "data-non-claim-number" in attrs
            )
            if not trusted_hidden_fallback:
                issues.append(
                    issue(
                        "A11Y006",
                        "The hidden attribute is restricted to the trusted account-name fallback.",
                    )
                )
        if attrs.get("aria-hidden") == "true":
            classes = set(attrs.get("class", "").split())
            trusted_hidden_glyph = (
                element.tag == "span"
                and (
                    (
                        classes == {"brand-joiner"}
                        and parser.direct_text(element) == "×"
                    )
                    or (
                        classes == {"button-arrow"}
                        and parser.direct_text(element) == "↗"
                    )
                )
            )
            if not trusted_hidden_glyph:
                issues.append(
                    issue(
                        "A11Y007",
                        "aria-hidden is restricted to trusted decorative glyphs.",
                    )
                )
        if "data-non-claim-number" in attrs:
            classes = set(attrs.get("class", "").split())
            has_claim_trace = any(
                key in attrs
                for key in (
                    "data-proof-id",
                    "data-claim-id",
                    "data-evidence-id",
                    "data-evidence-kind",
                    "data-source-id",
                    "data-source-ids",
                )
            )
            allowed_non_claim_marker = not has_claim_trace and (
                (
                    element.tag == "a"
                    and attrs.get("data-cta") == "primary"
                )
                or (
                    element.tag == "span"
                    and attrs.get("data-role") == "account-name"
                    and bool(
                        classes.intersection(
                            {"account-name", "account-name-narrow"}
                        )
                    )
                )
                or (
                    element.tag == "span"
                    and "path-index" in classes
                )
            )
            if not allowed_non_claim_marker:
                issues.append(
                    issue(
                        "PROOF009",
                        "data-non-claim-number is restricted to structural account, CTA, and path-index elements.",
                    )
                )
            elif (
                mode != "template"
                and "path-index" in classes
                and not re.fullmatch(r"0[1-3]", parser.direct_text(element))
            ):
                issues.append(
                    issue(
                        "PROOF010",
                        "Path-index exemptions may contain only 01, 02, or 03.",
                    )
                )
        if "style" in attrs:
            issues.append(issue("CSS006", "Inline style attributes are not allowed."))
        for attr_name in attrs:
            if not attr_name.startswith("on"):
                continue
            if attr_name != "onclick":
                issues.append(
                    issue(
                        "SCRIPT003",
                        f"Unexpected inline event handler {attr_name!r} on <{element.tag}>.",
                    )
                )
            elif attrs.get("data-cta") == "primary":
                if not valid_cta_onclick(attrs.get("onclick", "")):
                    issues.append(
                        issue(
                            "SCRIPT004",
                            "Primary CTA inline handler differs from the fixed analytics contract.",
                        )
                    )
            elif element.tag == "a" and "data-resource" in attrs:
                if not valid_resource_onclick(attrs.get("onclick", "")):
                    issues.append(
                        issue(
                            "SCRIPT005",
                            "Resource link handler differs from the fixed resource_click contract.",
                        )
                    )
            else:
                issues.append(
                    issue(
                        "SCRIPT003",
                        f"Unexpected inline event handler {attr_name!r} on <{element.tag}>.",
                    )
                )
        if element.tag == "script" and attrs.get("src"):
            issues.append(issue("ASSET001", "External JavaScript is not allowed."))
        if element.tag == "link" and "data-folloze-theme" not in attrs:
            issues.append(
                issue(
                    "ASSET002",
                    "Link elements are limited to the authorized Folloze theme stylesheet.",
                )
            )
        if element.tag == "img":
            src = attrs.get("src", "").strip()
            alt = attrs.get("alt")
            image_role = attrs.get("data-role", "")
            decorative = (
                attrs.get("aria-hidden") == "true"
                or attrs.get("role") == "presentation"
            )
            if image_role not in {"folloze-logo", "account-logo"}:
                issues.append(
                    issue(
                        "IMAGE004",
                        "Images are limited to the bound Folloze and prospect logo roles.",
                    )
                )
            if image_role == "folloze-logo" and src != FOLLOZE_LOGO_URL:
                issues.append(
                    issue(
                        "IMAGE005",
                        "Folloze logo source differs from the trusted brand asset.",
                    )
                )
            if image_role == "folloze-logo" and alt != "Folloze":
                issues.append(
                    issue(
                        "IMAGE007",
                        "Folloze logo alt text must be exactly 'Folloze'.",
                    )
                )
            if not src:
                issues.append(issue("IMAGE001", "Image has an empty source."))
            elif mode != "template" and not is_http_url(src):
                issues.append(
                    issue(
                        "IMAGE003",
                        "Final microsite logo images must use approved HTTP(S) URLs.",
                    )
                )
            if alt is None or (not alt.strip() and not decorative):
                issues.append(issue("IMAGE002", "Image needs useful alt text."))
        if element.tag == "button" and attrs.get("type") != "button":
            issues.append(issue("A11Y004", "Every button needs type=button."))

    folloze_logos = parser.elements_by_role("folloze-logo")
    if len(folloze_logos) != 1:
        issues.append(
            issue("IMAGE006", "Microsite requires exactly one trusted Folloze logo image.")
        )

    for link in [element for element in parser.elements if element.tag == "a"]:
        attrs = link.attrs
        href = attrs.get("href", "").strip()
        if not href:
            issues.append(issue("LINK001", "Anchor has an empty destination."))
            continue
        lower_href = href.lower()
        if lower_href == "#" or lower_href.startswith("javascript:"):
            issues.append(issue("LINK002", f"Unsafe link destination {href!r}."))
        if href.startswith("#"):
            issues.append(issue("NAV004", "Raw hash navigation is not allowed."))
        template_href = mode == "template" and bool(
            re.fullmatch(r"\[\[[A-Z0-9_]+\]\]", href)
        )
        if lower_href.startswith(("http://", "https://")):
            if attrs.get("target") != "_blank":
                issues.append(
                    issue("LINK003", "External links must use target=_blank.")
                )
            rel_tokens = set(attrs.get("rel", "").lower().split())
            if "noopener" not in rel_tokens:
                issues.append(
                    issue("LINK004", "External links must include rel=noopener.")
                )
        if "data-cta" in attrs:
            if (
                not template_href
                and not lower_href.startswith(("http://", "https://", "mailto:"))
            ):
                issues.append(issue("CTA010", "CTA needs a real link destination."))
            if not re.search(
                r"flzAnalytic\(\s*['\"]cta_click['\"]",
                attrs.get("onclick", ""),
            ):
                issues.append(
                    issue(
                        "CTA011",
                        "External CTA needs a direct inline cta_click call.",
                    )
                )
        if "data-resource" in attrs:
            if "data-cta" in attrs:
                issues.append(
                    issue("RESOURCE001", "Resource links cannot also be primary CTAs.")
                )
            if not template_href and not lower_href.startswith(("http://", "https://")):
                issues.append(
                    issue("RESOURCE002", "Resource links require an HTTP(S) URL.")
                )
            if not valid_resource_onclick(attrs.get("onclick", "")):
                issues.append(
                    issue(
                        "RESOURCE003",
                        "Resource links require the exact resource_click analytics call.",
                    )
                )
        if "data-cta" not in attrs and "data-resource" not in attrs:
            issues.append(
                issue(
                    "RESOURCE005",
                    "Every buyer-facing anchor must be an approved CTA or tracked resource.",
                )
            )

    for cta in [
        element
        for element in parser.elements_with("data-cta")
        if element.tag != "a"
    ]:
        issues.append(
            issue("CTA013", "Every primary CTA must be an external anchor link.")
        )

    for resource in parser.elements_with("data-resource"):
        if resource.tag != "a":
            issues.append(
                issue("RESOURCE004", "Every tracked resource must be an anchor link.")
            )

    for control in parser.elements_with("data-scroll-target"):
        attrs = control.attrs
        target_id = attrs.get("data-scroll-target", "")
        template_target = mode == "template" and bool(
            re.fullmatch(r"\[\[[A-Z0-9_]+\]\]", target_id)
        )
        if control.tag != "button" or attrs.get("type") != "button":
            issues.append(
                issue("NAV005", "Scroll controls must be button[type=button].")
            )
        if attrs.get("aria-controls") != target_id:
            issues.append(
                issue("NAV006", "Scroll control aria-controls must match target.")
            )
        if not template_target and (not target_id or target_id not in parser.ids):
            issues.append(
                issue("NAV007", f"Scroll target {target_id!r} does not exist.")
            )

    proof_ids = {
        element.attrs.get("data-proof-id", "")
        for element in parser.elements_with("data-proof-id")
        if element.attrs.get("data-proof-id")
    }
    claim_ids = {
        element.attrs.get("data-claim-id", "")
        for element in parser.elements_with("data-claim-id")
        if element.attrs.get("data-claim-id")
    }
    evidence_elements = [
        element
        for element in parser.elements
        if "proof-card" in element.attrs.get("class", "").split()
    ]
    for element in parser.elements:
        has_evidence_attribute = bool(
            {"data-evidence-id", "data-evidence-kind"}.intersection(
                element.attrs
            )
        )
        if has_evidence_attribute and element not in evidence_elements:
            issues.append(
                issue(
                    "PROOF011",
                    "Evidence attributes are permitted only on proof-card elements.",
                )
            )
    html_source_ids: set[str] = set()
    trace_required_classes = {
        "eyebrow",
        "hero-support",
        "outcome-copy",
        "section-intro",
        "proof-card",
        "path-step",
        "next-step-copy",
    }
    trace_required_ids = {
        "promise-title",
        "proof-title",
        "path-title",
        "next-step-title",
    }
    for element in parser.elements:
        element_ids = element_source_ids(element)
        html_source_ids.update(element_ids)
        actual_placement = element.attrs.get("data-placement", "")
        expected_placement = expected_element_placement(element)
        classes = set(element.attrs.get("class", "").split())
        requires_source_trace = bool(
            classes.intersection(trace_required_classes)
            or element.attrs.get("id") in trace_required_ids
        )
        if mode != "template" and requires_source_trace and not element_ids:
            issues.append(
                issue(
                    "SOURCE026",
                    f"Buyer copy element <{element.tag}> lacks an approved source trace.",
                )
            )
        if element_ids:
            if actual_placement not in BUYER_COPY_PLACEMENTS:
                issues.append(
                    issue(
                        "SOURCE027",
                        f"Sourced <{element.tag}> copy lacks a valid placement binding.",
                    )
                )
            if not expected_placement or actual_placement != expected_placement:
                issues.append(
                    issue(
                        "SOURCE028",
                        f"Sourced <{element.tag}> placement differs from its trusted module topology.",
                    )
                )
            expected_section_id = PLACEMENT_SECTION_IDS.get(actual_placement)
            if expected_section_id and element.section_id != expected_section_id:
                issues.append(
                    issue(
                        "SOURCE030",
                        f"Placement {actual_placement!r} must remain inside section #{expected_section_id}.",
                    )
                )
        if (
            mode != "template"
            and actual_placement
            and not element_ids
        ):
            issues.append(
                issue(
                    "SOURCE029",
                    "Placement attributes are allowed only on sourced buyer-copy elements.",
                )
            )
        if (
            mode != "template"
            and (
                "data-source-id" in element.attrs
                or "data-source-ids" in element.attrs
            )
            and not element_ids
        ):
            issues.append(
                issue("SOURCE023", "HTML contains an empty source trace attribute.")
            )

    if mode != "template" and brief is not None:
        approved_proof_ids = {
            canonical_display_text(value)
            for value in (
                get_path(brief, "claims_policy.approved_proof_ids", []) or []
            )
            if isinstance(value, str) and canonical_display_text(value)
        }
        approved_claim_ids = {
            canonical_display_text(value)
            for value in (
                get_path(brief, "claims_policy.approved_claim_ids", []) or []
            )
            if isinstance(value, str) and canonical_display_text(value)
        }
        proof_registry, _ = build_approved_content_registry(brief, "proof")
        claim_registry, _ = build_approved_content_registry(brief, "claim")
        mixed_evidence_trace = any(
            (
                bool(node.evidence_kind or node.evidence_id)
                and bool(node.proof_id or node.claim_id)
            )
            or (bool(node.proof_id) and bool(node.claim_id))
            for node in parser.visible_nodes
        ) or any(
            "data-proof-id" in evidence.attrs
            or "data-claim-id" in evidence.attrs
            for evidence in evidence_elements
        )
        if mixed_evidence_trace:
            issues.append(
                issue(
                    "PROOF012",
                    "Buyer copy cannot combine evidence, proof, and claim identities.",
                )
            )
        for evidence in evidence_elements:
            evidence_kind = evidence.attrs.get("data-evidence-kind", "")
            evidence_id = evidence.attrs.get("data-evidence-id", "")
            if evidence_kind not in {"proof", "claim"} or not evidence_id:
                issues.append(
                    issue(
                        "PROOF005",
                        "Every proof card needs one explicit proof-or-claim evidence trace.",
                    )
                )
                continue
            if evidence_kind == "proof":
                proof_ids.add(evidence_id)
            else:
                claim_ids.add(evidence_id)
            registry = (
                proof_registry if evidence_kind == "proof" else claim_registry
            )
            record = registry.get(evidence_id)
            if record is not None and element_source_ids(evidence) != record["source_ids"]:
                issues.append(
                    issue(
                        "PROOF007",
                        f"Evidence {evidence_id!r} source trace differs from its approved content registry.",
                    )
                )
        unknown_proof_ids = proof_ids.difference(approved_proof_ids)
        unknown_claim_ids = claim_ids.difference(approved_claim_ids)
        if unknown_proof_ids:
            issues.append(
                issue(
                    "PROOF001",
                    "HTML uses unapproved proof IDs: "
                    + ", ".join(sorted(unknown_proof_ids))
                    + ".",
                )
            )
        if unknown_claim_ids:
            issues.append(
                issue(
                    "PROOF002",
                    "HTML uses unapproved claim IDs: "
                    + ", ".join(sorted(unknown_claim_ids))
                    + ".",
                )
            )
        if "proof" not in parser.ids:
            issues.append(
                issue("PROOF003", "The standard proof section is absent.")
            )
        if "proof" in parser.ids and not evidence_elements:
            issues.append(
                issue("PROOF006", "Proof section has no traced evidence cards.")
            )

        for node in parser.visible_nodes:
            if node.non_claim_number:
                continue
            trace_kind = ""
            trace_id = ""
            if node.proof_id:
                trace_kind, trace_id = "proof", node.proof_id
            elif node.claim_id:
                trace_kind, trace_id = "claim", node.claim_id
            elif node.evidence_kind in {"proof", "claim"} and node.evidence_id:
                trace_kind, trace_id = node.evidence_kind, node.evidence_id
            if not trace_id:
                continue
            registry = proof_registry if trace_kind == "proof" else claim_registry
            record = registry.get(trace_id)
            if record is None:
                continue
            visible_copy = canonical_display_text(node.text)
            if visible_copy not in record["texts"]:
                issues.append(
                    issue(
                        "CONTENT011",
                        f"Visible {trace_kind} copy differs from approved content {trace_id!r}: {visible_copy!r}.",
                    )
                )
            if set(node.source_ids) != record["source_ids"]:
                issues.append(
                    issue(
                        "CONTENT012",
                        f"Visible {trace_kind} copy {trace_id!r} has a mismatched source trace.",
                    )
                )

        raw_selected_pillars = get_path(
            brief,
            "normalized_brief.selected_folloze_pillars",
            [],
        ) or []
        selected_pillars = {
            value
            for value in raw_selected_pillars
            if isinstance(value, str)
        } if isinstance(raw_selected_pillars, list) else set()
        html_pillars = {
            element.attrs.get("data-pillar", "")
            for element in parser.elements_with("data-pillar")
            if element.attrs.get("data-pillar")
        }
        if html_pillars != selected_pillars:
            issues.append(
                issue(
                    "PATH001",
                    "HTML path pillars do not match the approved selected pillars.",
                )
            )
        path_steps = [
            element
            for element in parser.elements
            if "path-step" in element.attrs.get("class", "").split()
        ]
        path_pillar_counts = Counter(
            element.attrs.get("data-pillar", "") for element in path_steps
        )
        if any(
            path_pillar_counts.get(pillar, 0) != 1
            for pillar in selected_pillars
        ):
            issues.append(
                issue(
                    "PATH002",
                    "Each approved Folloze pillar must render exactly one path card.",
                )
            )
        for path_step in path_steps:
            pillar = path_step.attrs.get("data-pillar", "")
            claim_id = path_step.attrs.get("data-claim-id", "")
            if not claim_id:
                issues.append(
                    issue("PATH003", f"Path card {pillar!r} lacks a claim ID.")
                )
                continue
            claim_record = claim_registry.get(claim_id)
            if claim_record is not None and claim_record.get("pillar") != pillar:
                issues.append(
                    issue(
                        "PATH004",
                        f"Path card {pillar!r} uses claim {claim_id!r} approved for {claim_record.get('pillar')!r}.",
                    )
                )

        source_ledger = get_path(brief, "research_policy.source_ledger", []) or []
        source_by_id = {
            item.get("source_id"): item
            for item in source_ledger
            if isinstance(item, dict) and item.get("source_id")
        }
        matrix_rows = get_path(
            brief, "normalized_brief.message_fit_matrix", []
        ) or []
        matrix_pairs = {
            (
                canonical_display_text(row.get("source_id", "")),
                canonical_display_text(row.get("buyer_safe_claim", "")),
                canonical_display_text(row.get("placement", "")),
            )
            for row in matrix_rows
            if isinstance(row, dict)
            and canonical_display_text(row.get("source_id", ""))
            and canonical_display_text(row.get("buyer_safe_claim", ""))
        }
        matrix_source_ids = {source_id for source_id, _, _ in matrix_pairs}
        sourced_visible_nodes = [
            node
            for node in parser.visible_nodes
            if (
                node.source_ids
                and not node.non_claim_number
                and not node.hidden_from_buyers
            )
        ]
        visible_source_pairs = {
            (source_id, canonical_display_text(node.text), node.placement)
            for node in sourced_visible_nodes
            for source_id in node.source_ids
        }
        approved_meta_source_ids = get_path(
            brief,
            "seller_inputs.page_goal.meta_description_source_ids",
            [],
        )
        if (
            isinstance(approved_meta_source_ids, list)
            and len(parser.description_contents) == 1
        ):
            visible_source_pairs.update(
                (
                    canonical_display_text(source_id),
                    canonical_display_text(parser.description_contents[0]),
                    "metadata",
                )
                for source_id in approved_meta_source_ids
                if isinstance(source_id, str)
                and canonical_display_text(source_id)
            )
        unknown_html_sources = html_source_ids.difference(source_by_id)
        if unknown_html_sources:
            issues.append(
                issue(
                    "SOURCE020",
                    "HTML uses unknown source IDs: "
                    + ", ".join(sorted(unknown_html_sources))
                    + ".",
                )
            )
        unapproved_html_sources = html_source_ids.difference(matrix_source_ids)
        if unapproved_html_sources:
            issues.append(
                issue(
                    "SOURCE021",
                    "HTML source IDs are not approved in the message-fit matrix: "
                    + ", ".join(sorted(unapproved_html_sources))
                    + ".",
                )
            )
        for node in sourced_visible_nodes:
            visible_copy = canonical_display_text(node.text)
            unapproved_sources_for_copy = {
                source_id
                for source_id in node.source_ids
                if (source_id, visible_copy, node.placement) not in matrix_pairs
            }
            if unapproved_sources_for_copy:
                issues.append(
                    issue(
                        "SOURCE024",
                        "Sourced visible copy lacks exact approval for source IDs "
                        + ", ".join(sorted(unapproved_sources_for_copy))
                        + f": {visible_copy!r}.",
                    )
                )
        missing_matrix_pairs = matrix_pairs.difference(visible_source_pairs)
        for source_id, approved_copy, placement in sorted(missing_matrix_pairs):
            issues.append(
                issue(
                    "SOURCE025",
                    f"Approved message-fit copy for {source_id!r} is absent, moved, or changed at {placement!r}: {approved_copy!r}.",
                )
            )
        for source_id in sorted(html_source_ids.intersection(source_by_id)):
            if source_by_id[source_id].get("buyer_use") not in BUYER_VISIBLE_USES:
                issues.append(
                    issue(
                        "SOURCE022",
                        f"HTML traces buyer-visible copy to non-visible source {source_id!r}.",
                    )
                )

        resource_registry, _ = build_approved_resource_registry(brief)
        resource_elements = parser.elements_with("data-resource")
        rendered_resource_ids = [
            canonical_display_text(element.attrs.get("data-resource", ""))
            for element in resource_elements
        ]
        duplicate_rendered_resources = {
            resource_id
            for resource_id, count in Counter(rendered_resource_ids).items()
            if resource_id and count > 1
        }
        if duplicate_rendered_resources:
            issues.append(
                issue(
                    "RESOURCE016",
                    "Rendered resource IDs are duplicated: "
                    + ", ".join(sorted(duplicate_rendered_resources))
                    + ".",
                )
            )
        if set(rendered_resource_ids) != set(resource_registry):
            issues.append(
                issue(
                    "RESOURCE017",
                    "Rendered resources do not exactly match the approved resource registry.",
                )
            )
        for resource in resource_elements:
            resource_id = canonical_display_text(
                resource.attrs.get("data-resource", "")
            )
            record = resource_registry.get(resource_id)
            if record is None:
                continue
            if resource.attrs.get("href", "").strip() != record["url"]:
                issues.append(
                    issue(
                        "RESOURCE018",
                        f"Rendered resource {resource_id!r} URL differs from the approved URL.",
                    )
                )
            if parser.semantic_text(resource) != record["label"]:
                issues.append(
                    issue(
                        "RESOURCE019",
                        f"Rendered resource {resource_id!r} label differs from the approved label.",
                    )
                )
            if element_source_ids(resource) != record["source_ids"]:
                issues.append(
                    issue(
                        "RESOURCE020",
                        f"Rendered resource {resource_id!r} source trace differs from the approved registry.",
                    )
                )

        for node in parser.visible_nodes:
            if node.non_claim_number or not NUMERIC_CLAIM_PATTERN.search(
                node.text
            ):
                continue
            numeric_proof_id = node.proof_id
            if not numeric_proof_id and node.evidence_kind == "proof":
                numeric_proof_id = node.evidence_id
            if not numeric_proof_id or numeric_proof_id not in approved_proof_ids:
                issues.append(
                    issue(
                        "PROOF004",
                        f"Numeric claim lacks an approved proof ID: {node.text!r}.",
                    )
                )
            elif canonical_display_text(node.text) not in proof_registry.get(
                numeric_proof_id,
                {},
            ).get("texts", set()):
                issues.append(
                    issue(
                        "PROOF008",
                        f"Numeric claim differs from approved proof copy {numeric_proof_id!r}.",
                    )
                )

        account_name = str(
            get_path(brief, "seller_inputs.prospect.account_name", "")
        ).strip()
        expected_page_title = f"Folloze for {account_name}"
        if canonical_display_text(parser.title) != canonical_display_text(
            expected_page_title
        ):
            issues.append(
                issue(
                    "META006",
                    "Page title must use the mechanical 'Folloze for <approved account>' form.",
                )
            )
        approved_meta_description = canonical_display_text(
            get_path(brief, "seller_inputs.page_goal.meta_description", "")
        )
        if (
            len(parser.description_contents) != 1
            or canonical_display_text(parser.description_contents[0])
            != approved_meta_description
        ):
            issues.append(
                issue(
                    "META007",
                    "HTML meta description must exactly match the approved buyer-safe description.",
                )
            )
        account_name_elements = parser.elements_by_role("account-name")
        if (
            not account_name
            or not account_name_elements
            or any(
                canonical_display_text(parser.direct_text(element))
                != canonical_display_text(account_name)
                for element in account_name_elements
            )
        ):
            issues.append(
                issue(
                    "ACCOUNT001",
                    "Every prospect account-name role must exactly match the approved account name.",
                )
            )

        seller_name = str(
            get_path(brief, "seller_inputs.seller.name", "")
        ).strip()
        seller_role = str(
            get_path(brief, "seller_inputs.seller.role", "")
        ).strip()
        expected_seller_line = (
            f"{seller_name} · {seller_role}" if seller_role else seller_name
        )
        seller_line_elements = parser.elements_by_role("seller-line")
        if (
            len(seller_line_elements) != 1
            or canonical_display_text(
                parser.direct_text(seller_line_elements[0])
            )
            != canonical_display_text(expected_seller_line)
        ):
            issues.append(
                issue(
                    "ACCOUNT006",
                    "Seller line must exactly match the approved seller name and role.",
                )
            )

        logo_policy = str(
            get_path(
                brief,
                "seller_inputs.visual_preferences.logo_policy",
                "",
            )
        )
        approved_logo_url = str(
            get_path(
                brief,
                "seller_inputs.prospect.official_logo_url",
                "",
            )
        ).strip()
        account_logos = parser.elements_by_role("account-logo")
        if logo_policy == "text_only":
            if account_logos:
                issues.append(
                    issue(
                        "ACCOUNT002",
                        "Text-only logo policy must not render a prospect logo image.",
                    )
                )
        elif logo_policy in {"official_public", "seller_supplied"}:
            if not is_http_url(approved_logo_url):
                issues.append(
                    issue(
                        "ACCOUNT003",
                        "Logo policy requires an approved HTTP(S) prospect logo URL.",
                    )
                )
            if len(account_logos) != 1:
                issues.append(
                    issue(
                        "ACCOUNT004",
                        "Logo policy requires exactly one prospect logo image.",
                    )
                )
            elif account_logos[0].attrs.get("src", "").strip() != approved_logo_url:
                issues.append(
                    issue(
                        "ACCOUNT005",
                        "Rendered prospect logo differs from the approved brief URL.",
                    )
                )
            elif account_logos[0].attrs.get("alt", "") != f"{account_name} logo":
                issues.append(
                    issue(
                        "ACCOUNT007",
                        "Prospect logo alt text must exactly match the approved account name.",
                    )
                )

        cta_type = str(
            get_path(brief, "seller_inputs.page_goal.primary_cta.type", "")
        )
        approved_label = str(
            get_path(brief, "seller_inputs.page_goal.primary_cta.label", "")
        ).strip()
        approved_destination = normalize_cta_destination(
            cta_type,
            str(
                get_path(
                    brief,
                    "seller_inputs.page_goal.primary_cta.destination",
                    "",
                )
            ),
        )
        primary_ctas = [
            element
            for element in parser.elements_with("data-cta")
            if element.attrs.get("data-cta") == "primary"
        ]
        if len(primary_ctas) != 3:
            issues.append(
                issue(
                    "CTA012",
                    "Microsite requires exactly three placements of the one approved primary CTA.",
                )
            )
        cta_areas: Counter[str] = Counter()
        for cta in primary_ctas:
            attrs = cta.attrs
            area_match = re.search(
                r"area:'(header|hero|next step)'",
                attrs.get("onclick", ""),
            )
            if area_match:
                cta_areas[area_match.group(1)] += 1
            if attrs.get("data-cta-type") != cta_type:
                issues.append(
                    issue("CTA015", "A primary CTA type differs from the brief.")
                )
            if attrs.get("data-cta-label", "").strip() != approved_label:
                issues.append(
                    issue("CTA016", "A primary CTA label differs from the brief.")
                )
            if parser.semantic_text(cta) != approved_label:
                issues.append(
                    issue(
                        "CTA017",
                        "Buyer-visible primary CTA text differs from the approved label.",
                    )
                )
            actual_destination = attrs.get("href", "").strip()
            if cta.tag != "a" or actual_destination != approved_destination:
                issues.append(
                    issue(
                        "CTA018",
                        "Every primary CTA must use the approved external destination.",
                    )
                )
        if cta_areas != Counter({"header": 1, "hero": 1, "next step": 1}):
            issues.append(
                issue(
                    "CTA019",
                    "Primary CTA placements must contain one trusted header, hero, and next-step analytics area.",
                )
            )

        allowed_untraced_text = {
            canonical_display_text(value)
            for value in STATIC_BUYER_TEXT
        }
        allowed_untraced_text.add(
            canonical_display_text(expected_seller_line)
        )
        for node in parser.visible_nodes:
            if node.non_claim_number:
                continue
            resolved_evidence = (
                node.evidence_kind == "proof"
                and node.evidence_id in proof_registry
            ) or (
                node.evidence_kind == "claim"
                and node.evidence_id in claim_registry
            )
            if (
                node.source_ids
                or node.proof_id
                or node.claim_id
                or resolved_evidence
            ):
                continue
            visible_copy = canonical_display_text(node.text)
            if visible_copy not in allowed_untraced_text:
                issues.append(
                    issue(
                        "CONTENT014",
                        f"Buyer-facing or hidden DOM copy lacks a source trace or trusted structural binding: {visible_copy!r}.",
                    )
                )

        prohibited_terms = set(
            get_path(
                brief,
                "stage2_handoff.constraints.prohibited_visible_terms",
                [],
            )
            or []
        )
        prohibited_terms.update(
            {
                "activation layer",
                "campaign agent",
                "activation agent",
                "insight agent",
                "buyer experience platform",
                "abx platform",
            }
        )
        prohibited_terms.update(
            value
            for value in (
                get_path(
                    brief,
                    "seller_inputs.business_context.forbidden_topics",
                    [],
                )
                or []
            )
            if isinstance(value, str) and value.strip()
        )
        prohibited_terms.update(
            value
            for value in (
                get_path(brief, "claims_policy.blocked_claims", []) or []
            )
            if isinstance(value, str) and value.strip()
        )
        buyer_readable_parts = [
            parser.visible_text,
            parser.title,
            *parser.description_contents,
            *[
                element.attrs.get("alt", "")
                for element in parser.elements
                if "alt" in element.attrs
            ],
            *[
                element.attrs.get("aria-label", "")
                for element in parser.elements
                if "aria-label" in element.attrs
            ],
        ]
        buyer_readable_text = " ".join(buyer_readable_parts)
        visible_lower = buyer_readable_text.casefold()
        for term in sorted(prohibited_terms):
            if term and term.casefold() in visible_lower:
                issues.append(
                    issue(
                        "COPY001",
                        f"Visible copy contains prohibited term {term!r}.",
                    )
                )
        if "—" in buyer_readable_text:
            issues.append(issue("COPY002", "Buyer-readable copy contains an em dash."))

        state = get_path(brief, "metadata.state", "")
        if state in PREVIEW_APPROVED_STATES or mode == "mcp":
            expected_digest = str(
                get_path(
                    brief,
                    "stage2_handoff.preview_approval.html_digest",
                    "",
                )
            )
            actual_digest = compute_preview_html_digest(raw_html)
            if expected_digest != actual_digest:
                issues.append(
                    issue(
                        "PREVIEW006",
                        "Approved preview digest does not match the exact HTML.",
                    )
                )

    theme_links = [
        element
        for element in parser.elements
        if element.tag == "link" and "data-folloze-theme" in element.attrs
    ]
    if mode == "template":
        if "FOLLOZE_THEME_LINK_SLOT" not in "\n".join(parser.comments):
            issues.append(issue("MCP010", "Template lacks the MCP theme link slot."))
        if theme_links:
            issues.append(
                issue("MCP013", "Authoring template must not contain a live theme link.")
            )
    elif mode == "mcp":
        if len(theme_links) != 1:
            issues.append(
                issue("MCP011", "MCP HTML needs exactly one Folloze theme link.")
            )
        elif brief is not None:
            expected_url = str(
                get_path(brief, "stage2_handoff.mcp_state.theme_url", "")
            )
            expected_theme_id = str(
                get_path(brief, "stage2_handoff.mcp_state.theme_id", "")
            )
            actual_url = theme_links[0].attrs.get("href", "")
            if actual_url != expected_url:
                issues.append(
                    issue("MCP012", "Theme link differs from approved MCP state.")
                )
            rel_tokens = set(theme_links[0].attrs.get("rel", "").lower().split())
            if "stylesheet" not in rel_tokens or not theme_links[0].in_head:
                issues.append(
                    issue(
                        "MCP019",
                        "Theme link must be a stylesheet inside <head>.",
                    )
                )
            if theme_links[0].attrs.get("data-folloze-theme", "") != expected_theme_id:
                issues.append(
                    issue(
                        "MCP020",
                        "Theme link ID differs from approved MCP state.",
                    )
                )
            recorded_path = str(
                get_path(brief, "stage2_handoff.mcp_state.local_html_path", "")
            ).strip()
            if html_path is not None and recorded_path:
                recorded = Path(recorded_path).expanduser()
                if not recorded.is_absolute():
                    issues.append(
                        issue(
                            "MCP022",
                            "Authorized local HTML path must be absolute.",
                        )
                    )
                elif recorded.resolve() != html_path.resolve():
                    issues.append(
                        issue(
                            "MCP021",
                            "Validated HTML path differs from the authorized local source path.",
                        )
                    )
    elif theme_links:
        issues.append(
            issue(
                "MCP013",
                "Local final HTML must retain the canonical theme slot and no live theme link.",
            )
        )

    return issues


def validate_pdf(
    raw_html: str,
    parser: PageParser,
    mode: str,
) -> list[Issue]:
    issues: list[Issue] = []
    if parser.h1_count != 1:
        issues.append(issue("PDF001", "Printable page must contain exactly one H1."))
    if mode == "template" and not re.search(r"\{\{[^{}]+\}\}", raw_html):
        issues.append(issue("PDF002", "Printable template has no template tokens."))
    return issues


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a Folloze prospect one-pager brief and HTML."
    )
    parser.add_argument("--brief", type=Path)
    parser.add_argument("--html", type=Path)
    parser.add_argument(
        "--profile",
        choices=("microsite", "pdf"),
        default="microsite",
    )
    parser.add_argument(
        "--mode",
        choices=("template", "final", "mcp"),
        default="final",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--digest",
        choices=("approval", "html", "mcp", "mcp-result", "public", "public-verification"),
        help="Print an approval, HTML, MCP authorization, MCP result, public-deployment, or public-verification SHA-256 digest and exit.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    issues: list[Issue] = []
    brief: dict[str, Any] | None = None

    if args.brief is not None:
        brief, brief_load_issues = load_json(args.brief, "Brief")
        issues.extend(brief_load_issues)
        if brief is not None and args.digest is None:
            issues.extend(validate_brief(brief, args.mode))

    if args.digest in {"approval", "mcp", "mcp-result", "public", "public-verification"}:
        if brief is None:
            print(
                "--brief with valid JSON is required for this digest.",
                file=sys.stderr,
            )
            return 2
        digest_functions = {
            "approval": compute_approval_digest,
            "mcp": compute_mcp_authorization_digest,
            "mcp-result": compute_mcp_save_result_digest,
            "public": compute_public_deployment_authorization_digest,
            "public-verification": compute_public_verification_digest,
        }
        print(digest_functions[args.digest](brief))
        return 0

    if args.digest == "html":
        if args.html is None:
            print("--html is required for HTML digest.", file=sys.stderr)
            return 2
        try:
            raw_html = args.html.read_text(encoding="utf-8")
        except (FileNotFoundError, UnicodeDecodeError):
            print("HTML file must exist and be UTF-8 text.", file=sys.stderr)
            return 2
        print(compute_preview_html_digest(raw_html))
        return 0

    if args.mode != "template" and args.brief is None:
        print("--brief is required in final and mcp modes.", file=sys.stderr)
        return 2
    if args.html is None:
        print("--html is required for validation.", file=sys.stderr)
        return 2

    try:
        raw_html = args.html.read_text(encoding="utf-8")
    except FileNotFoundError:
        print("HTML file does not exist.", file=sys.stderr)
        return 2
    except UnicodeDecodeError:
        print("HTML file is not UTF-8 text.", file=sys.stderr)
        return 2

    parser = PageParser()
    try:
        parser.feed(raw_html)
        parser.close()
    except Exception as exc:
        issues.append(issue("HTML000", f"HTML parser error: {exc}."))

    issues.extend(
        validate_document_basics(raw_html, parser, args.profile, args.mode)
    )
    if args.profile == "microsite":
        issues.extend(
            validate_microsite_structure(
                raw_html,
                parser,
                brief,
                args.mode,
                args.html,
            )
        )
    else:
        issues.extend(validate_pdf(raw_html, parser, args.mode))

    issues = sorted(set(issues))
    errors = [item for item in issues if item.severity == "error"]
    warnings = [item for item in issues if item.severity == "warning"]

    if args.as_json:
        payload = {
            "ok": not errors,
            "profile": args.profile,
            "mode": args.mode,
            "errors": [asdict(item) for item in errors],
            "warnings": [asdict(item) for item in warnings],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        status = "PASS" if not errors else "FAIL"
        print(f"{status}: {args.profile}/{args.mode}")
        for item in issues:
            print(f"{item.severity.upper()} {item.rule_id}: {item.message}")

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
