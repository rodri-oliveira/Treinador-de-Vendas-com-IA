# Arquitetura

## Objetivo
Pipeline modular CPU-only, custo zero, para analisar áudio e texto, descobrir padrões por produto e gerar recomendações acionáveis.

## Diagrama (alto nível)
```mermaid
flowchart LR
  A[data/raw/audio] --> B[Transcrição: faster-whisper]
  B --> C1[Texto limpo/anonimizado]
  B --> C2[Segmentos + timestamps]
  C2 --> D1[Prosódia: librosa/parselmouth]
  C1 --> D2[Linguística: embeddings + keyphrases]
  D1 --> E[Feature Store (SQLite + npy)]
  D2 --> E
  E --> F1[Clusterização (descoberta de estilos)]
  E --> F2[Modelos explicáveis por produto]
  F1 --> G[Clusters com maior conversão]
  F2 --> G
  G --> H[Feedback por vendedor]
  H --> I[Dashboard (Streamlit)]
```

## Decisões de tecnologia
- Transcrição: `faster-whisper` (pt-BR, VAD, INT8)
- Prosódia: `librosa` (e `parselmouth` opcional)
- NLP: `sentence-transformers`, `KeyBERT`, `scikit-learn`, `umap-learn`
- Banco: SQLite + artefatos em disco (`.npy`, `.pkl`)
- UI: Streamlit (local)
- LGPD: anonimização por regex + pseudonimização; audit trail

## Arquitetura em camadas (Clean/Hexagonal simplificada)

Regra de dependência: camadas externas dependem das internas; domínio não depende de nada externo.

```mermaid
flowchart LR
  subgraph Interfaces
    UI[Next.js (frontend)]
    API[FastAPI (REST)]
    CLI[CLI]
  end

  subgraph Application
    UC[Use Cases]
    Ports[Ports (interfaces)]
  end

  subgraph Domain
    Entities[Entidades/VOs]
    Rules[Serviços de Domínio]
    Repos[Repositórios (interfaces)]
  end

  subgraph Infrastructure
    Adapters[Whisper, Librosa, Sklearn, SQLite, JWT]
  end

  UI --> API
  API --> UC
  CLI --> UC
  UC --> Entities
  UC --> Rules
  UC --> Ports
  UC --> Repos
  Adapters --> Ports
  Adapters --> Repos
```

### Mapeamento em pastas (MVP)
- `src/domain/`: entidades, value objects, serviços de domínio, repositórios (interfaces)
- `src/application/`: casos de uso, portas (interfaces), DTOs/validators
- `src/infrastructure/`: adapters (transcrição, features, NLP, ML, persistência, segurança)
- `src/interfaces/`: API (FastAPI), UI (Streamlit/Next.js integração), CLI

## Frontend (Next.js)
- Next.js com TypeScript (App Router), Tailwind CSS, shadcn/ui, TanStack Query
- Autenticação: NextAuth (Credentials) integrando com FastAPI (JWT httpOnly)
- Consome endpoints REST do FastAPI; futuro: pode evoluir para React completo sem quebrar domínio

## Backend (FastAPI)
- Endpoints REST seguindo casos de uso (Application) e contratos do domínio
- Autenticação JWT (bcrypt para hash de senha; tokens com expiração)
- SQLite como armazenamento local; artefatos em disco

## Containers (Docker Compose)
- Serviços:
  - `api`: FastAPI (Uvicorn) porta 8000
  - `web`: Next.js (dev) porta 3000
- Volumes para hot-reload e dados: `./src -> /app/src`, `./data -> /app/data`, `./frontend -> /app`
- Variáveis de ambiente via `.env` (não commitar segredos)
- Rede `app_net` para comunicação interna

### Desenvolvimento (dev)
- `docker compose up --build` sobe API e Web
- Logs por serviço: `docker compose logs -f api` | `web`
- Derrubar: `docker compose down`

### Produção (posterior)
- API com `gunicorn`/`uvicorn.workers.UvicornWorker`, sem reload
- Next.js com `next build` + `next start` ou Nginx para estáticos
- Secrets por variáveis seguras; healthchecks
