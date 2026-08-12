# Scholarship sources

The app uses public, attributable scholarship pages rather than scraping
commercial scholarship platforms or relying on unavailable third-party APIs.

## Launch sourcing policy

Intellible imports opportunities only when the publisher is one of the
following:

- the scholarship funder or foundation itself;
- a government higher-education agency;
- an accredited college or university publishing its own award information; or
- a professional association publishing its own program rules.

We do **not** copy entries from commercial scholarship-search sites, paid
directories, account-only tools, or search pages whose terms do not expressly
allow reuse. A free-to-use search site is not automatically a reusable data
source.

For every record, the reviewer records the publisher, official source URL,
official application URL, review date, and a concise factual summary of the
published requirements. We link students to the official page rather than
republishing full source text. If an award is not currently open, lacks a
verifiable application page, or has unclear ownership, it stays out of the
live catalogue.

The first expansion target is 100 additional, individually reviewed entries.
They will be added in small source-backed batches and will not be counted until
their eligibility and official application links have been verified.

## Free launch catalogue

- **Reviewed scholarship sources:** University of Arizona Scholarship Universe,
  Kent State ScholarshipUniverse, and University of Cincinnati scholarships.
  Records from these official pages can be imported after review.
- **Local-discovery directory:** Council on Foundations Community Foundation
  Locator. Use it to find a local foundation, then import only details verified
  on that foundation's own scholarship page.
- **Institution enrichment:** College Scorecard. Its public data can enrich a
  university profile with institution and financial-aid context, but it is not
  an individual-scholarship database.

## State coverage plan

We add sources in groups of ten states. Every state receives at least one
official university or state-administered scholarship source before additional
sources are added to the largest states.

**Coverage batch 1:** California, Texas, Florida, New York, Pennsylvania,
Illinois, Ohio, Georgia, North Carolina, and Michigan. The catalogue contains
one official major-university scholarship source for each of these states.

**Coverage batch 2:** New Jersey, Virginia, Washington, Arizona, Tennessee,
Massachusetts, Indiana, Maryland, Missouri, and Wisconsin. The catalogue
contains one official major-university scholarship source for each of these
states.

**Coverage batch 3:** Colorado, Minnesota, South Carolina, Alabama, Louisiana,
Kentucky, Oregon, Oklahoma, Connecticut, and Utah. The catalogue contains one
official major-university scholarship source for each of these states.

**Coverage batch 4:** Iowa, Nevada, Arkansas, Mississippi, Kansas, New Mexico,
Nebraska, Idaho, West Virginia, and Hawaii. The catalogue contains one official
major-university scholarship source for each of these states.

**Coverage batch 5:** New Hampshire, Maine, Montana, Rhode Island, Delaware,
South Dakota, North Dakota, Alaska, Vermont, and Wyoming. The catalogue now
has a baseline official major-university scholarship source for all 50 states.

The API exposes these through `GET /ingestion/sources`. Each source is marked
`reviewed_manual`: a team member checks a listing on the original page, then
submits it with `POST /ingestion/scholarships` or in a group with
`POST /ingestion/scholarships/batch`. `discovery_only` and
`enrichment_only` sources are never treated as active scholarship listings.

For every imported record, retain `source_name`, `source_url`, and
`application_url`. Add the source's published requirements in
`requirements_raw`, and only enter facts present on that page. This preserves
the provenance needed to verify deadlines and deactivate expired awards.

## Free/open databases

Many government datasets report historical recipients or financial-aid
statistics rather than current opportunities. They are useful for research,
coverage analysis, or institution enrichment, but should not be imported as
active scholarship listings unless the dataset itself provides current award
details and an application link.

Before adding a database, confirm its licence or terms allow the intended use,
record its catalogue URL in `backend/app/sources/catalog.py`, and use the same
reviewed import process.

## Initial reviewed awards

`backend/data/reviewed_scholarships.json` holds the first curated import cohort:
one individually identified award or tuition-guarantee program for each of the
ten largest states. Every record has an official source URL, original eligibility
text, and verification timestamp. Run `python scripts/import_reviewed_scholarships.py`
from `backend` to add or refresh it. The importer is idempotent: it uses the
source name and source ID to refresh an existing record rather than duplicate it.
