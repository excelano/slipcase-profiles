# Slipcase Core Profile — Design Document

**Specification version:** 1.0 (draft)

`SPEC.md` states the rules. This document says why each one is drawn where it is, and what was considered and rejected. Nothing here is normative. This profile's rules are cited as **CORE §3.4**; the framework, the conventions, and the Slipcase specification as **FRAMEWORK §n**, **CONVENTIONS §n**, and **SPEC §n**.

## 1. Borrowed, not invented

Slipcase gives meaning to two keys and leaves the rest of the flyleaf to whoever writes it, which means containers from different producers describe the same thing as `title`, `Title`, and `doc_title`. The fix is a vocabulary, and the vocabulary already exists. Dublin Core, first published in 1995 and an ISO standard (15836) since 2003, is the common denominator of document description: Office's document properties are Dublin Core underneath, so are OpenDocument's and XMP's, and archive and repository systems commonly map to it. A profile with its own vocabulary would be one more set of names to map; a profile that is Dublin Core needs no mapping at all to anything that already speaks it.

**Key names are DCMI's own (CORE §2.2), case included.** `rightsHolder` breaks the snake case the rest of a flyleaf tends to use, on purpose: the key is the term, and anyone who knows Dublin Core reads it without a table. Each key cites its term's URI, so a program that wants RDF can have it without the profile defining any.

**The definitions are summaries, and DCMI's are the authority.** DCMI publishes its term definitions under CC BY 4.0, and this repository is CC0, so the profile writes its own short definitions and cites each term by URI rather than copying DCMI's text. Where the two read differently, DCMI's meaning is the term's meaning.

**The name says Core, and the page says Dublin Core.** FRAMEWORK §9 fixes an official name as one use word, the same as the table, the prefix, and the last segment of the URI. `core` keeps the table short and matches what Office calls the same properties. Every place a person reads the profile says that it is Dublin Core, so that nobody takes it for a vocabulary of Excelano's.

## 2. Which terms

**The fifteen elements, and the refinements people and files use.** The DCMI Metadata Terms define more than fifty properties. A profile carrying all of them would offer keys nobody fills. The set is the fifteen classic elements plus seven refinements. `created` and `modified` are what Office records as `dcterms:` elements. `alternative`, `issued`, `license`, `rightsHolder`, and `isPartOf` are in the set because a person describing a document reaches for them: a short title, a publication date, a license, an owner, the series a document belongs to. A term outside the set can be written in the table and is preserved (FRAMEWORK §3); a later version adds terms when files or people turn out to carry them.

**Nothing that is not Dublin Core.** Office records who last modified a file, its revision number, a category, and a status, and none of these are Dublin Core terms. Mapping them in would give the profile keys of its own, which is what it exists to avoid.

## 3. Attribution, not accountability

**A creator is whoever the document credits (CORE §3.1).** A report written by a consultant, a datasheet from a vendor, a paper with three authors: the people named are mostly outside the organization holding the file, and many are organizations. So an attribution is a name, required, with whatever identifiers are known beside it, and nothing in it is checked against any directory. It answers who the document says made it, not who in the organization answers for it.

**Identifiers are optional and never invented (CORE §4.5).** An ORCID iD identifies a researcher and an LEI a company, and either makes a name unambiguous. A tool filling the table from a file writes one only when the file states it, because a guessed identifier is worse than none: it looks authoritative.

**An author string stays whole.** `Doe, J.; Roe, R.` looks like two people, and splitting it looks helpful. But the separators in author strings are not standardized (a comma separates surname from initials as often as it separates people), and two tools splitting differently would write different tables from the same file, which CORE §4 exists to prevent.

## 4. Shapes

**Repeatable keys are always arrays (CORE §3.2).** Dublin Core lets any term repeat, so a reader of a repeatable key has to handle several values in any case. Allowing a bare string as well would make every reader handle two shapes for one key, and every query test two forms. One value is an array of one.

**Title, alternative title, and description are single (CORE §3.3).** Every source carries one of each, and a list of titles has no order a reader agrees on. A second title is what `alternative` is for.

**Dates, never instants (CORE §3.4).** CONVENTIONS §3 requires a profile to say which form each key takes and to refuse the other. A person describing a document knows the day it was made far more often than the time, and a document's date is a civil date with no zone. Sources record instants; a tool takes the UTC date, which is the one choice two tools in different zones agree on, at the cost of an evening's document in the Americas carrying the next day's date. The Word example shows that case on purpose.

**A closed type list, an open language registry (CORE §3.5, §3.7).** DCMI's Type Vocabulary has twelve terms and changes rarely, so `type` is closed and a misspelling is caught. BCP 47 tags are checked for form only: the subtag registry grows, and a checker that consulted it would need the network and would fail on a tag registered last month.

## 5. A statement, and filling from a source

**The table is authoritative (CORE §2.3).** A container's description is written deliberately, and it can be more right than the file it describes: an archive can correct a wrong author or a garbled title without rewriting the original, which is the reason for keeping a description beside a file instead of inside it. So where the two disagree, the table is what this profile reads, and no tool overwrites it from the file unless a person asks.

**Only Dublin Core fills it (CORE §4.1).** The rule is literal: a Dublin Core element a file carries fills the key of the same name, and nothing else does. Files carry a great deal of other metadata that resembles Dublin Core (Office's keywords, OpenDocument's author field, a PDF's document information, a camera's EXIF, a music file's ID3 tags), and mapping any of it would be a judgment that one vocabulary's field means a Dublin Core term. Those judgments are arguable, and making them here would give terms meanings DCMI does not give them. Each of those vocabularies can have a profile of its own, built on its own standard, where its fields keep their own meaning.

**One exception, by name.** OpenDocument writes `dc:creator` for whoever last saved the file, which is not what the term means, so that one element is excluded rather than read literally.

**Filling adds, it does not replace.** A tool fills only keys that are absent, so a description someone corrected is never undone by reading the file again.

**Values that would not conform map to nothing.** A file can carry `dc:language` as `English` or `dc:type` as `Document`. Writing either would produce a non-conforming table, and tools choosing differently would write different tables, so both are dropped.

**Partial dates map to nothing.** A source date of `2024` or `2024-03` cannot become a TOML local date without inventing a day, and an invented first of January would read as a fact.

## 6. One kind, no members

**`resource` is the only kind (CORE §1).** A description describes the content file, and there is nothing else for a Core container to be. The framework requires a kind, and DCMI's word for the thing described is resource.

**The prefix is reserved and empty.** Dublin Core describes; it carries no parts. The prefix is the framework's, held so that a later version can define members without colliding with anything.

## 7. Why a draft

The filling rules are the part most likely to meet a file they did not anticipate, and no implementation has run them yet. The profile stays a draft, with changes landing without moving its number, until a tool fills tables from real files and the table has met them.
