# app/src/main.py

import sys
from app.src.config.settings import (
    PATH_ARQUIVOS_ATUARIAIS
)
from app.src.source.competencia import resolver_competencia_mais_recente
from app.src.mysql.connection import get_mysql_connection
from app.src.pipeline.ingest_raw_layout_atuarial import IngestRawLayoutAtuarial
from app.src.observability.logger import get_logger

logger = get_logger(__name__)


def main():
    logger.info("==============================================")
    logger.info("Iniciando microsserviço RAW Layout Atuarial")
    logger.info("==============================================")

    try:
        # =========================
        # 1. Resolver competência
        # =========================
        caminho_competencia, competencia = resolver_competencia_mais_recente(
            PATH_ARQUIVOS_ATUARIAIS
        )

        logger.info(f"Competência resolvida: {competencia}")
        logger.info(f"Caminho da competência: {caminho_competencia}")

        # =========================
        # 2. Conectar ao MySQL
        # =========================
        mysql_connection = get_mysql_connection()
        logger.info("Conexão com MySQL estabelecida")

        # =========================
        # 3. Executar pipeline
        # =========================
        pipeline = IngestRawLayoutAtuarial(mysql_connection)
        pipeline.executar(
            caminho_competencia=caminho_competencia,
            competencia=competencia
        )

        logger.info("Pipeline executado com sucesso")

    except Exception as e:
        logger.exception(f"Erro fatal na execução do microsserviço: {e}")
        sys.exit(1)

    finally:
        try:
            mysql_connection.close()
            logger.info("Conexão MySQL encerrada")
        except Exception:
            pass

    logger.info("==============================================")
    logger.info("Execução finalizada")
    logger.info("==============================================")


if __name__ == "__main__":
    main()