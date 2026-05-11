# app/src/raw/hasher.py

import hashlib
import json


def gerar_hash(registro: dict) -> str:
    """
    Gera hash determinístico excluindo campos voláteis.
    """

    registro_hash = {
        k: v for k, v in registro.items()
        if k not in ("hash_registro", "dt_carga")
    }

    payload = json.dumps(
        registro_hash,
        sort_keys=True,
        ensure_ascii=False
    )

    return hashlib.sha256(payload.encode("utf-8")).hexdigest()