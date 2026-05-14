# Content Review Workflow Notes

## Design Reference

The Signbank paper was useful background because it shows how a sign-language dictionary can combine search, video, tags, feedback and editor workflows. My project is much smaller than Signbank, and it should stay that way. The aim here is an organisation-specific glossary workflow, not a full linguistic dictionary.

That distinction matters. A full dictionary might need fields for linguistic analysis, variant signs, corpus evidence and regional differences. This prototype only needs enough structure to support local staff use and a basic content review process.

## Design Rationale

The content workflow separates four concerns:

- public/staff glossary use
- organisation-manager triage of requests
- glossary editor review of signs, videos, descriptions, categories and tags
- platform administration through Django admin

The split may seem slightly formal for a small prototype, but it solves a real problem. A staff member may notice that a video link is broken. A manager may know that a requested term is useful in their workplace. Neither of those people should automatically be treated as the person who can verify ISL content.

## Requests and Reports

`SignRequest` handles both missing-sign requests and reports about existing signs.

Supported request/report types include:

- missing sign
- incorrect sign/video
- unclear description
- wrong category
- possible duplicate
- broken video link
- other

Missing signs start with organisation-manager triage. Reports about existing signs go directly to the glossary editor queue, because they are already about published or draft content that needs checking.

## Sign Workflow Fields

`SignEntry` includes two simple workflow fields:

- publication status: draft, needs video, needs review, published, archived
- video review status: unchecked, candidate video, approved for prototype, broken link, needs replacement

This is not as detailed as a professional dictionary workflow, but it gives enough structure to show that signs do not move straight from request to publication without review.

`SignEntryChangeLog` records which fields changed, who edited the sign and when. It is intentionally simple. A production system might store before/after values or use a stronger audit logging package, but that would be beyond the scope of this prototype.

## Visibility Rules

Public users and ordinary staff only see published signs.

Organisation managers and glossary editors can see draft or review-needed signs for their own organisation. Managers can understand what is in progress, but glossary editors are the ones who can edit sign content.

## Evaluation Note

The workflow makes the project feel less like a basic CRUD glossary. A realistic path might look like this:

1. A visitor reports that the `Deadline` video link is broken.
2. The report appears in the glossary editor dashboard.
3. The glossary editor opens the sign, checks the video URL, updates the video status and saves the change.
4. A change log entry records the edit.

That is still a small workflow, but it is enough to show request handling, role separation and content review without pretending the system is a complete ISL dictionary platform.
