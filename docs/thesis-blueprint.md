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

Organisation -> Categories -> Sign entries -> Video URLs / embeds -> Search and browse -> Staff login -> Staff dashboard -> Favourites -> Visitor/staff sign requests -> Organisation admin review -> Django admin content management

## Django Models

- `Organisation`
- `Category`
- `SignEntry`
- `FAQEntry`
- `StaffProfile`
- `FavouriteSign`
- `SignRequest`

## Key Workflows

1. A user opens an organisation-specific glossary.
2. They browse categories or search for a sign.
3. They view a sign entry with an English term, ISL video URL, description, usage context and category.
4. Staff can log in.
5. Staff can favourite useful signs from their own organisation.
6. Staff can use a basic dashboard with favourites, recent signs, request history, and portal-style placeholder panels.
7. Staff can submit missing-sign requests.
8. Visitors can submit simpler missing-sign requests with a contact email.
9. Organisation admins can review request statuses in an organisation-specific dashboard.
10. Django admin is used for official content management.

## Security and Design Principles

- Important content models link to an `Organisation`.
- Staff-only workflows check the logged-in user's `StaffProfile`.
- Staff access is scoped to their profile's organisation.
- Staff do not directly publish official signs through the public UI.
- Organisation admins are staff profiles with an added admin flag, not a full SaaS tenant-admin system.
- Sign requests use statuses: Pending, Approved, Rejected, Needs clarification.
- Django authentication and CSRF protection are used.

## Future Work

Keep the following out of the core prototype unless explicitly implemented later:

- production security hardening
- audit logging
- data export
- billing
- full multi-tenant SaaS administration
- production deployment automation

## Thesis Consistency Rule

Only implement and document what the prototype actually supports. If a feature is partial, mark it as partial or future work in the thesis.
