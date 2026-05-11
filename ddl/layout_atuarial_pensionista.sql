CREATE TABLE layout_atuarial_pensionista (
    id_layout_atuarial_pensionista BIGINT AUTO_INCREMENT PRIMARY KEY,

    /* =========================
       CHAVE NATURAL
       ========================= */
    ano_mes_competencia CHAR(6) NOT NULL COMMENT 'Competência no formato YYYYMM',
    matricula           VARCHAR(50) NOT NULL COMMENT 'RF + Vínculo do pensionista',
    situacao            VARCHAR(30) NOT NULL COMMENT 'Situação (PENSIONISTA)',

    /* =========================
       METADADOS DO ARQUIVO
       ========================= */
    orgao                VARCHAR(100) NOT NULL COMMENT 'Órgão de origem do arquivo',
    ano_mes_inicio       CHAR(6) NOT NULL COMMENT 'Início do período do arquivo',
    ano_mes_fim          CHAR(6) NOT NULL COMMENT 'Fim do período do arquivo',
    nome_arquivo_origem  VARCHAR(255) NOT NULL COMMENT 'Nome do arquivo CSV de origem',

    /* =========================
       IDENTIFICAÇÃO DO LAYOUT
       ========================= */
    layout_versao        INT NOT NULL DEFAULT 1 COMMENT 'Versão do layout vigente na competência',

    /* =========================
       DADOS DO PENSIONISTA (RAW)
       ========================= */
    payload_json         JSON NOT NULL COMMENT 'Conteúdo bruto conforme dicionário PENSIONISTAS',

    /* =========================
       CONTROLE TÉCNICO
       ========================= */
    hash_registro        CHAR(64) NOT NULL COMMENT 'Hash do conteúdo relevante',
    dt_carga             DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data/hora da carga',

    /* =========================
       CONSTRAINTS
       ========================= */
    CONSTRAINT uk_layout_atuarial_pensionista
        UNIQUE (
            ano_mes_competencia,
            matricula,
            situacao
        ),

    /* =========================
       ÍNDICES AUXILIARES
       ========================= */
    INDEX idx_competencia (ano_mes_competencia),
    INDEX idx_matricula (matricula),
    INDEX idx_situacao (situacao)

)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COMMENT='RAW atuarial - Pensionistas (1 linha por vínculo por competência)';