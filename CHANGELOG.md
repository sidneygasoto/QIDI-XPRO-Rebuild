# Changelog

Todas as mudanças relevantes deste projeto são documentadas neste arquivo.

O formato segue os princípios do **Keep a Changelog** e o projeto adota **Semantic Versioning**.

---

# [0.3.0] — 2026-10-25 — Consolidação e produção validada

Marco de saneamento: a configuração real da máquina passou a ser versionada e as três árvores
divergentes foram reconciliadas em um único caminho.

## Adicionado

- `03_Klipper_Config/` — espelho byte a byte da configuração ativa na CB1 (15 arquivos), com
  `MANIFEST.sha256` conferido contra a máquina.
- `03_Klipper_Config/README.md` — descrição dos parâmetros que definem a máquina e procedimento de
  aplicação.
- `05_Metrology/` — preservação da extensão de metrologia: código-fonte, patches staged/unstaged,
  estado do git, tarballs e `PROVENANCE.md`.
- `07_Backup/config_v0.1.0_2026-07/` — árvore de julho da fase pré-calibração, com `NOTE.md`.
- `07_Backup/config_2026-07-28_v0.2.5/commit-tree/` — árvore do commit `cb7f9fc` (geometria + dual nozzle),
  com `NOTE.md`.
- `07_Backup/*/NOTE.md` — avisos explícitos de que essas árvores **não** devem ser restauradas.
- `05_Metrology/PROVENANCE.md` — registro completo da captura de 25/10/2026.

## Alterado

- `00_Estado_Atual.md` reescrito como **v0.3.0**, substituindo duas seções contraditórias
  (v0.2.0 de 09/07 e “21/07”) por dados verificados na máquina.
- `11_Config_qidi_xpro/klipper/` movido para `07_Backup/config_v0.1.0_2026-07/`; a configuração
  passa a ser lida em `03_Klipper_Config/`.
- `CHANGELOG.md` reestruturado: cabeçalho duplicado removido, versões 0.2.0 e 0.2.5 separadas.
- `releases.md` e `README.md` alinhados à versão 0.3.0 e à estrutura real do repositório.

## Corrigido

- Documentação afirmava **sensorless homing** em X/Y; a máquina opera com **endstops mecânicos** e
  home no máximo.
- Documentação afirmava que a sonda não estava ativa; `[probe]` está ativo com `z_offset 0,652`.
- Credenciais padrão `root/root` documentadas em `02_Plataforma_CB1.md` estão **obsoletas**.
- Registrado que a extensão de metrologia **não carrega** (erro de sintaxe + API divergente),
  contrariando o status “framework em desenvolvimento” anterior.

## Observações

- A máquina opera em produção desde outubro; o repositório estava 89 dias atrasado.
- Nenhum arquivo de configuração da CB1 foi alterado nesta versão.

---

# [0.2.5] — 2026-07-28 — Geometria e dual nozzle

Commit `cb7f9fc`, tag anotada `v0.2.5` (a mensagem do commit diz “v0.2.0”).

## Adicionado

- Calibração geométrica: `rotation_distance 33.7298055705` em X/Y e `32.8449` nas extrusoras.
- Homing sensorless (`virtual_endstop`, `diag_pin PF4/PF3`, `SGTHRS 55/60`) — posteriormente
  abandonado na máquina.
- Offsets entre bicos via `SET_GCODE_OFFSET` (`T1`).
- `probe.cfg` e `adxl345.cfg` como arquivos próprios.
- Snapshot completo da configuração em `07_Backup/config_2026-07-28_v0.2.5/machine-snapshot/`.

## Alterado

- Limites de eixo ampliados (`X -14..262`, `Y -4..174`).

## Nota

- `probe.cfg` não era incluído pelo `printer.cfg` — a sonda não estava ativa nesta versão.

---

# [0.2.0] — 2026-07-09 — Infraestrutura Klipper funcional

## Adicionado

- Instalação do Armbian 26.5.1 na BIGTREETECH CB1.
- Instalação do Klipper Host, Moonraker e Fluidd.
- Comunicação USB entre CB1 e Manta M8P V2.0.
- Configuração inicial da impressora e dos cinco drivers TMC2209 em UART.
- Configuração dos dois hotends independentes, da mesa aquecida e dos ventiladores.
- Configuração do endstop mecânico de Z e do probe indutivo.
- Atualização do firmware STM32 para Klipper v0.13.
- Integração do ADXL345 via SPI3 da Manta e calibração completa do Input Shaper.
- Calibração PID dos dois hotends e da mesa.

