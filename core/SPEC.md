# Slipcase Core Profile — Specification

**Version:** 1.0  
**Status:** draft  
**Framework:** 1.0 · **Conventions:** 1.0 · **Slipcase:** 1.1

Dublin Core metadata for Slipcase containers. The Core Profile describes a container's content file: what it is, who made it, when, in what language, and under what rights. It defines no vocabulary of its own. Every key is a term of the DCMI Metadata Terms, maintained by the Dublin Core Metadata Initiative, cited here by its URI and given the meaning DCMI gives it.

## 1. Identity and terminology

The key words **MUST**, **MUST NOT**, and **MAY** are to be interpreted as described in BCP 14 when, and only when, they appear in capitals. **FRAMEWORK**, **CONVENTIONS**, and **SPEC** cite the profiles framework, the shared conventions, and the Slipcase specification.

| | |
|---|---|
| Name | Slipcase Core Profile |
| `profile` | `https://slipcaseformat.org/profiles/core` |
| Profile table | `[core]` |
| Profile prefix | `core/` (this version defines no members under it) |
| Kinds | `resource` |
| Conventions used | dates (CONVENTIONS §3) |

**Resource** — the content file the container holds, which the `[core]` table describes. DCMI calls the thing described a resource, and the kind takes its name.

**DCMI term** — a property of the DCMI Metadata Terms, identified by a URI of the form `http://purl.org/dc/terms/<name>`. Each key in §2.2 names the term it is, and DCMI's definition is the authority on what the term means. The definitions below are summaries for a reader of this document.

**Source** — Dublin Core metadata a content file already carries in its own format (§4).

## 2. The core table

A container is described under this profile when its flyleaf carries a `[core]` table with the three framework keys (FRAMEWORK §3) and `kind = "resource"`. Every other key is optional: a table carrying only the framework keys is conformant and says nothing about the resource.

### 2.1 Example

```toml
slipcase_version = "1.1"

[content]
file = "site-survey-2024.pdf"

[core]
profile = "https://slipcaseformat.org/profiles/core"
profile_version = "1.0"
kind = "resource"
title = "Site survey, Lake Charles terminal"
description = "Geotechnical survey of the north tank farm, with boring logs."
subject = ["geotechnical survey", "tank farm", "boring logs"]
type = "Text"
format = "application/pdf"
language = ["en-US"]
created = 2024-03-18
issued = 2024-04-02
identifier = ["GS-2024-0117"]
rights = ["Prepared for the owner under contract C-4471."]

[[core.creator]]
name = "Gulf Geotechnical Ltd."
lei = "5493000GULFGEO0EX060"

[[core.creator]]
name = "Jane Doe"
email = "jdoe@gulfgeo.example"
```

### 2.2 Keys

| Key | DCMI term | Form (§3) | Meaning |
|---|---|---|---|
| `title` | `http://purl.org/dc/terms/title` | single text | The name given to the resource. |
| `alternative` | `http://purl.org/dc/terms/alternative` | single text | Another name for it, such as an abbreviation or a translated title. |
| `description` | `http://purl.org/dc/terms/description` | single text | An account of the resource: an abstract, a summary, a table of contents. |
| `creator` | `http://purl.org/dc/terms/creator` | attribution | Who is responsible for making it. |
| `contributor` | `http://purl.org/dc/terms/contributor` | attribution | Who contributed to it. |
| `publisher` | `http://purl.org/dc/terms/publisher` | attribution | Who made it available. |
| `rightsHolder` | `http://purl.org/dc/terms/rightsHolder` | attribution | Who owns or manages rights over it. |
| `subject` | `http://purl.org/dc/terms/subject` | repeatable text | Its topics: keywords, key phrases, or classification codes. |
| `identifier` | `http://purl.org/dc/terms/identifier` | repeatable text | Unambiguous references to it in some context: a document number, an ISBN, a DOI, a URI. |
| `source` | `http://purl.org/dc/terms/source` | repeatable text | Resources it is derived from. |
| `relation` | `http://purl.org/dc/terms/relation` | repeatable text | Related resources. |
| `isPartOf` | `http://purl.org/dc/terms/isPartOf` | repeatable text | Resources it is physically or logically included in. |
| `coverage` | `http://purl.org/dc/terms/coverage` | repeatable text | Its spatial or temporal topic, where it applies, or the jurisdiction under which it is relevant. |
| `rights` | `http://purl.org/dc/terms/rights` | repeatable text | Statements about rights held in and over it. |
| `language` | `http://purl.org/dc/terms/language` | language (§3.7) | The languages of its content. |
| `license` | `http://purl.org/dc/terms/license` | license (§3.8) | Legal documents giving permission to do something with it. |
| `type` | `http://purl.org/dc/terms/type` | type (§3.5) | Its nature or genre. |
| `format` | `http://purl.org/dc/terms/format` | format (§3.6) | Its file format. DCMI's term also covers a physical medium or dimensions; for a content file it is the media type. |
| `date` | `http://purl.org/dc/terms/date` | date (§3.4) | A point or period of time in its life cycle. The refinements below say more where one fits. |
| `created` | `http://purl.org/dc/terms/created` | date | When it was created. |
| `modified` | `http://purl.org/dc/terms/modified` | date | A date on which it was changed. |
| `issued` | `http://purl.org/dc/terms/issued` | date | When it was formally issued or published. |

