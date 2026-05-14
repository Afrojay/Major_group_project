# Accessibility Review Notes

## Scope

These notes cover the main pages in the prototype: the organisation list, organisation glossary, sign detail page, request/report forms, staff dashboard, manager dashboard and glossary editor pages.

The accessibility work here is not a full audit. It is more of a structured check of the basics that should be in place for a web prototype like this.

## What Has Been Implemented

- The pages use semantic structure: header, navigation, main content, sections and headings.
- A skip link lets keyboard users jump to the main content.
- Navigation uses normal links, buttons, forms and `details`/`summary`.
- Focus states are visible on links, buttons and form controls.
- Organisation logos use alt text based on the organisation name.
- Search, category navigation and A-Z filtering do not rely only on colour.
- Request and report forms use Django forms and CSRF protection.
- Sign entries can include transcript text, which may help both accessibility and search.
- Text contrast was adjusted for body text, muted text, buttons, status labels and form borders.
- Flash messages can be dismissed and also expire after a short delay.

## Remaining Limitations

- The prototype does not host its own videos or captions.
- Some video URLs are placeholders or candidate sources that need ISL review.
- The interface has not been tested with a full group of Deaf users, ISL users or screen-reader users.
- Automated checks with tools such as WAVE or axe would still be useful.
- More work would be needed to test the Vue-enhanced pages with assistive technology.

## Thesis Note

The prototype can be described as accessibility-conscious, but not fully accessibility-tested. That distinction is important. It has sensible structure, labels, keyboard controls and transcript support, but a real deployment would need wider testing with users and better video/caption handling.
