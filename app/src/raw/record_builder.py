# app/src/raw/record_builder.py

from app.src.raw.hasher import gerar_hash


class ErroRecordBuilder(Exception):
    pass


class RecordBuilder:
    """
    Constrói um registro RAW a partir de uma linha de CSV + metadados.
    """

    @staticmethod
    def build(
        linha_csv: list,
        headers: list,
        metadata: dict,
        competencia: str,
        nome_arquivo: str
    ) -> dict:
        """
        Retorna um dicionário pronto para persistência no MySQL.
        """

        # =========================
        # 1. Validação básica
        # =========================
        if len(linha_csv) != len(headers):
            raise ErroRecordBuilder(
                f"Quantidade de colunas ({len(linha_csv)}) "
                f"diferente do esperado ({len(headers)})"
            )

        # =========================
        # 2. Montar payload JSON
        # =========================
        payload = dict(zip(headers, linha_csv))

        # =========================
        # 3. Extrair matrícula
        # =========================
        situacao = metadata["situacao"]

        if situacao == "SERVIDOR":
            matricula = payload.get("ID_SERVIDOR_MATRICULA")

        elif situacao == "APOSENTADO":
            matricula = payload.get("ID_APOSENTADO_MATRICULA")

        elif situacao == "PENSIONISTA":
            matricula = payload.get("ID_PENSIONISTA_MATRICULA")

        else:
            raise ErroRecordBuilder(
                f"Situação não suportada no RecordBuilder: {situacao}"
            )

        if not matricula:
            raise ErroRecordBuilder(
                "Matrícula não encontrada no payload"
            )

        # =========================
        # 4. Montar registro RAW
        # =========================
        registro = {
            "ano_mes_competencia": competencia,
            "matricula": str(matricula),
            "situacao": situacao,
            "orgao": metadata["orgao"],
            "ano_mes_inicio": metadata["ano_mes_inicio"],
            "ano_mes_fim": metadata["ano_mes_fim"],
            "nome_arquivo_origem": nome_arquivo,
            "layout_versao": metadata.get("layout_versao", 1),
            "payload_json": payload
        }

        # =========================
        # 5. Gerar hash determinístico
        # =========================
        registro["hash_registro"] = gerar_hash(registro)

        return registro