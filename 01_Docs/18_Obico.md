# Obico — câmera e detecção de falhas

**Documento:** 18_Obico.md
**Versão:** 1.0.0
**Data:** 2026-10-31
**Objetivo:** transmitir a imagem da impressora e enviar os quadros ao Obico para detecção de falhas
de impressão.

---

# 1. Estado

| Componente | Estado |
|---|---|
| Câmera USB | **DECXIN**, UVC, `/dev/video0` (e `video1`) |
| Stream MJPEG | **uStreamer 5.4** ativo em `:8080` |
| `ffmpeg` | instalado (usado pelo cliente Obico para o vídeo) |
| Cliente `moonraker-obico` | ativo, conectado ao Moonraker, macros carregadas |
| Vínculo com a conta Obico | **pendente** — aguarda autorização no app |

# 2. Câmera

```
DECXIN (usb-5200000.usb-1.2):  /dev/video0  /dev/video1  /dev/media0
```

Formatos disponíveis:

| Formato | Resoluções |
|---|---|
| MJPG | 1280x720@60, 960x720@60, 640x480@60 |
| YUYV | 1280x720@10, 960x720@10, 640x480@30 |

## 2.1 Por que não o `camera-streamer`

O `camera-streamer` (ayufan) foi compilado em `/opt/camera-streamer/source` **sem as bibliotecas
libav**, e por isso não serve para nenhum formato:

```
CAMERA: Cannot find encoder to convert from 'YUYV'
CAMERA: Cannot find 'MJPG' decoder
```

O serviço `camera-streamer.service` ficou em **loop de reinício** (exit 255) e foi **desativado**.

> Se um dia for necessário voltar a ele, será preciso recompilar com `libavcodec-dev`,
> `libavformat-dev` e `libavutil-dev` (já instalados na CB1).

## 2.2 uStreamer (adotado)

Está **empacotado no Debian** (5.4), não exige compilação e faz passagem direta de MJPG:

```bash
apt install -y ustreamer
```

Serviço: `/etc/systemd/system/ustreamer.service`

```ini
[Service]
User=sidney
ExecStart=/usr/bin/ustreamer --device=/dev/video0 --format=MJPEG --resolution=640x480 \
    --desired-fps=30 --encoder=HW --host=0.0.0.0 --port=8080
```

| Endpoint | Conteúdo |
|---|---|
| `http://<ip>:8080/stream` | vídeo MJPEG contínuo |
| `http://<ip>:8080/snapshot` | um quadro JPEG |

> **Atenção nas opções:** esta versão usa `--desired-fps` (não `--fps`) e `--encoder=HW` para não
> recodificar. O processo renomeia-se para `main`, então `pkill -x ustreamer` **não** o encontra —
> use `systemctl`.

# 3. Cliente Obico

## 3.1 Instalação manual

O instalador oficial (`install.sh`) **não foi usado**: ele chama `sudo` e o usuário `sidney` não tem
sudo sem senha. Os passos foram feitos um a um:

| Item | Caminho |
|---|---|
| Código | `/opt/3dprinter/moonraker-obico` (repo `TheSpaghettiDetective/moonraker-obico`) |
| Ambiente Python | `/opt/3dprinter/moonraker-obico-env` |
| Configuração | `/opt/3dprinter/moonraker-obico/moonraker-obico.cfg` |
| Log | `/opt/3dprinter/printer_data/logs/moonraker-obico.log` |
| Serviço | `/etc/systemd/system/moonraker-obico.service` (roda como `sidney`) |

## 3.2 Configuração

```ini
[server]
url = https://app.obico.io

[moonraker]
host = 127.0.0.1
port = 7125

[webcam]
disable_video_streaming = False
snapshot_url = http://127.0.0.1:8080/snapshot
stream_url = http://127.0.0.1:8080/stream

[logging]
path = /opt/3dprinter/printer_data/logs/moonraker-obico.log
level = INFO

[tunnel]
```

Não é necessário `api_key`: o `moonraker.conf` já traz `127.0.0.1` em `trusted_clients`.

## 3.3 Macros no Klipper

O `printer.cfg` já continha `[include moonraker_obico_macros.cfg]`; o cliente cria o arquivo como
**symlink** para `include_cfgs/moonraker_obico_macros.cfg`. É preciso **reiniciar o Klipper** depois
que o symlink existe, senão o cliente alerta:

```
OBICO_LINK_STATUS not configured as a macro
```

## 3.4 Vinculação

Com o serviço parado, para evitar conflito de porta:

```bash
systemctl stop moonraker-obico
su - sidney -c "cd /opt/3dprinter/moonraker-obico && \
  /opt/3dprinter/moonraker-obico-env/bin/python3 -m moonraker_obico.link \
  -c /opt/3dprinter/moonraker-obico/moonraker-obico.cfg"
```

A ferramenta anuncia a impressora na rede local e mostra um **código de vinculação manual**. No app
do Obico: adicionar impressora → ela aparece na mesma rede ("Link Now"), ou usar o código.

Depois de vinculada, o `auth_token` é gravado no `moonraker-obico.cfg`.

# 4. Verificação

```bash
systemctl is-active ustreamer moonraker-obico klipper moonraker
curl -s -o /dev/null -w "%{http_code} %{size_download}\n" http://127.0.0.1:8080/snapshot
tail -5 /opt/3dprinter/printer_data/logs/moonraker-obico.log
```

Esperado: os quatro serviços `active`, snapshot `200` com ~50 KB, e o log com
`connection is open`, `Klippy ready` e `printer_discovery started`.

# 5. Pendências

- [ ] **Vincular a impressora no app Obico** (código gerado em 2026-10-31: `b6v5t`; expira, basta
      gerar outro)
- [ ] Confirmar no app que a câmera aparece e que o vídeo abre
- [ ] Fazer uma impressão de teste com o Obico ativo e conferir a detecção
- [ ] Decidir se o `ustreamer` deve subir com resolução maior (720p) — hoje 640x480 por CPU
- [ ] Documentar o acesso ao painel do Obico (conta/servidor usado)
