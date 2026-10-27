# Relé de Energia — BTT Relay V1.2 + Manta M8P V2.0

**Documento:** 15_Relay_Energia.md
**Versão:** 1.0.0
**Data:** 2026-10-27
**Objetivo:** permitir desligar a impressora pelo painel (Fluidd), cortando a rede elétrica depois
que o host conclui o desligamento.

> **PERIGO — RISCO DE CHOQUE ELÉTRICO E INCÊNDIO.** Este documento descreve intervenção na rede
> 220 V. Monte com a tomada desligada, isole o módulo, confira a serigrafia da placa e, se não tiver
> habilitação para trabalho em instalações elétricas, execute a parte de rede com um eletricista.

---

# 1. Como a placa funciona

| Terminal | Função |
|---|---|
| `AC IN` (L / N) | entrada da rede — 85 a 265 V AC, 50/60 Hz |
| `AC OUT` (L / N) | saída que alimenta a fonte da impressora |
| `SC_DET` (5 V + GND) | monitora a linha de 5 V; curto ou perda de 5 V corta a energia |
| `PS_ON_IN` (sinal + GND) | controle: **nível ALTO mantém ligado**; nível baixo ou ausente desliga em **15–20 s** |

O módulo tem próprio MCU (STC15W201S), aceita lógica de 3,3 V ou 5 V e mantém a alimentação por
15–20 s após o sinal cair — tempo que permite ao Linux encerrar com segurança.

# 2. Decisão de projeto: quem comanda o relé

Duas opções foram avaliadas:

| Opção | Como funciona | Problema |
|---|---|---|
| **A — `PS_ON` da Manta (PD14)** | o firmware corta a energia | o MCU é alimentado pela mesma fonte: ao cortar a AC, a CB1 morre sem desligar o sistema de arquivos → risco de corromper o cartão |
| **B — GPIO da CB1 (PC8, pino 40)** | o host mantém a linha alta; ao concluir o `poweroff`, a linha cai e o relé corta a AC 15 s depois | exige overlay + serviço na CB1 |

**Adotada: opção B.** É a única que garante corte de energia **depois** do desligamento limpo do
host. O `PS_ON` da Manta (PD14) permanece desligado do módulo.

# 3. Diagrama

![Ligação do relé à Manta e à CB1](../08_Fotos/Relay_V12_Manta_M8P.png)

# 4. Ligações, ponto a ponto

| # | Origem | Destino | Observação |
|---|---|---|---|
| 1 | Rede — condutor F (ou L, conforme a instalação) | `AC IN` do relé | passar por fusível/disjuntor da impressora |
| 2 | Rede — neutro | `AC IN` (N) do relé | manter a polaridade |
| 3 | `AC OUT` do relé — L e N | entrada AC da fonte 24 V | é a fonte da impressora que será comutada |
| 4 | `SC_DET` 5 V e GND | `5V` e `GND` da Manta | monitor de curto; sem ele, a proteção não atua |
| 5 | `PS_ON_IN` sinal | **CB1, pino físico 40 (GPIO21 / PC8)** | sinal de 3,3 V |
| 6 | `PS_ON_IN` GND | GND da CB1/Manta | referência comum obrigatória |
| 7 | — | `PS_ON` (PD14) da Manta | **deixar desconectado** |

> Confira na serigrafia da sua unidade: os nomes usados aqui são os documentados pela BTT
> (`AC IN`, `AC OUT`, `SC_DET`, `PS_ON_IN`). Em versões antigas do manual os mesmos conectores
> aparecem apenas nos desenhos.

# 5. Software

## 5.1 CB1 — manter a linha alta

A CB1 precisa elevar o `PS_ON_IN` **antes** dos 15 s, senão o relé corta a energia durante o boot.
Isso é resolvido com:

1. **overlay de device tree** expondo o pino 40 como linha GPIO nomeada (`btt-relay`);
2. **serviço systemd** que solicita a linha como saída e a mantém em nível alto durante toda a
   operação. Quando o sistema encerra, o serviço termina, a linha cai e o relé corta a energia
   após o atraso.

