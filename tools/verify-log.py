#!/usr/bin/env python3
# Verify a chained log against CONVENTIONS §5: delimit entries by header line,
# hash their stored bytes, and check seq and prev.
#
# Usage: verify-log.py <log-file> <entry-name> <seed-string> [expected-head]
#
# Author: David M. Anderson
# Built with AI assistance (Claude, Anthropic)

import hashlib
import sys
import tomllib


def entries_of(data: bytes, name: str) -> list[bytes]:
    header = f"[[{name}]]\n".encode()
    if not data.startswith(header):
        raise SystemExit("the file does not begin with a header line (CONVENTIONS 5.2)")
    if not data.endswith(b"\n"):
        raise SystemExit("the file does not end with LF (CONVENTIONS 5.2)")
    if b"\r" in data:
        raise SystemExit("the file contains CR (CONVENTIONS 5.2)")
    starts = [0]
    at = 0
    while True:
        at = data.find(b"\n" + header, at)
        if at < 0:
            break
        starts.append(at + 1)
        at += 1
    return [data[a:b] for a, b in zip(starts, starts[1:] + [len(data)])]


def main() -> None:
    path, name, seed = sys.argv[1:4]
    head = sys.argv[4] if len(sys.argv) > 4 else None
    data = open(path, "rb").read()
    chunks = entries_of(data, name)
    parsed = tomllib.loads(data.decode("utf-8"))[name]
    if len(parsed) != len(chunks):
        raise SystemExit(f"{len(parsed)} tables parsed but {len(chunks)} entries delimited")

    expected = hashlib.sha256(seed.encode()).hexdigest()
    for n, (entry, raw) in enumerate(zip(parsed, chunks), start=1):
        if entry.get("seq") != n:
            raise SystemExit(f"broken at entry {n}: seq is {entry.get('seq')!r}")
        if entry.get("prev") != expected:
            raise SystemExit(f"broken at entry {n}: prev does not hash the previous entry")
        expected = hashlib.sha256(raw).hexdigest()
    if head is not None and expected != head:
        raise SystemExit("the last entry does not hash to the recorded head (CONVENTIONS 5.5)")
    print(f"intact: {len(chunks)} entries, head {expected}")


if __name__ == "__main__":
    main()
