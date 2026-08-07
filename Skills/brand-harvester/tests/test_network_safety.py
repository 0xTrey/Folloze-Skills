from __future__ import annotations

import importlib.util
import socket
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "brand_harvest.py"
SPEC = importlib.util.spec_from_file_location("brand_harvest_under_test", SCRIPT)
assert SPEC and SPEC.loader
brand_harvest = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(brand_harvest)


class PublicUrlSafetyTests(unittest.TestCase):
    def test_rejects_non_http_schemes(self) -> None:
        for url in ("file:///etc/passwd", "ftp://example.com/file", "gopher://example.com"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                brand_harvest.validate_public_url(url)

    def test_rejects_literal_private_and_metadata_addresses(self) -> None:
        for url in (
            "http://127.0.0.1",
            "http://10.0.0.1",
            "http://172.16.0.1",
            "http://192.168.1.2",
            "http://169.254.169.254/latest/meta-data",
            "http://[::1]",
            "http://[fc00::1]",
            "http://[fe80::1]",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                brand_harvest.validate_public_url(url)

    @mock.patch.object(socket, "getaddrinfo")
    def test_rejects_hostname_resolving_to_private_address(self, getaddrinfo: mock.Mock) -> None:
        getaddrinfo.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.1.2.3", 443))]
        with self.assertRaises(ValueError):
            brand_harvest.validate_public_url("https://public-looking.example")

    @mock.patch.object(socket, "getaddrinfo")
    def test_allows_hostname_resolving_only_to_global_addresses(self, getaddrinfo: mock.Mock) -> None:
        getaddrinfo.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))]
        self.assertEqual(
            brand_harvest.validate_public_url("https://example.com/path"),
            "https://example.com/path",
        )

    @mock.patch.object(socket, "getaddrinfo")
    def test_redirect_handler_rejects_private_destination(self, getaddrinfo: mock.Mock) -> None:
        getaddrinfo.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))]
        handler = brand_harvest.PublicOnlyRedirectHandler()
        request = brand_harvest.urllib.request.Request("https://example.com")
        with self.assertRaises(ValueError):
            handler.redirect_request(
                request,
                None,
                302,
                "Found",
                {},
                "http://169.254.169.254/latest/meta-data",
            )

    @mock.patch.object(socket, "getaddrinfo")
    def test_redirect_handler_rejects_authenticated_cross_host_redirect(self, getaddrinfo: mock.Mock) -> None:
        getaddrinfo.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))]
        handler = brand_harvest.PublicOnlyRedirectHandler()
        request = brand_harvest.urllib.request.Request(
            "https://api.brandfetch.io/v2/brands/domain/example.com",
            headers={"Authorization": "Bearer example-token-value"},
        )
        with self.assertRaises(ValueError):
            handler.redirect_request(
                request,
                None,
                302,
                "Found",
                {},
                "https://other.example/collect",
            )

    @mock.patch.object(socket, "getaddrinfo")
    def test_chrome_interception_blocks_private_subrequest(self, getaddrinfo: mock.Mock) -> None:
        getaddrinfo.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))]

        class FakeWebSocket:
            def __init__(self) -> None:
                self.messages: list[dict[str, object]] = []

            def send_json(self, message: dict[str, object]) -> None:
                self.messages.append(message)

        chrome = brand_harvest.ChromeCDP("/unused")
        chrome.ws = FakeWebSocket()
        chrome._handle_paused_request(
            {
                "requestId": "private-request",
                "request": {"url": "http://169.254.169.254/latest/meta-data"},
            }
        )
        self.assertEqual(chrome.ws.messages[-1]["method"], "Fetch.failRequest")

    @mock.patch.object(socket, "getaddrinfo")
    def test_chrome_interception_allows_public_subrequest(self, getaddrinfo: mock.Mock) -> None:
        getaddrinfo.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))]

        class FakeWebSocket:
            def __init__(self) -> None:
                self.messages: list[dict[str, object]] = []

            def send_json(self, message: dict[str, object]) -> None:
                self.messages.append(message)

        chrome = brand_harvest.ChromeCDP("/unused")
        chrome.ws = FakeWebSocket()
        chrome._handle_paused_request(
            {"requestId": "public-request", "request": {"url": "https://example.com/logo.svg"}}
        )
        self.assertEqual(chrome.ws.messages[-1]["method"], "Fetch.continueRequest")


if __name__ == "__main__":
    unittest.main()
