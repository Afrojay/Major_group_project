# Use Cases

## Use case 1: Visitor browses an organisation glossary

Actor: Visitor

Goal: Open a glossary for a specific organisation or service.

Basic flow:

1. Visitor opens the home page.
2. Visitor selects an organisation.
3. System displays the organisation homepage, categories and quick-reference signs.

## Use case 2: Visitor searches for a sign

Actor: Visitor

Goal: Find a sign by keyword.

Basic flow:

1. Visitor opens an organisation glossary.
2. Visitor enters a search term.
3. System returns matching signs from that organisation only.
4. Visitor opens a sign detail page.

## Use case 3: Visitor views quick-reference signs

Actor: Visitor

Goal: Quickly access commonly needed signs.

Basic flow:

1. Visitor opens an organisation glossary.
2. Visitor selects Quick Reference.
3. System displays signs marked as commonly needed for that organisation.

## Use case 4: Admin adds a new sign

Actor: Admin user

Goal: Add a new glossary entry.

Basic flow:

1. Admin logs into Django admin.
2. Admin selects Sign Entries.
3. Admin enters term, organisation, category, video URL, description and quick-reference status.
4. Admin saves the entry.
5. The sign becomes available on the public glossary pages.

## Use case 5: Admin edits a category

Actor: Admin user

Goal: Update a category name or description.

Basic flow:

1. Admin logs into Django admin.
2. Admin selects Categories.
3. Admin edits the category details.
4. Admin saves the category.

## Use case 6: Admin adds a new organisation

Actor: Admin user

Goal: Create another organisation-specific glossary instance.

Basic flow:

1. Admin logs into Django admin.
2. Admin creates an Organisation record.
3. Admin adds categories and signs linked to that organisation.
4. The new organisation appears on the home page.
