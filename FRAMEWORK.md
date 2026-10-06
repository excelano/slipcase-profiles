# Slipcase Profiles — Framework

**Version:** 1.0  
**Status:** draft  
**Slipcase version:** 1.1

A profile defines how Slipcase containers are used for one purpose. It gives meaning to keys in the flyleaf and to additional members, and it changes nothing in Slipcase itself. This document states what every profile has in common, so that a profile specification need only state what is particular to it, and so that a flyleaf can carry several profiles without any of them knowing about the others.

## 1. Terminology

The key words **MUST**, **MUST NOT**, and **MAY** are to be interpreted as described in BCP 14 ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) when, and only when, they appear in capitals.

**Slipcase** — the container specification at <https://github.com/excelano/slipcase>, cited as SPEC §n.  
**Profile** — a specification, written against this framework, giving meaning to a container for one purpose.  
**Profile table** — the one top-level table in the flyleaf that a profile owns (§3).  
**Profile prefix** — the one directory under which a profile's additional members live (§4).  
**Kind** — what a container is within a profile, named by the `kind` key (§5).  
**Implementation of a profile** — a program that reads or writes containers according to that profile.

A container is conformant to a profile, or not, in the same way that it is conformant to Slipcase or not: the profile's specification states properties that can be checked against the file. This framework states the properties every profile shares.

## 2. Relationship to Slipcase

A container conforming to a profile MUST be a conformant Slipcase container. A profile MUST NOT redefine, constrain, or assign meaning to any key or member that Slipcase defines, and MUST NOT state a rule under which a Slipcase-conformant container would need to change to remain Slipcase-conformant.

Slipcase requires an implementation to preserve keys and members it does not recognize (SPEC §3). That requirement is what carries a profile's data through tools that know nothing of the profile, and a profile relies on it rather than restating it.

A container that Slipcase calls undetermined (SPEC §2.2) is undetermined for every profile: no profile can be read from it and none can be said to apply.

## 3. The profile table

A profile owns exactly one top-level table in the flyleaf, and everything the profile defines in the flyleaf lives inside that table. The table's name is the profile's use-case word (§9), in lowercase ASCII letters.

The table MUST contain these three keys:

```toml
[records]
profile = "https://slipcaseformat.org/profiles/records"
profile_version = "1.0"
kind = "record"
```

- **`profile`** — string. A URI that identifies the profile and resolves to its specification. It is the profile's identity: it is the same for every version of the profile, and two tables carrying different `profile` values belong to different profiles whatever their table names.
- **`profile_version`** — string. The version of the profile's specification that the table conforms to. §6.
- **`kind`** — string. What this container is within the profile. §5.

A table carrying a `profile` key is a profile table. An implementation MUST identify a profile by the `profile` value and MUST NOT take a table's name as evidence of which profile it is. A profile's specification fixes its table name (§9), so a table whose name is not the one its `profile` value's specification fixes is non-conformant to that profile.

A flyleaf MAY carry any number of profile tables, each for a different profile. They are independent: a profile's specification governs its own table and nothing in any other, and an implementation of one profile MUST NOT read, change, or depend on another profile's table. A container is conformant to each profile it carries separately.

Keys inside a profile table that the profile's specification does not define are permitted and MUST be preserved, unless that specification says otherwise for a particular table or key. A profile MAY close a table or a value to a defined set; where it does, a value outside the set is non-conformant to the profile, never silently accepted.

## 4. The profile prefix

A profile's additional members live under a directory named for its table, with a trailing `/`: the Records Profile's members are `records/...`. A profile MUST NOT define a member outside its prefix, and an implementation of a profile MUST NOT write a member outside that profile's prefix except as a Slipcase implementation writing the flyleaf or the content file.

A member name under a prefix MUST satisfy SPEC §3's rule for members an implementation writes: segments separated by `/`, each non-empty and neither `.` nor `..`, and no `\`, `:`, or character in U+0000 to U+001F or U+007F.

Slipcase permits additional members of any name (SPEC §2.1). Members under a prefix that no profile table in the flyleaf claims have no meaning under any profile, and an implementation MUST preserve them.

## 5. Kinds

`kind` names what the container is within the profile, so that one profile can describe several kinds of container: a record and the batch that destroyed it, a document and the manifest that delivered it. A profile's specification defines its kinds, and for each kind the keys and members the container MUST and MAY carry.

The set of kinds is closed for each version of a profile. A `kind` value that the named `profile_version` does not define is non-conformant to that version.

## 6. Versioning

`profile_version` names the version of the profile's specification, and it follows the rules SPEC §2.4 sets for `slipcase_version`, restated here because they govern profiles independently of Slipcase's own version:

- Conformance is relative to a version. A profile's specification states whether a table declaring that version conforms to it, and states nothing about a table declaring any other value.
- A table declaring a version an implementation does not implement is outside that implementation's conformance question rather than failing it. The implementation MAY read and report the table, and MUST NOT act on it: it MUST NOT change the table or the profile's members, and MUST NOT take any decision the profile defines (such as whether a record may be destroyed) from it.
- The value implies no compatibility, at any level. An implementation written against one version cannot assume it can read a table declaring a higher one.
- Editorial revisions to a profile's specification do not change its version. It changes only when what counts as a conformant container under the profile changes.

