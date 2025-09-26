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
