# ISL Glossary Platform

Design and Development of an Adaptable Web-Based Irish Sign Language Glossary Platform for Domain-Specific Accessibility.

This Django prototype demonstrates an organisation-specific ISL glossary that can be adapted for contexts such as a college computing department, retail customer service team, or healthcare reception desk. It helps staff browse common signs, search service-specific terms, favourite useful signs, and request missing signs for admin review.

## Implemented prototype scope

- Organisation-specific glossary landing pages
- Categories linked to organisations
- Sign entries with English term, category, description, usage context, tags, and video URL
- Search and browse within the selected organisation
- Django staff login
- Staff profiles linked to one organisation, with optional organisation-admin permissions
- Staff dashboard with favourites, request history, recent signs, and portal-style placeholders
- Staff favourites for signs in their own organisation
- Staff and visitor missing-sign requests
- Organisation-admin request review dashboard
- Request statuses: Pending, Approved, Rejected, Needs clarification
- Django admin content management

## Not implemented

This is not a complete national ISL dictionary, a replacement for qualified ISL interpreters, a full ISL course, formal Deaf awareness training, or a production SaaS system. Production security hardening, audit logging, data export, billing, and full tenant administration remain future work.

Healthcare examples are included only as prototype service-access vocabulary. They are not clinical guidance and do not replace professional communication support.

## Run locally

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py load_sample_data
.\.venv\Scripts\python.exe manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Useful commands

```powershell
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Demo accounts created by `load_sample_data` use the password `prototype123`. Each sample organisation has a staff account, such as `college_staff`, and an organisation admin account, such as `college_admin`.
