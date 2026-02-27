import os
import pytest

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
def _connection_string():
    driver = os.getenv("ODBC_DRIVER", "ODBC Driver 17 for SQL Server")
    server = os.getenv("DB_SERVER", r"DESKTOP-5FSTOOH\SQLEXPRESS")
    db_name = os.getenv("DB_NAME", "ALITAS EL COMELON SF")
    user = os.getenv("DB_USER", "sa")
    password = os.getenv("DB_PASSWORD", "kevin190305")
    trust = os.getenv("DB_TRUST_CERT", "yes")

    return (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={db_name};"
        f"UID={user};"
        f"PWD={password};"
        f"TrustServerCertificate={trust};"
    )


def _db_esta_encendida():
    try:
        import pyodbc
        conn = pyodbc.connect(_connection_string(), timeout=2)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        row = cur.fetchone()
        conn.close()
        return bool(row) and row[0] == 1
    except Exception:
        return False


@pytest.fixture(autouse=True)
def _skip_si_bd_apagada_para_tests_mssql(request):
    if request.node.get_closest_marker("mssql"):
        if not _db_esta_encendida():
            pytest.skip(
                "SQL Server apagado o configuración faltante: se omiten tests marcados como mssql."
            )
