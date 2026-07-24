# Câmera

## Objetivo

Esta etapa documenta a instalação e configuração de uma câmera USB para utilização com o sistema **Klipper**, integrada ao **Moonraker** e à interface **Fluidd**.

O objetivo é disponibilizar streaming de vídeo para monitoramento da impressão e suporte a recursos que utilizam captura de imagem.

---

## Escopo

Esta documentação contempla:

- Instalação do **camera-streamer**;
- Compilação do software no **BIGTREETECH CB1**;
- Configuração do serviço `systemd`;
- Integração com o Moonraker;
- Configuração do Fluidd;
- Validação do streaming;
- Registro dos testes realizados.

---

## Ambiente

### Hardware

- Impressora QIDI X-Pro (Retrofit)
- BIGTREETECH Manta M8P V2.0
- BIGTREETECH CB1 V2.2
- Câmera USB compatível com V4L2

### Software

- Debian 13
- Klipper
- Moonraker
- Fluidd

---

## Estrutura da documentação

| Documento | Descrição |
|-----------|-----------|
| `01_Installing_Camera_Streamer.md` | Instalação, compilação e validação do camera-streamer. |
| `02_Systemd_Service.md` | Configuração do serviço responsável pelo streaming. |
| `03_Fluidd_Configuration.md` | Integração com Moonraker e Fluidd. |
| `04_Testing.md` | Registro dos testes realizados e respectivas validações. |

---

## Status

| Etapa | Situação |
|:------|:--------:|
| Compilação do camera-streamer | ✅ |
| Validação do executável | ✅ |
| Configuração do serviço `systemd` | ⏳ |
| Integração com Moonraker | ⏳ |
| Configuração do Fluidd | ⏳ |
| Validação do streaming | ⏳ |

---

## Observações

Durante o desenvolvimento foi utilizada uma webcam USB apenas para validação da infraestrutura e da compilação do **camera-streamer**.

A validação final do streaming será realizada com a câmera definitiva do projeto.

---

## Próxima Etapa

Prosseguir com a criação e configuração do serviço `camera-streamer.service`, seguida da integração com o Moonraker e o Fluidd.