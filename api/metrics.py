#!/usr/bin/env python3
"""Metrics HTTP handler — standard-library only."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


def summarize(numbers):
    if not numbers:
        return {"count": 0, "total": 0, "mean": None}
    total = sum(numbers)
    return {"count": len(numbers), "total": total, "mean": total / len(numbers)}


class MetricsHandler(BaseHTTPRequestHandler):
    server_version = "Metrics/1.0"

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/healthz":
            self._send(200, {"status": "ok"})
        elif parsed.path == "/summarize":
            from urllib.parse import parse_qs

            raw = parse_qs(parsed.query).get("numbers", [""])[0]
            numbers = []
            if raw:
                for part in raw.split(","):
                    part = part.strip()
                    if not part:
                        continue
                    try:
                        numbers.append(int(part))
                    except ValueError:
                        self._send(400, {"error": f"invalid number: {part}"})
                        return
            self._send(200, summarize(numbers))
        else:
            self._send(404, {"error": "not found"})

    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


def make_server(port=8080):
    return HTTPServer(("127.0.0.1", port), MetricsHandler)


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    make_server(port).serve_forever()
