.PHONY: run help all check-log test check score board

all: check

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  check     - Card schema tests + card check + compile research/*.py (what CI runs)"
	@echo "  score     - Merge assignments and rebuild research/scores.jsonl from research/judgments/"
	@echo "  board     - Render papers/README.md and the README board block from scores.jsonl"
	@echo "  run       - Fetch today's arXiv digest (inherited candidate fetcher; needs config.json + API key)"
	@echo "  test      - Run offline rendering unit tests of the digest"
	@echo "  check-log - Check digest activity logs"
	@echo "  help      - Display this help message"

check:
	python3 test_check_cards.py && python3 check_cards.py
	python3 -m py_compile research/*.py

score:
	python3 research/merge_assign.py
	PYTHONPATH=research python3 research/score.py build

board:
	python3 research/build_board.py

run:
	uv run python main.py

test:
	uv run python test_digest.py

check-log:
	uv run python check_log.py
