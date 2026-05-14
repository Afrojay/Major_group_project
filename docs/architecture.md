# Architecture Notes

## Overall Shape

The codebase has one Django project, `isl_glossary_platform`, and one main app, `glossary`. I kept it that way because a larger split into several apps would probably make the prototype look more "professional" at first glance, but it would also make it harder to explain in a final-year project.

The main files are:

- `glossary/models.py`: models and validation rules
- `glossary/views.py`: page views, JSON endpoints and workflow actions
- `glossary/forms.py`: forms for requests, reports, sign editing and dashboard items
- `glossary/admin.py`: Django admin setup for the platform admin
- `glossary/tests.py`: tests for the main workflows and access rules
- `templates/`: server-rendered HTML
- `static/glossary/`: CSS and small JavaScript/Vue files
- `docs/diagrams/`: PlantUML sources used for thesis diagrams

This structure appears to fit the scale of the project. It is not a large production system, so keeping the moving parts visible is more useful than hiding them behind too many layers.

## Main Data Model

The model design is centred on `Organisation`. Most content belongs to an organisation, because the same platform may be reused for different places with different glossary needs.

For example, a computing department might need signs such as "assignment", "debugging" and "deadline", while a reception desk might need "appointment", "waiting room" or "date of birth". The data model tries to support those local differences without becoming a full linguistic dictionary.

Important models:

- `Organisation`: the organisation or deployment context
- `Category`: a local grouping of signs
- `SignEntry`: the glossary item itself
- `Transcript`: optional transcript text for accessibility and search
- `StaffProfile`: links a Django user to one organisation and one role
- `FavouriteSign`: saved signs for staff users
- `SignRequest`: missing-sign requests and reports about existing signs
- `SignEntryChangeLog`: a small record of glossary editor changes
- `PortalItem`: simple dashboard tasks, notes or appointments for the prototype

## Page Flow

Public users can browse an organisation glossary, search for signs, view sign details and report problems. Staff users can do the same, but can also favourite signs and submit requests without typing their contact details every time.

Organisation managers get a request-triage dashboard. Glossary editors get a separate content queue and can edit signs from the sign detail page. This split may look slightly more complicated than one admin page, but it makes the responsibilities clearer.

## Why Django Stays At The Centre

Django handles the parts that need to be reliable and easy to test:

- models and migrations
- authentication and sessions
- CSRF protection
- form validation
- server-rendered templates
- Django admin for platform administration
- automated tests

Vue is used only where it improves the experience on top of Django pages. That means the application still makes sense if JavaScript is unavailable, and it also keeps the architecture easier to describe.
