# app/src/parsers/csv_reader.py

import csv
import os


class CsvVazio(Exception):
    pass


class CsvReader:
    """
    Leitor de CSV sem header para arquivos atuariais PRODAM.
    """

    def __init__(
        self,
        delimiter: str = ",",
        encoding: str = "latin-1"
    ):
        self.delimiter = delimiter
        self.encoding = encoding

    def is_empty(self, file_path: str) -> bool:
        """
        Verifica se o arquivo está vazio ou só contém espaços.
        """
        return os.path.getsize(file_path) == 0

    def read(self, file_path: str):
        """
        Itera sobre as linhas do CSV (sem header).
        Retorna listas de strings.
        """

        if self.is_empty(file_path):
            raise CsvVazio(f"Arquivo CSV vazio: {file_path}")

        with open(
            file_path,
            mode="r",
            encoding=self.encoding,
            newline=""
        ) as csvfile:

            reader = csv.reader(
                csvfile,
                delimiter=self.delimiter
            )

            for row in reader:
                # ignora linhas completamente vazias
                if not row or all(col.strip() == "" for col in row):
                    continue

                yield row