Key names are DCMI's own, case included, so that `rightsHolder` here is `rightsHolder` in every DCMI serialization. Keys this section does not define are permitted in the table and MUST be preserved (FRAMEWORK §3). A later version of this profile may add DCMI terms; it never adds a key that is not one.

### 2.3 A statement about the resource

The `[core]` table is a statement about the resource made by whoever wrote the container. Where it disagrees with metadata the content file carries, the table is what this profile reads: it may correct a file's own metadata without the file being rewritten. An implementation MUST NOT replace a value in the table with one taken from the content file except at a person's request.

## 3. Value forms

### 3.1 Attribution

`creator`, `contributor`, `publisher`, and `rightsHolder` are arrays of tables, one table per person or organization, in the order they are credited:

| Key | Type | |
|---|---|---|
| `name` | string, non-empty | The name as the resource credits it. Required. |
| `email` | string, optional | An address for the party. |
| `uri` | string, optional | A URI identifying the party. |
| `orcid` | string, optional | An ORCID iD, for a person. |
| `lei` | string, optional | A Legal Entity Identifier (ISO 17442), for an organization. |

Attribution names whoever the resource credits, inside the organization that wrote the container or not. Nothing in it is checked against a directory, and it says nothing about who is accountable for the container.

### 3.2 Repeatable text

`subject`, `identifier`, `source`, `relation`, `isPartOf`, `coverage`, and `rights` are arrays of strings. A single value is an array of one: a bare string is non-conformant, so a reader has one shape to handle. No entry is an empty string, and no array is empty: a key with no value is absent. An `identifier` entry is any string that refers to the resource, not an identifier in the sense of CONVENTIONS §1.

### 3.3 Single text

`title`, `alternative`, and `description` are strings, non-empty. Dublin Core allows a term to repeat; this profile does not repeat these three, because each source in §4 carries at most one of each.

### 3.4 Dates

`date`, `created`, `modified`, and `issued` are dates (CONVENTIONS §3): TOML local dates, never instants. A person describing a document knows the day it was made far more often than the moment, and CONVENTIONS §3 fixes one form per key.

### 3.5 Type

`type` is a string, one of the twelve terms of the DCMI Type Vocabulary: `Collection`, `Dataset`, `Event`, `Image`, `InteractiveResource`, `MovingImage`, `PhysicalObject`, `Service`, `Software`, `Sound`, `StillImage`, `Text`. Any other value is non-conformant. Each names the term `http://purl.org/dc/dcmitype/<value>`.

### 3.6 Format

`format` is a string: the content file's media type, written as RFC 6838 §4.2 defines a type and subtype name (`application/pdf`), without parameters.

### 3.7 Language

`language` is an array of strings, each a well-formed language tag under BCP 47 (RFC 5646 §2.1), such as `en-US` or `de`. A tag is checked for form, not against the language subtag registry.

### 3.8 License

`license` is an array of strings, each an absolute URI naming a license: a Creative Commons deed, an SPDX license page, an organization's own terms. Free-text statements belong in `rights`.

