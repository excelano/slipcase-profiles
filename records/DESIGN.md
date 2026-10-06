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

**Permitted, and logged as partial destruction.** A records profile that forbade all change after capture would be simpler and would be ignored, because content does get corrected and parts do get added. Permitting it with a log entry that names what was lost, its hash, and why, keeps the record's account of its own history true. The hold rule (§5) is what stops the permission being abused while it matters most.

**What this version does not do** is keep the replaced content. SEC 17a-4's audit-trail alternative requires that an original be recreatable after modification, not only that its existence be provable; serving that market means retaining prior versions, which is a different and larger design. The entry records the old hash so that a prior version kept elsewhere can be matched to it.

## 9. Non-goals in 1.0

Format identification beyond a media type (PRONOM); the key is reserved so that adding it is not a version change for anything else. Access control: `marking` is a string a person reads, and the profile takes no decision from it, because a profile that enforced access would have to know about users and permissions, which belong to the file share. Transfer of permanent records, which is the one place nested containers are intended to appear. Full-text search, which is an index.

## 10. The schedule: NARA's layout, as NARA writes it

**NARA's CSV layout rather than a format of this profile's own (SPEC §3.1).** The General Records Schedules are the one retention schedule published in a machine-readable form by an authority with no product to sell, and every United States federal agency already holds its records against them. A schedule format that could not load that file unchanged would be asking every organization to translate, and the translation is where the errors would live. So the requirement is absolute and testable: the published file is in the repository and loads with no mapping and no error.

**What the file actually contains decided several rules.** The FAQ describes a layout; the file departs from it, and the file wins because the file is what an organization downloads. The column is `Retention (Years)`, not `Retention`, so both names are the column. The values are `Event_Age` and `Creation_Age` with a capital A, so controlled values compare without regard to case. One row has `Final action ` with a trailing space, so values are trimmed. Fourteen trailing columns have empty names, so an empty-named column is ignored. Thirteen fields hold line breaks inside quotes, so a reader needs a real CSV parser and not a line splitter. Each of these was found by loading the file, and `examples/schedule/SOURCE.md` lists them so that the next transmittal can be checked against the same list.

**Descriptive rows load; they do not compute (SPEC §3.3).** Fifty-four rows of the GRS state no retention type, period, or event, because the published instruction cannot be reduced to one (an OPF is kept as long as the person is employed and then sent elsewhere). Two more state a range and one states hours. The first design refused any row it could not compute, which refused the GRS. The second accepted them as rows with no period, which is the design: a descriptive row is a real series a record can be classified under, and a record under it has an answer to "when may this be destroyed", which is "not by this profile". That answer is `cannot_evaluate` with the series named, and a person decides. Refusing to guess is the principle; refusing to load would have been refusing to help.

**NARA's vocabularies are open, this profile's are closed.** A value outside NARA's set in a NARA column is "not stated", because NARA's columns are NARA's and the next transmittal may add a value (it added `Submission` and `End of service` to the event column after the FAQ was written). A value outside the set in an `x_` column is an error, because the column is this profile's and a misspelling there is a mistake nobody else will catch.

**A retired row stays (SPEC §3.3).** Four GRS rows are superseded and say by what. Dropping them would leave records already classified under them pointing at nothing. Keeping them, forbidding new classification, and reporting the successor at evaluation is what lets a records manager find and reclassify those records rather than discover them as unknown series.

**`x_event_name` was in the first design and is not in this one.** It was to carry events finer than NARA's four general types. The file itself carries them in `Event Type (General)` (`End of service`, `Survey completion`), so a second column for the same thing would have been two places for one fact. A stated value outside the four is a named event, which is what the extension would have said.

**Minimum and maximum on one row (SPEC §3.4, `x_maximum`).** The alternative was two rows for one code, distinguished by `x_period_kind`, which breaks the rule that a code appears once per jurisdiction and makes "the series FIN-200" two things. A second period column on the same row keeps one row per series, and the constraint that `x_period_kind` is then absent or `minimum` stops the row contradicting itself.

