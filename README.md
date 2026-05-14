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
- Staff dashboard with favourites, request history, recent signs, and role/domain panels
- Simple portal items for prototype tasks, calendar notes, appointments, and access notes
- Login redirects staff to their own organisation dashboard
- Organisation dashboards show role/domain panels such as retail tasks, college calendar notes, healthcare reception checks, and manager to-dos
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

## Render deployment

The project can be deployed on Render using a Python Web Service and a Render PostgreSQL database. SQLite is only intended for local development. A deployed version should use PostgreSQL so the organisations, signs, users, favourites and requests persist after deployment.

### Render services used

- Web Service: Django application
- PostgreSQL: persistent production-style database
- Branch: `updated-functionality`

### Build and start commands

Use these Render settings for the web service:

```bash
Build Command: bash build.sh
Start Command: gunicorn isl_glossary_platform.wsgi:application
```

The `build.sh` script installs dependencies, collects static files, applies migrations and loads the demo data:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py load_sample_data
```

### Environment variables

Add these environment variables to the Render **Web Service**, not the PostgreSQL database page:

```txt
DATABASE_URL=<Render PostgreSQL Internal Database URL>
SECRET_KEY=<long random secret key>
DEBUG=False
ALLOWED_HOSTS=<your-render-domain.onrender.com>
CSRF_TRUSTED_ORIGINS=https://<your-render-domain.onrender.com>
```

Example for the current deployment:

```txt
ALLOWED_HOSTS=major-group-project-txed.onrender.com
CSRF_TRUSTED_ORIGINS=https://major-group-project-txed.onrender.com
```

If the deployed site shows `Bad Request (400)`, check that `ALLOWED_HOSTS` exactly matches the Render domain without `https://`. `CSRF_TRUSTED_ORIGINS` should include the full `https://` URL.

### Loading data on Render

The sample organisations and demo accounts are created by:

```bash
python manage.py load_sample_data
```

This command is included in `build.sh`, so the deployed site should show the sample organisations after deployment. If the homepage says `No organisations have been added yet`, run the command manually in a Render shell or redeploy after confirming the build script ran successfully.

### Deployment notes

- `DATABASE_URL` should use the Render PostgreSQL **Internal Database URL**.
- `DEBUG` should be `False` for deployment.
- The free Render instance may spin down after inactivity and take time to wake up.
- Video content is externally embedded or marked as needing review. The project does not claim ownership of external ISL videos.
