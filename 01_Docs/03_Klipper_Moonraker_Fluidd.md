# Estado da Instalação - CB1 / Klipper / Moonraker / Fluidd

Projeto: **QIDI-XPRO-Rebuild**
Plataforma: BIGTREETECH CB1 + Manta M8P V2.0
Data do registro: 09/07/2026

---

# 1. Objetivo da etapa v0.2.0

A versão planejada do projeto previa:

- [x] Instalação do Klipper
- [x] Instalação do Moonraker
- [x] Instalação do Fluidd
- [x] Compilação do firmware da BIGTREETECH Manta M8P V2.0
- [x] Primeira comunicação CB1 ↔ STM32H723

Estado atual:

A infraestrutura básica do sistema está operacional.

O CB1 executa:

- Debian 13 ARM64
- Klipper
- Moonraker
- Fluidd
- Nginx

A placa Manta M8P V2.0 comunica corretamente com o host.

---

# 2. Hardware

## Host

BIGTREETECH CB1

Características:

```
Arquitetura:
arm64

Sistema:
Debian 13

Kernel:
7.0.2-vendor-sunxi64

Python:
3.13.5
```

Comandos utilizados:

```bash
dpkg --print-architecture

uname -a

python3 --version
```

Resultado:

```
arm64

Linux bigtreetech-cb1
7.0.2-vendor-sunxi64
aarch64

Python 3.13.5
```

---

# 3. Estrutura principal do sistema

Diretório base:

```
/opt/3dprinter
```

Estrutura atual:

```
/opt/3dprinter
├── backups
├── firmware
├── klipper
├── logs
├── mainsail
├── moonraker
├── printer_data
├── qidi-xpro-rebuild
└── scripts
```

---

# 4. Git e sincronização do projeto

Repositório:

```
https://github.com/sidneygasoto/QIDI-XPRO-Rebuild.git
```

O nome oficial do projeto permanece:

```
QIDI-XPRO-Rebuild
```

## Problema inicial de push

Primeira tentativa:

```bash
git push
```

Resultado:

```
Password authentication is not supported
```

Motivo:

GitHub não aceita senha para operações Git.

O remote foi ajustado para SSH:

```bash
git remote -v
```

Resultado:

```
origin github.com:sidneygasoto/QIDI-XPRO-Rebuild.git
```

---

## Divergência entre CB1 e GitHub

Comando:

```bash
git push
```

Resultado:

```
rejected - fetch first
```

Foi executado:

```bash
git pull --rebase origin main
```

Resultado:

```
Successfully rebased and updated refs/heads/main
```

Depois:

```bash
git push
```

Resultado:

```
main -> main
```

Estado final:

```bash
git status
```

Resultado:

```
Your branch is up to date with 'origin/main'.

nothing to commit
```

---

# 5. Klipper

Serviço criado:

```
/etc/systemd/system/klipper.service
```

Configuração:

```
ExecStart=/opt/3dprinter/klipper/venv/bin/python \
/opt/3dprinter/klipper/klippy/klippy.py \
/opt/3dprinter/printer_data/config/printer.cfg
```

Posteriormente ajustado para comunicação Moonraker:

```
-a /tmp/klippy_uds
```

---

Verificação:

```bash
systemctl status klipper
```

Resultado:

```
Active: active (running)
```

Processo:

```bash
ps aux | grep klippy
```

Resultado:

```
python klippy.py printer.cfg -a /tmp/klippy_uds
```

Socket criado:

```bash
ls -lah /tmp/klippy_uds
```

Resultado:

```
srwxr-xr-x /tmp/klippy_uds
```

---

# 6. Firmware Manta M8P V2.0

Firmware encontrado:

```bash
find /opt/3dprinter -type f \
\( -name "*.bin" -o -name ".config" \)
```

Resultado:

```
/opt/3dprinter/klipper/.config

/opt/3dprinter/klipper/out/klipper.bin

/opt/3dprinter/qidi-xpro-rebuild/
06_Firmware/M8P_V2_H723_bootloader.bin
```

---

Configuração MCU:

Arquivo:

```
printer.cfg
```

Trecho:

