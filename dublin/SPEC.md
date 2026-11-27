# Slipcase Dublin Profile — Specification

**Version:** 1.0  
**Status:** draft  
**Framework:** 1.0 · **Conventions:** 1.0 · **Slipcase:** 1.1

The Dublin Profile describes the resource a Slipcase container holds, in fifteen elements: what it is called, who made it, what it is about, when, in what language, and under what rights. It describes and does nothing more. No value in it drives an action, and no value is interpreted.

## 1. Identity and terminology

The key words **MUST**, **MUST NOT**, and **MAY** are to be interpreted as described in BCP 14 when, and only when, they appear in capitals. **FRAMEWORK**, **CONVENTIONS**, and **SPEC** cite the profiles framework, the shared conventions, and the Slipcase specification.

| | |
|---|---|
| Name | Slipcase Dublin Profile |
| `profile` | `https://slipcaseformat.org/profiles/dublin` |
| Profile table | `[dublin]` |
| Profile prefix | `dublin/` |
| Kinds | `resource` |
| Conventions used | none |

**Resource** — what a `[dublin]` table describes: the content file, or what the content file stands for.  
**Element** — one of the fifteen keys of §2.2.

## 2. Resources

A container of kind `resource` carries a description of its resource in the `[dublin]` table. The content file is the resource, or stands for it, and this profile places no requirement on it.

### 2.1 Example

```toml
slipcase_version = "1.1"

[content]
file = "survey-report.txt"

[dublin]
profile = "https://slipcaseformat.org/profiles/dublin"
profile_version = "1.0"
kind = "resource"
title = ["Survey of the North Field"]
creator = ["A. Marsh", "Field Office 3"]
subject = ["drainage", "soil survey"]
date = ["2024-05-02"]
language = ["en"]
rights = ["Copyright 2024 Field Office 3. All rights reserved."]
```

### 2.2 Keys

The `[dublin]` table MUST contain the three framework keys (FRAMEWORK §3), with `kind = "resource"`, and MAY contain any of these elements. Each element's type is an array of strings (§2.3).

| Element | Key | Definition |
|---|---|---|
| Title | `title` | A name given to the resource. |
| Creator | `creator` | An entity primarily responsible for making the resource. |
| Subject | `subject` | The topic of the resource. |
| Description | `description` | An account of the resource. |
| Publisher | `publisher` | An entity responsible for making the resource available. |
| Contributor | `contributor` | An entity responsible for making contributions to the resource. |
| Date | `date` | A point or period of time associated with an event in the resource's lifecycle. |
| Type | `type` | The nature or genre of the resource. |
| Format | `format` | The file format, physical medium, or dimensions of the resource. |
| Identifier | `identifier` | An unambiguous reference to the resource within a given context. |
| Source | `source` | A related resource from which the described resource is derived. |
| Language | `language` | The language of the resource. |
| Relation | `relation` | A related resource. |
| Coverage | `coverage` | The spatial or temporal topic of the resource, spatial applicability, or jurisdiction. |
| Rights | `rights` | Information about rights held in and over the resource. |

Every element is optional. An absent element states nothing about the resource, and a table carrying no element is conformant.

### 2.3 Values

An element that is present MUST be an array of one or more items, and every item MUST be a non-empty string. A bare string, an empty array, an empty string, and an item of any other TOML type (a date, an integer, a table) are non-conformant.

Every value is text, as the writer states it. This profile assigns no vocabulary, syntax, or format to any element, and an implementation MUST NOT refuse or alter a value for its form beyond the rule above.

- `date` is text. It is not a date or an instant as CONVENTIONS §3 defines them, since a value can name a period, and this profile defines no form of its own for it.
- `identifier` is text. It is not an identifier as CONVENTIONS §1 defines one.

The items of an element are kept in the order written. The order has no meaning under this profile.

### 2.4 Other keys and members

Keys the table carries that §2.2 does not define are permitted and MUST be preserved (FRAMEWORK §3).

This profile defines no members. Members under `dublin/` have no meaning under this version, and an implementation MUST preserve them.

## 3. Conformance

A container conforms to this version of the profile when it is a conformant Slipcase container and its `[dublin]` table:

1. carries `profile = "https://slipcaseformat.org/profiles/dublin"` and `profile_version = "1.0"`, under the table name `dublin`;
2. carries `kind = "resource"`;
3. holds, for every element present, an array of one or more non-empty strings.

Nothing else about the table or the container bears on conformance to this profile.

## 4. Implementation requirements

Beyond FRAMEWORK §11, an implementation of this profile:

- MUST read and write every element value as text, and MUST NOT normalize, translate, or validate a value beyond §2.3;
- MUST, when it rewrites the table, preserve every item of every element it does not change, in the order written;
- MUST apply the display rule of FRAMEWORK §11 to every element value.

## 5. Security considerations

Every value is a claim by whoever wrote the container, and nothing in this profile verifies one. A `creator` or a `rights` statement is what the writer said, not evidence of authorship or of a license, and an implementation that presents a value presents it as that.

`identifier`, `source`, `relation`, and `rights` can hold text that reads as an address or a path. An implementation MUST NOT fetch, open, or follow a value without its own decision to do so (FRAMEWORK §12), and MUST NOT treat any value as a command.

No value has a length limit under this profile. An implementation bounds what it spends reading and displaying values, as SPEC §6 requires for the flyleaf.
