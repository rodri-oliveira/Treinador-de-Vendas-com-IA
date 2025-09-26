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
- Fase atual: documentação e planejamento do pipeline.
- Próximo passo: definir schema SQLite e iniciar ingestão/transcrição (CPU-only).

## Contribuição
- Padrões de contribuição e commits: [`docs/contributing.md`](./docs/contributing.md) e [`docs/commit_conventions.md`](./docs/commit_conventions.md)

## Licença
- Definir licença na fase de publicação (WIP).
