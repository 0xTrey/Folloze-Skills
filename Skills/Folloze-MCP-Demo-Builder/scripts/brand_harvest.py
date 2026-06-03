#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import datetime as dt
import html.parser
import json
import os
import random
import re
import shutil
import socket
import string
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36 "
    "FollozeBrandHarvest/0.1"
)

SKIP_DOMAINS = {
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "x.com",
    "twitter.com",
    "youtube.com",
    "wikipedia.org",
    "crunchbase.com",
    "bloomberg.com",
    "glassdoor.com",
    "zoominfo.com",
}


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def slugify(value: str, fallback: str = "brand") -> str:
    value = value.lower().strip()
    value = re.sub(r"https?://", "", value)
    value = re.sub(r"^www\.", "", value)
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:80] or fallback


def ensure_url(value: str) -> str:
    value = value.strip()
    if not value:
        return value
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", value):
        return f"https://{value}"
    return value


def domain_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(ensure_url(url))
    domain = (parsed.netloc or parsed.path).split("/")[0].lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def looks_like_domain(value: str) -> bool:
    value = value.strip().lower()
    if " " in value:
        return False
    parsed = urllib.parse.urlparse(ensure_url(value))
    host = parsed.netloc or parsed.path
    return "." in host and not host.endswith(".")


