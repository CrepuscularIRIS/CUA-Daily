"""Retired entry point; original is in archive/2026-10-21-reset/."""
import sys

def main():
    print("Legacy scoring/Reel workflow retired. Read docs/PIPELINE.md and research/SCORE_SPEC.md; no files written.", file=sys.stderr)
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
