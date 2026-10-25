# Proveniência — captura de 2026-10-25

> Registro do estado real da impressora e da extensão de metrologia, capturado antes de qualquer
> consolidação. Serve como ponto de restauração e como prova de qual configuração operava a máquina.

---

# 1. Captura

| Item | Valor |
|---|---|
| Data/hora | 2026-10-25, 13:03 (America/Sao_Paulo) |
| Host | `bigtreetech-cb1` — 192.168.10.126 |
| Acesso | SSH como `root` (chave `br_pc`), somente leitura |
| Interface secundária | Moonraker 7125 (`GET` apenas) |
| Alterações na máquina | Nenhuma, exceto 5 artefatos criados em `/root/` |

O usuário `sidney` **não** aceitou a chave; o acesso foi feito como `root`. Nenhum comando de
movimento, aquecimento ou alteração de configuração foi executado.

---

# 2. Fork do Klipper

| Item | Valor |
|---|---|
| Diretório | `/opt/3dprinter/klipper` |
| Branch | `feature/metrology-framework` |
| HEAD | `f5342a1ce` — *Add Metrology data models and geometry module* |
| Base | `7e64fc842` (upstream Klipper) |
| Commits de metrologia | `cef3494dc` → `1ec034cec` → `f5342a1ce` |
| Branch `master` | `1ec034cec` — `[origin/master: ahead 2, behind 8]` |
| Remoto | **somente** `https://github.com/Klipper3d/klipper.git` |
| Versão reportada | `metrology-v0.5.0-2-gf5342a1ce-dirty` |

**Consequência:** os três commits de metrologia e o trabalho não commitado **existem apenas neste
cartão SD**. Não há fork, branch remoto, tag publicada ou backup em nuvem.

## Árvore de trabalho

Modificados: `calibration.py`, `geometry.py`, `metrology.py` (parcialmente staged), `models.py`,
`persistence.py` — 1074 inserções / 450 remoções.

Não rastreados: `machine.py`, `tests/`, `AGENTS.md`, `CONTINUE.md`, `CONTRIBUTING.md`,
`README.md`, `ROADMAP.md`, `.vscode/`, `metrology.code-workspace`.

O patch staged contém apenas a remoção de uma linha em branco em `metrology.py`, enquanto o
working tree tem a reescrita completa — estado de índice inconsistente, propenso a commit parcial
incorreto.

---

# 3. Defeitos conhecidos da extensão (verificados estaticamente)

1. **Erro de sintaxe em `metrology.py`.** O arquivo contém duas `class Metrology` (linhas 25 e 466)
   e dois blocos de import: a versão monolítica antiga foi truncada no meio de um `raise
   gcmd.error(` e o cabeçalho do novo pacote foi concatenado em seguida. Verificado com
   `ast.parse` — é o único módulo que não compila; os outros seis compilam.
2. **API de persistência divergente.** `metrology.py` importa `load_devices`, `save_device`,
   `save_devices`; o `persistence.py` novo define apenas `save_config` e `load_config`. Mesmo
   corrigida a sintaxe, o import falharia.
3. **Geração de configuração inválida.** `calibration.py::apply_offsets_to_config` grava
   `offset_x/offset_y/offset_z` em `[extruder]` e `[extruder1]` — opções inexistentes no Klipper
   (o offset de ferramenta é aplicado por `SET_GCODE_OFFSET`, como nas macros `T0`/`T1`) — e usa
   `offset_*` em vez de `x_offset/y_offset/z_offset` para `[probe]`.

Por isso `#[include qidi_xpro/metrology.cfg]` está comentado em `printer.cfg`.

---

# 4. Configuração viva

Copiada byte a byte para [`../03_Klipper_Config/`](../03_Klipper_Config/), com
[`MANIFEST.sha256`](../03_Klipper_Config/MANIFEST.sha256) conferido contra o SHA256 calculado na
CB1 (15/15 iguais).

Destaques que **não** existem em nenhuma árvore versionada:

- Homing por **endstops mecânicos** (`^!PF4`, `^!PF3`, `^!PF2`); o `virtual_endstop` sensorless
  está comentado, com `stealthchop_threshold: 999999` e `driver_SGTHRS` inativo.
- Home no **máximo**: X 265, Y 155,3, Z 159.
- `rotation_distance 34.06` (X/Y), `32.8449` (extrusoras).
- `[probe]` ativo: `pin ^PD8`, `x_offset 18`, `y_offset 11`, `z_offset 0.652`, 5 amostras.
- `[bed_mesh]` 9×7 bicúbico com perfil `default` salvo (0,24 a 1,22 mm).
- `pressure_advance 0.0885` apenas no `extruder`.
- `T1` com `X=33.600 Y=0.290 Z=0.00`.
- Iluminação: `tool_light` PF8 e `cabin_light` PA4.
- Ventoinhas remapeadas: `[fan]` PF6, `hotend_fan_0` PF7, `hotend_fan_1` PF9.
- `max_velocity 600`, `max_accel 10000`.