def looks_like_url(value: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", value.strip()))


def fetch_text(url: str, timeout: float = 12.0, limit: int = 2_000_000) -> tuple[str, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        final_url = resp.geturl()
        content = resp.read(limit)
        charset = resp.headers.get_content_charset() or "utf-8"
    return content.decode(charset, errors="replace"), final_url


def http_probe(url: str, timeout: float = 4.0) -> tuple[bool, str | None]:
    req = urllib.request.Request(
        ensure_url(url),
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if 200 <= resp.status < 400:
                return True, resp.geturl()
    except Exception:
        return False, None
    return False, None


def brandfetch_brand(domain: str, token: str | None, timeout: float) -> dict[str, Any]:
    if not token:
        return {"status": "skipped", "reason": "BRANDFETCH_API_KEY or --brandfetch-token not provided"}
    url = f"https://api.brandfetch.io/v2/brands/domain/{urllib.parse.quote(domain)}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"status": "ok", "data": json.loads(resp.read().decode("utf-8"))}
    except urllib.error.HTTPError as exc:
        return {"status": "error", "code": exc.code, "reason": exc.reason}
    except Exception as exc:
        return {"status": "error", "reason": str(exc)}


def clean_account_name(value: str) -> str:
    stop = {
        "inc",
        "incorporated",
        "corp",
        "corporation",
        "company",
        "co",
        "llc",
        "ltd",
        "limited",
        "plc",
        "gmbh",
        "sa",
        "ag",
        "group",
        "holdings",
    }
    tokens = re.findall(r"[a-z0-9]+", value.lower())
    kept = [token for token in tokens if token not in stop]
    return "".join(kept) or "".join(tokens)


def account_domain_candidates(account_name: str) -> list[str]:
    cleaned = clean_account_name(account_name)
    words = re.findall(r"[a-z0-9]+", account_name.lower())
    acronym = "".join(word[0] for word in words if word)
    candidates: list[str] = []
    for root in dict.fromkeys([cleaned, acronym]):
        if len(root) < 2:
            continue
        for tld in ("com", "io", "ai", "co", "org", "net"):
            candidates.append(f"{root}.{tld}")
    return candidates[:12]


class LinkSearchParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._active_href: str | None = None
        self._active_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        attrs_dict = dict(attrs)
        href = attrs_dict.get("href")
        if href:
            self._active_href = href
            self._active_text = []

    def handle_data(self, data: str) -> None:
        if self._active_href:
            self._active_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._active_href:
            text = " ".join(" ".join(self._active_text).split())
            self.links.append((self._active_href, text))
            self._active_href = None
            self._active_text = []


def decode_duckduckgo_href(href: str) -> str:
    parsed = urllib.parse.urlparse(href)
    qs = urllib.parse.parse_qs(parsed.query)
    if "uddg" in qs and qs["uddg"]:
        return qs["uddg"][0]
    if href.startswith("//"):
        return "https:" + href
    return href


def search_account_domain(account_name: str, timeout: float) -> tuple[str | None, list[str]]:
    notes: list[str] = []
    for candidate in account_domain_candidates(account_name):
        ok, final_url = http_probe(f"https://{candidate}", timeout=min(timeout, 4.0))
        notes.append(f"candidate {candidate}: {'ok' if ok else 'no response'}")
        if ok and final_url:
            return final_url, notes

    query = urllib.parse.quote_plus(f"{account_name} official website")
    url = f"https://duckduckgo.com/html/?q={query}"
    try:
        html_text, _ = fetch_text(url, timeout=min(timeout, 8.0), limit=600_000)
    except Exception as exc:
        notes.append(f"search fallback failed: {exc}")
        return None, notes

    parser = LinkSearchParser()
    parser.feed(html_text)
    for href, text in parser.links:
        candidate_url = decode_duckduckgo_href(href)
        domain = domain_from_url(candidate_url)
        if not domain or any(domain == skip or domain.endswith("." + skip) for skip in SKIP_DOMAINS):
            continue
        if "/y.js" in candidate_url or "duckduckgo.com" in domain:
            continue
        notes.append(f"search picked {candidate_url} from result '{text[:80]}'")
        return candidate_url, notes
    notes.append("search fallback found no usable official-looking result")
    return None, notes


def resolve_input(query: str, source_url: str | None, timeout: float) -> dict[str, Any]:
    notes: list[str] = []
    raw = source_url or query
    input_type = "account_name"
    resolved_url: str | None = None

    if source_url:
        input_type = "source_url"
        resolved_url = ensure_url(source_url)
    elif looks_like_url(query):
        input_type = "source_url"
        resolved_url = ensure_url(query)
    elif looks_like_domain(query):
        input_type = "domain"
        resolved_url = ensure_url(query)
    else:
        resolved_url, notes = search_account_domain(query, timeout)

    domain = domain_from_url(resolved_url) if resolved_url else None
    return {
        "raw": raw,
        "query": query,
        "input_type": input_type,
        "source_url": resolved_url,
        "domain": domain,
        "resolution_notes": notes,
        "confidence": "high" if input_type in {"source_url", "domain"} else ("medium" if resolved_url else "low"),
    }


class BasicHTMLParser(html.parser.HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.title: str = ""
        self.meta: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.headings: list[dict[str, str]] = []
        self.scripts: list[dict[str, str]] = []
        self.stylesheets: list[str] = []
        self._tag_stack: list[str] = []
        self._title_text: list[str] = []
        self._heading_tag: str | None = None
        self._heading_text: list[str] = []

    def absolute(self, value: str | None) -> str:
        if not value:
            return ""
        return urllib.parse.urljoin(self.base_url, value)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs_dict = {key.lower(): value or "" for key, value in attrs}
        self._tag_stack.append(tag)
        if tag == "title":
            self._title_text = []
        elif tag == "meta":
            record = {key: attrs_dict[key] for key in ("name", "property", "content") if attrs_dict.get(key)}
            if record:
                self.meta.append(record)
        elif tag == "a" and attrs_dict.get("href"):
            self.links.append({"href": self.absolute(attrs_dict.get("href")), "text": ""})
        elif tag == "img":
            self.images.append(
                {
                    "src": self.absolute(attrs_dict.get("src")),
                    "alt": attrs_dict.get("alt", ""),
                    "class": attrs_dict.get("class", ""),
                    "loading": attrs_dict.get("loading", ""),
                }
            )
        elif tag == "script":
            self.scripts.append({"src": self.absolute(attrs_dict.get("src")), "type": attrs_dict.get("type", "")})
        elif tag == "link" and attrs_dict.get("rel"):
            rel = attrs_dict["rel"].lower()
            if "stylesheet" in rel and attrs_dict.get("href"):
                self.stylesheets.append(self.absolute(attrs_dict["href"]))
        elif tag in {"h1", "h2", "h3"}:
            self._heading_tag = tag
            self._heading_text = []

    def handle_data(self, data: str) -> None:
        if self._tag_stack and self._tag_stack[-1] == "title":
            self._title_text.append(data)
        if self._heading_tag:
            self._heading_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.title = " ".join(" ".join(self._title_text).split())
        elif tag == self._heading_tag:
            text = " ".join(" ".join(self._heading_text).split())
            if text:
                self.headings.append({"tag": tag, "text": text})
            self._heading_tag = None
            self._heading_text = []
        if self._tag_stack:
            self._tag_stack.pop()


def basic_html_harvest(url: str, timeout: float) -> dict[str, Any]:
    try:
        html_text, final_url = fetch_text(url, timeout=timeout)
    except Exception as exc:
        return {"status": "error", "reason": str(exc)}
    parser = BasicHTMLParser(final_url)
    parser.feed(html_text)
    color_values = sorted(set(re.findall(r"#[0-9a-fA-F]{3,8}\b", html_text)))[:80]
    font_families = sorted(set(re.findall(r"font-family\s*:\s*([^;}{]+)", html_text, re.I)))[:40]
    css_vars = {}
    for name, value in re.findall(r"(--[a-zA-Z0-9_-]+)\s*:\s*([^;}{]+)", html_text):
        if any(token in name.lower() for token in ("color", "font", "radius", "shadow", "space", "gap")):
            css_vars[name] = value.strip()
    return {
        "status": "ok",
        "final_url": final_url,
        "title": parser.title,
        "meta": parser.meta[:80],
        "headings": parser.headings[:80],
        "links": parser.links[:120],
        "images": parser.images[:120],
        "scripts": parser.scripts[:80],
        "stylesheets": parser.stylesheets[:40],
        "colors_from_source": color_values,
        "font_families_from_source": font_families,
        "css_variables_from_source": css_vars,
    }


class WebSocketClient:
    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock
        self.sock.settimeout(20)

    @classmethod
    def connect(cls, websocket_url: str, timeout: float = 20.0) -> "WebSocketClient":
        parsed = urllib.parse.urlparse(websocket_url)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or 80
        path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
        sock = socket.create_connection((host, port), timeout=timeout)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            "Connection: Upgrade\r\n"
            "Upgrade: websocket\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            f"Sec-WebSocket-Key: {key}\r\n\r\n"
        )
        sock.sendall(request.encode("ascii"))
        response = b""
        while b"\r\n\r\n" not in response:
            response += sock.recv(4096)
            if len(response) > 20000:
                break
        if b" 101 " not in response.split(b"\r\n", 1)[0]:
            raise RuntimeError("Chrome DevTools websocket handshake failed")
        return cls(sock)

    def close(self) -> None:
        try:
            self.sock.close()
        except Exception:
            pass

    def _recv_exact(self, length: int) -> bytes:
        chunks = []
        remaining = length
        while remaining:
            chunk = self.sock.recv(remaining)
            if not chunk:
                raise RuntimeError("websocket closed")
            chunks.append(chunk)
            remaining -= len(chunk)
        return b"".join(chunks)

    def send_json(self, data: dict[str, Any]) -> None:
        payload = json.dumps(data, separators=(",", ":")).encode("utf-8")
        header = bytearray([0x81])
        length = len(payload)
        if length < 126:
            header.append(0x80 | length)
        elif length < 65536:
            header.extend([0x80 | 126, (length >> 8) & 255, length & 255])
        else:
            header.append(0x80 | 127)
            header.extend(length.to_bytes(8, "big"))
        mask = os.urandom(4)
        masked = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
        self.sock.sendall(bytes(header) + mask + masked)

    def recv_json(self, timeout: float | None = None) -> dict[str, Any]:
        if timeout is not None:
            self.sock.settimeout(max(0.1, timeout))
        while True:
            first = self._recv_exact(2)
            opcode = first[0] & 0x0F
            length = first[1] & 0x7F
            masked = bool(first[1] & 0x80)
            if length == 126:
                length = int.from_bytes(self._recv_exact(2), "big")
            elif length == 127:
                length = int.from_bytes(self._recv_exact(8), "big")
            mask = self._recv_exact(4) if masked else b""
            payload = self._recv_exact(length) if length else b""
            if masked:
                payload = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
            if opcode == 8:
                raise RuntimeError("websocket closed by Chrome")
            if opcode in {1, 2}:
                return json.loads(payload.decode("utf-8"))


def find_chrome() -> str | None:
    env_path = os.environ.get("BRAND_HARVEST_CHROME")
    if env_path and Path(env_path).exists():
        return env_path
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    return None


HARVEST_JS = r"""
(() => {
  const abs = (value) => {
    if (!value) return "";
    try { return new URL(value, document.baseURI).href; } catch (_) { return value; }
  };
  const clean = (value) => String(value || "").replace(/\s+/g, " ").trim();
  const rectOf = (el) => {
    const rect = el.getBoundingClientRect();
    return {
      x: Math.round(rect.x),
      y: Math.round(rect.y),
      width: Math.round(rect.width),
      height: Math.round(rect.height)
    };
  };
  const colorToHex = (value) => {
    if (!value || value === "transparent") return null;
    if (value.startsWith("#")) return value.toUpperCase();
    const match = value.match(/rgba?\(([^)]+)\)/i);
    if (!match) return value;
    const parts = match[1].split(",").map((part) => part.trim());
    const alpha = parts[3] == null ? 1 : Number(parts[3]);
    if (alpha === 0) return null;
    const nums = parts.slice(0, 3).map((part) => Math.max(0, Math.min(255, parseInt(part, 10) || 0)));
    return "#" + nums.map((num) => num.toString(16).padStart(2, "0")).join("").toUpperCase();
  };
  const styleOf = (el) => {
    const style = window.getComputedStyle(el);
    return {
      color: colorToHex(style.color),
      backgroundColor: colorToHex(style.backgroundColor),
      borderColor: colorToHex(style.borderTopColor),
      borderWidth: style.borderTopWidth,
      borderRadius: style.borderRadius,
      boxShadow: style.boxShadow === "none" ? "" : style.boxShadow,
      fontFamily: style.fontFamily,
      fontSize: style.fontSize,
      fontWeight: style.fontWeight,
      lineHeight: style.lineHeight,
      letterSpacing: style.letterSpacing,
      textTransform: style.textTransform,
      padding: style.padding,
      margin: style.margin,
      display: style.display,
      position: style.position,
      gap: style.gap
    };
  };
  const visible = (el) => {
    const rect = el.getBoundingClientRect();
    const style = window.getComputedStyle(el);
    return rect.width > 0 && rect.height > 0 && style.visibility !== "hidden" && style.display !== "none";
  };
  const styleCount = (selector, props) => {
    const counts = {};
    Array.from(document.querySelectorAll(selector)).filter(visible).slice(0, 600).forEach((el) => {
      const style = window.getComputedStyle(el);
      props.forEach((prop) => {
        const raw = style[prop];
        const value = prop.toLowerCase().includes("color") ? colorToHex(raw) : clean(raw);
        if (!value || value === "rgba(0, 0, 0, 0)") return;
        counts[value] = (counts[value] || 0) + 1;
      });
    });
    return Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 40).map(([value, count]) => ({value, count}));
  };

  const rootStyle = window.getComputedStyle(document.documentElement);
  const cssVariables = {};
  for (let index = 0; index < rootStyle.length; index++) {
    const key = rootStyle[index];
    if (!key || !key.startsWith("--")) continue;
    const lower = key.toLowerCase();
    if (!/(color|font|radius|shadow|space|spacing|gap|button|card|brand|theme)/.test(lower)) continue;
    cssVariables[key] = clean(rootStyle.getPropertyValue(key));
  }

  const meta = Array.from(document.querySelectorAll("meta")).map((el) => ({
    name: el.getAttribute("name") || "",
    property: el.getAttribute("property") || "",
    content: el.getAttribute("content") || ""
  })).filter((item) => item.content).slice(0, 80);

  const headings = Array.from(document.querySelectorAll("h1,h2,h3")).filter(visible).slice(0, 80).map((el) => ({
    tag: el.tagName.toLowerCase(),
    text: clean(el.innerText),
    rect: rectOf(el),
    style: styleOf(el)
  }));

  const buttons = Array.from(document.querySelectorAll("a[href],button,[role='button']")).filter(visible).slice(0, 120).map((el) => ({
    tag: el.tagName.toLowerCase(),
    text: clean(el.innerText || el.getAttribute("aria-label") || el.getAttribute("title")),
    href: abs(el.getAttribute("href")),
    className: el.className && typeof el.className === "string" ? el.className : "",
    id: el.id || "",
    rect: rectOf(el),
    style: styleOf(el)
  })).filter((item) => item.text || item.href);

  const images = Array.from(document.querySelectorAll("img")).filter(visible).slice(0, 120).map((el) => ({
    src: abs(el.currentSrc || el.src),
    alt: el.alt || "",
    className: el.className && typeof el.className === "string" ? el.className : "",
    width: el.naturalWidth || 0,
    height: el.naturalHeight || 0,
    rect: rectOf(el)
  }));

  const backgroundImages = [];
  Array.from(document.querySelectorAll("body,header,main,section,article,div")).filter(visible).slice(0, 500).forEach((el) => {
    const style = window.getComputedStyle(el);
    const bg = style.backgroundImage;
    if (bg && bg !== "none" && backgroundImages.length < 50) {
      const urls = Array.from(bg.matchAll(/url\(["']?([^"')]+)["']?\)/g)).map((match) => abs(match[1]));
      if (urls.length) {
        backgroundImages.push({
          urls,
          tag: el.tagName.toLowerCase(),
          className: el.className && typeof el.className === "string" ? el.className : "",
          rect: rectOf(el),
          style: {
            backgroundColor: colorToHex(style.backgroundColor),
            backgroundSize: style.backgroundSize,
            backgroundPosition: style.backgroundPosition
          }
        });
      }
    }
  });

  const cards = Array.from(document.querySelectorAll("article,[class*='card' i],[class*='tile' i],[class*='item' i],li")).filter(visible).slice(0, 80).map((el) => ({
    tag: el.tagName.toLowerCase(),
    text: clean(el.innerText).slice(0, 220),
    className: el.className && typeof el.className === "string" ? el.className : "",
    rect: rectOf(el),
    style: styleOf(el)
  })).filter((item) => item.rect.width > 80 && item.rect.height > 40);

  const sections = Array.from(document.querySelectorAll("header,main,section,footer")).filter(visible).slice(0, 60).map((el) => ({
    tag: el.tagName.toLowerCase(),
    id: el.id || "",
    className: el.className && typeof el.className === "string" ? el.className : "",
    text: clean(el.innerText).slice(0, 280),
    rect: rectOf(el),
    style: styleOf(el)
  }));

  const links = Array.from(document.querySelectorAll("a[href]")).slice(0, 220).map((el) => ({
    text: clean(el.innerText || el.getAttribute("aria-label") || el.getAttribute("title")),
    href: abs(el.getAttribute("href")),
    className: el.className && typeof el.className === "string" ? el.className : ""
  })).filter((item) => item.href);

  const logos = images.filter((img) => /logo|brand|wordmark|mark/i.test([img.src, img.alt, img.className].join(" "))).slice(0, 30);
  const proofLinks = links.filter((link) => /customer|case|story|award|analyst|gartner|forrester|proof|resource|report|webinar|study/i.test([link.text, link.href, link.className].join(" "))).slice(0, 60);
  const ctaTexts = buttons.map((item) => item.text).filter(Boolean).slice(0, 80);

  const fixedOrSticky = Array.from(document.querySelectorAll("header,nav,[class*='sticky' i],[class*='fixed' i]")).filter(visible).map((el) => {
    const style = window.getComputedStyle(el);
    return {tag: el.tagName.toLowerCase(), className: el.className && typeof el.className === "string" ? el.className : "", position: style.position, rect: rectOf(el)};
  }).filter((item) => item.position === "fixed" || item.position === "sticky").slice(0, 20);

  return {
    url: location.href,
    title: document.title,
    lang: document.documentElement.lang || "",
    viewport: {width: window.innerWidth, height: window.innerHeight},
    metrics: {
      scrollWidth: document.documentElement.scrollWidth,
      scrollHeight: document.documentElement.scrollHeight,
      bodyScrollHeight: document.body ? document.body.scrollHeight : 0
    },
    meta,
    cssVariables,
    colorCounts: styleCount("body,header,main,section,footer,article,div,a,button,h1,h2,h3,p,span,li", ["color", "backgroundColor", "borderTopColor"]),
    fontCounts: styleCount("body,h1,h2,h3,p,a,button,nav,li", ["fontFamily"]),
    headings,
    buttons,
    images,
    backgroundImages,
    cards,
    sections,
    links,
    logos,
    proofLinks,
    ctaTexts,
    interactionPatterns: {
      fixedOrSticky,
      hasVideo: !!document.querySelector("video,iframe[src*='youtube'],iframe[src*='vimeo']"),
      hasCarousel: !!document.querySelector("[class*='carousel' i],[class*='slider' i],[class*='swiper' i]"),
      hasTabs: !!document.querySelector("[role='tab'],[class*='tab' i]"),
      hasForms: !!document.querySelector("form,input,select,textarea"),
      prefersReducedMotionCSS: Array.from(document.styleSheets).length > 0
    }
  };
})()
"""


class ChromeCDP:
    def __init__(self, chrome_path: str, timeout: float = 20.0) -> None:
        self.chrome_path = chrome_path
        self.timeout = timeout
        self.temp_dir: tempfile.TemporaryDirectory[str] | None = None
        self.proc: subprocess.Popen[bytes] | None = None
        self.ws: WebSocketClient | None = None
        self.message_id = 0

    def __enter__(self) -> "ChromeCDP":
        self.start()
        return self

    def __exit__(self, *_: object) -> None:
        self.stop()

    def start(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="brand-harvest-chrome-")
        user_data = self.temp_dir.name
        cmd = [
            self.chrome_path,
            "--headless=new",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-dev-shm-usage",
            "--disable-features=Translate,BackForwardCache",
            "--no-first-run",
            "--no-default-browser-check",
            "--hide-scrollbars",
            "--remote-debugging-port=0",
            f"--user-data-dir={user_data}",
            "about:blank",
        ]
        self.proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        active_file = Path(user_data) / "DevToolsActivePort"
        deadline = time.time() + self.timeout
        while time.time() < deadline:
            if active_file.exists():
                break
            if self.proc.poll() is not None:
                raise RuntimeError("Chrome exited before DevTools started")
            time.sleep(0.1)
        if not active_file.exists():
            raise RuntimeError("Chrome DevTools port was not created")
        port = active_file.read_text().splitlines()[0].strip()
        targets = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=self.timeout).read())
        page = next((target for target in targets if target.get("type") == "page"), targets[0])
        self.ws = WebSocketClient.connect(page["webSocketDebuggerUrl"], timeout=self.timeout)
        self.call("Page.enable")
        self.call("Runtime.enable")
        self.call("Network.enable")
        self.call("Network.setUserAgentOverride", {"userAgent": USER_AGENT})

    def stop(self) -> None:
        if self.ws:
            self.ws.close()
            self.ws = None
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
            self.proc = None
        if self.temp_dir:
            self.temp_dir.cleanup()
            self.temp_dir = None

    def call(self, method: str, params: dict[str, Any] | None = None, timeout: float | None = None) -> dict[str, Any]:
        if not self.ws:
            raise RuntimeError("Chrome DevTools websocket is not connected")
        self.message_id += 1
        request_id = self.message_id
        self.ws.send_json({"id": request_id, "method": method, "params": params or {}})
        deadline = time.time() + (timeout or self.timeout)
        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                raise TimeoutError(f"Timed out waiting for CDP method {method}")
            message = self.ws.recv_json(timeout=remaining)
            if message.get("id") != request_id:
                continue
            if "error" in message:
                raise RuntimeError(f"CDP {method} failed: {message['error']}")
            return message.get("result", {})

    def navigate(self, url: str, width: int, height: int, mobile: bool = False) -> None:
        self.call(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": width,
                "height": height,
                "deviceScaleFactor": 1,
                "mobile": mobile,
                "screenWidth": width,
                "screenHeight": height,
            },
        )
        self.call("Page.navigate", {"url": url}, timeout=self.timeout)
        self.wait_ready()

    def wait_ready(self) -> None:
        deadline = time.time() + self.timeout
        time.sleep(1.0)
        while time.time() < deadline:
            try:
                result = self.evaluate("document.readyState")
                if result in {"interactive", "complete"}:
                    time.sleep(1.2)
                    return
            except Exception:
                pass
            time.sleep(0.25)

    def evaluate(self, expression: str) -> Any:
        result = self.call(
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True, "awaitPromise": True},
            timeout=self.timeout,
        )
        remote = result.get("result", {})
        if "value" in remote:
            return remote["value"]
        return remote

    def screenshot(self, out_path: Path, max_height: int = 30000) -> dict[str, Any]:
        metrics = self.call("Page.getLayoutMetrics")
        content = metrics.get("contentSize", {})
        width = max(1, int(content.get("width") or 1440))
        height = max(1, int(content.get("height") or 1000))
        clipped = False
        if height > max_height:
            height = max_height
            clipped = True
        data = self.call(
            "Page.captureScreenshot",
            {
                "format": "png",
                "fromSurface": True,
                "captureBeyondViewport": True,
                "clip": {"x": 0, "y": 0, "width": width, "height": height, "scale": 1},
            },
            timeout=max(30.0, self.timeout),
        ).get("data")
        if not data:
            raise RuntimeError("Chrome returned no screenshot data")
        out_path.write_bytes(base64.b64decode(data))
        return {"path": str(out_path), "width": width, "height": height, "clipped": clipped}


