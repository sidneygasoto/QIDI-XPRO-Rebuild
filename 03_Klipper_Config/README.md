# Configuração Klipper ativa — espelho da CB1

> **Esta é a fonte da verdade.** Cópia byte a byte de `/opt/3dprinter/printer_data/config/` na
> CB1, capturada em **25/10/2026 13:03**. Os hashes estão em [`MANIFEST.sha256`](MANIFEST.sha256)
> e foram conferidos 15/15 contra a máquina. O contexto completo está em
> [`../05_Metrology/PROVENANCE.md`](../05_Metrology/PROVENANCE.md).

---

# Conteúdo

| Arquivo | Papel |
|---|---|
| `printer.cfg` | Arquivo mestre: includes, `[mcu]`, `[printer]`, `[exclude_object]`, bloco `SAVE_CONFIG` |
| `fluidd.cfg` | `virtual_sdcard`, `pause_resume`, `display_status`, `CANCEL_PRINT` |
| `moonraker.conf` | Servidor, `systemd_dbus`, clientes confiáveis |
| `qidi_xpro/steppers.cfg` | X/Y/Z com endstops mecânicos |
| `qidi_xpro/tmc2209.cfg` | UART + correntes (sensorless comentado) |
| `qidi_xpro/extruders.cfg` | Duas extrusoras (M4/M5), PA 0,0885 no `extruder` |
| `qidi_xpro/heaters.cfg` | Mesa PF5 / PB1 |
| `qidi_xpro/fans.cfg` | Part cooling PF6, hotend fans PF7 e PF9 |
| `qidi_xpro/probe.cfg` | Sonda AECO `^PD8`, offsets 18 / 11 |
| `qidi_xpro/bed_mesh.cfg` | Malha 9×7 bicúbica |
| `qidi_xpro/tools.cfg` | Macros T0 / T1 |
| `qidi_xpro/macros.cfg` | `PRINT_START`, `PRINT_END`, `PAUSE`, `RESUME`, `BED_CALIBRATE` |
| `qidi_xpro/lights.cfg` | `tool_light` PF8, `cabin_light` PA4 |
| `qidi_xpro/adxl345.cfg` | SPI por software, `cs_pin PA15` |
| `qidi_xpro/metrology.cfg` | Seção `[metrology]` — **comentada** no `printer.cfg` |

---

# Parâmetros que definem a máquina

| Item | Valor |
|---|---|
| Homing | **mecânico, no máximo** — X 265, Y 155,3, Z 159 |
| Limites | X −5..265, Y −5..156, Z −5..159 |
| `rotation_distance` | 34,06 (X/Y), 32,8449 (extrusoras), 8 (Z) |
| Sonda | `^PD8`, `x_offset 18`, `y_offset 11`, `z_offset 0,652` |
| Mesh | `mesh_min 40,30` / `mesh_max 253,165`, 9×7, fade 1→10 |
| Input shaper | X `3hump_ei` 64,8 Hz · Y `mzv` 31,2 Hz |
| Pressure advance | 0,0885 no `extruder`; 0 em `extruder1` |
| T1 | `X=33.600 Y=0.290 Z=0.00` |
| Cinemática | cartesiana, 600 mm/s, 10.000 mm/s² |

---

# Aplicar na CB1

Sempre preservando a configuração corrente:

```bash
# 1. backup remoto com data
ssh root@192.168.10.126 'cd /opt/3dprinter/printer_data/config && \
  cp printer.cfg printer.cfg.$(date +%F-%H%M)'

# 2. envio
scp -r printer.cfg fluidd.cfg moonraker.conf qidi_xpro \
  root@192.168.10.126:/opt/3dprinter/printer_data/config/

# 3. aplicar
curl -s http://192.168.10.126:7125/printer/gcode/script?script=FIRMWARE_RESTART
```

Conferir com `GET /printer/info` que o estado voltou a `ready`.

---

# Pendências conhecidas

1. **`metrology.cfg` comentado** — a extensão não carrega (erro de sintaxe + API de persistência
   divergente). Ver [`../05_Metrology/PROVENANCE.md`](../05_Metrology/PROVENANCE.md) §3.
2. **Mesh inconsistente** — `mesh_max y=165` excede `position_max y=156`; além disso nenhum start
   G-code carrega o perfil. A compensação não está em uso.
3. **`min_extrude_temp: 0`** nas duas extrusoras — permite extrusão a frio.
