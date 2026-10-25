# Klipper Metrology Extension

Development Roadmap

---

# Vision

Create a generic metrology framework capable of describing the geometry of
any Klipper-supported machine and automatically generating the corresponding
configuration.

The extension should become a reusable calibration subsystem rather than a
printer-specific tool.

---

# Guiding Principles

- Printer independent
- Generic mathematical model
- Modular implementation
- Automatic configuration generation
- Extensible architecture
- No duplicated logic

---

# Development Phases

## Phase 1 — Foundation

### Models

- [x] Point3D
- [x] Device
- [x] ReferencePoint

### Geometry

- [x] Distance calculation
- [x] Offset calculation
- [x] Axis offset calculation

### Persistence

- [x] Device loading
- [x] Device saving
- [x] Device removal

### Machine

- [x] Machine model
- [x] Tool offsets
- [x] Bed origin
- [x] Printable area

---

## Phase 2 — Calibration Engine

### Calibration Model

- [ ] Calibration workflow
- [ ] Machine builder
- [ ] Reference tool selection
- [ ] Validation routines

### Automatic Calculations

- [ ] Bed origin
- [ ] Tool offsets
- [ ] Probe offsets
- [ ] Machine geometry

---

## Phase 3 — SAVE_CONFIG Integration

Automatically generate:

- [ ] Tool offsets
- [ ] Probe offsets
- [ ] Bed origin
- [ ] Configuration sections
- [ ] Persistent machine model

---

## Phase 4 — Geometric Calibration

### Bed

- [ ] Printable origin
- [ ] Printable dimensions
- [ ] Bed rotation

### Tools

- [ ] X offset
- [ ] Y offset
- [ ] Z offset

### Probe

- [ ] Probe position
- [ ] Probe validation

---

## Phase 5 — Advanced Geometry

- [ ] Coordinate transformations
- [ ] Rotation matrices
- [ ] Translation matrices
- [ ] Local coordinate systems
- [ ] Multiple reference frames

---

## Phase 6 — Machine Validation

- [ ] Geometry consistency
- [ ] Measurement uncertainty
- [ ] Error estimation
- [ ] Calibration report

---

## Phase 7 — Multi-tool Support

- [ ] Unlimited tools
- [ ] Tool groups
- [ ] Automatic reference selection
- [ ] Dynamic offsets

---

## Phase 8 — Future Kinematics

Support for:

- [ ] Cartesian
- [ ] CoreXY
- [ ] CoreXZ
- [ ] H-Bot
- [ ] IDEX
- [ ] Delta
- [ ] SCARA
- [ ] Polar

---

# Planned Commands

## Measurements

- [x] METROLOGY_CAPTURE
- [x] METROLOGY_LIST
- [x] METROLOGY_COMPARE
- [x] METROLOGY_DELETE
- [x] METROLOGY_CLEAR

---

## Devices

- [x] METROLOGY_CAPTURE_DEVICE
- [x] METROLOGY_LIST_DEVICES
- [x] METROLOGY_CLEAR_DEVICES

---

## Geometry

- [x] METROLOGY_OFFSET
- [x] METROLOGY_OFFSET_X
- [x] METROLOGY_OFFSET_Y
- [x] METROLOGY_OFFSET_Z

---

## Calibration

- [ ] METROLOGY_BUILD
- [ ] METROLOGY_VALIDATE
- [ ] METROLOGY_REPORT
- [ ] METROLOGY_SAVE

---

# Long-Term Goals

- Complete machine geometric model
- Automatic printer configuration
- Generic calibration framework for Klipper
- Reusable by any printer manufacturer
- Mathematical foundation independent of hardware

---

# Current Priority

1. Calibration engine
2. Machine model
3. SAVE_CONFIG generation
4. Automatic printer configuration
5. Validation and reporting