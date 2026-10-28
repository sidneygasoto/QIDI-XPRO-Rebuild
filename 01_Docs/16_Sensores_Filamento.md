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

## 4.1 Condicionamento adotado — divisor 1,2 k / 2 k

O sensor (`SN74LVC1G14`, saída **push-pull de 5 V**) não pode ir direto ao pino. Adotado:

```
S do sensor ──[ 1,2 k ]──┬──> pino da Manta (PF0 / PC15)
                         │
                      [ 2 k ]
                         │
                        GND
```

A rede da própria Manta contribui com **10 kΩ de pull-up para 3,3 V + 1 kΩ em série + 100 nF para
GND** em cada entrada de fim de curso (R21/R25, R26/R27, R28/R30, R36/R38, R39/R40, R43/R46 e
C17/C18/C22/C25/C27/C29).

**Medido no pino da Manta:** **3,1 V** (nível 1) e **0,2 V** (nível 0).

| Nível | Medido | Limite do STM32H723 | Margem |
|---|---|---|---|
| Alto | 3,1 V | V_IH ≥ 0,7 × VDD = **2,31 V** | 0,8 V |
| Baixo | 0,2 V | V_IL ≤ 0,3 × VDD = **0,99 V** | 0,8 V |

> Um diodo 1N4148 em série foi descartado: com o 1 kΩ da placa, o nível baixo subiria para ~0,8 V
> (sem o resistor externo) ou ~1,0 V (com ele), encostando no limite de V_IL.

O `^` no `switch_pin` continua correto: o pull-up de 10 kΩ já existe na placa, e o `^` é inofensivo.

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

# 6. Validação (2026-10-28)

Método: arquivo [`09_Testes/teste_sensor_filamento.gcode`](../09_Testes/teste_sensor_filamento.gcode)
— `G28`, vai a Z=50 e extrusa 50 mm no ar (sem sujar a chapa), ~30 s.

## 6.1 Comportamento do Klipper que precisa ser conhecido

Duas condições, ambas confirmadas no código instalado:

1. **O sensor só é avaliado durante impressão.** `filament_motion_sensor.py` registra
   `idle_timeout:printing` (liga o timer) e `idle_timeout:ready`/`idle` (desliga). Em `standby` o
   timer vai para `NEVER` — **testar com `G1 E50` fora de impressão não prova nada**.
2. **O runout exige transição de estado.** `RunoutHelper` inicializa `filament_present = False` e
   `note_filament_present` retorna sem agir se o estado não mudou. Logo, é preciso que haja pulsos
   (estado vai a `True`) para que a ausência deles possa disparar o runout.

| Teste | Condição | Resultado |
|---|---|---|
| **Positivo** | E0 conectado, filamento no local | 50 mm extrudados durante impressão, **sem pausa**, `fil_t0` permaneceu `True` |
| **Negativo** | E0 desconectado (sem pulsos) | `runout event detected`, impressão **pausada**, `fil_t0 = False` |

A pausa do teste negativo ocorreu a 89,8 % do arquivo — correto: os 12 mm de detecção só são
contados a partir do momento em que o extrusor anda, e o `G1 E50` era a última linha.

# 7. Cuidados

1. **Nível do sinal** — 3,1 V / 0,2 V medidos; refazer a medida se trocar o divisor.
2. **GND comum** entre os dois sensores e a Manta (o próprio conector fornece).
3. **Roteamento**: junto ao feixe dos hotends, longe do cabo do termistor.
4. **Sentido do filamento**: respeitar entrada/saída marcadas; roda patinando = sensor cego.
5. **`detection_length` calibrado**: 12 mm para 2,35 mm/pulso (5 pulsos).

# 8. Pendências

- [x] Nível do pulso medido: **3,1 V** (alto) e **0,2 V** (baixo)
- [x] `qidi_xpro/filament.cfg` instalado e incluído no `printer.cfg` (`MANIFEST` 17/17)
- [x] E0 validado — testes positivo e negativo
- [ ] Validar **E1 (T1)** — exige aquecer o T1 e carregar filamento nele
- [ ] Teste de troca de ferramenta: T0 imprimindo com T1 sem filamento **não** deve pausar
