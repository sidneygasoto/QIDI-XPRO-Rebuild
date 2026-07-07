# Plataforma CB1

> Projeto: Retrofit Completo da QIDI X-Pro

**Documento:** 02_Plataforma_CB1.md
**Versão:** 0.1.0
**Última atualização:** 2026-07-06

**Relacionado a:**

- README.md
- CHANGELOG.md
- docs/00_Roadmap.md
- docs/03_Manta_M8P.md
- docs/04_Backups.md

---

# Objetivo

Este documento registra a caracterização técnica da plataforma computacional utilizada no retrofit da QIDI X-Pro.

Diferentemente de um tutorial de instalação, este documento tem como objetivo documentar todas as evidências experimentais obtidas durante a configuração do sistema, permitindo a reprodução do ambiente e servindo como referência técnica para futuras manutenções.

Todas as conclusões apresentadas neste documento são baseadas em testes executados na plataforma física utilizada neste projeto.

---

# Plataforma Utilizada

## Hardware

| Item | Especificação |
|------|---------------|
| Computador | BIGTREETECH CB1 |
| Revisão | V2.2 |
| Processador | Allwinner H616 |
| Arquitetura | ARM Cortex-A53 (64 bits) |
| Memória RAM | 1 GB |
| Sistema Operacional | Debian 13 (Trixie) |
| Kernel | 7.0.2-vendor-sunxi64 |

---

## Armazenamento

| Item | Especificação |
|------|---------------|
| Cartão | SanDisk Extreme PRO |
| Capacidade | 64 GB |
| Leitura | até 200 MB/s |
| Gravação | até 90 MB/s |

A utilização de um cartão de alto desempenho foi escolhida para reduzir o tempo de boot, melhorar o desempenho do sistema de arquivos e aumentar a confiabilidade da plataforma.

---

# Objetivos da Plataforma

O CB1 será responsável por executar todos os serviços de alto nível da impressora.

Entre eles:

- Klipper Host;
- Moonraker;
- Fluidd;
- Obico (futuramente);
- gerenciamento da comunicação USB com a MCU;
- Input Shaper;
- gerenciamento das interfaces de rede.

A controladora BIGTREETECH Manta M8P permanecerá responsável exclusivamente pelo controle em tempo real da impressora.

---

# Caracterização da Plataforma

Esta seção registra o estado da plataforma imediatamente após sua instalação e atualização.

Todas as informações abaixo foram obtidas diretamente da plataforma através de comandos executados durante este projeto.

---

# Sistema Operacional

## Objetivo

Identificar a versão exata do sistema operacional instalado.

---

## Procedimento Experimental

Comando executado:

```bash
cat /etc/os-release
```

---

## Evidência Experimental

```text
PRETTY_NAME="BIGTREETECH-CB1 3.1.0-26.05.0-trunk trixie"
NAME="Debian GNU/Linux"
VERSION_ID="13"
VERSION="13 (trixie)"
VERSION_CODENAME=trixie
DEBIAN_VERSION_FULL=13.4
ID=debian
HOME_URL="https://duckduckgo.com/"
SUPPORT_URL="https://community.armbian.com/"
BUG_REPORT_URL="https://armbian.atlassian.net/"
ARMBIAN_PRETTY_NAME="BIGTREETECH-CB1 3.1.0-26.05.0-trunk trixie"
```

---

## Análise

A imagem utilizada é baseada no Debian 13 (Trixie) e distribuída pela BIGTREETECH sobre a infraestrutura do Armbian.

Foi utilizada a imagem oficial:

```text
CB1_Debian13_minimal_kernel7.0_20260430
```

A escolha da versão **Minimal** foi motivada pela menor quantidade de serviços instalados, menor consumo de memória e menor atividade de escrita no cartão microSD.

---

## Conclusão

A imagem atende integralmente aos objetivos do projeto.

---

# Kernel

## Objetivo

Identificar a versão do kernel utilizada.

---

## Procedimento Experimental

```bash
uname -a
```

---

## Evidência Experimental

