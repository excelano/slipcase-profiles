# Slipcase Records Profile — Design Document

**Status:** design draft.  
**Specification version:** 1.0 (draft)

`SPEC.md` states the rules. This document says why each one is drawn where it is, and what was considered and rejected. Nothing here is normative. Rules are cited as **SPEC §2.4**; the framework, the conventions, and the Slipcase specification as **FRAMEWORK §n**, **CONVENTIONS §n**, and **SLIPCASE §n**.

---

## 1. What a record is here

A record is a file that an organization has decided to keep for a reason and to destroy on a schedule. Records management as a discipline is older than computers and has settled vocabulary (series, retention, disposition, holds, custodians) that this profile uses as it finds it. What the profile adds is a place for that vocabulary to live that travels with the file: the container's flyleaf and its own members, and nothing outside them.

**Files are the truth.** Every records system in use keeps a database and treats the files as payload. The database is where the retention state lives, so the files mean nothing without the vendor, and when the vendor goes, so does the meaning. This profile inverts that: the record says what it is, and a database is a cache that any tool rebuilds by reading the files. That is the whole reason for the profile to be open, and it is why every decision below prefers a fact in the container to a fact anywhere else.

## 2. Identity

**UUIDv7 at capture, never reassigned (SPEC §2.2).** A record needs an identity that survives being copied, moved, renamed, and backed up, which a path cannot be. It needs one that two systems can assign without coordinating, which a sequence number cannot be. It needs to be the same identity on every copy, because a copy of a record is not a second record: destroying one copy while another survives is the ordinary state of backups, and the register records the destruction of the record, not of a byte sequence.

The rejected alternative was a content hash as identity. A record's content can change (SPEC §2.9) and its identity cannot, so the two are different things.

**`created` and `captured` are different dates.** The content's date is what retention schedules measure from in the common case; the capture instant is when the organization took responsibility. Collapsing them was considered and rejected because every schedule that says "destroy six years after creation" means the document, not the day it was filed.

## 3. Two agents, and why both parts of each

**Creator and custodian are separate (SPEC §2.2)** because they answer different questions: who made it, and who is responsible for it now. A legal hold on a departed employee's records is matched on custodian, and custodian changes when the person leaves. Creator never changes.

**Email plus directory identifier** is CONVENTIONS §2 and the reasoning is there. The records-specific point is that holds arrive from outside (a legal platform names custodians by email) and renumbering of the organization's directory arrives from inside, and the two halves of an agent survive each other's failure.

## 4. Series as a list, with a snapshot

**A list, not a single series.** Most records have one. The ones that have several (a contract that is both a financial record and a legal one) are the ones that matter most to get right, because their retention is the longer of the two (SPEC §8), and a single-series design would force a records manager to pick one and be wrong.

**The organization's code, never a vendor identifier.** The series code is how a records manager thinks and how the schedule is written. A vendor's internal identifier in the flyleaf would tie every record to the vendor's database, which is the dependency the profile exists to remove. Renumbering, when the organization changes its codes, is a logged rewrite of the flyleaf under an old-to-new map, and the log entry (`renumbered`) is what lets an auditor follow the code across the change.

**The snapshot is informational and says so.** A reader with the container but not the schedule, an auditor or a successor organization, needs to see what the series meant when it was applied. But a decision taken from the snapshot would be a decision taken from stale data the moment the schedule changed, so the rule is absolute: nothing decides from it, and a snapshot that disagrees with the schedule is reported. The version identifier in the snapshot is what makes the disagreement traceable.

## 5. Holds and relations

**Holds as a list, one entry per matter.** A record can be under several matters at once, and each is released on its own; a single hold flag would have to be cleared when the last matter releases, which means knowing which was last, which means a database. The entry records the matter's identifier and nothing about the matter itself, so that releasing a matter is a change to one definition file plus the removal of one entry per record, and the matter's own history (SPEC §4) is where the reasons live.

**A hold blocks partial destruction too (SPEC §2.9).** Replacing a content file or removing a component destroys evidence as surely as deleting the container, and a hold exists to stop evidence being destroyed. The rule follows from what a hold is for.

