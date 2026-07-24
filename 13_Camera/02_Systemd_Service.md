# Configuração do Serviço Systemd

## Objetivo

Documentar a criação e configuração do serviço `camera-streamer.service`, responsável por iniciar automaticamente o servidor de streaming durante a inicialização do sistema.

---

## Ambiente

### Hardware

- BIGTREETECH CB1 V2.2
- Arquitetura ARM64

### Sistema

- Debian 13
- Klipper
- Moonraker
- Fluidd

### Software

- camera-streamer v0.4.2

---

## Estrutura utilizada

Diretório de instalação:

```text
/opt/camera-streamer/
├── source/
│   └── camera-streamer
├── config/
└── logs/
```

Executável utilizado pelo serviço:

```text
/opt/camera-streamer/source/camera-streamer
```

---

## Criação do serviço

Arquivo:

```text
/etc/systemd/system/camera-streamer.service
```

Conteúdo:

```ini
[Unit]
Description=Camera Streamer for Klipper
After=network.target

[Service]
Type=simple
User=sidney
WorkingDirectory=/opt/camera-streamer/source

ExecStart=/opt/camera-streamer/source/camera-streamer \
    --camera-type=v4l2 \
    --camera-path=/dev/video0 \
    --camera-width=640 \
    --camera-height=480 \
    --camera-format=YUYV \
    --camera-fps=30 \
    --http-listen=0.0.0.0 \
    --http-port=8080

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## Ativação do serviço

Recarregar os serviços do systemd:

```bash
sudo systemctl daemon-reload
```

Habilitar inicialização automática:

```bash
sudo systemctl enable camera-streamer
```

Iniciar o serviço:

```bash
sudo systemctl start camera-streamer
```

---

## Validação

Verificar o estado do serviço:

```bash
systemctl status camera-streamer
```

Resultado validado:

```text
Active: active (running)
```

O serviço foi iniciado corretamente durante o boot do sistema.

---

## Validação do servidor HTTP

O serviço disponibiliza os endpoints:

```text
http://<IP_DO_CB1>:8080/snapshot
http://<IP_DO_CB1>:8080/stream
http://<IP_DO_CB1>:8080/webrtc
http://<IP_DO_CB1>:8080/status
```

---

## Validação da câmera

A câmera USB foi reconhecida corretamente pelo sistema:

- Driver: V4L2 / UVC
- Dispositivo:

```text
/dev/video0
```

Formato detectado:

```text
640x480 YUYV
```

---

## Limitação encontrada

A câmera utilizada nos testes fornece somente o formato:

```text
YUYV 4:2:2
```

Durante a inicialização do `camera-streamer` foi identificado:

```text
CAMERA: Cannot find encoder to convert from 'YUYV'
```

O binário foi compilado com suporte FFmpeg, porém esta câmera não fornece formatos comprimidos adequados para streaming, como:

- MJPEG;
- H264.

Desta forma, a infraestrutura do serviço foi validada, mas a validação do streaming permanece pendente até a utilização de uma câmera compatível.

---

## Próxima etapa

Substituir a câmera de teste por uma câmera USB UVC com suporte nativo a:

- MJPEG;
- 720p ou 1080p;
- 30 FPS.

Após a substituição, serão realizados:

- teste de streaming;
- integração com Fluidd;
- documentação final.