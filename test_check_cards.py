"""Smallest check that check_cards.py accepts a valid card and rejects broken ones."""

from pathlib import Path

from check_cards import SECTIONS, check

VALID = """---
id: demo
title: "Demo: A Title"   # comment is stripped
authors: "A et al."
first_seen: 2026-01-01
arxiv: "2601.00001v1"
openreview: null
code: null
code_commit: null
license: null
venue: "arXiv preprint"
tier: A
platforms: [web, mobile]
components: [grounding, rl]
evidence_level: online
held_out: yes
budget_matched: partial
leakage_risk: low
code_status: none
checked: 2026-10-18
---
""" + "\n".join(SECTIONS)


def test_check_cards(tmp: Path = Path("/tmp/check_cards_test")) -> None:
    tmp.mkdir(exist_ok=True)
    good = tmp / "demo.md"
    good.write_text(VALID, encoding="utf-8")
    assert check(good) == [], check(good)

    bad = tmp / "demo.md"
    bad.write_text(VALID.replace("tier: A", "tier: C").replace("[web, mobile]", "[robot]")
                   .replace("## 来源", ""), encoding="utf-8")
    errs = check(bad)
    assert any(e.startswith("tier=") for e in errs), errs
    assert any(e.startswith("platforms=") for e in errs), errs
    assert "missing section: ## 来源" in errs, errs

    renamed = tmp / "other.md"
    renamed.write_text(VALID, encoding="utf-8")
    assert any("filename stem" in e for e in check(renamed))


if __name__ == "__main__":
    test_check_cards()
    print("ok")
