# Accessibility Review Notes

## Scope

This note records the accessibility considerations reviewed for the Django prototype. It covers the organisation list, organisation glossary, sign detail page, staff dashboard, manager dashboard, and sign request form.

## Implemented accessibility features

- Semantic page landmarks: header, navigation, main content, sections and headings.
- Skip link to the main content area.
- Keyboard-accessible navigation using native links, buttons, forms and `details`/`summary`.
- Visible focus indicators for links, buttons and form controls.
- Organisation logos use alt text based on the organisation name.
- Glossary pages provide search, category navigation and A-Z filtering without relying only on colour.
- Staff and visitor request forms use Django forms and CSRF protection.
- Sign entries support optional transcript text for accessibility and search support.
- Colour contrast was adjusted for body text, muted text, buttons, status labels and form borders.

## Known limitations

- Video hosting and captions are not implemented in the prototype.
- Some sample sign videos are marked as needing ISL content review before real deployment.
- Full screen reader testing with Deaf and disabled users remains future work.
- Automated accessibility scanning with tools such as WAVE or axe remains future work.

## Thesis note

The prototype supports accessible structure and basic transcript metadata, but it should not be presented as a complete accessibility-tested production system. The thesis should describe video captions, broader user testing, and production accessibility auditing as future work.
