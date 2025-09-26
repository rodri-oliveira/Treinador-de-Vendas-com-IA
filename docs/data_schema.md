# Esquema de Dados (SQLite)

## Tabelas
- `products(id, nome, kpis_json, created_at)`
- `datasets(id, product_id, version, periodo_inicio, periodo_fim, created_at)`
- `interactions(id, product_id, dataset_id, vendor_id, lead_id, canal, iniciou_em, duracao_s, resultado, valor)`
- `transcripts(interaction_id, idioma, modelo_whisper, texto_limpo, texto_hash, created_at)`
- `transcript_segments(interaction_id, idx, start_s, end_s, texto_segmento)`
- `features(id, entity_type, entity_id, product_id, dataset_id, feature_key, feature_value, created_at)`
- `clusters(id, product_id, dataset_id, level, n_clusters, label, silhouette, descricao, created_at)`
- `models(id, product_id, dataset_id, version, tipo_modelo, params_json, metrics_json, path_artifact, created_at)`
- `recommendations(id, target_type, target_id, product_id, dataset_id, titulo, descricao, prioridade, origem, created_at)`
- `audit_logs(id, evento, detalhe_json, created_at)`

## Diretrizes
- Artefatos binários (embeddings `.npy`, modelos `.pkl`) armazenados no disco e referenciados por caminho.
- Integridade via chaves estrangeiras e constraints simples.
