# ISL Glossary Platform - Thesis Prototype Plan

## Thesis-aligned purpose

The platform is an accessible and adaptable Irish Sign Language glossary prototype for organisation-specific or domain-specific deployment. It is intended as a staff-support and ISL awareness tool for everyday service contexts.

It should be described as a prototype, not as a national dictionary, formal ISL course, replacement for interpreters, full Deaf awareness programme, clinical guidance system, or commercial SaaS product.

The sample deployments cover college computing, retail customer service, and healthcare reception. Healthcare is included as a domain-specific access example, with content limited to everyday reception and appointment-support terms.

## Implemented model map

- `Organisation`: tenant-like grouping for all important content.
- `Category`: organisation-specific grouping of signs.
- `SignEntry`: official glossary content managed through Django admin.
- `Transcript`: optional text transcript linked to a sign for accessibility and search support.
- `FAQEntry`: organisation-specific support content for common questions.
- `StaffProfile`: connects a Django user to one organisation.
- `FavouriteSign`: lets staff save useful organisation signs.
- `SignRequest`: lets staff or visitors request missing signs without publishing official content.
- `PortalItem`: simple prototype staff/manager dashboard items such as tasks, appointments, calendar notes, and access notes.

## Implemented workflows

1. A visitor opens the list of available organisations.
2. A visitor opens an organisation-specific glossary.
3. A visitor browses categories, filters by first letter, or searches signs within that organisation.
4. A visitor views a sign entry with term, video URL, description, usage context, category, and optional transcript.
5. Staff log in through Django authentication.
6. Staff with an organisation profile are redirected after login to a basic organisation-specific portal dashboard.
7. The dashboard includes role/domain panels such as retail tasks, college calendar notes, healthcare reception checks, and manager to-dos.
8. Staff can favourite signs from their own organisation.
9. Staff can submit missing-sign requests for their own organisation.
10. Visitors can submit missing-sign requests with a contact email.
11. Managers and glossary managers review requests in a domain-specific dashboard.
12. Approved requests can then be handled through Django admin for interpreter/content review and official publication.
13. Official signs can be marked as published and can optionally include transcript and thumbnail metadata.

## Security/design notes

- Core content models link to `Organisation`.
- Staff-only workflows check the logged-in user's `StaffProfile`.
- Favourites and requests are scoped to the staff user's organisation.
- Staff users submit requests but cannot publish official `SignEntry` content through the public UI.
- Staff roles are represented on `StaffProfile`: staff, manager, and glossary manager.
- Managers can triage requests, but they do not publish official signs through the portal.
- Django admin is treated as the interpreter/content back office for official sign publication.
- Sign entries include an official publication flag so prototype content can be distinguished from reviewed content.
- Transcripts support accessibility, but full captioned media hosting remains future work.
- Django CSRF protection and authentication middleware are enabled.

## Security-related design change

The prototype originally considered a broader organisation-admin dashboard for request review. This was refined for security and governance reasons: the public/staff portal now separates request triage from official content publication. Managers and glossary managers can approve, reject, or ask for clarification on requests, but they cannot publish official signs from the portal. Interpreter/content review and official sign creation remain in the Django admin back office.

This separation reduces the risk of unvalidated or unsafe sign content being published directly by service staff, which is especially important for sensitive domains such as healthcare reception.

## Future work

- Stronger production configuration for secrets, hosts, HTTPS, and deployment.
- Email notification when requested signs are reviewed.
- Audit logging for content changes and request decisions.
- Data import/export.
- Rich video embedding, captions, and media hosting.
- Broader accessibility testing with Deaf users and ISL stakeholders.
- Full multi-tenant SaaS operations.

## Thesis diagram sources

PlantUML source files are stored in `docs/diagrams/`:

- `use-case.puml`: system actors and main use cases.
- `erd.puml`: implemented Django data model.
- `request-workflow.puml`: sign request triage and publication workflow.
- `project-structure.puml`: server-rendered Django prototype structure.
