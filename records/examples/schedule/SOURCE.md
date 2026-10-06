# The NARA fixture

`grs-transmittal36.csv` is the General Records Schedules in NARA's machine-implementable format, Transmittal 36 (August 2024), fetched unchanged on 2026-10-06 from <https://www.archives.gov/files/records-mgmt/grs/grs-csv-transmittal36.csv>. SHA-256 `7124c4e887f5b55398a7903ebf0dae28b7722b80066d39c65e304a2d66f23547`.

It is a work of the United States Government and in the public domain. It is here because SPEC §3.1 requires that it load with no mapping and no error, and a copy that cannot change is the only way to make that requirement a test.

What the file contains that a reader has to accept: a byte order mark; CRLF line endings; fourteen trailing columns with empty names; thirteen quoted fields holding line breaks; the column `Retention (Years)` where NARA's own FAQ says `Retention`; `Event_Age` and `Creation_Age` where the FAQ says `Event_age` and `Creation_age`; a value `Final action ` with a trailing space; `N/A`, `NA`, and `[Variable]` for not stated; retention values `4-7`, `72h`, and `[Variable]`; four rows with `Disposition` `N/A`, each naming a successor in `Superseded by`; and named events (`Submission`, `End of service`) beside the four general ones.
