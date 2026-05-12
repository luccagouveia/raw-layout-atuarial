# app/src/main.py

import sys
from .config.settings import PATH_ARQUIVOS_ATUARIAIS
from .source.competencia import resolver_competencia_mais_recente
from .observability.logger import get_logger

logger = get_logger(__name__)


def main():
    logger.info("==============================================")
    logger.info("Iniciando microsserviço RAW Layout Atuarial")
    logger.info("==============================================")

    caminho_competencia, competencia = resolver_competencia_mais_recente(
        PATH_ARQUIVOS_ATUARIAIS
    )

    logger.info(f"Competência resolvida: {competencia}")
    logger.info(f"Caminho da competência: {caminho_competencia}")

    # Bootstrap OK — resto vem depois
    return


if __name__ == "__main__":
    main()