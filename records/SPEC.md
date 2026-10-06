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
retention_type = "Event_Age"
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
retention_type = "Event_Age"
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

## 3. Retention schedules

A schedule says, for each series, how long records under it are kept and what happens then. The records manager maintains it elsewhere; this profile defines the form in which it is stored in the records root and read by every implementation.

### 3.1 Form

A schedule is a CSV file in the layout NARA publishes the General Records Schedules in ("machine-implementable format"; <https://www.archives.gov/records-mgmt/grs/machine-implementable-grs>). NARA's own file MUST load under this section with no mapping and no error; `examples/schedule/grs-transmittal36.csv` is that file as published and is the test.

- UTF-8, with or without a byte order mark. Lines end with LF or CRLF. Fields are quoted and escaped as RFC 4180 describes, and a quoted field MAY contain line breaks.
- The first row names the columns. Column order is free. A column whose name is empty is ignored, as are the cells under it. A column this section does not name is ignored and MUST be preserved by any implementation that rewrites the file.
- Column names and the values of controlled columns are compared after trimming leading and trailing whitespace and without regard to ASCII case. Values are stored as written.
- A row whose cells are all empty is ignored.

### 3.2 Columns

These columns MUST be present:

| Column | |
|---|---|
| `GRS ID` | The series code: the organization's own code (`FIN-200`), or NARA's where the GRS is used as is. Non-empty. |
| `Record Title` | The series' title. |
| `Disposition` | `Temporary` or `Permanent`. |
| `Retention (Years)`, or `Retention` | The retention period (§3.3). NARA's FAQ names this column `Retention` and its file names it `Retention (Years)`; either name is this column, and a file MUST NOT carry both. |
| `Retention Type` | `Creation_Age` (measured from the record's `created`) or `Event_Age` (measured from an event). |
| `Event Type (General)` | For `Event_Age`, the event retention is measured from (§3.3). |
| `Longer Retention Authorized?` | `Yes`: the period is a minimum. `No`: the period is fixed. |

These NARA columns MAY be present and are informational, except as noted:

| Column | |
|---|---|
| `Classification (General)` | A grouping, for display. |
| `Legal Citation` | The citation the period rests on. |
| `Deviations Allowed?` | `Yes` or `No`. |
| `Disposition Authority` | The authority reference. |
| `Superseded by` | Non-empty when the row is retired in favour of the series it names (§3.3). |
| `Last Updated` | When NARA last changed the row. |
| `Comments` | Free text. |

### 3.3 Values, and what a row means

In a controlled NARA column, the values `N/A`, `NA`, `[Variable]`, and an empty cell all mean **not stated**. The column's vocabulary is NARA's: a value outside it is not an error in the file, and it is not stated either. (Extension columns, §3.4, are this profile's, and their vocabularies are closed.)

**The period** is the `Retention (Years)` value, read as:

| Form | Meaning |
|---|---|
| An unsigned integer, `0` included | That many years. `0` means the record is eligible as soon as its trigger, after any cutoff, has passed. |
| An unsigned integer followed by `m` | That many months. |
| An unsigned integer followed by `d` | That many days. |
| Anything else | Not stated. NARA's file carries ranges (`4-7`), hours (`72h`), and `[Variable]`; this profile computes no period from them. |

**The event** is the `Event Type (General)` value. Four values are general events with meaning under this profile; any other stated value is a named event, which an organization records when it happens (§2.8, `event_applied`), and which this profile treats like `Final action`:

| Value | The trigger is |
|---|---|
| `End of FY` | The record's `created`, with the fiscal-year cutoff applied (§8.2). Stated for a `Creation_Age` row, it adds the cutoff; stated for an `Event_Age` row, it is the event. |
| `Final action` | The date the matter the record belongs to was closed, as recorded by `event_applied`. |
| `No longer needed` | The date the organization decided it no longer needed the record, as recorded by `event_applied`. |
| `Superseded or obsolete` | The date the record was superseded or became obsolete, as recorded by `event_applied`. |

A row is **permanent** when `Disposition` is `Permanent`, whatever else it says. Records under a permanent series are never destroyed under this profile (§8).

A row is **retired** when `Superseded by` is non-empty. A retired row stays in the schedule so that records already under it can be read; an implementation MUST NOT classify a record under a retired series, and evaluation of a record already under one reports the successor (§8).

A row that is neither permanent nor retired is **computable** when its `Disposition` is `Temporary`, its `Retention Type` is stated, its period is stated, and, for `Event_Age`, its event is stated. Otherwise it is **descriptive**: it loads, it can be looked up and displayed, and a record under it cannot be evaluated (§8). NARA's file has rows of every kind, and loads.

### 3.4 Extension columns

What NARA's layout lacks goes in columns whose names begin with `x_`. A file using none is a NARA-layout file; a file using them is still one, since the extra columns are ignored by anything that does not know them. Extension columns are never folded into NARA's columns, and an extension's vocabulary is closed: a value outside it is an error, and the file MUST be refused.

| Column | Values | Meaning |
|---|---|---|
| `x_disposal_action` | `destroy`, `transfer`, `review`, `retain` | What happens when the period elapses. Absent: `destroy` for `Temporary`, `retain` for `Permanent`. `review` is MoReq2010's review: a person decides (§8.4). `transfer` is reserved: records under it are treated as `retain` in this version. |
| `x_cutoff` | `none`, `calendar_year`, `fiscal_year`, `quarter`, `month` | Retention starts at the end of the cutoff period containing the trigger (§8.2). Absent: `fiscal_year` where the event is `End of FY`, otherwise `none`. |
| `x_period_kind` | `minimum`, `maximum`, `fixed` | Absent: `minimum` where `Longer Retention Authorized?` is `Yes`, `fixed` where it is `No`, and `minimum` where it is not stated. A `maximum` is a deadline (§8.3). |
| `x_maximum` | A period, as §3.3 reads one | A series that has both a minimum and a maximum states the minimum in the period column and the maximum here, on the one row. Where present, `x_period_kind` MUST be absent or `minimum`. |
| `x_citation_defining` | `yes`, `no` | Whether `Legal Citation` sets the period or only supports it. Informational. |
| `x_jurisdiction` | Free text | For a schedule that carries a baseline and per-jurisdiction variants: one row per variant, same code, different jurisdiction. |

### 3.5 Uniqueness

Within a file, no two rows MAY carry the same `GRS ID` and the same `x_jurisdiction` (empty counting as a value). A file that does is malformed and MUST be refused, as is a file missing a required column or carrying a row with an empty `GRS ID`. Refusal reports every problem with the row it is in.

### 3.6 The store

Schedules live in the records root (§7) as versions that are never edited:

```
schedule/
  current                                   # one line: the current version's identifier
  versions/
    20261005T140211Z-3fa9c2e1b7d0.csv       # the schedule
    20261005T140211Z-3fa9c2e1b7d0.toml      # about that version
```

- A **version identifier** is the UTC instant the version was written, as `YYYYMMDDThhmmssZ`, a hyphen, and the first twelve hexadecimal digits of the CSV's hash.
- The `.toml` beside a version records `imported` (instant), `imported_by` (agent), `source` (string: where the schedule came from, as a person would say it), `tool` (string, as §2.8), and `sha256` (hash of the CSV).
- A version is never changed. A change to the schedule is a new version.
- `current` holds the identifier of the version in force and nothing else, followed by LF. It is replaced by writing a new file beside it and renaming over it, so that a reader sees the old version or the new and never a partial file. A reader reads `current`, then the version it names.
- Every record's series snapshot and every disposal plan records the version identifier it was taken from or evaluated against, so that any decision traces to the exact schedule in force.

## 4. Hold matters

A hold stops destruction. A **hold matter** is one legal matter or business reason under which records are held, defined once, centrally, as a container of kind `hold` in the records root's `holds/` directory, named `<id>.slpc`. The matter's container describes the hold; it does not hold the records, which stay where they are and carry an entry naming the matter (§2.5).

### 4.1 Keys

```toml
[records]
profile = "https://slipcaseformat.org/profiles/records"
profile_version = "1.0"
kind = "hold"
id = "01927d01-4c2e-7a3b-8d5f-1e2a3b4c5d6e"
title = "Vendor dispute, Acme Corp."
type = "legal"
mandate = "Litigation hold, counsel's instruction of 2026-03-11"
placed = 2026-03-12
status = "active"
scope = 'custodian.email in ("jdoe@example.com", "asmith@example.com") and created >= 2023-01-01'
events_head = "..."

[records.approved_by]
email = "counsel@example.com"
id = "7a6b5c4d-3e2f-4a1b-9c8d-7e6f5a4b3c2d"
```

| Key | Type | |
|---|---|---|
| `id` | identifier | The matter. |
| `title` | string, non-empty | |
| `type` | string | `legal`: a hold on counsel's instruction. `extension`: a business reason to keep records past their period. |
| `mandate` | string, non-empty | The authority or reason, as a person would state it. |
| `approved_by` | agent | Who authorized the hold. |
| `placed` | date | When the hold was placed. |
| `end_date` | date, optional | For an `extension`, when it releases itself (§4.3). |
| `scope` | string | A SlipQL `where` expression (<https://github.com/excelano/slipql>) over a record's flyleaf. The hold applies to every record it is true for. |
| `status` | string | `active` or `released`. |
| `released` | date | Present when and only when `status` is `released`. |
| `events_head` | hash | §4.2. |

The content file is the hold notice or order, in any format, or an empty content file where there is none.

### 4.2 History

A matter carries a chained log at `records/events.toml`, entry name `event`, seeded from its `id`, head in `events_head`, with the entry keys of §2.8 other than `location`, and these types:

| `type` | `detail` |
|---|---|
| `placed` | — (the first entry) |
| `scope_changed` | `from`, `to` (the expressions) |
| `released` | `reason` |

The log answers who placed, changed, and released the matter, and when.

### 4.3 Applying, matching, releasing

- **Applying** a matter to a record adds a `holds` entry to the record (§2.5) and appends `hold_applied` to the record's log. An implementation applying a matter MUST evaluate its scope and show the count of records matched before applying, and MUST report a scope that matches no record rather than applying it silently.
- **Matching at classification.** Every active matter's scope MUST be evaluated against a record when the record is captured or its `[records]` table changes, so that a record that comes to match a hold placed earlier is held.
- **Matching at destruction.** A record's `holds` list is what it says; an active matter whose scope matches a record that carries no entry for it is a gap, and §8.5 makes such a record not eligible. An implementation finding one MUST report it as `hold_scope_unapplied`.
- **Releasing** sets `status` and `released`, appends `released` to the matter's log, and removes the matter's entry from each record that carries it, appending `hold_released` to each. Other matters' entries are untouched.
- An `extension` with an `end_date` is released by the implementation when the evaluation date passes it, logged like any release.
- A matter is never deleted. A released matter stays in `holds/` with its history.

## 5. Aggregations

An **aggregation** is a case file, a project file, or any other grouping of records that are managed together. It is a container of kind `aggregation` in the records root's `aggregations/` directory, named `<id>.slpc`. Like a hold matter, it does not hold its members: a record belongs to an aggregation by carrying a `member-of` relation to it (§2.6), and the members are found by a query.

### 5.1 Keys

```toml
[records]
profile = "https://slipcaseformat.org/profiles/records"
profile_version = "1.0"
kind = "aggregation"
id = "01927a55-2b1c-7e4d-9f6a-3c4d5e6f7a8b"
title = "Vendor contract C-4471"
status = "open"
default_series = "LEG-010"
events_head = "..."

[[records.relations]]
type = "member-of"
target = "01927a00-1111-7222-8333-444455556666"
title = "Vendor contracts 2024"
```

| Key | Type | |
|---|---|---|
| `id` | identifier | The aggregation. |
| `title` | string, non-empty | |
| `description` | string, optional | |
| `default_series` | string, optional | A series code. A record joining the aggregation is classified under it (§5.3). |
| `status` | string | `open` or `closed`. |
| `closed` | date | Present when and only when `status` is `closed`. |
| `relations` | array of tables, optional | §2.6. A `member-of` relation makes this aggregation a member of another. |
| `events_head` | hash | §5.2. |

The content file is a cover sheet or an index where one exists, and an empty content file otherwise.

### 5.2 History

A chained log at `records/events.toml`, entry name `event`, seeded from `id`, head in `events_head`, with the entry keys of §2.8 other than `location`, and these types:

| `type` | `detail` |
|---|---|
| `created` | — (the first entry) |
| `closed` | — |
| `reopened` | `reason` |
| `default_series_changed` | `from`, `to` |
| `relation_added`, `relation_removed` | as §2.8 |

### 5.3 Membership, inheritance, closing

- A record joins by having a `member-of` relation added (§2.6, `relation_added`). Where the aggregation has a `default_series` and the record has no entry for that code, a series entry for it is written to the record in the same operation (`classified`). Inheritance is a copy at joining, never a lookup at evaluation: a record's series are its own.
- Changing `default_series` changes nothing on existing members by itself. An implementation that offers to reclassify them does so as a previewed rewrite of each member, logged on each.
- **Closing** sets `status` and `closed`, appends `closed` to the aggregation's log, and, for every member record, sets the `trigger` of each `Event_Age` series whose event is `Final action` and whose `trigger` is absent to the closing date, appending `event_applied` to each. A member under some other event is not triggered by closing.
- A hold applied to an aggregation is a hold whose scope matches `member-of` that aggregation; the matter is applied to the members as §4.3 says, and the aggregation's own container is not held.

## 6. The disposition register

The register is the record of destruction: one entry per **batch**, where a batch is one run that destroyed records under one plan. After a record is destroyed, its row in a batch's manifest is the only evidence it existed. The register lives in the records root's `register/` directory, and its batches form a hash chain.

### 6.1 Files

Each batch occupies three files, named by its **sequence**, a six-digit zero-padded decimal starting at `000001`. The journal appears with the batch's first outcome, so an intent with no journal is a run that has not yet touched a record:

```
register/
  000123.intent.slpc     # the claim and the plan; written once
  000123.journal         # one entry per record outcome, appended during the run
  000123.slpc            # the final; written once
  000124.intent.slpc     # unfinished: no final
```

Batch N is **final** when `N.slpc` exists, and **unfinished** when `N.intent.slpc` exists without it. No file in the register is ever rewritten or removed: both containers are created with create-new semantics, and the journal is only appended to. A register therefore only gains files.

### 6.2 The intent

The intent is a container of kind `disposal-batch`, written before any record is destroyed. Creating it is how a run claims its sequence: a run MUST create `N.intent.slpc` exclusively, and MUST NOT proceed if the create fails. A run MUST NOT claim sequence N unless batch N−1 is final (§6.5).

```toml
slipcase_version = "1.1"

[content]
file = "intent-000124.txt"

[records]
profile = "https://slipcaseformat.org/profiles/records"
profile_version = "1.0"
kind = "disposal-batch"

[records.disposition]
sequence = 124
state = "intent"
started = 2026-10-05T13:58:40Z
host = "fs-ops-02"
user = "svc-fileroom"
records_planned = 4210
plan_id = "01929e10-2a3b-7c4d-8e5f-6a7b8c9d0e1f"
evaluated = 2026-10-01
schedule_version = "20261005T140211Z-3fa9c2e1b7d0"
approved_by = ["rm@example.com"]
scope_statement = "Removed from repository. Backup copies expire under the backup retention policy."

[records.chain]
manifest_sha256 = "e07d..."
```

| Key | Type | |
|---|---|---|
| `sequence` | integer | The batch's sequence. |
| `state` | string | `intent`. |
| `started` | instant | When the run began. |
| `host`, `user` | string | Where and as whom the run is executing, so that an unfinished intent can be traced. |
| `records_planned` | integer | Rows in the manifest. |
| `plan_id` | identifier | The plan this batch executes. |
| `evaluated` | date | The evaluation date the plan was made at (§8). |
| `schedule_version` | string | The schedule version the plan was evaluated against (§3.6). |
| `approved_by` | array of strings | Who approved the plan, as the caller states it. This profile does not authenticate anyone; the certificate says so. |
| `scope_statement` | string | What destruction means here. The default is above; an organization MAY state its own. |
| `chain.manifest_sha256` | hash | The planned manifest, §6.3. |

The content file is a plain-text statement that the batch is in progress, naming the sequence and the start. The manifest member (§6.3) lists every planned record with its `outcome` empty.

### 6.3 The manifest

`records/manifest.csv`, in the form of §3.1, one row per record in the batch:

| Column | |
|---|---|
| `id` | The record's identifier. |
| `title` | The content file's name, or the record's title where the organization keeps one. |
| `path` | The container's location when planned, as `root:path` where it had a root, else the raw path. |
| `series` | The series codes, separated by `;`. |
| `custodian_email` | |
| `created` | |
| `content_sha256` | The content file's hash as planned. |
| `flyleaf_sha256` | The flyleaf member's hash as planned (§6.4). |
| `outcome` | Empty in the intent. In the final: `destroyed`, `skipped`, `failed`, or `unknown`. |
| `reason` | For `skipped` and `failed`: why, as §6.4 and §6.6 state. |

### 6.4 The run

For each record, in manifest order, the run:

1. reads the container and compares its flyleaf member's hash with `flyleaf_sha256`; on a difference, the record is `skipped` with reason `changed_since_plan`, and nothing else is checked;
2. evaluates eligibility as of `evaluated` against `schedule_version`, with the hold matters active now (§4.3); if the record is not `eligible`, it is `skipped` with the reasons;
3. deletes the container, and confirms it is gone; where deletion fails or the file remains, the record is `failed` with the operating system's error;
4. appends the outcome to the journal before touching the next record.

Deletion is an ordinary filesystem delete. Nothing is overwritten, and nothing written under this profile claims secure erasure or media sanitization: the scope statement describes removal from the repository.

### 6.5 The journal

`N.journal` is a chained log (CONVENTIONS §5) beside the containers, entry name `outcome`, seeded from the UTF-8 bytes of the intent flyleaf's hash (the `intent_flyleaf_sha256` the final will carry). Each entry carries `seq`, `at`, `prev`, and:

| Key | |
|---|---|
| `record` | The record's identifier. |
| `outcome` | `destroyed`, `skipped`, or `failed`. |
| `reason` | For `skipped` and `failed`. |
| `error` | For `failed`: the operating system's error text. |

The journal is protected by the final's `journal_sha256` (§6.6), a hash of the whole file; it is complete when the final is written and is not appended to after.

### 6.6 The final

When every record has an outcome, the run writes `N.slpc`, also by exclusive create. If the final already exists, another finalizer won and this one fails without writing.

```toml
[records.disposition]
sequence = 124
state = "final"
started = 2026-10-05T13:58:40Z
completed = 2026-10-05T14:02:11Z
host = "fs-ops-02"
user = "svc-fileroom"
records_planned = 4210
records_destroyed = 4207
plan_id = "01929e10-2a3b-7c4d-8e5f-6a7b8c9d0e1f"
evaluated = 2026-10-01
schedule_version = "20261005T140211Z-3fa9c2e1b7d0"
component = "fileroom 0.3.1"
approved_by = ["rm@example.com"]
scope_statement = "Removed from repository. Backup copies expire under the backup retention policy."

[records.chain]
intent_flyleaf_sha256 = "4f20..."
previous_flyleaf_sha256 = "9c1e..."
content_sha256 = "51ab..."
manifest_sha256 = "e07d..."
journal_sha256 = "b7c4..."
```

In addition to the intent's keys: `completed` (instant), `records_destroyed` (integer), `component` (string: the implementation that destroyed, as `name version`), and, for a batch finished by recovery (§6.7), `recovered` (instant) and `recovered_by` (agent). The manifest is the intent's with every `outcome` filled. The content file is the certificate (§6.8).

`[records.chain]`:

| Key | Hash of |
|---|---|
| `intent_flyleaf_sha256` | The intent container's flyleaf member. |
| `previous_flyleaf_sha256` | The final flyleaf of batch N−1. For batch 1, the **genesis value**: `872a5013347fc0dcd51e6fe0af140a92b1881674b002fb2f069b2cbaaa16e88a`, the hash of the UTF-8 string `https://slipcaseformat.org/profiles/records#register-genesis`. |
| `content_sha256` | The certificate. |
| `manifest_sha256` | The final manifest. |
| `journal_sha256` | The journal file. |

Every hash is over stored bytes (CONVENTIONS §3). A register's chain is **intact** when, walking from batch 1, every final's five hashes are what they should be, every sequence from 1 to the last is present, no sequence is claimed twice, and every final's intent exists and matches. Verification reports the first batch at which any of this fails, and every unfinished intent; it never repairs.

**The register records what happened, never what was planned.** A certificate never claims a destruction that did not occur, and a final is never written until every planned record has an outcome.

### 6.7 One batch at a time, and recovery

A run MAY claim sequence N only when N−1 is final: batch N's final chains to N−1's, which does not exist while N−1 is running. A run that finds N−1 unfinished, or that loses the exclusive create for N, MUST refuse and report the unfinished batch: its sequence, host, user, start, and last journal entry.

An unfinished intent is finished only by **recovery**, an explicit action that a person confirms, never by a run that happens to find it. No tool can tell a crashed run from one still executing on another machine, and finishing a live batch would record a partial manifest while destruction continued. Recovery:

1. reads the intent and the journal;
2. for each planned record, takes the journal's outcome where the journal has one; where it has none, records `unknown` if the container is gone and `skipped` with reason `not_attempted` if it is present; it never assumes a record was destroyed;
3. writes the final by exclusive create, with `recovered` and `recovered_by`, and a certificate that states the batch was recovered and when.

Recovery never destroys a record. To continue, a person makes a new plan.

### 6.8 The certificate

The final's content file is the certificate: the human-readable statement of what the batch did. It MUST state the organization, the sequence, the plan identifier, the evaluation date and schedule version, who approved (and that approval was stated to the implementation and not verified by it), when the run started and completed, the host and user, the component, the scope statement, the counts planned and destroyed, and every record's identifier, title, path, series, custodian, created date, and outcome. A recovered batch's certificate states that, and when.

The certificate SHOULD be a PDF conforming to both PDF/A (for durability) and PDF/UA (for accessibility), PDF/A-4 with PDF/UA-2 or PDF/A-2a with PDF/UA-1, and an implementation producing one SHOULD validate it. An implementation that cannot render one MAY write a plain UTF-8 text certificate whose first line states that it is a text certificate; its content is the same.

The certificate's name is `certificate-<sequence>.pdf` or `certificate-<sequence>.txt`.

## 7. The records root

A records root is a directory holding everything a records-management system keeps centrally, as plain files. Records themselves live anywhere: on any share, in any folder structure. The root is the only central place, and nothing in it is a record.

```
records-root/
  settings.toml
  schedule/              # §3.6
  register/              # §6
  holds/                 # §4
  aggregations/          # §5
  fixity/                # sweep reports, §9
```

### 7.1 Settings

```toml
organization = "Example Corporation"
fiscal_year_start_month = 10

[roots.legal]
windows = '\\files\legal'
macos = "/Volumes/legal"
linux = "/mnt/legal"
```

- **`organization`** — string. The organization's name, as it appears on a certificate.
- **`fiscal_year_start_month`** — integer, 1 to 12. The month the fiscal year begins (§8.2).
- **`roots`** — a table of **share roots**, each a table keyed by platform (`windows`, `macos`, `linux`) giving the path at which that share is mounted there. A root's name is what event locations record (§2.8.1). A platform with no entry cannot resolve that root, and a container found there has a location with no `root`.

A root's name is permanent once any event has recorded it: renaming it would orphan every location that names it. A root's mount paths MAY change.

## 8. Eligibility

Eligibility is defined here and computed by an implementation of §9. It is a function of a record, the schedule in force, the settings, the active hold matters, and an **evaluation date**, which is always given: nothing in this section reads a clock.

### 8.1 Outcome

Evaluating a record yields one **outcome**, the **reasons** for it (all that apply), and any **flags**.

| Outcome | |
|---|---|
| `eligible` | The record MAY be destroyed. §8.5 holds. |
| `not_eligible` | It may not, for the reasons given. |
| `review_due` | A `review` series has fallen due and no `reviewed` event has decided it (§8.4). |
| `cannot_evaluate` | The record, or a series it is under, cannot be read well enough to say. |

| Reason | With |
|---|---|
| `permanent` | The series codes |
| `held` | The matter identifiers |
| `awaiting_event` | The series codes with no trigger |
| `period_not_elapsed` | Each series' due date |
| `no_series` | |
| `unknown_series` | The codes the schedule does not carry |
| `series_retired` | Each retired code and its successor |
| `series_not_computable` | The descriptive series' codes |
| `undetermined_container` | |
| `slipcase_version_unsupported`, `profile_version_unsupported`, `malformed_profile` | What was found |

| Flag | |
|---|---|
| `past_maximum` | A `maximum` period has elapsed (§8.3). |
| `max_before_min_conflict` | One series' maximum falls before another's minimum (§8.3). |
| `snapshot_drift` | A series snapshot disagrees with the schedule in force (§2.4). |

Where the record can be read, the earliest date it could become eligible is also reported, when it can be computed.

### 8.2 Dates

Dates are civil dates. No time zone takes part.

A series' **trigger** is `created` for `Creation_Age`, and the series entry's `trigger` for `Event_Age` (§2.4). An `Event_Age` series with no trigger is **awaiting its event**.

The **cutoff** (§3.4, `x_cutoff`) moves the start of retention to the last day of the period containing the trigger: the calendar year, the fiscal year (which begins on the first day of `fiscal_year_start_month`), the quarter of the calendar year, or the month. `none` leaves the trigger as it is.

The **due date** is the cutoff date plus the period. Adding years or months lands on the same day of the resulting month, or on its last day where that day does not exist: February 29 plus one year is February 28. Adding days is exact.

A series is **due** when the evaluation date is on or after its due date.

### 8.3 Minimum, fixed, maximum

A `minimum` or `fixed` period makes the series due at its due date. A `maximum` period makes the series due at its due date and sets the `past_maximum` flag once the evaluation date is past it. A series with both (§3.4, `x_maximum`) is due at the minimum's date and flagged past the maximum's.

A hold always wins over a maximum: a held record past its maximum is `not_eligible` and flagged, and when the hold is released it goes to the head of whatever queue the implementation keeps.

Where a record has several series and one series' maximum falls before another's minimum, the record is flagged `max_before_min_conflict` and is `not_eligible` until a person resolves it. This profile never resolves it.

### 8.4 Review

Where a series' action is `review`, the series falling due makes the record `review_due`. A person then applies a different series, sets a new period, or confirms the action, with a comment, and the decision is recorded as a `reviewed` event (§2.8). Until then the record is not eligible, and after a decision that keeps a `review` series, retention restarts from the review date.

### 8.5 Eligible

A record is `eligible` when, and only when:

1. it has at least one series, and every series is due with action `destroy`;
2. no series is permanent or has action `retain` or `transfer`;
3. no series is `review` and undecided;
4. it has no holds (§2.5), and no active hold matter's scope (§4) matches it;
5. no flag in §8.3 blocks it.

A record with several series is eligible only when it is eligible under every one of them: the longest retention governs.

Eligibility is as of the evaluation date and the schedule version evaluated against, and an implementation that destroys re-checks it (§6) at the moment of destruction.

## 9. Implementation requirements

Beyond FRAMEWORK §11, an implementation of this profile:

- MUST NOT destroy, under any instruction, a record that §8.5 does not make `eligible` at the moment of destruction: a permanent record; a held record, or one an active matter's scope matches; one with a review due and undecided, awaiting an event, under a retired, descriptive, or unknown series, or flagged `max_before_min_conflict`; an unclassified or undetermined container; a container declaring a `slipcase_version` or `profile_version` it does not implement; or a record whose flyleaf changed since it was planned (§6.4).
- MUST write a change to a record's `[records]` table and the event recording it in one operation (§2.8), and MUST NOT reserialize an existing log entry, an existing register container, or an existing schedule version.
- MUST report, where it acts over a set of containers in which records are expected, every undetermined container, every container declaring a version it does not implement, and every malformed profile table, rather than passing over any of them.
- MUST give every evaluation an evaluation date (§8) and record it wherever the result is kept.
- MUST, when applying a hold, show the matching count before applying and report a scope matching nothing (§4.3).
- MUST preview every bulk rewrite of records (renumbering, reclassifying an aggregation's members) as the exact set of containers and changes before performing it.
- **Fixity sweep.** An implementation that checks fixity walks a scope and, for each record, verifies `fixity.content_sha256` against the content file and each component's `sha256` against its member, and compares the container's location (§2.8.1) with the last location in its log. It writes a report of the sweep in the records root's `fixity/` directory as a TOML file named by the sweep's start instant, holding `started`, `completed`, `scope`, counts, and every failure, move, and unreadable container; it appends `fixity_failed` and `moved_detected` to affected records' logs and nothing to the others; and it never alters a content file, a hash, or a location.
- MUST apply the display rule of FRAMEWORK §11 to paths and titles as well as member names.

## 10. Security considerations

A hold's `scope` is an expression evaluated against every record. SlipQL has no side effects and no access to anything but the flyleaf, and an implementation MUST bound what it spends evaluating a scope, because a scope is written by a person and a matter's container is a file anyone with write access to the records root can edit.

`location.raw` is a path as some operating system reported it. It is for a person reading the log; an implementation MUST NOT open, delete, or write to a path taken from a log entry or a manifest. The containers an implementation acts on are the ones it found by walking the scope it was given.

The register is evidence, and its protection is the chain and the write-once rule. Anyone with write access to `register/` can delete it; the profile makes that detectable (a missing sequence breaks verification), not impossible. An organization that needs the register to survive its administrators keeps a copy of each final's flyleaf hash somewhere they cannot reach, which this profile does not define.

A certificate claims what the manifest says and no more. An implementation MUST NOT write a certificate before every outcome is known, and MUST NOT describe deletion as anything but removal from the repository unless it has done more and can state what.

The plan a batch executes is a file the caller holds. The intent hashes the planned manifest, so a plan changed after approval is detected at the first record (`changed_since_plan` for every record whose flyleaf hash the changed plan misstates), but a plan is not signed, and approval is a statement the implementation records, not one it verifies.