```text
Linux bigtreetech-cb1 7.0.2-vendor-sunxi64 #1 SMP PREEMPT Thu Apr 30 15:24:52 CST 2026 aarch64 GNU/Linux
```

---

## Análise

O sistema utiliza o kernel oficial disponibilizado pela BIGTREETECH para o processador Allwinner H616.

A arquitetura ARM64 é plenamente compatível com o ecossistema Klipper.

---

## Conclusão

Nenhuma alteração de kernel será necessária.

---

# Identificação da Plataforma

## Objetivo

Confirmar a identificação do equipamento e do hardware utilizado.

---

## Procedimento Experimental

```bash
hostnamectl
```

---

## Evidência Experimental

```text
Static hostname: bigtreetech-cb1
Operating System: BIGTREETECH-CB1 3.1.0-26.05.0-trunk trixie
Kernel: Linux 7.0.2-vendor-sunxi64
Architecture: arm64
```

---

### Modelo da Plataforma

Comando executado:

```bash
cat /proc/device-tree/model
```

Resultado:

```text
BigTreeTech CB1
```

---

### Compatibilidade

Comando executado:

```bash
cat /proc/device-tree/compatible
```

Resultado:

```text
bigtreetech,cb1
allwinner,sun50i-h616
```

---

## Análise

A plataforma foi corretamente identificada pelo sistema operacional.

Não foram observadas inconsistências entre o hardware instalado e a imagem utilizada.

---

## Conclusão

A instalação foi realizada utilizando a imagem apropriada para a revisão V2.2 do CB1.

---

# Processador

## Objetivo

Caracterizar o processador utilizado.

---

## Procedimento Experimental

Comando executado:

```bash
cat /proc/cpuinfo
```

---

## Evidência Experimental

Resumo dos resultados obtidos:

| Característica | Valor |
|----------------|-------|
| Núcleos | 4 |
| Arquitetura | ARMv8-A |
| Implementador | ARM |
| CPU | Cortex-A53 |
| Revisão | r0p4 |
| Recursos | AES, SHA1, SHA2, CRC32, PMULL |

---

## Análise

O processador Allwinner H616 possui quatro núcleos Cortex-A53 de 64 bits, oferecendo desempenho mais que suficiente para executar simultaneamente Klipper, Moonraker, Fluidd e os demais serviços previstos para este projeto.

Os recursos de aceleração por hardware para operações criptográficas também favorecem futuras integrações remotas, como VPNs e acesso seguro.

---

## Conclusão

Não há limitações de processamento para o escopo previsto do retrofit.

---

# Memória

## Objetivo

Caracterizar os recursos de memória disponíveis.

---

## Procedimento Experimental

Comando executado:

```bash
free -h
```

---

## Evidência Experimental

```text
               total        used        free      shared  buff/cache   available
Mem:           969Mi       126Mi       488Mi       3.2Mi       373Mi       843Mi
Swap:          484Mi          0B       484Mi
```

---

## Análise

A plataforma disponibiliza aproximadamente 1 GB de memória RAM.

O sistema utiliza ZRAM como área de swap comprimida, reduzindo significativamente gravações no cartão microSD.

Logo após a inicialização permanecem disponíveis aproximadamente 843 MiB de memória, indicando ampla margem para execução dos serviços previstos.

---

## Conclusão

A memória disponível é suficiente para todo o ecossistema planejado.

---

# Armazenamento

## Objetivo

Caracterizar a organização do armazenamento utilizado pelo sistema operacional.

---

## Procedimento Experimental

Comandos executados:

```bash
lsblk -f
```

```bash
df -h
```

---

## Evidência Experimental

### Estrutura dos dispositivos

```text
NAME        FSTYPE FSVER LABEL        UUID                                 MOUNTPOINTS

mmcblk0
├─mmcblk0p1 vfat   FAT16 BOOT         315E-2D5D                             /boot
└─mmcblk0p2 ext4   1.0   armbi_root   98a35c3f-0d3b-4eb6-984c-3205a7acd52d   /

zram0 swap
zram1 ext4 log2ram
zram2
```

