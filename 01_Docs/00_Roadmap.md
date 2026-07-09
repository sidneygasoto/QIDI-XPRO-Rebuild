# Roadmap

> Projeto: Retrofit Completo da QIDI X-Pro

**Versão:** 0.1.0
**Última atualização:** 2026-07-06
**Status:** Em desenvolvimento

---

# Objetivo

Este documento é o **plano diretor do projeto**.

Ele registra o estado atual do retrofit, as decisões de engenharia, os marcos alcançados, as etapas futuras e serve como referência para retomar o desenvolvimento em qualquer momento.

Sempre que uma etapa importante for concluída, este documento será atualizado.

---

# Objetivos do Projeto

Realizar um retrofit completo da impressora **QIDI X-Pro**, substituindo sua eletrônica e software originais por uma plataforma moderna baseada em **Klipper**, mantendo a robustez mecânica da máquina e priorizando:

- confiabilidade;
- facilidade de manutenção;
- documentação completa;
- hardware aberto;
- alto desempenho;
- reprodutibilidade.

---

# Filosofia de Engenharia

Durante todo o projeto serão seguidas as diretrizes:

- Nunca energizar hardware sem checklist.
- Nunca assumir informações sem confirmação.
- Validar experimentalmente todas as ligações.
- Documentar todas as decisões técnicas.
- Comentar integralmente todas as configurações.
- Priorizar soluções robustas e de fácil manutenção.
- Registrar problemas e respectivas soluções.
- Criar backups em todos os marcos importantes.

---

# Arquitetura Definida

## Controladora

- BIGTREETECH Manta M8P V2.0

## Host

- BIGTREETECH CB1 V2.2

## Drivers

- 5 × TMC2209 (UART)

## Firmware

- Klipper

## Interface Web

- Moonraker
- Fluidd

## Fatiador

- OrcaSlicer

## Monitoramento

- Obico

## Integração futura

- Home Assistant

---

# Hardware da Impressora

## Hotends

- 2 × Trianglelab Ceramic Hotend (originais)
- Sensores de temperatura NTC100
- Temperatura máxima de operação: 320 °C

## Sistema de Extrusão

Será mantida a arquitetura original:

- dois hotends;
- dois extrusores;
- um único carro de impressão.

Não haverá conversão para IDEX.

---

## Sensor de Nivelamento

- Sensor indutivo AECO
- M8
- Saída PNP

Validação futura:

- PROBE_ACCURACY

---

## Sensores

### Principal

- ADXL345 (SPI)

### Reserva

- MPU6050 (I²C)

---

## Iluminação

Placa desenvolvida especificamente para o projeto contendo:

- três LEDs brancos;
- resistores de 100 Ω;
- instalada entre os hotends.

---

# Situação Atual

## Concluído

### Hardware

- Arquitetura definida.
- Componentes principais adquiridos.
- Hotends substituídos.
- Sensor de nivelamento instalado.
- Sistema de iluminação instalado.

### Plataforma

- CB1 instalado.
- Debian 13 Minimal instalado.
- Sistema atualizado.
- Ethernet validada.
- SSH validado.
- SPI validado.
- GPIO validado.
- I²C validado.
- UART validada.
- Backup_0 criado.

---

## Em andamento

- Instalação do ecossistema Klipper.

---

# Próximas Etapas

## Etapa 1 — Plataforma

- [x] Instalar Debian.
- [x] Atualizar sistema.
- [x] Validar comunicação.
- [x] Habilitar SPI.
- [ ] Instalar Klipper.
- [ ] Instalar Moonraker.
- [ ] Instalar Fluidd.
- [ ] Compilar firmware da Manta M8P.
- [ ] Testar comunicação USB.

---

## Etapa 2 — Hardware

- [ ] Inventário completo da impressora.
- [ ] Identificação dos motores.
- [ ] Identificação dos ventiladores.
- [ ] Identificação da fonte.
- [ ] Identificação dos sensores.
- [ ] Identificação completa do cabeamento.

---

## Etapa 3 — Elétrica

- [ ] Esquema elétrico.
- [ ] Pinagem da Manta M8P.
- [ ] Pinagem do CB1.
- [ ] Ligações dos ventiladores.
- [ ] Ligações dos hotends.
- [ ] Ligações dos sensores.

---

## Etapa 4 — Klipper

- [ ] Configuração inicial.
- [ ] Configuração dos TMC2209.
- [ ] Configuração dos hotends.
- [ ] Configuração do sensor indutivo.
- [ ] Configuração dos ventiladores.
- [ ] Configuração dos LEDs.

---

## Etapa 5 — Calibração

- [ ] PID Hotend 0.
- [ ] PID Hotend 1.
- [ ] PID Mesa.
- [ ] PROBE_ACCURACY.
- [ ] Bed Mesh.
- [ ] Input Shaper.
- [ ] Pressure Advance.

---

## Etapa 6 — Recursos Avançados

- [ ] Obico.
- [ ] Home Assistant.
- [ ] Dashboard de diagnóstico.
- [ ] Monitoramento dos TMC2209.
- [ ] Monitoramento do CB1.
- [ ] Backup automático.
- [ ] Macros de manutenção.

---

# Marcos do Projeto

| Versão | Marco |
|--------:|-------|
| 0.1.0 | Foundation |
| 0.2.0 | Klipper instalado |
| 0.3.0 | Primeira comunicação com a Manta |
| 0.4.0 | Primeira impressão |
| 0.5.0 | Impressora funcional |
| 1.0.0 | Retrofit concluído |

---

# Decisões de Engenharia

## Arquitetura

Foi decidido manter a arquitetura mecânica original da QIDI X-Pro.

Justificativa:

- menor custo;
- maior confiabilidade;
- menor complexidade mecânica;
- preservação da robustez original.

---

## ADXL345

Será conectado diretamente ao CB1 utilizando SPI.

Justificativa:

- menor latência;
- maior taxa de amostragem;
- segue a recomendação do Klipper;
- reduz carga sobre a MCU STM32.

---

## Documentação

Toda decisão técnica deverá conter justificativa.

Nenhuma alteração será realizada sem atualização da documentação correspondente.

---

# Referências

- README.md
- CHANGELOG.md
- docs/02_Plataforma_CB1.md
- docs/03_Manta_M8P.md
- docs/04_Backups.md