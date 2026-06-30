# QIDI X-Pro Rebuild

> Retrofit completo da **QIDI X-Pro** para uma plataforma moderna baseada em **Klipper**, utilizando hardware aberto, foco em confiabilidade, facilidade de manutenção e documentação completa.

---

## 📖 Sobre o projeto

A QIDI X-Pro é uma excelente impressora em termos de estrutura mecânica, porém sua eletrônica e software ficaram defasados ao longo dos anos.

O objetivo deste projeto é reconstruir completamente a impressora utilizando hardware moderno e software open source, preservando sua robustez mecânica e adicionando recursos encontrados apenas em impressoras de última geração.

Este repositório documenta todas as etapas do retrofit, desde a desmontagem até a calibração final.

---

# 🎯 Objetivos

- Modernizar completamente a eletrônica
- Migrar para Klipper
- Melhorar a qualidade de impressão
- Aumentar a velocidade de impressão
- Facilitar futuras manutenções
- Documentar todas as modificações
- Utilizar somente hardware aberto
- Criar um projeto totalmente reproduzível

---

# 📊 Estado do Projeto

| Etapa | Status |
|-------|:------:|
| Planejamento | ✅ |
| Documentação | 🚧 |
| Hardware adquirido | ✅ |
| Instalação da M8P | ⏳ |
| Instalação do CB1 | ⏳ |
| Configuração do Klipper | ⏳ |
| Calibração | ⏳ |

### Legenda

- ✅ Concluído
- 🚧 Em andamento
- ⏳ Pendente

---

# 🖨 Impressora

**Modelo:** QIDI X-Pro

Arquitetura:

- Dual Extruder
- Dois hotends independentes
- Mesa aquecida
- Câmara fechada

---

# 🔧 Hardware

## Controladora

- BIGTREETECH Manta M8P V2.0

## Host

- BIGTREETECH CB1

## Drivers

- 5 × TMC2209 (UART)

## Hotends

- 2 × Hotends cerâmicos
- Sensores PT100
- Temperatura máxima: **320 °C**

## Sensor de nivelamento

- Sensor indutivo industrial AECO
- Corpo M8
- Saída PNP
- Montado entre os dois hotends

## Sensores

- ADXL345
- MPU6050 (reserva)

## Câmeras

- Webcam USB 1,3 MP
- Powerpack VX-8

---

# 💻 Software

- Klipper
- Moonraker
- Fluidd
- OrcaSlicer
- Obico

---

# 🚀 Recursos Planejados

## Impressão

- Pressure Advance
- Input Shaper
- Bed Mesh
- Adaptive Mesh
- PID Automático
- Auto Z Offset

## Monitoramento

- Webcam
- Timelapse
- Obico
- Monitoramento remoto

## Automação

- Controle inteligente dos ventiladores
- LEDs automáticos
- Macros inteligentes
- Diagnóstico automático
- Backup automático

---

# 📁 Estrutura do Repositório

```text
QIDI-XPRO-Rebuild/
│
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
│
├── docs/
├── hardware/
├── klipper/
├── cad/
├── scripts/
├── backups/
└── images/
```

---

# 📂 Estrutura dos Arquivos Klipper

```text
klipper/
│
├── printer.cfg
├── mcu.cfg
├── steppers.cfg
├── extruders.cfg
├── heaters.cfg
├── probe.cfg
├── bed_mesh.cfg
├── fans.cfg
├── leds.cfg
├── camera.cfg
├── input_shaper.cfg
├── pressure_advance.cfg
├── macros.cfg
└── backup/
```

---

# 🏗 Filosofia do Projeto

Este projeto segue alguns princípios fundamentais.

## Confiabilidade

Nenhuma ligação elétrica será realizada sem validação prévia.

## Documentação

Toda modificação será registrada.

## Modularidade

Toda configuração do Klipper será organizada em arquivos independentes.

## Reprodutibilidade

Qualquer pessoa deverá conseguir reproduzir este retrofit utilizando apenas esta documentação.

---

# 📈 Melhorias em relação ao equipamento original

| Original | Retrofit |
|-----------|-----------|
| Firmware proprietário | Klipper |
| Software antigo | OrcaSlicer |
| Interface limitada | Fluidd |
| Controle remoto limitado | Obico |
| Sem Input Shaper | ADXL345 |
| Eletrônica proprietária | Manta M8P |
| Configuração fechada | Totalmente aberta |
| Calibração limitada | Bed Mesh + Input Shaper |

---

# 📅 Roadmap

## Fase 1 — Plataforma

- Instalação da Manta M8P
- Instalação do CB1
- Instalação do Debian
- Instalação do Klipper
- Instalação do Moonraker
- Instalação do Fluidd

---

## Fase 2 — Hardware

- Motores
- Hotends
- Mesa aquecida
- Ventiladores
- Sensores

---

## Fase 3 — Calibração

- PID
- Pressure Advance
- Input Shaper
- Bed Mesh
- Auto Z Offset

---

## Fase 4 — Recursos Avançados

- Webcam
- Timelapse
- Obico
- LEDs automáticos

---

## Fase 5 — Otimização

- Benchmark
- Ajustes finos
- Documentação final

---

# 🔮 Melhorias Futuras

- Sensor de temperatura da câmara
- Dashboard de manutenção
- Integração com Home Assistant
- Diagnóstico dos TMC2209
- Estatísticas da impressora
- Atualizações automáticas
- Monitoramento da eletrônica

---

# 🤝 Contribuições

Sugestões, melhorias e correções são muito bem-vindas.

Caso encontre algum problema ou tenha alguma ideia para melhorar o projeto, abra uma *Issue* ou envie um *Pull Request*.

---

# 📜 Licença

Este projeto é distribuído sob a licença **MIT**.

---

# ⚠ Aviso

Este projeto envolve modificações elétricas e mecânicas na impressora.

Toda alteração é realizada por conta e risco do usuário.

Antes de energizar qualquer circuito:

- confira toda a fiação;
- valide as tensões de alimentação;
- confirme a configuração do firmware;
- execute os testes recomendados na documentação.

---

# 🙏 Agradecimentos

Agradecimentos à comunidade do Klipper, BIGTREETECH e a todos os desenvolvedores que contribuem para o ecossistema Open Source de impressão 3D.

---

> **Objetivo final:** transformar uma QIDI X-Pro em uma plataforma moderna, confiável, totalmente documentada e preparada para futuras evoluções.