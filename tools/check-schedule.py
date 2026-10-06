#!/usr/bin/env python3
# Load a schedule as records/SPEC.md section 3 reads one, and report how each
# row classifies: permanent, retired, computable, or descriptive. Exits 1 when
# the file is malformed (section 3.5, or an extension value outside its set).
#
# Usage: check-schedule.py <schedule.csv>
#
# Author: David M. Anderson
# Built with AI assistance (Claude, Anthropic)

import collections
import csv
import io
import re
import sys

REQUIRED = ["grs id", "record title", "disposition", "retention type",
            "event type (general)", "longer retention authorized?"]
PERIOD = re.compile(r"^(\d+)([md]?)$")
EXTENSIONS = {
    "x_disposal_action": {"destroy", "transfer", "review", "retain"},
    "x_cutoff": {"none", "calendar_year", "fiscal_year", "quarter", "month"},
    "x_period_kind": {"minimum", "maximum", "fixed"},
    "x_citation_defining": {"yes", "no"},
}
NOT_STATED = {"", "n/a", "na", "[variable]"}


def norm(value: str) -> str:
    return value.strip().lower()


def stated(value: str) -> bool:
    return norm(value) not in NOT_STATED


def main() -> None:
    raw = open(sys.argv[1], "rb").read().decode("utf-8-sig")
    rows = list(csv.reader(io.StringIO(raw, newline="")))
    header = [norm(h) for h in rows[0]]
    columns = {h: i for i, h in enumerate(header) if h}
    problems = []

    if "retention (years)" in columns and "retention" in columns:
        problems.append("row 1: both `Retention (Years)` and `Retention` are present")
    retention = columns.get("retention (years)", columns.get("retention"))
    if retention is None:
        problems.append("row 1: no `Retention (Years)` column")
    for name in REQUIRED:
        if name not in columns:
            problems.append(f"row 1: no `{name}` column")
    if problems:
        print("\n".join(problems))
        raise SystemExit(1)

    def cell(row, name):
        i = columns.get(name)
        return row[i] if i is not None and i < len(row) else ""

    seen = collections.Counter()
    kinds = collections.Counter()
    for n, row in enumerate(rows[1:], start=2):
        if not any(x.strip() for x in row):
            continue
        code = cell(row, "grs id").strip()
        if not code:
            problems.append(f"row {n}: empty GRS ID")
            continue
        key = (code, norm(cell(row, "x_jurisdiction")))
        seen[key] += 1
        if seen[key] > 1:
            problems.append(f"row {n}: GRS ID {code!r} repeated for the same jurisdiction")
        for name, allowed in EXTENSIONS.items():
            v = cell(row, name)
            if v.strip() and norm(v) not in allowed:
                problems.append(f"row {n}: {name} is {v!r}, not one of {sorted(allowed)}")
        if stated(cell(row, "x_maximum")) and not PERIOD.match(norm(cell(row, "x_maximum"))):
            problems.append(f"row {n}: x_maximum {cell(row, 'x_maximum')!r} is not a period")
        if stated(cell(row, "x_maximum")) and norm(cell(row, "x_period_kind")) not in ("", "minimum"):
            problems.append(f"row {n}: x_maximum with x_period_kind {cell(row, 'x_period_kind')!r}")

        disposition = norm(cell(row, "disposition"))
        period = norm(row[retention]) if retention < len(row) else ""
        rtype = norm(cell(row, "retention type"))
        event = cell(row, "event type (general)")
        if disposition == "permanent":
            kinds["permanent"] += 1
        elif cell(row, "superseded by").strip():
            kinds["retired"] += 1
        elif (disposition == "temporary" and rtype in ("creation_age", "event_age")
              and PERIOD.match(period) and (rtype == "creation_age" or stated(event))):
            kinds["computable"] += 1
        else:
            kinds["descriptive"] += 1

    if problems:
        print("\n".join(problems))
        raise SystemExit(1)
    total = sum(kinds.values())
    print(f"loaded {total} rows: " + ", ".join(f"{k} {v}" for k, v in sorted(kinds.items())))


if __name__ == "__main__":
    main()
