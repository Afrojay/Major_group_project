# ISL Glossary Platform

Final-year B.Sc. Computing prototype: **Design and Development of an Adaptable Web-Based Irish Sign Language Glossary Platform for Domain-Specific Accessibility**.

This project is a Django web application for small, organisation-specific Irish Sign Language glossary collections. The idea is not to build a national ISL dictionary. It is closer to a staff support tool for places such as a college department, a retail customer service desk, a healthcare reception area, or a public office where staff may need to recognise and practise a small set of useful signs.

The project should be read as a prototype. It does not replace qualified interpreters, formal ISL teaching, Deaf awareness training, or clinical communication support. Some of the sample signs and video references are deliberately marked as needing review, which reflects the reality that sign-language content should not be treated casually.

## Main Technologies

- Python and Django for the backend
- Django models for the main data structure
- Django templates for server-rendered pages
- Small Vue components for selected interactive parts of the staff-facing interface
- Plain CSS for layout, responsive design and organisation colours
- SQLite for the local prototype database
- Django tests for the main workflows and access rules

## What The Prototype Does

The application supports:

- organisation-specific glossary pages
- categories and sign entries
- descriptions, tags, usage context and video URLs
- search, category filtering and A-Z filtering
- staff login
- staff favourites
- missing-sign requests
- reports about existing signs, such as broken video links or unclear descriptions
- manager request triage
- a glossary editor queue
- a sign edit page for glossary editors
- publication and video review statuses
- a simple change log for sign edits
- platform administration through Django admin

## Role Model

The role model changed a bit during development. At first it was tempting to make an "organisation admin" do nearly everything, but that became confusing. The final version separates the work more clearly:

- **Platform admin**: uses Django admin for platform-level setup.
- **Organisation manager**: checks whether staff/visitor requests are relevant to the organisation.
- **Glossary editor / ISL reviewer**: edits sign content and reviews video/content status.
- **Staff user**: searches, favourites, requests and reports signs.

Only `platform_admin` uses the Django admin site. Managers and glossary editors use the normal application screens, which is easier to explain and avoids mixing Django's built-in `is_staff` flag with the project's own staff roles.

## Run Locally

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py load_sample_data
.\.venv\Scripts\python.exe manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Demo Accounts

All sample accounts created by `load_sample_data` use the password `prototype123`.

| Username | Password | Purpose |
| --- | --- | --- |
| `platform_admin` | `prototype123` | Django admin / platform admin |
| `college_staff` | `prototype123` | Normal staff user |
| `college_manager` | `prototype123` | Organisation manager |
| `college_glossary` | `prototype123` | Glossary editor |

The retail and healthcare examples use the same pattern.

## Useful Commands

```powershell
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py createsuperuser
```

## Documentation

The `docs/` folder contains the notes I would use to explain the project design:

- `architecture.md`: project structure and data model
- `content-review-workflow.md`: requests, reports and glossary review
- `frontend-implementation.md`: CSS, Vue and responsive interface decisions
- `security-and-access-control.md`: roles, organisation scoping and security limitations
- `accessibility-audit.md`: accessibility features and areas still needing work
- `testing-and-submission.md`: tests, manual checks and submission notes
- `diagrams/`: PlantUML diagram sources
