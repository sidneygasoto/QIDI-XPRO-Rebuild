# Changelog

Todas as mudanças relevantes deste projeto serão documentadas neste arquivo.

Este projeto segue o padrão **Keep a Changelog** e utiliza **Semantic Versioning (SemVer)**.

---

# [0.1.0] - 2026-07-06

## Foundation

Primeira versão documentada do projeto.

Representa a conclusão da preparação da plataforma de hardware e software necessária para iniciar o retrofit da QIDI X-Pro.

---

## Added

### Estrutura do Projeto

- Definida a estrutura oficial do repositório GitHub.
- Definida a organização da documentação técnica.
- Definido o fluxo de documentação baseado em pacotes.
- Definido o versionamento utilizando Semantic Versioning (SemVer).
- Definida a filosofia de documentação contínua.

---

### Hardware

#### Controladora

- BIGTREETECH Manta M8P V2.0.

#### Host

- BIGTREETECH CB1 V2.2.

#### Drivers

- 5 × TMC2209 em modo UART.

#### Hotends

Substituição dos hotends originais por:

- 2 × Trianglelab Ceramic Hotend.
- Sensores NTC100.
- Temperatura máxima de 320 °C.

#### Sensor de Nivelamento

- Sensor indutivo industrial AECO.
- Sensor instalado entre os dois hotends.
- Distância de detecção aproximada de 0,9 mm sobre a chapa PEI.

#### Iluminação

Adicionada placa desenvolvida especificamente para o projeto contendo:

- três LEDs brancos;
- resistores de 100 Ω;
- montagem entre os hotends.

---

### Arquitetura

Foi definida a manutenção da arquitetura original da impressora:

- Dual Extruder.
- Mesmo carro de impressão.
- Sem conversão para IDEX.

---

### Sistema Operacional

Instalada imagem:

```
CB1_Debian13_minimal_kernel7.0_20260430
```

Características:

- Debian 13 (Trixie)
- Kernel 7.0.2-vendor-sunxi64

---

### Atualizações

Realizada atualização completa do sistema operacional.

Todos os pacotes atualizados com sucesso.

Nenhum serviço apresentou falhas após reinicialização.

---

### Descobertas Técnicas

#### Slot de Boot

Foi validado experimentalmente que o CB1 inicializa utilizando o slot:

```
SoC-SDcard
```

Apesar da nomenclatura da placa sugerir interpretação diferente.

Esta descoberta será detalhada na documentação da plataforma.

---

#### Login

Na imagem utilizada, o acesso SSH ocorre utilizando:

Usuário:

```
root
```

Senha:

```
root
```

O usuário "biqu", citado em parte da documentação da BIGTREETECH, não está disponível nesta versão da imagem.

---

#### Interfaces validadas

Foram confirmados:

- Ethernet
- SSH
- SPI
- I²C
- UART
- GPIO
- ZRAM
- log2ram

---

#### SPI

Foi habilitado utilizando o overlay oficial:

```
spidev0_0
```

Após reinicialização foi validada a criação do dispositivo:

```
/dev/spidev0.0
```

O barramento será utilizado pelo ADXL345.

---

### Backups

Criado:

```
Backup_0
```

Conteúdo:

- Debian instalado.
- Sistema atualizado.
- SPI habilitado.
- Comunicação Ethernet validada.
- Acesso SSH validado.
- Plataforma pronta para instalação do Klipper.

---

## Documentation

Criados os documentos:

- README.md
- CHANGELOG.md
- Roadmap do projeto
- Introdução
- Documentação da plataforma CB1
- Documentação da Manta M8P
- Histórico de backups

---

## Next Milestone

Versão prevista:

```
0.2.0
```

Objetivos:

- Instalação do Klipper.
- Instalação do Moonraker.
- Instalação do Fluidd.
- Compilação do firmware da Manta M8P.
- Primeira comunicação entre CB1 e STM32.

---

## Histórico de Versões

| Versão | Descrição |
|---------|-----------|
| 0.1.0 | Foundation |