---

### Utilização do sistema de arquivos

```text
Filesystem      Size  Used Avail Use%

/dev/mmcblk0p2   58G  1.9G   56G   4%
/dev/mmcblk0p1  256M   96M  161M  38%
```

---

## Análise

A imagem expande automaticamente a partição principal para toda a capacidade do cartão microSD.

O sistema ocupa aproximadamente **1,9 GB**, restando mais de **56 GB** livres.

A partição de boot permanece separada em FAT16, facilitando futuras manutenções e recuperação do sistema.

---

## Conclusão

Não será necessário redimensionamento de partições ou alterações na estrutura de armazenamento.

---

# Comunicação de Rede

## Objetivo

Verificar o funcionamento da interface Ethernet.

---

## Procedimento Experimental

Comando executado:

```bash
ip -br addr
```

---

## Evidência Experimental

```text
lo      UNKNOWN 127.0.0.1/8

eth0    UP
192.168.10.126/24

wlan0   DOWN
```

---

## Análise

A interface Ethernet foi reconhecida automaticamente.

O endereço IP foi obtido via DHCP.

Durante toda a configuração inicial não ocorreram perdas de comunicação SSH.

A interface Wi-Fi permaneceu desabilitada, uma vez que o projeto utilizará exclusivamente conexão cabeada.

---

## Conclusão

A interface Ethernet atende integralmente aos requisitos do projeto.

---

# Estado dos Serviços

## Objetivo

Verificar a integridade dos serviços do sistema.

---

## Procedimento Experimental

Comando executado:

```bash
systemctl --failed
```

---

## Evidência Experimental

```text
0 loaded units listed.
```

---

## Análise

Nenhum serviço apresentou falha após:

- instalação da imagem;
- atualização completa do sistema;
- reinicialização.

Esse resultado demonstra boa estabilidade da distribuição fornecida pela BIGTREETECH.

---

## Conclusão

A plataforma encontra-se operacional.

---

# Atualização do Sistema

## Objetivo

Atualizar completamente o sistema operacional antes da instalação do ecossistema Klipper.

---

## Procedimento Experimental

Foram executados os comandos:

```bash
apt update
```

```bash
apt full-upgrade
```

```bash
apt autoremove
```

---

## Evidências Experimentais

Durante a atualização observou-se:

- 72 pacotes atualizados;
- nenhuma interrupção;
- nenhuma dependência quebrada;
- nenhuma falha de serviço após reinicialização.

Também foi observada a atualização do Debian:

```text
Version 13.4 → 13.5
```

Foi registrada ainda a seguinte mensagem durante a reconstrução do initramfs:

```text
ln: failed to create symbolic link '/boot/uInitrd':
Operation not permitted
```

Em seguida o processo executou automaticamente:

```text
moving /boot/uInitrd...
done.
```

---

## Análise

Embora a criação do link simbólico tenha falhado, o próprio script do Armbian realizou automaticamente a substituição do arquivo.

Após reinicialização:

- sistema iniciou normalmente;
- kernel carregado corretamente;
- nenhum serviço apresentou falhas.

Trata-se de um comportamento esperado do processo de atualização utilizado pelo Armbian.

---

## Conclusão

A atualização foi concluída com sucesso.

---

# Gerenciamento de Memória

## Objetivo

Caracterizar os mecanismos utilizados para reduzir gravações no cartão microSD.

---

## Evidências Experimentais

Foi observada a existência de:

```text
zram0
```

destinado à área de swap.

Também foi identificado:

```text
zram1
```

montado em:

```text
/var/log
```

Além disso:

```text
/var/log.hdd
```

permanece disponível como armazenamento persistente.

---

## Análise

A imagem oficial já implementa mecanismos para redução do desgaste do cartão microSD.

Os principais recursos encontrados foram:

- ZRAM para swap;
- ZRAM para logs;
- log2ram;
- tmpfs para diretórios temporários.

