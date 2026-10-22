import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import FT, OUT, ROOT, norm, verify_quotes, write_atomic  # noqa: E402
import _seeclick as sc  # noqa: E402
import _webvoyager as wv  # noqa: E402

spec = importlib.util.spec_from_file_location("cb", ROOT / "research/v2/check_batch.py")
cb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cb)

META = {"run_id": "gui-v22-20261021-01", "batch_id": "p8", "attempt": "a1"}


def txt(name):
    return norm((FT / "fulltext" / name).read_text())


MAT = {
    "2401.10935": {"M1": txt("2401.10935.r2.txt"), "M2": txt("2401.10935.pdf-supplement.txt"), "M4": txt("2306.06070.txt")},
    "2401.13919": {"M1": txt("2401.13919.txt"), "M4": txt("2306.06070.txt"), "M5": txt("2307.13854.txt")},
}

errors, summary = [], {}
for key, mod in (("2401.10935", sc), ("2401.13919", wv)):
    rec = mod.build(META)
    bad = verify_quotes(rec, MAT[key])
    if bad:
        errors.append((key, "bad quotes", bad))
    ev_ids = {e["evidence_id"] for e in rec["evidence"]}
    # every referenced evidence id must exist
    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("evidence_ids", "counterevidence_ids", "counterevidence") and isinstance(v, list):
                    for i in v:
                        if isinstance(i, str) and i not in ev_ids:
                            errors.append((key, "missing evidence id", path + "/" + k, i))
                walk(v, path + "/" + k)
        elif isinstance(o, list):
            for n, v in enumerate(o):
                walk(v, path + f"[{n}]")
    walk(rec)
    ce = []
    cb.check_record(rec, f"son55/{key}", ce)
    if ce:
        errors.append((key, "check_record", ce))
    summary[key] = rec["score"]
    path = OUT / f"{key}.json"
    if not errors:
        write_atomic(path, rec)

print(json.dumps(summary, ensure_ascii=False, indent=1))
print("ERRORS:", json.dumps(errors, ensure_ascii=False, indent=1)[:4000])
