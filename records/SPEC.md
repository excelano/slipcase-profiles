# Slipcase Records Profile — Specification

**Version:** 1.0  
**Status:** draft  
**Framework:** 1.0 · **Conventions:** 1.0 · **Slipcase:** 1.1

The Records Profile makes a Slipcase container a managed record: a thing with an identity, a custodian, a retention schedule, holds that can stop its destruction, a history that cannot be edited without the edit showing, and, at the end, a place in a register that says it was destroyed and how. It also defines the containers a records-management system keeps beside its records: hold matters, aggregations, and disposal batches.

Everything a record says about itself is in its own container. There is no index that the files depend on; any index is a cache rebuilt from the files.

## 1. Identity and terminology

The key words **MUST**, **MUST NOT**, and **MAY** are to be interpreted as described in BCP 14 when, and only when, they appear in capitals. **FRAMEWORK**, **CONVENTIONS**, and **SPEC** cite the profiles framework, the shared conventions, and the Slipcase specification.

| | |
|---|---|
| Name | Slipcase Records Profile |
| `profile` | `https://slipcaseformat.org/profiles/records` |
| Profile table | `[records]` |
| Profile prefix | `records/` |
| Kinds | `record`, `hold`, `aggregation`, `disposal-batch` |
| Conventions used | identifiers, agents, hashes, dates and instants, chained logs |

**Record** — a container of kind `record`.  
**Records root** — the directory holding a records-management system's central state: its schedule, register, hold matters, and aggregations (§7).  
**Series** — a line of a retention schedule, identified by the organization's code for it, that governs how long a record is kept.  
**Unclassified** — a container carrying no `[records]` table, or one whose `kind` is not `record`, considered as a candidate record. An unclassified container is not a record and nothing in this profile acts on it.

A container that Slipcase calls undetermined is never passed over silently where records are expected: an undetermined container can hide a record (§9).

## 2. Records

A record is a container whose `[records]` table has `kind = "record"`. Its content file is the record's primary document. Its parts, where it has several, are components (§2.7). Its history is the event log (§2.8).

### 2.1 Example

```toml
slipcase_version = "1.1"

[content]
file = "invoice-2024-0117.pdf"

[records]
profile = "https://slipcaseformat.org/profiles/records"
profile_version = "1.0"
kind = "record"
id = "01927c3e-8b2a-7d41-9f3c-2a6e5b1c4d7f"
created = 2024-01-17
captured = 2024-02-03T15:04:11Z
mime_type = "application/pdf"
size = 48213
essential = false
marking = "Confidential"
events_head = "9140413d6cd39affadb3669cb7b09cf05ca2a4cd12f3129049e7736d694f5d8a"

[records.creator]
email = "jdoe@example.com"
id = "8f1c2b9e-1d4a-4e5f-9a0b-6c7d8e9f0a1b"

[records.custodian]
email = "jdoe@example.com"
id = "8f1c2b9e-1d4a-4e5f-9a0b-6c7d8e9f0a1b"

[records.fixity]
content_sha256 = "51ab0e6a6f3f1b0a9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b"

[[records.series]]
code = "FIN-200"
trigger = 2024-01-17
[records.series.snapshot]
title = "Accounts Payable"
retention = "6"
retention_type = "Event_age"
event_type = "Final action"
disposition = "Temporary"
schedule_version = "20261005T140211Z-3fa9c2e1b7d0"

[[records.holds]]
matter = "01927d01-4c2e-7a3b-8d5f-1e2a3b4c5d6e"
type = "legal"
applied = 2026-03-12

[[records.relations]]
type = "member-of"
target = "01927a55-2b1c-7e4d-9f6a-3c4d5e6f7a8b"
title = "Vendor contract C-4471"
```

### 2.2 Keys

A record's `[records]` table MUST contain the three framework keys (FRAMEWORK §3) and the following. Types are TOML types; **identifier**, **agent**, **hash**, **date**, and **instant** are CONVENTIONS §1 to §4.

| Key | Type | |
|---|---|---|
| `id` | identifier | The record's identity. Assigned at capture and never changed, including when the container is copied: a copy is the same record. A new record made from an existing one gets a new `id` and a `related` relation to the original (§2.6). |
| `created` | date | The date of the content: when the document came into being, not when it became a record. |
| `captured` | instant | When the container became a record. |
| `mime_type` | string | The content file's media type, determined at capture. |
| `size` | integer | The content file's length in bytes, determined at capture. |
| `essential` | boolean | Whether the record is one the organization has designated essential (vital) for continuity. Informational in this version. |
| `events_head` | hash | The head of the event log (§2.8). |
| `creator` | agent | Who created the content. Fixed at capture. |
| `custodian` | agent | Who is responsible for the record now. Changes over time, and is what holds are matched against. |
| `fixity` | table | §2.3. |
| `series` | array of tables | §2.4. MAY be empty: a record with no series is captured and unclassified as to retention. |