Essa configuração está totalmente alinhada com um dos objetivos do projeto: minimizar gravações no cartão microSD.

---

## Conclusão

Nenhuma modificação adicional será necessária neste momento.

---

# Configuração de Boot

## Objetivo

Caracterizar a configuração de inicialização da plataforma.

---

## Procedimento Experimental

Arquivo analisado:

```text
/boot/armbianEnv.txt
```

---

## Evidências Experimentais

Configurações relevantes:

```text
fdtfile=sun50i-h616-bigtreetech-cb1-sd.dtb
```

```text
console=display
```

```text
overlays=hdmi
```

Posteriormente foi adicionada:

```text
overlays=hdmi spidev0_0
```

---

## Análise

O arquivo `armbianEnv.txt` concentra praticamente toda a configuração da plataforma.

A utilização de overlays evita recompilações do Device Tree e simplifica significativamente futuras expansões.

---

## Conclusão

Toda configuração adicional será realizada preferencialmente através de overlays.

---

# Validação da Interface SPI

## Objetivo

Preparar a plataforma para utilização do acelerômetro ADXL345.

---

## Procedimento Experimental

Foi editado o arquivo:

```text
/boot/armbianEnv.txt
```

Adicionando:

```text
spidev0_0
```

Após reinicialização foi validada a criação do dispositivo:

```text
/dev/spidev0.0
```

---

## Análise

A ativação do barramento ocorreu sem necessidade de:

- recompilar kernel;
- recompilar Device Tree;
- instalar drivers adicionais.

---

## Conclusão

A interface SPI encontra-se pronta para utilização pelo ADXL345.

---

# Descobertas do Projeto

## DP-001 — Slot correto para boot

Após testes experimentais verificou-se que o CB1 inicializa utilizando o slot identificado como:

```text
SoC-SDcard
```

Essa informação não é explicitamente esclarecida pela documentação da BIGTREETECH e pode gerar interpretações equivocadas devido à serigrafia da placa.

---

## DP-002 — Login padrão

Na imagem utilizada, o acesso inicial ocorreu utilizando:

```text
Usuário: root
Senha: root
```

O usuário `biqu`, citado em parte da documentação oficial, não estava disponível.

---

## DP-003 — Ausência de terminal local

Durante o primeiro boot não foi apresentado terminal local via HDMI.

Toda a configuração inicial foi realizada remotamente utilizando SSH.

---

## DP-004 — SPI habilitado por overlay

A interface SPI foi habilitada apenas através da inclusão do overlay:

```text
spidev0_0
```

Não foi necessária nenhuma outra modificação no sistema.

---

## DP-005 — Sistema otimizado para microSD

A imagem oficial já incorpora:

- ZRAM;
- log2ram;
- tmpfs;
- otimizações para redução de escrita.

Esses mecanismos atendem plenamente aos requisitos de preservação do cartão microSD.

---

# Backup_0

Após a conclusão desta etapa foi criado o **Backup_0** da plataforma.

Este backup representa o primeiro marco do projeto e permite restaurar rapidamente uma instalação funcional do sistema operacional sem repetir todas as etapas de configuração.

---

# Decisões de Engenharia

Nesta etapa foram definidas as seguintes decisões:

- utilizar exclusivamente conexão Ethernet;
- utilizar a imagem Debian 13 Minimal;
- preservar as otimizações padrão do Armbian para microSD;
- utilizar overlays sempre que possível;
- documentar todas as validações experimentais antes da instalação do Klipper.

---

# Próximos Passos

A próxima etapa do projeto consiste na instalação do ecossistema Klipper:

- Klipper Host;
- Moonraker;
- Fluidd;
- compilação do firmware para a BIGTREETECH Manta M8P V2.0;
- validação da comunicação entre o CB1 e a MCU STM32.

---

# Referências

- README.md
- CHANGELOG.md
- docs/00_Roadmap.md
- docs/03_Manta_M8P.md
- docs/04_Backups.md
- Documentação oficial BIGTREETECH CB1
- Documentação oficial Armbian