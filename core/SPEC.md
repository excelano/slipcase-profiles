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
| Conventions used | dates and instants |

**Resource** — the content file the container holds, which the `[core]` table describes. DCMI calls the thing described a resource, and the kind takes its name.

**DCMI term** — a property of the DCMI Metadata Terms, identified by a URI of the form `http://purl.org/dc/terms/<name>`. Each key in §2.2 names the term it is, and DCMI's definition is the authority on what the term means. The definitions below are summaries for a reader of this document.

**Source** — metadata a content file already carries in its own format: Office document properties, OpenDocument metadata, a PDF's document information or an XMP packet (§4).

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
lei = "5493001KJTIIGC8Y1R12"

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
| `creator` | `http://purl.org/dc/terms/creator` | attribution | Who is primarily responsible for making it. |
| `contributor` | `http://purl.org/dc/terms/contributor` | attribution | Who contributed to it. |
| `publisher` | `http://purl.org/dc/terms/publisher` | attribution | Who made it available. |
| `rightsHolder` | `http://purl.org/dc/terms/rightsHolder` | attribution | Who owns or manages rights over it. |
| `subject` | `http://purl.org/dc/terms/subject` | repeatable text | Its topics: keywords, key phrases, or classification codes. |
| `identifier` | `http://purl.org/dc/terms/identifier` | repeatable text | Unambiguous references to it in some context: a document number, an ISBN, a DOI, a URI. |
| `source` | `http://purl.org/dc/terms/source` | repeatable text | Resources it is derived from. |
| `relation` | `http://purl.org/dc/terms/relation` | repeatable text | Related resources. |
| `isPartOf` | `http://purl.org/dc/terms/isPartOf` | repeatable text | Resources it is physically or logically included in. |
| `coverage` | `http://purl.org/dc/terms/coverage` | repeatable text | Its spatial or temporal topic, or the jurisdiction it applies to. |
| `rights` | `http://purl.org/dc/terms/rights` | repeatable text | Statements about rights held in and over it. |
| `language` | `http://purl.org/dc/terms/language` | language (§3.7) | The languages of its content. |
| `license` | `http://purl.org/dc/terms/license` | license (§3.8) | Legal documents giving permission to do something with it. |
| `type` | `http://purl.org/dc/terms/type` | type (§3.5) | Its nature or genre. |
| `format` | `http://purl.org/dc/terms/format` | format (§3.6) | Its file format. |
| `date` | `http://purl.org/dc/terms/date` | date (§3.4) | A date associated with an event in its life cycle, where none of the three below is meant. |
| `created` | `http://purl.org/dc/terms/created` | date | When it was created. |
| `modified` | `http://purl.org/dc/terms/modified` | date | When it was last changed. |
| `issued` | `http://purl.org/dc/terms/issued` | date | When it was formally issued or published. |

Key names are DCMI's own, case included, so that `rightsHolder` here is `rightsHolder` in every DCMI serialization. Keys this section does not define are permitted in the table and MUST be preserved (FRAMEWORK §3). A later version of this profile may add DCMI terms; it never adds a key that is not one.

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

`subject`, `identifier`, `source`, `relation`, `isPartOf`, `coverage`, and `rights` are arrays of strings. A single value is an array of one: a bare string is non-conformant, so a reader has one shape to handle. No entry is an empty string.

### 3.3 Single text

`title`, `alternative`, and `description` are strings, non-empty. Dublin Core allows a term to repeat; this profile does not repeat these three, because every source in §4 carries one of each.

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

An implementation that fills `[core]` from metadata the content file already carries MUST map it as this section states, so that two implementations reading the same file write the same table. An implementation MAY fill some keys and not others; a key it fills, it fills this way. A person writing the table by hand is not bound by this section.

### 4.1 Office Open XML

The core properties part (`docProps/core.xml` in a Word, Excel, or PowerPoint file):

| Source | Key | |
|---|---|---|
| `dc:title` | `title` | |
| `dc:subject` | `subject` | First entry. Office's Subject field is a topic phrase. |
| `cp:keywords` | `subject` | Further entries: the value split on `;` and `,`, each part trimmed, empty parts dropped. |
| `dc:creator` | `creator` | One attribution table (§4.5). |
| `dc:description` | `description` | |
| `dc:language` | `language` | One entry. |
| `dc:identifier` | `identifier` | One entry. |
| `dcterms:created` | `created` | §4.5 for an instant. |
| `dcterms:modified` | `modified` | §4.5 for an instant. |

`cp:lastModifiedBy`, `cp:revision`, `cp:category`, `cp:contentStatus`, `cp:lastPrinted`, and `cp:version` are not Dublin Core and map to nothing.

### 4.2 OpenDocument

