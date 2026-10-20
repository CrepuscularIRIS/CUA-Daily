"""Offline tests for research/net.py and the 429/404 handling in fetch_fulltext.py (local HTTP server, no internet).

Run: python3 test_net.py
"""

import json
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "research"))
import net  # noqa: E402

ROOT = Path(__file__).parent


class Handler(BaseHTTPRequestHandler):
    """/ok → 200; /404 → 404; /429-<n>-<retry> → 429 for the first n hits (Retry-After <retry>), then 200."""

    hits: dict[str, int] = {}

    def do_GET(self) -> None:  # noqa: N802
        Handler.hits[self.path] = Handler.hits.get(self.path, 0) + 1
        name = self.path.rsplit("/", 1)[-1]
        if name.startswith("429-"):
            _, n, retry = name.split("-")
            if Handler.hits[self.path] <= int(n):
                self.send_response(429)
                if retry != "none":
                    self.send_header("Retry-After", retry)
                self.end_headers()
                return
        if name.startswith("404"):
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"<html><body><section class='ltx_section'><h2>1 Introduction</h2><p>hello</p></section></body></html>")

    def log_message(self, *a) -> None:
        pass


class NetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.srv = HTTPServer(("127.0.0.1", 0), Handler)
        cls.base = f"http://127.0.0.1:{cls.srv.server_port}"
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.srv.shutdown()

    def test_retry_after_parsing(self) -> None:
        self.assertEqual(net.retry_after_seconds("7"), 7.0)
        self.assertIsNone(net.retry_after_seconds(None))
        self.assertIsNone(net.retry_after_seconds("soon"))
        self.assertAlmostEqual(net.retry_after_seconds("Wed, 21 Oct 2015 07:28:10 GMT", now=1445412480.0), 10.0)

    def test_one_429_waits_then_succeeds(self) -> None:
        self.assertIn(b"hello", net.get(f"{self.base}/a/429-1-0", pace=0))
        self.assertEqual(Handler.hits["/a/429-1-0"], 2)

    def test_second_429_raises_without_loop(self) -> None:
        with self.assertRaises(net.RateLimited) as cm:
            net.get(f"{self.base}/b/429-5-0", pace=0)
        self.assertEqual(cm.exception.retry_after, 0.0)
        self.assertEqual(Handler.hits["/b/429-5-0"], 2)

    def test_long_retry_after_raises_immediately(self) -> None:
        with self.assertRaises(net.RateLimited):
            net.get(f"{self.base}/c/429-1-{net.MAX_WAIT + 1}", pace=0)
        self.assertEqual(Handler.hits[f"/c/429-1-{net.MAX_WAIT + 1}"], 1)

    def _fetch(self, version: str) -> tuple[int, Path]:
        tmp = Path(tempfile.mkdtemp())
        (tmp / "corpus.jsonl").write_text(json.dumps({"arxiv": "x", "latest_version": version, "title": "T",
                                                      "published": "2026-01-01", "abstract": "A"}) + "\n")
        (tmp / "ids.txt").write_text("x\n")
        code = (f"import sys; sys.argv=['f','--ids','{tmp}/ids.txt','--corpus','{tmp}/corpus.jsonl','--out','{tmp}/ft'];"
                f"sys.path.insert(0,'{ROOT}/research'); import net; net.PACE=0; net.MAX_WAIT=0;"
                f"import fetch_fulltext as f; f.URL='{self.base}/'+'{{id}}'; f.main()")
        return subprocess.run([sys.executable, "-c", code], capture_output=True).returncode, tmp / "ft" / "x.txt"

    def test_fulltext_429_stops_and_caches_nothing(self) -> None:
        rc, out = self._fetch("429-9-5")
        self.assertEqual(rc, 75)
        self.assertFalse(out.exists())

    def test_fulltext_404_caches_abstract_only(self) -> None:
        rc, out = self._fetch("404")
        self.assertEqual(rc, 0)
        self.assertTrue(out.read_text().startswith("FULLTEXT: none"))

    def test_fulltext_ok(self) -> None:
        rc, out = self._fetch("ok")
        self.assertEqual(rc, 0)
        self.assertIn("hello", out.read_text())


if __name__ == "__main__":
    unittest.main()
