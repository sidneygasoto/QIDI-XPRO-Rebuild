# Configuração v0.1.0 — julho/2026

**Origem:** `11_Config_qidi_xpro/klipper/`, commit `931e853` (09/07/2026). Movida para cá em
25/10/2026, durante a consolidação da configuração.

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
d60fdf923e2430e347391276791c3050309c654a274e8902da7ae1b8540e6b7b  printer.cfg
```
