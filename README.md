# raw_layout_atuarial

Microsserviço de ingestão **RAW** responsável por carregar **arquivos atuariais** provenientes da rede PRODAM para o MySQL, seguindo o padrão incremental.

---

## Objetivo

- Ler arquivos `.CSV` localizados na rede PRODAM
- Identificar automaticamente a **maior competência disponível**
- Fazer o **merge lógico de arquivos por situação**
- Enriquecer os dados com metadados técnicos
- Persistir os registros em tabelas RAW no MySQL com:
  - chave natural
  - hash de conteúdo
  - controle incremental (INSERT / UPDATE / IGNORE)

---

## Fonte dos dados

Caminho base:
    \xx.xx.xx.xx\Arquivos_Atuariais

Estrutura esperada:

    ANO/
    └── AAAAMM.zip/
    └── AAAAMM/
    ├── SERVIDOR_.CSV
    ├── APOSENTADOS_.CSV
    └── PENSIONISTA_*.CSV

---

## Tabelas de destino (MySQL)

Uma tabela RAW por situação:

- `layout_atuarial_servidor`
- `layout_atuarial_aposentados`
- `layout_atuarial_pensionista`

Cada tabela possui chave natural:
    ano_mes_competencia + matricula + situacao

---

## Funcionamento do pipeline

1. Resolve a **maior competência**
2. Lista arquivos CSV da competência
3. Ignora arquivos vazios
4. Faz parsing do nome do arquivo
5. Aplica schema conforme a situação
6. Constrói registro RAW
7. Persiste no MySQL com controle incremental

---

##  Execução

```bash
python app/src/main.py

Observações

Arquivos CSV não possuem header
Os nomes dos campos são aplicados no pipeline via schema_registry
Alterações futuras de layout devem ser versionadas por competência
Layouts *_FALEC serão tratados em evolução futura