def devtools_harvest(
    source_url: str,
    screenshots_dir: Path,
    timeout: float,
    capture: bool,
    max_screenshot_height: int,
) -> dict[str, Any]:
    chrome = find_chrome()
    if not chrome:
        return {"status": "skipped", "reason": "Chrome/Chromium executable not found"}

    screenshots_dir.mkdir(parents=True, exist_ok=True)
    result: dict[str, Any] = {
        "status": "ok",
        "engine": "chrome-devtools-protocol",
        "chrome_path": chrome,
        "desktop": {},
        "mobile": {},
        "screenshots": {},
        "errors": [],
    }
    try:
        with ChromeCDP(chrome, timeout=timeout) as browser:
            browser.navigate(source_url, width=1440, height=1000, mobile=False)
            result["desktop"] = browser.evaluate(HARVEST_JS)
            if capture:
                result["screenshots"]["desktop_full"] = browser.screenshot(
                    screenshots_dir / "homepage-desktop-full.png",
                    max_height=max_screenshot_height,
                )

            browser.navigate(source_url, width=390, height=900, mobile=True)
            result["mobile"] = browser.evaluate(HARVEST_JS)
            if capture:
                result["screenshots"]["mobile_full"] = browser.screenshot(
                    screenshots_dir / "homepage-mobile-full.png",
                    max_height=max_screenshot_height,
                )
    except Exception as exc:
        result["status"] = "partial" if result.get("desktop") else "error"
        result["errors"].append(str(exc))
    return result