## 4. Filling from a source

Many files already carry Dublin Core: an Office document's core properties, an OpenDocument file's metadata, the XMP packet in a PDF or an image. An implementation that fills `[core]` from Dublin Core a content file carries MUST fill it as this section states, so that two implementations reading the same file write the same table. It fills only keys that are absent; a key already present is replaced only at a person's request (§2.3). A person writing the table by hand is not bound by this section.

### 4.1 Which elements

An element in the Dublin Core elements namespace (`http://purl.org/dc/elements/1.1/`) or the DCMI terms namespace (`http://purl.org/dc/terms/`) whose local name is a key in §2.2 fills that key: `dc:title` fills `title`, `dcterms:created` fills `created`. Nothing else in a file fills `[core]`: an element in any other namespace maps to nothing, whatever it means, and so does a Dublin Core element whose local name §2.2 does not define.

One element is excluded by name. OpenDocument defines its `dc:creator` as the person who last modified the file, not the author, so an OpenDocument `dc:creator` maps to nothing.

### 4.2 Where to read

A format's primary metadata is read: `docProps/core.xml` in an Office Open XML file, `meta.xml` in an OpenDocument file, the document's metadata stream in a PDF, the XMP packet in an image. Where a file carries Dublin Core in more than one place, only the primary metadata is read.

### 4.3 Values

- A text element fills a single-text key with its value, or adds one entry to a repeatable-text key.
- An XMP language alternative contributes its `x-default` item, or its first item where there is none; an XMP sequence or bag contributes one entry per item, in order.
- A `creator`, `contributor`, `publisher`, or `rightsHolder` value becomes one attribution table whose `name` is the value, whatever separators it contains: `Doe, J.; Roe, R.` is one name. A source never yields an `email`, `uri`, `orcid`, or `lei` the file does not state as one.
- A date element holding a full date fills the date key with it. One holding a date and time fills it with the date in UTC, a time that states no offset being read as UTC. One giving only a year, or a year and month, maps to nothing.
- `type` is filled only by a value that is one of the twelve terms of §3.5.

### 4.4 Rules for every value

- A value is trimmed of leading and trailing whitespace. A value that is then empty maps to nothing, and a key with nothing mapped to it is left absent, never written as an empty string or an empty array.
- A value that would not satisfy §5 for its key maps to nothing; the rest of the file is still read.
- A repeatable key keeps the first occurrence of a value and drops later exact duplicates.

## 5. Conformance

A container conforms to this version when its `[core]` table satisfies FRAMEWORK §3 and §5 and each of the following, where the key is present:

1. Every attribution key (§3.1) is a non-empty array of tables, each with a non-empty string `name`, and each of its other §3.1 keys present is a string.
2. Every repeatable-text key (§3.2) is a non-empty array of non-empty strings.
3. Every single-text key (§3.3) is a non-empty string.
4. Every date key (§3.4) is a TOML local date (CONVENTIONS §3).
5. `type` is one of the twelve values of §3.5.
6. `format` is a media type in the form of §3.6.
7. `language` is a non-empty array, and every entry is a well-formed BCP 47 tag (§3.7).
8. `license` is a non-empty array, and every entry is an absolute URI (§3.8).

Nothing in this section depends on anything but the flyleaf, and nothing in it depends on the content file: whether a title is accurate is not a conformance question.

## 6. Implementation requirements

Beyond FRAMEWORK §11, an implementation of this profile:

- MUST preserve keys in `[core]` it does not recognize, and the order of entries in every array it does not change;
- MUST NOT write an empty string, an empty array, or an attribution table without a `name`;
- MUST NOT replace a value in the table with one taken from the content file except at a person's request (§2.3);
- MUST, when it fills the table from a source, follow §4.

## 7. Security considerations

Every value in `[core]` is text written by whoever wrote the container, for a person to read. `uri`, `license`, and `identifier` entries are not fetched, opened, or resolved on the container's say-so: an implementation that offers to follow one does so only at a person's request (FRAMEWORK §12). FRAMEWORK §11's display rule applies to every string in the table. A name, a title, or an identifier can claim anything, and nothing in this profile verifies it.
