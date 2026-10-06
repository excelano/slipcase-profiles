#!/usr/bin/env python3
# Walk a register as records/SPEC.md section 6.6 says: every final's five
# hashes, the sequence without gaps or repeats, every final's intent present,
# and every unfinished intent reported. Reads a register in directory form,
# where each container is a directory holding its members.
#
# Usage: verify-register.py <register-dir>
#
# Author: David M. Anderson
# Built with AI assistance (Claude, Anthropic)

import hashlib
import pathlib
import re
import sys
import tomllib

GENESIS = hashlib.sha256(b"https://slipcaseformat.org/profiles/records#register-genesis").hexdigest()


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    root = pathlib.Path(sys.argv[1])
    intents = {int(m.group(1)): p for p in root.iterdir() if (m := re.fullmatch(r"(\d{6})\.intent\.slpc", p.name))}
    finals = {int(m.group(1)): p for p in root.iterdir() if (m := re.fullmatch(r"(\d{6})\.slpc", p.name))}
    if not intents:
        raise SystemExit("no intents: not a register")
    last = max(intents)
    previous = GENESIS
    for n in range(1, last + 1):
        intent = intents.get(n)
        if intent is None:
            raise SystemExit(f"broken at {n:06d}: no intent, so the sequence has a gap")
        final = finals.get(n)
        if final is None:
            if n != last:
                raise SystemExit(f"broken at {n:06d}: unfinished, but a later batch exists")
            print(f"{n:06d}: unfinished intent (started {disposition(intent)['started']})")
            break
        d = disposition(final)
        chain = tomllib.loads((final / "slipcase.flyleaf.toml").read_text())["records"]["chain"]
        want = {
            "intent_flyleaf_sha256": sha(intent / "slipcase.flyleaf.toml"),
            "previous_flyleaf_sha256": previous,
            "content_sha256": sha(final / d["content_file"]),
            "manifest_sha256": sha(final / "records" / "manifest.csv"),
            "journal_sha256": sha(root / f"{n:06d}.journal"),
        }
        for key, value in want.items():
            if chain.get(key) != value:
                raise SystemExit(f"broken at {n:06d}: {key} does not match")
        if d["sequence"] != n or d["state"] != "final":
            raise SystemExit(f"broken at {n:06d}: sequence or state wrong in the final")
        print(f"{n:06d}: final, {d['records_destroyed']} of {d['records_planned']} destroyed")
        previous = sha(final / "slipcase.flyleaf.toml")
    print("chain intact")


def disposition(container: pathlib.Path) -> dict:
    doc = tomllib.loads((container / "slipcase.flyleaf.toml").read_text())
    d = dict(doc["records"]["disposition"])
    d["content_file"] = doc["content"]["file"]
    return d


if __name__ == "__main__":
    main()
