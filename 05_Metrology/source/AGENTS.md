# AGENTS.md

This document contains instructions for AI coding assistants working on this repository.

---

# Read First

Before modifying any code:

1. Read this file.
2. Preserve the existing architecture.
3. Prefer incremental changes.
4. Do not rewrite files unless requested.
5. Understand how the affected module interacts with the rest of the project before making changes.
6. If the requested change conflicts with the current architecture, explain the conflict before implementing it.
---

# Primary Rule

The architecture is more important than reducing lines of code.

Never simplify the project by merging responsibilities.

# Creating New Files

Do not create new modules unless:

- an existing module clearly violates the Single Responsibility Principle
- the new module has a well-defined responsibility
- the change cannot reasonably fit into the existing architecture

Prefer extending existing modules.

---

# Module Rules

## metrology.py

Acts only as the G-Code controller.

Allowed:

- register commands
- validate parameters
- call library functions
- format responses

Forbidden:

- geometry calculations
- persistence
- machine state

---

## models.py

Contains data structures only.

Never:

- call Klipper APIs
- perform calculations
- implement persistence

---

## geometry.py

Contains all mathematical operations.

Never:

- register commands
- access printer configuration
- write SAVE_CONFIG

---

## machine.py

Represents the printer geometry.

Stores the machine geometric model and runtime state.

Never read printer.cfg directly.
Never access Klipper objects.

No Klipper interaction.

---

## persistence.py

Handles persistence only.

Never perform calculations here.

---

## calibration.py

Contains calibration workflows and automatic machine construction.

---

# Development Rules

Always:

- preserve public APIs
- reuse existing classes
- reuse helper functions
- keep methods small
- keep code readable

Refactoring should preserve observable behavior unless the user explicitly requests behavioral changes.

If information is missing:

- ask for clarification
- do not guess printer geometry
- do not invent configuration values

When modifying existing behavior:

- preserve existing functionality
- avoid breaking backward compatibility
- suggest tests when appropriate

When adding new public APIs:

- update Markdown documentation
- document command parameters
- document expected behavior

---

# Decision Making

When multiple valid implementations exist:

- prefer the simplest solution
- preserve the current architecture
- minimize code changes
- explain important trade-offs before implementing

---

# Coordinate Convention

Offsets are always:

```
TARGET - REFERENCE
```

Never invert this convention.

---

# Reference Tool

Unless explicitly requested otherwise, assume:

```
RIGHT
```

is the machine reference tool.

---

# Project Philosophy

This is **not** a QIDI-specific project.

Although developed inside the QIDI X-Pro Rebuild project, the code must remain generic.

Avoid introducing printer-specific assumptions.

---

# Modification Policy

Prefer:

- adding methods
- extending classes
- refactoring incrementally

Avoid:

- large rewrites
- unnecessary formatting-only changes
- moving code between modules without justification

---

# Code Style

- Python 3
- Four-space indentation
- Explicit names
- Small functions
- Single responsibility
- English comments
- English documentation

---

# Long-Term Goal

Build a reusable geometric metrology framework for Klipper capable of supporting multiple printer architectures and measurement devices with minimal future changes.