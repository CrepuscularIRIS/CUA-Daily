"""Polite HTTP GET for the ingestion scripts: fixed pacing, HTTP 429 surfaced with its Retry-After, no retry loops.

Policy (docs/agents/GROK_PROMPT.md rule 7): ≥ PACE seconds between requests to the same host — arXiv's API terms ask
for 3 s and the same pace is used for arxiv.org/html. On 429 the caller gets RateLimited carrying the server's
Retry-After; `get` waits that long (capped at MAX_WAIT) and tries exactly once more, then raises so the run stops
without caching anything. Override the pace with CUA_RADAR_PACE (seconds).
"""

import os
import time
import urllib.error
import urllib.request
from email.utils import parsedate_to_datetime

USER_AGENT = "cua-radar/0.1 (+https://github.com/CrepuscularIRIS/cua-architecture-radar)"
PACE = float(os.environ.get("CUA_RADAR_PACE", "3"))
MAX_WAIT = 600  # a Retry-After longer than this stops the run instead of sleeping
DEFAULT_WAIT = 60  # 429 without a usable Retry-After

_last: dict[str, float] = {}


class RateLimited(Exception):
    def __init__(self, url: str, retry_after: float | None):
        super().__init__(f"HTTP 429 from {url} (Retry-After: {retry_after if retry_after is not None else 'absent'})")
        self.url, self.retry_after = url, retry_after


def retry_after_seconds(value: str | None, now: float | None = None) -> float | None:
    """Parse a Retry-After header: delta-seconds or an HTTP date. None if absent or unparseable."""
    if not value:
        return None
    value = value.strip()
    if value.isdigit():
        return float(value)
    try:
        return max(0.0, parsedate_to_datetime(value).timestamp() - (time.time() if now is None else now))
    except (TypeError, ValueError):
        return None


def _pace(host: str, pace: float) -> None:
    wait = _last.get(host, 0.0) + pace - time.monotonic()
    if wait > 0:
        time.sleep(wait)
    _last[host] = time.monotonic()


def _once(url: str, timeout: float, pace: float) -> bytes:
    _pace(urllib.request.urlparse(url).netloc, pace)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise RateLimited(url, retry_after_seconds(e.headers.get("Retry-After"))) from e
        raise


def get(url: str, timeout: float = 60, pace: float = PACE) -> bytes:
    """GET with pacing. On 429: honor Retry-After once, retry once; a second 429 (or a wait > MAX_WAIT) raises."""
    try:
        return _once(url, timeout, pace)
    except RateLimited as e:
        wait = DEFAULT_WAIT if e.retry_after is None else e.retry_after
        if wait > MAX_WAIT:
            raise
        print(f"429 from {url}; waiting {wait:.0f}s as advised, then one retry", flush=True)
        time.sleep(wait)
        return _once(url, timeout, pace)
