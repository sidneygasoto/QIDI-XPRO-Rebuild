# Sensores de Movimento de Filamento — 2 × IdeaFormer

**Documento:** 16_Sensores_Filamento.md
**Versão:** 3.0.0
**Data:** 2026-10-27
**Objetivo:** instalar um sensor de **movimento** por extrusora, detectando fim de filamento **e**
travamento, com parada apenas quando a ferramenta ativa é a afetada.

> **Histórico de correções:** v1 tratava o sensor como chave de fim de filamento (errado); v2
> corrigiu para `[filament_motion_sensor]`; v3 incorpora o pinout confirmado da Manta, o manual do
> fabricante e a medição real de pulsos.

---

# 1. O sensor

**IdeaFormer**, encoder óptico de roda dentada: o filamento gira uma roda dentada e um sensor óptico
lateral conta os dentes. Cada dente gera um pulso no sinal.

**Medição realizada nesta unidade: 85 pulsos em 200 mm de filamento → 2,35 mm por pulso.**

Manual do fabricante (PDF sem camada de texto, apenas imagens):
[`10_Datasheets/IdeaFormer Manual.pdf`](../10_Datasheets/IdeaFormer%20Manual.pdf). Ele não traz a
pinagem elétrica — apenas renders e exemplos de configuração de Marlin/Klipper —, por isso o 5 V foi
confirmado no pinout da Manta e a ordem dos pinos do conector deve ser verificada na bancada.

| Situação | Chave de fim | **Sensor de movimento** |
|---|---|---|
| Filamento acabou | detecta | detecta |
| Filamento travou no carretel | não | detecta |
| Roda de tração moeu o filamento | não | detecta |
| Bico entupido, extrusora patinando | não | detecta |

# 2. Pinos na Manta M8P V2.0 — com o 5 V confirmado

O pinout oficial da placa mostra os conectores **END-STOP** com três pinos cada:

| Conector | Sinal | Pino 2 | Pino 3 |
|---|---|---|---|
| END-STOP 5 | **PF0** | G | **+5V** |
| END-STOP 6 | **PC15** | G | **+5V** |

Fonte: [`10_Datasheets/BIGTREETECH MANTA M8P V2.0 PinOut.png`](../10_Datasheets/BIGTREETECH%20MANTA%20M8P%20V2.0%20PinOut.png)
(bloco "END-STOP") e a configuração de referência da BTT
([`06_Firmware/generic-bigtreetech-manta-m8p-V2_0.cfg`](../06_Firmware/generic-bigtreetech-manta-m8p-V2_0.cfg), linhas 77–92).

**Portanto: o sensor pode ser alimentado pelo próprio conector do sensor de filamento**, sem puxar
5 V de outro lugar. Os dois pinos estão livres na configuração atual (nenhuma ocorrência de `PF0`
ou `PC15` em `03_Klipper_Config/`).

# 3. Diagrama

![Sensores de movimento na Manta](../08_Fotos/Filament_Sensors_Manta.png)

# 4. Ligação elétrica

| Fio do sensor | Pino do conector | Observação |
|---|---|---|
| **S** (sinal) | 1 — `PF0` (T0) / `PC15` (T1) | pulsos |
| **G** | 2 — G | terra comum |
| **V** | 3 — **+5V** | alimentação do sensor |

## 4.1 Nível do sinal

O manual do fabricante mostra o exemplo com `switch_pin: PA1` (sem pull-up). Na Manta, usar
`^PF0` / `^PC15` é seguro em qualquer caso:

- se a saída do sensor for **coletor aberto**, o pull-up interno (para 3,3 V) define o nível alto —
  e a entrada nunca vê 5 V;
- se for **push-pull de 5 V**, o pull-up não ajuda, e é preciso um divisor (ex.: 10 kΩ / 20 kΩ) ou
  um level shifter.

**Antes de fechar a caixa**, meça com o multímetro no pino S enquanto gira a roda: se o nível alto
passar de 3,5 V, coloque o condicionamento. A entrada da Manta é de 3,3 V e não tolera 5 V.

## 4.2 `detection_length`

```
detection_length  >  distância entre dois pulsos
200 mm / 85 pulsos  =  2,35 mm por pulso
```

O manual do sensor usa `12` mm, o que equivale a **~5 pulsos perdidos** antes de declarar falha —
margem boa contra falso disparo e ainda detecta travamento em poucos milímetros. Adotado: **12.0**.

Se quiser reação mais rápida, `8.0` (3 pulsos) ainda é seguro para 2,35 mm/pulso.

# 5. Configuração no Klipper

Criar `qidi_xpro/filament.cfg` e incluir no `printer.cfg` (`[include qidi_xpro/filament.cfg]`):

```ini
########################################
# Sensores de movimento de filamento
# IdeaFormer: 85 pulsos / 200 mm = 2,35 mm/pulso
########################################

[filament_motion_sensor fil_t0]
switch_pin: ^PF0
extruder: extruder
detection_length: 12.0
event_delay: 3.0
pause_delay: 0.8
pause_on_runout: True
runout_gcode:
    M118 Fim ou travamento de filamento no T0
insert_gcode:
    M118 Filamento reposto no T0

[filament_motion_sensor fil_t1]
switch_pin: ^PC15
extruder: extruder1
detection_length: 12.0
event_delay: 3.0
pause_delay: 0.8
pause_on_runout: True
runout_gcode:
    M118 Fim ou travamento de filamento no T1
insert_gcode:
    M118 Filamento reposto no T1
```

## Por que a opção `extruder:` resolve as duas ferramentas

O `[filament_motion_sensor]` só avalia o sensor **enquanto aquela extrusora está extrudando**.
Com `extruder: extruder` e `extruder: extruder1`:

- T0 imprimindo e T1 sem filamento → **não pausa**;
- T1 entra em uso sem filamento → pausa imediatamente;
- T0 patinando → pausa.

# 6. Teste

| # | Ação | Esperado |
|---|---|---|
| 1 | `QUERY_FILAMENT_SENSOR SENSOR=fil_t0` | sensor presente |
| 2 | Puxar filamento devagar pelo T0 | estado alterna, sem pausar |
| 3 | Segurar o filamento e extrudar 20 mm | pausa com mensagem do T0 |
| 4 | Repetir no `fil_t1` | idem |
| 5 | Imprimir no T0 e remover filamento do **T1** | **não** pausa |
| 6 | Durante impressão no T0, segurar o filamento | pausa em ~12 mm |
| 7 | Repor e `RESUME` | retoma sem erro |

# 7. Cuidados

1. **Nível do sinal** (item 4.1) — medir antes de fechar a máquina.
2. **GND comum** entre os dois sensores e a Manta (o próprio conector fornece).
3. **Roteamento**: junto ao feixe dos hotends, longe do cabo do termistor — sinal pulsado de alta
   impedância sofre com ruído.
4. **Sentido do filamento**: respeitar entrada/saída marcadas; roda patinando = sensor cego.
5. **`detection_length` calibrado**: 12 mm para 2,35 mm/pulso (5 pulsos).

# 8. Pendências

- [ ] Medir o nível alto do pulso no pino S (confirmar ≤ 3,3 V)
- [ ] Instalar `qidi_xpro/filament.cfg` e incluir no `printer.cfg`
- [ ] Executar o teste da seção 6
- [ ] Sincronizar `03_Klipper_Config/` + `MANIFEST` e atualizar o `README`