## Alterado

- Abandonado o uso do Linux MCU da CB1 para o ADXL345; migração definitiva para SPI3 da Manta.

## Corrigido

- Incompatibilidade Host/MCU.
- Chip Select do ADXL345 (conflito em PA11, uso de PA15).
- Ajustes de limites dos eixos.

---

# [0.1.1] — 2026-07-06 — Correção de rede

## Corrigido

- Desabilitada a conexão Wi-Fi automática do CB1, que causava alerta ARP no ESET por ativação
  simultânea de `eth0` e `wlan0`.

---

# [0.1.0] — 2026-07-06 — Foundation

Primeira versão documentada do projeto. Representa a conclusão da preparação da plataforma de
hardware e software necessária para iniciar o retrofit.

## Adicionado

### Estrutura do Projeto

- Estrutura oficial do repositório GitHub e organização da documentação técnica.
- Fluxo de documentação baseado em pacotes e versionamento com SemVer.

### Hardware

- Controladora BIGTREETECH Manta M8P V2.0; host CB1 V2.2; 5× TMC2209 em UART.
- 2× Trianglelab Ceramic Hotend com sensores NTC100, máximo 320 °C.
- Sensor indutivo industrial AECO (M8, PNP), instalado entre os hotends, ~0,9 mm sobre a chapa PEI.
- Placa de iluminação própria: 3 LEDs brancos, resistores de 100 Ω, entre os hotends.

### Arquitetura

- Mantida a arquitetura original: dual extruder, mesmo carro, sem conversão para IDEX.

### Sistema Operacional

- Imagem `CB1_Debian13_minimal_kernel7.0_20260430` — Debian 13 (Trixie), kernel 7.0.2.
- Atualização completa do sistema, sem falhas de serviço após reinício.

### Descobertas Técnicas

- **DP-001:** o CB1 inicializa pelo slot `SoC-SDcard`, apesar da serigrafia da placa.
- **DP-002:** na imagem utilizada as credenciais eram `root/root` (usuário `biqu` inexistente).
  *Obsoleto desde então — ver 0.3.0.*
- **DP-003:** ausência de terminal local via HDMI no primeiro boot; configuração por SSH.
- **DP-004:** SPI habilitado apenas pelo overlay `spidev0_0`.
- **DP-005:** imagem já otimizada para microSD (ZRAM, log2ram, tmpfs).

### Backups

- `Backup_0` — Debian instalado e atualizado, SPI habilitado, rede e SSH validados.

### Documentation

- README, CHANGELOG, Roadmap, Introdução, Plataforma CB1, Histórico de Backups.

---

# Trabalho não incorporado a uma versão

| Item | Situação |
|---|---|
| Documentação da câmera (`13_Camera/`) | commits locais `4a65a23` e `b954875`, não presentes em `origin/main`; etapa pausada por incompatibilidade de hardware |
| Extensão de metrologia | branch `feature/metrology-framework` dentro do Klipper da CB1, com 3 commits locais e alterações não commitadas; preservada em `05_Metrology/` |

---

# Notas de versionamento

- As tags `v0.1.2` e `v0.1.3` apontam para commits cuja mensagem é “Primeira versão funcional do
  retrofit”, duplicando o rótulo `v0.1.0`.
- A tag `v0.2.0` é leve e aponta para o commit da stack Klipper/Moonraker/Fluidd.
- A tag `v0.2.5` é anotada e aponta para o commit cuja mensagem diz “v0.2.0”.
- A normalização das tags está pendente e exige autorização específica.

---

# Histórico de versões

| Versão | Data | Descrição |
|---|---|---|
| 0.3.0 | 2026-10-25 | Consolidação da configuração e validação do estado de produção |
| 0.2.5 | 2026-07-28 | Geometria e calibração dual nozzle |
| 0.2.0 | 2026-07-09 | Infraestrutura Klipper, Moonraker e Fluidd |
| 0.1.1 | 2026-07-06 | Correção de rede (Wi-Fi desabilitado) |
| 0.1.0 | 2026-07-06 | Foundation — plataforma preparada |
