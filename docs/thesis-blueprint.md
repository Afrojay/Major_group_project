# ISL Glossary Platform - Thesis Blueprint

This Django prototype should match the thesis direction for Chapters 1-5.

## Core Concept

The project is an accessible and adaptable Irish Sign Language glossary platform for organisation-specific or domain-specific deployment.

It is both:

- an organisation-specific staff-support tool
- a practical ISL awareness and accessibility tool

It helps hearing staff become more familiar with common ISL signs and Deaf communication needs in everyday service contexts.

Example domains in the prototype can include college computing, retail customer service, and healthcare reception. Healthcare examples should remain limited to everyday access and appointment-support vocabulary rather than clinical advice.

It is not:

- a complete national ISL dictionary
- a replacement for qualified ISL interpreters
- a full ISL course
- formal Deaf awareness training
- medical advice or clinical communication guidance
- a complete commercial SaaS product

## Prototype Feature Blueprint

Organisation -> Categories -> Sign entries -> Video URLs / embeds -> Search and browse -> Staff login -> Staff dashboard -> Favourites -> Visitor/staff sign requests -> Manager review -> Interpreter/content review -> Django admin content management

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

## Key Workflows

1. A user opens an organisation-specific glossary.
2. They browse categories, use A-Z filtering, or search for a sign.
3. They view a sign entry with an English term, ISL video URL, description, usage context and category.
4. Staff can log in.
5. Staff can favourite useful signs from their own organisation.
6. Staff can use a basic organisation-specific dashboard with favourites, recent signs, request history, role/domain placeholder panels, and relevant manager actions.
7. Staff can submit missing-sign requests.
8. Visitors can submit simpler missing-sign requests with a contact email.
9. Managers and glossary managers can review requests in an organisation-specific dashboard.
10. Manager-approved requests can be passed to interpreter/content review.
11. Django admin is used for official content management and publication.
12. Sign entries can include optional transcript and thumbnail metadata to support accessibility and browsing.
13. Staff and managers can use simple dashboard items for prototype tasks, appointments, calendar events and access notes.

## Security and Design Principles

- Important content models link to an `Organisation`.
- Organisation records support basic database-driven branding through theme colour, logo URL, description and contact email. This supports organisation-specific deployment while keeping advanced branding as future work.
- Staff-only workflows check the logged-in user's `StaffProfile`.
- Staff access is scoped to their profile's organisation.
- Staff do not directly publish official signs through the public UI.
- Staff profiles use simple role types: Staff, Manager, and Glossary manager.
- Managers can approve requests for interpreter/content review, but they do not publish official signs through the portal.
- Sign requests use statuses: Pending manager review, Needs clarification, Manager approved, Sent to interpreter, Completed, Rejected.
- Sign entries include an official publication flag so unreviewed prototype content can be identified.
- Django authentication and CSRF protection are used.

## Security-Related Workflow Refinement

The request review workflow was deliberately changed from a broad organisation-admin concept to a safer role-based process. Managers and glossary managers review whether a request is suitable to progress, while interpreter/content review and official publication remain in Django admin.

This supports a clearer separation of duties:

- staff and visitors can request missing signs
- managers can triage requests
- interpreter/content reviewers can handle official glossary publication

The change reduces the risk of unvalidated sign content being published directly through the staff portal.

## Future Work

Keep the following out of the core prototype unless explicitly implemented later:

- production security hardening
- audit logging
- data export
- billing
- full multi-tenant SaaS administration
- production deployment automation
- full video hosting, captions, and automated email notifications

## Thesis Consistency Rule

Only implement and document what the prototype actually supports. If a feature is partial, mark it as partial or future work in the thesis.
