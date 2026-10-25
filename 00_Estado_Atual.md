# QIDI X-PRO Rebuild — Estado Atual

**Versão:** 0.3.0 — Produção validada
**Referência operacional:** 2026-10-17 (último trabalho concluído)
**Captura de estado:** 2026-10-25, 13:03 (America/Sao_Paulo)
**Fonte da verdade da configuração:** [`03_Klipper_Config/`](03_Klipper_Config/README.md)

> Este documento substitui as duas seções contraditórias que existiam aqui (v0.2.0 de 09/07 e
> “21/07”). Todo dado abaixo foi verificado diretamente na máquina em 25/10/2026 — ver
> [`05_Metrology/PROVENANCE.md`](05_Metrology/PROVENANCE.md).

---

# Plataforma

| Item | Valor |
|---|---|
| Host | BIGTREETECH CB1 V2.2 — `bigtreetech-cb1` — 192.168.10.126 |
| Sistema | Armbian 26.5.1 trixie (Debian 13) |
| Kernel | 7.0.2-vendor-sunxi64 |
| Python | 3.13.5 |
| Cartão | SanDisk SR64G, 59,5 GiB |
| Controladora | BIGTREETECH Manta M8P V2.0 — STM32H723 |

# Software

| Componente | Versão |
|---|---|
| Klipper (host) | `metrology-v0.5.0-2-gf5342a1ce-dirty` — branch `feature/metrology-framework` |
| Klipper (MCU) | `v0.13.0-701-g7e64fc842` |
| Moonraker | `v0.10.0-31-gd5ee171` |
| Fluidd | servido por Nginx em `/opt/3dprinter/fluidd/dist` |
| Fatiador | OrcaSlicer 2.4.2 |

Firmware: `klipper.bin` com SHA256 `6a527307…` — **idêntico** ao binário versionado no repositório.

# Configuração ativa

| Item | Valor |
|---|---|
| Homing | **mecânico, no máximo**: X 265, Y 155,3, Z 159 |
| Limites | X −5..265 · Y −5..156 · Z −5..159 |
| `rotation_distance` | 34,06 (X/Y) · 32,8449 (extrusoras) · 8 (Z) |
| Drivers | 5× TMC2209 em UART; sensorless **desativado** (`SGTHRS` e `diag_pin` comentados) |
| Sonda | AECO M8 PNP, `pin ^PD8`, `x_offset 18`, `y_offset 11`, `z_offset 0,652`, 5 amostras |
| Bed mesh | 9×7 bicúbico, perfil `default` salvo (0,24–1,22 mm) — **não aplicado** nos trabalhos |
| Input shaper | X `3hump_ei` 64,8 Hz · Y `mzv` 31,2 Hz |
| Pressure advance | 0,0885 no `extruder` · 0 no `extruder1` |
| Ferramentas | `T0` → X0 Y0 Z0 · `T1` → X 33,600 · Y 0,290 · Z 0,00 |
| Iluminação | `tool_light` PF8 · `cabin_light` PA4 |
| Ventoinhas | Part cooling PF6 · hotend 0 PF7 · hotend 1 PF9 |
| Cinemática | cartesiana, 600 mm/s, 10.000 mm/s² |

# Calibrações concluídas

- [x] PID dos dois hotends e da mesa (valores no bloco `SAVE_CONFIG`)
- [x] Input shaper com ADXL345 em `spi3a` (`cs_pin PA15`)
- [x] `rotation_distance` de X, Y e das duas extrusoras
- [x] `z_offset` da sonda
- [x] Offsets entre bicos (`T1`)
- [x] `pressure_advance` da extrusora principal
- [x] Mesh da mesa medido (63 pontos, malha 9×7)
- [x] Nivelamento manual em 3 pontos (`BED_CALIBRATE`)

# Operação

A máquina está em uso produtivo, não em bancada.

| Métrica | Valor |
|---|---|
| Último trabalho concluído | `Base Suporte Camera_0.15mm_PETG_1h21m` — iniciado 17/10/2026 17:31, concluído 18:55 |
| Duração / filamento | 83,8 min · 6058 mm |
| Trabalhos no histórico | 15 (incluindo `Box Externo` 149,8 min e `Suporte Seeed` 23,2 min) |
| Falhas no log de 17/10 (9,6 MB) | **0** — sem `Timer too close`, `MCU shutdown`, perda de comunicação ou `Move out of range` |
| Câmera | não configurada (`webcams: []`) |

# Extensão de metrologia

| Item | Valor |
|---|---|
| Local | `/opt/3dprinter/klipper/klippy/extras/metrology/` |
| Branch | `feature/metrology-framework` @ `f5342a1ce` (+ 3 commits locais) |
| Estado | **não executável**: erro de sintaxe em `metrology.py`, API de persistência divergente e geração de `offset_*` inválida para `[extruder]`/`[probe]` |
| Ativação | `#[include qidi_xpro/metrology.cfg]` — comentada no `printer.cfg` |
| Preservação | código, patches e proveniência em [`05_Metrology/`](05_Metrology/PROVENANCE.md) |

O trabalho existia **somente** no cartão SD da CB1; a captura de 25/10/2026 passou a mantê-lo
também no repositório.

# Pendências

| Prioridade | Item |
|---|---|
| P1 | Corrigir a inconsistência do mesh: `mesh_max y=165` > `position_max 156` e nenhum start G-code carrega o perfil |
| P1 | Resolver a divergência de branches do repositório (`main` 2 commits à frente e 2 atrás de `origin/main`) |
| P2 | Reparar a extensão de metrologia (separar versão monolítica, restaurar API, corrigir offsets) |
| P2 | `min_extrude_temp: 0` nas extrusoras — permite extrusão a frio |
| P2 | Câmera: bloqueada por hardware (webcam de teste só entrega YUYV) |
| P3 | Limpar o blob órfão de 451 MB em `.git/objects` |
| P3 | Completar a documentação em falta (`01_Docs/03_Manta_M8P`, `06_Hardware_QIDI`, `07_Esquema_Eletrico`, …) |

# Riscos conhecidos

1. **Configuração não versionada até 25/10.** As edições de julho a agosto viveram apenas no
   diretório do Klipper. Mitigado por `03_Klipper_Config/` + `MANIFEST.sha256`.
2. **Restaurar árvores antigas causa colisão.** `07_Backup/config_v0.2.5_2026-07-28/` usa homing
   sensorless com limites diferentes dos reais. Ver o `NOTE.md` de cada snapshot.
3. **Credenciais documentadas estão obsoletas.** `root/root` não funciona mais; a chave SSH está
   autorizada para `root`, não para `sidney`.
4. **Moonraker confia em toda a `192.168.10.0/24` sem autenticação.** Qualquer host da LAN pode
   enviar G-code.
5. **O mesh salvo não é usado.** A primeira camada depende de nivelamento manual.

# Próxima milestone

**v0.4.0 — Geometria reconciliada**: mesh coerente e aplicado, metrologia carregável e versionada,
documentação completa em `01_Docs/`.

---

**Versão do documento:** 0.3.0
**Última atualização:** 2026-10-25
