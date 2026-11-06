"""Tests for the metrics handler."""

import threading
import unittest
import urllib.request

from api.metrics import make_server, summarize


class SummarizeTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(summarize([]), {"count": 0, "total": 0, "mean": None})

    def test_basic(self):
        result = summarize([1, 2, 3])
        self.assertEqual(result["count"], 3)
        self.assertEqual(result["total"], 6)
        self.assertEqual(result["mean"], 2)


class HandlerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server(0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def get(self, path):
        import json

        request = urllib.request.Request(f"http://127.0.0.1:{self.port}{path}")
        try:
            with urllib.request.urlopen(request) as resp:
                return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as err:
            return err.code, json.loads(err.read())

    def test_healthz(self):
        status, payload = self.get("/healthz")
        self.assertEqual(status, 200)
        self.assertEqual(payload, {"status": "ok"})

    def test_summarize(self):
        status, payload = self.get("/summarize?numbers=1,2,3")
        self.assertEqual(status, 200)
        self.assertEqual(payload["total"], 6)
        self.assertEqual(payload["mean"], 2)

    def test_summarize_invalid(self):
        status, payload = self.get("/summarize?numbers=1,x")
        self.assertEqual(status, 400)
        self.assertIn("invalid number", payload["error"])

    def test_not_found(self):
        status, payload = self.get("/nope")
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
