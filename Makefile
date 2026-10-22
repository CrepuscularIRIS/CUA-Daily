.PHONY: all check help score board run test check-log
all: check
check:
	python3 test_check_cards.py
	python3 check_cards.py
	python3 -m py_compile research/*.py
	python3 research/check_patterns.py
help:
	@echo "make check: offline checks; make run: inherited relevance digest; scoring/Reel reset: docs/PIPELINE.md"
score board:
	@echo "Legacy scoring/board retired. v2 is draft_uncalibrated; read research/SCORE_SPEC.md." >&2
	@exit 2
run:
	uv run python main.py
test:
	uv run python test_digest.py
check-log:
	uv run python check_log.py