**Versions that are never edited (SPEC §3.6).** A schedule change is a decision with a date and a person, and a record's snapshot and a disposal plan both name the version they used. Editing a version in place would make those references lie. The identifier carries the instant and a hash prefix so that two imports a second apart cannot collide and a renamed file cannot pass for another.

## 11. The records root and share roots

**One central directory of plain files (SPEC §7).** Everything a records system keeps that is not inside a record has to live somewhere, and the choice was between a database and a directory. A directory of TOML, CSV, and containers is readable by anyone, diffable, backed up by whatever backs up the share, and is the same thing on every platform. What it costs is speed on large registers, and a register is read in full only by `verify`, which is the operation that should read everything.

**Share roots are in the settings, named once.** The reasoning is in §7 of this document under location. The settings are where the names are declared because the settings are the one file every implementation reads before it does anything else, and a root name is meaningless until something declares what it stands for on this platform.

## 12. Eligibility

**An evaluation date is always given (SPEC §8).** A function of the clock is a function that cannot be tested against a fixed answer, and eligibility is the computation that destroys records. The implementation's command line defaults to today and says so; the definition does not know what today is.

**Civil dates, month-end clamping, cutoffs (SPEC §8.2).** Retention schedules are written in years and months from a date, by people who mean calendar arithmetic, and the only question such arithmetic leaves open is what February 29 plus a year is. Clamping to the month's last day is what every records manager would say, and it is stated so that no two implementations differ by a day. Cutoffs are stated the same way because "three years after the end of the fiscal year in which the record was created" is how schedules are written, and the fiscal year's start is the one organizational fact the arithmetic needs.

**The longest retention governs (SPEC §8.5).** A record under two series is eligible only when both say so, because the alternative is destroying a record one series still requires. A permanent series anywhere makes the record permanent for the same reason, stated separately because it is the case that matters most.

**Flags are not decisions (SPEC §8.3).** A record past its maximum while on hold, or whose series conflict, is a record a person has to look at. The profile reports and stops. Resolving a maximum-before-minimum conflict automatically would mean choosing which law to break.

**Review is a disposal action and an outcome (SPEC §8.4).** MoReq2010's review is the case where the schedule says "a person decides", and the profile makes that a first-class outcome rather than treating it as not-eligible-with-a-note, so that a records manager's queue of decisions is a query and not a search.

## 13. Holds and aggregations as containers

**Defined centrally, applied to records (SPEC §4, §5).** A hold matter and an aggregation are each one thing with one history, and the records they touch are many. The definition lives in one container in the records root; each record carries only a pointer (a `holds` entry, a `member-of` relation). Releasing a matter is then one change to the definition plus one small change per record, each logged where it belongs, and the question "who released this and when" has one answer in one place.

**As containers rather than TOML files**, so that the hold notice or the case file's cover sheet travels with the definition, and so that the definition has the same chained log every record has, with the same tools reading it. An empty content file is permitted for the common case of a definition with no document, which Slipcase allows.

**Scope as a SlipQL expression.** A hold has to say which records it covers in a form a program can apply to a hundred thousand containers and a person can read. SlipQL already exists for querying flyleafs and is the open layer's own query language, so the alternative would have been a second expression language for one key. The match count shown before applying is what makes an expression safe to write: a scope that matches nothing, or everything, is seen before it does anything.

**Matching at classification and at destruction, not only at placing.** A hold placed on Monday has to cover the record captured on Tuesday. And a record's `holds` list is maintained by the implementation that applies holds, which can have a gap; the defensive check at destruction (SPEC §4.3) is what makes the gap a reported condition rather than a destroyed record.

**Membership by relation in the record, found by query.** An aggregation that listed its members would have to be rewritten every time a record joined or left, and would be wrong the moment a record was copied elsewhere. The record saying what it belongs to is the same inversion as everything else here: the file is the truth.

**Inheritance is a copy at joining.** A member that looked up its series through its aggregation at evaluation time would have retention that changed when the aggregation's did, invisibly to the record's own log. Copying the series into the record, logged as `classified`, keeps every record's retention in the record.

