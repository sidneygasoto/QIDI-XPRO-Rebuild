# Retrofit Completo da QIDI X-Pro

> Modernização completa da impressora 3D QIDI X-Pro utilizando hardware aberto, Klipper e uma arquitetura orientada à confiabilidade, manutenção e documentação.

![Status](https://img.shields.io/badge/status-Em%20Desenvolvimento-orange)
![Version](https://img.shields.io/badge/version-0.1.0-blue)
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
| Sensor de temperatura | PTC100 |
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
- Sensores PTC100
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

# Iluminação

Foi desenvolvida uma placa exclusiva para este projeto contendo:

- três LEDs brancos;
- resistores de 100 Ω;
- montagem entre os dois hotends.

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

Toda a documentação técnica encontra-se na pasta **docs/**.

| Documento | Conteúdo |
|------------|----------|
| 00_Roadmap.md | Planejamento geral do projeto |
| 01_Introducao.md | Objetivos e filosofia |
| 02_Plataforma_CB1.md | Sistema operacional e configuração do CB1 |
| 03_Manta_M8P.md | Configuração da controladora |
| 04_Backups.md | Histórico dos backups |
| 05_Instalacao_Klipper.md | Instalação do Klipper |
| 06_Hardware_QIDI.md | Inventário da impressora |
| 07_Esquema_Eletrico.md | Esquemas elétricos |
| 08_Klipper_Configuration.md | Configuração do Klipper |
| 09_Macros.md | Macros do Klipper |
| 10_Calibracao.md | Procedimentos de calibração |
| 11_Problemas_Conhecidos.md | Registro de problemas e soluções |
| 12_Referencias.md | Datasheets e referências |

---

# Estrutura do Repositório

```text
QIDI-X-Pro-Retrofit/

├── README.md
├── CHANGELOG.md
├── LICENSE
├── docs/
├── firmware/
├── klipper_config/
├── cad/
├── stl/
├── images/
└── backups/
```

---

# Situação Atual

## Concluído

- Definição da arquitetura do retrofit.
- Instalação do Debian 13 Minimal no CB1.
- Atualização completa do sistema operacional.
- Validação da comunicação Ethernet.
- Acesso remoto via SSH.
- Validação do funcionamento do SPI.
- Criação do Backup_0.

---

## Em andamento

- Instalação do ecossistema Klipper.
- Caracterização completa da Manta M8P.
- Inventário da QIDI X-Pro.

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

**Versão do documento:** 0.1.0

**Última atualização:** 2026-07-06