A profile is versioned independently of this framework and of every other profile. A profile's specification names the version of this framework and the version of Slipcase it is written against.

## 7. Independence

Under this version of the framework, no profile may require another. A profile's specification MUST be implementable from a container that carries only that profile, and MUST NOT reference another profile's table, prefix, or kinds.

A later version of this framework may let a profile declare that it requires another. Nothing in a profile written against this version should be read as that declaration.

## 8. Shared conventions

Identifiers, agents, hashes, dates and instants, and chained logs are defined once, in `CONVENTIONS.md`, and are versioned with this framework. A profile MUST state which conventions it uses and MUST NOT define its own form for anything a convention defines. A profile MAY leave a convention unused.

## 9. Official profiles

An official profile is one specified in this repository. Its name is **Slipcase _Use_ Profile**, where _Use_ is one word naming the purpose, and that word is the same everywhere the profile is referred to:

| | Slipcase Records Profile |
|---|---|
| `profile` URI | `https://slipcaseformat.org/profiles/records` |
| Profile table | `[records]` |
| Profile prefix | `records/` |
| Directory in this repository | `records/` |

The table name and the prefix are the last segment of the URI. A profile's specification states all four and they MUST agree.

Each official profile lives in its own directory, holding its specification, a design document recording the reasoning behind its rules, and example files, and is versioned on its own. Everything in this repository is dedicated to the public domain under CC0 1.0.

A profile specified elsewhere is not made less valid by that: a `profile` URI under any origin identifies a profile, and this framework governs it the same way. Only the name form in this section and the directory in this repository are reserved for official profiles.

## 10. What a profile specification states

A profile's specification MUST state:

1. its name, `profile` URI, table name, prefix, and version, and the versions of this framework and of Slipcase it is written against;
2. its kinds, and for each kind the keys the table MUST and MAY contain, with each key's type, and the members the container MUST and MAY carry under the prefix;
3. which shared conventions it uses, and for any chained log it defines, the entry name and the seed (CONVENTIONS §5);
4. the properties a container must have to conform to the profile, stated so that each can be checked against the file;
5. the requirements it places on an implementation beyond those of this framework;
6. its security considerations.

## 11. Implementation requirements

An implementation of a profile:

- MUST identify the profile by the `profile` value and MUST check `profile_version` before acting (§3, §6);
- MUST read and write only its own profile's table and prefix, and MUST preserve every other key and member, as SPEC §3 requires;
- MUST NOT act on a table declaring a `profile_version` it does not implement, and MUST NOT report such a table as conformant or non-conformant to the version it does implement;
- MUST report, rather than pass over, a container whose profile table is non-conformant, where the implementation is acting over a set of containers in which that profile is expected;
- MUST treat an undetermined container as Slipcase requires, and MUST NOT act on it under the profile;
- MUST apply SPEC §3's display rule to any member name or string value it displays: the Unicode bidirectional formatting characters are rendered escaped, never applied.

## 12. Security considerations

A profile gives a container meaning, and with meaning comes the possibility of a container that lies. A profile that drives an action (destroying a record, accepting a delivery) MUST state what an implementation checks before acting and MUST NOT let a value in the flyleaf alone authorize an action the profile calls irreversible.

The profile table is data under the control of whoever wrote the container. A profile's specification MUST NOT define a key whose value is interpreted as a path outside the container, a command, or an address to be fetched without the implementation's own decision to do so.

Slipcase's security considerations (SPEC §6) apply to every container a profile is read from: an implementation bounds what it spends reading the flyleaf before it knows what the container is.

## Appendix A. A second profile, described against this framework (non-normative)

This appendix exists to show that the framework is general: a profile unrelated to records management is stated against it without a change to any section above. The profile is hypothetical.

**Slipcase Handover Profile**, for delivering a set of engineering documents from a contractor to an owner. URI `https://slipcaseformat.org/profiles/handover`, table `[handover]`, prefix `handover/`, written against Framework 1.0 and Slipcase 1.1.

Kinds: `document` (one delivered document; the content file is the document) and `manifest` (the delivery itself; the content file is the transmittal, and `handover/manifest.csv` lists every document delivered with its identifier and content hash).

A `document` table carries `id` (an identifier, CONVENTIONS §1), `delivery` (the identifier of the manifest it was delivered under), `document_number` and `revision` (strings, the owner's numbering), `fixity.content_sha256` (CONVENTIONS §3), and `issued` (a date, CONVENTIONS §4). A `manifest` table carries `id`, `from` and `to` (agents, CONVENTIONS §2), `delivered` (an instant), and `document_count`. Both kinds carry a chained log at `handover/events.toml` with entry name `event`, seeded from the table's `id`, recording `delivered`, `accepted`, and `rejected` events.

A document that is also a managed record carries both `[handover]` and `[records]`, each with its own prefix and its own log, and a records tool and a handover tool each read their own table and preserve the other's. Neither profile names the other, as §7 requires.

The specification would go on to state the conformance properties (every document named in a manifest's CSV exists with the hash stated; `revision` is non-empty), the implementation requirements (an acceptance is recorded only after the hash is verified), and the security considerations (a manifest's CSV names files by identifier, never by path).