**Closing triggers `Final action` only.** Closing a case file is what "final action" means in NARA's vocabulary, and a series triggered by some other event (a person leaving, a document being superseded) is not triggered by the case closing. Mapping closure to every event would have destroyed records early.

## 14. The register

**Intent, journal, final (SPEC §6).** Destruction is the one irreversible operation, and a crash in the middle of it is the one case the design has to survive. Three files, each written once or only appended, mean that at every instant the register says what has actually happened: the intent says what was going to be attempted, the journal says what has been attempted so far, and the final says what was done. A single file rewritten at the end would have said nothing during the run and would have had to be rewritten, which the chain forbids.

**The intent is the lock.** Creating `N.intent.slpc` with create-new semantics is atomic on every filesystem the profile targets, including SMB, so it is the one operation two runs cannot both win. Making the lock a file in the register, rather than a lock file beside it, means the register itself records that a claim was made, and an intent that never finalizes is an auditable fact rather than a stale lock.

**One batch at a time.** The chain needs batch N−1's final to write batch N's, so two concurrent runs could not both finalize. Serializing runs at the claim is simpler than any scheme for chaining in finalization order, and it also means two plans naming the same record cannot execute at once.

**Recovery is explicit and never automatic.** The first design had any run finalize an unfinished intent it found. Across machines, nothing in the register distinguishes a crashed run from one still deleting on another host, and a run that "recovered" a live batch would have written a final whose manifest was a lie while records went on being destroyed. A person who knows the run is dead confirms that; the profile cannot.

**`unknown` is an outcome.** When recovery finds a record gone and no journal entry for it, the record may have been destroyed by the run in the instant before it died, or by something else. Writing `destroyed` would be a claim; `unknown` is the truth.

**The final is also exclusive-created**, so that recovery racing a run that was alive after all, or two recoveries, produce one final and one failure rather than two finals.

**The chain is over stored bytes of members, not over containers**, for the reason CONVENTIONS §3 gives: repacking changes bytes. Every register container is written once and never repacked, and the rule that nothing reserializes a register flyleaf is what keeps that true.

**The journal is hashed whole rather than by head.** It is complete when the final is written, so a whole-file hash covers it entirely, and verification of a final then needs no knowledge of the journal's structure. CONVENTIONS §5.5 was widened to allow this once the register showed the case.

**The genesis value is a fixed string's hash**, published in the specification, rather than something per organization. A per-organization value would be one more thing to keep and to lose, and the first batch's `previous_flyleaf_sha256` has nothing to say except "there is no previous batch".

**Six digits.** A register that reaches a million batches has run one batch a day for 2,700 years. The width is fixed so that names sort.

**Approval is recorded, not verified.** This profile defines no users and no authority. The implementation writes what it was told and the certificate says that it was told, so that nobody reads a certificate as proof of an approval the profile never checked.

**No secure erasure.** Overwriting is unreliable on SSDs, copy-on-write filesystems, SMB shares with snapshots, and synced folders, and claiming it would be a false assurance. The scope statement says what happened and names backups; crypto-shredding is the one technique that would make destruction verifiable in backups too, and it is a possible later feature, not something this profile pretends to.

## 15. Implementation requirements and security

**The never-destroy list is in the implementation section (SPEC §9)**, restating §8.5 from the other side, because the one place a reader of an implementation looks for "what will this refuse" should hold the answer without a derivation.

**A sweep report in the records root, exceptions in the record (SPEC §9).** NARA requires a documented integrity check; a report per sweep is that document. The record's own log gets only what the sweep found wrong, for the reason §7 of this document gives.

**Paths in logs are never opened (SPEC §10).** A log is data that anyone who can write a container can write. Treating a path from it as a place to delete would make the register a weapon.

**What the profile protects and what it detects.** Anyone with write access can delete records and can delete the register. The profile makes both detectable, by fixity and by the chain, and does not pretend to prevent either; prevention is the file share's job and the organization's.
