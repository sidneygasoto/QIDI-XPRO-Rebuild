# Retrofit Completo da QIDI X-Pro

> Modernização completa da impressora 3D QIDI X-Pro utilizando hardware aberto, Klipper e uma arquitetura orientada à confiabilidade, manutenção e documentação.

![Status](https://img.shields.io/badge/status-Em%20Desenvolvimento-orange)
![Version](https://img.shields.io/badge/version-0.3.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

# Sobre o Projeto

Este projeto tem como objetivo realizar um **retrofit completo** da impressora **QIDI X-Pro**, substituindo toda a eletrônica original por uma plataforma moderna baseada em **Klipper**.

O foco não é apenas atualizar a impressora, mas desenvolver uma plataforma robusta, confiável e totalmente documentada, utilizando componentes amplamente disponíveis e soluções de hardware aberto.

Todo o desenvolvimento é realizado seguindo princípios de engenharia, com validação prática de cada etapa, documentação detalhada das decisões técnicas e criação de backups em marcos importantes do projeto.

---

# Objetivos

- Modernizar completamente a eletrônica da impressora.
- Utilizar exclusivamente hardware aberto sempre que possível.
- Melhorar a confiabilidade do equipamento.
- Facilitar futuras manutenções.
- Melhorar a qualidade de impressão.
- Criar uma documentação completa do retrofit.
- Disponibilizar um projeto totalmente reproduzível.

---

## Componentes Principais

| Componente | Modelo |
|------------|--------|
| Controladora | BIGTREETECH Manta M8P V2.0 |
| Host | BIGTREETECH CB1 V2.2 |
| Drivers | TMC2209 UART |
| Hotends | Trianglelab Ceramic Hotend |
| Sensor de temperatura | NTC100 |
| Sensor de nivelamento | AECO M8 PNP |
| Acelerômetro principal | ADXL345 |
| Acelerômetro reserva | MPU6050 |

---

# Configuração Mecânica

A arquitetura mecânica original da QIDI X-Pro será preservada.

Características:

- Dois hotends independentes.
- Dois extrusores independentes.
- Mesmo carro de impressão.
- Arquitetura Dual Extruder original.

Não será realizada conversão para IDEX.

---

# Hotends

Os hotends originais foram substituídos por:

- 2 × Trianglelab Ceramic Hotend
- Sensores NTC100
- Temperatura máxima de 320 °C

---

# Sensor de Nivelamento

Será utilizado um sensor indutivo industrial da AECO.

Características:

- M8
- Saída PNP
- Instalação entre os dois hotends
- Distância de detecção aproximada de 0,9 mm sobre a chapa PEI original

Após a montagem será executado:

- PROBE_ACCURACY

para validação da repetibilidade.

---

# Iluminação em baixo dos Hotends

Foi desenvolvida uma placa exclusiva para este projeto contendo:

- três LEDs brancos;
- resistores de 100 Ω;
- montagem entre os dois hotends.
- Alimentada por 5V - PWM, controlada por `tool_light` (PF8)
- Iluminação de gabinete separada em `cabin_light` (PA4)

Objetivos:

- melhorar a visualização da impressão;
- auxiliar o Obico;
- melhorar a qualidade das imagens da câmera.

---

# Sensores

## Principal

- ADXL345 (SPI)

## Reserva

- MPU6050 (I²C)

---

# Câmeras

Disponíveis:

- Webcam USB 1,3 MP
- Powerpack VX-8

Inicialmente será utilizada a webcam USB devido à maior compatibilidade com Linux.

---

# Software

O sistema será composto por:

- Klipper
- Moonraker
- Fluidd
- OrcaSlicer
- Obico

Integrações futuras:

- Home Assistant
- Dashboard de diagnóstico
- Backup automático
- Monitoramento dos drivers TMC2209

---

# Organização da Documentação

Toda a documentação técnica encontra-se em **`01_Docs/`**. Documentos previstos e ainda não
criados aparecem como pendentes.

| Documento | Conteúdo | Situação |
|------------|----------|:--------:|
| 00_Roadmap.md | Planejamento geral do projeto | ✅ |
| 01_Introducao.md | Objetivos e filosofia | ✅ |
| 02_Plataforma_CB1.md | Sistema operacional e configuração do CB1 | ✅ |
| 03_Klipper_Moonraker_Fluidd.md | Instalação da stack de software | ✅ |
| 04_Backups.md | Histórico dos backups | ✅ |
| 05_Metrology_Architecture.md | Arquitetura da extensão de metrologia | ✅ |
| 03_Manta_M8P.md | Caracterização da controladora | ⏳ |
| 06_Hardware_QIDI.md | Inventário da impressora | ⏳ |
| 07_Bed_Mesh.md | Diagnóstico e calibração do bed mesh | ✅ |
| 08_Klipper_Configuration.md | Configuração do Klipper | ⏳ |
| 09_Macros.md | Macros do Klipper | ⏳ |
| 10_Calibracao.md | Procedimentos de calibração | ⏳ |
| 11_Problemas_Conhecidos.md | Registro de problemas e soluções | ⏳ |
| 12_Referencias.md | Datasheets e referências | ⏳ |
| 14_Esquema_Eletrico.md | Esquemas elétricos | ⏳ |

A configuração operacional **não** fica em `01_Docs/`: ela é versionada em
[`03_Klipper_Config/`](03_Klipper_Config/README.md), espelho da CB1.

---

# Estrutura do Repositório

```text
QIDI-XPRO-Rebuild/

├── 00_Estado_Atual.md      ← estado verificado da máquina
├── README.md  CHANGELOG.md  releases.md  LICENSE
├── 01_Docs/                ← documentação técnica
├── 03_Klipper_Config/      ← configuração ativa (espelho da CB1)
├── 05_Metrology/           ← extensão de metrologia + proveniência
├── 06_Firmware/            ← bootloader e binários
├── 07_Backup/              ← Backup_0 e snapshots de configuração
├── 08_Fotos/  10_Datasheets/
├── 11_Config_qidi_xpro/    ← moonraker, nginx, systemd, firmware
├── 12_BKP_chat/  13_Camera/
└── 02_Esquemas/  03_CAD/  04_STL/  09_Testes/   (vazias)
```

---

# Situação Atual

**v0.3.0 — Produção validada.** O estado detalhado e verificado está em
[`00_Estado_Atual.md`](00_Estado_Atual.md).

## Concluído

- Arquitetura do retrofit e definição dos componentes.
- Debian 13 no CB1, rede, SSH e SPI validados.
- Klipper, Moonraker, Fluidd e Nginx operacionais.
- Comunicação CB1 ↔ STM32H723; firmware `v0.13.0-701` idêntico ao versionado.
- Cinco TMC2209 em UART; dois hotends independentes; mesa e ventoinhas.
- Endstops mecânicos em X/Y/Z, sonda indutiva e `z_offset` calibrado.
- PID dos dois hotends e da mesa; Input Shaper; `rotation_distance`; offsets T1; PA.
- Iluminação de ferramenta e de gabinete implementada.
- Impressão em produção desde outubro de 2026.
- Configuração real versionada em `03_Klipper_Config/`.

## Em andamento

- Consistência do bed mesh (limites e aplicação no start G-code).
- Extensão de metrologia: refatoração interrompida, não carregável.
- Câmera: aguardando hardware UVC com MJPEG.

---

# Filosofia do Projeto

Este projeto segue algumas regras fundamentais:

- Nunca energizar hardware sem checklist.
- Nunca assumir pinagens sem confirmação.
- Validar experimentalmente todas as conexões.
- Documentar todas as decisões técnicas.
- Comentar integralmente os arquivos de configuração.
- Priorizar soluções robustas e de fácil manutenção.

---

# Licença

Este projeto é distribuído sob a licença MIT.

Consulte o arquivo `LICENSE` para mais informações.

---

# Agradecimentos

Agradecemos às comunidades de software e hardware livre que tornam projetos como este possíveis, especialmente aos desenvolvedores do Klipper, Moonraker, Fluidd e aos fabricantes que disponibilizam documentação técnica aberta.

---

**Versão do documento:** 0.3.0

**Última atualização:** 2026-10-25