def copy_manual_screenshots(paths: list[str], screenshots_dir: Path) -> list[dict[str, Any]]:
    copied: list[dict[str, Any]] = []
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    for index, raw_path in enumerate(paths, start=1):
        source = Path(raw_path).expanduser()
        if not source.exists():
            copied.append({"source": raw_path, "status": "missing"})
            continue
        target = screenshots_dir / f"manual-{index}{source.suffix.lower() or '.png'}"
        shutil.copy2(source, target)
        copied.append({"source": raw_path, "status": "copied", "path": str(target)})
    return copied


def top_values(items: list[dict[str, Any]], key: str = "value", limit: int = 8) -> list[str]:
    values = []
    for item in items:
        value = item.get(key)
        if value and value not in values:
            values.append(value)
        if len(values) >= limit:
            break
    return values


def is_noise_cta(text: str | None) -> bool:
    value = (text or "").strip().lower()
    if not value:
        return True
    noise = {
        "skip to main content",
        "search",
        "open search form",
        "en",
        "europe",
        "americas",
        "asia pacific",
        "other",
    }
    return value in noise


def meaningful_buttons(buttons: list[dict[str, Any]], limit: int | None = None) -> list[dict[str, Any]]:
    selected = []
    for button in buttons:
        text = button.get("text")
        href = button.get("href")
        style = button.get("style") or {}
        if is_noise_cta(text):
            continue
        has_shape = bool(style.get("backgroundColor")) or style.get("borderRadius") not in {None, "", "0px"} or style.get("padding") not in {None, "", "0px"}
        if not (href or has_shape):
            continue
        selected.append(button)
        if limit and len(selected) >= limit:
            break
    return selected