And MAY contain:

| Key | Type | |
|---|---|---|
| `marking` | string | A security or handling marking, as the organization writes it. Informational: it never controls access and never changes what this profile does with the record. |
| `holds` | array of tables | §2.5. Absent and empty mean the same: no holds. |
| `relations` | array of tables | §2.6. |
| `components` | array of tables | §2.7. |

Keys this section does not define are permitted in the table and MUST be preserved (FRAMEWORK §3). A later version of this profile may define `pronom` for a format identifier; an implementation of this version MUST NOT interpret it.

### 2.3 Fixity

```toml
[records.fixity]
content_sha256 = "51ab..."
```

`content_sha256` is a hash (CONVENTIONS §3) of the content file, taken at capture and whenever the content file is replaced (§2.9). An implementation verifying fixity compares it with the content file's bytes as read; a difference means the content has changed since it was last written under this profile, and §9 says what an implementation does about that.

### 2.4 Series

Each entry of `series` names one line of the organization's retention schedule that governs the record:

```toml
[[records.series]]
code = "FIN-200"
trigger = 2024-01-17
[records.series.snapshot]
title = "Accounts Payable"
retention = "6"
retention_type = "Event_age"
event_type = "Final action"
disposition = "Temporary"
schedule_version = "20261005T140211Z-3fa9c2e1b7d0"
```

- **`code`** — string, non-empty. The organization's code for the series, as it appears in the schedule (§3). Never a vendor's identifier. Two entries MUST NOT carry the same `code`.
- **`trigger`** — date, optional. The date retention is measured from. Absent while the record is awaiting the event that starts its retention; present once that event has been recorded (§2.8, `event_applied`).
- **`snapshot`** — table, optional. What the schedule said about the series when the entry was written, for a reader with no schedule to hand. Every key in it is a string, and every key is optional. It is informational: no decision under this profile is taken from a snapshot, and a snapshot that differs from the schedule is reported, never acted on (§8). It is refreshed only by an explicit, logged action.

Most records have one series. A record MAY have several, and §8 defines what that means for its retention.

### 2.5 Holds

Each entry of `holds` records that a hold matter (§4) applies to the record:

```toml
[[records.holds]]
matter = "01927d01-4c2e-7a3b-8d5f-1e2a3b4c5d6e"
type = "legal"
applied = 2026-03-12
```

- **`matter`** — identifier. The hold matter's `id`. Two entries MUST NOT carry the same `matter`.
- **`type`** — string, `legal` or `extension`. Copied from the matter when applied.
- **`applied`** — date. When the hold was applied to this record.

A record under any hold MUST NOT be destroyed, and MUST NOT have its content file replaced or a component removed (§2.9). An entry is removed when its matter is released, leaving other entries intact.

### 2.6 Relations

Each entry of `relations` links the record to another record or to an aggregation (§5):

```toml
[[records.relations]]
type = "member-of"
target = "01927a55-2b1c-7e4d-9f6a-3c4d5e6f7a8b"
title = "Vendor contract C-4471"
```

- **`type`** — string, one of the following. Any other value is non-conformant.
- **`target`** — identifier. The `id` of the other record or aggregation.
- **`title`** — string, optional. The target's title when the relation was written, for a reader who cannot reach the target.

| `type` | Meaning | Consequence under this profile |
|---|---|---|
| `member-of` | The record belongs to the aggregation `target` names | Holds and events may be applied to an aggregation's members (§4, §5) |
| `version-of` | The record is an earlier or later version of `target` | None in this version |
| `supersedes` | The record replaces `target` | None in this version |
| `related` | Any other connection | None |

Relations link separate records. The parts of one record are components, never relations.

### 2.7 Components

A record that has several parts and no native format holding them together (a form and its supporting documents, where an email and its attachments would be one `.eml` file) keeps its primary document as the content file and each further part as a member under `records/components/`:

```toml
[[records.components]]
member = "records/components/01-invoice.pdf"
filename = "invoice.pdf"
mime_type = "application/pdf"
size = 20311
sha256 = "a9f2c1d0e8b7a6f5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1"
```

- **`member`** — string. The member's name, which MUST begin with `records/components/` and MUST satisfy FRAMEWORK §4. Two entries MUST NOT name the same member.
- **`filename`** — string, non-empty. The part's original filename, for display and for extraction.
- **`mime_type`**, **`size`**, **`sha256`** — as for the content file (§2.2, §2.3), determined when the component was added.

