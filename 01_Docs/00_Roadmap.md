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

## v0.2.0

Calibração da impressora.

Objetivos:

- Probe Offset
- Bed Mesh
- Z Offset
- Offsets entre hotends
- Primeiro layer
- Ajuste fino da extrusão

---

## v0.3.0

Recursos avançados.

- Pressure Advance
- Macros
- LEDs
- Filament Runout
- Timelapse
- Câmera

---

## v1.0.0

Retrofit totalmente concluído.

- Documentação completa
- Hardware validado
- Impressora pronta para produção
---

# Calibração mecânica

Pendente:

- Nivelamento da mesa.
- Z offset.
- Mesh bed leveling.
- Ajuste dos eixos.

---

# Finalização

Pendente:

- Câmera.
- Macros Klipper.
- Backup automático.
- Documentação final.
- Perfil de impressão.

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