def clean_cta_texts(values: list[str]) -> list[str]:
    cleaned = []
    for value in values:
        text = " ".join(str(value).split())
        if is_noise_cta(text):
            continue
        if text not in cleaned:
            cleaned.append(text)
    return cleaned


def pick_brandfetch_colors(brandfetch: dict[str, Any]) -> list[str]:
    data = brandfetch.get("data") if brandfetch.get("status") == "ok" else None
    if not isinstance(data, dict):
        return []
    colors = []
    for item in data.get("colors", []) or []:
        value = item.get("hex")
        if value and value not in colors:
            colors.append(value.upper())
    return colors


def pick_brandfetch_fonts(brandfetch: dict[str, Any]) -> list[str]:
    data = brandfetch.get("data") if brandfetch.get("status") == "ok" else None
    if not isinstance(data, dict):
        return []
    fonts = []
    for item in data.get("fonts", []) or []:
        name = item.get("name") or item.get("font")
        if name and name not in fonts:
            fonts.append(name)
    return fonts


def is_neutral_hex(value: str) -> bool:
    if not re.match(r"^#[0-9A-Fa-f]{6}$", value or ""):
        return False
    red = int(value[1:3], 16)
    green = int(value[3:5], 16)
    blue = int(value[5:7], 16)
    spread = max(red, green, blue) - min(red, green, blue)
    return spread < 18 or max(red, green, blue) < 28 or min(red, green, blue) > 236