**A closed relation vocabulary.** Four types, and an unknown one is non-conformant rather than ignored, because a relation that one tool writes and another does not understand is a relation that silently does nothing. Three of the four have no consequence in this version; they are in the vocabulary so that writers converge on one spelling now rather than inventing `relates-to` and `related_to` and `see-also` before a later version gives them meaning.

## 6. Components, not nested containers

**Native compound formats first.** An email with attachments is one `.eml` file, and splitting it into a message plus components would be inventing a structure the format already has. Components exist for the case with no native format: a form plus its supporting documents.

**Components live inside the record's container (SPEC §2.7)** rather than as separate records related to it, because they are not records: they have no identity of their own, no series, and no life after the record's. A single container means a single destruction, a single hold, and a single fixity check, which is the behaviour a records manager expects of "one record with three parts". Nested containers (a `.slpc` inside a `.slpc`) were considered and rejected for live records: they double the structure a reader has to understand for no gain, and SLIPCASE's own tools would see the inner container as an opaque member. Nesting is reserved for transfer packages, which are not live records.

**The list and the members must agree both ways.** A member no entry names is a part the record does not admit to; an entry naming no member is a part the record claims and lacks. Either is a record whose parts cannot be trusted, which is what fixity exists to detect.

## 7. The event log

The log's mechanics are CONVENTIONS §5 and the reasoning for them is in the top-level design document. The records-specific decisions:

**Inside the container.** The alternative, a central log, is a database, and it is the database that fails the moment a record leaves the system. A log inside the container goes where the record goes. The cost is that a log cannot be read across records without opening each container, and that cost is accepted: a central index of events is a cache, like every other index here.

**The head is in the flyleaf (SPEC §2.8).** CONVENTIONS §5.5 requires a profile to put the head somewhere the log cannot reach. The flyleaf is rewritten in the same operation as every append, so it costs nothing to put it there, and the flyleaf is what the disposal plan hashes (SPEC §6), so at the moment that matters most the head is covered by the register.

**One operation for the change and its entry.** A change to the table and the entry recording it are written in one rewrite of the container, so that there is no state in which one exists without the other. A crash between two separate writes would leave either an unlogged change or a logged change that did not happen, and both are the record lying about itself.

**`captured` is always the first entry.** A log that starts anywhere else is a log whose beginning is missing, and the rule makes that detectable rather than a matter of interpretation.

**Successful fixity checks are not logged in the record.** A sweep runs on a schedule over every record, and logging each pass would make the log grow with the calendar rather than with the record's history. The sweep's own report is the evidence that the check ran; the record's log carries only what the sweep found wrong.

**Location as root plus relative path (SPEC §2.8.1).** The first design recorded the path as the operating system gave it. A sweep run from a Mac over a share mounted from Windows would then have found every record "moved", and appended an event saying so to every log, permanently, because the log is append-only. The fix is a named root declared once in the records root's settings, with the path relative to it, and the raw path kept beside them for a person reading the log. Comparing on root and path makes the same share the same place from every platform. A location with no root is not compared at all, because a false move cannot be taken back.

**A case-only rename is a move.** Case-insensitive filesystems make it tempting to compare case-insensitively. But a case-insensitive comparison would call two different files on a case-sensitive filesystem the same file, and a false "not moved" is a record whose location the log misstates. Exact comparison can only produce a true move report.

## 8. Changes after capture

**Permitted, and logged as partial destruction.** A records profile that forbade all change after capture would be simpler and would be ignored, because content does get corrected and parts do get added. Permitting it with a log entry that names what was lost, its hash, and why, keeps the record honest about its own history. The hold rule (§5) is what stops the permission being abused while it matters most.

**What this version does not do** is keep the replaced content. SEC 17a-4's audit-trail alternative requires that an original be recreatable after modification, not only that its existence be provable; serving that market means retaining prior versions, which is a different and larger design. The entry records the old hash so that a prior version kept elsewhere can be matched to it.

## 9. Non-goals in 1.0

Format identification beyond a media type (PRONOM); the key is reserved so that adding it is not a version change for anything else. Access control: `marking` is a string a person reads, and the profile takes no decision from it, because a profile that enforced access would have to know about users and permissions, which belong to the file share. Transfer of permanent records, which is the one place nested containers are intended to appear. Full-text search, which is an index.
