"""CI turns red unless every required row receives full marks, including gates."""
from __future__ import annotations
import json
import sys
from pathlib import Path

# Import metadata only; no app, network, or test subprocesses.
from check import REQUIRED

def gate(report):
    rows = report.get("results", [])
    names = [row.get("name") for row in rows]
    return report.get("total") == sum(REQUIRED.values()) and report.get("score") == sum(REQUIRED.values()) \
        and len(names) == len(REQUIRED) and set(names) == set(REQUIRED) \
        and all(row.get("status") == "pass" and row.get("points") == REQUIRED[row["name"]]
                and row.get("max") == REQUIRED[row["name"]] for row in rows)

if __name__ == "__main__":
    try:
        valid = gate(json.loads(Path("results/report.json").read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError):
        valid = False
    print("PASS required gate" if valid else "FAIL required gate: rerun bash check.sh and inspect failing rows")
    sys.exit(0 if valid else 1)
