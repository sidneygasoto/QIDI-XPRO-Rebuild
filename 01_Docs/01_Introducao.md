# Introdução

> Projeto: Retrofit Completo da QIDI X-Pro

**Versão:** 0.1.0
**Última atualização:** 2026-07-06
**Status:** Em desenvolvimento

---

# Objetivo

Este documento apresenta a visão geral do projeto, seus objetivos, escopo, filosofia de engenharia e os critérios adotados durante o desenvolvimento.

O retrofit da QIDI X-Pro não tem como finalidade apenas substituir componentes eletrônicos, mas transformar a impressora em uma plataforma moderna, aberta, confiável e completamente documentada.

Todo o desenvolvimento será conduzido como um projeto de engenharia, priorizando decisões técnicas fundamentadas, validação experimental e documentação contínua.

---

# Motivação

A QIDI X-Pro é uma impressora mecanicamente robusta e possui excelente qualidade construtiva. Entretanto, sua eletrônica e software apresentam limitações quando comparados às plataformas atuais.

Entre essas limitações destacam-se:

- firmware proprietário;
- pouca flexibilidade para expansões;
- limitações de configuração;
- dificuldade de manutenção;
- documentação limitada;
- baixa integração com ferramentas modernas.

Ao invés de substituir toda a impressora, este projeto busca preservar sua estrutura mecânica e atualizar completamente sua plataforma eletrônica e de controle.

---

# Objetivos do Retrofit

Os principais objetivos deste projeto são:

- substituir toda a eletrônica original;
- migrar para Klipper;
- utilizar hardware aberto;
- facilitar futuras manutenções;
- melhorar a qualidade das impressões;
- aumentar a confiabilidade do equipamento;
- simplificar futuras expansões;
- produzir documentação técnica completa;
- criar um projeto totalmente reproduzível.

---

# Escopo

Este projeto contempla:

## Hardware

- substituição da placa controladora;
- substituição do computador embarcado;
- substituição dos drivers dos motores;
- atualização do sistema de aquecimento;
- atualização do sistema de controle;
- integração de novos sensores;
- melhoria do sistema de ventilação;
- instalação de iluminação controlada.

---

## Software

Serão utilizados exclusivamente softwares amplamente conhecidos pela comunidade de impressão 3D.

Principais componentes:

- Klipper
- Moonraker
- Fluidd
- OrcaSlicer
- Obico

Integrações futuras:

- Home Assistant
- monitoramento remoto;
- automação residencial;
- backup automático;
- diagnóstico remoto.

---

# Filosofia do Projeto

O projeto será conduzido seguindo os princípios abaixo.

## 1. Engenharia antes da velocidade

Nenhuma modificação será realizada apenas por tentativa.

Toda alteração deverá possuir justificativa técnica.

---

## 2. Validação Experimental

Nenhuma informação será considerada correta apenas porque aparece em documentação ou fóruns.

Sempre que possível será realizada validação prática.

Exemplos já realizados:

- validação do slot correto de boot do CB1;
- validação da comunicação SPI;
- validação do acesso SSH;
- validação da alimentação da plataforma.

---

## 3. Documentação Contínua

Toda etapa será documentada.

Toda descoberta será registrada.

Toda decisão será justificada.

O objetivo é que qualquer pessoa consiga reproduzir integralmente este retrofit.

---

## 4. Manutenção Simplificada

Sempre que existirem múltiplas soluções tecnicamente equivalentes, será escolhida aquela que apresentar:

- menor complexidade;
- maior disponibilidade de peças;
- menor custo de manutenção;
- maior confiabilidade.

---

## 5. Segurança

Nenhum hardware será energizado sem checklist.

Toda ligação elétrica será revisada antes da energização.

Sempre que necessário serão realizados testes individuais antes da montagem definitiva.

---

# Arquitetura Geral

A arquitetura definida para o retrofit é composta por:

## Controladora

- BIGTREETECH Manta M8P V2.0

Responsável pelo controle em tempo real da impressora.

---

## Computador Embarcado

- BIGTREETECH CB1 V2.2

Responsável por executar:

- Debian 13;
- Klipper Host;
- Moonraker;
- Fluidd;
- Obico.

---

## Drivers

- 5 × TMC2209 em modo UART.

---

## Sistema Mecânico

Será preservada a mecânica original da QIDI X-Pro.

A arquitetura permanecerá:

- dois extrusores;
- dois hotends;
- um único carro de impressão.

Não será realizada conversão para IDEX.

---

## Hotends

Serão utilizados:

- dois Trianglelab Ceramic Hotend (originais);
- sensores de temperatura NTC100;
- temperatura máxima de operação de 320 °C.

---

## Sensor de Nivelamento

Será mantido o sensor atualmente instalado:

- AECO industrial;
- M8;
- saída PNP.

Sua repetibilidade será validada futuramente utilizando o comando `PROBE_ACCURACY`.

---

## Sensores de Movimento

Principal:

- ADXL345 (SPI)

Reserva:

- MPU6050 (I²C)

---

# Organização da Documentação

Toda a documentação está organizada por assunto.

Cada documento possui um objetivo específico.

| Documento | Finalidade |
|-----------|------------|
| 00_Roadmap.md | Planejamento geral |
| 02_Plataforma_CB1.md | Sistema operacional e configuração do CB1 |
| 03_Manta_M8P.md | Caracterização da controladora |
| 04_Backups.md | Histórico dos backups |
| 05_Instalacao_Klipper.md | Instalação do Klipper |
| 06_Hardware_QIDI.md | Inventário da impressora |
| 07_Esquema_Eletrico.md | Diagramas elétricos |
| 08_Klipper_Configuration.md | Arquivos de configuração |
| 09_Macros.md | Macros do Klipper |
| 10_Calibracao.md | Procedimentos de calibração |
| 11_Problemas_Conhecidos.md | Registro de problemas e soluções |
| 12_Referencias.md | Datasheets e referências |

---

# Metodologia de Trabalho

Cada etapa seguirá o mesmo fluxo:

1. Planejamento.
2. Execução.
3. Validação.
4. Documentação.
5. Backup.
6. Próxima etapa.

Essa metodologia garante que o estado da documentação reflita exatamente o estado físico da impressora.

---

# Estado Atual do Projeto

Atualmente encontram-se concluídos:

- arquitetura do retrofit;
- definição dos principais componentes;
- instalação do Debian 13 no CB1;
- atualização completa do sistema operacional;
- validação da comunicação Ethernet;
- validação do acesso SSH;
- validação do barramento SPI;
- criação do Backup_0.

O projeto encontra-se pronto para iniciar a instalação do ecossistema Klipper.

---

# Público-Alvo

Esta documentação destina-se a:

- proprietários da QIDI X-Pro;
- entusiastas de Klipper;
- estudantes;
- pesquisadores;
- profissionais da área de automação;
- makers interessados em retrofits de impressoras 3D.

---

# Considerações Finais

Este projeto busca demonstrar que é possível prolongar significativamente a vida útil de equipamentos de boa qualidade mecânica através da substituição criteriosa de sua eletrônica e software.

Mais do que um guia de montagem, esta documentação pretende servir como referência técnica para projetos semelhantes, incentivando o uso de hardware aberto, documentação de qualidade e boas práticas de engenharia.