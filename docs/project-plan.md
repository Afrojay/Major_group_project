# ISL Glossary Platform - Prototype Plan

## Purpose

The platform is an adaptable Irish Sign Language glossary prototype for organisation-specific use. I am treating it as a staff-support and accessibility tool rather than a complete dictionary.

That boundary is important. A real ISL dictionary needs much more linguistic detail and proper expert review. This prototype focuses on a smaller question: could an organisation maintain a local glossary of useful signs for its own staff?

The sample deployments are:

- College Computing Department
- Retail Customer Service
- Healthcare Reception

The healthcare example is limited to reception and appointment-support vocabulary. It should not be read as clinical guidance.

## Model Map

- `Organisation`: the local deployment context.
- `Category`: groups signs inside one organisation.
- `SignEntry`: a glossary term with description, context, tags, video URL and workflow status.
- `SignEntryChangeLog`: records simple edit history for signs.
- `Transcript`: optional text transcript linked to a sign.
- `FAQEntry`: short organisation-specific support content.
- `StaffProfile`: connects a Django user to one organisation and role.
- `FavouriteSign`: saved signs for staff.
- `SignRequest`: missing-sign requests and reports about existing signs.
- `PortalItem`: small dashboard items such as tasks, appointments and notes.

## Main Workflows

1. A visitor opens the organisation list.
2. They choose an organisation, such as College Computing.
3. They browse categories, search signs, or filter by first letter.
4. They open a sign detail page.
5. Staff can log in and are redirected to their own organisation dashboard.
6. Staff can favourite signs.
7. Staff or visitors can request a missing sign.
8. Staff or visitors can report an issue with an existing sign.
9. Organisation managers triage missing-sign requests.
10. Glossary editors review approved requests and direct sign reports.
11. Glossary editors can edit sign definitions, tags, video details and workflow statuses.
12. Sign edits create a simple change log.

This is a modest workflow, but it shows the difference between using the glossary and managing its content.

## Security and Design Notes

- Core content is linked to `Organisation`.
- Staff-only pages check the user's `StaffProfile`.
- Favourites, requests and reports are organisation-scoped.
- Staff and organisation managers cannot publish signs.
- Glossary editors edit signs through the application, not Django admin.
- Django admin is reserved for the platform admin.
- CSRF protection and Django authentication are used.

The role split may seem a little strict for a small prototype, but it makes sense for sign-language content. A manager can decide whether a request is relevant to their organisation, while a glossary editor or ISL reviewer should check the actual content.

## Future Work

Items deliberately left outside the core prototype:

- production deployment settings
- email notifications
- stronger audit logging
- import/export tools
- proper video hosting and captions
- broader accessibility testing with Deaf users and ISL stakeholders
- full multi-tenant SaaS administration

## Diagram Sources

PlantUML source files are stored in `docs/diagrams/`:

- `use-case.puml`: actors and main use cases
- `erd.puml`: implemented Django data model
- `request-workflow.puml`: request/report review workflow
- `project-structure.puml`: Django project structure
