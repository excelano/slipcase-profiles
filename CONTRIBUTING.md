# Contributing

This repository holds specifications. Most of what it needs is not code.

## Contributions are dedicated to the public domain

Everything here is dedicated to the public domain under [CC0 1.0](LICENSE). By contributing you dedicate your contribution on the same terms, waiving copyright and related rights in it to the extent possible under law. Nothing can be accepted on any other basis: a profile anyone may implement, quote, fork, or embed cannot carry a part that they may not.

## What is most useful

A question a document cannot answer. Two implementations of one profile disagreeing about the same container is the clearest form of this, and the most valuable thing to report. A case a specification leaves open is a specification bug, not a matter of opinion about what an implementation should do.

Open an issue, naming the document and section.

## Security

Do not open a public issue for a security defect. Use **Report a vulnerability** under the Security tab, which reaches the maintainers privately.

For a specification the plausible defects are in the rules: a value a profile lets a container state that an implementation then acts on without checking, or an ambiguity in a convention that lets two readers hash the same log differently.

## A rule and its reasoning travel together

`FRAMEWORK.md` and `CONVENTIONS.md` state the rules; `DESIGN.md` says why. Each profile's directory has the same pair. A change to a rule needs the matching change to the reasoning in the same commit, or the reasoning behind a rule ends up written down nowhere.

## Versions

The framework and the conventions are versioned together; each profile is versioned on its own. A version's rules follow FRAMEWORK §6, which is Slipcase's §2.4 applied to profiles: while a version is a draft, changes land without moving the number; once it is final, a change to what counts as a conformant container moves the number, and an editorial change does not.

Example files are not normative. Where an example and a specification disagree, the specification wins and the example is a bug.
