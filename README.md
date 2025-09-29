# Treinador de Vendas com IA — MVP

Este repositório contém o MVP de um sistema que identifica padrões comportamentais (voz/prosódia) e linguísticos (texto) que levam à conversão em vendas, treinável por produto, com custo zero e execução local (CPU-only).

## Documentação
Toda a documentação detalhada está em `docs/`.
- Visão geral e índice: [`docs/README.md`](./docs/README.md)
- Arquitetura: [`docs/architecture.md`](./docs/architecture.md)
- Pipeline: [`docs/pipeline.md`](./docs/pipeline.md)
- Esquema de dados: [`docs/data_schema.md`](./docs/data_schema.md)
- LGPD/Privacidade: [`docs/privacy_lgpd.md`](./docs/privacy_lgpd.md)
- Roadmap: [`docs/roadmap.md`](./docs/roadmap.md)

## Estrutura do repositório
```
Treinador de Vendas com IA/
├─ docs/
│  ├─ README.md
│  ├─ architecture.md
│  ├─ pipeline.md
│  ├─ data_schema.md
│  ├─ ...
├─ data/               # dados locais (ignorado no git)
├─ models/             # artefatos de modelos (ignorado no git)
├─ embeddings/         # vetores/embeddings (ignorado no git)
├─ artifacts/          # artefatos auxiliares (ignorado no git)
├─ logs/               # logs locais (ignorado no git)
├─ .gitignore
└─ README.md           # este arquivo
```

## Status
- Transcrição por Whisper (faster-whisper) integrada no endpoint `POST /transcriptions/upload`.
- Extração de prosódia (librosa) disponível em `POST /prosody/extract` e opcional no upload de transcrição via `include_prosody=true`.
- Execução local (venv) e suporte a Docker Compose.

## Visão de Produto: Plano Futuro (exemplo e direção)

Esta seção descreve o que este MVP pode se tornar. É um guia direcional, não um compromisso fechado. O objetivo é evoluir para um Treinador de Vendas que:

- Aprende com casos de sucesso (top performers) e extrai padrões de linguagem e prosódia.
- Gera feedbacks práticos para quem está abaixo da meta, reduzindo o gap de performance.

### Exemplo 10–30–60 (apenas ilustrativo)
- ~10%: acima da média de conversão com consistência.
- ~30%: atingem a meta regularmente.
- ~60%: abaixo da meta — foco do treinador.

O sistema aprende o que funciona com os 10–30% e aplica feedbacks nos 60% para elevar conversão. Este é um exemplo de segmentação, ajustável conforme o contexto.

### Próximas etapas de “análise rica”
- Diarização (quem falou o quê) para contextualizar trechos.
- Sentimento/emoção por trecho.
- Detecção de tópicos/intenções/objeções.
- Coaching com LLM (agente) para insights e recomendações acionáveis.

### Como integrar sem quebrar o core (Arquitetura Hexagonal)
- Novas Ports (ex.: `ICoachAgent`, `IEmotionClassifier`, `IDiarization`).
- Novos Adapters que implementam essas Ports (LLM, Pyannote, HuggingFace etc.).
- Domínio e casos de uso permanecem estáveis; apenas plugamos os adapters.

### Métricas sugeridas
- Negócio: lift de conversão dos 60% após feedbacks.
- Adoção: % de recomendações aplicadas.
- Qualidade: avaliação humana dos insights.
- Operacional: latência (`*_ms`) e custo por análise (quando houver LLM).

## Contribuição
- Padrões de contribuição e commits: [`docs/contributing.md`](./docs/contributing.md) e [`docs/commit_conventions.md`](./docs/commit_conventions.md)

## Licença
- Definir licença na fase de publicação (WIP).

---

## Como rodar (local, venv)

1) Python 3.11+ e venv ativo:
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Variáveis de ambiente (opcional, com defaults seguros):
```
WHISPER_MODEL=small
WHISPER_COMPUTE_TYPE=int8
WHISPER_LANGUAGE=pt
TMP_AUDIO_DIR=./data/tmp
MAX_UPLOAD_MB=50
```

3) Subir API (FastAPI + Uvicorn):
```
python -m uvicorn src.interfaces.api.main:app --reload --port 8000
```

4) Swagger UI: http://127.0.0.1:8000/docs

## Como rodar (Docker Compose)

Após editar `.env` na raiz:
```
docker compose build api
docker compose up api
```

## Endpoints principais

- `GET /health`
  - Retorna `{ "status": "ok" }`.

- `POST /transcriptions/upload`
  - multipart/form-data com `file`
  - Query param opcional: `include_prosody=true`
  - Retorna `TranscriptResponse` (tipado) com:
    - `model`, `language`, `text`, `segments`
    - `transcription_ms`
    - `prosody` e `prosody_ms` quando `include_prosody=true`
  - Header: `X-Process-Time-ms` com tempo total da requisição.

Exemplo (PowerShell):
```
curl.exe --noproxy "*" -s -S "http://127.0.0.1:8000/transcriptions/upload?include_prosody=true" -F "file=@C:/Windows/Media/Alarm02.wav;type=audio/wav" | python -m json.tool
```

- `POST /prosody/extract`
  - multipart/form-data com `file`
  - Retorna `ProsodyResponse` com `duration_s`, `rms_*`, `zcr_*` e `f0_*` (atual MVP mantém `f0_*` como `null`).
  - Header: `X-Process-Time-ms`.

## Configuração (variáveis de ambiente)

- `WHISPER_MODEL` (default: `small`) — qualidade vs. custo. Use `tiny` em máquinas fracas.
- `WHISPER_COMPUTE_TYPE` (default: `int8`) — CPU-friendly.
- `WHISPER_LANGUAGE` (default: `pt`).
- `WHISPER_BEAM_SIZE` (default: `1`) — trade-off qualidade x velocidade.
- `TMP_AUDIO_DIR` (default: sistema) — diretório onde os uploads são salvos temporariamente.
- `MAX_UPLOAD_MB` (default: `50`) — limite de tamanho do arquivo de upload.

## Notas de performance

- O modelo Whisper é carregado apenas uma vez (singleton no router) para reduzir latência.
- A prosódia usa `librosa` em 16kHz mono (CPU). F0 está desativado no MVP por custo; pode ser habilitado futuramente (`pyin`).
