# Configuração v0.2.5 — 28/07/2026

**Origem:** `03_Klipper_Config/` do commit `cb7f9fc` (branch `main` de `origin`), extraída em
25/10/2026 durante a consolidação — antes de `03_Klipper_Config/` passar a espelhar a máquina.

**Nota de versionamento:** a mensagem do commit diz *“v0.2.0 - Machine geometry and dual nozzle
calibration”*, porém a tag anotada sobre ele é `v0.2.5`. O sufixo de versão ficou ambíguo.

## Estado

Primeira calibração geométrica realmente medida:

- Homing **sensorless** (`tmc2209_stepper_x:virtual_endstop`, `diag_pin PF4/PF3`, `SGTHRS 55/60`)
- `X: -14..262`, `Y: -4..174`, `rotation_distance 33.7298055705`
- `T1: SET_GCODE_OFFSET X=33.600 Y=-0.640 Z=-0.080`
- `probe.cfg` presente no diretório, **mas não incluído** por `printer.cfg`
- Sem `[bed_mesh]`, sem `[exclude_object]`, sem iluminação, sem PA

## Aviso

> **Não restaurar sobre a CB1.** Esta árvore já divergia da máquina em agosto: o homing real é
> **mecânico e no máximo** (X 265 / Y 155,3 / Z 159), e os limites de Y são diferentes. Restaurá-la
> inverteria a estratégia de homing e provocaria colisão.

## Integridade

```
bd05e77f8aadfb536fdf7362e7d540d3b994d577b21c12b71b24b1fdd69f3385  printer.cfg
```
