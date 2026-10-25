# QIDI-XPRO-Rebuild - Roadmap do Projeto

Projeto de reconstrução e modernização da impressora 3D QIDI X-Pro utilizando Klipper, BIGTREETECH Manta M8P V2.0 e CB1 como host.

---

# Visão geral

O objetivo do projeto é substituir a eletrônica original da QIDI X-Pro por uma arquitetura aberta baseada em Klipper, mantendo a estrutura mecânica original e evoluindo a máquina para uma plataforma moderna, configurável e expansível.

Arquitetura definida:

| Componente | Modelo |
|---|---|
| Controladora | BIGTREETECH Manta M8P V2.0 |
| MCU | STM32H723 |
| Host | BIGTREETECH CB1 |
| Firmware | Klipper |
| Interface | Fluidd |
| API | Moonraker |
| Drivers | TMC2209 UART |
| Extrusão | Dual Extruder |
| Sensores temperatura | NTC 100K Generic 3950 |
| Sensor de vibração | ADXL345 |

---

# Roadmap

## v0.1.0 ✅

Infraestrutura concluída.

---

## v0.2.0 ✅

Stack Klipper/Moonraker/Fluidd e calibração inicial.

- Comunicação CB1 ↔ STM32H723
- Cinco TMC2209 em UART
- Dois hotends independentes
- Input Shaper (ADXL345)
- PID dos aquecedores

---

## v0.2.5 ✅

Geometria e dual nozzle.

- `rotation_distance` calibrado
- Offsets entre bicos
- Probe Offset e Z Offset
- Bed Mesh medido

---

## v0.3.0 ✅

Produção validada — 25/10/2026.

- Configuração real versionada (`03_Klipper_Config/`)
- Pressure Advance
- Macros (`PRINT_START`, `PRINT_END`, `PAUSE`, `RESUME`, `BED_CALIBRATE`)
- Iluminação de ferramenta e de gabinete
- Impressão em produção desde outubro

---

## v0.4.0

Geometria reconciliada.

- Mesh coerente com os limites reais e aplicado no início dos trabalhos
- Extensão de metrologia carregável e versionada
- Documentação completa em `01_Docs/`

---

## v1.0.0

Retrofit totalmente concluído.

- Documentação completa
- Hardware validado
- Impressora pronta para produção

---

# Calibração mecânica

Concluído:

- Nivelamento manual em 3 pontos (`BED_CALIBRATE`).
- Z offset da sonda (0,652 mm).
- Mesh bed leveling medido (9×7).

Pendente:

- Recalibrar o mesh a quente e carregar o perfil no início da impressão.

---

# Finalização

Pendente:

- Câmera (aguardando hardware UVC com MJPEG).
- Filament runout.
- Timelapse.
- Backup automático.
- Perfil de impressão documentado.

---

# Organização do desenvolvimento

## PC

Responsável por:

- Documentação.
- Manuais.
- Esquemas.
- Diagramas.
- Revisão dos arquivos Markdown.

---

## CB1

Responsável por:

- Configurações reais.
- Testes.
- Serviços.
- Firmware.
- Logs.

---

# Milestone v0.1.0

## Objetivo

Concluir toda a infraestrutura necessária para transformar a QIDI X-Pro em uma plataforma Klipper totalmente funcional.

## Principais entregas

- Armbian instalado.
- Klipper Host configurado.
- Moonraker configurado.
- Comunicação USB validada.
- Firmware da Manta atualizado.
- Configuração dos motores.
- Configuração dos dois extrusores.
- Sensorless Homing.
- Probe indutivo.
- PID dos aquecedores.
- ADXL345 via SPI3.
- Input Shaper calibrado.

## Estado

A plataforma encontra-se estável e pronta para iniciar a fase de calibração geométrica.

## Próxima milestone

v0.2.0 — Calibração Mecânica