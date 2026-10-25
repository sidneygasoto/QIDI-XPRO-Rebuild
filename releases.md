# Releases

## v0.3.0 — Produção validada

Data: 2026-10-25

### Estado

✔ Máquina operando em produção (último trabalho: 17/10/2026, 1h21m, PETG)

✔ Configuração real versionada em `03_Klipper_Config/` (espelho da CB1)

✔ Firmware publicado = firmware gravado (SHA256 `6a527307…`)

✔ Sonda ativa com `z_offset 0,652`

✔ Endstops mecânicos e home no máximo

✔ PID (2 hotends + mesa), Input Shaper, `rotation_distance`, offsets T1, PA

✔ Extensão de metrologia preservada em `05_Metrology/`

### Pendente

- Mesh da mesa inconsistente e não aplicado
- Extensão de metrologia não executável
- Divergência de branches no repositório
- Câmera (bloqueada por hardware)

### Próxima versão

**v0.4.0 — Geometria reconciliada**

- Mesh coerente com os limites reais e aplicado no início dos trabalhos
- Metrologia carregável, testada e versionada
- Documentação completa em `01_Docs/`

---

## v0.2.5

Data: 2026-07-28 — commit `cb7f9fc`

### Estado

✔ Geometria calibrada (`rotation_distance` de X/Y e extrusoras)

✔ Offsets entre bicos via `SET_GCODE_OFFSET`

✖ Homing sensorless (abandonado na máquina em favor de endstops mecânicos)

✖ Sonda presente no diretório, mas não incluída pelo `printer.cfg`

---

## v0.2.0

Data: 2026-07-09 — commit `6b32a7e`

### Estado

✔ Klipper, Moonraker e Fluidd instalados

✔ Comunicação CB1 ↔ STM32H723

✔ Cinco drivers TMC2209 em UART

✔ ADXL345 em SPI3 e Input Shaper calibrado

---

## v0.1.0

Data: 2026-07-06

### Estado

✔ Plataforma estável (Debian 13 no CB1, rede, SSH, SPI)

✔ `Backup_0` criado
