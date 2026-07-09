# QIDI X-PRO Rebuild
## Estado Atual - v0.2.0

Data: 09/07/2026

## Plataforma

- Host: BIGTREETECH CB1
- Sistema: Debian 13 arm64
- Kernel: 7.0.2-vendor-sunxi64

## Controle

- Placa: BIGTREETECH Manta M8P V2.0
- MCU: STM32H723
- Firmware Klipper compilado e carregado

## Software

[x] Klipper
[x] Moonraker
[x] Fluidd
[x] Nginx

## Comunicação

CB1 ↔ STM32:
OK

## Sensores

NTC 100K Generic 3950:

- Extruder 0: 25.2 °C
- Extruder 1: 25.2 °C
- Heated Bed: 25.2 °C

## Configuração

Arquivos ativos:

- steppers.cfg
- tmc2209.cfg
- extruders.cfg
- heaters.cfg
- fans.cfg

## Próximas etapas

- Teste dos aquecedores
- PID tuning
- Teste motores
- Homing
- Input Shaper ADXL345
