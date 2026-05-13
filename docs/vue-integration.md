# Vue Integration Notes

## Chosen approach

The project uses Vue as a progressive enhancement layer inside Django templates.

Django remains responsible for:

- data modelling through Django models
- staff authentication and permissions
- form validation and saving
- Django admin content management
- server-rendered fallback pages

Vue is used for small staff-facing improvements:

- reactive glossary search and A-Z filtering
- favourite and unfavourite buttons
- sign detail interaction
- missing-sign request form feedback
- staff dashboard summaries

## Why this fits the project

This approach avoids a full frontend rewrite. It keeps the system suitable for a final-year project because each Vue feature is added to an existing Django page, backed by a small Django JSON endpoint where needed.

The architecture is easier to explain than a separate single-page application because there is still one main backend application, one data model layer, and one trusted admin interface.

## API endpoints added for Vue

- `/org/<organisation_slug>/api/signs/`
  Returns organisation-scoped signs for glossary search and filtering.

- `/org/<organisation_slug>/dashboard/api/`
  Returns staff-scoped favourites, recent signs, and request history for the dashboard summary.

The existing favourite endpoint also returns JSON when Vue sends `Accept: application/json`, while continuing to support normal Django form posts.

## Accessibility decisions

- Django-rendered pages remain available if JavaScript fails.
- Controls use real buttons and links.
- Favourite buttons expose `aria-pressed`.
- Form errors are connected to fields with `aria-invalid` and `aria-describedby`.
- Existing skip links, headings, labels, focus states, and responsive CSS are retained.

## Testing approach

Django tests cover:

- organisation-scoped API filtering
- favourite state in JSON responses
- cross-organisation protection
- JSON favourite toggling
- request form rendering for staff and visitors
- dashboard API access and payloads

Manual browser testing should check:

- keyboard navigation through search, category links, A-Z filters, favourite buttons, and forms
- mobile layout at narrow widths
- no-JavaScript fallback by disabling JavaScript or checking the rendered Django markup
- screen-reader-friendly labels, headings, and status messages
