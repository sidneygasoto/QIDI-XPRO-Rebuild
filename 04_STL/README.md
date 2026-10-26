# STL — Teste de Primeira Camada

## `Bed_Level_5x40x40_0.2mm.stl`

Arquivo de teste para validar a primeira camada em **cinco pontos** da mesa, conforme o critério de
aceite de [`01_Docs/07_Bed_Mesh.md`](../01_Docs/07_Bed_Mesh.md) §7.

| Propriedade | Valor |
|---|---|
| Formato | STL binário, 60 triângulos |
| Elementos | 5 pastilhas de 40 × 40 mm |
| Altura | 0,20 mm (uma camada) |
| Extensão | X 25..235 · Y 22..142 |
| Área impressa | 8.000 mm² — ~2 g de PETG |
| Centros | (45, 42) · (215, 42) · (130, 82) · (45, 122) · (215, 122) |

## Por que os centros foram deslocados

A malha cobre as coordenadas da **sonda** de 40..253 × 30..154, o que corresponde ao **bico** em
22..235 × 19..143. As pastilhas foram posicionadas para caber integralmente nessa faixa; fora dela
o Klipper extrapola a correção das bordas, e o teste mediria a extrapolação em vez da malha.

## Fatiamento

| Parâmetro | Valor |
|---|---|
| Camada inicial | 0,20 mm |
| Perímetro | 0 (a peça tem uma única camada) |
| Preenchimento | 100 % sólido / linhas |
| Brim / skirt | 0 (opcional: brim 3 mm para aderência) |
| Filamento | PETG, mesa 80 °C, bico conforme o perfil |

O fatiador deve gerar exatamente **uma camada**. Se aparecerem duas, a altura do STL (0,20 mm) não
coincide com a camada inicial do perfil.

## Como avaliar

1. Imprimir e deixar esfriar.
2. Medir a espessura de cada pastilha com paquímetro (3 leituras por pastilha).
3. Comparar com a camada nominal de 0,20 mm.

| Resultado | Interpretação |
|---|---|
| 0,17–0,23 mm em todas | aprovado |
| variação > 0,03 mm entre pastilhas | malha ou nivelamento fora de tolerância |
| uniformemente < 0,17 mm | bico baixo — revisar `z_offset` |
| uniformemente > 0,23 mm | bico alto — revisar `z_offset` |
| uma pastilha isolada fora | conferir se o local está dentro da cobertura da malha |

## Histórico

| Data | Evento |
|---|---|
| 2026-10-26 | Arquivo criado para validar a malha recalibrada e o `z_offset` de 0,515 mm |
