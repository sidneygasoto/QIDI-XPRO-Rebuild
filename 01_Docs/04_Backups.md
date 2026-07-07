# Backup_0 - Comissionamento da Plataforma Computacional (CB1)

> Estado inicial validado da BIGTREETECH CB1 antes da instalação do Klipper.

---

# Objetivo

Este documento descreve o procedimento completo para instalação, atualização e validação da plataforma computacional utilizada no retrofit da QIDI X-Pro.

Ao final deste procedimento é recomendado gerar uma imagem completa do cartão microSD, denominada **Backup_0**, que servirá como ponto de restauração do sistema operacional.

---

# Hardware utilizado

## Controladora

- BIGTREETECH Manta M8P V2.0

## Módulo computacional

- BIGTREETECH CB1 V2.2

## Cartão microSD

- SanDisk Extreme PRO
- 64 GB
- 200 MB/s leitura
- 90 MB/s gravação

---

# Sistema Operacional

Imagem utilizada:

```
CB1_Debian13_minimal_kernel7.0_20260430
```

Motivos da escolha:

- sistema mínimo;
- maior controle da instalação;
- ausência de softwares desnecessários;
- documentação reproduzível.

---

# Gravação da imagem

Gravar a imagem no cartão microSD utilizando o software de sua preferência.

Exemplos:

- Raspberry Pi Imager
- balenaEtcher
- Rufus

---

# Slot correto do cartão microSD

A Manta M8P possui dois leitores microSD.

Apesar dos nomes dos slots gerarem dúvidas, o cartão contendo o sistema operacional deve ser instalado em:

```
SoC-SD
```

O slot:

```
MCU-SD
```

é destinado ao STM32.

> **Observação**

A documentação oficial não explica claramente essa diferença, o que pode causar confusão durante a primeira inicialização.

---

# Primeiro Boot

Conectar:

- alimentação;
- cabo Ethernet.

Opcionalmente:

- monitor HDMI;
- teclado USB.

Embora possam ser conectados para testes, nesta versão da imagem eles não foram utilizados durante o processo de configuração.

# Acesso inicial

Embora o CB1 possua saídas HDMI e suporte a dispositivos USB, **a imagem utilizada neste projeto não apresentou interface local durante o primeiro boot**.

Durante os testes realizados:

- monitor HDMI conectado;
- teclado USB conectado;
- ambas as saídas HDMI testadas;

não foi exibida nenhuma imagem na tela e não foi possível acessar um terminal local.

Entretanto, o sistema operacional inicializou normalmente.

A confirmação foi feita através de:

- resposta ao comando `ping`;
- conexão via SSH utilizando o PuTTY.

Portanto, **todo o processo de instalação, atualização e configuração descrito neste documento foi realizado exclusivamente por acesso remoto via SSH**.

> **Observação**
>
> Esse comportamento foi observado especificamente com a imagem:
>
> `CB1_Debian13_minimal_kernel7.0_20260430`
>
> Não significa necessariamente que outras imagens da BIGTREETECH apresentem o mesmo comportamento.

# Login

Na imagem utilizada, as credenciais padrão são:

Usuário

```
root
```

Senha

```
root
```

> **Importante**

O manual da BIGTREETECH ainda informa:

```
Usuário: biqu
Senha: biqu
```

Entretanto, para a imagem

```
CB1_Debian13_minimal_kernel7.0_20260430
```

as credenciais corretas são:

```
root / root
```

---

# Verificação da versão do sistema

Executar:

```bash
cat /etc/os-release
```

Resultado esperado:

- Debian 13 (Trixie)
- Base Armbian
- BIGTREETECH CB1

---

Executar:

```bash
uname -a
```

Resultado esperado:

```
Linux 7.0.2-vendor-sunxi64
```

---

Executar:

```bash
hostnamectl
```

Resultado esperado:

Hostname:

```
bigtreetech-cb1
```

---

# Verificação do armazenamento

Executar:

```bash
lsblk -f
```

Resultado esperado:

- partição BOOT em FAT16;
- partição ROOT em ext4;
- expansão automática do cartão.

---

Executar:

```bash
df -h
```

Resultado esperado:

Partição raiz próxima de:

```
58 GB
```

Espaço livre:

```
≈56 GB
```

---

# Verificação da memória

Executar:

```bash
free -h
```

Resultado esperado:

- aproximadamente 1 GB RAM;
- swap em ZRAM.

---

# Verificação da rede

Executar:

```bash
ip -br addr
```

Resultado esperado:

Interface Ethernet ativa.

---

# Verificação dos serviços

Executar:

```bash
systemctl --failed
```

Resultado esperado:

```
0 loaded units listed.
```

---

# Atualização do sistema

Atualizar a lista de pacotes:

```bash
apt update
```

Em seguida:

```bash
apt full-upgrade
```

Após a atualização:

```bash
apt autoremove
```

Reiniciar:

```bash
reboot
```

---

# Mensagem durante update-initramfs

Durante a atualização poderá aparecer:

```
ln: failed to create symbolic link '/boot/uInitrd': Operation not permitted
```

Essa mensagem é esperada.

Motivo:

A partição

```
/boot
```

utiliza FAT16.

O sistema FAT não suporta links simbólicos.

O script da Armbian detecta essa condição e automaticamente substitui o link simbólico por uma renomeação do arquivo.

Nenhuma intervenção é necessária.

---

# Validação após reinicialização

Executar:

```bash
uname -a
```

Confirmar:

```
Linux 7.0.2-vendor-sunxi64
```

---

Executar:

```bash
systemctl --failed
```

Resultado esperado:

```
0 loaded units listed.
```

---

Executar:

```bash
df -h /boot
```

Confirmar montagem correta da partição BOOT.

---

# Recursos já configurados pela imagem

A imagem oficial da BIGTREETECH apresenta diversas otimizações já habilitadas.

## ZRAM

Swap totalmente em memória.

Benefícios:

- menor desgaste do cartão microSD;
- melhor desempenho.

---

## Log2RAM

Diretório:

```
/var/log
```

mantido em memória RAM.

Benefícios:

- reduz significativamente as gravações no cartão;
- aumenta a vida útil do microSD.

---

## Expansão automática

Na primeira inicialização a partição principal é expandida automaticamente para utilizar praticamente todo o cartão microSD.

Nenhuma ação manual é necessária.

---

# Estado final do sistema

Após concluir todas as etapas, o sistema deverá apresentar:

| Item | Status |
|-------|:------:|
| Debian 13 atualizado | ✅ |
| Kernel 7.0.2 | ✅ |
| Boot validado | ✅ |
| SSH funcional | ✅ |
| Ethernet funcional | ✅ |
| Partição expandida | ✅ |
| ZRAM | ✅ |
| Log2RAM | ✅ |
| Serviços com falha | 0 |

---

# Backup_0

Neste ponto recomenda-se criar uma imagem completa do cartão microSD.

Este backup representa o estado inicial da plataforma computacional.

Nenhum software específico da impressora (Klipper, Moonraker, Fluidd ou firmware STM32) foi instalado.

Este backup servirá como ponto oficial de restauração do projeto.

---

# Próxima etapa

A próxima fase do retrofit consiste em:

- configuração regional;
- configuração do SSH;
- levantamento dos GPIOs do CB1;
- documentação dos periféricos;
- instalação do Klipper;
- instalação do Moonraker;
- instalação do Fluidd.