# Bed Mesh — Diagnóstico e Calibração

**Documento:** 07_Bed_Mesh.md
**Versão:** 1.0.0
**Data:** 2026-10-25
**Base:** configuração ativa em [`03_Klipper_Config/`](../03_Klipper_Config/README.md)

---

# 1. Objetivo

Registrar o estado real da compensação de mesa da QIDI X-Pro, a análise geométrica do perfil salvo
e o procedimento adotado para torná-la efetiva.

Este documento também corrige uma afirmação incorreta publicada na versão 0.3.0 da documentação.

---

# 2. Correção: `mesh_max` não excede os limites

A documentação anterior afirmava que `mesh_max: 253,165` excedia `stepper_y position_max: 156`.
**Está incorreto.** O código do Klipper em execução mostra que `mesh_min/mesh_max` são coordenadas
**da sonda**, não do bico:

```python
# klippy/extras/bed_mesh.py:824
self.probe_helper.use_xy_offsets(True)

# klippy/extras/probe.py:474-475
if self.use_offsets:
    nextpos[0] -= self.probe_offsets[0]
    nextpos[1] -= self.probe_offsets[1]
```

Com `x_offset 18` e `y_offset 11`:

| Ponto do mesh | Sonda | Bico | Limite do eixo | Válido |
|---|---|---|---|---|
| mínimo | 40, 30 | 22, 19 | −5..265 / −5..156 | sim |
| máximo | 253, 165 | **235, 154** | 265 / 156 | sim |

Além disso, `_init_mesh_config()` **não valida** o mesh contra os limites dos eixos — apenas
`max > min`. Um mesh fora do curso não falharia ao carregar, e sim em movimento.

---

# 3. Estado verificado

| Fato | Evidência |
|---|---|
| Perfil `default` existe e tem 63 pontos | bloco `SAVE_CONFIG` em `printer.cfg` |
| **Nunca é carregado** | zero comandos `BED_MESH*` nos logs de outubro; nenhum `BED_MESH_PROFILE LOAD` no start G-code do OrcaSlicer |
| **Está vencido** | salvo em 11/08; os logs de outubro registram 34 ocorrências de `BED_CALIBRATE` (nivelamento mecânico em 3 pontos) |
| Start G-code | `M140 → M104 → G90/G21/M83 → G28 → M190 → M109 → T0`, sem mesh |
| `PRINT_START` do Klipper | existe, mas é código morto: nenhum gcode o chama |

Conclusão: a máquina imprime **sem compensação de mesa**, apoiada apenas no nivelamento manual em
três pontos e no `z_offset 0,652`.

---

# 4. Análise geométrica do perfil salvo

Ajuste de plano por mínimos quadrados sobre os 63 pontos (`z = a + b·x + c·y`):

```
z = 0,3125 − 0,000233·x + 0,005340·y

inclinação:  X  −0,023 mm/100 mm     Y  +0,534 mm/100 mm
plano:       amplitude 0,770 mm
deformação:  amplitude 0,375 mm   (RMS 0,075 mm)
bruto:       amplitude 0,988 mm
```

| Componente | Amplitude | Interpretação |
|---|---|---|
| Plano (inclinação) | 0,770 mm | dominado por Y; é o que o `BED_CALIBRATE` corrige mecanicamente |
| Deformação (resíduo) | 0,375 mm | concentrada em x = 40 (borda esquerda) e y = 165 (borda traseira) |

Ou seja: **78 % do desvio era inclinação**, não empenamento. Como o nivelamento mecânico foi refeito
várias vezes depois de agosto, essa inclinação já não corresponde à máquina — carregar o perfil
injetaria até ~1 mm de correção errada.

---

# 5. Opções avaliadas

| Opção | Custo | Risco | Decisão |
|---|---|---|---|
| **A** — mesh novo, a quente, aplicado no início | ~8 min, uma vez | baixo | **adotada** |
| B — mesh adaptativo a cada peça | +5–9 min por impressão | baixo | descartada (mesa estável) |
| C — sem mesh, só nivelamento manual | 0 | bordas fora de tolerância | descartada |
| D — carregar o perfil de agosto | 0 | compensação invertida | **proibida** |

---

# 6. Procedimento executado

1. Aquecimento estabilizado: mesa 80 °C, bico 250 °C, 10 min de patamar.
2. `G28`.
3. `BED_MESH_CALIBRATE PROBE_COUNT=7,5` — 35 pontos, ~5 min.
4. `BED_MESH_PROFILE SAVE=default` + `SAVE_CONFIG`.
5. Revalidação do `z_offset` **após** a malha (a malha herda o erro do offset).
6. `BED_MESH_PROFILE LOAD=default` no início da impressão.
7. Impressão de teste de primeira camada e medição em 5 pontos.

---

# 7. Critérios de aceite

- [ ] `BED_MESH_CALIBRATE` conclui sem `Probe triggered prior to movement` ou `Move out of range`
- [ ] amplitude do mesh novo < 0,4 mm
- [ ] variação de espessura da primeira camada ≤ 0,03 mm em 5 pontos
- [ ] `z_offset` final registrado em `SAVE_CONFIG`

---

# 8. Resultado

> Preenchido após a execução. Ver seção 9.

| Item | Valor |
|---|---|
| Data/hora | — |
| `probe_count` | — |
| Amplitude do mesh | — |
| Inclinação X / Y | — |
| Deformação | — |
| `z_offset` final | — |

---

# 9. Histórico

| Data | Evento |
|---|---|
| 2026-08-11 | Mesh original medido e salvo como `default` (9×7, 63 pontos) |
| 2026-10-25 | Diagnóstico: perfil inerte e vencido; correção da afirmação sobre limites |
| 2026-10-25 | Recalibração e aplicação (ver §8) |
