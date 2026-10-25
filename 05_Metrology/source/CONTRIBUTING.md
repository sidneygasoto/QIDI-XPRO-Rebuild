# Contributing

Thank you for contributing to the Klipper Metrology Extension.

This project aims to provide a generic geometric calibration framework for Klipper through a clean, modular and extensible architecture.

---

# Project Goals

The objective is **not** to build a printer-specific calibration script.

The objective is to build a reusable metrology framework capable of supporting different printer architectures with minimal changes.

The architecture should remain:

- modular
- deterministic
- maintainable
- hardware independent whenever possible

---

# Project Structure

```
metrology/

├── metrology.py
├── models.py
├── geometry.py
├── machine.py
├── persistence.py
├── calibration.py
```

Future modules may be added without changing the overall architecture.

---

# Module Responsibilities

## metrology.py

Responsible for:

- registering G-Code commands
- validating parameters
- invoking library functions
- formatting responses for Klipper

This module must **not** implement:

- geometry
- persistence
- machine logic

---

## models.py

Contains only data structures.

Examples:

- Point3D
- Device
- ReferencePoint

No calculations.

No persistence.

No Klipper API.

---

## geometry.py

Contains mathematical operations.

Examples:

- offsets
- distances
- coordinate transformations
- geometric calculations

No G-Code commands.

No SAVE_CONFIG.

No Klipper configuration access.

---

## machine.py

Represents the machine geometric model.

Contains:

- printable area
- bed origin
- devices
- reference tool
- tool offsets

This module stores state only.

---

## persistence.py

Responsible for persistent storage.

Examples:

- load
- save
- delete
- SAVE_CONFIG support

No geometry.

No machine calculations.

---

## calibration.py

Contains calibration workflows.

Examples:

- machine construction
- calibration routines
- validation
- automatic parameter generation

---

# Coding Guidelines

Prefer:

- descriptive names
- short methods
- single responsibility
- reusable functions
- explicit code

Avoid:

- duplicated code
- hidden side effects
- tightly coupled modules

---

# Coordinate System

The project follows Klipper coordinates.

- +X → right
- +Y → back
- +Z → up

Offsets are always computed as:

```
TARGET - REFERENCE
```

Example:

```
LEFT - RIGHT
```

---

# Reference Tool

The reference tool defines the machine coordinate system.

Normally:

```
RIGHT
```

---

# Measurements

Measurements always represent real machine coordinates.

Examples:

- hotends
- probes
- bed origin
- cameras
- fixtures

---

# Persistence

Persistent data must be written only through:

```
persistence.py
```

---

# Dependency Flow

```
models
    ↓
geometry
    ↓
machine
    ↓
calibration
    ↓
persistence
    ↓
metrology
```

Dependencies must remain acyclic.

---

# Future Scope

The architecture is expected to support:

- multiple tools
- probes
- cameras
- dial indicators
- touch probes
- vision systems
- additional kinematics

without redesigning the core.