The metadata of an OpenDocument file (`meta.xml`):

| Source | Key | |
|---|---|---|
| `dc:title` | `title` | |
| `dc:description` | `description` | |
| `dc:subject` | `subject` | First entry. |
| `meta:keyword` | `subject` | Further entries, one per element, in document order. |
| `meta:initial-creator` | `creator` | One attribution table (§4.5). |
| `meta:creation-date` | `created` | §4.5 for an instant. |
| `dc:date` | `modified` | §4.5 for an instant. |
| `dc:language` | `language` | One entry. |

OpenDocument's `dc:creator` names whoever last modified the file, not its author, and maps to nothing; `meta:initial-creator` is the author. `meta:generator` maps to nothing.

### 4.3 PDF document information

The document information dictionary of a PDF:

| Source | Key | |
|---|---|---|
| `/Title` | `title` | |
| `/Author` | `creator` | One attribution table (§4.5). |
| `/Subject` | `description` | A PDF's Subject is a sentence about the document, not a topic. |
| `/Keywords` | `subject` | The value split on `;` and `,`, each part trimmed, empty parts dropped. |
| `/CreationDate` | `created` | §4.5 for an instant. |
| `/ModDate` | `modified` | §4.5 for an instant. |

`/Creator` names the application that made the original document and `/Producer` the one that wrote the PDF; neither maps.

### 4.4 XMP

An XMP packet: a PDF's metadata stream, or the metadata embedded in an image.

| Source | Key | |
|---|---|---|
| `dc:title` | `title` | The `x-default` alternative, else the first. |
| `dc:creator` | `creator` | One attribution table per sequence item, in order. |
| `dc:description` | `description` | The `x-default` alternative, else the first. |
| `dc:subject` | `subject` | One entry per bag item. |
| `dc:rights` | `rights` | One entry: the `x-default` alternative, else the first. |
| `dc:format` | `format` | |
| `dc:language` | `language` | One entry per bag item. |
| `xmp:CreateDate` | `created` | §4.5 for an instant. |
| `xmp:ModifyDate` | `modified` | §4.5 for an instant. |
| `xmpRights:WebStatement` | `license` | One entry, when the value is an absolute URI. |

Where a PDF carries both an XMP packet and a document information dictionary, they are combined key by key: each key takes the XMP value where XMP yields one, and the dictionary's where it does not.

### 4.5 Rules for every source

- A value is trimmed of leading and trailing whitespace. A value that is then empty maps to nothing, and a key with nothing mapped to it is left absent, never written as an empty string or an empty array.
- An author string becomes one attribution table whose `name` is the string, whatever separators it contains: `Doe, J.; Roe, R.` is one name. Only the keyword fields of §4.1 and §4.3 are split. A source never yields an `email`, `uri`, `orcid`, or `lei` the file does not state as one.
- An instant becomes its date in UTC. A timestamp that states no offset is read as UTC. A date that gives only a year or a year and month maps to nothing, since a date key holds a whole day.
- Subject entries keep their first occurrence and drop later exact duplicates.
- `format`, where the source does not state it, is the content file's media type as the implementation determines it, or absent.

## 5. Conformance

A container conforms to this version when its `[core]` table satisfies FRAMEWORK §3 and §5 and each of the following, where the key is present:

1. Every attribution key (§3.1) is an array of tables, each with a non-empty string `name`, and each of its other §3.1 keys present is a string.
2. Every repeatable-text key (§3.2) is an array of non-empty strings.
3. Every single-text key (§3.3) is a non-empty string.
4. Every date key (§3.4) is a TOML local date (CONVENTIONS §3).
5. `type` is one of the twelve values of §3.5.
6. `format` is a media type in the form of §3.6.
7. Every `language` entry is a well-formed BCP 47 tag, in an array (§3.7).
8. Every `license` entry is an absolute URI, in an array (§3.8).

Nothing in this section depends on anything but the flyleaf, and nothing in it depends on the content file: whether a title is accurate is not a conformance question.

## 6. Implementation requirements

Beyond FRAMEWORK §11, an implementation of this profile:

- MUST preserve keys in `[core]` it does not recognize, and the order of entries in every array it does not change;
- MUST NOT write an empty string, an empty array, or an attribution table without a `name`;
- MUST, when it fills the table from a source, follow §4.

## 7. Security considerations

Every value in `[core]` is text written by whoever wrote the container, for a person to read. `uri`, `license`, and `identifier` entries are not fetched, opened, or resolved on the container's say-so: an implementation that offers to follow one does so only at a person's request (FRAMEWORK §12). FRAMEWORK §11's display rule applies to every string in the table. A name, a title, or an identifier can claim anything, and nothing in this profile verifies it.
