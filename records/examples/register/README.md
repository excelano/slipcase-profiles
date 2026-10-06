# A register in directory form

Batch 000001 is final; batch 000002 is an unfinished intent with no journal yet, as a register looks when a run has claimed its sequence and not yet touched a record, or died before it did. Each `.slpc` here is a directory holding the container's members, to be packed by a reader that wants a real container. `tools/verify-register.py` walks it as SPEC 6.6 says and reports the chain intact and 000002 unfinished.
