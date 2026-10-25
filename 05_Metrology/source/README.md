# Klipper Metrology Extension

A generic metrology framework for Klipper.

The objective of this project is to provide a modular and extensible
calibration system capable of measuring the geometric characteristics of a
machine and automatically generating its configuration.

The extension is designed to be printer-independent and reusable across
different machine architectures.

---

## Features

Current capabilities:

- Capture machine coordinates
- Register persistent devices
- Calculate geometric offsets
- Calculate distances
- Compare measurements
- Persist reference devices

---

## Architecture

```
metrology/

├── metrology.py
│   GCode command interface
│
├── models.py
│   Data models
│
├── geometry.py
│   Geometry calculations
│
├── machine.py
│   Machine representation
│
├── persistence.py
│   SAVE_CONFIG support
│
└── calibration.py
    Calibration engine
```

Each module has a single responsibility.

---

## Design Principles

- Generic implementation
- Printer independent
- Modular architecture
- Separation of responsibilities
- Small reusable methods
- Explicit data models
- High readability
- Minimal dependencies

---

## Documentation

Project documentation is available in the `01_Docs` directory.

Main documents include:

- Architecture
- Mathematical model
- Calibration workflow
- Development notes

---

## Development

The development roadmap is maintained in:

```
ROADMAP.md
```

---

## Status

Current status:

**Active Development**

The extension is currently being developed as part of the **QIDI X-Pro
Rebuild** project but is intended to become a generic metrology framework
for Klipper.

---

## License

Same license as Klipper unless otherwise specified.