```ini
[mcu]

serial:
/dev/serial/by-id/
usb-Klipper_stm32h723xx_34002F000A51333231343036-if00
```

Comunicação confirmada.

---

# 7. Sensores de temperatura

Antes da conexão dos componentes:

Foram instalados três resistores de teste:

```
THB
TH0
TH1
```

Todos:

```
100KΩ
```

Objetivo:

Validar leitura analógica dos canais.

---

# 8. Configuração dos extrusores

Arquivo:

```
11_Config_qidi_xpro/extruders.cfg
```

Configuração:

## Extruder 0

```ini
heater_pin: PA0

sensor_pin: PB0

sensor_type:
Generic 3950
```

---

## Extruder 1

```ini
heater_pin: PA1

sensor_pin: PC5

sensor_type:
Generic 3950
```

---

# 9. Mesa aquecida

Arquivo:

```
heaters.cfg
```

Configuração:

```ini
[heater_bed]

heater_pin: PF5

sensor_pin: PB1

sensor_type:
Generic 3950
```

---

# 10. Validação dos sensores

Inicialmente houve dúvida sobre ausência de interface.

Depois da instalação do Fluidd foi possível confirmar.

Resultado:

Temperatura esperada:

```
aproximadamente 25°C
```

Leitura apresentada:

```
25.2°C
```

Conclusão:

Sensores:

```
TH0
TH1
THB
```

Estão funcionando corretamente.

---

# 11. Moonraker

Código instalado:

```
/opt/3dprinter/moonraker
```

Arquivo criado:

```
11_Config_qidi_xpro/moonraker/moonraker.conf
```

Rede autorizada:

```
192.168.10.0/24
```

---

Serviço criado:

```
11_Config_qidi_xpro/systemd/moonraker.service
```

Copiado:

```bash
sudo cp \
11_Config_qidi_xpro/systemd/moonraker.service \
/etc/systemd/system/
```

Ativado:

```bash
sudo systemctl daemon-reload

sudo systemctl enable moonraker

sudo systemctl start moonraker
```

---

Verificação:

```bash
journalctl -u moonraker -n 50 --no-pager
```

Resultado:

```
Starting Moonraker on (0.0.0.0, 7125)

Klippy Connection Established

Klippy ready
```

Sensores detectados:

```
heater_bed
extruder
extruder1
```

---

# 12. Fluidd

Inicialmente não instalado.

Foi utilizado:

```bash
cd /opt/3dprinter

git clone https://github.com/fluidd-core/fluidd.git fluidd
```

---

Dependências:

Node.js 22:

```bash
curl -fsSL \
https://deb.nodesource.com/setup_22.x | sudo -E bash -
```

Instalação:

```bash
sudo apt install nodejs -y
```

---

PNPM:

```bash
sudo npm install -g pnpm
```

Versão:

```
pnpm 11.10.0
```

---

Build:

Dentro de:

```
/opt/3dprinter/fluidd
```

Executado:

```bash
pnpm install

pnpm build
```

Resultado:

```
✓ built
files generated

dist/sw.js
```

---

# 13. Nginx

Instalado:

```bash
sudo apt install nginx -y
```

Serviço:

```bash
systemctl status nginx
```

Resultado:

```
Active: active (running)
```

---

# 14. Estado atual

Sistema operacional:

OK

Klipper:

OK

Comunicação Manta M8P:

OK

Firmware:

OK

Moonraker:

OK

Fluidd:

OK

Sensores:

OK

---

# 15. Próximas etapas

## Documentação

Criar:

```
11_Config_qidi_xpro/documentacao/
```

com:

```
01_estado_inicial.md

02_estado_instalacao_cb1.md

03_configuracao_manta_m8p.md

04_configuracao_klipper.md
```

---

## Configurações futuras

Ainda pendente:

- validar motores
- validar drivers TMC2209 UART
- configurar eixos X/Y/Z
- configurar extrusores físicos
- configurar PID real dos heaters
- instalar ADXL345
- calibrar Input Shaper
- configurar câmera
- finalizar reconstrução da QIDI X-Pro

---

# Estado da versão

Versão:

```
v0.2.0
```

Status:

```
Infraestrutura Klipper completa e validada.
```
