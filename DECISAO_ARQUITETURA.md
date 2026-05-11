# Decisão de Arquitetura – raw_layout_atuarial (decisões técnicas e justificativas)

## 1. Contexto

O serviço `raw_layout_atuarial` foi criado para ingerir arquivos atuariais provenientes da PRODAM, com múltiplas situações, layouts distintos e possibilidade de evolução futura sem impacto nos dados históricos.

---

## 2. Uma tabela RAW por situação

### Decisão
Criar **uma tabela por situação**, em vez de uma tabela genérica.

### Justificativa
- Cada situação possui layout próprio
- Evita campos nulos e ambiguidade semântica
- Facilita auditoria e troubleshooting
- Mantém consistência com o padrão RAW existente

---

## 3. Chave natural

### Decisão
Utilizar:
    ano_mes_competencia + matricula + situacao

### Justificativa
- A matrícula é composta por RF + vínculo
- Mudança de vínculo gera nova matrícula
- Falecimentos são diferenciados pela situação
- Permite carga histórica e reprocessamento seguro

---

## 4. Controle incremental por hash

### Decisão
Aplicar hash determinístico ao conteúdo relevante do registro.

### Justificativa
- Evita duplicidade
- Permite UPDATE apenas quando o conteúdo muda
- Garante idempotência do pipeline

---

## 5. CSV sem header

### Decisão
Aplicar os nomes dos campos no pipeline, não no banco.

### Justificativa
- O MySQL não deve inferir estrutura
- O schema deve ser controlado pelo código
- Permite versionamento de layout por competência

---

## 6. Merge por situação no pipeline

### Decisão
Realizar o merge lógico de arquivos por situação durante a ingestão.

### Justificativa
- Arquivos diferem apenas por órgão
- Evita staging físico
- Simplifica o fluxo e mantém rastreabilidade

---

## 7. Evolução futura

- Inclusão de layouts *_FALEC
- Alterações de layout versionadas por competência
- Possibilidade de carga histórica fora da maior competência

---

## 8. Conclusão

A arquitetura adotada privilegia:
- simplicidade
- rastreabilidade
- segurança de dados
- evolução sem quebra do histórico