def structured_brain_pool(resolved: dict[str, Any], brandfetch: dict[str, Any], basic: dict[str, Any], devtools: dict[str, Any]) -> dict[str, Any]:
    desktop = devtools.get("desktop") if isinstance(devtools.get("desktop"), dict) else {}
    mobile = devtools.get("mobile") if isinstance(devtools.get("mobile"), dict) else {}
    identity_meta = desktop.get("meta") or basic.get("meta") or []
    headings = desktop.get("headings") or basic.get("headings") or []
    images = desktop.get("images") or basic.get("images") or []
    links = desktop.get("links") or basic.get("links") or []
    buttons = desktop.get("buttons") or []
    colors = pick_brandfetch_colors(brandfetch) or top_values(desktop.get("colorCounts", []), limit=12) or basic.get("colors_from_source", [])[:12]
    fonts = pick_brandfetch_fonts(brandfetch) or top_values(desktop.get("fontCounts", []), limit=8) or basic.get("font_families_from_source", [])[:8]
    css_variables = desktop.get("cssVariables") or basic.get("css_variables_from_source", {})
    logos = desktop.get("logos") or [
        image for image in images if re.search(r"logo|brand|wordmark|mark", " ".join(str(value) for value in image.values()), re.I)
    ][:30]
    proof_assets = desktop.get("proofLinks") or [
        link for link in links if re.search(r"customer|case|story|award|analyst|report|webinar|study", json.dumps(link), re.I)
    ][:60]
    risks: list[str] = []
    if resolved.get("confidence") == "low":
        risks.append("Input could not be resolved to a source URL.")
    if brandfetch.get("status") != "ok":
        risks.append(f"Brandfetch data unavailable: {brandfetch.get('reason') or brandfetch.get('status')}")
    if devtools.get("status") not in {"ok", "partial"}:
        risks.append(f"DevTools harvest unavailable: {devtools.get('reason') or devtools.get('errors')}")
    if not logos:
        risks.append("No obvious logo assets found; verify official logo source before board build.")
    if not colors:
        risks.append("No reliable brand colors found; inspect screenshots manually before styling.")
    overlay_text = " ".join(
        str(item.get("text", ""))
        for item in (desktop.get("sections", [])[:6] + desktop.get("buttons", [])[:20])
        if isinstance(item, dict)
    ).lower()
    sticky_items = (desktop.get("interactionPatterns") or {}).get("fixedOrSticky", [])
    if sticky_items and re.search(r"\b(cookie|privacy|consent|tailor your privacy|select.*region)\b", overlay_text):
        risks.append("A cookie/privacy or region overlay may be captured in screenshots; use a dismissed manual GoFullPage capture or rerun after handling the banner.")
    return {
        "identity": {
            "name": (brandfetch.get("data") or {}).get("name") if brandfetch.get("status") == "ok" else None,
            "domain": resolved.get("domain"),
            "source_url": resolved.get("source_url"),
            "title": desktop.get("title") or basic.get("title"),
            "meta": identity_meta,
            "headings": headings[:30],
        },
        "visual_tokens": {
            "colors": colors,
            "fonts": fonts,
            "css_variables": css_variables,
            "desktop_color_counts": desktop.get("colorCounts", []),
            "desktop_font_counts": desktop.get("fontCounts", []),
        },
        "component_pool": {
            "buttons": buttons[:60],
            "cards": desktop.get("cards", [])[:60],
            "sections": desktop.get("sections", [])[:50],
            "header_or_sticky": (desktop.get("interactionPatterns") or {}).get("fixedOrSticky", []),
        },
        "asset_pool": {
            "logos": logos,
            "images": images[:80],
            "background_images": desktop.get("backgroundImages", [])[:50],
            "brandfetch_logos": (brandfetch.get("data") or {}).get("logos", []) if brandfetch.get("status") == "ok" else [],
        },
        "proof_pool": {
            "proof_links": proof_assets,
            "cta_texts": clean_cta_texts(desktop.get("ctaTexts", []))[:80],
            "source_links": links[:100],
        },
        "interaction_pool": desktop.get("interactionPatterns", {}),
        "responsive_pool": {
            "desktop_metrics": desktop.get("metrics", {}),
            "mobile_metrics": mobile.get("metrics", {}),
            "mobile_headings": mobile.get("headings", [])[:20],
            "mobile_buttons": mobile.get("buttons", [])[:30],
        },
        "risks": risks,
    }


def summarize_surface(pool: dict[str, Any]) -> str:
    colors = pool["visual_tokens"].get("colors", [])[:8]
    sections = pool["component_pool"].get("sections", [])[:8]
    surfaces = []
    for section in sections:
        style = section.get("style", {})
        bg = style.get("backgroundColor")
        if bg and bg not in surfaces:
            surfaces.append(bg)
    parts = []
    if colors:
        parts.append("brand colors " + ", ".join(colors))
    if surfaces:
        parts.append("observed section backgrounds " + ", ".join(surfaces[:6]))
    return "; ".join(parts) or "No reliable surface signal captured."


def summarize_type(pool: dict[str, Any]) -> str:
    fonts = pool["visual_tokens"].get("fonts", [])[:5]
    headings = pool["identity"].get("headings", [])[:4]
    heading_text = [item.get("text", "")[:80] for item in headings if item.get("tag") == "h1"]
    parts = []
    if fonts:
        parts.append("font families " + " | ".join(fonts))
    if heading_text:
        parts.append("H1 sample: " + " / ".join(heading_text))
    return "; ".join(parts) or "No reliable type signal captured."


