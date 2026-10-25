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

1. Aquecimento: mesa 80 °C, bico 180 °C (sem ooze), com `SET_IDLE_TIMEOUT TIMEOUT=3600`.
2. Patamar térmico até a potência da mesa estabilizar (~20 %).
3. `G28` — `homed_axes = xyz`, home em X 265 / Y 155,3 / Z 159.
4. **`PROBE_ACCURACY SAMPLES=10`** no centro (115, 75).
5. `BED_MESH_CALIBRATE` — primeira tentativa falhou por tolerância (ver §6.1).
6. Varredura das bordas para localizar o limite físico da chapa (ver §6.2).
7. `BED_MESH_CALIBRATE PROBE_COUNT=7,5 MESH_MAX=253,154 SAMPLES_TOLERANCE=0.03` — 35 pontos.
8. Ajuste permanente de `probe.cfg` e `bed_mesh.cfg`.
9. `SAVE_CONFIG` — malha gravada no `printer.cfg`; Klipper reiniciado às 17:04:14.

## 6.1 Repetibilidade da sonda

```
probe accuracy results: maximum 0.370500, minimum 0.358000, range 0.012500,
average 0.362000, median 0.361750, standard deviation 0.003742
```

Faixa de **12,5 µm** e desvio-padrão de **3,7 µm** em 10 amostras. A tolerância configurada era
`samples_tolerance: 0.010` (10 µm) e o primeiro ponto da malha falhou com
`Probe samples exceed samples_tolerance`. Corrigido para **0,030 mm**, mantendo
`samples_result: median` e `samples: 5` — o erro da mediana fica em ~4 µm.

Este era o `PROBE_ACCURACY` previsto no README desde julho e nunca medido.

## 6.2 Limite físico da chapa

Sondagens isoladas na borda (coordenadas da sonda):

| Sonda Y | Leituras (3 amostras) | Interpretação |
|---|---|---|
| 146 | −0,085 / +0,016 / +0,038 | dispersa, dentro da chapa |
| 156 | −0,007 / +0,013 / +0,016 | estável, ainda sobre a chapa |
| 161 | −0,057 / −0,050 / −0,052 | **degrau de −0,06** |
| 166 | −0,195 / −0,200 / −0,197 | **degrau de −0,20** — fora da chapa |

A sonda em Y = 165 (o `mesh_max` antigo) estava **9 mm além da chapa de aço**; o sensor lia o
quadro, não a mesa. Isso explica o resíduo de −0,36 mm naquele canto na primeira tentativa.

Na borda X o comportamento é saudável: 253 → +0,055; 258 → +0,049; 263 → +0,010. O limite de
253 é seguro.

Novo limite adotado: `mesh_max: 253,154` (sonda em 154, duas amostras dentro da chapa).

---

# 7. Critérios de aceite

- [x] `BED_MESH_CALIBRATE` conclui sem `Probe triggered prior to movement` ou `Move out of range`
- [ ] amplitude do mesh novo **< 0,4 mm** — obtido **0,417 mm** (ver §8)
- [ ] variação de espessura da primeira camada ≤ 0,03 mm em 5 pontos — pendente (§10)
- [ ] `z_offset` final registrado em `SAVE_CONFIG` — pendente (§10)

---

# 8. Resultado

| Item | Antes (11/08) | Agora (25/10) |
|---|---|---|
| Data/hora | 2026-08-11 22:09 | 2026-10-25 17:04 |
| `probe_count` | 9 × 7 (63 pontos) | **7 × 5 (35 pontos)** |
| Região | 40..253 × 30..**165** | 40..253 × 30..**154** |
| Amplitude bruta | 0,988 mm | **0,417 mm** |
| Inclinação X | −0,023 mm/100 mm | **−0,063 mm/100 mm** |
| Inclinação Y | +0,534 mm/100 mm | **−0,134 mm/100 mm** |
| Deformação (resíduo) | 0,375 mm (RMS 0,075) | **0,333 mm (RMS 0,076)** |
| Aplicação | nunca carregado | pendente de `LOAD` (§10) |

Leitura: a **inclinação caiu 4×** — efeito direto do re-nivelamento mecânico. A **deformação
permaneceu praticamente igual** (RMS 0,076 mm), como esperado: é forma física da chapa, não erro de
nivelamento. A amplitude de 0,417 mm concentra-se na última linha e coluna, já na transição de borda.

---

# 9. Histórico

| Data | Evento |
|---|---|
| 2026-08-11 | Mesh original medido e salvo como `default` (9×7, 63 pontos, sonda até Y=165) |
| 2026-10-25 | Diagnóstico: perfil inerte e vencido; correção da afirmação sobre limites |
| 2026-10-25 | `PROBE_ACCURACY`: faixa 12,5 µm; tolerância ajustada de 0,010 para 0,030 |
| 2026-10-25 | Borda Y mapeada: sonda sai da chapa a partir de ~157 |
| 2026-10-25 | Malha refeita 7×5, `mesh_max 253,154`, gravada em `SAVE_CONFIG` |

---

# 10. Pendências

| # | Item | Depende de |
|---|---|---|
| 1 | Revalidar o `z_offset` **após** a malha (`PROBE_CALIBRATE` com papel ou teste de primeira camada) | presença no equipamento |
| 2 | Carregar o perfil no início da impressão (`BED_MESH_PROFILE LOAD=default`) | decisão sobre centralizar o start |
| 3 | Teste de primeira camada 240×140 com medição em 5 pontos | impressão com filamento |
| 4 | Confirmar se a última linha/coluna do perfil representa a chapa ou transição de borda | nova sondagem, se necessário |

> Enquanto o item 2 não for feito, a malha está **gravada mas não aplicada** — a máquina continua
> imprimindo sem compensação, exatamente como antes.
