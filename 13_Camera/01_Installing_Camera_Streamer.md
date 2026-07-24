# Instalação do Camera Streamer

## Objetivo

Instalar e compilar o **camera-streamer** no **BIGTREETECH CB1**, fornecendo a infraestrutura necessária para o streaming de vídeo integrado ao Klipper.

---

## Ambiente

### Hardware

- BIGTREETECH CB1 V2.2
- Arquitetura ARM64
- Sistema operacional Debian 13

### Software

- Klipper
- Moonraker
- Fluidd

---

## Dependências

Atualize o sistema:

```bash
sudo apt update
```

Instale as dependências necessárias para compilação:

```bash
sudo apt install -y \
    git \
    build-essential \
    cmake \
    pkg-config \
    libevent-dev \
    libjpeg-dev \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libcamera-dev \
    libssl-dev \
    xxd
```

---

## Estrutura de diretórios

Criar o diretório de trabalho:

```bash
sudo mkdir -p /opt/camera-streamer
sudo chown -R $USER:$USER /opt/camera-streamer
```

---

## Obtenção do código-fonte

```bash
cd /opt/camera-streamer

git clone https://github.com/ayufan/camera-streamer.git source

cd source
```

---

## Inicialização dos submódulos

```bash
git submodule update --init --recursive
```

---

## Compilação

Compilar utilizando apenas um núcleo de processamento:

```bash
make -j1
```

> **Observação**
>
> A compilação em núcleo único reduz significativamente o consumo de memória do CB1 e evita interrupções durante o processo.

---

## Validação da compilação

Verificar a existência do executável:

```bash
ls -lh camera-streamer
```

Resultado esperado:

```text
-rwxrwxr-x ... camera-streamer
```

Verificar a arquitetura do executável:

```bash
file camera-streamer
```

Resultado esperado:

```text
ELF 64-bit LSB pie executable, ARM aarch64
```

Verificar a execução:

```bash
./camera-streamer --help
```

O programa deverá exibir a lista completa de parâmetros suportados.

---

## Resultado

Ao término desta etapa, o executável **camera-streamer** encontra-se compilado e pronto para configuração.

Nesta fase não é realizada a instalação do serviço `systemd` nem a integração com o Moonraker.

Essas etapas são documentadas nos próximos capítulos.

---

## Critérios de validação

- [x] Dependências instaladas.
- [x] Repositório clonado.
- [x] Submódulos inicializados.
- [x] Compilação concluída sem erros.
- [x] Executável gerado.
- [x] Executável iniciado com sucesso utilizando `--help`.