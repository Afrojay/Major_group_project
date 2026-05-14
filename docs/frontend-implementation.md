# Frontend Implementation Notes

## Design Approach

The interface is meant to feel like a working staff tool, not a glossy landing page. In a real college or reception setting, a user would probably want to find a sign quickly rather than read a long introduction.

The pages use:

- clear headings
- breadcrumbs on detail and edit pages
- obvious buttons and links
- small status labels for workflow states
- cards for repeated dashboard/request items
- responsive grids
- organisation accent colours stored in the database

There is still room to improve the visual design. For example, some of the dashboard sections are quite plain. I kept them restrained on purpose, though, because the project is more about workflow and accessibility than heavy visual branding.

## CSS

The styling is written in plain CSS in `static/glossary/styles.css`.

I considered whether a framework such as Tailwind would make sense, but for this prototype it felt like an extra layer to explain. Plain CSS is less fashionable, maybe, but it is easier to inspect and it keeps the submission simpler.

Some key CSS choices:

- CSS variables hold the organisation accent colour.
- Flexbox and grid are used for layout.
- Buttons and form controls use consistent spacing.
- Focus states are visible for keyboard navigation.
- Mobile views stack content rather than forcing tiny text.

Tailwind CSS is not part of the submitted application. That choice may limit rapid styling, but it avoids a build process that the project does not really need.

## Vue

Vue is used as progressive enhancement inside Django templates. It is not a separate single-page application.

The Vue layer supports:

- reactive glossary search and filtering
- favourite/unfavourite interaction
- sign detail interaction
- request form feedback
- staff dashboard summaries

The Django-rendered content stays on the page as a fallback. This is important because the site should not become blank or unusable just because JavaScript fails.

## JavaScript Files

- `vue-glossary.js`: search, category filtering and A-Z filtering
- `vue-sign-detail.js`: sign detail interaction and favourite state
- `vue-request-form.js`: request-form validation feedback
- `vue-staff-dashboard.js`: staff dashboard summary
- `messages.js`: dismissible/auto-expiring messages

The files are deliberately small and page-specific. That makes them less reusable, but much easier to understand during a viva or code walkthrough.