## Inconsistência aberta

`mesh_max: 253,165` excede `stepper_y position_max: 156` e o start G-code do OrcaSlicer não carrega
nem recalibra mesh (`G28` + `M140/M190` + `M104/M109` apenas). O perfil salvo existe, mas não é
aplicado — a primeira camada depende do nivelamento manual em 3 pontos (`BED_CALIBRATE`).

---

# 5. Firmware e versões

| Item | Valor |
|---|---|
| `out/klipper.bin` na CB1 | SHA256 `6a527307d186f6f7457c6e4d85cc0c926d6fb0df1effe954f3eae5781546b5c4` |
| `11_Config_qidi_xpro/firmware/manta_m8p_v2/klipper.bin` no repo | mesmo SHA256 |
| `06_Firmware/klipper.bin` no repo | mesmo SHA256 |
| Versão do MCU | `v0.13.0-701-g7e64fc842` |
| Host / Moonraker | `metrology-v0.5.0-2-gf5342a1ce-dirty` / `v0.10.0-31-gd5ee171` |
| Sistema | Armbian 26.5.1 trixie, kernel 7.0.2-vendor-sunxi64, Python 3.13.5 |
| Cartão | SanDisk SR64G, 59,5 GiB |

O binário publicado no repositório é **exatamente** o gravado na máquina — único artefato com
proveniência completa até aqui.

---

# 6. Clone do projeto na CB1

`/opt/3dprinter/qidi-xpro-rebuild` — branch `feature/dual-extrusion-validation`, árvore **limpa**,
HEAD `cb7f9fc` (= `origin/main`), remoto `git@github.com:sidneygasoto/QIDI-XPRO-Rebuild.git`.

Ou seja: as edições de configuração de julho a agosto foram feitas **no diretório do Klipper**, não
no clone; o repositório nunca as viu.

---

# 7. Operação

Último job concluído: `Base Suporte Camera_0.15mm_PETG_1h21m.gcode`, iniciado em 17/10/2026 17:31
e concluído às 18:55 (83,8 min, 6058 mm de filamento). Quinze jobs no histórico, entre eles `Box Externo` (149,8 min) e
`Suporte Seeed` (23,2 min). PETG a 250 °C / mesa 80 °C, OrcaSlicer 2.4.2, `exclude_object` ativo.

O log de 17/10 (9,6 MB) não contém `Timer too close`, `MCU shutdown`, `lost communication`,
`Move out of range` ou `Probe triggered prior`. Nenhuma câmera configurada (`webcams: []`).

---

# 8. Artefatos desta captura

| Arquivo | Conteúdo | SHA256 |
|---|---|---|
| `backup/metrology-2026-10-25.tgz` | diretório `metrology/` (sem `.venv` e `__pycache__`) | `2a43a867…` |
| `backup/metrology-unstaged-2026-10-25.patch` | diff não commitado (52 KB) | `9fa828a3…` |
| `backup/metrology-staged-2026-10-25.patch` | diff do índice | `311eae4e…` |
| `backup/metrology-git-state-2026-10-25.txt` | status, log, branches, diffstat, remotes | `5b43c16d…` |
| `backup/qidi-config-active-2026-10-25.tgz` | config viva compactada | `bdaff711…` |
| `source/` | extração legível do código de metrologia | — |

Integridade conferida: os 5 hashes calculados após a cópia coincidem com os da CB1.

---

# 9. Reprodução

```bash
ssh root@192.168.10.126
cd /opt/3dprinter/klipper
git -c safe.directory=/opt/3dprinter/klipper status --porcelain=v1 -b
git -c safe.directory=/opt/3dprinter/klipper log --oneline -10
sha256sum /opt/3dprinter/printer_data/config/printer.cfg
/opt/3dprinter/klipper/venv/bin/python -c "import ast; ast.parse(open('klippy/extras/metrology/metrology.py').read())"
```

---

# 10. Pendências decorrentes

- **P1** — promover `03_Klipper_Config/` a fonte da verdade no repositório. Atenção: `origin/main`
  já possui uma `03_Klipper_Config/` (julho); a substituição precisa ser explícita, não um merge cego.
- **P3** — separar a versão monolítica da versão em pacote, restaurar a API de persistência,
  corrigir `apply_offsets_to_config` e só então avaliar `[include metrology.cfg]`.
- Nenhum commit, tag, merge ou remoção foi realizado nesta etapa.
