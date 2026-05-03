# Technology Decision

## Original plan

The project originally considered a React frontend, Node.js backend, MongoDB database and Docker for development/deployment. This reflected the first idea of building a modern web application with a separate frontend and backend.

## Reason for review

After Semester 1 feedback, the project scope was reviewed. The revised system is mainly a database-driven glossary and content management platform. It needs to manage organisations, categories, sign entries, quick-reference signs and support content.

## Final decision

The final implementation uses Python and Django.

Django was selected because it provides built-in support for:

- database models and migrations
- URL routing
- server-rendered templates
- forms
- authentication
- Django admin

These features support a working prototype within the academic timeframe.

## Development lifecycle link

This change should be described as iterative planning and technology evaluation. The original plan is preserved in the `archive/semester-1-prototype` branch, while this branch contains the revised Django implementation.
