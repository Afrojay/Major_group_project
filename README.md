# ISL Glossary Platform

Design and Development of an Adaptable Web-Based Irish Sign Language Glossary Platform for Domain-Specific Accessibility.

This Django prototype demonstrates an organisation-specific ISL glossary that can be adapted for contexts such as a college computing department, retail customer service team, or healthcare reception desk. It helps staff browse common signs, search service-specific terms, favourite useful signs, and request missing signs for manager review before interpreter/content follow-up.

## Implemented prototype scope

- Organisation-specific glossary landing pages
- Categories linked to organisations
- Sign entries with English term, category, description, usage context, tags, thumbnail URL, transcript support, official publication flag, and video URL
- Search, A-Z filtering, category navigation, and browse within the selected organisation
- Django staff login
- Staff profiles linked to one organisation with staff, manager, and glossary manager roles
- Staff dashboard with favourites, request history, recent signs, and portal-style placeholders
- Simple portal items for prototype tasks, calendar notes, appointments, and access notes
- Login redirects staff to their own organisation dashboard
- Organisation dashboards show simple role/domain placeholder panels such as retail tasks, college calendar notes, healthcare reception checks, and manager to-dos
- Staff favourites for signs in their own organisation
- Staff and visitor missing-sign requests
- Manager request review dashboard
- Request statuses: Pending manager review, Needs clarification, Manager approved, Sent to interpreter, Completed, Rejected
- Manager approval and interpreter notes on sign requests
- Django admin content management

## Not implemented

This is not a complete national ISL dictionary, a replacement for qualified ISL interpreters, a full ISL course, formal Deaf awareness training, or a production SaaS system. Production security hardening, audit logging, email automation, data export, billing, and full tenant administration remain future work.

Healthcare examples are included only as prototype service-access vocabulary. They are not clinical guidance and do not replace professional communication support.

The manager review flow is a security-related design choice. Managers can triage requests, but official sign publication remains in the Django admin back office so unvalidated glossary content is not published directly from the staff portal.

Organisation records support basic database-driven branding through theme colour, logo URL, description and contact email. This supports organisation-specific deployment while keeping advanced branding as future work.

## Run locally

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
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

Demo accounts created by `load_sample_data` use the password `prototype123`. Each sample organisation has a staff account, such as `college_staff`, a manager account, such as `college_manager`, and a glossary manager account, such as `college_glossary`.