Implementação de referência, já validada para CB1 v2.2 + Manta: [`evgs/power_cb1`](https://github.com/evgs/power_cb1).
Verificação após instalar:

```bash
sudo apt install gpiod
gpioinfo | grep btt
# esperado: line 72: unnamed "btt-relay" output active-high [used]
```

## 5.2 Klipper / Moonraker

Nada muda no `printer.cfg`. O desligamento pelo painel já existe:

```ini
[gcode_macro SHUTDOWN_HOST]
description: Desliga a CB1 com segurança
gcode:
    {action_call_remote_method("shutdown_machine")}
```

Fluxo completo: **`SHUTDOWN_HOST`** → Moonraker encerra o sistema (`systemd_dbus`, `shutdown_action: poweroff`)
→ o serviço do relé termina → `PS_ON_IN` cai → **15–20 s depois a AC é cortada**.

O `poweroff` configurado no `moonraker.conf` é pré-requisito:

```ini
[machine]
provider: systemd_dbus
shutdown_action: poweroff
```

# 6. Como ligar a impressora

A placa **não tem botão de ligar**. O manual só descreve `P5.4` como pino de reset/gravação de
firmware do MCU. A sequência real de partida é:

1. aplicar rede ao módulo → o relé **fecha por padrão** e alimenta a fonte;
2. a CB1 inicia o boot e o overlay de device tree eleva `PS_ON_IN` (~2–3 s, via u-boot);
3. com o sinal alto, o relé **fica retido**;
4. se o sinal não subir em **15–20 s**, o relé abre e a impressora desliga sozinha.

> **Consequência prática:** após desligar pelo painel, a **chave geral continua ligada** e o relé
> está aberto. Para religar é preciso **ciclar a rede** (chave geral desligar/ligar) ou instalar um
> botão.

## 6.1 Opções de botão de ligar

| Opção | Como funciona | Cuidado |
|---|---|---|
| **Pulsador NA de rede em série com a fase** | um toque aplica AC, a CB1 arranca e retém — comportamento tipo ATX | componente e fiação isolados para 220 V, em caixa fechada |
| **Tomada inteligente / interruptor de parede** | liga remotamente, sem tocar na máquina | suportar a corrente de pico da fonte |
| **Jumper de `PS_ON_IN` ao 3,3 V** | mantém o relé fechado sem a CB1, apenas para manutenção | **nunca** em uso normal: anula a proteção |

## 6.2 O que faz o sistema entrar em loop de boot

O sinal precisa subir **antes dos 15–20 s**. Se for elevado por um **serviço systemd**, ele só atua
depois do Linux subir (~20–30 s na CB1) e o relé corta no meio do boot. Por isso o overlay precisa
ser um **hog de device tree** com `output-high`, aplicado pelo u-boot — não um serviço tardio.

# 7. Cuidados específicos desta placa

1. **O relé alimenta a carga por padrão** quando a rede é aplicada. Ligar a chave geral energiza a
   impressora e a CB1 inicia o boot; se o sinal não subir em 15–20 s, o módulo corta tudo e o ciclo
   recomeça. **Meça o tempo de boot antes de deixar a máquina sozinha.**
2. **Chave geral continua sendo o corte definitivo.** O relé não substitui a chave nem o fusível.
3. **Isolamento**: o módulo trabalha com 220 V expostos. Use caixa isolada.
4. **Não ligue o `PS_ON` da Manta no relé** — é a opção A, descartada.
5. O `SC_DET` deve ser ligado à linha de 5 V **da própria Manta**, não ao 24 V.
6. **Host morto = impressora desligada em 15–20 s.** É uma boa proteção, mas impede diagnóstico com
   a máquina energizada; para manutenção use o jumper do item 6.1 com consciência do risco.

# 8. Plano de teste (antes de confiar no painel)

| # | Teste | Critério |
|---|---|---|
| 1 | Continuidade e isolação, tudo desligado | nenhum curto entre L, N e terra |
| 2 | Ligar com a chave geral, sem a CB1 | relé liga a fonte por padrão e corta após 15–20 s |
| 3 | Medir `PS_ON_IN` com a CB1 ligada | 3,3 V (alto) |
| 4 | Cronometrar do AC até o sinal alto | **abaixo de 15 s** |
| 5 | `SHUTDOWN_HOST` pelo Fluidd | CB1 desliga; AC cai 15–20 s depois |
| 6 | Religar ciclando a chave geral | sistema sobe sem intervenção |
| 7 | Repetir 5 e 6 três vezes | comportamento consistente |
| 8 | Simular `SC_DET` (desconectar o 5 V) | relé corta a energia |

# 9. Pendências

- [ ] Confirmar na serigrafia os nomes dos conectores da unidade recebida
- [ ] Instalar o overlay (hog) na CB1 e medir o tempo até `PS_ON_IN` ficar alto
- [ ] Decidir a forma de ligar: ciclar a chave, pulsador ou tomada inteligente
- [ ] Executar o plano de teste da seção 8 e registrar os tempos
- [ ] Atualizar o `README` (seção de hardware) e o `00_Estado_Atual` após validação
