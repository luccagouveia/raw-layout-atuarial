# app/src/pipeline/ingest_raw_layout_atuarial.py

import os
from app.src.parsers.filename_parser import FilenameParser, FilenamePadraoInvalido
from app.src.parsers.csv_reader import CsvReader, CsvVazio
from app.src.raw.schema import get_headers
from app.src.raw.record_builder import RecordBuilder, ErroRecordBuilder
from app.src.mysql.raw_layout_atuarial_repository import RawLayoutAtuarialRepository
from app.src.observability.logger import get_logger

logger = get_logger(__name__)


class IngestRawLayoutAtuarial:
    """
    Pipeline de ingestão RAW dos layouts atuariais.
    """

    def __init__(self, mysql_connection):
        self.mysql_connection = mysql_connection
        self.csv_reader = CsvReader()

    def executar(self, caminho_competencia: str, competencia: str):
        """
        Executa a ingestão para uma pasta de competência (AAAAMM).
        """

        logger.info(f"Iniciando ingestão | competencia={competencia}")
        logger.info(f"Caminho base: {caminho_competencia}")

        arquivos = [
            f for f in os.listdir(caminho_competencia)
            if f.upper().endswith(".CSV")
        ]

        if not arquivos:
            logger.warning("Nenhum arquivo CSV encontrado")
            return

        repository = RawLayoutAtuarialRepository(self.mysql_connection)

        for nome_arquivo in arquivos:
            caminho_arquivo = os.path.join(caminho_competencia, nome_arquivo)

            # =========================
            # 1. Ignorar arquivo vazio
            # =========================
            try:
                if self.csv_reader.is_empty(caminho_arquivo):
                    logger.warning(f"Arquivo vazio ignorado: {nome_arquivo}")
                    continue
            except OSError as e:
                logger.error(f"Erro ao acessar arquivo {nome_arquivo}: {e}")
                continue

            # =========================
            # 2. Parse do nome do arquivo
            # =========================
            try:
                metadata = FilenameParser.parse(nome_arquivo)
            except FilenamePadraoInvalido as e:
                logger.error(e)
                continue

            situacao = metadata["situacao"]
            metadata["layout_versao"] = 1

            # =========================
            # 3. Resolver tabela destino
            # =========================
            if situacao == "SERVIDOR":
                tabela_destino = "layout_atuarial_servidor"
            elif situacao == "APOSENTADO":
                tabela_destino = "layout_atuarial_aposentados"
            elif situacao == "PENSIONISTA":
                tabela_destino = "layout_atuarial_pensionista"
            else:
                logger.warning(f"Situação não suportada ainda: {situacao}")
                continue

            logger.info(
                f"Processando arquivo | {nome_arquivo} "
                f"| situacao={situacao} | tabela={tabela_destino}"
            )

            # =========================
            # 4. Obter headers (schema)
            # =========================
            try:
                headers = get_headers(situacao)
            except Exception as e:
                logger.error(e)
                continue

            # =========================
            # 5. Ler CSV e persistir
            # =========================
            try:
                for linha in self.csv_reader.read(caminho_arquivo):
                    try:
                        registro = RecordBuilder.build(
                            linha_csv=linha,
                            headers=headers,
                            metadata=metadata,
                            competencia=competencia,
                            nome_arquivo=nome_arquivo
                        )

                        repository.upsert(
                            tabela=tabela_destino,
                            registro=registro
                        )

                    except ErroRecordBuilder as e:
                        logger.error(
                            f"Erro ao construir registro | arquivo={nome_arquivo} | erro={e}"
                        )
                        continue

            except CsvVazio:
                logger.warning(f"Arquivo vazio ignorado: {nome_arquivo}")
                continue

        logger.info(f"Ingestão finalizada | competencia={competencia}")
