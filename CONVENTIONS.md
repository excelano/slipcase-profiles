# Slipcase Profiles — Shared Conventions

**Version:** 1.0  
**Status:** draft  
**Framework version:** 1.0

Things that every profile needs and that would otherwise be defined slightly differently by each: how to write an identifier, an agent, a hash, a date, and a log that cannot be edited without the edit showing. A profile states which of these it uses (FRAMEWORK §8) and defines none of them itself.

The key words **MUST**, **MUST NOT**, and **MAY** are to be interpreted as described in BCP 14 when, and only when, they appear in capitals.

## 1. Identifiers

An identifier is a UUID version 7 ([RFC 9562 §5.7](https://www.rfc-editor.org/rfc/rfc9562#section-5.7)), written as a TOML string in the 36-character hyphenated form with lowercase hexadecimal digits:

```toml
id = "01927c3e-8b2a-7d41-9f3c-2a6e5b1c4d7f"
```

An identifier is assigned once, when the thing it identifies comes into being, and is never reassigned or changed. A profile states what each of its identifiers identifies and when it is assigned. Comparison is exact over the string.

A string that is not of this form where an identifier is required is non-conformant.

## 2. Agents

An agent is a person or a system that did something. It is written as a table with two keys, both required:

```toml
actor = { email = "rm@example.com", id = "8f1c2b9e-1d4a-4e5f-9a0b-6c7d8e9f0a1b" }
```

- **`email`** — string. The address external systems match on.
- **`id`** — string. A stable identifier from the organization's directory, which survives a change of name or address. Its form is the directory's; this convention constrains only that it is a non-empty string.

Two agents are the same when their `id` values are equal. `email` is for people reading and for systems that have nothing else.

## 3. Hashes

A hash is SHA-256 ([FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)), written as a TOML string of 64 lowercase hexadecimal digits.

A hash is always taken over the exact bytes of the thing named, as stored. A profile names what is hashed; this convention fixes how:

- A member of a container is hashed as the bytes the member holds, uncompressed, as a reader receives them. The flyleaf is a member and is hashed the same way.
- A file outside a container is hashed as its bytes.
- A container as a whole is never hashed, because repacking a ZIP archive changes its bytes without changing what it holds (SPEC §3 requires a rewrite to preserve members, not bytes).
- A TOML document is never hashed from a re-serialization of it. TOML defines no canonical form, so the bytes as stored are the only bytes two readers can agree on.

## 4. Dates and instants

A date is a civil calendar date: a TOML local date.

```toml
created = 2024-01-17
```

An instant is a point in time: a TOML offset date-time in UTC, written with `Z`.

```toml
captured = 2024-02-03T15:04:11Z
```

A profile states, for each key, whether it is a date or an instant, and an implementation MUST NOT accept the other form in its place. A TOML local date-time, which names no zone, MUST NOT be used for either.

Date arithmetic is a profile's to define. This convention fixes only the representation.

## 5. Chained logs

A chained log records what happened to something, in order, in a form where any later edit to an earlier entry can be detected. It is a UTF-8 text file: an additional member of a container under the profile's prefix, or a file beside containers, as the profile states.

### 5.1 Form

The file is a TOML document consisting of an array of tables under one name, the log's **entry name**, which the profile chooses:

```toml
[[event]]
seq = 1
at = 2024-02-03T15:04:11Z
prev = "11bea12d8e12dbe5505968cf4501bc6a53e44304021054ea8de76e0b069eae37"
type = "captured"

[[event]]
seq = 2
at = 2026-03-12T09:14:02Z
prev = "47b9e224f9aad9d4106b0917cc5d8a78fa4c945fe9e60c86d6db816108b906f9"
type = "hold_applied"
```

The example is a real log: the first `prev` is the hash of the seed `01927c3e-8b2a-7d41-9f3c-2a6e5b1c4d7f`, and the second is the hash of the first entry's bytes (§5.3), including the blank line that follows it. `examples/conventions/events.toml` holds it byte for byte.

Every entry MUST contain:

- **`seq`** — integer. `1` for the first entry, and one more than the previous entry's for each entry after it.
- **`at`** — an instant (§4). Entries need not be in `at` order: a clock can be wrong, and `seq` is the order.
- **`prev`** — a hash (§3). §5.3.

The profile defines every other key an entry carries.

### 5.2 Written form

So that an entry's bytes can be found without parsing the file, a writer MUST write the file in this form, and a file not in this form is non-conformant:

- Line endings are LF (U+000A) alone. There is no byte order mark.
- The file begins with the first entry's header line. Nothing precedes it.
- Each entry begins with a **header line** that consists of `[[`, the entry name, `]]`, and LF, with nothing else on the line: no leading or trailing whitespace, and no comment.
- No other line in the file is equal to a header line. To make that checkable, an entry MUST NOT contain a multi-line string (TOML's `"""` and `'''` forms) and MUST NOT contain a comment line.
- The file ends with LF.

The file remains an ordinary TOML document, and any TOML reader reads it. The rules above constrain only what a writer produces.

### 5.3 Entry bytes and the chain

An entry's **bytes** are the bytes of the file from the first byte of its header line to the byte before the first byte of the next header line, or to the end of the file for the last entry. The LF that ends the entry's last line is part of the entry. A reader finds entry bytes by scanning lines for header lines; it MUST NOT find them by parsing the document and serializing a table again.

The chain:

- `prev` of the first entry is the hash of the log's **seed**, a byte string the profile defines. A profile ties the seed to the thing the log belongs to (the UTF-8 bytes of the container's identifier, for example), so a log cannot be moved from one container to another without the first link breaking.
- `prev` of every later entry is the hash of the previous entry's bytes.

A log is **intact** when every entry's `seq` is in sequence from `1` and every entry's `prev` is the hash it should be. A log that is not intact is **broken at** the first entry whose `seq` or `prev` is wrong, and everything from that entry on is unverified. Verification reads the document to take `seq` and `prev` from each entry and delimits the bytes to hash them; both are needed, and neither replaces the other.

### 5.4 Appending

A writer appends an entry by writing its bytes after the last byte of the file. It MUST NOT change any byte already in the file. It computes the new entry's `prev` over the bytes of the last entry as stored, which it reads back rather than remembers. Where the file does not end with LF, or holds no header line at all, the writer MUST refuse to append rather than repair the file, because repairing it would change bytes an earlier hash covers.

A profile may place the append inside a larger operation (a repack of the container that also changes the flyleaf) and require the two to succeed or fail together. The convention does not.

### 5.5 What breaks a log, and what is meant to

Any tool that rewrites the file's bytes while preserving its TOML meaning breaks the chain: a TOML formatter, a text editor that converts line endings, a version control system normalizing LF to CRLF. The chain is meant to break in every such case, because the log's claim is that the bytes are the bytes that were written. A profile that stores a chained log in a place where such tools run should say so, and an implementation that sees a broken log reports it and never repairs it.
