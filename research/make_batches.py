"""Write the next judge batches research/judgments/ids_bNN.txt for board papers that have full text and no batch yet.

Usage: python research/make_batches.py <start_index> <max_batches> [--size 10]
"""

import sys
from pathlib import Path

J = Path("research/judgments")


def main(start: int, n: int, size: int = 10) -> None:
    ids = Path("research/board1_ids.txt").read_text().split()
    done = set()
    for f in J.glob("ids_b*.txt"):
        done |= set(f.read_text().split())
    todo = [i for i in ids if i not in done and Path(f"research/fulltext/{i}.txt").exists()]
    made = []
    for k in range(n):
        chunk = todo[k * size:(k + 1) * size]
        if len(chunk) < size and k > 0:
            break
        if not chunk:
            break
        (J / f"ids_b{start + k:02d}.txt").write_text("\n".join(chunk) + "\n")
        made.append(f"b{start + k:02d}")
    print(" ".join(made), f"({len(todo)} ready)")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(int(a[0]), int(a[1]))