Every member of the container under `records/components/` MUST be named by one entry, and every entry MUST name a member the container holds. A container failing either is non-conformant.

Components are destroyed with their container, and a component is never shared between containers.

### 2.8 The event log

Every record carries its own history as a chained log (CONVENTIONS §5):

| | |
|---|---|
| Member | `records/events.toml` |
| Entry name | `event` |
| Seed | The UTF-8 bytes of the record's `id` |
| Head | `events_head` in the `[records]` table (§2.2) |

A record MUST carry the log, the log MUST be intact, and `events_head` MUST equal the hash of its last entry. The first entry MUST have `type = "captured"`.

Every change to the `[records]` table appends an entry describing it, and the two are written in one operation: a rewrite of the container that changes the table and appends the entry, so that a change and its record can never be separated. `events_head` is updated in that same operation.

Each entry carries the keys CONVENTIONS §5.1 requires and:

| Key | Type | |
|---|---|---|
| `type` | string | What happened, from the table below. |
| `actor` | agent | Who did it, or on whose authority a tool did it. |
| `tool` | string | The program that wrote the entry and its version, as `name version`. |
| `location` | table | Where the container was when the entry was written (§2.8.1). |
| `detail` | table, optional | What the type requires, below. |

| `type` | Meaning | `detail` |
|---|---|---|
| `captured` | The container became a record | — |
| `classified` | A series was added | `code` |
| `reclassified` | A series was removed or replaced | `from` (code), `to` (code or absent) |
| `renumbered` | A series code changed under a renumbering of the schedule | `from`, `to` |
| `custodian_changed` | `custodian` changed | `from` (agent), `to` (agent) |
| `hold_applied` | A hold was applied | `matter` |
| `hold_released` | A hold was released | `matter` |
| `event_applied` | A series' trigger date was set | `code`, `trigger` (date) |
| `reviewed` | A review fell due and was decided (§8) | `code`, `decision`, `comment` (non-empty) |
| `relation_added` | A relation was added | `type`, `target` |
| `relation_removed` | A relation was removed | `type`, `target` |
| `component_added` | A component was added | `member`, `sha256` |
| `component_removed` | A component was removed | `member`, `sha256`, `reason` |
| `content_replaced` | The content file was replaced | `from_sha256`, `to_sha256`, `reason` |
| `marking_changed` | `marking` changed | `from`, `to` |
| `fixity_failed` | A fixity check found the content or a component changed (§9) | `member`, `expected`, `found` |
| `moved_detected` | A fixity check found the container at a different location (§2.8.1) | `from` (location table) |

A `type` not in this table is non-conformant. A successful fixity check is not an event: it is recorded in the sweep's own report (§7), so that a log does not grow with every sweep.

The log is destroyed with the record. What survives destruction is the record's row in the disposal batch that destroyed it (§6).

#### 2.8.1 Location

Every entry records where the container was when the entry was written. The same share is reached by a different path from every platform (`\\files\legal`, `Z:\`, `/Volumes/legal`, `/mnt/legal`), so a path alone does not say whether a container has moved. The location is a table of three keys:

```toml
location = { root = "legal", path = "contracts/C-4471/invoice-2024-0117.pdf.slpc", raw = '\\files\legal\contracts\C-4471\invoice-2024-0117.pdf.slpc' }
```

- **`root`** — string, optional. The name of a share root declared in the records root's settings (§7) under which the container was found. Absent when the container was under no declared root.
- **`path`** — string. The container's path relative to `root`, with `/` separators, NFC-normalized. Present when and only when `root` is.
- **`raw`** — string. The path as the operating system reported it, always present.

A root is matched against the container's canonical path: on Windows a mapped drive letter resolves to the UNC path it stands for, so a container reached as `Z:\contracts\...` is under a root declared as `\\files\legal`.

Two locations are the same when their `root` and `path` are equal, compared exactly and case-sensitively: a rename that changes only case is a move. Two locations of which either lacks `root` are not comparable, and an implementation MUST NOT record a move between them.

### 2.9 Changes after capture

The content file and the components MAY change after capture. Every change is logged in the same operation (§2.8):

- Adding a component appends `component_added`.
- Removing a component, or replacing the content file, is a partial destruction outside disposition. It MUST NOT be done while the record is under any hold (§2.5). The entry (`component_removed`, `content_replaced`) records the old hash and a reason, and `fixity`, `mime_type`, and `size` are updated in the same operation.

A record never loses its `id`, and nothing in this profile edits an earlier entry of the log.
