# Slipcase Profiles — Design Document

**Status:** design draft.  
**Covers:** Framework 1.0, Shared Conventions 1.0

`FRAMEWORK.md` and `CONVENTIONS.md` state the rules. This document says why each one is drawn where it is, and what was considered and rejected. Nothing here is normative: where this document and either of those disagree, they win and this document is wrong.

A rule lives in one place. A change to a rule is an edit to the document that states it; a change to the reasoning is an edit here. Rules are cited as **FRAMEWORK §3** or **CONVENTIONS §5**, and the Slipcase specification as **SPEC §2.1**, because all three have a §3 and they are not the same subject. Each profile has a design document of its own in its directory.

---

## 1. Why profiles exist at all

Slipcase defines two keys and assigns meaning to nothing else. That is the format's strength, and it is also why nothing can be built on it without a second layer: a records tool and a handover tool both need to put their keys somewhere, and if each chooses freely, two tools meet in one flyleaf and collide, or a reader cannot tell which keys belong to whom.

The framework is that second layer, kept as thin as the first. It answers one question, how a purpose claims a part of a flyleaf and a part of the archive, and leaves every other question to the profile. It is not a schema language and defines no key a profile would use.

## 2. One table, self-identifying

**One top-level table per profile (FRAMEWORK §3)** rather than a profile's keys at the top level, because the top level is where collisions happen. Two profiles each defining `title` would be a conflict with no resolution; two profiles each owning a table cannot conflict, and the table name is the namespace.

**Identity by URI, not by table name.** The table name is a convention for people; the `profile` value is what a program checks. Two reasons. A URI resolves to the specification, so a reader meeting an unfamiliar table can find out what it is. And a table name is one word in one language chosen by one project; a URI is under an origin someone controls, so two projects cannot both claim `[records]` and mean different things without one of them being wrong by the URI. The name is still fixed per profile (FRAMEWORK §9), so a table named `records` whose `profile` names another specification is non-conformant to both rather than ambiguous.

**No top-level list of profiles.** A `profiles = [...]` key naming which tables are present was considered and rejected: it is a second place the same fact is stated, and a tool adding a profile would have to find and edit it. Every profile table carries its own identity, so the list is the set of tables carrying a `profile` key, and nothing has to be kept in sync.

**`kind` in the framework rather than left to each profile**, because every profile that has been thought about needs it (a record and a disposal batch; a document and a manifest), and a profile that needs only one kind pays one line. Putting it in the framework means a reader can ask "what is this container, under this profile" the same way for every profile.

## 3. One prefix

**Members under `<table>/` (FRAMEWORK §4)** for the reason the table exists: so that two profiles' members cannot collide and a reader can tell whose a member is. Tying the prefix to the table name, rather than letting a profile choose one, removes a decision that could only be made worse.

**SPEC §3's member-name rule applies to profile members.** Slipcase constrains the names of members an implementation writes to disk, not the names a container may hold. A profile's members will be extracted (a component of a record, handed to a person), so the rule for written members is the right one for them, and applying it at write time means no profile member can be one that extraction would later refuse.

## 4. Versions, and acting on them

FRAMEWORK §6 restates SPEC §2.4 rather than citing it, which this repository otherwise avoids. The restatement is deliberate: a profile's version has nothing to do with Slipcase's, and a reader of the framework should not have to hold both documents open to learn that a profile version implies no compatibility.

**Read and report, never act, on a version not implemented.** This goes beyond SPEC §2.4, which only puts an unrecognized version outside the conformance question. A profile drives actions that Slipcase does not: a records tool destroys files. A tool that destroyed a record under a profile version it did not implement would be acting on rules it had never read. Reading is allowed because the identity keys are the framework's and are stable across versions, and because refusing even to say "this is a Records Profile 2.0 table" would hide the container from the person who most needs to know it is there.

## 5. Independence in 1.0

**No profile may require another (FRAMEWORK §7).** The case for dependencies is real: a handover profile might reasonably say that every document it delivers is a record. The case against, for a first version, is that dependencies need rules the framework does not yet have (what happens when the required profile is absent, or at a version the requiring profile did not anticipate), and getting those wrong is harder to undo than adding them later. The framework reserves the idea so that a profile written now does not accidentally foreclose it.

## 6. Why the conventions are separate from the framework

The framework is about where a profile's data lives. The conventions are about how a few common things are written. They are separate documents because they change for different reasons: a new convention (a signature form, say) is a change to CONVENTIONS and to no rule about tables or prefixes, and a profile declares which conventions it uses (FRAMEWORK §8), which is a statement about the conventions document, not the framework.

**A profile must not redefine a convention.** The alternative, a profile that uses "mostly UUIDv7 but with one exception", is how a shared convention stops being shared. A profile that needs something a convention does not provide asks for the convention to change.

## 7. The conventions, one by one

