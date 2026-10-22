.PHONY: all check help score board run test check-log
all: check
check:
	python3 test_check_cards.py
	python3 check_cards.py
	python3 -m py_compile research/*.py
	python3 research/check_patterns.py
help:
	@echo "make check: offline checks; current scoring contract: research/scoring/README.md; old results withdrawn"
score board:
	@echo "Legacy scoring/board retired. read research/scoring/README.md; old results withdrawn." >&2
	@exit 2
run:
	uv run python main.py
test:
	uv run python test_digest.py
check-log:
	uv run python check_log.py
