# LGPD, Privacidade e Segurança

## Princípios
- Anonimização de PII (regex: e-mail, telefone, CPF/CNPJ, endereços)
- Pseudonimização de nomes (consistente)
- Minimização de dados (armazenar apenas o necessário; hash do texto original)
- Consentimento e finalidade específica
- Audit trail em `audit_logs`

## Riscos e Mitigações
- Vazamento de PII → anonimização automática + revisão amostral
- Acesso não autorizado → separar `data/raw/` de `data/processed/`
- Retenção → políticas de limpeza por produto/período
