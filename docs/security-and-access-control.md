# Security and Access Control Notes

## Prototype Security Scope

This is a local academic prototype, so the security work is mostly about design discipline rather than production hardening. It uses Django's built-in protections where possible, but it should not be presented as production-ready.

Implemented security-related features include:

- Django login and sessions
- CSRF protection on POST forms
- role checks in views
- organisation scoping for staff data
- model validation for cross-organisation relationships
- publication-status checks so ordinary users only see published signs

These features are enough to show the intended access-control model. They do not cover every risk a deployed public system would face.

## Role Separation

The final role model separates four jobs:

- **Platform admin**: manages platform setup through Django admin.
- **Organisation manager**: triages requests but does not verify ISL correctness.
- **Glossary editor / ISL reviewer**: edits signs and checks content/video workflow states.
- **Staff user**: searches, favourites, requests and reports signs.

This separation is probably the most important design decision in the project. A manager may know what vocabulary is useful in their workplace, but that does not mean they should approve the correctness of an ISL sign. The glossary editor role gives the project a more realistic review step.

## Organisation Scoping

Most records are linked to an `Organisation`. Views check the logged-in user's `StaffProfile` before showing staff-only data.

For example:

- staff can only favourite signs from their own organisation
- staff dashboards only show their own organisation data
- managers only triage requests for their organisation
- glossary editors only edit signs from their organisation

This is not full multi-tenant SaaS security, but it does show the core idea of keeping organisation data separated.

## Content Visibility

Public users and ordinary staff only see signs marked as `published`.

Organisation managers and glossary editors may see draft or review-needed signs for their own organisation. That is useful because they need to understand the workflow state, but editing is still limited to glossary editors.

## Django Admin

Django admin is reserved for the platform admin. Organisation managers and glossary editors use normal application screens instead.

This avoids a confusing problem in Django: the built-in `is_staff` field really means "can access the Django admin", not "is a staff user in this project". Keeping those two meanings separate makes the role model easier to defend.

## Known Limitations

A production version would need more work, including:

- secret key and settings loaded from environment variables
- `DEBUG = False`
- real production `ALLOWED_HOSTS`
- HTTPS configuration
- more detailed audit logging
- email notifications
- spam/rate-limit protection for public forms
- proper media upload and video hosting rules
