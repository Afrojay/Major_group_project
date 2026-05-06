# Thesis Diagrams

This folder contains PlantUML source diagrams for the thesis and presentation.

Recommended diagrams to export:

- `use-case.puml`: actor/system boundary diagram for Chapter 3 or Chapter 4.
- `erd.puml`: entity relationship diagram for the implemented Django data model.
- `request-workflow.puml`: activity diagram for staff/visitor request review.
- `project-structure.puml`: component diagram showing the Django prototype structure.

These diagrams describe the implemented prototype. Keep future-work items out of the diagrams unless they are clearly marked as future work in the thesis.

To render them, use the PlantUML VS Code extension or PlantUML command line:

```powershell
java -jar plantuml.jar docs/diagrams/*.puml
```
