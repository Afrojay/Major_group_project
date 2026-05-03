# Semester 1 Prototype Archive — Irish Sign Language Glossary Platform

This branch preserves the original Semester 1 version of the Irish Sign Language (ISL) Glossary project.

The purpose of this branch is historical. It records the first project concept, early design direction, original technology plan, and initial proof-of-concept prototype before the project was later reviewed and re-scoped.

The current/final project direction is developed on the `main` branch.

---

## Original Project Concept

The original concept was a general web-based Irish Sign Language glossary and learning/reference platform.

At this stage, the project was described as:

> A web-based learning and reference tool for Irish Sign Language.

The aim was to allow users to search for ISL signs, view video demonstrations, browse categories, and access learning-support features. The project was motivated by the idea that ISL learners, staff, students, and members of the public could benefit from easier digital access to ISL vocabulary.

The early project idea focused on:

- A searchable ISL glossary
- Video demonstrations for signs
- Categories of signs
- A mobile-friendly interface
- Basic learning/reference support
- Improved accessibility and inclusion

---

## Original Problem Statement

The original problem statement was based on the idea that there was no single comprehensive online glossary or learning platform for Irish Sign Language, and that existing resources could be fragmented, limited, outdated, or focused on specific topics.

This branch preserves that early framing. However, later supervisor feedback showed that this argument needed stronger evidence, clearer research, and a better distinction between a dictionary, a glossary, and a learning platform.

This feedback became an important part of the project’s development cycle.

---

## Original Target Users

The early prototype considered a broad range of possible users, including:

- ISL learners
- Students
- Staff in public-facing services
- People interested in basic ISL vocabulary
- Members of the Deaf community looking for digital reference material

At this stage, the project was still broad and was not yet focused on organisation-specific deployments.

---

## Original Technology Plan

The original technical plan considered the following stack:

- React for the frontend
- Node.js for the backend
- MongoDB for the database
- Docker for development/deployment
- GitHub for version control
- YouTube embedding or video URLs for sign demonstrations

This stack reflected the team’s early intention to build a modern web application with a separate frontend, backend, and database.

---

## Original Prototype Goals

The Semester 1 prototype was intended to demonstrate the basic idea of an ISL glossary website.

The planned or explored prototype features included:

- A homepage introducing the project
- A glossary/search area
- Sign categories
- Video-based sign demonstrations
- Basic responsive layout
- Early exploration of learning/reference features

This version should be understood as a proof-of-concept rather than the final system architecture.

---

## Design Ideas at This Stage

The early design focused on creating a simple website where users could access ISL vocabulary quickly.

The main design assumptions were:

- Users would search or browse for signs
- Each sign would have a video demonstration
- Signs could be grouped into categories
- The interface should be simple and accessible
- YouTube/video links could be used temporarily for prototype sign content

The design was useful as a starting point, but it later became clear that the project needed a more focused and defensible scope.

---

## Known Limitations of the Semester 1 Version

This archive branch intentionally preserves the limitations of the first iteration.

Known limitations included:

- The project scope was too broad
- The system was closer to a general glossary/learning website than a focused platform
- The research argument needed stronger evidence
- The distinction between a dictionary and a glossary needed to be clearer
- Accessibility needed to be defined more specifically
- The prototype was limited and did not yet show enough advanced functionality
- There was limited evidence of design iteration
- Testing and evaluation had not yet been developed properly
- The original stack would require more custom work for admin/content management

These limitations were later used as part of the project review and re-planning process.

---

## Supervisor Feedback and Review Point

After Semester 1, the project was reviewed using supervisor feedback.

The feedback highlighted the need for:

- Deeper research into ISL as a language
- Evidence for the claimed gap in existing ISL resources
- Examples and comparisons of existing ISL glossaries/tools
- A clearer explanation of accessibility
- A stronger prototype
- More design evidence
- A more obvious iterative development process
- Testing and evaluation
- A clearer timeline and project plan
- Better documentation and project diary evidence

This feedback became a formal review point in the development lifecycle.

---

## How This Version Connects to the Final Project

This branch should not be treated as abandoned work. It represents the first iteration of the project.

The project later evolved from:

> A general ISL glossary/learning website

into:

> An accessible and adaptable Django-based ISL glossary platform for organisation-specific or domain-specific deployment.

The newer direction focuses on a reusable platform that can be configured for a specific organisation, department, public service, classroom, or business. For example, a college computing department or retail store could have its own custom glossary containing only the signs and categories relevant to that environment.

---

## Reason for Later Technology Change

The original React/Node.js/MongoDB stack was later reviewed against the actual requirements of the project.

The project increasingly required:

- Structured database-driven glossary data
- Organisation-specific content
- Categories
- Sign entries
- Video links
- Search
- FAQ content
- Admin/content management
- A working prototype within the academic timeframe

The team therefore decided to switch to Python and Django for the final implementation. Django provides built-in support for database models, migrations, views, templates, forms, authentication, and an admin interface, making it more suitable for the revised content-management-focused prototype.

---

## Development Lifecycle Role

This archive branch supports the project’s Agile-inspired iterative development story:

1. Initial idea and research
2. Semester 1 general ISL glossary prototype
3. Supervisor feedback and review
4. Re-planning and scope refinement
5. Technology evaluation
6. Switch to Django
7. Development of the final organisation-specific glossary platform on `main`

This branch exists to show the early project direction and how the final project evolved from it.

---

## Branch Status

This branch is archived for reference.

Future development should continue on:

```txt
main
```

This branch should only be used when discussing the original prototype, Semester 1 development history, or project lifecycle evidence.
