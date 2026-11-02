# Calibração para PLA — T0

**Documento:** 19_Calibracao_PLA.md
**Versão:** 1.0.0
**Data:** 2026-10-31
**Objetivo:** levar a impressora ao melhor resultado possível com **PLA no hotend 0**, na ordem em
que cada grandeza depende da anterior.

---

# 1. Ordem e por quê

| # | Etapa | Depende de | Precisa de impressão? |
|---|---|---|---|
| 1 | **Input shaping** (vibração) | nada — independe de temperatura | não |
| 2 | **Malha da mesa a 60 °C** | temperatura de impressão | não |
| 3 | **Offset de Z a quente** | malha | não |
| 4 | **Pressure advance** | filamento, mesa e Z corretos | sim (torre/torres) |
| 5 | **Multiplicador de fluxo** | PA calibrado | sim (cubo) |
| 6 | **Torre de temperatura** | fluxo correto | sim |
| 7 | **Retração / stringing** | temperatura escolhida | sim |
| 8 | **Vazão máxima (volumétrica)** | tudo acima | sim |

**Por que a malha vem antes de tudo que imprime:** a chapa empena com a temperatura — foi medido
0,2 mm de deflexão nos pontos de fixação entre frio e quente. Uma malha medida a 80 °C (PETG) **não
vale** para impressão a 60 °C (PLA). A malha precisa ser medida **no mesmo estado térmico** da
impressão: mesa na temperatura de trabalho e bico quente.

# 2. Etapa 1 — Input shaping ✅ (2026-10-31)

`SHAPER_CALIBRATE` com o ADXL345 da CB1 (SPI), ponto de medição (115, 75, 20).

| Eixo | Shaper | Frequência | Vibração residual | Suavização |
|---|---|---|---|---|
| **X** | `3hump_ei` | **67,2 Hz** | 0,0 % | 0,297 |
| **Y** | `ei` | **37,2 Hz** | 0,0 % | 0,238–0,292 |

Ajuste de referência medido: `ei` 37,2 Hz, `2hump_ei` 44,0 Hz e `3hump_ei` 55,2 Hz no eixo Y.

Gravado em `[input_shaper]` via `SAVE_CONFIG`; configuração ativa conferida após o restart.

> O Y ressoa em 37 Hz e o X em 67 Hz — diferença grande, coerente com a mesa móvel no Y. Se um dia
> aparecer ringing só em uma direção, é o eixo de 37 Hz.

# 3. Etapa 2 — Malha a 60 °C

Procedimento: com o PLA carregado, aquecer **mesa 60 °C e bico 215 °C**, aguardar estabilizar
(potência da mesa abaixo de 25 %) e então:

```
BED_MESH_CALIBRATE
SAVE_CONFIG
```

O perfil anterior (`default`, medido a 80 °C) é **substituído**. Se for voltar a imprimir PETG, é
preciso re-medir a 80 °C — a malha não é transferível entre temperaturas.

# 4. Etapa 3 — Offset de Z a quente

Método do papel (0,10 mm) no centro e nos três parafusos, com mesa e bico na temperatura de
impressão. Registrar o valor encontrado e ajustar `z_offset` com `PROBE_CALIBRATE` + `SAVE_CONFIG`.

Referência atual: `z_offset = 0,550` (ajustado para PETG a 250 °C / mesa 80 °C — **não** deve ser
reutilizado sem conferência).

# 5. Etapa 4 — Pressure advance

PLA é o filamento em que o PA mais aparece (é rígido e o filete tem memória elástica curta).

Método: torre de PA (Orca: *Calibration → Pressure Advance*), com `SET_PRESSURE_ADVANCE ADVANCE=…`
variando por altura, ou linha a linha. Registrar o valor que elimina o *bulge* nos cantos sem
deixar falha no início da linha.

Valor atual em uso: `pressure_advance = 0,0885` (único para as duas extrusoras — revisar).

# 6. Etapas 5 a 8

| Etapa | Como medir | Critério |
|---|---|---|
| Fluxo | cubo vazado de parede única | espessura medida × fluxo atual = novo fluxo |
| Temperatura | torre 195–225 °C | melhor equilíbrio entre brilho, resistência e stringing |
| Retração | teste de stringing em escada | menor distância/velocidade sem fios |
| Vazão máxima | aumento gradual de velocidade | ponto em que a extrusão falha |

# 7. Números de partida (Orca, perfil PLA)

| Parâmetro | Valor |
|---|---|
| Bico / mesa | 215 °C / 60 °C |
| Primeira camada | 0,20 mm, 20 mm/s |
| Altura de camada | 0,20 mm |
| Fluxo | 1,0 (a calibrar) |
| PA | 0,0885 (a calibrar) |
| Retração | a calibrar |

# 8. Registro de resultados

| Etapa | Valor encontrado | Data |
|---|---|---|
| Input shaping X | `3hump_ei` 67,2 Hz | 2026-10-31 |
| Input shaping Y | `ei` 37,2 Hz | 2026-10-31 |
| Malha 60 °C | 5×7, **−0,657 a −0,185** (amplitude 0,472, média −0,331) | 2026-11-02 |
| **z_offset PLA** | **0,900** (antes 0,550 / PETG) | 2026-11-02 |
| Pressure advance | — | pendente |
| Fluxo | — | pendente |
| Temperatura | — | pendente |
| Retração | — | pendente |
| Vazão máxima | — | pendente |

# 9. O que a calibração de Z ensinou (2026-11-02)

O `z_offset` foi de **0,550 → 0,900**. Esse erro de 0,35 mm não foi detectado pelo teste de papel,
por três motivos que se somaram:

1. **o papel embute a própria espessura** — ele para de passar quando a folha encosta, não quando o
   bico toca a mesa;
2. **o bico quente baba** — um fio de PLA na ponta faz o papel "encostar" antes do bico, e o
   resultado muda a cada minuto;
3. **o valor era herdado de outro filamento** (PETG a 250 °C / mesa 80 °C).

A medida que resolveu foi a **primeira camada impressa**, com deslocamento conhecido via
`SET_GCODE_OFFSET`: em +0,10 mm o filamento não aderia (alto), em −0,30 saiu película fina com
linhas separadas e em −0,35 saiu camada fechada. O deslocamento foi então **incorporado** ao
`z_offset` com `Z_OFFSET_APPLY_PROBE` (0,55 + 0,35 = 0,90) e validado por impressão de confirmação,
que saiu perfeita.

> **Regra que ficou:** a malha é **herdeira do `z_offset`**. Ao mudar o `z_offset`, os valores da
> malha ficam defasados pela mesma quantidade e **precisam ser re-medidos**. Não foi o que fiz de
> início, e a impressão de confirmação saiu sem adesão — o erro de 0,35 voltou embutido na malha.
> Depois de re-medir, a média da malha deslocou-se exatamente 0,331 mm, confirmando o diagnóstico.
