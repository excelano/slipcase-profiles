#!/usr/bin/env python3
# Author: David M. Anderson
# Built with AI assistance (Claude, Anthropic)

import datetime
import pathlib
import re
import sys
import tomllib

PROFILE = "https://slipcaseformat.org/profiles/core"
ATTRIBUTION = ["creator", "contributor", "publisher", "rightsHolder"]
ATTRIBUTION_KEYS = ["email", "uri", "orcid", "lei"]
REPEATABLE = ["subject", "identifier", "source", "relation", "isPartOf", "coverage", "rights"]
SINGLE = ["title", "alternative", "description"]
DATES = ["date", "created", "modified", "issued"]
TYPES = {"Collection", "Dataset", "Event", "Image", "InteractiveResource", "MovingImage",
         "PhysicalObject", "Service", "Software", "Sound", "StillImage", "Text"}

RESTRICTED = r"[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]{0,126}"
MEDIA_TYPE = re.compile(rf"{RESTRICTED}/{RESTRICTED}")
URI = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*:\S+")

ALNUM = "[A-Za-z0-9]"
LANGTAG = (
    r"(?:[A-Za-z]{2,3}(?:-[A-Za-z]{3}){0,3}|[A-Za-z]{4}|[A-Za-z]{5,8})"
    r"(?:-[A-Za-z]{4})?"
    r"(?:-(?:[A-Za-z]{2}|[0-9]{3}))?"
    rf"(?:-(?:{ALNUM}{{5,8}}|[0-9]{ALNUM}{{3}}))*"
    rf"(?:-[0-9A-WYZa-wyz](?:-{ALNUM}{{2,8}})+)*"
    rf"(?:-[Xx](?:-{ALNUM}{{1,8}})+)?"
)
PRIVATEUSE = rf"[Xx](?:-{ALNUM}{{1,8}})+"
GRANDFATHERED = (
    "en-GB-oed|i-ami|i-bnn|i-default|i-enochian|i-hak|i-klingon|i-lux|i-mingo|i-navajo|"
    "i-pwn|i-tao|i-tay|i-tsu|sgn-BE-FR|sgn-BE-NL|sgn-CH-DE|art-lojban|cel-gaulish|"
    "no-bok|no-nyn|zh-guoyu|zh-hakka|zh-min|zh-min-nan|zh-xiang"
)
BCP47 = re.compile(rf"(?:{LANGTAG}|{PRIVATEUSE}|{GRANDFATHERED})", re.IGNORECASE)


class NonConformant(Exception):
    def __init__(self, rule: str, message: str):
        super().__init__(f"{rule}: {message}")


def nonempty_string(value) -> bool:
    return isinstance(value, str) and value != ""


def string_array(core: dict, key: str, rule: str) -> list:
    value = core[key]
    if not isinstance(value, list) or not value:
        raise NonConformant(rule, f"{key} is not a non-empty array")
    for entry in value:
        if not nonempty_string(entry):
            raise NonConformant(rule, f"{key} holds {entry!r}, not a non-empty string")
    return value


def check(core: dict) -> None:
    if core.get("profile") != PROFILE:
        raise NonConformant("FRAMEWORK 3", f"profile is {core.get('profile')!r}")
    if core.get("kind") != "resource":
        raise NonConformant("FRAMEWORK 5", f"kind {core.get('kind')!r} is not defined by Core 1.0")
    for key in ATTRIBUTION:
        if key not in core:
            continue
        parties = core[key]
        if not isinstance(parties, list) or not parties or not all(isinstance(p, dict) for p in parties):
            raise NonConformant("5.1", f"{key} is not a non-empty array of tables")
        for party in parties:
            if not nonempty_string(party.get("name")):
                raise NonConformant("5.1", f"a {key} table has no name")
            for extra in ATTRIBUTION_KEYS:
                if extra in party and not isinstance(party[extra], str):
                    raise NonConformant("5.1", f"{key} {extra} is not a string")
    for key in REPEATABLE:
        if key in core:
            string_array(core, key, "5.2")
    for key in SINGLE:
        if key in core and not nonempty_string(core[key]):
            raise NonConformant("5.3", f"{key} is not a non-empty string")
    for key in DATES:
        if key in core and type(core[key]) is not datetime.date:
            raise NonConformant("5.4", f"{key} is not a local date")
    if "type" in core and not (isinstance(core["type"], str) and core["type"] in TYPES):
        raise NonConformant("5.5", f"type {core['type']!r} is not a DCMI Type term")
    if "format" in core and not (isinstance(core["format"], str) and MEDIA_TYPE.fullmatch(core["format"])):
        raise NonConformant("5.6", f"format {core['format']!r} is not a media type")
    if "language" in core:
        for tag in string_array(core, "language", "5.7"):
            if not BCP47.fullmatch(tag):
                raise NonConformant("5.7", f"language {tag!r} is not a well-formed BCP 47 tag")
    if "license" in core:
        for uri in string_array(core, "license", "5.8"):
            if not URI.fullmatch(uri):
                raise NonConformant("5.8", f"license {uri!r} is not an absolute URI")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check-core.py <case-directory>", file=sys.stderr)
        return 2
    flyleaf = pathlib.Path(sys.argv[1]) / "slipcase.flyleaf.toml"
    try:
        doc = tomllib.loads(flyleaf.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as error:
        print(f"check-core.py: {error}", file=sys.stderr)
        return 2
    core = doc.get("core")
    if not isinstance(core, dict):
        print("non-conformant FRAMEWORK 3: no [core] table")
        return 1
    if core.get("profile_version") != "1.0":
        print(f"out of scope: profile_version {core.get('profile_version')!r}", file=sys.stderr)
        return 2
    try:
        check(core)
    except NonConformant as finding:
        print(f"non-conformant {finding}")
        return 1
    print("conformant")
    return 0


if __name__ == "__main__":
    sys.exit(main())
