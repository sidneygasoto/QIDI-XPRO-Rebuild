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

# 21/07/2026
# Estado Atual do Projeto

## Hardware

- BIGTREETECH Manta M8P V2.0
- BIGTREETECH CB1
- 5× TMC2209
- 2× Hotends
- ADXL345

---

## Sistema

✔ Armbian

✔ Klipper

✔ Moonraker

---

## Comunicação

✔ USB

✔ UART

✔ SPI

---

## Movimento

✔ X

✔ Y

✔ Z

---

## Homing

✔ Sensorless X

✔ Sensorless Y

✔ Endstop Z

✔ Probe

---

## Temperatura

✔ Bed

✔ Extruder

✔ Extruder1

---

## Input Shaper

X

- 3hump_ei
- 64.8 Hz

Y

- mzv
- 31.2 Hz

---

## PID

✔ Bed

✔ Extruder

✔ Extruder1

---

## Situação

Sistema totalmente operacional.

A próxima fase será dedicada exclusivamente à calibração geométrica da impressora.