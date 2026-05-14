# Testing and Submission Notes

## Automated Tests

Testing is handled with Django's built-in test framework. The tests are not meant to prove that the system is perfect, but they do check the parts most likely to break: roles, organisation scoping, forms and workflow changes.

The test suite covers:

- organisation-scoped search and API responses
- category filtering
- staff favourites
- staff and visitor sign requests
- reports about existing signs
- manager request triage
- glossary editor dashboard access
- glossary editor sign editing
- sign change log creation
- unpublished sign visibility
- cross-organisation validation
- platform-admin access to Django admin

Run the tests with:

```powershell
.\.venv\Scripts\python.exe manage.py test
```

Run Django's system checks with:

```powershell
.\.venv\Scripts\python.exe manage.py check
```

## Manual Test Checklist

Before submission, I would still check the main flows in the browser. Automated tests are helpful, but they do not show whether the page feels awkward or whether a button is in a strange place.

Suggested checks:

- Open the organisation list page.
- Open the College Computing glossary.
- Search for a term such as `deadline` or `login`.
- Filter by a category and by an A-Z letter.
- Open a sign detail page.
- Log in as `college_staff` and favourite a sign.
- Submit a missing-sign request.
- Report an issue on an existing sign.
- Log in as `college_manager` and triage a request.
- Log in as `college_glossary` and check the glossary editor dashboard.
- Use the edit button on a sign page and confirm a change log entry appears.
- Log in as `platform_admin` and confirm Django admin is available.

## Submission Notes

The `.gitignore` file excludes local or generated files such as:

- `.venv/`
- `db.sqlite3`
- `runserver*.log`
- `.idea/`
- `frontend/`
- `node_modules/`
- generated static output

The submitted repository should contain the Django code, templates, static CSS/JavaScript, migrations, tests and documentation.

## Known Prototype Limitations

- Some sample video URLs are placeholders or candidate references.
- The project is not a complete ISL dictionary.
- The project does not replace qualified interpreters.
- Public reporting forms do not yet send email notifications.
- There is no spam protection for public forms.
- The interface has not been tested with a full group of Deaf users or ISL experts.
