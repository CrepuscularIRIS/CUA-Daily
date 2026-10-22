"""Retired entry point; original removed from the tree 2026-10-22 (git history, or local ~/GUI/moved-out-2026-10-22/)."""
import sys

def main():
    print("Legacy scoring/Reel workflow retired. Read docs/PIPELINE.md and research/SCORE_SPEC.md; no files written.", file=sys.stderr)
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
