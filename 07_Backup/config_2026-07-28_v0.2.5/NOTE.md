# Configuração de 28/07/2026 — versão v0.2.5

**Origem:** commit `cb7f9fc` (tag anotada `v0.2.5`; a mensagem do commit diz “v0.2.0”).

Este momento do projeto tem **duas árvores diferentes**, e a diferença entre elas é justamente a
prova de que a máquina evoluía fora do Git. Ambas foram reconstruídas a partir dos blobs do commit,
com `core.autocrlf=false` (bytes fiéis, LF).

## `commit-tree/` — 9 arquivos

O que o repositório versionava em `03_Klipper_Config/`:

- Homing **sensorless** (`tmc2209_stepper_x:virtual_endstop`, `diag_pin PF4/PF3`, `SGTHRS 55/60`)
- `X: -14..262`, `Y: -4..174`, `rotation_distance 33.7298055705`
- `probe.cfg` presente no diretório, **mas não incluído** pelo `printer.cfg`
- Sem `[bed_mesh]`, sem `[exclude_object]`, sem iluminação, sem PA

## `machine-snapshot/` — 12 arquivos

O snapshot mais completo que existia em `07_Backup/config_v0.2.0/` no mesmo commit. Acrescenta
`fluidd.cfg`, `tools.cfg` e `metrology.cfg`, e o `printer.cfg` inclui `[probe]`, `[include
qidi_xpro/tools.cfg]` e `#[include qidi_xpro/metrology.cfg]`.

Ou seja: em 28/07 a máquina já tinha sonda ativa e offsets de ferramenta (`T0`/`T1`) que a árvore
versionada não registrava.

## Aviso

> **Não restaurar sobre a CB1.** Esta árvore usa homing sensorless e limites diferentes dos reais.
> A máquina opera com endstops mecânicos, home no máximo (X 265 / Y 155,3 / Z 159) e `Y` máximo
> 156. Restaurar inverteria a estratégia de homing e provocaria colisão.

## Integridade

```
9b8e67c7959e61498a6dedd89a24390168d006675ee61ba05ea8ef3012dcbad6  commit-tree/printer.cfg
6831c9eed82ab320a4abd3d92a7271977faea82b60e9957ba6ec90df235f0071  machine-snapshot/printer.cfg
```
