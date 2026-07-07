# Backup_0

Data: 2026-07-06

Descrição:
Sistema operacional instalado e atualizado.
Nenhum software da impressora instalado.

Imagem:
CB1_Debian13_minimal_kernel7.0_20260430

Kernel:
7.0.2-vendor-sunxi64

Cartão:
SanDisk Extreme PRO 64 GB

Ferramenta:
USB Image Tool

Modo:
Compressed Backup

SHA256:
<preencher>

Observações:
Primeiro marco oficial do projeto.

## Correção de rede

Durante a validação do Backup_0 foi identificado alerta ARP no ESET.

A causa foi a ativação simultânea das interfaces Ethernet e Wi-Fi do CB1.

Interfaces detectadas:

| Interface | IP | MAC |
|---|---|---|
| eth0 | 192.168.10.126 | BA:03:65:C8:78:D1 |
| wlan0 | 192.168.10.127 | DC:84:03:E8:C9:60 |

Não foi identificado spoofing de MAC.

A interface Wi-Fi foi desabilitada para operação normal, mantendo Ethernet como interface principal.