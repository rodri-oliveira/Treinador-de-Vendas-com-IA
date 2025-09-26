# Treino por Produto (Versionamento)

## Conceitos
- `product_id`: contexto de negócio
- `dataset_version`: snapshot dos dados usados no treino
- `model_version`: artefatos e métricas associadas

## Fluxo
1. Selecionar produto e período → criar `dataset_version`
2. Extrair/atualizar features deste dataset
3. Treinar modelos (logística/árvore)
4. Registrar métricas e artefatos (`models`)
5. Publicar versão para geração de recomendações
6. Possibilidade de rollback para versão anterior

## Configuração por produto
- KPIs, lexicon de domínio, limiares, idioma
