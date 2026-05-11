# app/src/parsers/filename_parser.py

import re


class FilenamePadraoInvalido(Exception):
    pass


class FilenameParser:
    """
    Parser de nomes de arquivos atuariais PRODAM.

    Exemplo esperado:
    SERVIDOR_2026_04_a_2026_04_IPREM.CSV
    APOSENTADOS_2026_04_a_2026_04_IPREM_APOSENTADOS.CSV
    """

    # Regex central do padrão
    _PATTERN = re.compile(
        r"""
        ^(?P<situacao>[A-Z_]+)_
        (?P<ano_ini>\d{4})_(?P<mes_ini>\d{2})_a_
        (?P<ano_fim>\d{4})_(?P<mes_fim>\d{2})_
        (?P<orgao>[A-Z_]+)
        \.CSV$
        """,
        re.VERBOSE
    )

    @classmethod
    def parse(cls, filename: str) -> dict:
        """
        Faz o parsing do nome do arquivo e devolve os metadados.
        """

        filename_upper = filename.upper()

        match = cls._PATTERN.match(filename_upper)

        if not match:
            raise FilenamePadraoInvalido(
                f"Nome de arquivo fora do padrão esperado: {filename}"
            )

        situacao_raw = match.group("situacao")
        orgao = match.group("orgao")

        ano_mes_inicio = (
            match.group("ano_ini") + match.group("mes_ini")
        )
        ano_mes_fim = (
            match.group("ano_fim") + match.group("mes_fim")
        )

        situacao = cls._normalizar_situacao(situacao_raw)

        return {
            "situacao": situacao,
            "orgao": orgao,
            "ano_mes_inicio": ano_mes_inicio,
            "ano_mes_fim": ano_mes_fim
        }

    @staticmethod
    def _normalizar_situacao(situacao_raw: str) -> str:
        """
        Normaliza a situação para os valores usados no pipeline.
        """

        # Base atual
        if situacao_raw.startswith("SERVIDOR"):
            return "SERVIDOR"

        if situacao_raw.startswith("APOSENTADOS"):
            return "APOSENTADO"

        if situacao_raw.startswith("PENSIONISTA"):
            return "PENSIONISTA"

        # Preparação para o futuro (_FALEC)
        if "FALEC" in situacao_raw:
            return situacao_raw

        raise FilenamePadraoInvalido(
            f"Situação não reconhecida no nome do arquivo: {situacao_raw}"
        )