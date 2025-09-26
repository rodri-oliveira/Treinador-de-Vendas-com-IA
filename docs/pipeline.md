# Pipeline de Processamento

## Estágios
1. Ingestão: áudios + metadados (CSV) em `data/raw/`
2. Transcrição: faster-whisper (pt-BR, VAD, INT8), cache por hash
3. Limpeza/Anonimização: regex de PII, pseudonimização
4. Features:
   - Prosódia: pitch, energia, ritmo, pausas
   - Linguística: embeddings, keyphrases, n-grams, métricas de pergunta/CTA/objeção
5. Descoberta de padrões: clusterização (KMeans) + UMAP p/ visualização
6. Modelos por produto: logística/árvore; explicabilidade (coef./SHAP)
7. Recomendações: gaps vs. perfil top performer e drivers do modelo
8. Dashboard: Streamlit

## Entradas/Saídas por estágio
- Definidas em arquivos individuais e registradas em `audit_logs`.