**UUIDv7 (CONVENTIONS §1).** Time-ordered, so identifiers sort in creation order and index well, with no coordination needed to assign one. Lowercase hyphenated form because that is what RFC 9562 prints and what every library produces; constraining the case means comparison is a string comparison.

**Agents as email plus directory ID (§2).** Email is what external systems (a legal hold platform, a mail server) match on, and a stable directory identifier is what survives a person changing their name or address. Neither alone is enough: email changes, and a directory ID means nothing to a system outside the directory. Both required, so that a record does not end up with one agent written one way and the next another.

**Hashes over stored bytes (§3)**, never over a re-serialization, because TOML has no canonical form and SPEC says so (SPEC §2.2). A container is never hashed whole for the same reason at the ZIP level: a repack preserves every member and changes the bytes. The convention names the things that can be hashed so that a profile does not have to rediscover which.

**Local dates and UTC instants, nothing else (§4).** A local date-time names no zone and so names no instant; two readers in two zones would disagree about when it was. A civil date (the date a document was created, the date a retention period starts) genuinely has no zone and is a different kind of value from an instant, and a profile says which each key is so that a reader does not guess. UTC with `Z` rather than an offset, so that instants compare as strings.

## 8. The chained log

This is the convention with the most rules, because it makes a claim the others do not: that the bytes are the bytes that were written. Everything in CONVENTIONS §5 follows from making that claim checkable.

**Why hash bytes and not meaning.** The obvious design hashes a canonical form of each entry, so that a formatter could reflow the file without breaking anything. TOML has no canonical form, so the design would have to invent one, and then every implementation would have to produce it byte for byte, which is the same problem moved somewhere harder to see. Hashing stored bytes needs no agreement about anything but where an entry starts and ends.

**Why delimit by header line.** The byte range of an entry has to be found without parsing, or the hash depends on the parser. A header line that is exactly `[[event]]` is the one thing in a TOML array of tables that marks a boundary, and the written-form rules (§5.2) exist to make it unambiguous: no other line may equal it. Multi-line strings are forbidden because a multi-line string could contain such a line; comments are forbidden because a comment could too, and because nothing in a log needs one. The rejected alternative was a length prefix or a separator byte, which would have made the file not TOML.

**The trailing blank line belongs to the entry before it.** An entry runs to the byte before the next header, so the blank line a writer puts between entries is part of the earlier entry's bytes and is covered by the later entry's `prev`. That is the simpler rule (one boundary, not two), and it means the whitespace between entries is also something an edit cannot change unnoticed.

**LF only, no BOM, nothing before the first header.** Each of these is a byte that would otherwise be outside every entry and so outside every hash, or a byte that a tool changes silently. CRLF is the one that bites: a version control system or an editor on Windows will convert it, and the chain breaks. CONVENTIONS §5.5 says that is the chain working, which is true, and it is also why a profile should think about where a log is stored. The Records Profile stores its log inside the container, where no such tool runs.

**The seed ties the log to its owner.** Without it, a log could be lifted out of one container and dropped into another and verify perfectly. Seeding the first `prev` from the container's identifier means the first link breaks instead. The seed is the profile's to define because only the profile knows what the log belongs to.

**Appending reads the last entry back rather than remembering it.** A writer that computes `prev` from what it wrote last time, rather than from what is in the file now, will produce a correct-looking entry on top of a file somebody else has changed, and the chain will be intact from the writer's view and broken from everyone else's. Reading back costs one read of the tail of a small file.

**Refuse rather than repair.** A file that does not end with LF, or that has no header line, is either not a log or has been damaged. Fixing it means writing bytes into a region an earlier hash may cover. The writer stops and reports; a person decides.

**The head (CONVENTIONS §5.5).** A chain of `prev` links covers every entry but the last, so the two edits it cannot see are an edit to the last entry and a truncation. The first test written against the verifier found the first of these: change `hold_applied` to `hold_released` in a two-entry log and the log is intact. Both are closed by recording the hash of the last entry somewhere the log cannot reach. The convention requires a profile to say where, rather than fixing a place, because the right place differs: the Records Profile has a flyleaf that changes in the same repack as every append, which is the natural home; a log that is a file beside containers has to find one.

**`seq` as well as `prev`.** With the head recorded, `prev` and the head together detect every edit. `seq` adds nothing to detection; it makes a gap or a reorder reportable by number rather than only as "the hash is wrong somewhere", and it gives entries an order independent of `at`, which a wrong clock can scramble.

## 9. Non-goals

The framework does not define a schema language, a way to validate a profile table mechanically from a description, or a registry. A profile's specification is prose with examples, as Slipcase's is, and its example files are what an implementation tests against. If two official profiles turn out to need the same validation machinery, that is the point to consider a shared form, and not before.

It does not define signatures. A chained log detects an edit; it does not say who wrote an entry. A signature convention is the obvious next addition to CONVENTIONS and is deliberately not sketched here, because a half-designed signature scheme is worse than none.
