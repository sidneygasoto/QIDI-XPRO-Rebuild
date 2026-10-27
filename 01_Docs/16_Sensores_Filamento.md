# Sensores de Movimento de Filamento — 2 × IdealForm

**Documento:** 16_Sensores_Filamento.md
**Versão:** 2.0.0
**Data:** 2026-10-27
**Objetivo:** instalar um sensor de **movimento** por extrusora, detectando fim de filamento **e**
travamento, com parada apenas quando a ferramenta ativa é a afetada.

> **Correção da v1.0:** o sensor não é uma chave de fim de filamento. Ele emite **pulsos** conforme
> o filamento avança. No Klipper isso é `[filament_motion_sensor]`, não `[filament_switch_sensor]`.

---

# 1. Por que o sensor de pulsos é melhor aqui

| Situação | Chave de fim | **Sensor de movimento** |
|---|---|---|
| Filamento acabou | detecta | detecta |
| Filamento travou no carretel | **não** | detecta |
| Roda de tração moeu o filamento | **não** | detecta |
| Bico entupido e extrusora patinando | **não** | detecta |

Com PETG em impressões de várias horas, o caso mais frequente não é o carretel acabar — é o
filamento parar de avançar com o carretel cheio. A chave não vê isso; o sensor de pulsos vê.

# 2. Pinos na Manta M8P V2.0

Conectores reservados pela BIGTREETECH para sensor de filamento, **livres** na configuração atual
(verificado: nenhuma ocorrência de `PF0` ou `PC15` em `03_Klipper_Config/`):

| Sensor | Pino do MCU | Conector (referência BTT) |
|---|---|---|
| T0 (extrusora 0) | **PF0** | End-Stop 5 |
| T1 (extrusora 1) | **PC15** | End-Stop 6 |

Referência: [`06_Firmware/generic-bigtreetech-manta-m8p-V2_0.cfg`](../06_Firmware/generic-bigtreetech-manta-m8p-V2_0.cfg)
linhas 77–92.

# 3. Diagrama

![Sensores de movimento na Manta](../08_Fotos/Filament_Sensors_Manta.png)

# 4. Ligação elétrica

O sensor tem **3 fios**:

| Fio | Ligar em | Observação |
|---|---|---|
| **V** | **5 V** da Manta | não usar 24 V |
| **G** | **GND** da Manta | mesmo terra dos dois sensores |
| **S** | `PF0` (T0) ou `PC15` (T1) | sinal pulsado |

## 4.1 Medição obrigatória antes de conectar S

1. Alimente o sensor com 5 V e GND, **sem** ligar o fio S na placa.
2. Com o multímetro entre S e GND, puxe o filamento devagar:
   - **0 / 3,3 V** → ligar direto;
   - **0 / 5 V** → divisor resistivo ou level shifter;
   - **0 / 24 V** → optoacoplador obrigatório.
3. Confirme que há pulsos reais ao mover o filamento (a tensão deve alternar). Sensor parado ou
   sem pulsos = defeito ou tensão insuficiente.

> A entrada da Manta é de 3,3 V. Aplicar 5 V ou 24 V no pino de sinal o destrói.

## 4.2 Intervalo entre pulsos — define o `detection_length`

O Klipper dispara quando o filamento avança **X mm sem nenhum pulso**. Portanto:

```
detection_length  >  distância entre dois pulsos consecutivos
```

Meça assim: marque 100 mm de filamento, puxe devagar e conte quantas vezes o sinal alterna. Se
houver, por exemplo, um pulso a cada 10 mm, use `detection_length: 15`. Se o sensor der vários
pulsos por milímetro (roda dentada), `7.0` é folgado.

Comece com **10.0** e reduza depois de confirmar que não há falso disparo.

## 4.3 Identificar os pinos do conector (unidade IdeaFormer)

A unidade recebida é um **encoder óptico**: roda dentada movida pelo filamento, lida por um sensor
óptico na plaquinha lateral. O conector branco é de 3 vias, mas **não vem com cabo** e não há
serigrafia confiável — descubra a ordem com multímetro, **sem alimentar**:

1. **GND** — no multímetro em continuidade, é o pino ligado ao plano de terra da plaqueta (e ao
   terminal do capacitor/ LED do sensor óptico).