def summarize_structure(pool: dict[str, Any]) -> str:
    sections = pool["component_pool"].get("sections", [])[:8]
    labels = []
    for section in sections:
        text = section.get("text") or section.get("className") or section.get("tag")
        text = " ".join(str(text).split())[:90]
        if text:
            labels.append(text)
    return " | ".join(labels[:6]) if labels else "No reliable structure signal captured."


def summarize_buttons(pool: dict[str, Any]) -> str:
    buttons = meaningful_buttons(pool["component_pool"].get("buttons", []), limit=10)
    if not buttons:
        buttons = pool["component_pool"].get("buttons", [])[:10]
    values = []
    for button in buttons:
        style = button.get("style", {})
        text = button.get("text") or button.get("href") or "button"
        values.append(
            f"{text[:40]}: bg {style.get('backgroundColor')}, text {style.get('color')}, "
            f"radius {style.get('borderRadius')}, font {style.get('fontWeight')}"
        )
    return "\n".join(f"  - {value}" for value in values) or "  - No button variants captured."


def choose_shape(pool: dict[str, Any]) -> str:
    proof_count = len(pool["proof_pool"].get("proof_links", []))
    has_video = pool.get("interaction_pool", {}).get("hasVideo")
    has_forms = pool.get("interaction_pool", {}).get("hasForms")
    headings = " ".join(item.get("text", "") for item in pool["identity"].get("headings", [])[:20]).lower()
    if has_video or has_forms:
        return "Workbench"
    if any(token in headings for token in ("platform", "workflow", "operations", "security", "data", "automation")):
        return "Workbench"
    if proof_count >= 8 and ("customer" in headings or "case" in headings):
        return "Quote-Led Or Proof-Led"
    if any(token in headings for token in ("industry", "solution", "journey", "process")):
        return "Narrative Workflow"
    return "Split Studio"


def source_dna_markdown(pool: dict[str, Any], resolved: dict[str, Any], files: dict[str, str]) -> str:
    risks = pool.get("risks", [])
    proof = pool["proof_pool"].get("proof_links", [])[:8]
    proof_lines = "\n".join(f"  - {item.get('text') or item.get('href')}: {item.get('href')}" for item in proof) or "  - No verified proof links captured."
    return f"""# Source DNA - {resolved.get('domain') or resolved.get('query')}

Generated: {utc_now()}
Input: {resolved.get('raw')}
Resolved source: {resolved.get('source_url') or 'unresolved'}
Confidence: {resolved.get('confidence')}

Source DNA:
- Surface: {summarize_surface(pool)}
- Type: {summarize_type(pool)}
- Structure: {summarize_structure(pool)}
- Button variants:
{summarize_buttons(pool)}
- Motion: {json.dumps(pool.get('interaction_pool', {}), indent=2)}
- Proof assets:
{proof_lines}
- Risks or unavailable signals:
{chr(10).join(f'  - {risk}' for risk in risks) if risks else '  - None captured.'}

Folloze usage:
- Suggested shape: {choose_shape(pool)}
- Use this note as working input only. Do not paste source-harvest language into buyer-facing board copy.
- Verify official logo treatment before save, especially dark/light navbar variants.
- Screenshots: {files.get('screenshots_dir', '')}
"""


def board_brief_markdown(pool: dict[str, Any], resolved: dict[str, Any], target: str | None, files: dict[str, str]) -> str:
    colors = ", ".join(pool["visual_tokens"].get("colors", [])[:10]) or "not captured"
    fonts = " | ".join(pool["visual_tokens"].get("fonts", [])[:6]) or "not captured"
    logos = pool["asset_pool"].get("logos", [])[:8]
    logo_lines = "\n".join(f"- {item.get('alt') or item.get('src')}: {item.get('src')}" for item in logos) or "- No obvious logos captured"
    ctas = pool["proof_pool"].get("cta_texts", [])[:18]
    cta_lines = "\n".join(f"- {text}" for text in ctas if text) or "- No CTA labels captured"
    risks = "\n".join(f"- {risk}" for risk in pool.get("risks", [])) or "- No major harvest risks captured"
    target_line = f"\nTarget account: {target}\n" if target else ""
    return f"""# Folloze Board Brand Harvest Brief

Company/domain: {resolved.get('domain') or resolved.get('query')}
Source URL: {resolved.get('source_url') or 'unresolved'}{target_line}
Recommended experience shape: {choose_shape(pool)}

## Design Direction

- Surface: {summarize_surface(pool)}
- Typography: {fonts}
- Primary color candidates: {colors}
- Source structure: {summarize_structure(pool)}

## CTA Language Pool

{cta_lines}

## Logo And Asset Candidates

{logo_lines}

## Board Builder Notes

- Start from the source screenshots and `source-dna.md` before writing HTML.
- Treat the extracted buttons as the component map for nav, hero, resource, modal, and final CTA states.
- Use the source-site proof links only after verifying they are public and relevant to the buyer motion.
- If this becomes a Folloze MCP board, still run the normal link, analytics, mobile, and save-readiness gates.

## Risks To Resolve

{risks}

## Output Files

- Brand JSON: {files.get('brand_json', '')}
- Source DNA: {files.get('source_dna', '')}
- Brand tokens CSS: {files.get('tokens_css', '')}
- Asset manifest: {files.get('asset_manifest', '')}
- Screenshots: {files.get('screenshots_dir', '')}
"""


