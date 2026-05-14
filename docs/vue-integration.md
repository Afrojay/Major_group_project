# Vue Integration Notes

## Chosen Approach

Vue is used as a progressive enhancement layer inside Django templates. I did not turn the project into a separate Vue single-page app, because that would add a lot of frontend structure for a prototype that is still mainly about Django models, forms and workflow.

Django still handles:

- data modelling
- authentication and permissions
- form validation and saving
- platform administration through Django admin
- fallback server-rendered pages

Vue adds interaction where it is useful, mainly on staff-facing pages.

## Where Vue Is Used

Vue supports:

- glossary search and A-Z filtering
- favourite/unfavourite buttons
- sign detail interaction
- request form feedback
- staff dashboard summaries

This appears to be a reasonable middle ground. The interface feels more responsive, but the system does not depend entirely on JavaScript.

## JSON Endpoints

Two small JSON endpoints support the Vue components:

- `/org/<organisation_slug>/api/signs/`
  Returns organisation-scoped signs for glossary search and filtering.

- `/org/<organisation_slug>/dashboard/api/`
  Returns staff-scoped favourites, recent signs and request history.

The favourite endpoint can also return JSON if Vue sends `Accept: application/json`. The same endpoint still works as a normal Django form post, which keeps the fallback behaviour simple.

## Accessibility Notes

The Vue layer tries not to remove the accessibility work already provided by Django templates.

- Django-rendered content remains available if JavaScript fails.
- Buttons and links remain real HTML controls.
- Favourite buttons use `aria-pressed`.
- Form feedback uses field-level error messages.
- Existing headings, labels, skip links and focus styles remain in place.

There is still more work that could be done, especially full screen-reader testing. For this prototype, the main aim was to avoid making the Vue layer a barrier.

## Testing Approach

Django tests cover the server-side behaviour behind the Vue features:

- organisation-scoped API filtering
- favourite state in JSON responses
- cross-organisation protection
- JSON favourite toggling
- request form rendering for staff and visitors
- dashboard API access and payloads

Manual browser testing is still useful. In particular, search, filters, favourite buttons and forms should be checked with a keyboard and at narrow screen widths.
