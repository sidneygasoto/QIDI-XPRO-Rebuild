# Firmware do Relé BTT V1.2 — análise e modificação

**Documento:** 17_Relay_Firmware.md
**Versão:** 1.0.0
**Data:** 2026-10-27
**Objetivo:** estender a janela de 15–20 s do relé para que o Klipper consiga elevar o `PS_ON`
antes do corte de energia.

---

# 1. O que existe publicado (verificado)

| Item | Situação |
|---|---|
| Código-fonte (`.c` / `.h`) | **não publicado** — os 192 repositórios da conta `bigtreetech` foram listados; só há `BIGTREETECH-Relay-V1.2` (binário, manual, fotos) e `MK3_Power_Panic` (placa diferente) |
| Binário | [`10_Datasheets/Relay_V1.2_STC15W201S_original.hex`](../10_Datasheets/Relay_V1.2_STC15W201S_original.hex) — 615 bytes de arquivo, **184 bytes de código** |
| Pinagem do MCU | documentada no manual (abaixo) |

# 2. Pinagem do MCU (manual oficial)

| Pino | Função |
|---|---|
| **P3.2** | entrada do sinal de desligamento (é o `PS_ON_IN`) |
| **P5.5** | comando do relé |
| **P3.3** | detecção de curto-circuito (`SC_DET`) |
| **P5.4** | reset / restart |
| **P3.0 / P3.1** | gravação da firmware (UART) |

# 3. Leitura estática preliminar do binário

Endereços relevantes (decodificação manual, sujeita a confirmação empírica):

| Endereço | Conteúdo | Interpretação |
|---|---|---|
| `0x0000` | `LJMP 0x0095` | reset |
| `0x0095` | limpa RAM interna, `SP=#0x08`, `LJMP 0x005A` | inicialização |
| `0x005A` | `MOV P5M0,#0xFF` | P5 como saída push-pull |
| `0x005D` | `LCALL 0x00A1` | `CLR P5.5`, `CLR P3.0`, `CLR P3.1`, `SETB P3.2` |
| `0x0060` | `LCALL 0x00AC` | habilita interrupção externa (INT1 = P3.3, o `SC_DET`) |
| `0x0063` | `R7:R6 = 0x401F` → `LCALL 0x007E` | **primeira espera** (~16 415 unidades) |
| `0x006A` | `JNB P3.2,$` | espera o sinal subir |
| `0x006D` | `R7:R6 = 0x4C1D` → `LCALL 0x007E` | **segunda espera** (~19 485 unidades) |
| `0x0074` | `JNB P3.2,0x006A` | se o sinal caiu, recomeça |
| `0x0077` | `SETB P5.5` | comanda o relé |
| `0x000E` | rotina de interrupção | trata `SC_DET` |

A rotina de atraso (`0x007E`) é um laço de 16 bits com laço interno de `0x0BBE`, ou seja, o tempo é
**proporcional** ao valor `R7:R6`. Duas constantes, portanto, definem as esperas.

> **Não confiar nisto para gravar.** A polaridade de `P5.5` e a origem exata da janela de 15–20 s
> não estão resolvidas pela leitura estática. Antes de gravar qualquer coisa, caracterizar na
> bancada (seção 4).

# 4. Caracterização na bancada — sem rede elétrica

O módulo pode ser energizado só com **5 V**, com o lado AC desconectado. Assim dá para medir o
comportamento com multímetro e cronômetro, sem risco.

## 4.1 Material

- fonte de 5 V (ou a própria Manta, com o relé fora do circuito AC);
- multímetro em continuidade (para ver o contato do relé);
- jumper para forçar `P3.2` em 5 V ou GND;
- cronômetro.

## 4.2 Procedimento

| # | Ação | O que registrar |
|---|---|---|
| 1 | Alimentar 5 V e GND; **não** conectar AC | o relé comuta? em quanto tempo? |
| 2 | Medir continuidade em `AC OUT` após ligar | contato aberto ou fechado? |
| 3 | Forçar `P3.2` em 5 V | o contato muda? em quanto tempo? |
| 4 | Soltar `P3.2` (para GND) | quanto tempo até o contato abrir? |
| 5 | Repetir 3–4 três vezes | o tempo se repete? |
| 6 | Medir `P3.3` | nível em repouso |

Com isso ficam respondidas as três dúvidas: **polaridade** de `P5.5`, **qual espera** corresponde
aos 15–20 s, e **o que acontece** quando o sinal nunca sobe.

# 5. Dois caminhos para modificar

## 5.1 Caminho A — gravar firmware próprio (recomendado)

Escrever um programa novo para o STC15W201S (~80 linhas de C), com o atraso definido por constante:

```
ao energizar:  fecha o relé (mantém a carga)
               espera P3.2 subir por até T segundos (T = 120)
               se P3.2 subir  -> trava em "ligado" e só desliga quando P3.2 cair por T segundos
               se P3.2 não subir em T -> abre o relé (proteção)
               se P3.3 indicar curto -> abre imediatamente
```

Vantagens: comportamento documentado, `T` explícito, sem engenharia reversa.
Custo: compilar com SDCC (gratuito) e gravar; validar na bancada antes da rede.

## 5.2 Caminho B — corrigir o binário existente

Alterar as constantes `0x401F` / `0x4C1D` no `.hex` (recalculando os checksums) e regravar. O atraso
é proporcional ao valor, então `0xFFFF` daria ~4× o tempo atual.

Risco: a semântica das duas esperas não está confirmada — o patch pode não alterar a janela que
importa, ou pode eliminar a proteção. Só é aceitável **depois** da caracterização da seção 4.

# 6. Gravação

O STC15W201S grava por **UART** (P3.0 = RXD, P3.1 = TXD), com o chip reiniciado no momento em que o
programador se conecta. Procedimento geral:

1. Adaptador USB-serial (CH340/CP2102) em **3,3 V**: TX→P3.0, RX→P3.1, GND→GND.
2. Alimentar o módulo com 5 V (separado, ou pelo adaptador se ele fornecer 5 V).
3. Abrir o **STC-ISP**, selecionar `STC15W201S`, carregar o `.hex`.
4. Clicar em "Download/Program" e **ciclar a alimentação** do módulo (P5.4 a GND → soltar, ou
   desligar/ligar os 5 V).
5. Confirmar a mensagem de sucesso e verificar o comportamento na bancada.

> Nunca grave com a rede 220 V conectada ao módulo.

# 7. Pendências

- [ ] Executar a caracterização da seção 4 e registrar tempos e polaridade
- [ ] Decidir entre caminho A e B com base na caracterização
- [ ] Gravar e validar na bancada (5 V, sem rede)
- [ ] Só então religar o lado AC e repetir os testes de 15_Relay_Energia.md
