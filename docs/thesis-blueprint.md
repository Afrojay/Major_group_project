# ISL Glossary Platform - Thesis Blueprint

These notes are intended to keep the implementation aligned with the thesis chapters. They are not a replacement for the thesis text, but they give the main argument in plain language.

## Core Idea

The project is an organisation-specific Irish Sign Language glossary platform. It is meant to support staff in everyday service situations, for example a computing help desk, a shop counter, or a reception desk.

It is both:

- a local staff-support tool
- a small accessibility and ISL-awareness prototype

It is not:

- a national ISL dictionary
- a replacement for qualified interpreters
- an ISL course
- formal Deaf awareness training
- medical or clinical communication guidance
- a commercial SaaS system

This boundary is worth repeating in the thesis, because it keeps the project realistic.

## Feature Flow

The main flow is:

Organisation -> Categories -> Sign entries -> Video URLs -> Search and browse -> Staff login -> Favourites -> Requests/reports -> Manager triage -> Glossary editor review -> Sign edit page -> Change log -> Platform admin

The flow may look long, but each step is fairly small. The point is to show how glossary content can move from use, to feedback, to review.

## Django Models

- `Organisation`
- `Category`
- `SignEntry`
- `Transcript`
- `FAQEntry`
- `StaffProfile`
- `FavouriteSign`
- `SignRequest`
- `PortalItem`
- `SignEntryChangeLog`

## Key Workflows

1. A user opens an organisation glossary.
2. They search, browse categories, or filter signs A-Z.
3. They view a sign with term, category, description, usage context and video reference.
4. Staff can log in.
5. Staff can favourite useful signs.
6. Staff can submit missing-sign requests.
7. Visitors can submit requests with contact details.
8. Users can report issues on existing signs.
9. Organisation managers triage missing-sign requests.
10. Glossary editors review content and edit signs.
11. Sign edits are recorded in a simple change log.
12. Platform admin uses Django admin for platform-level management.

## Security and Design Principles

- Important models link back to `Organisation`.
- Staff access is checked through `StaffProfile`.
- Ordinary staff only see published signs.
- Organisation managers can triage requests but cannot publish signs.
- Glossary editors can edit signs for their own organisation.
- Django admin is reserved for the platform admin.
- Django authentication and CSRF protection are used.

## Workflow Refinement

The design moved away from a broad "organisation admin" idea. That earlier approach made too many users feel like managers or administrators. The current version separates the roles more clearly:

- staff and visitors request or report signs
- organisation managers decide whether missing-sign requests are relevant
- glossary editors review and edit content
- platform admin manages the overall system

This appears to be a safer design for sign-language content. It acknowledges that organisational relevance and ISL correctness are related, but not the same thing.

## Future Work

These should remain future work unless implemented later:

- production security hardening
- richer audit logging
- data export
- billing or SaaS features
- deployment automation
- full video hosting and captions
- email notifications
- wider testing with Deaf users and ISL stakeholders

## Consistency Rule

Only document features that the prototype actually supports. If something is partial, it should be described as partial or future work rather than presented as complete.
