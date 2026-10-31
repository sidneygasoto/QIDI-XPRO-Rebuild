# Configuração do Fluidd

## Objetivo

Documentar a integração da câmera com o **Moonraker** e a interface **Fluidd**.

> **Status: resolvido em 2026-10-31.** O `camera-streamer` foi descartado (build sem libav) e o
> stream passou a ser servido pelo **uStreamer**, com proxy no nginx. O contexto completo está em
> [`01_Docs/18_Obico.md`](../01_Docs/18_Obico.md). Este documento registra o **motivo técnico** do
> proxy.

---

## 1. Cadastro no Moonraker

```ini
[webcam qidi_xpro]
location: Impressora
service: mjpegstreamer
stream_url: http://192.168.10.126/webcam/?action=stream
snapshot_url: http://192.168.10.126/webcam/?action=snapshot
```

## 2. Por que o stream **não** pode ficar em `:8080`

O Fluidd não usa `<img src="...">` para MJPEG. Ele usa um **Web Worker** que baixa o stream com
`fetch()` e entrega cada quadro como `Blob`:

```js
// MjpegstreamerCamera-*.js
let t = this.buildAbsoluteUrl(this.camera.stream_url || '');
t.searchParams.set('cacheBust', Date.now().toString());
```

`fetch()` cross-origin exige **CORS**. O uStreamer **não envia** `Access-Control-Allow-Origin`, e
como o Fluidd é servido na porta **80** e o stream estava na **8080**, origens diferentes ⇒ o worker
falha e o cartão mostra `(error)`.

Medido:

```
GET :8080/?action=stream  →  200, multipart/x-mixed-replace
                            (sem cabeçalho Access-Control-Allow-Origin)
```

## 3. Solução — mesma origem via nginx

O nginx já serve o Fluidd na porta 80. Basta um `location` que encaminhe `/webcam/` ao uStreamer,
de modo que navegador e stream fiquem na **mesma origem**:

```nginx
location /webcam/ {
    proxy_pass http://127.0.0.1:8080/;
    proxy_http_version 1.0;
    proxy_set_header Host $host;
    proxy_buffering off;
    proxy_read_timeout 3600s;
}
```

Arquivo completo versionado em [`nginx-fluidd.conf`](nginx-fluidd.conf).

> `proxy_pass` com barra final reescreve `/webcam/?action=stream` → `/?action=stream`.
> `proxy_buffering off` é obrigatório para MJPEG — sem isso o nginx acumula os quadros e o vídeo
> congela.

## 4. Verificação

```bash
nginx -t && systemctl reload nginx
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" \
     "http://192.168.10.126/webcam/?action=stream"
# esperado: 200 multipart/x-mixed-replace
```

Depois, **recarregar o Fluidd com `Ctrl+Shift+R`** — o app carrega a lista de câmeras uma única vez,
ao abrir a página.

## 5. Histórico

| Data | Evento |
|---|---|
| 2026-07 | tentativa com `camera-streamer` (compilado sem libav; falhou) |
| 2026-10-31 | uStreamer adotado; câmera no Fluidd via proxy `/webcam/` (mesma origem) |
