# Configuração v0.1.0 — julho/2026

**Origem:** commit `931e853` (09/07/2026), caminho original `11_Config_qidi_xpro/klipper/`.

Reconstruída em 25/10/2026 a partir dos blobs do próprio commit, com `core.autocrlf=false` — os
arquivos estão em **LF**, byte a byte como o Git os armazena.

## Estado

Pré-calibração — a árvore que existia antes de a máquina começar a operar:

- `rotation_distance: 40` (valor padrão, não calibrado)
- Endstops mecânicos `^PF4` / `^PF3` / `^PF2`
- `tmc2209.cfg` **integralmente comentado** (drivers operando em modo standalone)
- Sem `[probe]`, sem `[adxl345]`, sem `[input_shaper]`, sem bloco `SAVE_CONFIG`
- Cinco arquivos: `printer.cfg` + `qidi_xpro/{steppers,tmc2209,extruders,heaters,fans}.cfg`

## Aviso

> **Não operar a máquina com esta árvore.** Os parâmetros não correspondem ao hardware calibrado:
> o deslocamento sairia ~18 % errado e não há sonda configurada.

## Integridade

```
03886e1652f24123d58de2d8e310133d26e8f174ad5f482d7a7920aa1e45a7a1  printer.cfg
```
