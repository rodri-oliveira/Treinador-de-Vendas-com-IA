# Módulo de Áudio

## Padrões e Configuração
- Formatos aceitos: wav, mp3, m4a (normalização interna opcional para wav)
- Idioma: pt-BR forçado (quando aplicável)
- Modelo: faster-whisper `small` INT8; `base` como alternativa; VAD ligado
- Batching: fila por arquivo; paralelismo moderado conforme CPU
- Cache: por hash do arquivo para evitar reprocessamento

## Saídas
- Transcrição por interação (texto limpo + hash)
- Segmentos com timestamps (para alinhar prosódia)

## Considerações de performance
- CPU-only; estimar tempo ~0.3–1.0x tempo real dependendo do hardware
