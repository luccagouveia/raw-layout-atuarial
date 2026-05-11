# app/src/mysql/raw_layout_atuarial_repository.py

from typing import Dict
from app.src.observability.logger import get_logger

logger = get_logger(__name__)


class RawLayoutAtuarialRepository:
    """
    Repository para carga RAW atuarial (incremental).
    """

    def __init__(self, connection):
        self.connection = connection

    def upsert(self, tabela: str, registro: Dict):
        """
        INSERT / UPDATE / IGNORE baseado em hash_registro.
        """

        sql = f"""
        INSERT INTO {tabela} (
            ano_mes_competencia,
            matricula,
            situacao,
            orgao,
            ano_mes_inicio,
            ano_mes_fim,
            nome_arquivo_origem,
            layout_versao,
            payload_json,
            hash_registro
        )
        VALUES (
            %(ano_mes_competencia)s,
            %(matricula)s,
            %(situacao)s,
            %(orgao)s,
            %(ano_mes_inicio)s,
            %(ano_mes_fim)s,
            %(nome_arquivo_origem)s,
            %(layout_versao)s,
            %(payload_json)s,
            %(hash_registro)s
        )
        ON DUPLICATE KEY UPDATE
            payload_json = IF(hash_registro <> VALUES(hash_registro), VALUES(payload_json), payload_json),
            hash_registro = IF(hash_registro <> VALUES(hash_registro), VALUES(hash_registro), hash_registro),
            nome_arquivo_origem = IF(hash_registro <> VALUES(hash_registro), VALUES(nome_arquivo_origem), nome_arquivo_origem),
            layout_versao = IF(hash_registro <> VALUES(hash_registro), VALUES(layout_versao), layout_versao)
        ;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(sql, registro)

        self.connection.commit()

        logger.debug(
            f"Upsert executado | tabela={tabela} | "
            f"competencia={registro['ano_mes_competencia']} | "
            f"matricula={registro['matricula']} | "
            f"situacao={registro['situacao']}"
        )