def css_tokens(pool: dict[str, Any]) -> str:
    colors = pool["visual_tokens"].get("colors", [])
    fonts = pool["visual_tokens"].get("fonts", [])
    buttons = meaningful_buttons(pool["component_pool"].get("buttons", []))
    cards = pool["component_pool"].get("cards", [])

    def button_style(prop: str, fallback: str) -> str:
        for button in buttons:
            value = (button.get("style") or {}).get(prop)
            if value:
                return value
        return fallback

    def card_style(prop: str, fallback: str) -> str:
        for card in cards:
            value = (card.get("style") or {}).get(prop)
            if value:
                return value
        return fallback

    chromatic = [color for color in colors if isinstance(color, str) and color.startswith("#") and not is_neutral_hex(color)]
    primary = chromatic[0] if chromatic else (colors[0] if colors else "#111827")
    accent = chromatic[1] if len(chromatic) > 1 else (colors[1] if len(colors) > 1 and colors[1] != primary else primary)
    text = "#111827"
    body_font = fonts[0] if fonts else "system-ui, sans-serif"
    display_font = fonts[1] if len(fonts) > 1 else body_font
    return f""":root {{
  --brand-primary: {primary};
  --brand-accent: {accent};
  --brand-text: {text};
  --brand-surface: #FFFFFF;
  --brand-font-display: {display_font};
  --brand-font-body: {body_font};
  --brand-button-radius: {button_style('borderRadius', '0px')};
  --brand-button-padding: {button_style('padding', '12px 18px')};
  --brand-button-font-weight: {button_style('fontWeight', '600')};
  --brand-card-radius: {card_style('borderRadius', '8px')};
  --brand-card-shadow: {card_style('boxShadow', 'none')};
}}
"""


def asset_manifest(pool: dict[str, Any], manual_screenshots: list[dict[str, Any]], screenshot_files: dict[str, Any]) -> dict[str, Any]:
    return {
        "logos": pool["asset_pool"].get("logos", []),
        "images": pool["asset_pool"].get("images", []),
        "background_images": pool["asset_pool"].get("background_images", []),
        "brandfetch_logos": pool["asset_pool"].get("brandfetch_logos", []),
        "screenshots": screenshot_files,
        "manual_screenshots": manual_screenshots,
    }


def default_out_dir(query: str) -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    return Path(tempfile.gettempdir()) / "folloze-brand-harvest" / f"{slugify(query)}-{stamp}"


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def run(args: argparse.Namespace) -> int:
    out_dir = Path(args.out).expanduser() if args.out else default_out_dir(args.query)
    screenshots_dir = out_dir / "screenshots"
    out_dir.mkdir(parents=True, exist_ok=True)
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    resolved = resolve_input(args.query, args.source_url, timeout=args.timeout)
    manual_screenshots = copy_manual_screenshots(args.manual_screenshot or [], screenshots_dir)

    if not resolved.get("source_url"):
        brandfetch = {"status": "skipped", "reason": "source URL unresolved"}
        basic = {"status": "skipped", "reason": "source URL unresolved"}
        devtools = {"status": "skipped", "reason": "source URL unresolved"}
    else:
        domain = resolved["domain"]
        brandfetch = brandfetch_brand(domain, args.brandfetch_token or os.environ.get("BRANDFETCH_API_KEY"), args.timeout)
        basic = basic_html_harvest(resolved["source_url"], args.timeout)
        devtools = devtools_harvest(
            resolved["source_url"],
            screenshots_dir=screenshots_dir,
            timeout=args.timeout,
            capture=args.capture_mode != "none",
            max_screenshot_height=args.max_screenshot_height,
        )

    pool = structured_brain_pool(resolved, brandfetch, basic, devtools)
    files = {
        "brand_json": str(out_dir / "brand.json"),
        "source_dna": str(out_dir / "source-dna.md"),
        "board_brief": str(out_dir / "folloze-board-brief.md"),
        "tokens_css": str(out_dir / "brand-tokens.css"),
        "asset_manifest": str(out_dir / "asset-manifest.json"),
        "screenshots_dir": str(screenshots_dir),
    }
    screenshot_files = devtools.get("screenshots", {}) if isinstance(devtools, dict) else {}
    brand_json = {
        "schema_version": "0.1",
        "generated_at": utc_now(),
        "input": {
            "query": args.query,
            "source_url": args.source_url,
            "target": args.target,
        },
        "resolved": resolved,
        "brandfetch": brandfetch,
        "basic_html": basic,
        "devtools": devtools,
        "structured_brain_pool": pool,
        "files": files,
    }
    write_json(out_dir / "brand.json", brand_json)
    write_json(out_dir / "asset-manifest.json", asset_manifest(pool, manual_screenshots, screenshot_files))
    (out_dir / "source-dna.md").write_text(source_dna_markdown(pool, resolved, files))
    (out_dir / "folloze-board-brief.md").write_text(board_brief_markdown(pool, resolved, args.target, files))
    (out_dir / "brand-tokens.css").write_text(css_tokens(pool))

    summary = {
        "status": "ok",
        "out_dir": str(out_dir),
        "resolved_source_url": resolved.get("source_url"),
        "domain": resolved.get("domain"),
        "confidence": resolved.get("confidence"),
        "devtools_status": devtools.get("status"),
        "brandfetch_status": brandfetch.get("status"),
        "screenshots": screenshot_files,
        "risks": pool.get("risks", []),
        "files": files,
    }
    print(json.dumps(summary, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Harvest brand/design signals for Folloze MCP board builds.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("query", help="Domain, source URL, or account name.")
    parser.add_argument("--source-url", help="Explicit source URL when query is an account name.")
    parser.add_argument("--target", help="Optional target account for the generated Folloze board brief.")
    parser.add_argument("--out", help="Output directory. Defaults to a timestamped /tmp bundle.")
    parser.add_argument("--brandfetch-token", help="Optional Brandfetch API token. Falls back to BRANDFETCH_API_KEY.")
    parser.add_argument("--manual-screenshot", action="append", default=[], help="Path to a GoFullPage/manual screenshot to copy into the bundle.")
    parser.add_argument("--capture-mode", choices=["auto", "none"], default="auto", help="Capture full-page screenshots with local Chrome when available.")
    parser.add_argument("--timeout", type=float, default=20.0, help="Network and Chrome DevTools timeout in seconds.")
    parser.add_argument("--max-screenshot-height", type=int, default=30000, help="Cap full-page screenshot height to avoid huge files.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
