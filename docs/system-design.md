# System Design

## Overview

The system is designed as one reusable Django application that can support multiple organisation-specific ISL glossary instances.

The platform does not use separate websites or branches for each domain. Instead, adaptability is handled through the database.

## Main architecture

```txt
Django project
→ glossary app
→ Organisation records
→ Category records
→ SignEntry records
→ Quick-reference signs
```

## Data model

### Organisation

Represents a deployed glossary instance, such as a college department or retail service.

### Category

Represents a group of signs belonging to one organisation.

### SignEntry

Represents an individual ISL glossary term with a video URL, description, usage context and quick-reference flag.

### FAQEntry

Represents simple written support questions and answers that can be linked to an organisation.

## URL structure

```txt
/                                      Home page
/org/<organisation_slug>/              Organisation glossary home
/org/<organisation_slug>/category/<category_slug>/
/org/<organisation_slug>/sign/<sign_slug>/
/org/<organisation_slug>/search/?q=term
/org/<organisation_slug>/quick-reference/
```

## Reason for one codebase

Using one Django codebase with multiple Organisation records demonstrates the adaptable-platform concept more clearly than creating separate websites. It also keeps the project easier to maintain and explain during the demonstration.