2. **V** — é o pino que alimenta o LED do sensor óptico; costuma ir a um resistor e ao emissor.
3. **S** — é o que sai do coletor do fototransistor (o sinal). Normalmente com resistor de pull-up
   na própria plaqueta.

Se ficar em dúvida entre V e S: alimente **em 3,3 V primeiro** (menos risco) com o terra correto e
meça os dois pinos restantes. O que estiver em ~3,3 V fixo é V; o que alternar ao girar a roda é S.

> Só depois de identificar S é que o fio vai para `PF0` / `PC15`.

## 4.4 Cabo

O conector é JST de 2,0 mm (PH) ou 2,5 mm (XH) — **meça o passo com paquímetro** antes de comprar o
pigtail. Use cabo de 3 vias trançado, com comprimento suficiente para acompanhar o feixe dos hotends.

## 4.5 Estimativa de partida para o `detection_length`

A roda dentada tem diâmetro aproximado de 15 mm (circunferência ~47 mm) e cerca de 10 dentes, o que
dá **um pulso a cada ~4–5 mm** de filamento. Nesse caso `detection_length: 10` é folgado e seguro.
Confirme pela contagem real (item 4.2) antes de reduzir.

# 5. Configuração no Klipper

Criar `qidi_xpro/filament.cfg` e incluir no `printer.cfg` (`[include qidi_xpro/filament.cfg]`):

```ini
########################################
# Sensores de movimento de filamento
########################################

[filament_motion_sensor fil_t0]
switch_pin: ^PF0
extruder: extruder
detection_length: 10.0
pause_on_runout: True
event_delay: 3.0
pause_delay: 0.5
runout_gcode:
    M118 Fim ou travamento de filamento no T0
insert_gcode:
    M118 Filamento reposto no T0

[filament_motion_sensor fil_t1]
switch_pin: ^PC15
extruder: extruder1
detection_length: 10.0
pause_on_runout: True
event_delay: 3.0
pause_delay: 0.5
runout_gcode:
    M118 Fim ou travamento de filamento no T1
insert_gcode:
    M118 Filamento reposto no T1
```

## Por que a opção `extruder:` resolve o problema das duas ferramentas

O `[filament_motion_sensor]` avalia o sensor **somente enquanto aquela extrusora está extrudando**.
Com `extruder: extruder` e `extruder: extruder1` nos respectivos sensores:

- T0 imprimindo e T1 sem filamento → **não pausa**;
- T1 entra em uso e não tem filamento → pausa imediatamente;
- T0 patinando (entupimento) → pausa.

Isso elimina a lógica manual que a versão 1.0 deste documento usava.

# 6. Teste

| # | Ação | Esperado |
|---|---|---|
| 1 | `QUERY_FILAMENT_SENSOR SENSOR=fil_t0` | sensor detectado / state |
| 2 | Puxar filamento devagar pelo T0 | estado alterna sem pausar |
| 3 | Segurar o filamento e mandar extrudar 20 mm | pausa com mensagem do T0 |
| 4 | Repetir 1–3 no `fil_t1` | idem |
| 5 | Imprimir no T0 e remover o filamento do **T1** | **não** pausa |
| 6 | Durante a impressão no T0, segurar o filamento | pausa em até `detection_length` mm |
| 7 | Repor e mandar `RESUME` | retoma sem erro |

# 7. Cuidados

1. **Meça a tensão de S antes de conectar** (item 4.1). Não é opcional.
2. **GND comum** entre os dois sensores e a Manta.
3. **Roteamento**: passar os fios junto ao feixe dos hotends, longe do cabo do termistor. O sinal é
   pulsado e de alta impedância com pull-up; ruído gera falso disparo.
4. **`detection_length` calibrado** ao intervalo real entre pulsos (item 4.2) — valor pequeno demais
   gera pausas falsas em impressões longas.
5. Os dois sensores são instalados **antes** da extrusora, um em cada caminho de filamento; com a
   máquina desmontada é o momento de definir a fixação mecânica.

# 8. Pendências

- [ ] Confirmar a tensão de saída do IdealForm e o intervalo entre pulsos
- [ ] Definir o `detection_length` a partir da medição
- [ ] Instalar `qidi_xpro/filament.cfg`, incluir no `printer.cfg` e reiniciar
- [ ] Executar o teste da seção 6 e registrar
- [ ] Sincronizar `03_Klipper_Config/` + `MANIFEST` e atualizar o `README`
