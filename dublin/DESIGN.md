# Slipcase Dublin Profile — Design Document

**Specification version:** 1.0 (draft)

`SPEC.md` states the rules. This document says why each one is drawn where it is. Nothing here is normative. This profile's rules are cited as **DUBLIN §2.3**; the framework, the conventions, and the Slipcase specification as **FRAMEWORK §n**, **CONVENTIONS §n**, and **SPEC §n**, as they are everywhere else in this repository.

---

## 1. What the profile is for

A file passed from one person to another loses what its owner knew about it: who made it, what it is about, whose it is to copy. Slipcase gives that knowledge a place that travels with the file, and this profile gives it a shape that any tool can read without agreeing on anything else. The profile describes. It drives no action and makes no decision, which is why it is small.

## 2. Fifteen elements, and only these

The elements and their definitions are the profile, stated once in DUBLIN §2.2 and nowhere else. The profile adds no further elements, no sub-keys, and no qualifiers, and its table carries nothing else of its own beyond the three keys every profile carries (FRAMEWORK §3). A writer who needs a finer distinction than an element offers states it in the element's text, or carries another profile beside this one.

**One kind (DUBLIN §2.2).** The framework requires a `kind`, and every definition speaks of "the resource", so the one kind is `resource`. A description profile has nothing to distinguish between kinds: a report and a photograph are described with the same fifteen elements.

**Lowercase keys.** The table names and keys of every profile in this repository are lowercase, and the element names become keys by lowercasing alone, so a reader moves between the definition table and a flyleaf without a mapping.

## 3. One value shape for every element

**An array of strings, always (DUBLIN §2.3).** Several elements routinely hold more than one value: a report has two creators, a dataset three subjects, a bilingual document two languages. If some elements were strings and others arrays, every writer would have to remember which, and every reader would have to handle both. One shape means one rule to state, one to check, and one way to write a single value: an array of one.

The cost is that `title = "Survey"` is non-conformant where a reader might expect it to pass. It is reported rather than accepted, because a reader that accepted both forms would make the bare string conventional and the rule meaningless.

**Non-empty arrays and strings.** An element is either absent or says something. An empty array and an empty string would both be ways of saying nothing that differ from absence only in bytes, and a reader would have to decide whether they mean "unknown", "none", or "not yet filled in". The profile gives them no meaning by making them non-conformant, so that absence is the only way to state nothing.

**Order is kept and means nothing.** A writer who lists a principal creator first has done something a person reading the flyleaf will notice, so a rewrite preserves the order (DUBLIN §4). The profile does not say the first creator is the principal one, because nothing in the definitions says so and a reader cannot tell a deliberate order from an incidental one.

## 4. Text, and no interpretation

**No vocabularies, no syntax.** Every value is text as the writer states it. A vocabulary for `type` or `language`, or a syntax for `date`, would be a second specification the profile depends on, and every writer would have to know it before writing anything. The profile defines the elements and leaves their values to the people who know the resource. A community that wants a vocabulary can agree on one without changing what a conformant container is.

**`date` is not a convention date (DUBLIN §2.3).** CONVENTIONS §3 defines a date and an instant, and FRAMEWORK §8 forbids a profile its own form for either. The `date` element is defined as "a point or period of time", and a period is neither a TOML local date nor an instant, nor is a year on its own, nor a season. Typing `date` as a convention date would make most real values unwritable; typing it as a mix of convention dates and strings would give a reader two shapes to handle for one element. It is text, and because the profile gives that text no form, it defines nothing that competes with the convention.

**`identifier` is not a convention identifier.** CONVENTIONS §1 uses the word for a UUIDv7 that a profile assigns. The `identifier` element holds whatever reference the resource already has in some context (an ISBN, a report number, a URL), which the profile neither assigns nor checks. The specification says so in one line, because the shared word invites the wrong reading.

**No mapping from file formats.** Many file formats carry descriptive fields of their own. The profile does not say how those fields fill the elements, because each mapping would be a judgment about another format's semantics that the profile has no basis to make, and a tool that makes one makes it in its own name.

## 5. An open table, and no members

**Other keys are preserved (DUBLIN §2.4).** The framework's default is that a key a profile does not define is permitted and kept. Closing the table would turn every addition a writer makes into non-conformance without telling a reader anything about the fifteen elements, which are all a reader of this profile looks at.

**No members.** Everything the profile says fits in the flyleaf. The prefix `dublin/` exists because the framework reserves one for every profile (FRAMEWORK §4), and this version defines nothing under it.

## 6. Security

A description is a claim, and the profile says so (DUBLIN §5) so that no implementation presents a `creator` as proof of authorship or a `rights` statement as a grant. Because the profile drives no action, FRAMEWORK §12's requirement to state what is checked before acting has nothing to apply to; what remains is that values are text from an untrusted writer, so none is fetched, opened, or run, and each is displayed under the framework's bidirectional-text rule.
