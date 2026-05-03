# Accessible and Adaptable ISL Glossary Platform

This repository contains the revised Django implementation for the final-year group project:

**Design and Development of an Accessible and Adaptable Web-Based Irish Sign Language Glossary Platform for Domain-Specific Deployment**

The project is a reusable web-based Irish Sign Language (ISL) glossary platform. Instead of building one large national ISL dictionary, the system is designed so that different organisations or services can have their own glossary instance with relevant categories, signs, quick-reference terms and support content.

Example organisation-specific deployments include:

- College Computing Department
- Retail Customer Service
- Healthcare Reception

Each deployment uses the same Django codebase but different database records.

---

## Development history

The project originally began as a general ISL glossary website. The early technology plan considered React for the frontend, Node.js for the backend, MongoDB for the database, Docker for development/deployment and YouTube/video URLs for sign demonstrations.

After Semester 1 feedback and review, the project was re-scoped. The revised version focuses on a database-driven, organisation-specific glossary platform. Python and Django were chosen because Django provides built-in support for models, migrations, templates, forms, authentication and the Django admin interface. These features suit the project because the system needs to manage organisations, categories, sign entries, quick-reference signs and optional FAQ/support content.

The branch `archive/semester-1-prototype` preserves the original Semester 1 prototype and early project direction. The `main` branch is intended to contain the revised Django implementation once this work has been reviewed and merged.

---

## Current Django architecture

The project uses:

- Python
- Django
- SQLite for local development
- Django templates for server-rendered pages
- HTML and CSS for the interface
- Django admin for content management
- Video URLs or YouTube embeds for sign videos

The core app is called `glossary`.

Main data model:

```txt
Organisation
→ Category
→ SignEntry
→ Quick-reference signs
→ FAQ/support entries
```

The important design decision is that adaptability is handled through the database model, not through separate websites or branches. For example:

```txt
/org/college-computing/
/org/retail-customer-service/
/org/healthcare-reception/
```

These pages can all run from the same Django application.

---

## Repository structure

```txt
Major_group_project/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── isl_glossary_platform/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── glossary/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   ├── tests.py
│   ├── templates/glossary/
│   └── static/glossary/css/
└── docs/
    ├── requirements.md
    ├── use-cases.md
    ├── system-design.md
    ├── technology-decision.md
    ├── accessibility.md
    ├── testing-plan.md
    ├── project-plan.md
    └── diary/
```

---

## Local setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Load sample data:

```bash
python manage.py load_sample_data
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Open the site at:

```txt
http://127.0.0.1:8000/
```

Open Django admin at:

```txt
http://127.0.0.1:8000/admin/
```

---

## Main pages

```txt
/                                      Home page
/org/<organisation_slug>/              Organisation glossary home
/org/<organisation_slug>/category/<category_slug>/
/org/<organisation_slug>/sign/<sign_slug>/
/org/<organisation_slug>/search/?q=term
/org/<organisation_slug>/quick-reference/
```

---

## Managing content

Content can be managed through Django admin.

Admin users can add and edit:

- Organisations
- Categories
- Sign entries
- FAQ/support entries

Some signs can be marked as quick-reference signs using the `is_quick_reference` field. These signs appear on the quick-reference page for that organisation.

---

## Running tests

```bash
python manage.py test
```

The initial tests check that the main public pages load and that search and quick-reference filtering work as expected.

---

## Notes and limitations

This is a prototype for an academic project. It is not a complete ISL dictionary, a replacement for qualified ISL interpreters, or a full ISL learning course.

Sample video URLs are placeholders unless replaced with verified ISL video sources. Any real sign content should be checked carefully and referenced appropriately in the final report.
