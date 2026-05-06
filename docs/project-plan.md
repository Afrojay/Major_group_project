# ISL Glossary Platform - Thesis Prototype Plan

## Thesis-aligned purpose

The platform is an accessible and adaptable Irish Sign Language glossary prototype for organisation-specific or domain-specific deployment. It is intended as a staff-support and ISL awareness tool for everyday service contexts.

It should be described as a prototype, not as a national dictionary, formal ISL course, replacement for interpreters, full Deaf awareness programme, clinical guidance system, or commercial SaaS product.

The sample deployments cover college computing, retail customer service, and healthcare reception. Healthcare is included as a domain-specific access example, with content limited to everyday reception and appointment-support terms.

## Implemented model map

- `Organisation`: tenant-like grouping for all important content.
- `Category`: organisation-specific grouping of signs.
- `SignEntry`: official glossary content managed through Django admin.
- `FAQEntry`: organisation-specific support content for common questions.
- `StaffProfile`: connects a Django user to one organisation.
- `FavouriteSign`: lets staff save useful organisation signs.
- `SignRequest`: lets staff or visitors request missing signs without publishing official content.

## Implemented workflows

1. A visitor opens the list of available organisations.
2. A visitor opens an organisation-specific glossary.
3. A visitor browses categories or searches signs within that organisation.
4. A visitor views a sign entry with term, video URL, description, usage context, and category.
5. Staff log in through Django authentication.
6. Staff with an organisation profile can use a basic portal-style dashboard.
7. Staff can favourite signs from their own organisation.
8. Staff can submit missing-sign requests for their own organisation.
9. Visitors can submit missing-sign requests with a contact email.
10. Organisation admins review request statuses in a domain-specific dashboard.
11. Admin users manage official content through Django admin.

## Security/design notes

- Core content models link to `Organisation`.
- Staff-only workflows check the logged-in user's `StaffProfile`.
- Favourites and requests are scoped to the staff user's organisation.
- Staff users submit requests but cannot publish official `SignEntry` content through the public UI.
- Organisation admin users are represented by a flag on `StaffProfile`.
- Sign request review is represented through admin-managed statuses.
- Django CSRF protection and authentication middleware are enabled.

## Future work

- Stronger production configuration for secrets, hosts, HTTPS, and deployment.
- Per-organisation admin dashboards outside Django admin.
- Email notification when requested signs are reviewed.
- Audit logging for content changes and request decisions.
- Data import/export.
- Rich video embedding and media hosting.
- Broader accessibility testing with Deaf users and ISL stakeholders.
- Full multi-tenant SaaS operations.
