# Slipcase Profiles

How Slipcase containers are used for a purpose.

[Slipcase](https://github.com/excelano/slipcase) binds a file to a flyleaf describing it and assigns meaning to nothing in that flyleaf beyond two keys. A profile gives it meaning for one purpose: which keys a records-management tool reads, what a container is when a document is handed over, which additional members belong to whom. A flyleaf can carry several profiles at once, and a tool that understands one preserves the rest.

`FRAMEWORK.md` states what every profile has in common: the one top-level table a profile owns, how that table identifies itself, the one directory its members live under, how it is versioned, and what its specification has to say. `CONVENTIONS.md` defines the things every profile would otherwise define slightly differently: identifiers, agents, hashes, dates, and a log that shows when it has been edited. `DESIGN.md` records why each rule is drawn where it is.

Each official profile lives in its own directory, with its specification, its design document, and example files, and is versioned on its own:

| Profile | Table | Status |
|---|---|---|
| Slipcase Records Profile (`records/`) | `[records]` | draft: records (§2) written; schedules, holds, aggregations, register, records root to come |

A profile specified somewhere else is a profile all the same: the framework identifies a profile by its URI, under any origin.

## This repository

The framework, the conventions, and every official profile are dedicated to the public domain under [CC0 1.0](LICENSE), as Slipcase is. Anyone can implement a profile, or write one, without obligation to this project.

The Slipcase specification is not changed by anything here. Where a profile and Slipcase disagree, Slipcase wins and the profile is wrong.
